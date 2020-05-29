
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HostileSignalInfo(models.Model):
    '''
    敌对信号机信息
    '''
    _name = 'metro_park.interlock.hostile_signal_info'
    _description = '敌对信号机信息'
    _track_log = True

    route_id = fields.Many2one(comodel_name="metro_park.interlock.route",
                               string="进路")

    condition_switches = fields.One2many(string='条件道岔',
                                         comodel_name="metro_park.interlock.condition_switches_info",
                                         inverse_name="hostile_id")
    signal = fields.Many2one(string='信号机',
                             comodel_name='metro_park_base.signals')
