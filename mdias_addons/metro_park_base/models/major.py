# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Major(models.Model):
    '''
    专业
    '''
    _name = 'metro_park_base.major'
    _description = '专业'
    _track_log = True

    name = fields.Char(string='名称')
    no = fields.Char(string="专业代码")

    _sql_constraints = [('no_unique', 'UNIQUE(no)', "专业代码不能重复")]
