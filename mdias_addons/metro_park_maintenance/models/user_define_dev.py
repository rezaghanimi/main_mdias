
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UserDefineDev(models.Model):
    '''
    用户指定设备
    '''
    _name = 'metro_park_maintenance.user_define_dev'
    
    dev = fields.Many2one(
        string='用户指定设备',
        comodel_name='metro_park_maintenance.train_dev',
        required=True)

    @api.multi
    def on_ok(self):
        '''
        用户指定设备确定
        :return:
        '''
        plan_info_id = self.env.context.get('plan_info_id')
        plan_info = self.env['metro_park_maintenance.rule_info'].browse(plan_info_id)
        # onchange没有触发，这里强制指定
        plan_info.user_define_dev = self.dev.id
        plan_info.dev = self.dev.id
