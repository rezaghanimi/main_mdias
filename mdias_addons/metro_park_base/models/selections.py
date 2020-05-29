
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Selections(models.Model):
    '''
    使用many2one来模拟selection
    '''
    _name = 'metro_park_base.selections'
    
    value = fields.Char(string='值')
    name = fields.Char(string='名称')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "参数名称不能重复"),
                        ('value_unique', 'UNIQUE(value)', "值不能重复")]

