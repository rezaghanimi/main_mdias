
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DayTypes(models.Model):
    '''
    日期类型
    '''
    _name = 'metro_park_dispatch.day_types'
    _description = '日期类型'
    _track_log = True
    
    name = fields.Char(string='名称')
    type = fields.Selection(string='类型',
                            selection=[('week_day', '工作日'),
                                       ('weekend', '周未')])
