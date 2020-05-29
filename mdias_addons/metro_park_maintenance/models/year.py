# -*- coding: utf-8 -*-

from odoo import models, fields


class Year(models.Model):
    '''
    年，用于筛选
    '''
    _name = 'metro_park_maintenance.year'
    _rec_name = 'name'
    _order = 'val'
    _description = '年'

    name = fields.Char(string="名称")
    val = fields.Integer(string='年')

