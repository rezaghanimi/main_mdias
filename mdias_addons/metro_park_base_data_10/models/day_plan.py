# -*- coding: utf-8 -*-

from odoo import models, api, exceptions
import pendulum
import logging
import json
import random

TASK_TYPE_RUN = 'run'
TASK_TYPE_PLAN = 'plan'
TASK_TYPE_MILE = 'mile'

_logger = logging.getLogger(__name__)


class DayPlan(models.Model):
    '''
    日计划, 计处日计划
    '''
    _inherit = 'metro_park_maintenance.day_plan'

    @api.multi
    def plan_train(self):
        '''
        安排车辆，目的是为了给运营任务安排车车
        1、车的话得看车前一天在什么地方，得衔接起来。
        2、存在一个车一天跑两个高峰的情况。
        3、同一个车不能跑两个时间有交叉的任务
        车是变量的值，1-运营车数量，变量为运营任务
        正线的车辆先安排
        车的剩余公里数也要考虑
        :return:
        '''
        max_count_info = []

        # 10号线针10号线的正线, 日计划创建的时假就定了运营任务
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id

        # 如果是高峰车则使用登顶车等进行
        run_trains = self.run_trains
        if len(run_trains) == 0:
            raise exceptions.ValidationError("当前没有设置运营车!")

        # 设备信息缓存, 只安排运营车，运营车要考虑车辆检修和扣车, 值是从1开始
        dev_cache = {}
        devs = []
        for index, dev in enumerate(run_trains):
            item = {
                "id": dev.id,
                "index": index,
                "val": index + 1,   # 值从1开始， c++计算使用的值
                "dev_no": dev.dev_no
            }
            dev_cache[dev.id] = item
            devs.append(item)

        plan_date = pendulum.parse(str(self.plan_date))
        plan_date_str = plan_date.format("YYYY-MM-DD")

        next_date = plan_date.add(days=1)
        next_date_str = next_date.format('YYYY-MM-DD')

        # 对所有运营任务行安排车辆, 排除用户指定的车, 用户指定了的设备还要进行排除
        run_task_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('rule.id', '=', main_line_rule_id),
                     ('date', '=', plan_date_str),
                     ('user_define_dev', '=', False)])

        # 收集run task, 日计划就是为了给run task安排车辆
        run_tasks = []
        info_cache = dict()
        for info in run_task_infos:

            data = info.time_table_data
            info_cache[info.id] = info

            run_task = dict()

            # 这个是为了便于计算，将时间转化成为分钟数
            run_task["id"] = info["id"]
            run_task['work_start_val'] = data['plan_out_val']
            run_task['work_end_val'] = data['plan_in_val']
            run_task['work_start_time'] = data['plan_out_time']
            run_task['work_end_time'] = data['plan_in_time']
            run_task['time_table_data_id'] = data.id

            # 这个是以分钟为单位
            run_task['span'] = data['plan_in_val'] - data['plan_out_val']
            run_task['type'] = TASK_TYPE_RUN
            run_task['planed'] = False
            run_task['miles'] = data['miles']
            run_task['train_no'] = data['train_no']

            # 对每个任务进行一个编号
            run_task['index'] = len(run_tasks)
            run_task['back_location'] = data['back_location'].id
            run_task['is_back_main_line'] = \
                True if data['back_location'].id == main_line_rule_id else False
            run_task['out_location'] = data['out_location'].id
            run_task['is_from_main_line'] = \
                True if data['out_location'].id == main_line_rule_id else False

            # 使用正线运营的规程
            run_task['rule_id'] = main_line_rule_id

            # 计算之后的值
            run_task['val'] = 0
            run_tasks.append(run_task)

        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有设置location!")

        conflict_infos = []

        line = location.line
        locations_ids = line.get_locations()
        locations = self.env['metro_park_base.location'].browse(locations_ids)

        # 取得前一日车的位置(也就是当日)
        pre_date = plan_date.subtract(days=1)
        pre_date_str = pre_date.format('YYYY-MM-DD')

        prev_location = {}
        for info in self.train_infos:
            prev_location[info.train.id] = info.location.id

        def get_location_run_tasks(tmp_location_id, go_back=True):
            '''
            取得返回到特定场段的任务, 有些是有特殊要求，
            比如试车线，D2和D4这种, 具体哪个车回哪个场段生产说明上已经说明
            :return:
            '''
            tmp_run_tasks = []
            for tmp_task1 in run_tasks:
                if go_back:
                    if tmp_task1['back_location'] == tmp_location_id:
                        tmp_run_tasks.append(tmp_task1)
                else:
                    if tmp_task1['back_location'] != tmp_location_id:
                        tmp_run_tasks.append(tmp_task1)

            return tmp_run_tasks

        # 处理次日任务, 次日检修任务会要求回库场段, 周计划中会有
        next_date_info = self.env["metro_park_maintenance.rule_info"].search(
            [('date', '=', next_date_str),
             ('rule.target_plan_type', 'in', ['year', 'month', 'week']),
             ('data_source', '=', 'week')])
        for info in next_date_info:
            # 根据工班确定回库位置
            work_class = info['work_class']
            if work_class:
                location = work_class.locations
                if len(location) > 1:
                    raise exceptions.ValidationError('工班属于两个不同的地方!')
                else:
                    location = location[0]
                tmp_tasks = get_location_run_tasks(location.id)
                index_array = [tmp_task['index'] for tmp_task in tmp_tasks]
                for task in run_tasks:
                    if task["index"] not in index_array:
                        # 有可能不在运行车里面, 如果在运营车里则限制
                        if info.dev.id in dev_cache:
                            conflict_infos.append({
                                "task_index": task["index"],
                                "val": dev_cache[info.dev.id]["val"]
                            })

        # 高峰车一个就可以了, 因为多了的话有可能正线出问题回不了车，会把计划弄得很乱
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.rule_info, {plan_id}'.format(plan_id=self.id))])

        # 登顶这些一个地方不能超过多少个, 登顶都扣车了， 但是如果数量超了就要发到另外一个场去
        # 限制必需要有车跑，这几个车中至少有超出的数量要参与运营任务，并且终点只能是另一个场段
        def constrain_max_count_info(max_rule_id):
            '''
            限制洗车、登顶等的数量, 原有的数量减去离开的数量，
            然后加上到达的数量再看是否超过最大值
            :param max_rule_id:
            :return:
            '''
            repair_rule_l = self.env.ref(
                'metro_park_base_data_10.repair_rule_l')
            repair_rule_dd = self.env.ref(
                'metro_park_base_data_10.repair_rule_dd')

            location_ban_qiao = self.env.ref('metro_park_base_data_10.ban_qiao').id
            location_gao_da_lu = self.env.ref('metro_park_base_data_10.gao_da_lu').id

            special_tasks = rule_infos.get_spec_tasks(max_rule_id)
            # 由于线路特殊性，这里先写死，后面再做檲
            total_count = len(special_tasks)
            for tmp_location in locations:
                max_count = None
                # 登顶
                if max_rule_id == repair_rule_dd:
                    if tmp_location.id == location_ban_qiao:
                        if total_count > 8:
                            max_count = 5
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 4
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 3
                        elif total_count <= 4:
                            max_count = 2

                    if tmp_location.id == location_gao_da_lu:
                        if total_count > 8:
                            max_count = 4
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 3
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 2
                        elif total_count <= 4:
                            max_count = 1
                # 里程检
                if max_rule_id == repair_rule_l:
                    if tmp_location.id == location_ban_qiao:
                        if total_count > 8:
                            max_count = 5
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 4
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 3
                        elif total_count <= 4:
                            max_count = 2

                    if tmp_location.id == location_gao_da_lu:
                        if total_count > 8:
                            max_count = 4
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 3
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 2
                        elif total_count <= 4:
                            max_count = 1
                # 登顶
                if max_rule_id == repair_rule_dd:
                    if tmp_location.id == location_ban_qiao:
                        if total_count > 8:
                            max_count = 5
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 4
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 3
                        elif total_count <= 4:
                            max_count = 2

                    if tmp_location.id == location_gao_da_lu:
                        if total_count > 8:
                            max_count = 4
                        elif total_count == 8:
                            max_count = 4
                        elif total_count == 7:
                            max_count = 3
                        elif total_count == 6:
                            max_count = 3
                        elif total_count == 5:
                            max_count = 2
                        elif total_count <= 4:
                            max_count = 1

                if not max_count:
                    continue

                # 取得回特定场地的task
                back_tasks = get_location_run_tasks(tmp_location.id)
                back_vars = [tmp_back_task['index'] for tmp_back_task in back_tasks]

                out_tasks = get_location_run_tasks(tmp_location.id, False)
                out_vars = [tmp_out_task['index'] for tmp_out_task in out_tasks]

                # 取得关联的设备信息
                tmp_vals = [dev_cache[special_task.dev.id]["val"] for special_task in special_tasks]
                tmp_dev_ids = special_tasks.mapped("dev.id")
                old_num = 0
                for dev_id1 in tmp_dev_ids:
                    if dev_id1 in prev_location and prev_location[dev_id1] == tmp_location.id:
                        old_num += 1

                max_count_info.append({
                    "vals": tmp_vals,
                    "back_tasks": back_vars,
                    "out_tasks": out_vars,
                    "max_count": max_count,
                    "old_num": old_num
                })

        # 限制登顶等
        rules = self.env["metro_park_maintenance.repair_rule"].search(
            [('target_plan_type', 'in', ['week', 'day'])])
        for rule in rules:
            constrain_max_count_info(rule.id)

        # 如果车的位置不同，出库场段和前一日回库场段要相同，否则不能安排, 有可能跑两次，所以还不能简单的安排
        # for run_task in run_tasks:
        #     for train in run_trains:
        #         info = info_cache[run_task["id"]]
        #         if train.id in prev_location and prev_location[train.id] \
        #                 != info.time_table_data.out_location.id:
        #             conflict_infos.append({
        #                 "task_index": run_task["index"],
        #                 "val": dev_cache[train.id]["val"]
        #             })

        # 前一日的运营信息
        prev_run_tasks = \
            self.env['metro_park_maintenance.rule_info'].search(
                [('rule.id', '=', main_line_rule_id),
                 ('date', '=', pre_date_str),
                 ('data_source', '=', 'day')])
        pre_mile_cache = {task.dev.id: task.time_table_data.miles for task in prev_run_tasks}

        max_mile_info = []
        # 取前一日的公里数
        mile_rule = \
            self.env.ref('metro_park_base_data_10.repair_rule_l')
        # 取的时当前计划的前一天之前的里程, 然后再加上前一天的运行里程, 这样才能知道当日里程的大概
        train_miles = {record.train.id: record.miles for record in self.train_infos}

        # 有可能是在当日进行里程修
        delta_miles_cache = {
            record.train.id: record.miles_after_last_repair for record in self.train_infos}

        for dev_id in train_miles:
            if dev_id in dev_cache:

                # 当日预估公里数
                delta_mile = delta_miles_cache[dev_id]
                if dev_id in pre_mile_cache:
                    delta_mile = delta_mile + pre_mile_cache[dev_id]

                # 如果超了需要安排里程检
                rule_max_miles = mile_rule.run_miles + mile_rule.positive_offset_miles
                if delta_mile > rule_max_miles:
                    max_mile_info.append({
                        "dev": dev_id,
                        "val": dev_cache[dev_id]['val'],
                        "max_miles": 0
                    })
                else:
                    max_miles = rule_max_miles - delta_mile
                    max_mile_info.append({
                        "dev": dev_id,
                        "val": dev_cache[dev_id]['val'],
                        "max_miles": max_miles
                    })

        # 任务指定了回库的场段, 那么就不能安排这些不到这个地方的车
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('date', 'in', [plan_date_str]),
                     ('data_source', '=', 'day')])
        for info in rule_infos:
            if info.user_define_location and info.dev.id:
                # 取得不到这个地方的task
                tmp_tasks = get_location_run_tasks(info.user_define_location.id, False)
                for tmp_task in tmp_tasks:
                    conflict_infos.append({
                        "task_index": tmp_task["index"],
                        "val": dev_cache[info.dev.id]["val"]
                    })

        # 取得所有日计划检修数量的车, 那么日计划不再强制要求扣车
        # 这样就可以区分出来, 还要扣除掉结合了均衡车的车
        day_repair_devs = []
        # 先查不需要扣车的
        rule_infos = self.env["metro_park_maintenance.rule_info"]\
            .search([('rule.need_retain', '=', False),
                     ('date', '=', str(self.plan_date)),
                     ('data_source', '=', 'day'),
                     ('rule.target_plan_type', 'in', ['day', 'week'])])
        day_repair_dev_ids = rule_infos.mapped('dev.id')

        # 再查需要扣车的
        rule_infos = self.env["metro_park_maintenance.rule_info"]\
            .search([('rule.need_retain', '=', True),
                     ('date', '=', str(self.plan_date)),
                     ('data_source', '=', 'day')])
        detain_ids = rule_infos.mapped('dev.id')
        for tmp_dev_id in day_repair_dev_ids:
            if tmp_dev_id not in detain_ids:
                tmp_info = dev_cache[tmp_dev_id]
                day_repair_devs.append(tmp_info['index'])

        # 高峰车只能安排特定时间之前回来的车，不能安排超过这个时间点的车
        for info in self.limit_infos:
            if info.max_repair_back_time:
                end_time = pendulum.parse('2019-01-01 ' + info.max_repair_back_time)
                for run_task in run_tasks:
                    # 存的时候转换成了UTC,比较的时候转换成本地时间
                    back_time = pendulum.parse(str(run_task['work_end_time'])).add(hours=8)
                    if back_time >= end_time:
                        for dev_id in day_repair_dev_ids:
                            conflict_infos.append({
                                "task_index": run_task["index"],
                                "val": dev_cache[dev_id]["val"]
                            })

        # 每个地方的高峰车信息, 高峰车不能太多
        hight_run_limits = []
        for info in self.limit_infos:
            if info.max_repair_after_high_run:
                tmp = {
                    "location": info.location.id,
                    "tasks": [],
                    "devs": day_repair_devs,
                    "max_count": info.max_repair_after_high_run
                }
                tmp_tasks = get_location_run_tasks(info.location.id)
                for task in tmp_tasks:
                    tmp['tasks'].append(task['index'])
                hight_run_limits.append(tmp)

        # 设备信息
        dev_place_info = []
        ids = []
        for info in self.train_infos:
            if info.train.id in dev_cache:
                # 可能是有多个检修任务
                # if info.train.id in ids:
                #     raise exceptions.ValidationError('发现两条位置信息')
                if info.train.id in ids:
                    continue
                ids.append(info.train.id)
                dev_place_info.append({
                    "dev": dev_cache[info.train.id]["val"],
                    "place": info.location.id
                })

        return {
            "devs": devs,
            "run_tasks": run_tasks,
            "conflict_infos": conflict_infos,
            "max_mile_info": max_mile_info,
            "high_dev_infos": day_repair_devs,
            "day_repair_devs": day_repair_devs,
            "hight_run_limits": hight_run_limits,
            "max_count_info": max_count_info,
            "dev_place_info": dev_place_info
        }

    @api.model
    def plan_week_plans(self, day_plan_id):
        '''
        安排周计划
        :return:
        '''
        pass

    @api.multi
    def simulate_train_info(self):
        '''
        模拟里程数据
        :return:
        '''
        for info in self.train_infos:
            info.last_repair_miles = info.miles - random.randint(1, 1000)

    @api.depends('run_task_count', 'run_trains')
    def _compute_plan_description(self):
        '''
        计算计划信息
        :return:
        '''
        location_cache = {}
        from_location_tasks = {}
        back_location_tasks = {}
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id

        for record in self:

            # 取得运营任务信息
            date = str(record.plan_date)
            infos = self.env['metro_park_maintenance.rule_info'].search(
                [('date', '=', date), ('data_source', '=', 'day'), ('rule_type', '=', 'run')])
            for info in infos:
                location = info.time_table_data.out_location
                from_location_tasks.setdefault(location.name, []).append(info)
                location = info.time_table_data.back_location
                back_location_tasks.setdefault(location.name, []).append(info)

            # 取得车辆信息
            pre_date = pendulum.parse(date).subtract(days=1)
            pre_day_run_tasks = self.env["metro_park_maintenance.rule_info"] \
                .search([('rule.id', '=', main_line_rule_id),
                         ('date', '=', pre_date.format('YYYY-MM-DD')),
                         ('data_source', '=', 'day')], order="work_end_time asc")

            # 前一日计划位置
            black_ids = []
            for tmp_task in pre_day_run_tasks:
                if tmp_task.dev:
                    prev_back_location = tmp_task.time_table_data.back_location
                    location_cache.setdefault(prev_back_location.name, []).append(True)
                    black_ids.append(tmp_task.dev.id)

            # 如果没有前一日的计划信息则取现车位置
            cur_trains = \
                self.env["metro_park_dispatch.cur_train_manage"].search([('train.id', 'not in', black_ids)])
            for cur_train in cur_trains:
                if cur_train.cur_location:
                    location_cache.setdefault(cur_train.cur_location.name, []).append(True)
                else:
                    location_cache.setdefault(cur_train.cur_location.name, []).append(True)

            info = []
            for location in location_cache:
                if not location:
                    continue

                info.append({
                    "name": location + '车辆:',
                    "value": len(location_cache[location])
                })

            for location in from_location_tasks:
                info.append({
                    "name": '从' + location + "出发的车辆:",
                    "value": len(from_location_tasks[location])
                })

            for location in back_location_tasks:
                info.append({
                    "name": '到' + location + "的车辆:",
                    "value": len(from_location_tasks[location])
                })

            record.plan_info_description = json.dumps(info)
