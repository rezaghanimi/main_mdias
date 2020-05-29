
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class Location(models.Model):
    '''
    位置管理
    '''
    _name = 'metro_park_base.location'

    _description = '位置, 位置是一个抽象的概念，这个按类型可以分成车站、站间区间和车辆段、车场'
    _track_log = True

    name = fields.Char(string='位置名称', required=True)
    alias = fields.Char(string="别名")
    rtu_id = fields.Char(string="场段号")

    line = fields.Many2one(string='线别',
                           comodel_name='metro_park_base.line',
                           required=True)
    line_code = fields.Char(string='线别代码',
                            related='line.code')
    location_type = fields.Many2one(string='位置类型',
                                    comodel_name='metro_park_base.location_type',
                                    required=True)
    location_code = fields.Char(string='位置编码')

    location_map = fields.Many2one(string='位置图',
                                   comodel_name='metro_park_base.park_map')

    # 站场图数据
    location_map_data = fields.Binary(string='位置图数据',
                                      related="location_map.xml")
    rail_secs = fields.One2many(string='区段',
                                comodel_name="metro_park_base.rails_sec",
                                inverse_name="location")

    electric_areas = fields.One2many(string='供电分区',
                                     comodel_name='metro_park_base.electric_area',
                                     inverse_name='location_id')

    is_active = fields.Boolean(string='状态', default='True')

    # 是否是车场
    location_type_show = fields.Boolean(string='是否是车场',
                                        help='控制字段显示隐藏')
    park_btns = fields.One2many(string="按扭表",
                                comodel_name="metro_park_base.btn_table",
                                inverse_name="location")

    electric_area_btn = fields.Char(
        string="供电分区", help="供点分区按扭暂位，可以通过widget替换")

    work_class = fields.Many2many(string="检修工班",
                                  comodel_name="funenc.wechat.department",
                                  relation="location_work_class_rel",
                                  column1="location_id",
                                  column2="department_id")

    @api.model
    def default_deal_method(self):
        return self.env.ref("metro_park_base.selection_nothing", raise_if_not_found=False).id

    temp_train_back_deal_method = \
        fields.Many2one(comodel_name="metro_park_base.selections",
                        domain="[('value', 'in', ['nothing', 'auto', 'user_select'])]",
                        default=default_deal_method,
                        string="临时收车处理方式")

    receive_train_need_min = fields.Integer(string="收车需求时间", default="5", required=True)
    send_train_pre_min = fields.Integer(string="出库提间时间", default="5", required=True)
    plan_rail_pre_min = fields.Integer(string="排进路提前时间", default="2", required=True)

    max_repair_after_high_run = fields.Integer(string="高峰车最大检修数量", default=2, help="每日每个地点高峰车最大数量")
    max_repair_back_time = fields.Char(string="最大返回时间", default='16:00', help='检修最近返回时间，登顶等作业')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', " 线别名称不能重复"),
                        ('alias_unique', 'UNIQUE(alias)', "别名不能重复")]

    @api.model
    def get_special_rails(self, location_id, rail_property):
        '''
        取得带有特殊属生的轨道
        :return:
        '''
        location = self.browse(location_id)
        rail_ids = location.rail_secs.ids
        rail_model = self.env['metro_park_base.rails_sec']
        records = rail_model.search([('id', 'in', rail_ids),
                                     ('rail_property', 'in', rail_property)])
        return records

    @api.model
    def get_work_area_rails(self, location_id, work_area):
        '''
        取得作业区域的轨道
        :return:
        '''
        rail_model = self.env['metro_park_base.rails_sec']
        records = rail_model.search([('work_area', '=', work_area), ("location", "=", location_id)])
        return records

    @api.onchange('location_type')
    def _set_location_type_show(self):
        self.ensure_one()
        if self.location_type and self.location_type.name == '车场':
            self.location_type_show = True
        else:
            self.location_type_show = False

    @api.onchange('line')
    def _onchange_line_seg(self):
        line_segs = self.env['metro_park_base.line_segment']\
            .search([('line_id', '=', self.line.id)])
        if len(line_segs) == 1:
            self.line_seg = line_segs.id
        else:
            self.line_seg = False
        return {
            'domain': {'line_seg': [('line_id', '=', self.line.id)]},
        }

    @api.model
    def get_location_by_name(self, name):
        '''
        根据位置取得名称
        :param name:
        :return:
        '''
        record = self.search(['name', '=', name])
        record.ensure_one()
        return record.read()[0]

    @api.model
    def get_btn_tables(self, location):
        '''
        取得按扭表
        :return:
        '''
        record = self.browse(location)
        if record.park_btns:
            return json.loads(record.park_btns)
        else:
            return {}

    @api.multi
    def open_electric_area(self):
        '''
        查看供电分区
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "tag": "electric_area",
            "context": {
                "location_id": self.id
            }
        }

    @api.multi
    def get_location_alias(self):
        '''
        取得位置别名
        :return:
        '''
        self.ensure_one()
        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        if self.id == location_banqiao:
            return "banqiao"
        elif self.id == location_gaodalu:
            return "gaodalu"

    @api.multi
    def get_train_test_rail_num(self):
        '''
        取得试车线的条数
        :return:
        '''
        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        if self.id == location_banqiao:
            return 1
        elif self.id == location_gaodalu:
            return 0

        return 0

    @api.multi
    def get_platform_count(self):
        '''
        取得登顶平台的数量
        :return:
        '''
        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        if self.id == location_banqiao:
            return 4
        elif self.id == location_gaodalu:
            return 2

        return 0
