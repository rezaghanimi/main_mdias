# -*- coding: utf-8 -*-

from odoo import models


class ExtendResGroup(models.Model):
    _inherit = 'res.groups'

    @staticmethod
    def get_config_info():
        '''
        该函数返回一个dict, 共有4个key,
        key: module_name 当前项目的module名，一般是__manifest__.py中的name对应的值，category_id_list会在此module下搜索相应的id
        key: category_id_list 需要展示group的对应的category的id的列表，这个id不包含自定义的组category的id
        key: custom_group_id 自定义的组category的id
        :return:
        '''
        return {
            'module_name': 'metro_park_base',
            'category_id_list': ['category_metro_park_base'],
            'custom_group_id': 'category_metro_park_base'
        }
