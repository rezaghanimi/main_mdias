
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Operation(models.Model):
    '''
    调车计划钩数
    '''
    _name = 'metro_park_dispatch.operation'
    _order = 'index'
    _description = '钩计划操作'

    index = fields.Integer(string="序号", default=0)
    name = fields.Char(string='名称')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "操作名称不能重复")]

