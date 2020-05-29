# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import datetime
import logging
_logger = logging.getLogger(__name__)

DETAIL_STATE = [('finished', '已完成'),
                ('executing', '执行中'),
                ('wait_accept', '待推入'),
                ('rebacked', '已经撤回')]


class TrainBackOutDetail(models.Model):
    '''
    收发车每一勾详情
    '''
    _name = "metro_park_dispatch.train_back_out_detail"

    sequence = fields.Integer(string="序号")

    # 这个作为target rail
    rail = fields.Many2one(string='目标股道',
                           comodel_name='metro_park_base.rails_sec')

    source_rail = fields.Many2one(string='起始股道',
                                  comodel_name='metro_park_base.rails_sec')

    back_plan_id = fields.Many2one(
        comodel_name='metro_dispatch_dispatch.train_back_plan', string='收车计划')
    out_plan_id = fields.Many2one(
        comodel_name='metro_dispatch_dispatch.train_out_plan', string='发车计划')

    interlock_routes = fields.One2many(string="联锁进路",
                                       comodel_name="metro_park_dispatch.dispatch_detail_route_info",
                                       inverse_name="back_out_plan_id")
    work_start_time = fields.Datetime(string='开始时间')
    work_end_time = fields.Datetime(string='结束时间')

    state = fields.Selection(selection=DETAIL_STATE,
                             default="wait_accept", string="状态")
    remark = fields.Text(string='注意事项')

    @api.model
    def update_state(self, detail_state):
        '''
        更新状态
        :param detail_state: 详情的id和状态字典
        :return:
        '''
        record = self.browse(detail_state['id'])
        if not record:
            _logger.error("调车详情不存在")
            raise exceptions.ValidationError("调车详情不存在")

        if record.state != detail_state['state']:
            if detail_state['state'] == 'executing':
                record.work_start_time = datetime.datetime.now()
            elif detail_state['state'] == 'finished':
                record.work_end_time = datetime.datetime.now()
        record.state = detail_state['state']
        return record

    @api.model
    def get_state_name(self, state):
        '''
        取得状态名名
        :return:
        '''
        for tmp_state in DETAIL_STATE:
            if tmp_state[0] == state:
                return tmp_state[1]

    @api.multi
    def build_instruct(self):
        '''
        创建命令, 需要传递经过的道岔和区段信息
        ["3", "5", "7", "13", "15", "21", "23", "23_61WG", "61", "20G"]
        :return:
        '''
        self.ensure_one()

        # 到B股的收车或者从B股的发车
        is_dispatch = self.source_rail.port == 'B' or self.rail.port == 'B'

        # 道岔和区段
        rail_and_switches = []
        # 防护道岔
        protect_switches = []
        # 道岔方向信息
        switches_direction = {}

        if is_dispatch:
            routes = self.env['metro_park.interlock.route']\
                .search_dispatch_route(self.source_rail.location.id, self.source_rail, self.rail)
        else:
            routes = self.env['metro_park.interlock.route']\
                .search_train_plan_route(self.source_rail.location.id, self.source_rail,
                                         self.rail, "back_plan" if self.back_plan_id else "out_plan")
        if not routes:
            raise exceptions.ValidationError(
                "未找到%s->%s的路径" % (self.source_rail.no, self.rail.no))

        if self.interlock_routes:
            self.interlock_routes.unlink()

        write_routes = []
        for index, route in enumerate(routes[0]):
            rail_and_switches += route.get_rail_and_switches()
            protect_switches += route.get_protect_switches()
            switches_direction.update(route.get_switches_direction())
            write_routes.append((0, 0, {
                "index": index,
                'route_id': route.id
            }))

        self.write({
            "interlock_routes": write_routes
        })

        self._cr.commit()

        operation_btns = "%s %s" % (
            str(self.interlock_routes[0].route_id.mdias_press_start).upper(),
            str(self.interlock_routes[-1].route_id.mdias_press_end).upper())

        return {
            "id": self.id,
            "sequence": self.sequence,
            "type": 'train_dispatch' if is_dispatch else "train_back" if self.back_plan_id else "train_out",
            "condition": None,
            # 司机确认状态
            # 故障, 待执行, 信号未开放，执行中，已完成
            "state": self.get_state_name(self.state),
            # 开始和完成时间
            "start_time": None if not self.work_start_time else pendulum.parse(
                str(self.work_start_time)).format('YYYY-MM-DD HH:mm:ss'),
            "end_time": None if not self.work_end_time else pendulum.parse(
                str(self.work_end_time)).format('YYYY-MM-DD HH:mm:ss'),
            # 可显示排列进路按钮
            "prepare": True,
            # 源和目标股道
            "start_rail": self.source_rail.no,
            "start_rail_alias": self.source_rail.alias,
            "end_rail": self.rail.no,
            "end_rail_alias": self.rail.alias,
            # 是否需要手动确认, 默认为False, 区分是作业指令还是非作业指令
            "manual_confirm": False,
            # 注意事项
            "attention": self.remark,
            "job": self.remark,
            "show_operation_btns": True,
            # 监控股道道岔, 根据这些信息判断进路是否完成
            "sections": list(set(rail_and_switches)),
            # 防护道岔
            "protect_switches": protect_switches,
            # 道岔方向
            "switches_direction": switches_direction,
            # 操作按扭
            "operation_btns": operation_btns
        }
