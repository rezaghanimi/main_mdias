# -*- coding: utf-8 -*-

from odoo import models, api
import pendulum
import logging
_logger = logging.getLogger(__name__)


class DayPlanWizard(models.TransientModel):
    '''
    重写onok函数，每条线路各自实现各自的
    '''
    _inherit = 'metro_park_maintenance.day_plan_wizard'

    @api.multi
    def on_ok(self):
        '''
        点击确定按扭, 创建的时候就把当日的运行图数据放进去，这样便于修改
        :return:
        '''
        tmp_date = pendulum.parse(self.date.name)
        plan_date = tmp_date.format("YYYY-MM-DD")

        # 创建日计划
        record = self.env["metro_park_maintenance.day_plan"].create([{
            "plan_name": self.name,
            "plan_date": plan_date,
            "state": "draft",
            "week_plan_id": self.week_plan_id.id,
            "pms_work_class_info": self.pms_work_class_info.id,
            "run_trains": [(6, 0, self.run_trains.ids)],
            "time_table_id": self.time_table_id.id
        }])

        main_line_rail_id = self.env.ref('metro_park_base_data_6.main_line_rail').id
        main_line_rule_id = self.env.ref('metro_park_base_data_6.main_line_run_rule').id

        # 日计划需要复制周计划数据
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'
                      .format(plan_id=self.week_plan_id.id))])
        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'day',
                'date': str(info.date),
                'parent_id': info.id,
                'plan_id':
                    'metro_park_maintenance.day_plan, {plan_id}'.format(plan_id=record.id)
            })

        # 根据运行图创建新的运营任务
        time_table_datas = self.time_table_id.time_table_data
        for data in time_table_datas:
            vals.append({
                    "rule_type": 'run',
                    "data_source": "day",
                    "date": plan_date,
                    "year": tmp_date.year,
                    "month": tmp_date.month,
                    "day": tmp_date.day,
                    "work_start_time": data["plan_out_val"] * 60,
                    "work_end_time": data["plan_in_val"] * 60,
                    "rule": main_line_rule_id,
                    "rail": main_line_rail_id,
                    'plan_id': 'metro_park_maintenance.day_plan, {plan_id}'.format(plan_id=record.id),
                    "time_table_data": data.id
                })

        return self.env["metro_park_maintenance.rule_info"] \
            .create(vals)

    @api.model
    def get_day_plan_action(self):
        '''
        取得日计划动作
        :return:
        '''
        records = self.env['metro_park_maintenance.year_plan'] \
            .search([('state', '=', 'published')])
        years = records.mapped('year')
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.day_plan_wizard",
            'view_mode': 'form',
            "target": "new",
            "domain": {
                "year": [("val", "in", years)]
            },
            "views": [[self.env.ref('metro_park_maintenance.day_plan_wizard_form').id, "form"]]
        }

    @api.model
    def get_parent_plan_data(self):
        '''
        获取上一级计划的检修计划数据
        :return:
        '''
        option = []
        datas = self.env['metro_park_maintenance.rule_info']\
            .search_read([('data_source', '=', 'week')],
                         fields=['id', 'date', 'rule_name'])
        for data in datas:
            option.append({
                'value': data.get('id'),
                'label': str(data.get('date')) + '/' + str(data.get('rule_name')),
            })
        return option



