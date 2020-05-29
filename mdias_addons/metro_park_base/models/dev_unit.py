
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DevMeasureUnit(models.Model):
    '''
    设备计量单位
    '''
    _name = 'metro_park_base.dev_unit'
    _description = '设备计量单位'
    _rec_name = 'name'
    
    name = fields.Char(string='名称', rquired=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "单位名称不能重复")]
