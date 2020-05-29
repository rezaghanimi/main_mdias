
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RunTrainWizard(models.TransientModel):
    '''
    运行车设置向导
    '''
    _name = 'metro_park_dispatch.run_train_wizard'

    work_shop_day_plan_id = \
        fields.Many2one(comodel_name="metro_park_dispatch.work_shop_day_plan",
                        string="车间日生产计划")
    cur_trains = fields.Many2many(string='现车',
                                  comodel_name='metro_park_dispatch.cur_train_manage',
                                  relation='cur_train_wizard_cur_train_rel',
                                  col1='wizard_id',
                                  col2='cur_train_id')

    @api.multi
    def on_ok(self):
        '''
        ok 按扭点击
        :return:
        '''
        self.work_shop_day_plan_id.run_trains = [(6, 0, self.cur_trains.ids)]

