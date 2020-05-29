
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum


class MonthPlanClearWizard(models.Model):
    '''
    月计划清除向导
    '''
    _name = 'metro_park_maintenance.month_plan_clear_wizard'

    @api.model
    def _get_default(self):
        '''
        取得默认的天
        :return:
        '''
        day1 = self.env.ref('metro_park_maintenance.day_1').id
        return day1

    start_date = fields.Many2one(string='开始日期',
                                 comodel_name="metro_park_maintenance.day",
                                 default=_get_default)

    @api.multi
    def clear_week_datas(self, month_plan_id):
        '''
        清除周计划数据，用于生产计划
        :return:
        '''
        record = self.env["metro_park_maintenance.month_plan"].browse(month_plan_id)
        start_date = pendulum.date(record.year, record.month,
                                   self.start_date.val).format('YYYY-MM-DD')
        infos = self.env["metro_park_maintenance.rule_info"] \
            .search([("date", ">=", start_date),
                     ("date", "<=", str(record.end_date)),
                     ("rule.target_plan_type", '=', "week")])
        infos.write({
            "active": False
        })

    @api.multi
    def clear_month_and_week_datas(self, month_plan_id):
        '''
        清除年月周数据, 年计划如果被删除了可以重新去拉取
        :return:
        '''
        record = self.env["metro_park_maintenance.month_plan"].browse(month_plan_id)
        start_date = pendulum.date(record.year, record.month, self.start_date.val)
        infos = self.env["metro_park_maintenance.rule_info"]\
            .search([("date", ">=", start_date.format('YYYY-MM-DD')),
                     ("date", "<=", str(record.end_date)),
                     ("rule.target_plan_type", 'in', ["year", "month", "week"]),
                     ("plan_id", "=", "metro_park_maintenance.month_plan, {plan_id}".format(
                         plan_id=month_plan_id))])
        infos.write({
            "active": False
        })


