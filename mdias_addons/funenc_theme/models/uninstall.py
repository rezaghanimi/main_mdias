# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions


class UninstallExtend(models.TransientModel):
    _inherit = "base.module.uninstall"

    pass_word = fields.Char(string="uinstall password")

    @api.multi
    def action_uninstall(self):
        '''
        护展卸载必需输入密码，防止误操作
        :return:
        '''
        if self.pass_word != 'my code is 9527':
            raise exceptions.ValidationError('the uninstall password is error')
        modules = self.mapped('module_id')
        return modules.button_immediate_uninstall()