
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BackPlanAlarm(models.Model):
    '''
    接车提醒
    '''
    _name = 'metro_park_dispatch.back_plan_alarm'
    _description = '接车提醒'
    _track_log = True
    
    plan_id = fields.Many2one(string='计划',
                              comodel_name='metro_park_dispatch.train_back_plan')

    @api.model
    def alarm(self, plan_id):
        '''
        提醒时间
        :param plan_id:
        :return:
        '''
        plan = self.env['metro_park_dispatch.train_back_plan'].browse(plan_id)
        return {
            "name": '接车提醒，车号{train_no}将到达转换轨!'.format(train_no=plan.base_train_no),
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.back_plan_alarm",
            'view_mode': 'form'
        }
