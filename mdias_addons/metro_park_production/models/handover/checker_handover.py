# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class CheckerHandover(models.Model):
    _name = 'metro_park_production.handover.checker'
    _inherit = ['metro_park_production.handover.abstract']
    _track_log = True
    _HANDOVER_TYPE = 'checker'

    date = fields.Date('时间', default=datetime.date.today())

    # 生产类交班
    production_succession_content = fields.Text(string='交班内容')
    production_succession_per = fields.Many2one('res.users', string='交办人')
    production_succession_date = fields.Date(string='交办时间')
    production_single_phase = fields.Char(string='单期')
    production_progress = fields.Char(string='当班进展')
    production_flight_schedule = fields.Char(string='班次安排')
    production_note = fields.Char(string='备注')
    production_location = fields.Many2one("metro_park_base.location", string='场段')

    # 扣车情况统计表
    button_vehicle_unit = fields.Char(string='扣车单位')
    button_vehicle_number = fields.Many2one('metro_park_maintenance.train_dev', string='列车编号')
    button_vehicle_reason = fields.Char(string='扣车原因')
    button_vehicle_time = fields.Text(string='扣车时间')
    button_vehicle_note = fields.Text(string='备注')
    button_vehicle_location = fields.Many2one("metro_park_base.location", string='场段')

    # 专项安排
    special_arrangement_content = fields.Text(string='交办内容')
    special_arrangement_per = fields.Many2one('res.users', string='交办人')
    special_arrangement_date = fields.Date(string='时间')
    special_arrangement_progress = fields.Char(string='进展')

    # 施工类交办
    construction_content = fields.Text(string='交班内容')
    construction_per = fields.Many2one('res.users', string='交办人')
    construction_date = fields.Date(string='时间')
    construction_single_phase = fields.Char(string='单期')
    construction_progress = fields.Char(string='当班进展')
    construction_flight_schedule = fields.Char(string='班次安排')
    construction_note = fields.Char(string='备注')
    construction_location = fields.Many2one("metro_park_base.location", string='场段')

    # 10号线近期专项梳理
    comb_notice_no = fields.Char(string='通知号')
    comb_notice_name = fields.Char(string='通知名称')
    comb_notice_person = fields.Char(string='编制者')
    comb_notice_system = fields.Char(string='系统')
    comb_notice_limit = fields.Char(string='整改范围')
    comb_notice_date = fields.Date(string='下发时间')
    comb_notice_type = fields.Selection([('普查', '普查'), ('专项', '专项'), ('整改', '整改')], string='通知类型')
    comb_notice_complete = fields.Selection([('是', '是'), ('否', '否')], string='是否完成', dafault='否')
    comb_notice_conditions_work = fields.Char(string='是否具备作业条件')
    comb_notice_start_time = fields.Char(string='预计开始作业时间')
    comb_notice_plan = fields.Char(string='排产计划')

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
