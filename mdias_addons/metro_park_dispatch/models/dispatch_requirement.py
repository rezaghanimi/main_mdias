
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchRequirement(models.Model):
    '''
    调车作业要求
    '''
    _name = 'metro_park_dispatch.dispatch_requirement'
    _order = "index"
    
    name = fields.Char(string='名称')
    is_system = fields.Boolean(string="系统内置", default=False, help="系统内置无法删除")
    index = fields.Integer(string="序号", default=1)
    remark = fields.Text(string='备注')
