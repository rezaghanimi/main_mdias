# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning


class WechatApp(models.Model):
    '''
    企业微信应用信息
    '''
    _name = 'funenc.wechat.apps'
    _rec_name = 'name'
    _description = '应用'

    account_id = fields.Many2one(comodel_name='funenc.wechat.account', string='企业帐号')
    name = fields.Char(string='应用名称', required=True, help='应用名称')
    app_agent = fields.Char(string='agent', required=True, help='应用agent')
    app_secret = fields.Char(string='应用secret', required=True, help='应用secret')
    is_login_app = fields.Boolean(string='作为扫码登录应用',
                                  default=False,
                                  help='是否作为扫码登录后台的应用配置，同时只能配置一个应用')
    app_redirect_url = fields.Char(string='应用可信域名')
    is_exempts = fields.Boolean(string='免登应用',
                                default=False,
                                help='是否作为免登企业微信pc后台的应用配置，同时只能配置一个应用')
    # jssdk验证文件
    jssdk_file = fields.Binary(string='jssdk校验文件',
                               attachment=True,
                               help='企业微信「网页授权及JS-SDK」域名归属验证上传文件的文件名')
    jssdk_file_filename = fields.Char(string='jssdk校验文件-文件名')

    @api.onchange('is_login_app')
    def _onchange_is_login_app(self):
        if not self.is_login_app:
            self.app_redirect_url = None

    @api.model
    def create(self, vals):
        '''
        cretae-检查设置默认扫码登录、免登时是否只有一个
        :param vals: 
        :return: 
        '''
        is_login_app = vals.get('is_login_app', False)
        is_exempts = vals.get('is_exempts', False)
        if is_login_app != False:
            else_login_app = self.search([('is_login_app', '!=', False)])
            if len(else_login_app) != 0:
                raise Warning('「{}-{}」已作为扫码登录应用的app'.format(else_login_app.account_id.name, else_login_app.name))
        if is_exempts != False:
            else_exempts = self.search([('is_exempts', '!=', False)])
            if len(else_exempts) != 0:
                raise Warning('「{}-{}」已作为免登应用'.format(else_exempts.account_id.name, else_exempts.name))
        create_super = super().create(vals)
        return create_super

    @api.multi
    def write(self, vals):
        '''
        write-检查设置默认扫码登录、免登时是否只有一个
        :param vals: 
        :return: 
        '''
        is_login_app = vals.get('is_login_app', False)
        is_exempts = vals.get('is_exempts', False)
        if is_login_app != False:
            else_login_app = self.search([('is_login_app', '!=', False)])
            if len(else_login_app) != 0:
                raise Warning('「{}-{}」已作为扫码登录应用的app'.format(else_login_app.account_id.name, else_login_app.name))
        if is_exempts != False:
            else_exempts = self.search([('is_exempts', '!=', False)])
            if len(else_exempts) != 0:
                raise Warning('「{}-{}」已作为免登应用'.format(else_exempts.account_id.name, else_exempts.name))
        write_super = super().write(vals)
        return write_super