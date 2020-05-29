# !user/bin/env python3
# -*- coding: utf-8 -*-

from odoo import models, api



class UserExtend(models.Model):
    '''
    用户扩展，增加获取用户权限xml函数
    '''
    _inherit = 'res.users'

    @api.model
    def get_user_xml_groups(self):
        '''
        取得用户权限的xml, 返回字典，方便前端查询
        :return:
        '''
        group_ids = self.env.user.groups_id.ids
        records = self.env['ir.model.data'] \
            .search_read([('model', '=', 'res.groups'), ('res_id', 'in', group_ids)], fields=["complete_name"])
        return {record["complete_name"]: True for record in records}

