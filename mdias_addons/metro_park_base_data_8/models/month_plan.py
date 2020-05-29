# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class TenMonthPlan(models.Model):
    '''
    月计划, 用计划计算的时候才将年计划的数据拿出来，然后更新. 月计划重新计算规则，
    找到最后执行的计划，之后的以此作为历史记录，然后进行偏移。
    '''
    _inherit = 'metro_park_maintenance.month_plan'

    def _get_work_class_domain(self):
        '''
        取和工班domain
        :return:
        '''
        return self.env['funenc.wechat.department'].get_work_class_domain()

    work_class = fields.Many2one(comodel_name="funenc.wechat.department",
                                 domain=_get_work_class_domain,
                                 string="工班")
