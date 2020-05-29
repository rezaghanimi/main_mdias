
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Property(models.Model):
    '''
    部门属性扩展
    '''
    _name = 'funenc_wechat.property'

    name = fields.Char(string='名称')
    remark = fields.Text(string='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "属性名称不能重复")]

