# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ParkArea(models.Model):
    '''
    检修区域
    '''
    _name = 'metro_park_base.park_area'
    
    name = fields.Char(string='名称')
    remark = fields.Char(string='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "park_area区域不能重复")]
