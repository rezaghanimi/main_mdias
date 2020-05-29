# -*- coding: utf-8 -*-
import random
from odoo.tests.common import TransactionCase


class TestWechat(TransactionCase):

    def setUp(self):
        '''
        数据初始化，创建测试企业账户，获取到微信的部门信息和顶级部门ID
        :return:
        '''
        super(TestWechat, self).setUp()
        self.account = self.funenc_account = self.env['funenc.wechat.account'].create({
            'name': 'test_funenc',
            'code': 'test_001',
            'corp': 'wwc4cf9cc042245fb4',
            'account_secret': '3CD0M37kCrwMEKfCQ3BGvu6Dg4XknnskhIprSrjpPMw',
        })
        self.client = self.account.get_contact_client(self.account)
        self.wx_departments = self.client.department.get()  # {'name','id','parentid'}
        self.parent_departments = []
        self.User = self.env['cdtct.wechat.user']
        self.Department = self.env['funenc.wechat.department']
        for department in self.wx_departments:
            if bool(department['parent_id']) is False:
                self.parent_departments.append(department['id'])
        print('start test 微信')

    def dict_2_domain(self, values):
        """
        将字典对象转换为odoo 的domain条件格式
        :param values: 字典对象
        :return: domain
        """
        domain = []
        for k,v in values.items():
            tmp = (k,'=',v)
            domain.append(tmp)
        return domain

    def get_wx_department_data(self):
        """
        获取微信的部门数据用作对比的源
        :return: list [微信部门数据序列，本地部门字段信息]
        """
        department_fields_rel = {
            'name': 'name',
            'wx_id': 'id',
            'wx_parent_id': 'parentid'
        } # 字段对应关系，本地为键，微信为值
        server_values = self.wx_departments
        wx_values = [] # 微信部门数据序列化为本地格式
        for server_value in server_values:
            department_tmp = {}
            for lfield, sfield in department_fields_rel.items():
                department_tmp[lfield] = server_value[sfield]
            wx_values.append(department_tmp)
        return [wx_values,list(department_fields_rel.keys())]

    def test_wx_department_empty(self):
        """
        部门同步测试用例：
            没有部门信息的同步
        :return: 
        """
        domain = [('account_id', '=', self.account.id)]
        wx_values, lfields = self.get_wx_department_data()
        self.Department.sync_wechat_department(self.account, self.client)
        local_departmen_count = self.Department.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.Department.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')

    def test_wx_department_same(self):
        """
        部门同步测试用例：
            有部分相同信息的同步
        :return: 
        """
            # 创建相同的记录值
        exist_value = [
            {
                'name': '主部门',
                'wx_id': 1,
                'account_id': self.account.id
            },
            {
                'name': '测试部门',
                'wx_id': 2,
                'wx_parent_id': 1,
                'account_id': self.account.id
            }
        ]
        local_values = self.Department.create(exist_value)
        domain = [('account_id', '=', self.account.id)]
        wx_values, lfields = self.get_wx_department_data()
        self.Department.sync_wechat_department(self.account, self.client)
        local_departmen_count = self.Department.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.Department.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')

    def test_wx_department_diff(self):
        """
        部门同步测试用例：
            有部不相同信息的同步
        :return: 
        """
        # 创建不同的记录值
        exist_value = [
            {
                'name': '主部门',
                'wx_id': 100,
                'account_id': self.account.id
            },
            {
                'name': '测试部门',
                'wx_id': 101,
                'wx_parent_id': 100,
                'account_id': self.account.id
            }
        ]
        local_values = self.Department.create(exist_value)
        domain = [('account_id', '=', self.account.id)]
        wx_values, lfields = self.get_wx_department_data()
        self.Department.sync_wechat_department(self.account, self.client)
        local_departmen_count = self.Department.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.Department.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')

    def get_wx_user_data(self):
        """
        获得序列后的微信用户信息和比较值的字段
        :return: 
        """
        user_fields_rel = {
            'name': 'name',
            'wx_userid': 'userid',
            'job': 'position',
            'email': 'email',
            'mobile': 'mobile',
            'avatar': 'avatar',
            'user_state': 'status' # 微信数据不是字符类型，需要转换
        } # 字段对应关系，本地为键，微信为值
        server_values = self.wx_departments
        wx_values = []
        for parent in self.parent_departments:
            server_values += self.client.user.list(department_id=parent,
                                             fetch_child=True)
        for server_value in server_values:
            user_tmp = {}
            for lfield, sfield in user_fields_rel.items():
                user_tmp[lfield] = server_value[sfield]
            wx_values.append(user_tmp)
        wx_values = list(set(wx_values)) # 去重
        return [wx_values,list(user_fields_rel.keys())]

    def test_wx_user_same(self):
        """
        微信用户信息同步测试用例
            有部分相同信息的同步
        :return: 
        """
        exist_value = [
            {
                'name': '陈驰',
                'wx_userid': 'ChenChi',
                'job': '综合管理部部长',
                'email': 'chi.chen@funenc.com',
                'mobile': '13548025619',
                'avatar': 'http://p.qlogo.cn/bizmail/7OIT6VxDAJjEkXAp9sOib57Vjn9erIKLL17Fer2psHxpiacYzEUjlGEg/0',
                'user_state': '1'
            }
        ]
        local_value = self.User.create(exist_value)
        domain = [('account_id', '=', self.account.id)]
        wx_values, lfields = self.get_wx_user_data()
        self.User.sync_wechat_users(self.account, self.client)
        local_departmen_count = self.User.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.User.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')

    def test_wx_user_empty(self):
        """
        微信用户信息同步测试用例
            没有用户信息的同步
        :return: 
        """
        domain = [('account_id', '=', self.account.id)]
        wx_values, lfields = self.get_wx_user_data()
        self.User.sync_wechat_users(self.account, self.client)
        local_departmen_count = self.User.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.User.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')

    def test_wx_user_diff(self):
        """
        微信用户信息同步测试用例
            有部分不同信息的同步
        :return: 
        """
        exist_value = [
            {
                'name': 'Grit',
                'wx_userid': 'Grit',
                'job': '开发工程师',
                'email': 'grit@163.com',
                'mobile': '123456789',
                'avatar': 'http://p.qlogo.cn/bizmail/7OIT6VxDAJjEkXAp9sOib57Vjn9erIKLL17Fer2psHxpiacYzEUjlGEg/0',
                'user_state': '2'
            }
        ]
        local_value = self.User.create(exist_value)
        domain = [('account_id', '=', self.account.id),('user_state', '!=', '10')]
        wx_values, lfields = self.get_wx_user_data()
        self.User.sync_wechat_users(self.account, self.client)
        local_departmen_count = self.User.search_count(domain)
        self.assertEqual(local_departmen_count, len(wx_values), '部门同步数据与微信数据记录数不符！')
        for wx_value in wx_values:
            local = self.User.search(self.dict_2_domain(wx_value+domain))
            self.assertEqual(len(local), 1, '同步后，本地数据与微信数据不匹配！')