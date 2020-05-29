# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging
import datetime
import threading
from queue import Queue
from . import utility
from odoo.addons.odoo_operation_log.model_extend import LogManage

LogManage.register_type('train_plan_log', '计划日志')

_logger = logging.getLogger(__name__)

TRAIN_BACK_STATES = [("unpublish", "未发布"),
                     ('preparing', '待接车'),
                     ('executing', '执行中'),
                     ('finished', '已完成'),
                     ('canceled', '已取消')]


class TrainBackPlan(models.Model):
    '''
    收车计划, 收车是从转换轨2收车
    '''
    _name = 'metro_park_dispatch.train_back_plan'
    _description = '收车计划'
    _rec_name = 'plan_train_no'
    _track_log = True

    day_plan_id = fields.Many2one(string='日计划',
                                  comodel_name='metro_park_dispatch.day_run_plan')

    # work_shop_day_plan_id = fields.Many2one(comodel_name="metro_park_dispatch.work_shop_day_plan",
    #                                         string='车间日生产计划')
    # work_shop_data_id = fields.Many2one(comodel_name="metro_park_dispatch.work_shop_day_plan_data",
    #                                     string="车间日生产计划数据")

    # 不要用today, today是算的当日开始的时僮，加上8小时仍然不正确
    date = fields.Date(string="日期", help="冗余字段，便于计算",
                       default=lambda self: pendulum.now('UTC').add(hours=8).format('YYYY-MM-DD'))

    plan_train_no = fields.Char(string='计划车次', help="车次号是运行时决定的")
    real_train_no = fields.Char(string='实际车次', help="车次号是运行时决定的")

    # 这个是给排列进路使用
    route_infos = fields.Many2many(string="联锁路由",
                                   comodel_name="metro_park_dispatch.route_info",
                                   relation="train_back_plan_route_infos_rel",
                                   column1="back_plan_id",
                                   column2="route_info_id")

    train_id = fields.Many2one(string='车辆',
                               comodel_name='metro_park_dispatch.cur_train_manage')

    # 由于存在次日的话说, 所以时间都改成int类型
    exchange_rail_time = fields.Integer(string='到达转换轨时间')
    plan_back_time = fields.Integer(
        string='回库时间',
        compute="_compute_plan_back_time")
    real_back_tm = fields.Integer(string='实际时间')

    plan_back_location = fields.Many2one(
        comodel_name="metro_park_base.location",
        string="计划位置")
    real_start_rail = fields.Many2one(string="实际进入场段位置",
                                      comodel_name='metro_park_base.rails_sec')
    plan_back_rail = fields.Many2one(string='到库位置',
                                     comodel_name='metro_park_base.rails_sec',
                                     domain="[('location.id', '=', plan_back_location)]")

    real_back_rail = fields.Many2one(string='实际回库位置',
                                     comodel_name='metro_park_base.rails_sec')

    # 这里是要关联检修计划, 检调将检修任务放到窗口期的时候就存在这种情况
    repair_plan = fields.Many2one(string="检修计划",
                                  comodel_name="metro_park_maintenance.rule_info")

    wash = fields.Boolean(string='洗车',
                          default=False,
                          help="是否洗车，这个没有放到检修计划里面")

    # 作业要求
    work_requirement = fields.Many2many(string='作业要求',
                                        related="repair_plan.rule.work_requirement")
    # 作业要求文字
    work_requirement_txt = fields.Text(
        string="作业要求", compute="_compute_work_requirement")

    dispatch = fields.Boolean(string='是否调车')

    plan_details = fields.One2many(string="勾计划详情",
                                   comodel_name="metro_park_dispatch.train_back_out_detail",
                                   inverse_name="back_plan_id")

    plan_info_id = fields.Many2one(string="metro_park_maintenance.rule_info",
                                   help="计划id")

    # 状态
    state = fields.Selection(string='状态',
                             selection=TRAIN_BACK_STATES,
                             default="unpublish")

    button = fields.Char(string="操作")

    @api.model
    def get_all_back_plan_action(self):
        '''
        back plan action
        '''

        if not self.env.user.cur_location:
            raise exceptions.Warning("当前用户没有配置位置")

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "metro_park_dispatch.train_back_plan",
            "name": "收车计划",
            "views": [[self.env.ref('metro_park_dispatch.train_back_plan_list').id, "tree"]],
            "domain": [("plan_back_location.alias", "=", self.env.user.cur_location.alias)]
        }

    @api.multi
    def get_location_spell(self):
        '''
        取得位置
        :return:
        '''
        self.ensure_one()

        location = None
        try:
            if self.plan_back_rail and self.plan_back_rail.location:
                location = self.plan_back_rail.location.alias
            else:
                location = self.env.user.cur_location.alias
        except Exception as e:
            _logger.info(e)

        return location

    @api.model
    def _send_add_plan_success_callback(self, msg_data, map_name):
        '''
        添加计划成功
        :return:
        '''
        for data in msg_data:
            if "log_id" in data:
                log_id = data["log_id"]
                log = self.env["metro_park_dispatch.train_in_out_log"].browse(
                    log_id)
                log.result = '成功'

    @api.model
    def _send_execute_plan_success_callback(self, msg_data, map_name):
        '''
        添加执行计划成功
        :return:
        '''
        log_id = msg_data["log_id"]
        if log_id:
            log = self.env["metro_park_dispatch.train_in_out_log"].browse(
                log_id)
            log.result = '成功'

    @api.multi
    def receive_train(self):
        '''
        接车, 开始排列进路, 进路开始排了才是
        :return:
        '''
        location = self.get_location_spell()

        data = self.get_plan_data()
        if data:
            if data["instructs"] == []:
                try:
                    # 添加日志
                    log_record = self.env["metro_park_dispatch.train_in_out_log"].create([{
                        "type": "out_plan",
                        "train_dev": self.train_id.train.id,
                        "operation": "收车计划勾计划为空:{out_instructs}".format(
                            out_instructs=str(data["instructs"]))
                    }])
                    data["log_id"] = log_record.id
                except Exception as error:
                    _logger.info("log error {error}".format(error=error))
            else:
                try:
                    # 添加日志
                    log_record = self.env["metro_park_dispatch.train_in_out_log"].create([{
                        "type": "out_plan",
                        "train_dev": self.train_id.train.id,
                        "operation": "收车计划勾计划:{out_instructs}".format(
                            out_instructs=str(data["instructs"]))
                    }])
                    data["log_id"] = log_record.id
                except Exception as error:
                    _logger.info("log error {error}".format(error=error))
            self.state = 'preparing'
            try:
                # 添加日志
                log_record = self.env["metro_park_dispatch.train_in_out_log"].create([{
                    "type": "out_plan",
                    "train_dev": self.train_id.train.id,
                    "operation": "推送收车计划:{start_rail}-{end_rail}到信号楼".format(
                        start_rail=self.real_start_rail.no,
                        end_rail=self.plan_back_rail.no)
                }])
                data["log_id"] = log_record.id
            except Exception as error:
                _logger.info("log error {error}".format(error=error))

            # 之前出现指令重复的情况，防止重复
            cache = dict()
            instructs = data["instructs"]
            new_instructs = []
            for instruct in instructs:
                if instruct["start_rail"] not in cache:
                    new_instructs.append(instruct)
                    cache[instruct["start_rail"]] = True
            data["instructs"] = new_instructs

            # 添加计划, 信号楼如果已经有了则只是更新信息
            try:
                self._cr.commit()
                self.trigger_up_event("funenc_socketio_server_msg", data={
                    "msg_type": "add_plan",
                    "msg_data": [data],
                    "location": location
                }, room="xing_hao_lou", callback_name="_send_add_plan_success_callback")
            except Exception as error:
                LogManage.put_log(
                    content='推送添加收车计划失败{error}'.format(error=error), mode='train_plan_log')

            # 添加日志
            excute_record = None
            try:
                # 这个必需要加，不然回调处理record回出错，
                # 回调应当是一直在等侍，但回调函数在另一线程
                excute_record = self.env["metro_park_dispatch.train_in_out_log"].create([{
                    "type": "out_plan",
                    "train_dev": self.train_id.train.id,
                    "operation": "推送执行收车计划:{start_rail}-{end_rail}到信号楼".format(
                        start_rail=self.real_start_rail.no,
                        end_rail=self.plan_back_rail.no)
                }])
            except Exception as error:
                _logger.info("log error {error}".format(error=error))

            # 执行计划,发送给信号楼
            try:
                # 这个必需要加，不然回调处理record回出错，
                # 回调应当是一直在等侍，但回调函数在另一线程
                self._cr.commit()
                self.trigger_up_event("funenc_socketio_server_msg", data={
                    "msg_type": "excute_plan",
                    "location": location,
                    "msg_data": {
                        "id": self.id,
                        "type": 'train_back',
                        "location": location,
                        "log_id": excute_record.id if excute_record else None
                    }
                }, room="xing_hao_lou", callback_name="_send_execute_plan_success_callback")
            except Exception as error:
                _logger.info("log error {error}".format(error=error))
                LogManage.put_log(
                    content='推送执行收车计划失败{error}'.format(error=error), mode='train_plan_log')

    @api.depends("work_requirement")
    def _compute_work_requirement(self):
        '''
        计算所有的需求
        :return:
        '''
        for record in self:
            if record.work_requirement:
                text = ""
                for tmp in record.work_requirement:
                    text = text + tmp.name
                record.work_requirement_txt = text

    @api.multi
    def dispatch_now(self):
        '''
        立即发车, 信号楼弹出对话框
        :return:
        '''
        self.state = 'preparing'
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "excute_plan",
            "location": self.get_location_spell(),
            "msg_data": {
                "id": self.id,
                "type": 'train_back'
            }
        }, room="xing_hao_lou")

    @api.multi
    def arrive_request_point(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.train_track",
            "view_mode": 'tree',
            "target": "new",
            'domain': [('back_id', '=', self.id)],
            "views": [[self.env.ref(
                'metro_park_dispatch.tree_track_view').id, "list"]]
        }

    @api.model
    def update_state(self, plan_state):
        '''
        发车用的id和计划id是同一个id
        :param plan_state:
        :return:
        '''

        if plan_state['state'] not in [item[0] for item in TRAIN_BACK_STATES]:
            _logger.error("状态不正确")

        record = self.browse(plan_state['id'])
        if not record:
            _logger.error("计划不存在")
            raise exceptions.ValidationError("计划不存在")

        # 不相同的时候才存在更新
        if record.state != plan_state['state']:
            if plan_state['state'] == 'executing':
                record.exchange_rail_time = utility.get_now_time_int_repr()
                today = pendulum.today('UTC')
                # 可能在前一天也可能在后一天
                plan_date = pendulum.parse(str(record.date))
                if today > plan_date:
                    record.exchange_rail_time += 24 * 60 * 60
                elif today < plan_date:
                    record.exchange_rail_time -= 24 * 60 * 60
            elif plan_state['state'] == 'finished':
                record.real_back_tm = utility.get_now_time_int_repr()
                today = pendulum.today('UTC')
                # 可能在前一天也可能在后一天
                plan_date = pendulum.parse(str(record.date))
                if today > plan_date:
                    record.real_back_tm += 24 * 60 * 60
                elif today < plan_date:
                    record.real_back_tm -= 24 * 60 * 60

            # 通知前端刷新界面
            self.trigger_up_event("funenc_socketio_server_msg", data={
                "msg_type": "update_train_back_plan_state",
                "plan_id": self.id,
                "location_alias": record.plan_back_rail.location.alias
            })

        record.state = plan_state['state']
        if 'detail_state' in plan_state:
            self.env['metro_park_dispatch.train_back_out_detail'] \
                .sudo() \
                .update_state(plan_state['detail_state'])

    @api.multi
    def cancel_plan(self):
        '''
        取消计划, 这个函数是市场这边调用的函数，后信号楼调用的不是同一个函数
        :return:
        '''
        self.state = 'canceled'
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "reback_plan",
            "location": self.get_location_spell(),
            "msg_data": [{
                'type': 'train_back',
                "id": self.id
            }]
        }, room="xing_hao_lou")

    @api.multi
    def reback_train_plan(self):
        '''
        撤回计划, 场/检调主动撤销
        :return:
        '''
        self.state = 'canceled'
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "reback_plan",
            "location": self.get_location_spell(),
            "msg_data": [{
                'type': 'train_back',
                "id": self.id
            }]
        }, room="xing_hao_lou")

    @api.model
    def reback_plan(self, id):
        '''
        撤回计划, 信号楼发起撤销, 这里同样要通知场调客户端更新界面
        :return:
        '''
        plan = self.browse(id)
        plan.state = 'canceled'

        # 通知前端刷新界面
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "update_train_back_plan_state",
            "plan_id": id,
            "location_alias": plan.plan_back_rail.location.alias
        })

        return True

    @api.multi
    def _ensure_route(self):
        '''
        搜索进路, 收发车可以直接到到进路
        :return:
        '''
        self.ensure_one()
        details = []
        if self.real_start_rail and self.plan_back_rail:
            all_routes = self.env["metro_park.interlock.route"] \
                .search_train_plan_route(self.real_start_rail.location.id,
                                         self.real_start_rail,
                                         self.plan_back_rail, 'back_plan')
            for index, routes in enumerate(all_routes):
                details.append((0, 0, {
                    'sequence': index + 1,
                    "source_rail": routes[0].start_rail.id,
                    "rail": routes[-1].end_rail.id,
                    "interlock_routes": [
                        (0, 0, {
                            "index": i,
                            "route_id": route.id
                        }) for i, route in enumerate(routes)]
                }))
            self.plan_details.unlink()
            if details:
                self.plan_details = details
            else:
                raise exceptions.ValidationError("没有找到进路，请确定联锁表已经导入!")

    @api.model
    def create_tmp_plan(self, location_id, start_rail, train_id, train_no):
        '''
        创建临时性的计划
        :return:
        '''
        data = dict()
        data['real_train_no'] = train_no
        data['train_id'] = train_id
        data['state'] = 'unpublish'
        config = self.env["metro_park_base.system_config"].get_configs()
        back_train_need_min = config['back_train_need_min'] or 10
        data['plan_back_time'] = utility.get_now_time_int_repr() + \
                                 back_train_need_min * 60
        data['exchange_rail_time'] = utility.get_now_time_int_repr()

        data['date'] = pendulum.now('UTC').add(hours=8).format('YYYY-MM-DD')

        rail = self.env["metro_park_base.rails_sec"] \
            .search(['|', ('no', '=', start_rail),
                     ('alias', '=', start_rail),
                     ('location', '=', location_id)])
        data['real_start_rail'] = rail.id

        domain = [
            ('lock', '=', 0),
            ('block', '=', 0),
            ('hold', '=', 0),
            ('location', '=', location_id)
        ]

        # rail_type_stop_and_check 停车/列检线 (分AB股)
        records = self.env['metro_park_base.rails_sec'].search(domain + [
            ('port', '=', 'A'),
            ('rail_type', '=', self.env.ref(
                'metro_park_base.rail_type_stop_and_check').id)
        ])

        # rail_type_two_week_or_three_month_repair 双周三月检线
        if not records:
            records = self.env['metro_park_base.rails_sec'].search(domain + [
                ('rail_type', '=', self.env.ref(
                    'metro_park_base.rail_type_two_week_or_three_month_repair').id)
            ])

        # rail_type_construction_vehicle 调机工程车库线
        if not records:
            records = self.env['metro_park_base.rails_sec'].search(domain + [
                ('rail_type', '=', self.env.ref(
                    'metro_park_base.rail_type_construction_vehicle').id)
            ])

        # rail_type_download_train 卸车线
        if not records:
            records = self.env['metro_park_base.rails_sec'].search(domain + [
                ('rail_type', '=', self.env.ref(
                    'metro_park_base.rail_type_download_train').id)
            ])

        if records:
            data['plan_back_rail'] = records[0].id
            return self.create(data)
        else:
            # todo 通知没有空闲股道可建立接车
            pass

    @api.model
    def check_train_back(self, cur_park, rail_no, train_id, train_no):
        '''
        # 依据ats车辆信息
        # 检查车辆所处位置是否是出入段线，然后再检查照查状态，然后再检查计划信息
        # 然后再进行冲突检测
        # 如果有多条计划的时候需要匹配时间最适合的计划
        :return:
        '''
        try:
            location = self.env['metro_park_base.location'].browse(
                cur_park['model']['id'])
            for key, value in cur_park['rules'].items():
                _logger.info("check train back %s" % rail_no)
                if rail_no == value['hold_sec']:  # 存在出入段线
                    cur_train = \
                        self.env["metro_park_dispatch.cur_train_manage"] \
                            .browse(train_id)
                    # 检查照查是否亮
                    record = self.env['metro_park_base.indicator_light'].search(
                        [('name', '=', key),
                         ('location', '=', location.id)]
                    )
                    if record and record.light:  # 对应的照查亮了
                        _logger.info("begin find plan!")
                        # 添加日志
                        self.env["metro_park_dispatch.train_back_plan_log"].create([{
                            "location": location.name,
                            "train_no": cur_train.train_no,
                            "remark": '车辆回段',
                            "rail": rail_no
                        }])
                        plan = self.search(
                            [("train_id", '=', train_id),
                             ('state', 'in', ['preparing'])],
                            order="write_date desc", limit=1)
                        if not plan:
                            plan = self.search(
                                [("train_id", '=', train_id),
                                 ('state', '=', 'executing')])
                            if not plan:
                                _logger.info("notice to create plan!")

                                # 通知信号楼没有创建计划
                                self.env["metro_park_dispatch.train_back_plan_log"].create([{
                                    "location": location.name,
                                    "train_no": cur_train.train_no,
                                    "rail": rail_no,
                                    "remark": '车辆回段没有找到相应的计划!'
                                }])

                                # 通知场调重新安排计划
                                self.trigger_up_event("funenc_socketio_server_msg", data={
                                    "msg_type": "notice_no_plan",
                                    "location": location.alias,
                                    "msg_data": {
                                        'train_id': train_id,
                                        'rail_no': value['start_rail']
                                    }
                                })
                            else:
                                _logger.info("plan is executing!")
                                self.env["metro_park_dispatch.train_back_plan_log"].create([{
                                    "location": location.name,
                                    "train_no": cur_train.train_no,
                                    "rail": rail_no,
                                    "remark": '计划正在执行中, 不在推送计划!'
                                }])
                        else:
                            # 如果出现多条计划的时候
                            if plan.real_start_rail:
                                self.env["metro_park_dispatch.train_back_plan_log"].create([{
                                    "location": location.name,
                                    "train_no": cur_train.train_no,
                                    "rail": rail_no,
                                    "remark": '车辆已经触发，不再推送计划!'
                                }])
                            else:
                                _logger.info("write real rail!")

                                rail = self.env['metro_park_base.rails_sec'].search([
                                    ('no', '=', value['start_rail']),
                                    ('location', '=', location.id)
                                ])

                                plan.write({
                                    'real_start_rail': rail.id
                                })

                                # 检查是否冲突
                                check_result = self.check_back_position()
                                if check_result['conflict']:
                                    # 添加日志
                                    self.env["metro_park_dispatch.train_back_plan_log"].create([{
                                        "location": location.name,
                                        "train_no": cur_train.train_no,
                                        "rail": rail_no,
                                        "remark": '车辆回段冲突, 目标轨道{target_rail}, 原因{reason}!'.format(
                                            target_rail=plan.plan_back_rail.no, reason=check_result['reason'])
                                    }])
                                    # 通知场调重新安排计划
                                    self.trigger_up_event("funenc_socketio_server_msg", data={
                                        "msg_type": "notice_no_plan",
                                        "location": location.alias,
                                        "msg_data": {
                                            'train_id': train_id,
                                            'rail_no': value['start_rail']
                                        }
                                    })
                                else:
                                    # 添加日志, 之前出现过莫名妙的real_start_rail被写入了，导致计划无法触发
                                    self.env["metro_park_dispatch.train_back_plan_log"].create([{
                                        "location": location.name,
                                        "train_no": cur_train.train_no,
                                        "rail": rail_no,
                                        "remark": '车辆回段找到计划, 目标轨道{target_rail}!触发计划id为{id}'.format(
                                            target_rail=plan.plan_back_rail.no, id=plan.id)
                                    }])
                                    # 发布并执行计划
                                    _logger.info("begin publish plan!")
                                    plan.receive_train()
                    else:
                        _logger.info("the no zao cha status is error!")
                        self.env["metro_park_dispatch.train_back_plan_log"].create([{
                            "location": location.name,
                            "train_no": cur_train.train_no,
                            "rail": rail_no,
                            "remark": '出现车辆压入，但照查没有亮的情况(可能是发车)!'
                        }])
                    break
        except Exception as error:
            self.env["metro_park_dispatch.train_back_plan_log"].create([{
                "location": location.id,
                "train_no": train_no,
                "rail": rail_no,
                "remark": '检查车车入段出错{error}!'.format(error=error)
            }])

    @api.model
    def get_state_name(self, state):
        '''
        取得状态名名
        :return:
        '''
        for tmp_state in TRAIN_BACK_STATES:
            if tmp_state[0] == state:
                return tmp_state[1]

    @api.one
    @api.depends('exchange_rail_time')
    def _compute_plan_back_time(self):
        '''
        计算计划回库时间, 日期部份不作考虑，统一使用date
        :return:
        '''
        if self.exchange_rail_time:
            config = self.env["metro_park_base.system_config"].get_configs()
            back_train_need_min = config['back_train_need_min'] or 10
            self.plan_back_time = self.exchange_rail_time + back_train_need_min * 60
        else:
            self.plan_back_time = None

    @api.multi
    def get_plan_data(self, publish=False):
        '''
        取得命令数据
        :return:
        '''
        self.ensure_one()
        self._ensure_route()

        if self.state == 'unpublish' and publish:
            self.state = 'preparing'

        instructs = []
        if self.plan_details:
            # 道岔和区段
            for detail in self.plan_details:
                instructs.append(detail.build_instruct())

        if self.exchange_rail_time:
            tmp = utility.time_int_to_time(self.exchange_rail_time)
            start_time = pendulum.parse(str(self.date) + " " + tmp['time'])
            if tmp['next_day']:
                start_time = start_time.add(days=1)
            start_time = start_time.format('YYYY-MM-DD HH:mm:ss')
        else:
            start_time = None

        if self.real_back_tm:
            tmp = utility.time_int_to_time(self.real_back_tm)
            end_time = pendulum.parse(str(self.date) + ' ' + tmp['time'])
            if tmp['next_day']:
                end_time.add(days=1)
            end_time = end_time.format('YYYY-MM-DD HH:mm:ss')
        else:
            end_time = None

        data = {
            "id": self.id,
            "type": "train_back",  # 计划类型 train_dispatch 调车 train_back 收车 train_out 发车
            "start_time": start_time,  # 计划执行时间
            "end_time": end_time,  # 完成时间
            "trainId": self.train_id.train_no,  # 车号
            "trainNo": self.real_train_no if self.real_train_no else self.plan_train_no,  # 车次号
            "job": '收车',  # 作业内容
            "operation": "add",  # delete update add // 计划状态
            "state": self.get_state_name(self.state),  # 待执行, 信号未开放，执行中，已完成
            "start_rail": self.real_start_rail.no if self.real_start_rail else "待定",  # 源股道
            "start_rail_alias": self.real_start_rail.alias if self.real_start_rail else "待定",
            "end_rail": self.real_back_rail.no if self.real_back_rail else self.plan_back_rail.no,  # 目标股道
            "end_rail_alias": self.real_back_rail.alias if self.real_back_rail else self.plan_back_rail.alias,
            "instructs": instructs,
            "location": self.get_location_spell()
        }

        return data

    @api.multi
    def unlink(self):
        '''
        重写删除函数，通知前段删除对应数据
        '''

        if self:
            # records = self.filtered(lambda x: x.state != 'executing')
            records = self

            all_datas = [{'id': record.id, 'type': 'train_back'}
                         for record in records]
            # 此处为单个场调的操作，肯定是属于一个场段的计划，若不是，需在筛选出做处理
            location = self[0].get_location_spell()
            if location:
                self.trigger_up_event("funenc_socketio_server_msg", data={
                    "msg_type": "delete_plan",
                    "location": location,
                    "msg_data": all_datas
                }, room="xing_hao_lou")

            super(TrainBackPlan, records).unlink()

    @api.model
    def create_test_data(self):
        '''
        创建测试数据
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError('当前用户没有配置场段信息，请先进行配置')

        rails = self.env["metro_park_base.rails_sec"] \
            .search([('rail_type.name', '=', '停车/列检线'),
                     ('location', '=', location.id)])

        train_devs = self.env["metro_park_dispatch.cur_train_manage"] \
            .search([('train.dev_type.name', '=', '电客车')])

        # 不要用today, today是算的当日开始的时僮，加上8小时仍然不正确
        date_str = pendulum.now('UTC').add(hours=8).format('YYYY-MM-DD')

        datas = []
        for index, rail in enumerate(rails):
            if index >= len(train_devs):
                break
            exchange_rail_time = pendulum.now(
                "UTC").add(hours=1, minutes=index * 5)
            plan_back_time = exchange_rail_time.add(minutes=5)

            datas.append({
                'train_id': train_devs[index].id,
                'plan_back_location': location.id,
                'date': date_str,
                'plan_back_time': utility.time_str_to_int(plan_back_time.format(
                    'YYYY-MM-DD HH:mm:ss')),
                'plan_back_rail': rail.id,
                'exchange_rail_time': utility.time_str_to_int(exchange_rail_time.format(
                    'YYYY-MM-DD HH:mm:ss')),
                "plan_train_no": '10{index}'.format(index=index)
            })
        self.create(datas)

    @api.multi
    def mock_train_arrive(self):
        '''
        模拟车辆达到
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError('当前用户没有设置场段信息!')

        # 默认从1714回
        if location.alias == 'banqiao':
            rail = self.env['metro_park_base.rails_sec'].search([
                ('no', '=', 'T1714G'),
                ('location', '=', location.id)
            ])
        else:
            rail = self.env['metro_park_base.rails_sec'].search([
                ('no', '=', 'T2614G'),
                ('location', '=', location.id)
            ])

        cur_trains = \
            self.env["metro_park_dispatch.cur_train_manage"].search([])
        if len(cur_trains) > 0:
            cur_trains[0].cur_rail = rail.id
            cur_trains[0].notify_train_position_changed()

        self.real_start_rail = rail.id
        self.receive_train()

    @api.multi
    def check_back_position(self):
        '''
        检查回库位置
        :return:
        '''

        return {
            "conflict": False,
            "reason": 'A端已经被占用'
        }

        # 如果是回B端检查是否已经停了车
        rail = self.plan_back_rail
        if rail.port and rail.port == 'B':
            record = self.env['metro_park_dispatch.cur_train_manage'] \
                .search([('cur_rail', '=', rail.reverse_port.id)])
            if record:
                return {
                    "conflict": True,
                    "reason": 'A端已经被占用'
                }

        # 如果是在A端, 但B端的车又没有回去
        if rail.port and rail.port == 'A':
            # 如果还有计划并且还没有被占用的话, 那么车则回不去
            record = self.search(
                [('plan_back_rail', '=', rail.reverse_port.id)])
            if record:
                cur_train = self.env['metro_park_dispatch.cur_train_manage'] \
                    .search([('cur_rail', '=', rail.reverse_port.id)])
                if not cur_train:
                    return {
                        "conflict": True,
                        "reason": 'B端车还没有回库'
                    }

        # 检查自身股道是否被占用
        cur_train = self.env['metro_park_dispatch.cur_train_manage'] \
            .search([('cur_rail', '=', rail.id)])
        if cur_train:
            return {
                "conflict": True,
                "reason": '回库股道已经被占用'
            }

        # 检查当前收车计划之后是否还有发车计划
        # after_train_back = self.search([('plan_back_time', ">", str(self.plan_back_time)),
        #                                 ('state', 'in', ['preparing', 'executing'])],
        #                                order="plan_back_time asc")
        # if after_train_back:
        #     rule_infos = self.env["metro_park_maintenance.rule_info"] \
        #         .search([('dev_id', '=', self.train_id.id),
        #                  ('work_start_time', '>', str(self.plan_back_time)),
        #                  ('work_start_time', '<', str(after_train_back.plan_back_time))])
        # else:
        #     rule_infos = self.env["metro_park_maintenance.rule_info"] \
        #         .search([('dev_id', '=', self.train_id.id),
        #                  ('work_start_time', '>', str(self.plan_back_time)),
        #                  ('work_start_time', '<', str(after_train_back.plan_back_time))])
        # if rule_infos:
        #     rule_info = rule_infos[0]
        #     rail_properties = rule_info.mapped('')
        #     for rail_property in rail_properties:
        #         if rail_property not in self.plan_back_rail.rail_property:
        #             return {
        #                 "conflict": True,
        #                 "reason": '检修轨道不符合要求!'
        #             }

        return {
            "conflict": False
        }

    @api.model
    def create(self, vals_list):
        recs = super(TrainBackPlan, self).create(vals_list)
        try:
            config = self.env['metro_park_base.system_config'].get_configs()
            start_pms = config.get('start_pms', False)
            if start_pms == 'yes':
                for rec in recs:
                    main_threading = threading.Thread(
                        target=self.env['mdias_pms_interface'].transceiver_vehicle_information,
                        args=[rec, 'train_back_plan'],
                        daemon=True)
                    main_threading.start()
        except Exception as f:
            _logger.info('PMS基础信息配置错误' + str(f))
        return recs

    @api.model
    def is_target_rail_free(self, target_rail):
        '''
        检查当前的轨道是否被点用
        :return:
        '''
        records = self.env["metro_park_dispatch.cur_train_manage"].search(
            [('cur_rail', '=', target_rail)])
        if len(records) > 0:
            return False
        return True

    @api.model
    def check_route(self, rail_ids, switch_ids):
        '''
        检查路径是否被占用
        '''
        busy_rails = self.env['metro_park_base.rails_sec'].search(
            [('id', 'in', rail_ids)])
        if len(busy_rails):
            return True

        busy_switches = self.env['metro_park_base.switches'].search(
            [('id', 'in', switch_ids)])
        if len(busy_switches):
            return True

        return False

    @api.model
    def check_in_construction(self):
        '''
        检查是不是正在施工
        :return:
        '''
        return False

    @api.model
    def dynamic_plan_rail(self, train_no, location_id):
        '''
        如果回来的车位置被占用了，那么动态的去找一个轨道进行安排
        :return:
        '''
        pass
