
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class YearPlanHistoryInfo(models.TransientModel):
    '''
    年计划历史信息
    '''
    _name = 'metro_park_maintenance.year_plan_history_info'

    plan_id = fields.Many2one(comodel_name="metro_park_maintenance.year_plan", string="年计划")
    # 直接修改的是rule_info中的修次
    rule_infos = fields.Many2many(string='修程信息',
                                  comodel_name='metro_park_maintenance.rule_info',
                                  relation='year_plan_history_and_rule_info_rel',
                                  col1='year_id',
                                  col2='rule_id')
    month = fields.Many2one(string='月份',
                            comodel_name='metro_park_maintenance.month')

    @api.onchange("month")
    def on_change_month(self):
        '''
        取得历史修程记录
        :return:
        '''
        if self.month:
            plan = self.plan_id
            start_date = pendulum.date(plan.year, self.month.val, 1).format('YYYY-MM-DD')

            dev_type_electric_train = \
                self.env.ref('metro_park_base.dev_type_electric_train').id

            # 车辆
            devs = self.env["metro_park_maintenance.train_dev"]\
                .search([('dev_type', '=', dev_type_electric_train)])
            dev_ids = devs.ids

            is_year_plan = self.env.context.get("year", True)
            if is_year_plan:
                rules = self.env["metro_park_maintenance.repair_rule"]\
                    .search([('target_plan_type', '=', 'year'),
                             ('rule_status', '=', 'normal')])
            else:
                rules = self.env["metro_park_maintenance.repair_rule"]\
                    .search([('target_plan_type', 'in', ['year', 'month']),
                             ('rule_status', '=', 'normal')])

            rule_ids = rules.ids
            if is_year_plan:
                sql = 'select distinct on(dev) dev, rule, date, id from metro_park_maintenance_rule_info' \
                      ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
                      'and date < \'{date}\' and active=true and data_source = \'year\' order by dev, date desc'
            else:
                sql = 'select distinct on(dev) dev, rule, date, id from metro_park_maintenance_rule_info' \
                      ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
                      'and date < \'{date}\' and active=true and data_source = \'month\' order by dev, date desc'
            sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                             dev_ids=str(dev_ids).strip('[]'),
                             date=start_date)

            self.env.cr.execute(sql)
            ids = [x[3] for x in self.env.cr.fetchall()]

            self.rule_infos = [(6, 0, ids)]
