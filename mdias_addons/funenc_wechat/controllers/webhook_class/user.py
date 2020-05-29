# !user/bin/env python3
# -*- coding: utf-8 -*-
# author: artorias
from odoo.http import request


class User(object):
    '''
    通讯录变更事件-人员变更，处理函数必须返回字符串'success'返回给企业微信的请求，不然好像会重复发送请求
    '''

    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.action_type = xml_tree.find('ChangeType').text
        self.corp = None
        self.account = None

    def check_account(self):
        '''
        检查企业账号是否唯一
        :return: 
        '''
        self.corp = [] if self.xml_tree.find('ToUserName') is None else self.xml_tree.find('ToUserName').text,
        self.account = request.env['funenc.wechat.account'].sudo().search([('corp', 'in', self.corp)])
        account_num = len(self.account)
        assert account_num == 1, "not find account of the corp"
        return

    def get_action(self):
        '''
        根据self.class_type的值调用相应的处理函数
        :return: 
        '''
        return getattr(self, self.action_type)()

    def create_user(self):
        '''
        新增成员事件
        :return: 
        '''
        self.check_account()
        params_dict = dict(
            corp=self.corp,
            wx_userid=None if self.xml_tree.find('UserID') is None else self.xml_tree.find('UserID').text,
            name=None if self.xml_tree.find('Name') is None else self.xml_tree.find('Name').text,
            mobile=None if self.xml_tree.find('Mobile') is None else self.xml_tree.find('Mobile').text,
            job=None if self.xml_tree.find('Position') is None else self.xml_tree.find('Position').text,
            email=None if self.xml_tree.find('Email') is None else self.xml_tree.find('Email').text,
            user_state=None if self.xml_tree.find('Status') is None else self.xml_tree.find('Status').text,
            avatar=None if self.xml_tree.find('Avatar') is None else self.xml_tree.find('Avatar').text,
            department=[] if self.xml_tree.find('Department') is None else self.xml_tree.find(
                'Department').text.split(','),
        )
        # 绑定部门 the departments
        records = request.env['funenc.wechat.department'].sudo().search(
            [('wx_id', 'in', params_dict['department'])])
        ids = [[6, 0, [i['id'] for i in records]]]
        # 创建user
        user = request.env['res.users'].sudo().create({
            'login': params_dict['wx_userid'],
            'wx_login': params_dict['wx_userid'],
            'email': params_dict['email'],
            'mobile': params_dict['mobile'],
            'name': params_dict['name'],
            'password': '000000'
        })
        # 创建wx_user
        value = {
            'user_id': user['id'],
            'account_id': self.account.id,
            'name': params_dict['name'],
            'wx_userid': params_dict['wx_userid'],
            'job': params_dict['job'],
            'email': params_dict['email'],
            'mobile': params_dict['mobile'],
            'user_state': str(params_dict['user_state']),
            'avatar': params_dict['avatar'],
            'department_ids': ids
        }
        request.env['funenc.wechat.user'].sudo().create(value)
        return 'success'

    def delete_user(self):
        '''
        删除成员事件
        :return: 
        '''
        self.check_account()
        wx_userid = None if self.xml_tree.find('UserID') is None else self.xml_tree.find('UserID').text
        wx_user = request.env['funenc.wechat.user'].sudo().search(
            [('wx_userid', '=', wx_userid), ('account_id', '=', self.account.id)])
        if len(wx_user) == 0:
            return 'success'
        wx_user.sudo().write({
            'user_state': '10',
            'can_login': False,
        })
        user = request.env['res.users'].sudo().search([('wx_login', '=', wx_userid)])
        user.sudo().write({
            'active': False
        })
        return 'success'

    def update_user(self):
        '''
        更新成员信息事件
        :return: 
        '''
        self.check_account()
        wx_userid = self.xml_tree.find('UserID').text
        word_dict = dict(
            name='Name', mobile='Mobile', job='Position', email='Email', user_state='Status',
            avatar='Avatar', department_ids='Department', wx_userid='NewUserID'
        )
        params_dict = {}
        for key in word_dict:
            if self.xml_tree.find(word_dict[key]) is not None:
                # 部门字段单独处理
                if key == 'department_ids':
                    records = request.env['funenc.wechat.department'].sudo().search(
                        [('wx_id', 'in', self.xml_tree.find(word_dict[key]).text.split(','))])
                    ids = [[6, 0, [i['id'] for i in records]]]
                    params_dict[key] = ids
                else:
                    params_dict[key] = self.xml_tree.find(word_dict[key]).text
        # 更新user
        if len(params_dict) != 0:
            request.env['funenc.wechat.user'].sudo().search(
                [('account_id', '=', self.account.id), ('wx_userid', '=', wx_userid)]).sudo().write(params_dict)
        return 'success'