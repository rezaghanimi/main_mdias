
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InterlockSwitchSubInfo(models.Model):
    '''
    道岔
    '''
    _name = 'metro_park.interlock.switch_sub_info'
    _order = 'index'
    _description = '道岔信息'
    _track_log = True

    switch_info_id = fields.Many2one(string="子道岔",
                                     comodel_name="metro_park.interlock.switch_info")
    index = fields.Integer(string="序号", help="在分组中的顺序", default=0)
    switch = fields.Many2one(string='道岔',
                             comodel_name="metro_park_base.switches")

