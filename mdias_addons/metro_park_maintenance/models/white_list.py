
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WhiteList(models.Model):
    '''
    白名单
    '''
    _name = 'metro_park_maintenance.white_list'
    
    date = fields.Date(string='日期')
    remark = fields.Char(string='备注')

    _sql_constraints = [('date', 'UNIQUE(date)', "日期不能重复")]
