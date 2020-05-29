# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
from odoo.tools import pycompat

group_cache = None


class ResGroups(models.Model):
    """
        将系统权限组定义为两部分,不是原子权限组就是角色组
        1、角色组，角色组可以包含多个权限组，是权限组的集合
        2、原子权限组该权限组不可以拆分，仅作为角色组的原子成分，是权限管理的基础成分，通过系统定义·
    """
    _inherit = 'res.groups'

    sequence = fields.Integer(index=True, default=0)
    active = fields.Boolean(default=True)
    # 是否是原子权限组，原子权限组表示该组不可以包含其他权限组,仅仅为最基础的权限
    atomic = fields.Boolean(string='Atomic group', default=False, required=True)
    user_count = fields.Integer(compute='_compute_user_count')

    @api.one
    @api.depends('users')
    def _compute_user_count(self):
        self.user_count = len(self.users)

    @api.constrains('implied_ids')
    def check_implied_ids(self):
        '''
        限制原子权限组不能包含其它权限组
        :return:
        '''
        for group in self:
            if group.atomic and len(group.implied_ids) > 0:
                raise UserError('Atomic group, not implied other group')

    _USER_TYPE_IDS = []

    @property
    def user_type_ids(self):
        '''
        :return:
        '''
        if ResGroups._USER_TYPE_IDS:
            return ResGroups._USER_TYPE_IDS
        user_category_id = self.env.ref('base.module_category_user_type').id
        user_type_ids = self.search([('category_id', '=', user_category_id)]).ids
        ResGroups._USER_TYPE_IDS = user_type_ids
        return ResGroups._USER_TYPE_IDS

    @api.multi
    def unlink(self):
        if self.env.user.id != SUPERUSER_ID:
            for re in self:
                if re.atomic:
                    raise UserError('not delete atomic group')
        self.remove_group_by_role_gid([])
        res = super(ResGroups, self).unlink()
        return res

    def make_group_tree_by_category(self, root_categories, parent_path=''):
        """
            生成权限组结构，这里进行一次全局缓存，然后将数据写入全局缓存
        :param root_categories:
        :param parent_path:
        :return:
        """
        tree = []

        for category in root_categories:
            children = []
            # path 便于快捷查询
            path = '%s/%s' % (parent_path, category.name)
            if category.child_ids:
                children += self.make_group_tree_by_category(category.child_ids)
            groups = self.search([('category_id', '=', category.id),
                                  ('atomic', '=', True), ('active', '=', True)])
            for group in groups:
                children.append({
                    'name': _(group.name),
                    'id': '%s-%s' % (group.id, 'group'),
                    'type': 'group',
                    'path': path
                })
            tree.append({
                'type': 'category',
                'id': '%s-%s' % (category.id, 'category'),
                'name': _(category.name),
                'children': children,
                'path': path
            })
        return tree

    def make_group_cache(self):
        self = self.with_context(dict(self.env.context, lang='zh_CN'))
        groups = self.search([('atomic', '=', True), ('active', '=', True), ('id', 'not in', self.user_type_ids)])
        category_ids = groups.mapped('category_id')
        # 查找根类别
        root_category = []
        for category in category_ids:
            while category.parent_id:
                category = category.parent_id
            root_category.append(category)
        tree = self.make_group_tree_by_category(set(root_category))
        other_groups = groups.filtered(lambda re: not re.category_id)
        _child = []
        for gr in other_groups:
            _child.append({
                'name': _(gr.name),
                'id': '%s-%s' % (gr.id, 'group'),
                'type': 'group',
                'path': '其他/%s' % gr.name
            })
        if _child:
            tree.append({
                'type': 'category',
                'id': '%s-%s' % ('0', 'category'),
                'name': '其他',
                'children': _child,
                'path': '其他'
            })

        global group_cache
        group_cache = tree

    @api.model
    def get_group_data(self):
        global group_cache
        if group_cache:
            return group_cache
        else:
            self.make_group_cache()
            return group_cache

    def get_group_inherits(self, gids):
        self.env.cr.execute("""
                                WITH 
                                   RECURSIVE group_imply(gid, hid) AS (
                                       SELECT gid, hid
                                       FROM res_groups_implied_rel
                                       UNION
                                       SELECT i.gid, r.hid
                                       FROM res_groups_implied_rel r
                                       JOIN group_imply i ON (i.hid = r.gid))

                                   SELECT gid, hid FROM  group_imply WHERE  gid IN  %(gids)s
                               """, dict(gids=tuple(gids)))
        group_gid_and_hid_map = self.env.cr.dictfetchall()
        result = {}
        for val in group_gid_and_hid_map:
            result.setdefault(val['gid'], [])
            result[val['gid']].append(val['hid'])
        return result

    def remove_roles_for_user(self, gids, uids):
        """
            当一个用户从该权限移除时候应该移除该用户所有相关权限
        :param uids:
        :return:
        """

        for uid in uids:
            self.env.cr.execute("""
                SELECT gid FROM res_groups_users_rel 
                    WHERE  gid IN (SELECT id FROM  res_groups WHERE atomic !=TRUE AND id IN %(gids)s)
            """, dict(gids=tuple(gids)))
            role_ids = [row[0] for row in self.env.cr.fetchall()]
            group_maps = self.get_group_inherits(role_ids)
            remove_ids = []
            all_hids = {}
            for gid in role_ids:
                remove_ids += group_maps[gid]
            for gval in group_maps.values():
                for hid in gval:
                    all_hids.setdefault(hid, 0)
                    all_hids[hid] += 1
            # 仅仅有一个就删除
            ids = [rid for rid in set(remove_ids) if all_hids[rid] == 1]
            ids += gids
            self._cr.execute("""
                    DELETE FROM res_groups_users_rel WHERE  uid = %(uid)s AND gid IN %(gids)s        
            """, dict(uid=uid, gids=tuple(ids)))

    @api.multi
    def _remove_group_by_role_gid(self, gid, hids):
        """

        :param gid: 角色
        :param hids: 权限<atomic= True> 原子权限
        :return:
        """
        self.env.cr.execute("""
                                          WITH 
                                             RECURSIVE group_imply(gid, hid) AS (
                                                 SELECT gid, hid
                                                 FROM res_groups_implied_rel
                                                 UNION
                                                 SELECT i.gid, r.hid
                                                 FROM res_groups_implied_rel r
                                                 JOIN group_imply i ON (i.hid = r.gid))

                                             SELECT gid, hid FROM  group_imply WHERE  
                                                  hid in %(hids)s
                                         """, dict(hids=tuple(hids)))
        group_gid_and_hid_map = self.env.cr.dictfetchall()
        gid_dict = {}
        # 获取哪些hids被哪些权限继承,也就是包含在哪些角色之中
        for val in group_gid_and_hid_map:
            gid_dict.setdefault(val['hid'], [])
            gid_dict[val['hid']].append(val['gid'])
        for hid, group in gid_dict.items():
            # 查询包响应含权限组的用户
            self.env.cr.execute("""
                   SELECT uid, gid  FROM res_groups_users_rel WHERE 
                          gid  IN (SELECT id FROM  res_groups WHERE atomic !=TRUE AND id IN %(gids)s)
              """, dict(gids=tuple(group)))
            user_group_dict = self.env.cr.dictfetchall()
            user_role = {}
            # 将权限按照用户拆分列表,查询响应用户下面包含该权限的所有角色
            for val in user_group_dict:
                user_role.setdefault(val['uid'], [])
                user_role[val['uid']].append(val['gid'])
            for uid, cgroup in user_role.items():
                # 判断权限要删除的权限角色是否在其中，并且包含这个原子权限的角色仅仅只有一个
                if gid in cgroup and len(cgroup) == 1:
                    self._cr.execute("""
                                         DELETE FROM res_groups_users_rel WHERE  uid = %(uid)s AND gid = %(gid)s   
                                 """, dict(uid=uid, gid=hid))

    def remove_group_by_role_gid(self, implied_ids):
        for group in self:
            remove_gids = set(group.implied_ids.ids) - set(implied_ids)
            if remove_gids:
                self._remove_group_by_role_gid(group.id, remove_gids)

    def write(self, values):

        """
            当一个用户权限仅有一次的时候，该权限应该主动移除
            当该用户其他角色还拥有该权限的时候，该权限不作处理
        :param values:
        :return:
        """

        # 移除该角色所有相关权限
        if values.get('implied_ids'):
            implied_value = values['implied_ids']
            if implied_value[0][0] == 6:
                implied_ids = values['implied_ids'][0][2]
                self.remove_group_by_role_gid(implied_ids)
        self.make_group_cache()
        res = super(ResGroups, self).write(values)
        return res

    @api.depends('category_id.name', 'name')
    def _compute_full_name(self):
        # 仅仅原子权限组name才显示全名
        for group, group1 in pycompat.izip(self, self.sudo()):
            if group1.category_id and group1.atomic:
                group.full_name = '%s / %s' % (group1.category_id.name, group1.name)
            else:
                group.full_name = group1.name

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResGroups, self).create(vals_list)
        self.make_group_cache()
        return res
