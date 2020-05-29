
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaxRepairInfo(models.Model):
    '''
    最大检修数量
    '''
    _name = 'metro_park_maintenance.max_repair_info'
    
    max_count = fields.Char(string='数量')
    rule_id = fields.Many2one(string='修程',
                              comodel_name='metro_park_maintenance.repair_rule')
    location = fields.Many2one(string="位置",
                               comodel_name="metro_park_base.location")

