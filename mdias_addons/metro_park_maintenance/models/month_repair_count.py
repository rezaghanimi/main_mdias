
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MonthRepairCount(models.TransientModel):
    '''
    月检修数量
    '''
    _name = 'metro_park_maintenance.month_repair_count'
    
    month = fields.Char(string='月')
    count = fields.Char(string='检修数量')

    compute_wizard_id = fields.Many2one(comodel_name="", string="向导id")
