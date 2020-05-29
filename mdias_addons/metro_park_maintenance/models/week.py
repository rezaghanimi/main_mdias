
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Week(models.Model):
    '''
    周
    '''
    _name = 'metro_park_maintenance.week'
    
    name = fields.Char(string='名称')
    val = fields.Integer(string='值')
