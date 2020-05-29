
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChangeTimeTableWizard(models.TransientModel):
    '''
    修改运行图向导
    '''
    _name = 'metro_park_dispatch.change_time_table_wizard'
    _description = '修改运行图向导'
    _track_log = True
    
    time_table = fields.Many2one(string='运行图',
                                 comodel_name='metro_park_base.time_table',
                                 required=True)

    @api.multi
    def on_ok(self):
        '''
        确认按扭点击
        :return:
        '''
        active_id = self.env.context.get('active_id')
        if active_id:
            record = self.env['metro_park_dispatch.nor_time_table_config'].browse(active_id)
            record.time_table = self.time_table
        return False
