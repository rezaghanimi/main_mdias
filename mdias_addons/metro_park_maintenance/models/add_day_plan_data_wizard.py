# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum
import time
from datetime import datetime, timedelta


class AddDayPlanDataWizard(models.TransientModel):
    '''
    添加日计划数据向导
    '''
    _name = 'metro_park_maintenance.add_day_plan_data_wizard'

    day_plan_id = fields.Many2one(string="所属日计划",
                                  comodel_name="metro_park_maintenance.day_plan")

    # 冗余数据，便于查询规则的存历史数据, 用于年计划等的排列
    dev = fields.Many2one(string="设备", comodel_name="metro_park_maintenance.train_dev")

    date = fields.Date(string="日期")
    rule_type = fields.Selection(string='类型',
                                 selection=[('normal', '规程'), ('temp', '检技通')],
                                 default="temp",
                                 required=True)

    rule = fields.Many2one(string="修程",
                           comodel_name="metro_park_maintenance.repair_rule",
                           help="只有在类型为规程的时候")

    temp_rule = fields.Many2one(string="检技通",
                                comodel_name="metro_park_maintenance.repair_tmp_rule",
                                help="只有在临时修程的时候有效")

    def _get_default_start_time(self):
        '''
        取得默认时间
        :return:
        '''
        delta = timedelta(hours=8)
        return datetime.now().replace(hour=9, minute=0, second=0) - delta

    def _get_default_end_time(self):
        '''
        :return:
        '''
        delta = timedelta(hours=8)
        return datetime.now().replace(hour=17, minute=0, second=0) - delta

    start_time = fields.Datetime(string='开始时间', required=True, default=_get_default_start_time)
    end_time = fields.Datetime(string='结束时间', required=True, default=_get_default_end_time)

    remark = fields.Text(string='备注')

    @api.onchange('dev')
    def on_change_dev(self):
        '''
        设备更改时，限制特定的检技通, 检技通是针对当前选择的设备，且日期在范围内
        :return:
        '''
        if self.dev and self.rule_type == 'temp':
            dev_id = self.dev.id
            records = self.env["metro_park_maintenance.repair_tmp_rule"] \
                .search([('trains', '=', dev_id),
                         ('start_date', '<=', str(self.date)),
                         ('end_date', '>=', str(self.date))])
            return {
                "domain": {
                    "temp_rule": [('id', 'in', records.ids)]
                }
            }
        else:
            return {
                "domain": {
                    "temp_rule": [('id', 'in', [])]
                }
            }

    @api.multi
    def add_day_plan_data(self):
        '''
        添加日计划数据
        :return:
        '''
        tmp_date = pendulum.parse(str(self.date))
        # 根据日期获取默认的日计划
        day_plan = self.env['metro_park_maintenance.day_plan'].search([('plan_date', '=', self.date)])
        self.day_plan_id = day_plan.id
        self.env["metro_park_maintenance.rule_info"].create({
            "plan_id":
                "metro_park_maintenance.day_plan, {plan_id}".format(plan_id=day_plan.id),
            "rule_type": self.rule_type,
            "dev": self.dev.id,
            "date": str(self["date"]),
            "year": tmp_date.year,
            "month": tmp_date.month,
            "day": tmp_date.day,
            "rule": self.rule.id,
            "tmp_rule": self.temp_rule.id,
            "data_source": 'day',
            "work_start_time": time.mktime(
                time.strptime(str(self["start_time"]), "%Y-%m-%d %H:%M:%S")),
            "work_end_time": time.mktime(
                time.strptime(str(self["end_time"]), "%Y-%m-%d %H:%M:%S")),
            "remark": self.remark,
        })
