# !user/bin/env python3
# -*- coding: utf-8 -*-
# author: artorias
from . import department
from . import user
from odoo.http import request

class MapWebhook(object):

    def __init__(self, xml_tree):
        '''
        实例化一个map，初始化实例变量
        :param xml_tree: xml解析树
        '''
        self.xml_tree = xml_tree
        self.class_type = xml_tree.find('ChangeType').text.split('_')[1]
        if self.class_type != 'user' and self.class_type != 'party':
            raise Exception('class_type is not user or party', xml_tree.find('ChangeType').text)

    def distribute_class(self):
        '''
        分配处理类进行处理
        :return: 
        '''
        class_map = {
            'party': department.Department,
            'user': user.User
        }
        return class_map[self.class_type](self.xml_tree).get_action()