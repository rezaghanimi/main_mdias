# !user/bin/env python3
# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class WechatDepartment(models.Model):
    ''''
    企业微信部门
    '''

    _name = 'funenc.wechat.department'
    _rec_name = 'name'
    _description = '部门'
    _order = 'account_id asc, parent_path asc'
    _parent_store = True
    _parent_order = 'wx_id'

    account_id = fields.Many2one(comodel_name='funenc.wechat.account',
                                 required=True,
                                 string="企业帐号")
    name = fields.Char(string='部门名称',
                       required=True,
                       readonly=True)
    wx_id = fields.Integer(string='部门编号',
                           required=True,
                           readonly=True)
    wx_parent_id = fields.Integer(string='父部门编号',
                                  readonly=True)
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(comodel_name='funenc.wechat.department',
                                string='父部门',
                                ondelete='cascade')
    child_ids = fields.One2many(comodel_name='funenc.wechat.department',
                                inverse_name='parent_id',
                                string='子部门')
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    properties = fields.Many2many(string='部门属性',
                                  comodel_name='funenc_wechat.property',
                                  relation="department_property_rel",
                                  column1="department_id",
                                  column2="property_id")

    users = fields.Many2many(
        comodel_name='funenc.wechat.user',
        relation='funenc_wechat_user_department_rel',
        column1='department_id',
        column2='user_id',
        string='企业微信用户',
        readonly=True)

    def sync_wechat_department(self, account, client):
        '''
        写入部门信息
        :param account: funenc.wechat.account的一条记录
        :param client: wechat的连接client
        :return: 
        '''
        server_values = client.department.get()
        local_values = {row['wx_id']: row for row in self.sudo().search_read(
            [('account_id', '=', account.id)],
            ['name', 'wx_id', 'wx_parent_id'])}

        _logger.info('start syn department')

        create_list = []
        for server_value in server_values:
            # 如果用户同时在本地、远程
            department_id = server_value['id']
            if server_value['id'] in local_values:
                temp_server_value = {
                    'name': server_value.get('name', False),
                    'wx_parent_id': server_value['parentid'],
                    'wx_id': department_id
                }
                temp_local_value = {
                    'name': local_values[department_id]['name'],
                    'wx_parent_id': local_values[department_id]['wx_parent_id'],
                    'wx_id': local_values[department_id]['wx_id']
                }

                # if have difference, update it
                if len(set(temp_server_value.items()).symmetric_difference(set(temp_local_value.items()))) != 0:
                    self.sudo().browse(local_values[department_id]['id']).sudo().write(temp_server_value)

                # un registry local value
                del local_values[department_id]

            # if someone on server but not in local so we add it to local
            else:
                # add local department
                value = {
                    'name': server_value['name'],
                    'wx_id': department_id,
                    'wx_parent_id': server_value['parentid'],
                    'account_id': account.id
                }
                create_list.append(value)

        batch_num = self.env['res.config.settings'].get_values().get('batch_num') | 50
        if len(create_list) < batch_num:
            self.sudo().create(create_list)
        else:
            while len(create_list) > 0:
                tmp = create_list[0:batch_num]
                create_list = create_list[batch_num:]
                _logger.info('batch create department...{num}!'.format(num=len(create_list)))
                self.sudo().create(tmp)

        # update the local status
        if len(local_values) > 0:
            mismatch_ids = [item['id'] for item in local_values.values()]
            self.sudo().browse(mismatch_ids).sudo().unlink()

        # update the parent_id
        department_cache = {}
        # fix 同步多个企业微信导致部门混乱
        records = self.search([('account_id', '=', account.id)])
        for record in records:
            department_cache[record.wx_id] = record

        for record in records:
            if record.wx_parent_id:
                record.sudo().write({
                    'parent_id': department_cache[record.wx_parent_id].id if record.wx_parent_id is not None else None
                })

    @api.model
    def get_tree_data(self):
        '''
        取得数形数据
        :return:
        '''
        ret_records = []
        # 按照account_id 进行分组，
        accounts = super(WechatDepartment, self).search([]).mapped('account_id')
        for account in accounts.ids:
            pid_records = super(WechatDepartment, self).search_read(
                [('parent_id', '=', False), ('account_id', '=', account)])
            records = super(WechatDepartment, self).search_read([('account_id', '=', account)])
            records_cache = {record['id']: record for record in records}
            for record in records:
                parent = record['parent_id'] and record['parent_id'][0]
                if parent in records_cache:
                    records_cache[parent].setdefault(
                        'children', []).append(record)

            def get_sub_ids(pid):
                if pid in records_cache:
                    tmp_record = records_cache[pid]
                    if 'children' in tmp_record:
                        children = tmp_record['children']
                        for child in children:
                            ret_records.append(child)
                            get_sub_ids(child['id'])

            for pid_record in pid_records:
                ret_records.append(pid_record)
                get_sub_ids(pid_record['id'])

        return ret_records

    @api.model
    def get_children_dep_ids(self, dep_id):
        '''
        获取当前部门的所有子部门和自身id的list
        :param dep_id:
        :return:
        '''
        dep = self.browse(dep_id)
        children_dep = self.search([('parent_path', '=like', dep.parent_path + '%')])
        return children_dep.ids

    @api.model
    def get_sub_departments_info(self, department_id):
        '''
        tree页获取用户树结构
        :param department_id: 部门id
        :return:
        '''
        records = self.search([('parent_id', '=', department_id)])
        result = [{
            'id': i.id,
            'name': i.name,
            'leaf': True if len(i.child_ids) == 0 else False,
            'parent_left': i.parent_left,
            'parent_right': i.parent_right} for i in records]
        return result
