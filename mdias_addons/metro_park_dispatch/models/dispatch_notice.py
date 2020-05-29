# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import json
from .dispatch_request import DISPATCH_STATE
import datetime


class DispatchNotice(models.Model):
    '''
    调车通知 dispatch_detail 包含勾计划
    包含一个或多个instruct，instruct又包含了具体的进路，可能有多条。
    '''
    _name = 'metro_park_dispatch.dispatch_notice'
    _description = '调车通知'
    _track_log = True

    request_id = fields.Many2one(string='调车申请',
                                 comodel_name='metro_park_dispatch.dispatch_request')

    batch_no = fields.Char(string='调车批次', help="手动填写", required=True)

    dispatch_group = fields.Many2one(
        string='调车班组', comodel_name='funenc.wechat.department')
    dispatch_driver = fields.Many2one(
        string="调车司机", comodel_name="funenc.wechat.user")
    park_dispatcher = fields.Many2one(
        string='场调班组', comodel_name='funenc.wechat.department')

    notice_time = fields.Datetime(string='通知时间', help="通知单下达时间")

    # 关联显示项
    train = fields.Many2one(string="车", related="request_id.train")
    dev_type = fields.Many2one(string='车辆类型', related="request_id.dev_type")

    dispatch_date = fields.Date(
        string="调车日期", related="request_id.dispatch_date")
    start_time = fields.Datetime(
        string='开始时间', related="request_id.start_time")
    finish_time = fields.Datetime(
        string='结束时间', related="request_id.finish_time")
    display_time = fields.Char(
        string="显示时间", related="request_id.display_time")

    dispatch_type = fields.Selection(
        string='调车类型', related="request_id.dispatch_type")

    is_wash = fields.Boolean(string='是否洗车', related="request_id.is_wash")

    source_rail = fields.Many2one(
        string='起始股道', related="request_id.source_rail")
    target_rail = fields.Many2one(
        string='目标股道', related='request_id.target_rail')

    work_content = fields.Text(
        string='作业内容',
        related='request_id.work_content')

    state = fields.Selection(string="状态", related="request_id.state")

    iron_shoe_no = fields.Char(string='铁鞋号', related='request_id.iron_shoe_no')
    iron_shoe_place = fields.Char(
        string='铁鞋位置', related='request_id.iron_shoe_place')

    # 调车详情, 这里只是个中间信息
    dispatch_detail = fields.One2many(string="调车详情",
                                      comodel_name="metro_park_dispatch.dispatch_detail",
                                      inverse_name="notice_id")
    publish_time = fields.Datetime(string='发布时间')

    remark = fields.Text(string='备注')
    driver_finished = fields.Boolean(default=False)

    @api.multi
    def get_location_spell(self):
        '''
        取得位置
        :return:
        '''
        self.ensure_one()

        if self.target_rail:
            location = self.target_rail.location.alias
        else:
            location = self.env.user.cur_location.alias

        return location

    @api.multi
    def check_rails(self):
        '''
        检查调车股道先后是否一致, 手动添加的项由于sequence没有发生变动，会导致顺序混乱问题
        :return:
        '''
        self.ensure_one()
        if len(self.dispatch_detail) > 1:
            ids = self.dispatch_detail.ids
            records = self.env["metro_park_dispatch.dispatch_detail"]\
                .search([("id", "in", ids)], order="sequence asc, id asc")
            last_record = None

            for index, record in enumerate(records):
                if not last_record:
                    last_record = record
                    continue
                if record.source_rail.id != last_record.rail.id:
                    raise exceptions.ValidationError("调车股道先后不一致！")
                last_record = record

    @api.multi
    def write(self, vals):
        '''
        更新计划
        :param vals:
        :return:
        '''
        for sel in self:
            super(DispatchNotice, sel).write(vals)
        return True

    @api.model
    def get_unfinished_plans(self, alias):
        '''
        取得待执行的计划
        :return:
        '''
        plans = []
        records = self.search([("request_id.state", "in", ["wait_executing", "executing"]),
                               ('source_rail.location.alias', '=', alias)], order="start_time asc")
        for record in records:
            plans.append(record.get_detail_cmd())
        return plans

    @api.model
    def get_orders(self, location):
        '''
        取得调车工单
        :param location:
        :return:
        '''
        plans = []
        records = self.search([("request_id.state", "in", ["wait_executing", "executing"]),
                               ('source_rail.location.id', '=', location)])
        for record in records:
            tmp_data = record.read(
                ["id", "batch_no", "dispatch_group",
                 "notice_time", "train", "dispatch_date",
                 "start_time", "finish_time", "source_rail",
                 "target_rail", "work_content", 'dispatch_driver', 'dispatch_group'])[0]
            tmp_data["cmds"] = record.get_detail_cmd()
            tmp_data["dispatch_date"] = str(tmp_data["dispatch_date"])
            tmp_data["start_time"] = str(tmp_data["start_time"])
            tmp_data["notice_time"] = str(tmp_data["notice_time"])
            tmp_data["finish_time"] = str(tmp_data["finish_time"])
            tmp_data["dispatch_driver"] = tmp_data["dispatch_driver"]
            tmp_data['dispatch_group'] = tmp_data['dispatch_group']
            plans.append(tmp_data)
        return plans

    @api.model
    def get_state_name(self, state):
        '''
        取得状态名名
        :return:
        '''
        for tmp_state in DISPATCH_STATE:
            if tmp_state[0] == state:
                return tmp_state[1]

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        '''
        重写，检查路由是否连续
        :param vals_list:
        :return:
        '''
        records = super(DispatchNotice, self).create(vals_list)
        for record in records:
            record.check_rails()
        return records

    @api.multi
    def get_detail_cmd(self, refresh_routes=False):
        '''
        取得命令
        :return:
        '''
        self.ensure_one()
        star_time = \
            pendulum.parse(str(self.start_time)).add(hours=8).format(
                'YYYY-MM-DD HH:mm:ss') if self.start_time else ""
        end_time = \
            pendulum.parse(str(self.finish_time)).add(hours=8).format(
                'YYYY-MM-DD HH:mm:ss') if self.finish_time else ""
        publish_time = \
            pendulum.parse(str(self.publish_time)).add(hours=8).format(
                'YYYY-MM-DD HH:mm:ss') if self.publish_time else ""
        data = {
            'id': self.request_id.id,
            # 计划类型 train_dispatch 调车 train_back 收车 train_out 发车
            "type": "train_dispatch",
            # 计划执行时间
            "start_time": star_time,
            # 完成时间
            "end_time": end_time,
            "is_wash": self.is_wash,  # 是否为洗车
            "trainId": self.train.train_no,  # 车号
            "batch_no": self.batch_no,
            "job": self.work_content,  # 作业内容
            "dispatch_driver": self.dispatch_driver.name,
            "operation": "add",  # delete update add // 计划状态
            # 待执行,信号未开放，执行中，已完成
            "state": self.get_state_name(self.request_id.state),
            "start_rail": self.source_rail.no,
            "start_rail_alias": self.source_rail.alias,
            "end_rail": self.target_rail.no,
            "end_rail_alias": self.target_rail.alias,
            "location": self.get_location_spell(),
            "instructs": [],
            'publish_time': publish_time,
            'dispatch_group': self.dispatch_group.name,
            'dispatch_date':  str(self.dispatch_date),
            "start_rail_alia": self.source_rail.alias,
            "end_rail_alia": self.target_rail.alias
        }

        # 组装命令, 一个detail可能有多条路径
        instructs = []
        for index, detail in enumerate(self.dispatch_detail):
            instructs.append(detail.build_instruct(refresh_routes))

        instructs = list(sorted(instructs, key=lambda v: v['sequence']))
        data["instructs"] = instructs

        return data

    @api.model
    def notify_publish_notice_success(self, data, location_alias):
        '''
        发知发布成功
        :return:
        '''
        dispatch_id = data[0]["id"]
        record = self.env["metro_park_dispatch.dispatch_request"].browse(
            dispatch_id)
        record.state = "wait_executing"
        record.notice_id.dispatch_detail[0].driver_state = 'wait_dispatch'

    @api.multi
    def publish_notice(self):
        '''
        发布计划, 此时根据调车详情添加调车命令
        :return:
        '''
        # 关联计车计划
        self.request_id.notice_id = self.id
        self.publish_time = datetime.datetime.now()

        msg_data = []
        for item in self:
            msg_data.append(item.get_detail_cmd())

        self._cr.commit()
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "add_plan",
            "location": self.get_location_spell(),
            "msg_data": msg_data
        }, room="xing_hao_lou", callback_name="notify_publish_notice_success")

    @api.multi
    def view_request_print(self):
        '''
        打印调车通知单
        :return:
        '''
        add_hours = datetime.timedelta(hours=8)

        data = dict()
        data['detail'] = []
        data['dispatch_date'] = self.dispatch_date
        data['start_time'] = (self.start_time + add_hours).strftime(
            '%Y-%m-%d %H:%M:%S')[10:]
        data['finish_time'] = (self.finish_time + add_hours).strftime(
            '%Y-%m-%d %H:%M:%S')[10:]
        data['display_time'] = self.display_time
        data["batch_no"] = self.batch_no
        data["write_date"] = (self.write_date + add_hours).strftime(
            '%Y-%m-%d %H:%M:%S')[10:]
        data["dispatch_group"] = self.dispatch_group.department_code \
            if self.dispatch_group.department_code else ''
        details = self.dispatch_detail
        for detail in details:
            if detail.operation.name == '(加)+':
                operation = '+'
            elif detail.operation.name == '(减)-':
                operation = '-'
            else:
                operation = ''
            data['detail'].append({
                'sequence': abs(detail.sequence) + 1,
                'rail': detail.rail.alias,
                'source_rail': detail.source_rail.alias,
                'operation': operation,
                'train_num': detail.train_num.id if detail.train_num else 0,
                'remark': detail.remark if detail.remark else "无",
                'work_start_time': detail.work_start_time,
                'work_end_time': detail.work_end_time,
            })
        new_data = sorted(
            data['detail'], key=lambda e: e['sequence'], reverse=False)
        data['detail'] = new_data

        return {
            "name": "调车作业通知单",
            "type": "ir.actions.client",
            "tag": "print_dispatch_request",
            'target': 'new',
            'context': {"vue_data": data}
        }

    @property
    def wait_execute_command(self):
        commands = self.dispatch_detail.sorted('sequence')
        for cmd in commands:
            if cmd.state != 'finished':
                return cmd
        return None

    @api.multi
    def change_notice(self):
        '''
        变更计划, 允许改变目的地
        :return:
        '''
        # 检查目的地是否相同, 如果不同的化还要变更目的地
        if len(self.dispatch_detail):
            last_detail = self.dispatch_detail[-1]
            if last_detail.rail.id != self.target_rail.id:
                self.request_id.target_rail = last_detail.rail.id

        # 关联计车计划
        msg_data = []
        for item in self:
            msg_data.append(item.get_detail_cmd(refresh_routes=True))

        self._cr.commit()
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "change_plan",   # 变更计划消息类型
            "location": self.get_location_spell(),
            "msg_data": msg_data
        }, room="xing_hao_lou", callback_name="notify_publish_notice_success")
