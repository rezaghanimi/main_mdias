
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintainceConfig(models.Model):
    '''
    检修配置
    '''
    _name = 'metro_park_maintenance.maintaince_config'
    
    out_plan_pre_min = fields.Char(string='收发车提前时间')

