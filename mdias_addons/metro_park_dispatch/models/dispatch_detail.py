# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import datetime
import logging
from pytz import timezone
_logger = logging.getLogger(__name__)

tz_cn = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')

DETAIL_STATE = [
    ('wait_accept', '待执行'),
    ('executing', '执行中'),
    ('finished', '已完成')
]


class DispatchDetail(models.Model):
    '''
    调车详情，用于保存调车通知单的列表内容 一个勾计划
    '''
    _name = 'metro_park_dispatch.dispatch_detail'
    _description = '调车详情'
    _order = "sequence"
    _track_log = True

    @api.multi
    def _get_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            if self.source_rail:
                domain.append(('id', '!=', self.source_rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    @api.multi
    def _get_source_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            if self.rail:
                domain.append(('id', '!=', self.rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    sequence = fields.Integer(string="序号", default=-1)
    display_sequence = fields.Integer(
        string="显示序号", compute="_compute_display_sequence")
    notice_id = fields.Many2one(string='调车通知单',
                                comodel_name='metro_park_dispatch.dispatch_notice')

    # 这里有可能是调其它的工程车，所以不能使用notice_id的train
    train = fields.Many2one(string="车辆",
                            comodel_name="metro_park_dispatch.cur_train_manage")

    rail = fields.Many2one(string='目标股道',
                           comodel_name='metro_park_base.rails_sec',
                           domain=_get_rail_domain,
                           help="这个相当于是target rail")

    source_rail = fields.Many2one(string='起始股道',
                                  comodel_name='metro_park_base.rails_sec',
                                  domain=_get_source_rail_domain)

    plan_name = fields.Char(string="计划名称", help="这里实际上是要关联到计划")
    operation = fields.Many2one(comodel_name="metro_park_dispatch.operation",
                                string="操作")

    # 关联的联锁进路，相关信息要从这里获取
    interlock_routes = fields.One2many(string="联锁进路",
                                       comodel_name="metro_park_dispatch.dispatch_detail_route_info",
                                       inverse_name="detail_id")
    # 调车时间, 这个时间不需要
    work_start_time = fields.Datetime(string='开始时间')
    work_end_time = fields.Datetime(string='结束时间')
    display_time = fields.Char(string="显示时间", compute="_compute_display_time")

    train_num = fields.Many2one(string='数量',
                                comodel_name="metro_park_dispatch.train_num")
    train_num_text = fields.Char(string="车辆总数",
                                 compute="_compute_train_num_txt",
                                 help="由于要显示单机等, 所以这里要计算下")

    notice_time = fields.Datetime(string='计划下达时间', help="计划下达时间")

    state = fields.Selection(selection=DETAIL_STATE,
                             default="wait_accept", string="状态", inverse=lambda self: self._inverse_state(),  store=True)

    remark = fields.Text(string='注意事项')
    execute_start_time = fields.Datetime(string='命令执行开始时间')
    execute_end_time = fields.Datetime(string='命令执行结束时间')
    driver_state = fields.Selection([('lock', '锁定'),
                                     ('wait_dispatch', '待调车'),
                                     ('wait_signal_open', '待信号开放'),
                                     ('executing', '执行中'),
                                     ('finished', '完成')
                                     ], string='司机操作状态', default='lock')

    def _inverse_state(self):
        for record in self:
            if record.state == 'executing':
                record.driver_state = 'executing'
            if record.state == 'finished' and record.driver_state in ['wait_signal_open', 'wait_dispatch']:
                record.driver_state = 'executing'

    @api.onchange("source_rail")
    def on_source_rail_change(self):
        return {
            "domain": {
                "rail": self._get_rail_domain()
            }
        }

    @api.onchange("rail")
    def on_rail_change(self):
        return {
            "domain": {
                "source_rail": self._get_source_rail_domain()
            }
        }

    @api.onchange('sequence')
    def on_change_sequence(self):
        '''
        改变序号
        :return:
        '''
        if self.sequence == -1:
            self.sequence = len(self.notice_id.dispatch_detail)

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
    def _compute_display_time(self):
        '''
        显示时间
        :return:
        '''
        for record in self:
            record.display_time = \
                str(record.work_start_time).split(":")[1] \
                + "-" \
                + str(record.work_end_time).split(":")[1]

    @api.depends('source_rail', 'rail')
    def _compute_from_wash(self):
        '''
        计算是否从洗车线经过
        :return:
        '''
        raise exceptions.Warning('线别没有实现_compute_from_wash函数')

    @api.model
    def get_state_name(self, state):
        '''
        取得状态名名
        :return:
        '''
        for tmp_state in DETAIL_STATE:
            if tmp_state[0] == state:
                return tmp_state[1]

    @classmethod
    def _format_datetime_to_time(cls, datetime_obj):
        if not datetime_obj:
            return ''
        return datetime_obj.replace(tzinfo=utc_tz).astimezone(tz_cn).strftime('%H:%M:%S')

    @api.multi
    def build_instruct(self, refresh_routes=False):
        '''
        创建命令, 需要传递经过的道岔和区段信息
        ["3", "5", "7", "13", "15", "21", "23", "23_61WG", "61", "20G"]
        :return:
        '''
        self.ensure_one()

        # 道岔和区段
        rail_and_switches = []
        # 防护道岔
        protect_switches = []
        # 道岔方向信息
        switches_direction = {}
        routes = self.env['metro_park.interlock.route'].search_dispatch_route(
            self.source_rail.location.id, self.source_rail, self.rail)
        if not routes:
            raise exceptions.ValidationError(
                "未找到%s->%s的路径" % (self.source_rail.no, self.rail.no))

        if self.notice_id.state not in ['wait_executing', 'executing', 'finished'] or refresh_routes:
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
        else:
            for route in self.interlock_routes:
                rail_and_switches += route.route_id.get_rail_and_switches()
                protect_switches += route.route_id.get_protect_switches()
                switches_direction.update(
                    route.route_id.get_switches_direction())

        start_rail_alias = self.source_rail.alias
        if self.notice_id.is_wash and self.notice_id.get_location_spell() == "gaodalu" and start_rail_alias == "牵3":
            start_rail_alias = "%s(经洗车线)" % (start_rail_alias)

        # 卸车线有可能会一直占用掉，所以这里要移除掉
        if self.notice_id.get_location_spell() == "banqiao" and \
                self.source_rail.id == self.env.ref("metro_park_base_data_10.ban_qiao_36G").id:
            rail_and_switches.remove(self.source_rail.no)

        return {
            "id": self.id,
            "is_wash": self.notice_id.is_wash,
            "location": self.notice_id.get_location_spell(),
            "sequence": self.sequence,
            "type": "train_dispatch",
            "condition": None,  # 司机确认状态
            "state": self.get_state_name(self.state),  # 故障, 待执行, 信号未开放，执行中，已完成
            # 开始和完成时间
            "start_time": None if not self.work_start_time else pendulum.parse(
                str(self.work_start_time)).format('YYYY-MM-DD HH:mm:ss'),
            "end_time": None if not self.work_end_time else pendulum.parse(
                str(self.work_end_time)).format('YYYY-MM-DD HH:mm:ss'),
            "prepare": True,  # 可显示排列进路按钮
            "operation": self.operation.name,
            "train_num": self.train_num_text,
            # 源和目标股道
            "start_rail": self.source_rail.no,
            "end_rail": self.rail.no,
            "start_rail_alias": start_rail_alias,
            "end_rail_alias": self.rail.alias,
            "start_rail_alia": start_rail_alias,
            "end_rail_alia": self.rail.alias,
            "manual_confirm": False,      # 是否需要手动确认, 默认为False, 区分是作业指令还是非作业指令
            "attention": self.remark,   # 注意事项
            "job": self.remark,
            # 监控股道道岔,
            # 若rail_and_switches为空，一定要设置终点的监控状态
            "sections": list(set(rail_and_switches)),
            # 防护道岔
            "protect_switches": list(set(protect_switches)),
            # 道岔方向
            "switches_direction": switches_direction,
            # 操作按扭
            "operation_btns": "%s %s" % (
                str(self.interlock_routes[0].route_id.mdias_press_start).upper(
                ),
                str(self.interlock_routes[-1].route_id.mdias_press_end).upper()),
            'execute_start_time': self._format_datetime_to_time(self.work_start_time),
            'execute_end_time': self._format_datetime_to_time(self.work_end_time),
            'driver_state': self.driver_state,
            'cmd_state': self.state,
        }

    @api.model
    def request_start_plan(self, data):
        '''
        移动端请求开始调车，先操作端发起调车提示
        '''
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "request_start_plan",
            "msg_data": data
        }, room="xing_hao_lou")

        return True

    @api.onchange("source_rail")
    def on_change_source_rail(self):
        '''
        更改源轨道
        :return:
        '''
        if self.rail and self.source_rail \
                and self.source_rail == self.rail:
            self.rail = False

    @api.onchange("operation")
    def on_change_operation(self):
        '''
        更改操作
        :return:
        '''
        if not self.operation or self.operation.name == '无':
            self.train_num = False

    @api.depends("train_num")
    def _compute_train_num_txt(self):
        '''
        计算车辆总数, 只有一辆车的情况下显示单机 △
        :return:
        '''
        train_num_total = 1
        records = self.sorted('sequence')
        for index, record in enumerate(records):
            if record.operation.name == '' and record.train_num:
                train_num_total = train_num_total + record.train_num
            elif record.operation.name == '':
                train_num_total = train_num_total - record.train_num

            if train_num_total == 1:
                record.train_num_txt = '△'
            else:
                record.train_num_txt = str(train_num_total)

    @api.depends('sequence')
    def _compute_display_sequence(self):
        '''
        显示序号
        :return:
        '''
        for record in self:
            record.display_sequence = record.sequence
