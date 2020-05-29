# -*- coding: utf-8 -*-

from odoo import models, fields


class FunencSystemStyle(models.Model):
    '''
        系统样式
    '''
    _name = 'funenc_theme.funenc_system_style'
    _table = 'funenc_theme_style'

    name = fields.Char(string='名称')

    login_page_background_image = fields.Binary(string='登录页面背景图')
    background_color = fields.Char(string='背景色')
    active = fields.Boolean(string='是否启用')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Style name already exists!'),
    ]
