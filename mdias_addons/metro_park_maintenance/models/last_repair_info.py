# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class LastRepairInfo(models.Model):
    '''
    最新修程信息
    '''
    _name = 'metro_park_maintenance.last_repair_info'
    
    repair_date = fields.Date(string='维修日期')
    rule = fields.Many2one(string='修程',
                           comodel_name='metro_park_maintenance.repair_rule')
    repair_num = fields.Char(string='修次')

    @api.model
    def get_last_repair_action(self, plan_id, start_date):
        '''
        取得历史修程记录
        :return:
        '''
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train').id

        # 车辆
        devs = self.env["metro_park_maintenance.train_dev"]\
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids

        # 规程
        rules = self.env["metro_park_maintenance.repair_rule"]\
            .search([('target_plan_type', '=', 'year'), ('rule_status', '=', 'normal')])
        rule_ids = rules.ids

        sql = 'select distinct on(dev) dev, rule, date, id from metro_park_maintenance_rule_info' \
              ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
              'and date < \'{date}\' and plan_id=\'{plan_id}\' order by dev, date desc'
        sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                         dev_ids=str(dev_ids).strip('[]'),
                         date=start_date,
                         plan_id=plan_id)
        self.env.cr.execute(sql)
        ids = [x[3] for x in self.env.cr.fetchall()]

        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.rule_info",
            'view_mode': 'form, tree',
            "target": "new",
            'context': {},
            'domain': [('id', 'in', ids)],
            "views": [
                [self.env.ref('metro_park_maintenance.dev_year_rule_edit').id, 'tree'],
                [False, "form"]]
        }
