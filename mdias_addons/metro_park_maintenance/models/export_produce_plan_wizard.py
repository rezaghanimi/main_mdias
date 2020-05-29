
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class ExportProducePlanWizard(models.TransientModel):
    '''
    导出生产计划
    '''
    _name = 'metro_park_maintenance.export_produce_plan_wizard'
    
    end_month = fields.Many2one(string='结束月份',
                                comodel_name='metro_park_maintenance.month', required=True)
    start_year = fields.Many2one(string='开始年份',
                                 comodel_name='metro_park_maintenance.year', required=True)
    start_month = fields.Many2one(string='开始月份',
                                  comodel_name='metro_park_maintenance.month', required=True)
    end_year = fields.Many2one(string='结束年份',
                               comodel_name='metro_park_maintenance.year', required=True)

    @api.multi
    def on_ok(self):
        '''
        确定按扭点击, 导出对应年月的计划
        :return:
        '''
        return {
            'name': '月计划下载',
            'type': 'ir.actions.act_url',
            'url': '/export_produce_plan/{month_plan_id}'.format(month_plan_id=self.id)
        }

