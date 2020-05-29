
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MonthPlanDeltaInfo(models.TransientModel):
    '''
    月计划间隔天数, 用于对比上月天数
    '''
    _name = 'metro_park_maintenance.month_plan_delta_info'
    
    dev = fields.Many2one(string='设备',
                          comodel_name='metro_park_maintenance.train_dev')
    days = fields.Char(string='天数')

