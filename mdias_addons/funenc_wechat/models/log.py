# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class WechatFilterErrorLog(models.Model):
    '''
    日志模块
    '''
    _name = 'funenc.wechat.log'
    _order = 'create_date desc'
    _description = '日志'

    name = fields.Char('名称')
    message = fields.Char('消息')

    @api.model
    def log_info(self, name, message):
        print(name, message)
        self.sudo().create({'name': name, 'message': message})
