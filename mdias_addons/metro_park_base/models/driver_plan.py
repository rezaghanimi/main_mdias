
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DriverPlan(models.Model):
    '''
    model project
    '''
    _name = 'metro_park_base.driver_plan'
    
    name = fields.Char(string='名称')
