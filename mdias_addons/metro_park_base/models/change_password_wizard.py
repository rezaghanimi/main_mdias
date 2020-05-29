
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChangePasswordWizard(models.Model):
    '''
    修改密码向导
    '''
    _name = 'metro_park_base.change_password_wizard'
    _description = '修改密码向导'
    _track_log = True
    
    confirm_password = fields.Char(string='确认密码')
    new_password = fields.Char(string='新密码')
    login = fields.Char(string='登录名')
    old_password = fields.Char(string='旧密码')

