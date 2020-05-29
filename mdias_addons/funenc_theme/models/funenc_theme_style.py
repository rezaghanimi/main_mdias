
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class FunencThemeStyle(models.Model):
    '''
    主题样式
    '''
    _name = 'funenc_theme.funenc_theme_style'
    
    uid = fields.Many2one(string='用户')
    style_txt = fields.Text(string='样式内容')
    remark = fields.Text(string='备注')

    @api.model
    def get_user_style(self):
        '''
        取得用户颜色, 如果没有系统颜色的话就使用admin颜色
        :return:
        '''
        uid = self.env.user.id
        records = self.search([('uid', '=', uid)])
        if len(records) == 0:
            admin_uid = self.env.ref('base.user_admin').id
            records = self.search([('uid', '=', admin_uid)])
        if len(records) == 0:
            return {}
        else:
            return json.loads(records[0].style_txt)

    @api.model
    def update_user_style(self, style_txt):
        '''
        更新用户样式, 如果没有的话则创建一条
        :param style_txt: 样式文字
        :return:
        '''
        uid = self.env.user.id
        records = self.search([('uid', '=', uid)])
        if len(records) == 0:
            self.create([{
                'uid': uid,
                'style_txt': json.dumps(style_txt)
            }])
        else:
            records.write({
                'style_txt': json.dumps(style_txt)
            })
