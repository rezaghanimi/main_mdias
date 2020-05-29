# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import pendulum
from odoo.exceptions import ValidationError
import requests
import logging

_logger = logging.getLogger(__name__)


class RepairRule(models.Model):
    '''
    检修修程设定, 检修规程实质上就是检修的规则
    '''
    _name = 'metro_park_maintenance.repair_rule'
    _rec_name = 'name'

    _description = '修程设定'
    _track_log = True

    dev_standard = fields.Many2one(string='车辆型号',
                                   comodel_name="metro_park_base.dev_standard",
                                   help="针对于某个型号的车型",
                                   ondelete="restrict")

    name = fields.Char(string='修程名称', copy=False)
    no = fields.Char(string='修程代码', copy=False)

    # 由于均衡修比较特殊, 用户区分
    balance = fields.Selection(string="均衡修",
                               selection=[('yes', '是'), ('no', '否')], default='no')
    priority = fields.Integer(string='优先级', default="0")
    rule_type = fields.Selection(selection=[('plan', '计划'),
                                            ('mile', '里程'),
                                            ('temp', '临时'),
                                            ('run', "运营")],
                                 string='修程类型',
                                 default='plan',
                                 required=True,
                                 help="计划针对检修")

    target_plan_type = fields.Selection(selection=[
        ('year', '年'),
        ('month', '月'),
        ('week', '周'),
        ('day', '日')],
        string="目标计划类型",
        help="只针对计划检修")

    period = fields.Integer(string='周期天数',
                            required=True,
                            help="周期指的是中间的间隔天数，不算上自身，所以计算next day的时候要加1")
    # 正向偏差天数
    positive_offset = fields.Integer(string='最晚不超过', required=True)
    # 反向偏差天数
    negative_offset = fields.Integer(string='最早不超过', required=True)

    # 只针对里程检有效
    run_miles = fields.Float(string='运行里程', default="0")
    positive_offset_miles = fields.Float(string='正向偏差里程', default="0")
    negative_offset_miles = fields.Float(string='负向偏差里程', default="0")

    repair_days = fields.Integer(string='检修天数', required=True)
    plan_method = fields.Selection(string='排程方式',
                                   selection=[('auto', '自动'),
                                              ('manual', '手动')],
                                   default='auto',
                                   required=True)

    cycle_type = fields.Selection(string="循环方式",
                                  selection=[('miles', '里程'),
                                             ('day', '天数'),
                                             ('miles_and_day', '里程天数结合')],
                                  default='day')

    rule_status = fields.Selection(string='状态',
                                   selection=[('normal', '正常'),
                                              ('disable', '禁用')],
                                   default='enable',
                                   required=True)

    work_class = fields.Many2many(string="作业工班",
                                  comodel_name="funenc.wechat.department",
                                  relation="rule_and_work_class_rel",
                                  column1="rule_id",
                                  column2="work_class_id",
                                  help="哪些工班可以进行这个修程")
    # PMS工班
    pms_department = fields.Many2one('pms.department', string='PMS工班')

    # 最多能排多少项
    max_plan_per_day = fields.Integer(string="单日数量(最大)",
                                      defaut=9999,
                                      help="用于辅助计划排列, 仅周计划时考虑!")\

    min_plan_per_day = fields.Integer(string="单日最小数量")

    nax_plan_per_weekend_day = fields.Integer(string="周未数量(最大)",
                                              default=9999,
                                              help="用于区分周未和平日")

    min_plan_per_weekend_day = fields.Integer(string="周未最大数量",
                                              default=-1,
                                              help="用于周计算")

    # 可以覆盖的修程
    overlap_rules = fields.Many2many(string='覆盖修程',
                                     comodel_name='metro_park_maintenance.repair_rule',
                                     relation="repair_duration_overlap_rel",
                                     column1="this_id",
                                     column2="that_id")

    combine_rules = fields.Many2many(string='结合修程',
                                     comodel_name='metro_park_maintenance.repair_rule',
                                     relation="repair_duration_overlap_rel",
                                     column1="this_id",
                                     column2="that_id", compute="_compute_combine_rules")

    # 这里针对每天的开始时间和结束时间, 用于具体的日计划
    work_start_time = fields.Datetime(string='开始时间')

    # 用于排计划, 这个时间只是个大概时间
    work_start_val = fields.Integer(string='开始时间(分钟)',
                                    compute="_compute_work_val")
    work_end_time = fields.Datetime(string='结束时间')

    # 用于排计划, 这个时间只是个大概时间
    work_end_val = fields.Integer(string="结束时间(分钟)",
                                  compute="_compute_work_val")

    # D2 D4 需要上试车线，10号线只能在板桥进行
    need_train_test = fields.Boolean(string="试车线", default=False)

    # 分钟数, 说明，没有什么特别意义
    work_consume_time = \
        fields.Integer(string='作业耗时',
                       default=2,
                       help="这个是用户手动填写, 开始时间和结束时间只是当天的一个检修时间范围")

    # 检修的具体内容
    repair_content = fields.Text(string='作业内容')

    def get_location_domain(self):
        '''
        取得位置domain
        :return:
        '''
        location_type_park = self.env.ref('metro_park_base.location_type_park').id
        return [('location_type', '=', location_type_park)]

    # 多个作业场段
    locations = fields.Many2many(string='作业场段',
                                 comodel_name='metro_park_base.location',
                                 domain="[('location_type.name', '=', '车场')]",
                                 relation="repair_config_locations_rel",
                                 column1="repair_id",
                                 column2="location_id",
                                 required=True)
    # 轨道属性要求
    work_requirement = fields.Many2many(string='段内作业需求',
                                        comodel_name='metro_park_base.rail_property',
                                        relation='repair_rule_and_property_rel',
                                        column1='rule_id',
                                        column2='property_id',
                                        help="登高、地沟等要求")

    # 是否需要扣车, 要扣车的话就不能参与运营
    need_retain = fields.Boolean(string='是否扣车', default=False, required=True)

    # 修程名称可以重复
    _sql_constraints = [('constrain_name', 'UNIQUE(name)', "名称不能重复"),
                        ('constrain_no', 'UNIQUE(no)', "修程代号不能重复")]

    @api.constrains('work_start_time', 'work_end_time')
    def check_times(self):
        '''
        检查时间
        :return:
        '''
        if self.work_start_time >= self.work_end_time:
            raise ValidationError('开始时间必须小于结束时间！')

    @api.depends('work_start_time', 'work_end_time')
    def _compute_work_val(self):
        '''
        计算工作时间
        :return:
        '''
        for record in self:
            start = pendulum.parse(str(record.work_start_time))
            end = pendulum.parse(str(record.work_end_time))

            if start.hour < 2:
                record.work_start_val = (start.hour + 24) * 60 + start.minute
            else:
                record.work_start_val = start.hour * 60 + start.minute

            if end.hour < 2:
                record.work_end_val = (end.hour + 24) * 60 + end.minute
            else:
                record.work_end_val = end.hour * 60 + end.minute

    @api.model
    def init_rule_department(self):
        '''
        初始化检修工班, 这个放在数据配置里面
        :return:
        '''
        pass

    @api.depends('overlap_rules')
    def _compute_combine_rules(self):
        '''
        结合
        :return:
        '''
        pass

    @api.multi
    def unlink(self):
        lis = []
        for delete_data in self:
            data = {
                "sourceSystemId": "10MDIAS{}".format(delete_data.id),
                "repairingTimeId": delete_data.id,
                "dataType": 3,
                "vehicleModel": delete_data.dev_standard.name,
                "repaireTypeName": delete_data.name,
                "repaireCode": delete_data.no
            }
            lis.append(data)

        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)

        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().repairing_information(data)
        except Exception as e:
            _logger.info('PMS接口修程设定删除' + str(e))
        res = super(RepairRule, self).unlink()
        return res

    @api.model
    def create(self, vals_list):
        res = super(RepairRule, self).create(vals_list)
        data = {
            "sourceSystemId": "10MDIAS{}".format(res.id),
            "repairingTimeId": res.id,
            "dataType": 1,
            "vehicleModel": res.dev_standard.name,
            "repaireTypeName": res.name,
            "repaireCode": res.no
        }

        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)

        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().repairing_information(data)
        except Exception as e:
            _logger.info('PMS接口修程设定创建' + str(e))
        return res

    @api.multi
    def write(self, vals):
        '''
        重写，写入的时候发送给pms
        :param vals:
        :return:
        '''
        res = super(RepairRule, self).write(vals)
        data = {
            "sourceSystemId": "10MDIAS{}".format(self.id),
            "repairingTimeId": self.id,
            "dataType": 2,
            "vehicleModel": self.dev_standard.name,
            "repaireTypeName": self.name,
            "repaireCode": self.no
        }

        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)
        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().repairing_information(data)
        except Exception as e:
            _logger.info('PMS接口修程设定修改' + str(e))

        return res
