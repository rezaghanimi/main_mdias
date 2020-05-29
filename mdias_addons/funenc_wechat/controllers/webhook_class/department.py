# !user/bin/env python3
# -*- coding: utf-8 -*-
# author: artorias
from odoo.http import request

class Department(object):
    '''
    通讯录变更事件-部门变更，处理函数必须返回字符串'success'返回给企业微信的请求，不然好像会重复发送请求
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

    def create_party(self):
        '''
        新增部门事件
        :return: 
        '''
        self.check_account()
        # 企业微信传入的部门id即为系统内的部门编号
        dep_order = self.xml_tree.find('Id').text
        dep_name = self.xml_tree.find('Name').text
        parent_dep_order = None if self.xml_tree.find('ParentId') is None else self.xml_tree.find('ParentId').text
        parent_dep = request.env['funenc.wechat.department'].sudo().search(
            [('wx_id', '=', parent_dep_order), ('account_id', '=', self.account.id)])
        request.env['funenc.wechat.department'].sudo().create({
            'account_id': self.account.id,
            'name': dep_name,
            'wx_id': dep_order,
            'wx_parent_id': parent_dep_order,
            'parent_id': None if len(parent_dep) == 0 else parent_dep.id
        })
        return 'success'

    def delete_party(self):
        '''
        删除部门事件
        :return: 
        '''
        self.check_account()
        dep_order = self.xml_tree.find('Id').text
        request.env['funenc.wechat.department'].sudo().search([
            ('wx_id', '=', dep_order), ('account_id', '=', self.account.id)]).unlink()
        return 'success'

    def update_party(self):
        '''
        更新部门事件
        :return: 
        '''
        self.check_account()
        dep_order = self.xml_tree.find('Id').text
        word_dict = dict(name='Name', wx_parent_id='ParentId')
        params_dict = {}
        for key in word_dict:
            if self.xml_tree.find(word_dict[key]) is not None:
                # 父部门单独处理
                if key == 'wx_parent_id':
                    params_dict[key] = self.xml_tree.find(word_dict[key]).text
                    parent_dep = request.env['funenc.wechat.department'].sudo().search(
                        [('wx_id', '=', self.xml_tree.find(word_dict[key]).text),
                         ('account_id', '=', self.account.id)])
                    params_dict['parent_id'] = None if len(parent_dep) == 0 else parent_dep.id
                else:
                    params_dict[key] = self.xml_tree.find(word_dict[key]).text
        if len(params_dict) != 0:
            request.env['funenc.wechat.department'].sudo().search([
                ('wx_id', '=', dep_order), ('account_id', '=', self.account.id)]).sudo().write(params_dict)
        return 'success'
