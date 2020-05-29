# !usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil import relativedelta
import base64
import xml.etree.ElementTree as ET

from odoo import http
from odoo.http import request
from wechatpy.enterprise import WeChatClient

from .webhook_class import MapWebhook
from .sdk.Crypt import WXBizMsgCrypt

import logging
import json

_logger = logging.getLogger(__name__)


class MobileControllers(http.Controller):

    @http.route('/api/sign', type='http', auth="public", method=['GET'])
    def api_sign(self, **kwargs):
        '''
        移动端获取签名
        :param kwargs: url: 本地url, serial: 企业编号, agentID: 应用id
        :return:
        '''
        url = kwargs['url']
        account_code = kwargs['serial']
        agent_id = kwargs['agentID']
        wechat_controllers = WechatControllers()
        auth_config = json.loads(wechat_controllers.auth_config(url, account_code, agent_id))
        auth_config['corpId'] = auth_config.pop('appId')
        auth_config['nonceStr'] = auth_config.pop('noncestr')
        auth_config['timeStamp'] = auth_config.pop('timestamp')
        result = dict(errcode=0, msg='', data=auth_config)
        return json.dumps(result)

    @http.route('/api/login', type='http', auth='public', methods=['POST'], csrf=False)
    def api_login(self, **kwargs):
        '''
        移动端登录
        :param kwargs:
        :return:
        '''
        # 获取用户信息
        account_code = kwargs['serial']
        agent_id = kwargs['agentID']
        app = request.env["funenc.wechat.apps"].sudo().search(
            [('app_agent', '=', agent_id), ('account_id.code', '=', account_code)], limit=1)
        client = WeChatClient(app.account_id.corp, app.app_secret)
        wx_userid = client.oauth.get_user_info(kwargs['code'])
        request.session['auth_code'] = kwargs['code']
        password = {
            'model': 'wechat',
            'auth_code': kwargs['code']
        }
        authenticate = request.session.authenticate(request.session.db, wx_userid['UserId'], password)
        if authenticate is False:
            return '该用户不在系统用户列表中'
        else:
            session_info = request.env['ir.http'].session_info()
            _logger.info(dict(errcode=0, msg='', data={'token': session_info['session_id']}))
            return json.dumps(dict(errcode=0, msg='', data={'token': session_info['session_id']}))


class WechatControllers(http.Controller):
    @http.route('/funenc_wechat/auth/', type='json', auth="none")
    def auth(self, code, db, account_code, agent_id):
        client = http.request.env['funenc.wechat.account'].get_client_by_app(account_code, agent_id)
        if not client:
            logging.info("can not find the enterprise acccount")
            raise Exception('can not find the enterprise acccount')

        # 取得用户信息
        user_info = client.oauth.get_user_info(code)
        userid = user_info['UserId']

        # 取得user
        user = request.env['res.users'] \
            .sudo().search_read([('login', '=', userid)], fields=['password'])
        if not user:
            raise Exception("can not find user, login error")

        logging.info(user_info)
        request.session['auth_code'] = code
        password = {
            'model': 'wechat',
            'auth_code': code
        }
        request.session.authenticate(db, userid, password)
        return request.env['ir.http'].session_info()

    @http.route('/funenc_wechat/auth_config/', type='json', auth="none")
    def auth_config(self, url, account_code, agent_id):
        client = http.request.env['funenc.wechat.account'].get_client_by_app(account_code, agent_id)
        if not client:
            raise Exception('can not find the enterprise acccount')

        jsapi = client.jsapi
        # gen time stamp
        now = datetime.now() + relativedelta.relativedelta(hours=8)
        timestamp = datetime.timestamp(now)
        timestamp = int(round(timestamp))

        auth_params = {}
        ticket = jsapi.get_jsapi_ticket()
        noncestr = 'sdfsdfsdfertgjki7swwerw89080erwrwer'

        auth_params['signature'] = jsapi.get_jsapi_signature(noncestr, ticket, timestamp, url)
        auth_params['appId'] = client.corp_id
        auth_params['timestamp'] = timestamp
        auth_params['noncestr'] = noncestr
        return json.dumps(auth_params)

    @http.route('/<string:filename>.txt', type='http', auth="none", methods=['GET'])
    def load_file(self, filename=None):
        '''
        读取jssdk校验文件内容，进行企业微信验证
        :param filename: 文件名，不带txt后缀
        :param kwargs:
        :return: jssdk_file的文件内容，并将二进制流转为utf-8
        '''
        file_record = request.env['funenc.wechat.apps'].sudo().search(
            [('jssdk_file_filename', '=', '{}.txt'.format(filename))])
        if len(file_record) == 0:
            content = None
        else:
            content = base64.b64decode(file_record[0].jssdk_file).decode('utf-8')
        return content

    @http.route('/funenc_wechat/success_login_by_wechat', type='http', auth='public', methods=['GET'])
    def success_login(self, **kwargs):
        '''
        扫码成功后登录后台
        :param kwargs: dict类型，key值code对应value为传入的code
        :return:
        '''
        # 获取用户信息
        app = request.env["funenc.wechat.apps"].sudo().search([("is_login_app", "=", True)], limit=1)
        client = WeChatClient(app.account_id.corp, app.app_secret)
        wx_userid = client.oauth.get_user_info(kwargs['code'])
        request.session['auth_code'] = kwargs['code']
        password = {
            'model': 'wechat',
            'auth_code': kwargs['code']
        }
        authenticate = request.session.authenticate(request.session.db, wx_userid['UserId'], password)
        if authenticate is False:
            return '该用户不在系统用户列表中'
        else:
            if request.env['funenc.wechat.user'].sudo().search(
                    [('user_id', '=', authenticate)], limit=1).can_login is False:
                return '该用户没有扫码登录权限，请联系管理员'
            else:
                return http.redirect_with_hash('/web')

    @http.route('/funenc_wechat/login_free', type='http', auth="none", methods=['GET'])
    def login_free(self):
        '''
        企业微信免登入口
        :return: 跳转
        '''
        apps = request.env['funenc.wechat.apps'].sudo().search([('is_exempts', '=', True)], limit=1)
        if len(apps) == 0:
            return '没有设置免登默认企业应用'
        corpid = apps.account_id.corp
        corpsecret = apps.app_secret
        if corpid is False or corpsecret is False:
            return '没有填写企业应用信息/没有填写可信域名'
        client = WeChatClient(corpid, corpsecret)
        url = client.oauth.authorize_url(
            'http://' + request.httprequest.host.split(':')[0] + '/funenc_wechat/success_login_free_by_wechat')
        return http.redirect_with_hash(url)

    @http.route('/funenc_wechat/success_login_free_by_wechat', type='http', auth='public', methods=['GET'])
    def success_login_by_wechat(self, **kwargs):
        '''
        免登成功后登录后台
        :param kwargs: dict类型，key值code对应value为传入的code
        :return:
        '''
        # 获取用户信息
        app = request.env["funenc.wechat.apps"].sudo().search([("is_exempts", "=", True)], limit=1)
        client = WeChatClient(app.account_id.corp, app.app_secret)
        wx_userid = client.oauth.get_user_info(kwargs['code'])
        request.session['auth_code'] = kwargs['code']
        password = {
            'model': 'wechat',
            'auth_code': kwargs['code']
        }
        authenticate = request.session.authenticate(request.session.db, wx_userid['UserId'], password)
        if authenticate is False:
            return '该用户不在系统用户列表中'
        else:
            return http.redirect_with_hash('/web')

    @http.route('/funenc_wechat/contacts_directory_webhook/<string:url>', type='http', auth="public", csrf=False)
    def contacts_directory_webhook(self, url, **kwargs):
        '''
        企业微信通讯录有更改时进行通知, GET方式是进行验证, POST是通知
        :param url: 后台配置的回调url
        :param msg_signature: 
        :param timestamp: 
        :param nonce: 
        :param echostr: 
        :return: 
        '''
        account = request.env['funenc.wechat.account'].sudo().search([('url', '=', url), ('open_syn', '=', True)])
        if len(account) == 0 or account[0].token is False or account[0].EncodingAESKey is False \
                or account[0].corp is False:
            return
        if request.httprequest.method == 'GET':
            content_tuple = WXBizMsgCrypt.WXBizMsgCrypt(
                account[0].token, account[0].EncodingAESKey, account[0].corp).VerifyURL(
                kwargs['msg_signature'], kwargs['timestamp'], kwargs['nonce'], kwargs['echostr'])
            return content_tuple[1]
        elif request.httprequest.method == 'POST':
            xmltext = request.httprequest.data.decode('utf-8')
            content = WXBizMsgCrypt.WXBizMsgCrypt(
                account[0].token, account[0].EncodingAESKey, account[0].corp).DecryptMsg(
                xmltext, kwargs['msg_signature'], kwargs['timestamp'], kwargs['nonce'])
            xml_tree = ET.fromstring(content[1])
            message = MapWebhook(xml_tree).distribute_class()
            return message
