# !user/bin/env python3
# -*- coding: utf-8 -*-

import logging
import threadpool
from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

ACTIVED = '1'
UN_ACTIVED = '4'
DISABLED = '2'
DELETED = '10'


class WechatUser(models.Model):
    '''
    企业微信用户管理
    '''
    _name = 'funenc.wechat.user'
    _rec_name = 'name'
    _description = '企业微信用户'

    user_state = fields.Selection(selection=[(ACTIVED, '已激活'),
                                             (UN_ACTIVED, '未激活'),
                                             (DISABLED, '已禁用'),
                                             (DELETED, '已删除')],
                                  string='企业微信用户状态',
                                  default='4',
                                  readonly=True)

    name = fields.Char('名称', required=True, readonly=True)
    wx_userid = fields.Char(string='微信userid', required=True, readonly=True)
    user_id = fields.Many2one('res.users', ondelete='cascade', readonly=True)
    mobile = fields.Char('电话', readonly=True)
    email = fields.Char('邮箱', readonly=True)
    avatar = fields.Char('头像', readonly=True)
    job = fields.Char('职务', readonly=True)

    custom_json_info = fields.Text('自定义成员信息',
                                   readonly=True)  # 提取自定义内容时需要json.loads转换

    can_login = fields.Boolean(string='允许扫码登录后台',
                               default=False)

    department_ids = fields.Many2many(comodel_name='funenc.wechat.department',
                                      relation='wechat_user_department_rel',
                                      column1='user_id',
                                      column2='department_id',
                                      string='部门',
                                      readonly=True)

    cur_department = fields.Many2one(comodel_name="funenc.wechat.department",
                                     string="当前部门",
                                     store=True,
                                     compute="_compute_cur_department",
                                     ondelete='set null')

    first_department_id = fields.Many2one(
        comodel_name="funenc.wechat.department",
        string='主部门',
        store=True,
        compute="_com_get_first_department",
        readonly=True,
        ondelete='set null')

    account_id = fields.Many2one(comodel_name='funenc.wechat.account',
                                 required=True,
                                 readonly=True)
    color = fields.Integer()
    active = fields.Boolean(string="状态", default=True)

    @api.model
    def update_cur_department(self):
        '''
        更新用户当前部门
        :return:
        '''
        records = self.search([])
        for record in records:
            if len(record.department_ids) > 0:
                record.cur_department = record.department_ids[0]

    @api.depends("department_ids")
    def _compute_cur_department(self):
        '''
        计算当前所属部门
        :return:
        '''
        for record in self:
            if not record.cur_department and len(record.department_ids) > 0:
                record.cur_department = record.department_ids[0]

    @api.onchange('user_id')
    def onchange_user(self):
        self.update({
            'name': self.user_id.name,
            'mobile': self.user_id.mobile,
            'email': self.user_id.email
        })

    @api.depends('department_ids')
    def _com_get_first_department(self):
        for record in self:
            if len(record.department_ids) > 0:
                record.first_department_id = record.department_ids[0]

    @api.model
    def change_can_login(self):
        '''
        变更扫码登录后台权限，可批量操作
        :return: 
        '''
        ids = self._context['active_ids']
        for tmp_id in ids:
            record = self.browse([tmp_id])
            # 更改状态
            record.write({'can_login': not record.can_login})

    def crete_users(self, users):
        with api.Environment.manage():
            with self.pool.cursor() as new_cr:
                _logger.info("thread user syn user, count: {count}!".format(count=len(users)))
                current_self = self.with_env(self.env(cr=new_cr))
                current_self.env['res.users'].create(users)
                self._cr.commit()

    @api.model
    def sync_wechat_users(self, account, client):
        '''
        同步企业微信用户
        :param account: 企业微信帐号
        :param client: 企业微信client实例
        :return:
        '''
        department_model = self.env['funenc.wechat.department']
        user_model = self.env['funenc.wechat.user']
        parent_departments = department_model.sudo().search([
            ('parent_id', '=', None), ('account_id', '=', account.id)
        ])
        local_values = {v['wx_userid']: v for v in self.sudo().search_read(
            domain=[('account_id', '=', account.id)],
            fields=['user_state', 'wx_userid', 'name', 'mobile', 'email', 'job', 'avatar',
                    'department_ids', 'custom_json_info'])}

        local_departments = department_model.sudo().search([])
        department_cache = {}
        for department in local_departments:
            department_cache[department['wx_id']] = department.id

        def wx_department_to_local(department_ids):
            '''
            部门编号到部门id
            :param department_ids: 从微信取得的部门ids
            :return:
            '''
            rst = []
            for tmp_order in department_ids:
                if tmp_order not in department_cache:
                    raise exceptions.Warning(u'the order is not in cache')
                rst.append(department_cache[tmp_order])
            return rst

        def _sync_imply(wx_users_vals):
            ''''
            同步用户
            '''
            config_model = self.env['res.config.settings']
            batch_num = config_model.get_values().get('funenc_wechat.batch_num', 100)
            syn_thread_num = config_model.get_values().get('funenc_wechat.syn_thread_num', 5)

            create_list = []
            create_cache = {}

            for server_val in wx_users_vals:
                wx_userid = server_val['userid']
                server_departments = server_val.get('department', [])
                # if someone on server and in local
                if wx_userid in local_values:
                    if server_val.get('extattr', {'attrs': False})['attrs'] is False or \
                            len(server_val.get('extattr', {'attrs': False})['attrs']) == 0:
                        custom_json = False
                    else:
                        custom_json = str(server_val.get('extattr', {'attrs': False})['attrs'])

                    temp_server_value = {
                        'name': server_val['name'],
                        'mobile': server_val.get('mobile', False),
                        'job': server_val.get('position', False),
                        'email': server_val.get('email', False),
                        'user_state': str(server_val['status']),
                        'avatar': server_val.get('avatar', False),
                        'custom_json_info': custom_json,
                        'wx_userid': wx_userid,
                        'active': True
                    }

                    custom_json = False
                    if local_values[wx_userid].get('custom_json_info', False):
                        custom_json = str(local_values[wx_userid].get('custom_json_info'))

                    temp_local_value = {
                        'name': local_values[wx_userid]['name'],
                        'mobile': local_values[wx_userid].get('mobile', False),
                        'job': local_values[wx_userid].get('job', False),
                        'email': local_values[wx_userid].get('email', False),
                        'user_state': local_values[wx_userid]['user_state'],
                        'avatar': local_values[wx_userid].get('avatar', False),
                        'custom_json_info': custom_json,
                        'wx_userid': local_values[wx_userid].get('wx_userid', False),
                        'active': local_values[wx_userid].get('active', False),
                    }
                    local_departments_ids = local_values[wx_userid].get('department_ids', [])
                    server_departments_ids = wx_department_to_local(server_departments)

                    # if have difference
                    if len(set(local_departments_ids).symmetric_difference(set(server_departments_ids))) != 0 or \
                            len(set(temp_server_value.items()).symmetric_difference(
                                set(temp_local_value.items()))) != 0:
                        temp_server_value['department_ids'] = [[6, 0, server_departments_ids]]
                        user_model.sudo().browse(local_values[wx_userid]['id'])\
                            .sudo().write(temp_server_value)

                    # un registry local value, for update local status
                    del local_values[wx_userid]

                # if someone on server but not in local so we add it to local
                else:
                    new_user = {
                        'account_id': account.id,
                        'name': server_val['name'],
                        'wx_userid': wx_userid,
                        'job': server_val.get('position', False),
                        'email': server_val.get('email', False),
                        'mobile': server_val.get('mobile', False),
                        'avatar': server_val.get('avatar', False),
                        'custom_json_info': server_val.get('extattr', {'attrs': False})['attrs'],
                        'user_state': str(server_val['status']),
                        'department_ids': server_departments
                    }
                    create_list.append(new_user)
                    create_cache[wx_userid] = new_user

            # 创建用户
            _logger.info("开始构建系统用户数据!")
            new_wx_user_ids = [item['wx_userid'] for item in create_list]
            old_users = self.env['res.users'].sudo() \
                .search([('login', 'in', new_wx_user_ids), '|',
                         ('active', '=', False),
                         ('active', '=', True)])
            # 这样的话有个问题就是wx_login和用户唯一绑定了
            old_user_cache = {old_user['wx_login']: old_user for old_user in old_users}
            user_create_list = []
            wx_login_ar = old_users.mapped("wx_login")
            for tmp in create_list:
                wx_login = tmp['wx_userid']
                old_name = '{wx_login}_old_9527'.format(wx_login=wx_login)
                if wx_login not in wx_login_ar and old_name not in wx_login_ar:
                    user_create_list.append({
                        'login': wx_login,
                        'wx_login': wx_login,
                        'email': tmp['email'],
                        'mobile': tmp['mobile'],
                        'name': tmp['name'],
                        'password': wx_login,
                        'active': True
                    })
                else:
                    # 更新老的用户, 而不是新关联的用户
                    if old_name in wx_login_ar:
                        local_user = old_user_cache[old_name]
                    else:
                        local_user = old_user_cache[wx_login]

                    local_user_val = {
                        'wx_login': wx_login,
                        'email': local_user['email'],
                        'mobile': local_user['mobile'],
                        'name': local_user['name'],
                        'active': local_user['active']
                    }
                    server_user_val = {
                        'wx_login': wx_login,
                        'email': tmp['email'],
                        'mobile': tmp['mobile'],
                        'name': tmp['name'],
                        'active': True
                    }
                    # 做下比较,防止重复写入
                    if len(set(local_user_val).symmetric_difference(set(server_user_val))):
                        old_user_cache[wx_login].sudo().write(server_user_val)

            if len(user_create_list) > 0:
                batch_num = 100
                tmp_list = []
                while len(user_create_list) > 0:
                    tmp = user_create_list[0:batch_num]
                    user_create_list = user_create_list[batch_num:]
                    tmp_list.append(tmp)

                _logger.info("begin syn user use thread pool!")

                pool = threadpool.ThreadPool(syn_thread_num)
                requests = threadpool.makeRequests(self.crete_users, tmp_list)
                [pool.putRequest(req) for req in requests]
                # 等待任务执行完成
                pool.wait()

            _logger.info("thread pool syn user success!")
            all_users = self.env['res.users'].sudo().search_read([], fields=['wx_login', 'id'])
            all_user_id_cache = {}
            for user in all_users:
                all_user_id_cache[user['wx_login']] = user['id']

            for item in create_list:
                item['user_id'] = all_user_id_cache[item['wx_userid']]
                item['department_ids'] = [[6, 0, wx_department_to_local(item['department_ids'])]]

            if len(create_list) < batch_num:
                self.create(create_list)
            else:
                while len(create_list) > 0:
                    tmp = create_list[0:batch_num]
                    _logger.info("batch create user {num}!".format(num=len(tmp)))
                    create_list = create_list[batch_num:]
                    self.sudo().create(tmp)

        # 可以出现多个顶级成员
        for parent in parent_departments:
            wx_parent_id = parent.wx_id
            server_values = client.user.list(department_id=wx_parent_id,
                                             fetch_child=True)
            _sync_imply(server_values)

        # 删除不存在的用户
        if len(local_values) > 0:
            mis_ids = [item['id'] for item in local_values.values()]
            self.browse(mis_ids) \
                .sudo() \
                .write({'user_state': DELETED, 'can_login': False})
            wx_user_ids = [item['wx_userid'] for item in local_values.values()]
            self.env['res.users'].sudo() \
                .search([('wx_login', 'in', wx_user_ids)]).sudo().write({'active': False})

        # 更新wx_user_ids
        _logger.info("begin deal user relation!")
        user_count = user_model.sudo().search_count([])
        for offset in range(0, user_count + 100, 100):
            wx_users = user_model.search([], offset=offset, limit=100)
            for tmp_user in wx_users:
                tmp_user.user_id.wx_user_ids = [(4, tmp_user.id)]
                if not tmp_user.user_id.cur_wx_user_id:
                    tmp_user.user_id.cur_wx_user_id = tmp_user.id




