
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SignalInfos(models.Model):
    '''
    信号信息
    '''
    _name = 'metro_park.interlock.signal_infos'
    _description = '信号信息'
    _track_log = True

    route_id = fields.Many2one(string="所属进路",
                               comodel_name="metro_park.interlock.route",
                               ondelete="cascade")
    signal = fields.Many2one(string='信号机',
                             comodel_name='metro_park_base.signals')
    indicator = fields.Char(string='指示器')
    display = fields.Char(string='显示')

