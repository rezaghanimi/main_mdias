
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StationRailState(models.Model):
    '''
    股道类型
    '''
    _name = 'metro_park_base.rail_state'
    _description = '占线板状态'
    _track_log = True

    index = fields.Integer(string="序号")

    name = fields.Char(string='名称')
    remark = fields.Text(string='备注')

    is_enable = fields.Boolean(string="是否占用")

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "状态名称不能重复")]
