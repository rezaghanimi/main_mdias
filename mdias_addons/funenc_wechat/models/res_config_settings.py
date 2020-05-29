#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    '''
    企业微信配置，批量处理
    '''
    _inherit = 'res.config.settings'

    batch_num = fields.Integer("同步批次数量")
    syn_thread_num = fields.Integer()

    @api.model
    def get_values(self):
        '''
        取得配置
        :return:
        '''
        res = super(ResConfigSettings, self).get_values()
        res['batch_num'] = int(self.env['ir.config_parameter']
                               .sudo().get_param('funenc_wechat.batch_num', default=0))
        res['syn_thread_num'] = int(self.env['ir.config_parameter']
                                    .sudo().get_param('funenc_wechat.syn_thread_num', default=5))
        return res

    @api.model
    def set_values(self):
        '''
        设置配置值
        :return:
        '''
        self.env['ir.config_parameter'].sudo().set_param('funenc_wechat.batch_num', self.batch_num)
        self.env['ir.config_parameter'].sudo().set_param('funenc_wechat.syn_thread_num', self.syn_thread_num)

        super(ResConfigSettings, self).set_values()
