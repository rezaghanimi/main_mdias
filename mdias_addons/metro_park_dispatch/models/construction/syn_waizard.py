# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PlanSynWizard(models.TransientModel):
    '''
    计划同步向导
    '''
    _name = 'metro_park_dispatch.wizard.plan_syn'

    syn_date = fields.Date(string='同步日期',
                           default=fields.Date.today)

    @api.one
    def button_confirm(self):
        '''
        确认按扭点击
        :return:
        '''
        obj = self.env['metro_park_dispatch.construction_plan']
        obj.corn_synchronization(self.syn_date)
