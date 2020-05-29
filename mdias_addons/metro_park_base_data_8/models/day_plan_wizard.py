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

        tmp_date = pendulum.parse(self.day.name)
        plan_date = tmp_date.format("YYYY-MM-DD")

        infos = []
        for info in self.limit_infos:
            infos.append((0, 0, {
                "location": info.location.id,
                "max_repair_after_high_run": info.max_repair_after_high_run,
                "max_repair_back_time": info.max_repair_back_time
            }))

        pre_date_train_infos = []
        for tmp in self.train_infos:
            pre_date_train_infos.append((0, 0, {
                "train": tmp.train.id,
                "location": tmp.location.id,
                "rail": tmp.rail.id,
                "miles": tmp.miles,
                "last_mile_repair_date": tmp.last_mile_repair_date,
                "last_repair_miles": tmp.last_repair_miles,
                "miles_after_last_repair": tmp.miles_after_last_repair
            }))

        # 创建日计划
        record = self.env["metro_park_maintenance.day_plan"].create([{
            "plan_name": self.name,
            "plan_date": plan_date,
            "state": "draft",
            "week_plan_id": self.week_plan_id.id,
            "pms_work_class_info": self.pms_work_class_info.id,
            "run_trains": [(6, 0, self.run_trains.ids)],
            "train_infos": pre_date_train_infos,
            "limit_infos": infos,
            "time_table_id": self.time_table_id.id
        }])

        main_line_rail_id = self.env.ref(
            'metro_park_base_data_10.main_line_rail').id
        main_line_rule_id = self.env.ref(
            'metro_park_base_data_10.main_line_run_rule').id

        # 日计划需要复制周计划数据
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'
                      .format(plan_id=self.week_plan_id.id)), ('date', '=', plan_date)])
        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'day',
                'date': str(info.date),
                'parent_id': info.id,
                'repair_num': info.repair_num,
                'work_class': [(6, 0, info.work_class.ids)],
                'plan_id': 'metro_park_maintenance.day_plan, {plan_id}'.format(
                    plan_id=record.id)
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
                    'plan_id': 'metro_park_maintenance.day_plan, {plan_id}'.format(
                        plan_id=record.id),
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
            "views": [[self.env.ref(
                'metro_park_maintenance.day_plan_wizard_form').id, "form"]]
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

    @api.onchange('day')
    def on_change_day(self):
        '''
        更改日期的时候计算现车及上日车的最终位置
        :return:
        '''
        if self.year_plan_id \
                and self.month_plan_id \
                and self.week_plan_id \
                and self.day:

            plan_date = self.day.name
            self.name = plan_date

            # 所有的车辆
            dev_type_electric_train_id = self.env.ref(
                'metro_park_base.dev_type_electric_train').id

            # 所有在检修计划中的车
            rule_infos = self.env["metro_park_maintenance.rule_info"] \
                .search([('rule.need_retain', '!=', False),
                         ('date', '=', str(self.day.name)),
                         ('data_source', '=', 'week'),
                         ('rule.target_plan_type', 'in', ['year', 'month'])])
            dev_ids = rule_infos.mapped('dev.id')

            # 所有被扣了的车
            detain_trains = self.env["metro_park_dispatch.cur_train_manage"] \
                .search([('train_status', '!=', 'wait')])
            dev_ids += detain_trains.ids

            free_devs = self.env["metro_park_maintenance.train_dev"].search(
                [("dev_type", "=", dev_type_electric_train_id), ("id", "not in", dev_ids)])

            self.run_trains = [(6, 0, free_devs.ids)]

            # 取得上一日的车辆位置
            pre_date_train_info = {}
            pre_date_info_cache = {}
            pre_day_str = pendulum.parse(
                str(self.day.name)).subtract(days=1).format('YYYY-MM-DD')
            main_line_rule_id = self.env.ref(
                'metro_park_base_data_10.main_line_run_rule').id
            rule_infos = self.env["metro_park_maintenance.rule_info"].search(
                [("date", "=", pre_day_str), ('rule', '=', main_line_rule_id), ('data_source', '=', 'day')])
            for info in rule_infos:
                pre_date_info_cache[info.dev.id] = info

            dev_type_electric_train_id = self.env.ref(
                "metro_park_base.dev_type_electric_train").id
            all_devs = self.env["metro_park_maintenance.train_dev"].search(
                [('dev_type', '=', dev_type_electric_train_id)])
            all_dev_cache = {dev.id: dev for dev in all_devs}
            for dev in all_devs:
                if dev.id in pre_date_info_cache:
                    info = pre_date_info_cache[dev.id]
                    pre_date_train_info[dev.id] = {
                        "train": info.dev.id,
                        'location': info.back_location.id,
                        'rail': info.rail.id
                    }

            cur_trains = self.env["metro_park_dispatch.cur_train_manage"].search([])
            cur_train_cache = {cur_train.train.id: cur_train for cur_train in cur_trains}
            for dev in all_devs:
                if dev.id not in pre_date_train_info and dev.id in cur_train_cache:
                    pre_date_train_info[dev.id] = {
                        "train": dev.id,
                        "location": cur_train_cache[dev.id].cur_location.id,
                        "rail": cur_train_cache[dev.id].cur_rail.id
                    }

            main_line_location = self.env.ref('metro_park_base_data_10.main_line_location')
            main_line_rail = self.env.ref('metro_park_base_data_10.main_line_sec')
            for dev in all_devs:
                if dev.id not in cur_train_cache:
                    pre_date_train_info[dev.id] = {
                        "train": dev.id,
                        "location": main_line_location.id,
                        "rail": main_line_rail.id
                    }

            # 取得设备的里程修信息
            info = all_devs.inner_compute_last_repair_info(pre_day_str)
            last_repair_info = info["last_repair_info"]
            info_cache = info["info_cache"]

            for dev_id in pre_date_train_info:
                item = pre_date_train_info[dev_id]
                if dev_id in last_repair_info:
                    item["last_mile_repair_date"] = str(last_repair_info[dev_id])
                    key = '{dev_no}_{date}'.format(
                        dev_no=all_dev_cache[dev_id]['dev_no'], date=last_repair_info[dev_id])
                    if key in info_cache:
                        item["last_repair_miles"] = info_cache[key].total_mileage

            # 取得上一日的里程数
            mile_infos = self.env['funenc.tcms.vehicle.data'].get_miles_by_date(pre_day_str)
            for dev_id in pre_date_train_info:
                item = pre_date_train_info[dev_id]
                dev_no = all_dev_cache[dev_id]["dev_no"]
                if dev_no in mile_infos:
                    item["miles"] = mile_infos[dev_no]

            vals = []
            for dev_id in pre_date_train_info:
                vals.append((0, 0, pre_date_train_info[dev_id]))

            self.train_infos = vals

