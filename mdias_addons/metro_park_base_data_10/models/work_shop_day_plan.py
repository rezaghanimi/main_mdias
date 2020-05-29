# -*- coding: utf-8 -*-

from odoo import models, api
from odoo import exceptions
import pendulum
import logging

try:
    import websocket
    from websocket import create_connection
except ImportError:
    websocket = None

_logger = logging.getLogger(__name__)

TASK_TYPE_RUN = 'run'
TASK_TYPE_PLAN = 'plan'
TASK_TYPE_MILE = 'mile'


class WorkShopDayPlan(models.Model):
    '''
    车间日生产计划
    '''
    _inherit = 'metro_park_dispatch.work_shop_day_plan'

    @api.multi
    def publish_plan(self):
        '''
        发布计划, 当日的收车和次日的发车, 发布以后再到收发车那边再进行发布，之后发布到信号楼
        :return:
        '''
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id

        cur_trains = self.env["metro_park_dispatch.cur_train_manage"].search([])
        cur_train_cache = {train.train.id: train for train in cur_trains}

        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有设置location")

        line = location.line
        locations_ids = line.get_locations()

        # 当日收车股道
        train_position_cache = {}
        datas = self.plan_datas
        for data in datas:
            if data.rule.id == main_line_rule_id \
                    and data.time_table_data_id.back_location.id in locations_ids:
                self.env["metro_park_dispatch.train_back_plan"].create({
                    'status': 'unpublish',
                    'train_id': cur_train_cache[data.dev.id].id if data.dev else False,
                    'plan_back_location': data.time_table_data_id.back_location.id,
                    'date': data.plan_date,
                    'plan_back_time': data.work_start_tm,
                    'plan_back_rail': data.rail.id,
                    'exchange_rail_time': data.work_start_tm,
                    "plan_train_no": data.time_table_data_id.train_no,
                    "work_shop_data_id": data.id,
                    "work_shop_day_plan_id": self.id
                })
            # 缓存当日所在轨道
            train_position_cache[data.dev.id] = data.rail.id

        # 次日发车股道
        plan_date = pendulum.parse(str(self.plan_date))
        next_date = plan_date.add(days=1).format("YYYY-MM-DD")
        workshop_plan = self.search([("plan_date", "=", next_date)])
        if not workshop_plan:
            raise exceptions.ValidationError("检调还未发布次日计划! 需要检调先发布次日计划!")

        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有配置场段！请在右上角头像处配置!")

        datas = workshop_plan.plan_datas
        for data in datas:
            if data.rule.id == main_line_rule_id \
                    and data.time_table_data_id.out_location.id in locations_ids:

                out_train_pre_min = data.time_table_data_id.out_location.send_train_pre_min
                if data.dev.id in train_position_cache:
                    plan_out_rail = train_position_cache[data.dev.id]
                else:
                    plan_out_rail = cur_trains[data.dev.id].cur_rail.id

                self.env["metro_park_dispatch.train_out_plan"].create({
                    'status': 'unpublish',
                    'train_id': cur_train_cache[data.dev.id].id if data.dev else False,
                    'plan_out_location': data.time_table_data_id.back_location.id,
                    'date': data.plan_date,
                    'plan_out_time': data.work_start_tm,
                    'plan_out_rail': plan_out_rail,
                    'exchange_rail_time': data.work_start_tm + out_train_pre_min * 60,
                    "plan_train_no": data.time_table_data_id.train_no,
                    "work_shop_data_id": data.id,
                    "work_shop_day_plan_id": self.id
                })

        self.state = 'published'

    @api.multi
    def reback_plan(self):
        '''
        撤回计划
        :return:
        '''
        self.state = 'un_publish'

    @api.multi
    def get_rail_plan_info(self, location_id):
        '''
        计算具体的轨道，计算当日的收车轨道，当日发布第二日的收发车计划, 这里获取数据去重前端计算，
        由于两边都有场调，所以各自管各自的
        高峰车单独处理
        :return:
        '''
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id

        date_str = str(self.plan_date)

        # 取得所有的可停轨道, 通过can_stop进行标识，通过stop_order安排优先级
        rails = self.env["metro_park_base.rails_sec"] \
            .search([('can_stop', '=', True),
                     ('location', '=', location_id)],
                    order="stop_order asc")

        port_count = 0
        for rail in rails:
            if rail.port:
                port_count += 1

        # 给rail设置值，必需按顺序，和c++对应起来
        rail_info = {}
        val = 1
        for rail in rails:
            rail_info[rail.id] = val
            val += 1

        # 检修计划是第二天的, 所以计划日期的前一天才是当天
        # 当天的收车信息, 确定每个车收到哪个轨道, 已经完成收车的不在计划之内
        # 如果一个车跑了两个任务，那么回的场地和另外一个出的场地必需要相同
        info_cache = {}
        tasks = []
        plan_datas = self.plan_datas
        for data in plan_datas:
            if not data.rule \
                    or data.rule.id != main_line_rule_id \
                    or not data.dev:
                continue

            # 位置不相同跳过, 各个场段分别安排
            if data.time_table_data_id.back_location.id != location_id:
                continue

            dev_id = data["dev"]["id"]

            # 跑两次, 前一次不在计算中作安排
            next_task = data.get_next_run_task()
            if next_task:
                continue

            # 如果有前次任务, 那么当天需要发车, 那么不能被挡
            prev_task = data.get_prev_run_task()
            if prev_task:
                tasks.append({
                    "dev_id": dev_id,
                    "data_id": data["id"],
                    "index": len(tasks),
                    "val": 0,  # 这个值是轨道的数值
                    "back_time": data["work_end_tm"],
                    "back_location": data.time_table_data_id.back_location.id,  # 回库的位置发车需要
                    "have_prev_task": True,
                    "have_run_task_next_day": False    # 默认是第二天没有跑车任务
                })
            else:
                tasks.append({
                    "dev_id": dev_id,
                    "data_id": data["id"],
                    "index": len(tasks),
                    "val": 0,  # 这个值是轨道的数值
                    "back_time": data["work_end_tm"],
                    "back_location": data.time_table_data_id.back_location.id,  # 回库的位置发车需要
                    "have_prev_task": False,
                    "have_run_task_next_day": False    # 默认是第二天没有跑车任务
                })
            info_cache[data["id"]] = data

        next_date_str = pendulum.parse(date_str).add(days=1).format('YYYY-MM-DD')

        # 根据第二天的发车和检修来决定当日的收车位置信息,
        # 还有当天本来计划的检修
        # 发车轨道决定了停靠的先后顺序
        next_date_work_shop_plan = \
            self.search([("plan_date", "=", next_date_str)])
        if not next_date_work_shop_plan:
            raise exceptions.ValidationError("检调还没有发布次日计划, 请先发布次日检修计划!")
        next_day_datas = next_date_work_shop_plan.plan_datas

        # 关联每个车第二天的发车时间, 要发车的不能在不发车的B股,
        # 也就是不发的不能档着要发的
        for task in tasks:
            dev_id = task["dev_id"]

            # 如果是高峰车则不作考虑
            for data in next_day_datas:
                if dev_id == data.dev.id:
                    task["have_run_task_next_day"] = True

            # 检修任务的车必需要在特定的股道,
            # 当天有检修计划, 当天的检修计划只能是登顶, 里程修等
            plan_data = self.env["metro_park_dispatch.work_shop_day_plan_data"]\
                .browse(task['data_id'])
            tmp_tasks = plan_data.get_tasks_after_run() or []

            work_requirement_ids = []
            for tmp_task in tmp_tasks:
                if tmp_task.work_requirement:
                    work_requirement_ids += tmp_task.work_requirement.ids

            # 第二天的检修任务需求
            # next_date_rule_ids = plan_data.next_day_works
            # work_requirement_ids += next_date_rule_ids.mapped("work_requirement.id")

            # 如果有特殊要求，则只能安排到特殊的轨道上面
            # if work_requirement_ids:
            #     rails = self.env["metro_park_base.rails_sec"] \
            #         .search([('can_stop', '=', True),
            #                  ('location', '=', location_id),
            #                  ('rail_property', 'in', work_requirement_ids)],
            #                 order="stop_order asc")
            #     if not rails:
            #         raise exceptions.ValidationError('没有找到特定属性的轨道!')
            #     else:
            #         # 限制只能安排在这些股道上面
            #         task['white_list'] = rails.mapped("stop_order")

        rail_info = []
        rail_info_cache = {}
        for index, rail in enumerate(rails):
            data = {
                "id": rail.id,
                "index": index
            }
            rail_info.append(data)
            rail_info_cache[rail.id] = index

        # 调车计划
        # train_dispatches = \
        #     self.env["metro_park_dispatch.train_dispatch"].search(
        #         [('dispatch_date', '=', date_str),
        #          ('source_rail.id', 'in', rails.ids)], order='start_time')
        # train_dispatch_cache = {dispatch.source_rail.id: dispatch for dispatch in train_dispatches}

        # 轨道当前被占用，如果是a羰的话那么需要放到b端去, 那么b端就不能安排。 并且需要自动安排调车计划
        # new_dispatch_info = []
        # black_list = []
        # cur_trains = self.env["metro_park_dispatch.cur_train_manage"]\
        #     .search([('cur_rail.can_stop', '=', 1)])
        # for cur_train in cur_trains:
        #     if cur_train.cur_rail.port == 'A':
        #         reverse_port = cur_train.cur_rail.reverse_port
        #         # 查看是否会被调走, 那么就可以排，如果不被调走，那么就只能调到B端去
        #         dispatch = train_dispatch_cache.get(cur_train.cur_rail.id, [])
        #         if dispatch:
        #             dispatch = train_dispatch_cache.get(cur_train.cur_rail.id, [])
        #             for task in tasks:
        #                 tmp_back_time = pendulum.parse(task["back_time"])
        #                 dispatch_time = pendulum.parse(dispatch["start_time"])
        #                 if tmp_back_time < dispatch_time:
        #                     black_list.append({
        #                         "val": rail_info[cur_train.cur_rail.id],
        #                         "index": task["index"]
        #                     })
        #         else:
        #             # 具体什么时候调车要根据安排的车来决定, 必需要在车回来之前给调车
        #             new_dispatch_info.append({
        #                 "cur_train_id": cur_train.id,
        #                 "source_rail": cur_train.cur_rail.id,
        #                 "target_rail": reverse_port.id
        #             })
        #             for task in tasks:
        #                 # 这个时假b端不能安排车
        #                 black_list.append({
        #                     "index": task["index"],
        #                     "val": rail_info[reverse_port.id]
        #                 })

        # 有调车要调特定股的时候,
        # 如果是A端，那么调来之前还可以放到B端去,
        # 如果是B端，那么调来之前不能回车，回车了就调不进去了
        # train_dispatches = \
        #     self.env["metro_park_dispatch.train_dispatch"].search(
        #         [('dispatch_date', '=', date_str),
        #          ('target_rail.id', 'in', rails.ids)], order='start_time')
        # for dispatch in train_dispatches:
        #     if dispatch.target_rail and dispatch.target_rail.port == 'A':
        #         reverse_port = dispatch.target_rail.reverse_port.id
        #         dispatch_time = pendulum.parse(str(dispatch.start_time))
        #         for task in tasks:
        #             arrive_time = pendulum.parse(task["back_time"])
        #             if arrive_time > dispatch_time:
        #                 black_list.append({
        #                     "index": task["id"],
        #                     "val": rail_info[reverse_port.id]
        #                 })
        #     elif dispatch.target_rail and dispatch.target_rail.port == 'B':
        #         reverse_port = dispatch.target_rail.reverse_port.id
        #         dispatch_time = pendulum.parse(str(dispatch.start_time))
        #         for task in tasks:
        #             arrive_time = pendulum.parse(task["back_time"])
        #             if arrive_time < dispatch_time:
        #                 black_list.append({
        #                     "index": task["id"],
        #                     "val": rail_info[reverse_port.id]
        #                 })

        return {
            "rails": rails.ids,
            "tasks": tasks,
            "black_list": [],
            "port_count": port_count
        }

    @api.multi
    def get_after_run_task(self):
        '''
        当前是一个收车任务，但后面还有运行， 高峰车的情况, 这个也是判断高峰车的标准 train_no
        :return:
        '''
        date_str = str(self.plan_date)
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id
        # 同一车跑了两个任务, 那么第一个不用考虑
        # 第二天的检修任务，但轨道要对应上
        records = self.search([('rule', '=', main_line_rule_id),
                               ('dev', '=', self.dev.id),
                               ('plan_date', '=', date_str),
                               ('work_start_tm', '>', self.work_end_tm)],
                              order="work_start_tm asc")
        return records[0] if records else None
