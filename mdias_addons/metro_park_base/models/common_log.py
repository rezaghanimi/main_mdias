
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CommonLog(models.Model):
    '''
    通用日志
    '''
    _name = 'metro_park_base.common_log'
    
    log = fields.Text(string='日志')
    type = fields.Selection(string='类型',
                            selection=[('socketio', 'socketio')])
