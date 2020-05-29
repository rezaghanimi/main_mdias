
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StationTrackType(models.Model):
    '''
    股道类型
    '''
    _name = 'metro_park_base.rail_type'
    _description = '轨道管理，带有特殊属性的轨道叫做股道'
    _track_log = True
    
    name = fields.Char(string='名称')
    remark = fields.Text(string='备注')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "股道类型不能重复")]
