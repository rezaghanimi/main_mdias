# -*- coding: utf-8 -*-
import re
import time
import datetime
from odoo.addons.odoo_operation_log.model_extend import LogManage

LogManage.register_type('login', '登录')

from odoo import models, fields, api, exceptions


class UserExtend(models.Model):
    '''
    扩展用户, 添加属性
    '''
    _inherit = 'res.users'
    _track_log = True

    locations = fields.Many2many(string="所属场段",
                                 comodel_name="metro_park_base.location",
                                 relation="user_location_rel",
                                 column1="user_id",
                                 column2="location_id")

    cur_location = fields.Many2one(string="当前场段",
                                   comodel_name="metro_park_base.location",
                                   domain="[('id', 'in', locations)]")

    today_continuous_error_count = fields.Integer('今日密码连续错误次数', default=0)
    no_login_minute = fields.Integer('当日限制登录分钟数', default=1)  # 分钟数按当日失败进行翻倍累加
    no_login_start_time = fields.Datetime('限制登录起始时间')

    last_change_password_date = fields.Date(
        '最后修改密码时间', default=lambda *a: time.strftime('%Y-%m-%d'))  # 最后修改密码的时间，要求每过3个月提醒修改一次密码

    def get_cur_user_groups(self):
        '''
        取得当前用户的group
        :return:
        '''
        group_ids = self.env.user.groups_id.ids
        return [('id', 'in', group_ids), ('atomic', '=', False)]

    cur_role = fields.Many2one(string="当前角色",
                               comodel_name="res.groups",
                               domain=get_cur_user_groups)

    @api.model
    def get_user_line(self):
        '''
        取得用户所属线路
        :return:
        '''
        user = self.env.user
        if user.cur_location:
            return user.cur_location.line.id
        elif user.locations:
            return user.locations[0].line.id
        else:
            return None

    @api.model
    def get_cur_location(self):
        '''
        取得当前位置
        :return:
        '''
        return self.cur_location.id

    @api.model
    def get_user_location_info(self):
        '''
        取得用户所在位置
        :return:
        '''
        if not self.env.user.cur_location:
            raise exceptions.Warning("当前用户没有配置位置")

        record = self.env.user.cur_location.read()[0]
        gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        if record["id"] == gaodalu:
            record["location_alias"] = 'gaodalu'
        else:
            record["location_alias"] = 'banqiao'

        return record

    @api.onchange('locations')
    def on_change_locations(self):
        '''
        改变location的时候理改location
        :return:
        '''
        if not self.locations:
            self.cur_location = False
        elif len(self.locations) > 0 and not self.cur_location:
            self.cur_location = self.locations[0].id

    @staticmethod
    def judge_password(new_password):
        result = {'error_content': '', 'error': True}
        password_re = re.compile(
            '^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_]+$)(?![a-z0-9]+$)(?![a-z\W_]+$)(?![0-9\W_]+$)[a-zA-Z0-9\W_]{8,}$')
        if len(new_password) < 8:
            result['error_content'] = '密码长度需要大于等于8位'
            result['error'] = False
        elif re.match(password_re, new_password) is None:
            result['error_content'] = '密码需要由大小写字母、数字和特殊字符中任意三种组合而成'
            result['error'] = False
        return result

    @api.model
    def judge_change_password(self):
        # 登录成功后验证是否密码已经超过3个月未修改
        user = self.env.user
        return datetime.date.today() - user.last_change_password_date > datetime.timedelta(days=30)

    @api.multi
    def write(self, vals):
        for record in self:
            if 'password' in vals:
                # 验证密码是否符合强度验证
                custom_judge = self.judge_password(vals['password'])
                if not custom_judge['error']:
                    raise exceptions.UserError(custom_judge['error_content'])
                record.write({'last_change_password_date': time.strftime('%Y-%m-%d')})
        return super().write(vals)

    @api.model
    def _update_last_login(self):
        '''
        登录成功之后将当日失败次数清零，清空失败起始时间，限制时间回到1分
        :return:
        '''
        super()._update_last_login()
        LogManage.put_log(content='用户登录系统', mode='login')
        self.env.user.write({
            'today_continuous_error_count': 0,
            'no_login_minute': 1,
            'no_login_start_time': None
        })

    @api.model
    def trigger_up_to_sso_login(self, uid):
        '''
        用户登录时发送通知，uid可能为None，此时不发送
        :param uid:
        :return:
        '''
        if uid is not None:
            self.trigger_up_event('sso_login', '用户已在其他地点登录', to=uid)

    @api.model
    def login_error_clean(self):
        '''
        清理每日登录密码错误失败次数累计的定时任务
        :return:
        '''
        self.search([('today_continuous_error_count', '!=', 0)]).write({
            'today_continuous_error_count': 0,
            'no_login_minute': 1,
            'no_login_start_time': None
        })

    @api.multi
    def action_save_preference(self):
        '''
        更新当前用户的wx_login
        :return:
        '''
        cur_wx_user_id = self.cur_wx_user_id
        if cur_wx_user_id:
            old_user = self.env["res.users"].search([('wx_login', '=', cur_wx_user_id.wx_userid)])
            if old_user:
                old_user.wx_login = str(old_user.wx_login) + "_old_9527"
            self.wx_login = cur_wx_user_id.wx_userid
        return {'type': 'ir.actions.client', 'tag': 'reload'}



