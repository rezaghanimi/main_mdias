# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
import base64
import xlrd
import pendulum


class TrainDev(models.Model):
    '''
    车辆设备, 说明，由于初期设计原因，多了一堆的废弃字段
    '''
    _name = 'metro_park_maintenance.train_dev'

    _description = '车辆设备'
    _rec_name = 'dev_name'
    _track_log = True

    dev_name = fields.Char(string='设备名称', required=True)
    dev_no = fields.Char(string='设备编码', required=True)
    batch_no = fields.Many2one('metro_park_maintenance.dev_batch', string='批次号')
    # 上次修程
    repair_offset = fields.Integer(string="均衡修规程修次")
    major = fields.Many2one('metro_park_base.major', string='所属专业')

    # 下边三个具有级联关系
    location = fields.Many2one('metro_park_base.location', required=True, string='位置')
    location_detail = fields.Char(string="位置补充说明")

    location_rail_sec = fields.Many2one('metro_park_base.rails_sec', string='当前股道')
    import_type = fields.Selection(selection=[('manual', '手动'), ('auto', '自动')],
                                   default="auto",
                                   string='增加方式')
    line = fields.Many2one(comodel_name='metro_park_base.line',
                           string='线别',
                           required=True)
    line_seg = fields.Many2one(comodel_name='metro_park_base.line_segment', string='线段')

    pms_id = fields.Char(string='纪录id', help="pms记录id")
    major_type = fields.Many2one("metro_park_base.major_type", string="专业系统")
    dev_type = fields.Many2one('metro_park_base.dev_type', string='设备类型')
    standard = fields.Many2one("metro_park_base.dev_standard", string='型号规格')
    unit = fields.Char(string='单位', default='辆')

    # 暂时单独放置
    res_code = fields.Char(string='资产代码')
    res_name = fields.Char(string='资产名称')
    res_type = fields.Char(string="资产类别")
    brand = fields.Char(string='品牌')
    install_area = fields.Char(string='安装区域')
    dev_status = fields.Selection(
        [('using', '使用中'),
         ('free', '未使用')],
        string='设备状态',
        default='free')
    out_no = fields.Char(string="出厂编号")
    contract_no = fields.Char(string='合同号')

    responsible_person = fields.Many2one(comodel_name='funenc.wechat.user', string='责任人')
    owner_department = fields.Many2one(comodel_name='funenc.wechat.department', string='使用权单位')
    maintenance_department = fields.Many2one(comodel_name='funenc.wechat.department', string='维护单位')

    import_user = fields.Many2one('funenc.wechat.user', string='录入人员', readonly=True)
    start_use_time = fields.Date(string="运营日期")
    end_use_time = fields.Date(string="结束日期")

    miles = fields.Float(string="设备公里数", default=0.00, compute="_compute_miles")

    remark = fields.Text(string='备注')
    dev_qty = fields.Float(string='数量')

    measure_unit = fields.Many2one('metro_park_base.dev_unit', string='计量单位')
    traction_energy = fields.Float(string='牵引能耗')
    traction_unit = fields.Char(string='单位', default='KWh')
    renewable_energy = fields.Float(string='再生能耗')
    renewable_unit = fields.Char(string='单位', default='KWh')
    auxiliary_energy = fields.Float(string='辅助能耗')
    auxiliary_unit = fields.Char(string='单位', default='KWh')
    object_code = fields.Char(string='PMS来源的')
    mat_code = fields.Char(string='PMS传入物资编码')
    file = fields.Binary(string='导入文件')

    display_color = fields.Char(string="公里数显示颜色", compute="_compute_mile_color")

    # 里程检公里数单独配置
    repair_mile = fields.Integer(string="里程修公里数", default=2900)
    repair_mile_negative_offset = fields.Integer(string="负向公里数", default=600)
    repair_mile_positive_offset = fields.Integer(string='正向公里数', default=600)

    last_repair_miles = fields.Float(string="上次里程检公里数",
                                     default=0,
                                     compute="_compute_last_repair_info",
                                     help="里程检完成以后公里数")
    last_mile_repair_date = fields.Date(string="上次里程检日期",
                                        compute="_compute_last_repair_info")

    miles_after_last_repair = fields.Float(string="里程检后的公里数",
                                           compute="_compute_miles_after_last_repair")

    cur_train_id = fields.Many2one(comodel_name="metro_park_dispatch.cur_train_manage",
                                   string="现车", compute='_compute_cur_train')
    cur_location = fields.Many2one(string='当前车辆位置', comodel_name='metro_park_base.location',
                                   compute="_compute_cur_train")
    operation_btns = fields.Char(string="操作")

    _sql_constraints = [('dev_name_unique', 'UNIQUE(dev_name, location)', "同一位置名称不能重复!")]

    @api.model
    def sync_manual_miles(self):
        """
        点击手工同步按钮后执行的动作
        :return:
        """
        # 获取tcms配置参数,并判断使用哪种工具进行同步
        config = self.env['metro_park_base.system_config'].search([], limit=1)
        if config and config.tcms_synchronize_tool == 'api':
            return self.env['tcms.tcms'].get_train_info(sync_miles=True)
        return self.env['funenc.tcms.vehicle.data'].start_pull_vehicle_data()

    @api.model
    def create_train_dev_form(self):
        form_id = self.env.ref("metro_park_maintenance.train_dev_form").id
        return {
            'name': '车辆设备信息创建',
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': 'metro_park_maintenance.train_dev',
            'target': 'new',
        }

    @api.model
    def import_train_dev_form(self):
        form_id = self.env.ref("metro_park_maintenance.train_dev_form_import").id
        return {
            'name': '车辆设备信息导入',
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': 'metro_park_maintenance.repair_tmp_rule_import',
            'target': 'new',
        }

    @api.model
    def train_dev_excel_download(self):
        return {
            'name': '车辆设备导入模板下载',
            'type': 'ir.actions.act_url',
            'url': '/GetTrainDevImportExcel'
        }

    @api.multi
    def import_train_dev(self):
        '''
        导入设备
        :return:
        '''
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)
        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        vals = []
        for row in range(1, sheet.nrows):
            data = sheet.row_values(row)
            batch_no = self.env['metro_park_maintenance.dev_batch'].search(
                [('batch_no', '=', int(data[2]))])
            if not batch_no:
                raise ValidationError('%s的批次号不存在' % int(data[0]))
            major = self.env['metro_park_base.major'].search([('name', '=', data[3])])
            if not major:
                raise ValidationError('%s的所属专业不存在' % int(data[0]))
            location = self.env['metro_park_base.location'].search([('name', '=', data[4])])
            if not location:
                raise ValidationError('%s的位置不存在' % int(data[0]))
            line = self.env['metro_park_base.line'].search([('name', '=', data[5])])
            if not line:
                raise ValidationError('%s的线别不存在' % int(data[0]))
            line_seg = self.env['metro_park_base.line_segment'].search([('name', '=', data[6])])
            if not line_seg:
                raise ValidationError('%s的线段不存在' % int(data[0]))
            dev_type = self.env['metro_park_base.dev_type'].search([('name', '=', data[7])])
            if not dev_type:
                raise ValidationError('%s的设备类型不存在' % int(data[0]))
            standard = self.env['metro_park_base.dev_standard'].search([('name', '=', data[8])])
            if not standard:
                raise ValidationError('%s的型号规格不存在' % int(data[0]))
            vals.append({
                'dev_name': int(data[0]),
                'dev_no': data[1],
                'batch_no': batch_no.id,
                'major': major.id,
                'location': location.id,
                'line': line.id,
                'line_seg': line_seg.id,
                'dev_type': dev_type.id,
                'standard': standard.id,
                'res_name': data[9]
            })
        self.env['metro_park_maintenance.train_dev'].create(vals)

    @api.depends('miles_after_last_repair',
                 'repair_mile',
                 'repair_mile_negative_offset',
                 'repair_mile_positive_offset')
    def _compute_mile_color(self):
        '''
        计算公里数显示颜色, 正常显示绿色，范围内显示黄色，超出显示红色
        :return:
        '''
        for record in self:
            le_mile = record.repair_mile - record.repair_mile_negative_offset
            ge_mile = record.repair_mile + record.repair_mile_positive_offset
            if record.miles_after_last_repair < le_mile:
                record.display_color = 'green'
            elif le_mile < record.miles_after_last_repair < ge_mile:
                record.display_color = 'yellow'
            else:
                record.display_color = 'red'

    @api.depends("miles", "last_repair_miles")
    def _compute_miles_after_last_repair(self):
        '''
        计算距离上次里程公里数
        :return:
        '''
        for record in self:
            record.miles_after_last_repair = record.miles - record.last_repair_miles

    @api.depends()
    def _compute_cur_train(self):
        '''
        计算关联的现车
        :return:
        '''
        cur_trains = self.env["metro_park_dispatch.cur_train_manage"].search([])
        cur_train_cahce = {cur_train.train.id: cur_train for cur_train in cur_trains}
        for record in self:
            if record.id in cur_train_cahce:
                record.cur_train_id = cur_train_cahce[record.id].id
                record.cur_location = cur_train_cahce[record.id].cur_location

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        '''
        重写，添加的时候要同步添加现车
        :param vals_list:
        :return:
        '''
        record = super(TrainDev, self).create(vals_list)
        val = {
            'train': record.id,
            'train_status': 'wait',
            'old_status': 'wait',
        }

        # 同步到现车
        self.env['metro_park_dispatch.cur_train_manage'].create([val])

        # 同步到历史公里数
        today = pendulum.today()
        self.env['metro_park_maintenance.history_miles'].check_dev(
            today.year, today.month)

        return record

    @api.multi
    def train_dev_history(self):
        """
        打开指定列表行- 跳转所属车辆历史里程界面
        :return:
        """
        for res in self:
            dev_name = res.dev_name
            tree_id = self.env.ref(
                'metro_park_maintenance.view_designated_vehicle_data_tree').id
            return {
                "type": "ir.actions.act_window",
                "view_mode": "tree",
                "res_model": "funenc.tcms.vehicle.data",
                "name": "车辆历史公里数",
                "views": [[tree_id, "tree"]],
                "domain": [("name", "=", dev_name)],
                "target": "new",
            }

    @api.model
    def open_vehicle_data_action(self):
        """
        跳转到历史车辆公里数列表
        :return:
        """
        tree_id = self.env.ref(
            'metro_park_maintenance.view_funenc_tcms_vehicle_data_tree').id
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "funenc.tcms.vehicle.data",
            "name": "车辆历史公里数",
            "views": [[tree_id, "tree"]],
        }

    @api.depends()
    def _compute_last_repair_info(self):
        '''
        计算上次里程修信息， 线别中去实现此函数
        :return:
        '''
        pass

    @api.depends()
    def _compute_miles(self):
        '''
        计算里程数, 根据历史记录计算里程数
        :return:
        '''
        today_str = pendulum.today('UTC').format('YYYY-MM-DD')
        mile_infos = self.env['funenc.tcms.vehicle.data'].get_miles_by_date(today_str)
        for record in self:
            if record.dev_no in mile_infos:
                record.miles = mile_infos[record.dev_no]

    @api.multi
    def view_history_miles(self):
        '''
        查看历史公里数
        :return:
        '''
        dev_name = self.dev_name
        tree_id = self.env.ref(
            'metro_park_maintenance.view_designated_vehicle_data_tree').id
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "funenc.tcms.vehicle.data",
            "name": "车辆历史公里数",
            "views": [[tree_id, "tree"]],
            "domain": [("name", "=", dev_name)],
            "target": "new",
        }
