
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DevType(models.Model):
    '''
    设备类型
    '''
    _name = 'metro_park_base.dev_type'
    _description = '设备类型'
    _track_log = True
    
    name = fields.Char(string='名称', rquired=True)
    code = fields.Char(string='代码')

    remark = fields.Text(string='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "线别名称不能重复")]

