
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConditionSwitchsInfo(models.Model):
    '''
    敌对信号条件道岔信息
    '''
    _name = 'metro_park.interlock.condition_switches_info'
    _description = '敌对信号条件道岔信息'
    _track_log = True


    index = fields.Integer(string="序号")
    switch_id = fields.Many2one(string='道岔',
                                comodel_name='metro_park_base.switches')
    hostile_id = fields.Many2one(string="敌对信号",
                                 comodel_name="metro_park.interlock.hostile_signal_info")
    is_protect = fields.Boolean(string='是否保护')
    is_reverse = fields.Boolean(string='是否反向')

    representation = fields.Text(string="描述")
