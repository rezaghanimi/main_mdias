
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Day(models.Model):
    '''
    月份中的天
    '''
    _name = 'metro_park_maintenance.day'
    
    name = fields.Char(string='名称')
    val = fields.Integer(string='值')
