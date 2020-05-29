
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UpdateBalanceOffset(models.Model):
    '''
    更新修次时间
    '''
    _name = 'metro_park_maintenance.update_balance_offset'
    
    year = fields.Many2one(string='年',
                           comodel_name='metro_park_maintenance.year')
    month = fields.Many2one(string='月',
                            comodel_name='metro_park_maintenance.month')

    @api.multi
    def on_ok(self):
        '''
        更新修次时间
        :return:
        '''
        year = self.year.val
        month = self.month.val

        self.env['metro_park_maintenance.balance_rule_offset']\
            .update_balance_offset_year_month(year, month)
