
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OutPlanAlarm(models.Model):
    '''
    发车计划提醒
    '''
    _name = 'metro_park_dispatch.out_plan_alarm'
    _description = '发车计划提醒'
    _track_log = True
    
    plan_id = fields.Many2one(string='发车提醒',
                              comodel_name='metro_park_dispatch.train_out_plan')

    @api.model
    def alarm(self, plan_id):
        '''
        提醒时间
        :param plan_id:
        :return:
        '''
        plan = self.env['metro_park_dispatch.train_out_plan'].browse(plan_id)
        return {
            "name": '接车提醒，车号{train_no}即将发车!'.format(train_no=plan.base_train_no),
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.back_plan_alarm",
            'view_mode': 'form'
        }
