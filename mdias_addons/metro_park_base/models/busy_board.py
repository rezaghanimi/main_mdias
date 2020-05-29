
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class BusyBoard(models.Model):
    '''
    占线板信息
    '''
    _name = 'metro_park_base.busy_board'

    icons = fields.Char(string='占线板')
    rail = fields.Many2one(string='轨道', comodel_name='metro_park_base.rails_sec')
    switch = fields.Many2one(string='道岔', comodel_name='metro_park_base.switches')
    uid = fields.Char(string="场段uid", compute='_compute_uid')

    @api.depends('rail', 'switch')
    def _compute_uid(self):
        '''
        计算uid
        :return:
        '''
        for record in self:
            if record.rail:
                record.uid = record.rail.no
            elif record.switch:
                record.uid = record.switch.name

    @api.model
    def set_busy_icon_status(self, uid, location_alias, operation, busy_types):
        '''
        设置轨道占线板信息
        :return:
        '''
        raise exceptions.Warning('没有实现set_busy_icon_status, 请在线别中去实此函数!')


