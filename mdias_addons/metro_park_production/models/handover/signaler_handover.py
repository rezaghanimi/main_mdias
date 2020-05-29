# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SignalerHandover(models.Model):
    _name = 'metro_park_production.handover.signaler'
    _track_log = True
    _HANDOVER_TYPE = 'signaler'

    _inherit = ['metro_park_production.handover.abstract']
    _inherits = {'metro_park_production.handover.work_info': 'handover_work_info_id'}
    handover_work_info_id = fields.Many2one('metro_park_production.handover.work_info')

    handover_type = fields.Selection([('day', '白班'), ('night', '夜班')], string='交接班类型', default='day')

    clean_condition = fields.Text('卫生情况')
    zone_run_train = fields.Text('段内现车')

    search_handover_sign_user = fields.Char(string='交班人', compute='_search_handover_sign_user')
    search_accept_user = fields.Char(string='接班人', compute='_search_accept_user')
    back_train_number = fields.Integer(string='接车')
    out_train_number = fields.Integer(string='发车')
    add_train_number = fields.Integer(string='加开')
    handover_date = fields.Datetime('交接班时间')

    @api.one
    @api.depends('handover_sign_user')
    def _search_handover_sign_user(self):
        self.search_handover_sign_user = self.handover_sign_user.name

    @api.one
    @api.depends('accept_user')
    def _search_accept_user(self):
        self.search_handover_sign_user = self.accept_user.name
