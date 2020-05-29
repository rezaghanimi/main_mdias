
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchRequestOperationLog(models.Model):
    '''
    调车申请操作记录
    '''
    _name = 'metro_park_dispatch.dispatch_request_operation_log'
    _track_log = True

    request_id = fields.Many2one(string="调车申请",
                                 comodel_name="metro_park_dispatch.dispatch_request")
    content = fields.Char(string='内容')
