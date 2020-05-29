
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class BalanceOffsetWizard(models.Model):
    '''
    修程偏移向导
    '''
    _name = 'metro_park_maintenance.balance_offset_wizard'

    year = fields.Many2one(comodel_name="metro_park_maintenance.year", string='年')
    month = fields.Many2one(comodel_name="metro_park_maintenance.month", string="月")
    offset = fields.Many2one(string='偏移',
                             comodel_name='metro_park_maintenance.plan_config_data')

    @api.multi
    def on_ok(self):
        '''
        确认按扭点击
        :return:
        '''
        dev_id = self.env.context.get('dev_id', None)
        if not dev_id:
            raise exceptions.ValidationError('没有设置设备!')

        record = self.env['metro_park_maintenance.balance_rule_offset'].search(
            [('dev', '=', dev_id)])
        if not record:
            raise exceptions.AccessDenied('没有找到设备')
        record.offset_num = self.offset.index
