# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Users(models.Model):
    '''
    用户所具有的角色
    '''
    _inherit = 'res.users'

    role_ids = fields.Many2many(comodel_name='res.groups',
                                string="角色",
                                compute='compute_role_ids',
                                inverse='inverse_role_ids',
                                domain=[('atomic', '!=', True)],
                                help="元子权限不构成角色组")

    @api.one
    @api.depends('groups_id')
    def compute_role_ids(self):
        self.role_ids = self.groups_id.filtered(lambda re: not re.atomic)

    @api.multi
    def inverse_role_ids(self):
        # 当前的用户组
        exits_group = self.groups_id.filtered(lambda re: not re.atomic)
        remove_groups = exits_group - self.role_ids
        # 移除权限组
        if remove_groups:
            self.env['res.groups'].remove_roles_for_user(remove_groups.ids, self.ids)
        # 增加权限组
        for gr in (self.role_ids - exits_group):
            users = gr.users.ids + self.ids
            gr.write({'users': [[6, False, users]]})

    @api.multi
    def close_window(self):
        action_id = self.env.ref('odoo_groups_manage.act_odoo_groups_manage_users_menu').id
        return {
            'type': 'ir.actions.client',
            'tag': 'ReloadControllerAndClose',
            'params': {
                'action_ids': [action_id]
            }
        }

    @api.multi
    @api.constrains('groups_id')
    def _check_one_user_type(self):
        pass
