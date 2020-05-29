
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LocationType(models.Model):
    '''
    位置类型
    '''
    _name = 'metro_park_base.location_type'
    _description = '位置类型'
    _track_log = True
    
    remark = fields.Char(string='备注')
    name = fields.Char(string='名称')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "位置类型不能复复")]
