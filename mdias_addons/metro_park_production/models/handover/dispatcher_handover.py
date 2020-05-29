# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SignalerHandover(models.Model):
    _name = 'metro_park_production.handover.dispatcher'
    _inherit = ['metro_park_production.handover.abstract']
    _track_log = True
    _HANDOVER_TYPE = 'dispatcher'

    handover_type = fields.Selection([('day', '白班'), ('night', '夜班')], string='交接班类型', default='day')

    line_execute_diagram = fields.Many2one(comodel_name='metro_park_base.time_table', string='正线运行图')

    # 800兆电台
    eight_hundred_radio_total = fields.Integer("总数")
    eight_hundred_radio_give = fields.Integer("交班数量")
    eight_hundred_radio_accept = fields.Integer("接班数量")
    # 400兆电台
    four_hundred_radio_total = fields.Integer("总数")
    four_hundred_radio_give = fields.Integer("交班数量")
    four_hundred_radio_accept = fields.Integer("接班数量")
    # 钥匙
    key_total = fields.Integer("总数")
    key_give = fields.Integer("交班数量")
    key_accept = fields.Integer("接班数量")
    # 雨伞
    umbrella_total = fields.Integer("总数")
    umbrella_give = fields.Integer("交班数量")
    umbrella_accept = fields.Integer("接班数量")

    # 其他备品
    other_equipment = fields.Char("其他备品")
    # 酒测
    test_person_num = fields.Integer("应测人数")
    actual_test_person_num = fields.Integer("实测人数")
    # 调试/施工人员计划
    nun_person_plan = fields.Char("调试/施工人员计划")
    # 人员情况
    sick_leave_num = fields.Integer("病假人数")
    compassionate_leave_num = fields.Integer("事假人数")
    annual_leave_num = fields.Integer("年休假人数")
    handover_num = fields.Integer("换班人数")
    break_off_num = fields.Integer("调休人数")
    marriage_leave_num = fields.Integer("婚假人数")
    funeral_leave_num = fields.Integer("丧假人数")
    nursing_leave_num = fields.Integer("护理假人数")
    num_person_learning = fields.Integer('学习人数')
    num_other_learning = fields.Integer('其他人数')
    # 其他交班事宜
    handover_other = fields.Text("其他交班事宜")

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
