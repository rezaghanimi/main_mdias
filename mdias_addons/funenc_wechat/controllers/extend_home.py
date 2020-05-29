# !user/bin/env python3
# -*- coding: utf-8 -*-
# Author: Artorias
from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home, ensure_db


# class DingHome(Home):
#
#     @http.route('/web/login', type='http', auth='public', csrf=False)
#     def web_login(self, redirect=None, **kw):
#         '''
#         企业微信扫码登录odoo后台
#         说明：redirect_url，配置后扫码登录后会通过该应用的允许跳转到以这个域名为开头的url；
#              app_id：为企业微信的crop；
#              agent_id：为企业微信应用的agent；
#         使用：需要先同步企业微信，否则无法使用扫码登录；
#              需要在后台配置好企业信息以及应用信息；
#              如果扫码的用户不在odoo的user表里（通过wx_userid对应），则会登录失败；
#         :return:
#         '''
#         ensure_db()
#         if request.httprequest.method == 'GET' and redirect and request.session.uid:
#             return http.redirect_with_hash(redirect)
#         apps = request.env['funenc.wechat.apps'].sudo().search([('is_login_app', '=', True)])
#         can_user_qr_code = "True"
#         if len(apps) == 0:
#             render_values = {
#                 'redirect_url': None,
#                 'appid': None,
#                 'agentid': None,
#                 'can_user_qr_code': "False"
#             }
#         else:
#             redirect_url = apps[0].app_redirect_url or ''
#             app_id = apps[0].account_id.corp
#             agent_id = apps[0].app_agent
#             if redirect_url == '' or app_id is False or agent_id is False:
#                 can_user_qr_code = "False"
#             render_values = {
#                 'redirect_url': 'http://' + redirect_url + '/funenc_wechat/success_login_by_wechat',
#                 'appid': app_id,
#                 'agentid': agent_id,
#                 'can_user_qr_code': can_user_qr_code
#             }
#         return request.render('funenc_wechat.funenc_layui_theme_wechat_qr_code_login', render_values)
