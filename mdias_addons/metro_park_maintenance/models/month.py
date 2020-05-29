
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Month(models.Model):
    '''
    月，用于筛选
    '''
    _name = 'metro_park_maintenance.month'
    _order = 'val'
    _rec_name = 'name'
    _description = '月份'
    
    name = fields.Char(string='月')
    val = fields.Integer(string="值")
