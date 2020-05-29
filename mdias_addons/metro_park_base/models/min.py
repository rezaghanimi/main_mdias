
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Min(models.Model):
    '''
    分钟数
    '''
    _name = 'metro_park_base.min'
    
    min = fields.Char(string='分钟')
    val = fields.Char(string='值')
