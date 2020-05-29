
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DriverManage(models.Model):
    '''
    司机管理
    '''
    _name = 'driver_plan.driver_manage'
    
    name = fields.Char(string='名称')
