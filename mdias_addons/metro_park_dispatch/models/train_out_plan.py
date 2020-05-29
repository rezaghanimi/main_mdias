# -*- coding: utf-8 -*-

import logging
import threading

import pendulum

from odoo import models, fields, api, exceptions
from . import utility

_logger = logging.getLogger(__name__)

TRAIN_OUT_STATES = [('finished', '已完成'),
                    ('preparing', '待发车'),
                    ('executing', '执行中'),
                    ('canceled', '已取消'),
                    ('unpublish', '未发布')]


class TrainOutPlan(models.Model):
    '''
    发车计划
    '''
    _name = 'metro_park_dispatch.train_out_plan'
    _description = '发车计划'
    _rec_name = 'train_id'
    _track_log = True

    day_plan_id = fields.Many2one(string='日计划',
                                  comodel_name='metro_park_dispatch.day_run_plan')
    date = fields.Date(string="日期",
                       help="冗余信息, 方便查询",
                       default=lambda self: pendulum.today("UTC"))

    exchange_rail_time = fields.Integer(string='转换轨时间',
                                        help="运行图要求的时间或手动添加的时间")

    plan_train_no = fields.Char(string='车次')
    real_train_no = fields.Char(string='实际车次')

    # 根据这个位置
    train_id = fields.Many2one(string='车辆',
                               comodel_name='metro_park_dispatch.cur_train_manage')

    # 计划出库位置
    plan_out_location = fields.Many2one(
        comodel_name="metro_park_base.location", string="计划位置")

    # 发车指的是当前的位置
    plan_out_rail = fields.Many2one(string='位置',
                                    comodel_name='metro_park_base.rails_sec',
                                    domain="[('location.id', '=', plan_out_location)]")
    # 出场段位置
    plan_out_end_rail = fields.Many2one(
        string='出场段位置',
        comodel_name='metro_park_base.rails_sec',
        domain="[('location.id', '=', plan_out_location), ('rail_type.name', '=', '转换轨')]")

    plan_out_time = fields.Integer(string='出库时间')
    real_out_time = fields.Integer(string='实际时间')

    immediately = fields.Boolean(string="立即",
                                 default=False,
                                 help="用于区分是否立即发车")

    plan_details = fields.One2many(string="勾计划详情",
                                   comodel_name="metro_park_dispatch.train_back_out_detail",
                                   inverse_name="out_plan_id")
    split_routes = fields.Boolean(string="路径拆分",
                                  default=False)

    state = fields.Selection(string='状态',
                             selection=TRAIN_OUT_STATES,
                             default="unpublish")

    plan_info_id = fields.Many2one(string="metro_park_maintenance.rule_info",
                                   help="计划id")

    remark = fields.Text(string='备注')
    button = fields.Char(string="操作")
    track_ids = fields.One2many(
        'metro_park_dispatch.train_track', 'out_id', string='报点位置')

    # work_shop_day_plan_id = fields.Many2one(comodel_name="metro_park_dispatch.work_shop_day_plan",
    #                                         string='车间日生产计划')
    # work_shop_data_id = fields.Many2one(comodel_name="metro_park_dispatch.work_shop_day_plan_data",
    #                                     string="车间日生产计划数据")

    @api.model
    def get_all_out_plan_action(self):
        '''
        out plan action
        '''
        if not self.env.user.cur_location:
            raise exceptions.Warning("当前用户没有配置位置")

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "metro_park_dispatch.train_out_plan",
            "name": "发车计划",
            "views": [[self.env.ref('metro_park_dispatch.train_out_plan_list').id, "tree"]],
            "domain": [("plan_out_location.alias", "=", self.env.user.cur_location.alias)]
        }

    @api.multi
    def dispatch_now(self):
        '''
        立即发车, 信号楼弹出对话框
        :return:
        '''
        if self.state == 'unpublish':
            raise exceptions.Warning('当前计划尚未发布，请先发布!')
        else:
            self.state = 'preparing'
            self.trigger_up_event("funenc_socketio_server_msg", data={
                "msg_type": "excute_plan",
                "location": self.get_location_spell(),
                "msg_data": {
                    'type': "train_out",
                    "id": self.id
                }
            }, room="xing_hao_lou")
            log = {
                'type': 'out_plan',
                'train_dev': self.train_id.train.id,
                'operation': '立即发车'
            }
            self.env['metro_park_dispatch.train_in_out_log'].create(log)

    @api.multi
    def dispatch_request_point(self):
        '''
        报点
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.train_track",
            "view_mode": 'tree',
            "target": "new",
            'domain': [('out_id', '=', self.id)],
            "views": [[self.env.ref(
                'metro_park_dispatch.tree_track_view').id, "list"]],
            'context': dict(self.env.context, create=False)
        }

    @api.model
    def update_state(self, plan_state):
        '''
        发车用的id和计划id是同一个id
        :param plan_id:
        :param state:
        :return:
        '''
        if plan_state['state'] not in [item[0] for item in TRAIN_OUT_STATES]:
            _logger.error("状态不正确")
        record = self.browse(plan_state['id'])
        if not record:
            _logger.error("计划不存在")
            raise exceptions.ValidationError("计划不存在")
        if record.state != plan_state['state']:
            if plan_state['state'] == 'executing':
                record.real_out_time = utility.get_now_time_int_repr()
                today = pendulum.today('UTC')
                # 可能在前一天也可能在后一天
                plan_date = pendulum.parse(str(record.date))
                if today > plan_date:
                    record.real_out_time += 24 * 60 * 60
                elif today < plan_date:
                    record.real_out_time -= 24 * 60 * 60
            elif plan_state['state'] == 'finished':
                record.exchange_rail_time = utility.get_now_time_int_repr()
                today = pendulum.today('UTC')
                # 可能在前一天也可能在后一天
                plan_date = pendulum.parse(str(record.date))
                if today > plan_date:
                    record.exchange_rail_time += 24 * 60 * 60
                elif today < plan_date:
                    record.exchange_rail_time -= 24 * 60 * 60

            # 通知前端刷新界面
            self.trigger_up_event("funenc_socketio_server_msg", data={
                "msg_type": "update_train_out_plan_state",
                "plan_id": self.id,
                "location_alias": record.plan_out_rail.location.alias
            })

        record.state = plan_state['state']
        if 'detail_state' in plan_state:
            self.env['metro_park_dispatch.train_back_out_detail'].sudo(
            ).update_state(plan_state['detail_state'])

    @api.multi
    def get_location_spell(self):
        '''
        取得位置
        :return:
        '''
        self.ensure_one()

        location = None
        try:
            if self.plan_out_rail and self.plan_out_rail.location:
                location = self.plan_out_rail.location.alias
            else:
                location = self.env.user.cur_location.alias
        except Exception as e:
            _logger.info(e)

        return location

    @api.multi
    def cancel_train_plan(self):
        '''
        取消计划
        :return:
        '''
        self.state = 'canceled'
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "reback_plan",
            "location": self.get_location_spell(),
            "msg_data": [{
                'type': 'train_out',
                "id": self.id
            }]
        }, room="xing_hao_lou")
        log = {
            'type': 'out_plan',
            'train_dev': self.train_id.train.id,
            'operation': '取消发车'
        }
        self.env['metro_park_dispatch.train_in_out_log'].create(log)

    # @api.multi
    # def reback_train_plan(self):
    #     '''
    #     撤回计划, 场/检调主动撤销
    #     :return:
    #     '''
    #     self.state = 'unpublish'
    #     self.trigger_up_event("funenc_socketio_server_msg", data={
    #         "msg_type": "reback_plan",
    #         "location": self.get_location_spell(),
    #         "msg_data": [{
    #             'type': 'train_out',
    #             "id": self.id
    #         }]
    #     }, room="xing_hao_lou")
    #     log = {
    #         'type': 'out_plan',
    #         'train_dev': self.train_id.id,
    #         'operation': '撤回计划'
    #     }
    #     self.env['metro_park_dispatch.train_in_out_log'].create(log)

    @api.model
    def reback_plan(self, id):
        '''
        撤回计划, 信号楼发起撤销, 这里只是个回调函数, 给信号楼回调使用
        :return:
        '''
        plan = self.browse(id)
        plan.state = 'canceled'
        return True

    @api.multi
    def _search_route(self):
        '''
        搜索进路, 转换轨1出，转换轨2入, 如果不是在运用库的话要先调车
        :return:
        '''
        self.ensure_one()
        details = []
        if self.plan_out_rail and self.plan_out_end_rail:
            all_routes = self.env["metro_park.interlock.route"] \
                .search_train_plan_route(self.plan_out_rail.location.id,
                                         self.plan_out_rail, self.plan_out_end_rail, 'out_plan')
            split_index = 1
            route_size = len(all_routes)
            if route_size == 2:
                # 从B端到A端
                details.append((0, 0, {
                    'sequence': split_index,
                    "source_rail": all_routes[0].start_rail.id,
                    "rail": all_routes[0].end_rail.id,
                    "interlock_routes": [
                        (0, 0, {
                            "index": i,
                            "route_id": route.id
                        }) for i, route in enumerate(all_routes[0])]
                }))
                split_index += 1

            if route_size:
                # 到总入总出
                if len(all_routes[-1]) > 1:
                    details.append((0, 0, {
                        'sequence': split_index,
                        "source_rail": all_routes[-1][0].start_rail.id,
                        "rail": all_routes[-1][-2].end_rail.id,
                        "interlock_routes": [
                            (0, 0, {
                                "index": i,
                                "route_id": route.id
                            }) for i, route in enumerate(all_routes[-1][0:-1])]
                    }))
                    split_index += 1
                # 总入总出到场段外
                details.append((0, 0, {
                    'sequence': split_index,
                    "source_rail": all_routes[-1][-1].start_rail.id,
                    "rail": all_routes[-1][-1].end_rail.id,
                    "interlock_routes": [
                        (0, 0, {
                            "index": i,
                            "route_id": route.id
                        }) for i, route in enumerate(all_routes[-1][-1])]
                }))

            if details:
                self.plan_details = details
            else:
                raise exceptions.ValidationError("没有找到进路，请确定联锁表已经导入!")
        else:
            raise exceptions.ValidationError("未设置发车开始或结束位置！")

    @api.onchange("plan_out_location")
    def on_change_plan_out_location(self):
        '''
        计化位置发生改变
        :return:
        '''
        if self.plan_out_rail and self.plan_out_location and self.plan_out_rail.location.id \
                != self.plan_out_location.id:
            self.plan_out_rail = False

    @api.model
    def get_state_name(self, state):
        '''
        取得状态名
        :return:
        '''
        for tmp_state in TRAIN_OUT_STATES:
            if tmp_state[0] == state:
                return tmp_state[1]

    @api.onchange('plan_out_time')
    def _compute_exchange_rail_time(self):
        '''
        计算转换轨道时间
        :return:
        '''
        if self.plan_out_time:
            config = self.env["metro_park_base.system_config"].get_configs()
            out_train_pre_min = config['out_train_pre_min'] or 10
            self.exchange_rail_time = self.plan_out_time + out_train_pre_min * 60
        else:
            self.exchange_rail_time = None

    @api.multi
    def cancel_plan(self):
        '''
        需要通知信号楼取消调车
        :return:
        '''
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "cancel_plan",
            "location": self.get_location_spell(),
            "msg_data": [{
                'type': 'train_out',
                "id": self.id
            }]
        }, room="xing_hao_lou")

    @api.multi
    def get_plan_data(self, publish=False):
        '''
        取得信号楼命令数据
        :return:
        '''
        self.ensure_one()

        location = self.plan_out_rail.location

        if self.plan_details:
            self.plan_details = [(5, 0, 0)]

        self._search_route()

        if self.state == 'unpublish' and publish:
            self.state = 'preparing'

        if self.plan_details:

            # 道岔和区段
            instructs = []
            for detail in self.plan_details:
                instructs.append(detail.build_instruct())

            # 由于存在数据库里为utc时间，所以需要加8小时给前端
            date_obj = pendulum.parse(str(self.date))
            tmp = utility.time_int_to_time(self.plan_out_time)
            if tmp['next_day']:
                date_obj.add(days=1)
            date_str = date_obj.format('YYYY-MM-DD')
            time_str = pendulum.parse(tmp['time']).format('HH:mm:ss')
            start_time = pendulum.parse(date_str + " " + time_str)

            # 还需要减去排计划的提前量
            start_time = start_time.subtract(
                minutes=location.plan_rail_pre_min)

            real_out_time = None
            if self.real_out_time:
                tmp = utility.time_int_to_time(self.real_out_time)
                date_obj = pendulum.parse(str(self.date))
                if tmp['next_day']:
                    date_obj.add(days=1)
                real_out_time = pendulum.parse(
                    date_str + " " + time_str).format('YYYY-MM-DD HH:mm:ss')

            data = {
                "id": self.id,
                "type": "train_out",  # 计划类型 train_dispatch 调车 train_back 收车 train_out 发车
                # 计划执行时间
                "start_time": start_time.format('YYYY-MM-DD HH:mm:ss'),
                # 完成时间
                "end_time": real_out_time,
                "trainId": self.train_id.train_no,  # 车号
                "trainNo": self.real_train_no if self.real_train_no else self.plan_train_no,  # 车次号
                "job": '发车',  # 作业内容
                "operation": "add",  # delete update add // 计划状态
                "state": self.get_state_name(self.state),  # 待执行,信号未开放，执行中，已完成
                "start_rail": self.plan_out_rail.no,  # 源股道
                "start_rail_alias": self.plan_out_rail.alias,
                "end_rail": self.plan_out_end_rail.no,  # 目标股道
                "end_rail_alias": self.plan_out_end_rail.alias,
                "instructs": instructs,
                "location": self.get_location_spell()
            }

            return data
        else:
            return None

    @api.multi
    def unlink(self):
        '''
        重写删除函数，通知前段删除对应数据
        '''
        if self:
            # 暂时可以删除所有
            # records = self.filtered(lambda x: x.state != 'executing')
            records = self

            all_datas = [{'id': record.id, 'type': 'train_out'}
                         for record in records]
            # 此处为单个场调的操作，肯定是属于一个场段的计划，若不是，需在筛选出做处理
            location = self[0].get_location_spell()
            self.trigger_up_event("funenc_socketio_server_msg", data={
                "msg_type": "delete_plan",
                "location": location,
                "msg_data": all_datas
            }, room="xing_hao_lou")

            super(TrainOutPlan, records).unlink()

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

        if location.alias == 'banqiao':
            exchange_rail = self.env.ref(
                'metro_park_base_data_10.ban_qiao_T1701G').id
        else:
            exchange_rail = self.env.ref(
                'metro_park_base_data_10.gao_da_lu_rail_T2617G').id

        datas = []
        for index, rail in enumerate(rails):
            if index >= len(train_devs):
                break

            # 提前5分钟发车
            plan_out_time = utility.get_now_time_int_repr() + 3 * 60 + index * 60
            exchange_rail_time = plan_out_time - 5 * 60

            datas.append({
                'train_id': train_devs[index].id,
                'plan_out_location': location.id,
                'date': date_str,
                'plan_out_time': plan_out_time,
                'plan_out_rail': rail.id,
                'plan_out_end_rail': exchange_rail,
                'exchange_rail_time': exchange_rail_time,
                "plan_train_no": '10{index}'.format(index=index)
            })
        self.create(datas)

    @api.multi
    def mock_send_train(self):
        '''
        模拟车辆达到
        :return:
        '''
        self.dispatch_now()

    @api.model
    def create(self, vals_list):
        recs = super(TrainOutPlan, self).create(vals_list)
        try:
            config = self.env['metro_park_base.system_config'].get_configs()
            start_pms = config.get('start_pms', False)
            if start_pms == 'yes':
                for rec in recs:
                    main_threading = threading.Thread(
                        target=self.env['mdias_pms_interface'].transceiver_vehicle_information,
                        args=[rec, 'train_out_plan'],
                        daemon=True)
                    main_threading.start()
        except Exception as f:
            _logger.info('PMS基础信息配置错误' + str(f))
        return recs
