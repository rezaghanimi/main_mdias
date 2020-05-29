
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchWizard(models.TransientModel):
    '''
    调车向导
    '''
    _name = 'metro_park_dispatch.dispatch_wizard'
    _track_log = True

    method = fields.Selection(string='方式',
                              selection=[('own', '自身动力'), ('engine', '工程车')],
                              default="own")
    dev = fields.Many2one(string='现车',
                          comodel_name='metro_park_dispatch.cur_train_manage')
    engine = fields.Many2one(string='工程车',
                             comodel_name='metro_park_dispatch.cur_train')
    start_trail = fields.Many2one(string='起始股道',
                                  comodel_name='metro_park_base.rails_sec')
    target_rail = fields.Many2one(string='目标轨',
                                  comodel_name='metro_park_base.rails_sec')

    @api.multi
    def on_ok(self):
        '''
        确定创建调车计划
        :return:
        '''
        self.env["metro_park_dispatch.dispatch_request"].create({
            "train": self.dev,
        })
