# -*- coding: utf-8 -*-
import functools
import operator
import datetime as dt

from odoo import http
from odoo.exceptions import UserError, AccessDenied
from odoo.http import request
from odoo.tools.translate import _, config

from odoo.modules import get_resource_path
from addons.web.controllers.main import Session
from ...funenc_theme.controllers.controllers import UserLogin


class Login(UserLogin):
    @http.route('/web/login', type='http', auth="public", csrf=False)
    def web_login(self, redirect=None, **kw):
        login_zh_title = config.get('login_zh_title', 'Funenc')
        login_en_title = config.get('login_en_title', 'Funenc')
        request.params['title'] = login_zh_title.encode('latin-1').decode('unicode-escape')
        request.params['english_title'] = login_en_title
        # sso登录时跳转到登录页并提示
        if kw.get('sso_login', False) is not False:
            request.params['no_login'] = '该用户已在其他地点登录，你已下线'
        # 如果被限制登录了，直接提示
        if request.httprequest.method == 'POST':
            login_user = request.env['res.users'].sudo().search([('login', '=', kw['login'])])
            if len(login_user) != 0 and login_user.today_continuous_error_count != 0 and \
                    login_user.today_continuous_error_count % 5 == 0 and \
                    dt.datetime.utcnow() - login_user.no_login_start_time <= dt.timedelta(
                seconds=login_user.no_login_minute * 60):
                request.params['no_login'] = '该账户今日密码已连续错误{}次，禁止登录{}分钟'.format(
                    login_user.today_continuous_error_count, login_user.no_login_minute)
                values = request.params.copy()
                response = request.render('web.login', values)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        result = super().web_login(redirect, **kw)
        if request.httprequest.method == 'POST' and result.qcontext.get('login_success', True) is False and \
                result.qcontext.get('error', '') == '错误的登录名/密码':
            if len(login_user) != 0:
                today_continuous_error_count = login_user.today_continuous_error_count + 1
                if today_continuous_error_count <= 5:
                    no_login_minute = 1
                elif today_continuous_error_count % 5 == 0:
                    no_login_minute = login_user.no_login_minute * 2
                else:
                    no_login_minute = login_user.no_login_minute
                no_login_start_time = dt.datetime.utcnow()
                login_user.sudo().write({
                    'today_continuous_error_count': today_continuous_error_count,
                    'no_login_minute': no_login_minute,
                    'no_login_start_time': no_login_start_time
                })
        return result


class IncludeController(Session):
    @http.route('/web/session/change_password', type='json', auth="user")
    def change_password(self, fields):
        old_password, new_password,confirm_password = operator.itemgetter('old_pwd', 'new_password','confirm_pwd')(
            {f['name']: f['value'] for f in fields})
        if not (old_password.strip() and new_password.strip() and confirm_password.strip()):
            return {'error':_('You cannot leave any password empty.'),'title': _('Change Password')}
        if new_password != confirm_password:
            return {'error': _('The new password and its confirmation must be identical.'),'title': _('Change Password')}
        custom_judge = request.env['res.users'].judge_password(new_password)
        if not custom_judge['error']:
            return {'error': custom_judge['error_content'], 'title': _('Change Password')}
        msg = _("Error, password not changed !")
        try:
            if request.env['res.users'].change_password(old_password, new_password):
                return {'new_password':new_password}
        except UserError as e:
            msg = e.name
        except AccessDenied as e:
            msg = e.args[0]
            if msg == AccessDenied().args[0]:
                msg = _('The old password you provided is incorrect, your password was not changed.')
        return {'title': _('Change Password'), 'error': msg}


class MetroParkBaseController(http.Controller):
    '''
    基础接口
    '''
    @http.route('/metro_park_dispatch/get_location_info_by_name/',
                auth='public',
                type='http')
    def get_location_info_by_name(self, **kw):
        '''
        根据名称取得位置信息
        :param kw:
        :return:
        '''
        name = http.request.params.get('name', None)
        model = http.request.env['metro_park_base.location']
        return model.get_location_by_name(name)

    @http.route('/static/img/logo', type='http', auth="public")
    def company_logo(self, dbname=None, **kw):
        """
        更改默认logo
        :param dbname:
        :param kw:
        :return:
        """
        placeholder = functools.partial(get_resource_path, 'metro_park_base', 'static', 'img')
        response = http.send_file(placeholder('logo.png'))

        return response

    @http.route('/metro_park_base/get_rail_state/',
                auth='public',
                type='http')
    def get_rail_state(self, **kw):
        '''
        根据名称取得位置信息
        :param kw:
        :return:
        '''
        alias = http.request.params.get('alias', None)
        models = http.request.env['metro_park_base.rails_sec'].search([('location.alias', '=', alias)])
        state_list = []
        for model in models:
            power_failure = 0
            rail_type_occupy = 0
            rail_type_construction = 0
            for state in model.rail_state:
                if state.name == "停电":
                    power_failure = 1
                    continue
                if state.name == "占用":
                    rail_type_occupy = 1
                    continue
                if state.name == "施工":
                    rail_type_construction = 1
                    continue
            data = {
                "name": model.name,
                "alias": model.alias,
                "state": {
                    "power_failure": power_failure,
                    "rail_type_occupy": rail_type_occupy,
                    "rail_type_construction": rail_type_construction
                }

            }
            state_list.append(data)
        return state_list
