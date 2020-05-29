
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class InitWizard(models.Model):
    '''
    初始化向导,为了防止错误的进行初始化操作
    '''
    _name = 'metro_park_dispatch.init_wizard'
    _track_log = True
    
    password = fields.Char(string='密码')

    @api.multi
    def on_ok(self):
        '''
        确定按扭点击, 如果密码正则进行初始化
        :return:
        '''
        if self.password != 'funenc_passowrd':
            raise exceptions.ValidationError("密码不正确")

        model = self.env['metro_park_dispatch.cur_train_manage']
        model.syn_cur_train()

