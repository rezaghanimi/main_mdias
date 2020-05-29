
# -*- coding: utf-8 -*-

from odoo import models, fields


class MajorType(models.Model):
    '''
    专业类型
    '''
    _name = 'metro_park_base.major_type'
    _description = '专业类型'
    _track_log = True
    
    major_id = fields.Many2one(string='所属专业', comodel_name='metro_park_base.major')
    name = fields.Char(string='名称')
    no = fields.Many2one(string="代码")

    _sql_constraints = [('name_unique', 'UNIQUE(no)', "专业类型代码不能重复")]
