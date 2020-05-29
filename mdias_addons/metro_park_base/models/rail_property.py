
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RailProperty(models.Model):
    '''
    轨道属性
    '''
    _name = 'metro_park_base.rail_property'
    _track_log = True
    
    name = fields.Char(string='名称')
    remark = fields.Char(string='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "属性名称不能重复")]
