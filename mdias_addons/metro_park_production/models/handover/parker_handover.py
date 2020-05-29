# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class ParkerHandover(models.Model):
    _name = 'metro_park_production.handover.parker'
    _track_log = True
    _HANDOVER_TYPE = 'parker'

    _inherit = ['metro_park_production.handover.abstract']

    #  交班现车情况
    date = fields.Date('交接日期', default=fields.Date.context_today)
    handover_type = fields.Selection([('day', '白班'), ('night', '夜班')], string='交接班类型', default='day')
    # 时刻表
    today_time_table_id = fields.Many2one(string="当日运行图",
                                          comodel_name="metro_park_base.time_table",
                                          required=True)
    next_day_time_table_id = fields.Many2one(string="次日运行图",
                                             comodel_name="metro_park_base.time_table",
                                             required=True)
    radio_800 = fields.Char(string='800兆电台')
    radio_400 = fields.Char(string='400兆电台')
    equipment_situation = fields.Char(string='设备情况')
    spares_situation = fields.Char(string='备品情况')
    track_condition = fields.One2many('metro_park_production.handover.track_condition', 'handover_work_info_id',
                                      string='交班现车情况')

    # 生产任务完成情况 接发车作业
    back_train_number = fields.Integer(string='接车')
    out_train_number = fields.Integer(string='发车')
    spares_train_number = fields.Integer(string='备用车加开')

    # 调洗车作业
    shunting_number = fields.Integer(string='调车辆数')
    shunting_hook_number = fields.Integer(string='调车钩数')
    shunting_column_number = fields.Integer(string='调车列数')
    wash_column_number = fields.Integer(string='洗车列数')

    # 停送电作业
    power_outages_number = fields.Integer(string='停电次数')
    sending_power_number = fields.Integer(string='送电次数')

    # 施工作业完成情况 计划施工
    construction_click_number = fields.Integer(string='请点数量')
    construction_destruction_number = fields.Integer(string='销点数量')

    # 巡检、巡道
    patrol_click_number = fields.Integer(string='请点数量')
    patrol_destruction_number = fields.Integer(string='销点数量')

    # 抢修
    repair_click_number = fields.Integer(string='请点数量')
    repair_destruction_number = fields.Integer(string='销点数量')

    # 施工异常数
    construction_anomalies_number = fields.Char(string='施工异常数')

    # 调试
    trunk_line_debug = fields.Integer(string='正线调试')
    test_line_debug = fields.Integer(string='试车线调试')
    train_validation = fields.Integer(string='车辆验证')
    signal_verification = fields.Integer(string='验证信号')

    # 出退勤作业
    flights_number = fields.Integer(string='出勤机班数')
    departures_number = fields.Integer(string='退勤机班数')

    # 备品借用登记栏
    spare_goods_borrowing_register = fields.One2many('metro_park_production.handover.spare_goods_borrowing',
                                                     'borrow_rec', string='备品借用登记栏')

    # 设备故障/抢修记录栏
    equipment_break_or_repair_rec = fields.One2many('metro_park_production.handover.equipment_break_repair',
                                                    'repair_rec', string='设备故障/抢修记录栏')

    # 停送电情况栏
    power_outage_status_bar = fields.One2many('metro_park_production.handover.power_outage_status_bar',
                                              'outage_status_rec', string='停送电情况栏')

    # 调度命令登记栏
    scheduling_command_registration = fields.One2many('metro_park_production.handover.scheduling_command',
                                                      'scheduling_command_rec', string='调度命令登记栏')

    # 记事栏
    note_bar = fields.One2many('metro_park_production.handover.content_bar',
                               'note_rec', string='记事栏')

    # 交接事项栏
    content_bar = fields.One2many('metro_park_production.handover.content_bar',
                                  'content_rec', string='交接事项栏')

    handover_work_info_id = fields.Many2one('metro_park_production.handover.work_info')
    track_condition = fields.Many2one('metro_park_production.handover.track_condition')

    search_handover_sign_user = fields.Char(string='交班人', compute='_search_handover_sign_user')
    search_accept_user = fields.Char(string='接班人', compute='_search_accept_user')

    @api.one
    @api.depends('handover_sign_user')
    def _search_handover_sign_user(self):
        self.search_handover_sign_user = self.handover_sign_user.name

    @api.one
    @api.depends('accept_user')
    def _search_accept_user(self):
        self.search_handover_sign_user = self.accept_user.name


class SpareGoodsBorrowingRegister(models.Model):
    _name = 'metro_park_production.handover.spare_goods_borrowing'
    _description = '备品借用登记栏'

    borrow_time = fields.Datetime(string='借用时间', required=True)
    goods_name_number = fields.Char(string='物品名称及数量', required=True)
    borrow_depart_person = fields.Char(string='借用部门/人', required=True)
    return_time = fields.Datetime(string='归还时间')
    return_person = fields.Char(string='归还人')
    note = fields.Text(string='备注')
    borrow_rec = fields.Many2one('metro_park_production.handover.parker')

    @api.multi
    def delete_rec(self):
        self.unlink()


class EquipmentBreakOrRepairRec(models.Model):
    _name = 'metro_park_production.handover.equipment_break_repair'
    _description = '设备故障/抢修记录栏'

    break_time = fields.Datetime(string='故障时间', required=True)
    break_number = fields.Char(string='故障编码')
    report_position_or_name = fields.Char(string='填报人职务姓名', required=True)
    transfer_discovery_time = fields.Char(string='故障接报/发现时间')
    break_site = fields.Char(string='故障地点')
    break_des = fields.Text(string='故障现象')
    fault_specialty = fields.Char(string='故障所属专业')
    notice_time = fields.Datetime(string='通知时间')
    notice_department = fields.Char(string='通知单位')
    accept_department = fields.Char(string='接收人')
    reply_date = fields.Datetime(string='回复时间')
    break_reason = fields.Char(string='故障原因')
    deal_results = fields.Char(string='处理结果')
    reply_per = fields.Char(string='回复人')
    note = fields.Char(string='备注')
    repair_rec = fields.Many2one('metro_park_production.handover.parker')

    @api.multi
    def delete_rec(self):
        self.unlink()


class PowerOutAgeStatusBar(models.Model):
    _name = 'metro_park_production.handover.power_outage_status_bar'
    _description = '停送电情况栏'

    power_outages_time = fields.Datetime(string='停电时间', required=True)
    outages_command_number = fields.Char(string='命令号码')
    equity_channel_area = fields.Char(string='股道/区域')
    ground_conditions = fields.Char(string='地线情况')
    sending_time = fields.Datetime(string='送电时间')
    sending_command_number = fields.Char(string='命令号码')
    note = fields.Char(string='备注')
    outage_status_rec = fields.Many2one('metro_park_production.handover.parker')

    @api.multi
    def delete_rec(self):
        self.unlink()


class SchedulingCommandRegistration(models.Model):
    _name = 'metro_park_production.handover.scheduling_command'
    _description = '调度命令登记栏'

    instruction_time = fields.Datetime(string='受令时分', required=True)
    command_number = fields.Char(string='命令号码')
    instruction_name = fields.Char(string='发令人姓名', required=True)
    instruction_site = fields.Char(string='受令处所')
    instruction_note = fields.Char(string='命令内容')
    scheduling_command_rec = fields.Many2one('metro_park_production.handover.parker')

    @api.multi
    def delete_rec(self):
        self.unlink()


class ContentBar(models.Model):
    _name = 'metro_park_production.handover.content_bar'
    _description = '记录内容'

    content = fields.Text(string='内容', required=True)
    note_rec = fields.Many2one('metro_park_production.handover.parker')
    content_rec = fields.Many2one('metro_park_production.handover.parker')

    @api.multi
    def delete_rec(self):
        self.unlink()
