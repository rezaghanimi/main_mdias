# !user/bin/env python3
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    wx_login = fields.Char(string='企业微信登录账号')

    wx_user_ids = fields.One2many(comodel_name='funenc.wechat.user',
                                  inverse_name='user_id',
                                  string='微信帐号')

    cur_wx_user_id = fields.Many2one(comodel_name="funenc.wechat.user",
                                     string="当前微信帐号",
                                     domain="[('id', 'in', wx_user_ids)]",
                                     help="多个用户的情况下选择当前对应哪个微信用户")

    cur_department = fields.Many2one(comodel_name="funenc.wechat.department",
                                     string="当前部门",
                                     related='cur_wx_user_id.cur_department')

    def __init__(self, pool, cr):
        """ Override of __init__ to add access rights on
        display_employees_suggestions fields. Access rights are disabled by
        default, but allowed on some specific fields defined in
        self.SELF_{READ/WRITE}ABLE_FIELDS.
        """
        init_res = super(ResUserInherit, self).__init__(pool, cr)
        # duplicate list to avoid modifying the original reference
        self.SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        self.SELF_WRITEABLE_FIELDS.extend(['wx_user_ids'])
        # duplicate list to avoid modifying the original reference
        self.SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        self.SELF_READABLE_FIELDS.extend(['wx_user_ids'])
        return init_res

    @api.model
    def _check_credentials(self, password):
        '''
        改写了原有的_check_credentials函数，原有方法检查成功，则不抛错，直接return，所以通过是否抛错来绕过验证。
        在验证之前加入了一个自定的验证函数
        :param password: 传入的密码
        :return:
        '''
        check_result = self.check_login_source(password)
        if check_result is True:
            return
        else:
            super()._check_credentials(password)

    @api.depends("wx_user_ids")
    def _compute_default_wx_user(self):
        '''
        计算默认微信用户
        :return:
        '''
        for record in self:
            if len(record.cur_wx_user_id) > 0:
                record.cur_wx_user_id = record.cur_wx_user_id[0].id

    @api.model
    def check_login_source(self, password):
        '''
        继承并添加企业微信验证
        :param password: 如果是企业微信扫码、免登过来的，则为一个dict，否则为一个字符串
        :return:
        '''
        if isinstance(password, dict) is False:
            return False
        elif request.session['auth_code'] == password['auth_code']:
            return True
        else:
            return False
