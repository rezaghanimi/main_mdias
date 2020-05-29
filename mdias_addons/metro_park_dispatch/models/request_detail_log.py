
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RequestDetailLog(models.Model):
    '''
    调车请求日志
    '''
    _name = 'metro_park_dispatch.request_detail_log'
    _description = '调车请求日志'
    _track_log = True
    
    operation_time = fields.Datetime(string='作业时间')
    worker = fields.Many2one(string='操作人',
                             comodel_name='funenc.wechat.user')
    content = fields.Text(string='作业内容')
