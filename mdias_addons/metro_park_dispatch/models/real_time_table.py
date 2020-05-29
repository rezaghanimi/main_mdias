
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RealTimeTable(models.Model):
    '''
    实际运行图
    '''
    _name = 'metro_park_dispatch.real_time_table'
    _description = '实际运行图'
    _track_log = True
    
    time_table = fields.Many2one(string='时刻表',
                                 comodel_name='metro_park_dispatch.time_table')
    date = fields.Date(string='日期')
    remark = fields.Char(string='备注')

