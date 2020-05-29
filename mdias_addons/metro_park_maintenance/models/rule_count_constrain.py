
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RuleCountConstrain(models.TransientModel):
    '''
    规程数量限制
    '''
    _name = 'metro_park_maintenance.rule_count_constrain'

    count = fields.Char(string='数量')
    year_compute_wizard = fields.Many2one(comodel_name="year_plan_compute_wizard",
                                          string="年计划向导")
    month_compute_wizard = fields.Many2one(comodel_name="metro_park_maintenance.month_plan_compute_wizard",
                                           string="年计划向导")
    rule = fields.Many2one(string='规程',
                           comodel_name='metro_park_maintenance.repair_rule')
