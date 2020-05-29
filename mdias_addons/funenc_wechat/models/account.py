# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from wechatpy.enterprise import WeChatClient
from wechatpy.exceptions import WeChatClientException
import logging
import datetime
import threading
import traceback

_logger = logging.getLogger(__name__)

# 全局开关，防止重入
IS_SYNING = False


class WechatAccount(models.Model):
    ''''
    企业帐号管理，可以管理多个帐号
    '''
    _name = 'funenc.wechat.account'
    _description = '企业帐号管理'

    name = fields.Char(string='企业名称', required=True, help='企业名称')
    code = fields.Char(string='企业编号', required=True, help='企业编号')
    corp = fields.Char(string='CorpID', required=True, help='企业CorpID')
    account_secret = fields.Char('通讯录secret', required=True, help='企业通讯录secret')
    app_ids = fields.One2many(comodel_name='funenc.wechat.apps', inverse_name='account_id', string='应用')
    open_syn = fields.Boolean(default=False, string='开启通讯录修改同步', help='开启通讯录修改时本地同步')
    url = fields.Char(string='回调url',
                      help='在企业微信中接收事件服务器地址为：http://host:port/funenc_wechat/contacts_directory_webhook/回调url')
    token = fields.Char(string='Token')
    EncodingAESKey = fields.Char(string='EncodingAESKey')

    _sql_constraints = [
        ('funenc_wechat_account_code_unique', 'unique(code)', '企业编号必须唯一!'),
        ('funenc_wechat_account_url_unique', 'unique(url)', '回调url必须唯一!'),
    ]

    @api.model
    def is_syning(self):
        '''

        :return:
        '''
        return IS_SYNING

    @api.constrains('url')
    def _check_url(self):
        '''
        检查链接
        :return:
        '''
        for record in self:
            if record.url is not False and len(record.url.split('/')) > 1:
                raise exceptions.ValidationError('回调url中不能出现"/" ')

    @api.onchange('open_syn')
    def _onchange_open_syn(self):
        '''
        是否同步开关
        :return:
        '''
        if not self.open_syn:
            self.url = None
            self.token = None
            self.EncodingAESKey = None

    @api.multi
    def get_contact_client(self, account):
        '''
        取得client
        :param account:
        :return:
        '''
        return WeChatClient(account.corp, account.account_secret)

    @api.model
    def get_client_by_app(self, code, agent_id):
        '''
        :param code:
        :param agent_id:
        :return:
        '''
        account = self.search([('code', '=', code)])
        if account:
            app = self.env['funenc.wechat.apps'].sudo()\
                .search([('account_id', '=', account.id), ('app_agent', '=', agent_id)])
            if app:
                return WeChatClient(app.account_id.corp, app.app_secret)

        return None

    @api.multi
    def sync_wechat(self):
        """
        同步执行改为异步执行
        :param account_id:
        :return:
        """
        global IS_SYNING
        if IS_SYNING:
            raise exceptions.UserError('当前正在同步中，请稍候!')

        IS_SYNING = True
        t = threading.Thread(target=self._sync_wechat, args=(self.id, ))
        t.start()

    @api.model
    def _sync_wechat(self, account_id):
        '''
        同步企业微信部门帐号信息
        :param account_id:
        :return:
        '''
        # 由于主线程env已销毁，创建新env
        global IS_SYNING
        with api.Environment.manage():
            with self.pool.cursor() as new_cr:
                new_cr.autocommit(True)
                self = self.with_env(self.env(cr=new_cr))
                # 根据传入的account_id去查询对应的cropId和secretKey
                start_time = datetime.datetime.now()
                account = self.browse([account_id])
                client = account.get_contact_client(account)
                log_model = self.env['funenc.wechat.log']
                try:
                    # 同步部门信息
                    self.env['funenc.wechat.department'].sync_wechat_department(account, client)

                    # 同步用户信息
                    self.env['funenc.wechat.user'].sync_wechat_users(account, client)

                    # 更新当前部门
                    self.env['funenc.wechat.user'].update_cur_department()

                    end_time = datetime.datetime.now()
                    self.env['funenc.wechat.log']\
                        .log_info(u'同步成功', u'同步成功, 用时{use_time}'
                                  .format(use_time=(end_time-start_time).total_seconds()))
                    IS_SYNING = False
                except WeChatClientException as e:
                    traceback.print_exc()
                    log_model.log_info(u'同步失败', '错误信息：{}'.format(str(e)))
                except Exception as e:
                    traceback.print_exc()
                    log_model.log_info(u'同步失败', '错误信息：{}'.format(str(e)))