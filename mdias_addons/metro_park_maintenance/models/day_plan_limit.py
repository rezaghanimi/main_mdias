
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DayPlanLimit(models.Model):
    '''
    日计划限制
    '''
    _name = 'metro_park_maintenance.day_plan_limit'

    location = fields.Many2one(string='地点', comodel_name='metro_park_base.location')
    max_repair_after_high_run = fields.Integer(string='高峰车最大检修数量')
    max_repair_back_time = fields.Char(string="返回时间", help='最大返回时间')


class DayPlanLimit(models.TransientModel):
    '''
    日计划向导限制
    '''
    _name = 'metro_park_maintenance.day_plan_wizard_limit'

    location = fields.Many2one(string='地点', comodel_name='metro_park_base.location')
    max_repair_after_high_run = fields.Integer(string='高峰车最大检修数量')
    max_repair_back_time = fields.Char(string="返回时间", help='最大返回时间')
