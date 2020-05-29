# -*- coding: utf-8 -*-
from odoo import http

import logging
_logger = logging.getLogger(__name__)
import json


class MobileApi(http.Controller):
    '''
    测试接口
    '''
    @http.route('/metro_park_dispatch/login', type='http', auth='public', csrf=False)
    def do_login(self, **kw):
        '''
        取得调度计划
        :param kw:
        :return:
        '''
        print(kw)
        account = kw.get("account", None)
        password = kw.get("password", None)
        print(account, password)
        if not account or not password:
            return json.dumps({
                'status': 400,
                'data': '请填写用户名和密码'
            })
        try:
            user_id = http.request.env["res.users"].sudo()\
                .authenticate("metro_park_0828", account, password, None)
            return json.dumps({
                'status': 200,
                'data': user_id
            })
        except Exception as e:
            _logger.info(e)
            return json.dumps({
                'status': 500,
                'data': str(e)
            })

    '''
    根据uid取得对应的工单
    '''
    @http.route('/metro_park_dispatch/get_orders', type='json', auth='public', methods=['post'], csrf=False)
    def get_orders(self, **kw):
        '''
        取得调车工单
        :param kw:
        :return:
        '''
        user_id = kw.get("user_id", None)
        print(kw)
        print(user_id)
        if not user_id:
            return json.dumps({
                'status': 400,
                'data': '请先登录'
            })
        try:
            user = http.request.env["res.users"].sudo().search_read([('id', '=', user_id)])
            if len(user) == 0:
                return json.dumps({
                    'status': 500,
                    'data': "请先登录"
                })
            user = user[0]
            location = user["cur_location"][0]
            if not location:
                return json.dumps({
                    'status': 500,
                    'data': "当前用户没有设置场段"
                })
            plans = http.request.env["metro_park_dispatch.dispatch_notice"].sudo(user_id).get_orders(location)
            print(plans)
            return json.dumps({
                'status': 200,
                'data': plans
            })
        except Exception as e:
            _logger.info(e)
            return json.dumps({
                'status': 500,
                'data': str(e)
            })

    @http.route('/metro_park_dispatch/get_user_info', type='http', auth='public', csrf=False)
    def get_user_info(self, **kw):
        user_id = kw['user_id']
        if not user_id:
            return json.dumps({
                'status': 400,
                'data': '请先登录'
            })
        user = http.request.env["res.users"].sudo().search([('id', '=', user_id)])
        print(user)
        if not user:
            return json.dumps({
                'status': 400,
                'data': '用户查找失败'
            })
        return json.dumps({
            'status': 200,
            'data': {
                'login': user.login,
                'name': user.name
            }
        })





