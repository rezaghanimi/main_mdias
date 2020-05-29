# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import pendulum

from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

DISPATCH_STATE = [('draft', '草稿'),
                  ('wait_accept', '待审核'),
                  ('accepted', '已通过'),
                  ('wait_executing', '待执行'),
                  ('executing', '执行中'),  # 调车已经开始
                  ('rebacked', '已驳回'),
                  ('canceled', '已撤回'),
                  ('finished', '已完成')]
SHUNTING_CLAIM = [
    ('y', '是'),
    ('n', '否')
]


class DispatchRequest(models.Model):
    '''
    调车申请,
    '''
    _name = 'metro_park_dispatch.dispatch_request'
    _description = '调车申请'
    _rec_name = 'base_train_no'
    _track_log = True

    @api.model
    def _get_default_domain(self):
        # 当前位置
        cur_location = self.env.user.cur_location
        if cur_location:
            cur_location_id = cur_location.id
            return [('cur_location.id', '=', cur_location_id)]
        else:
            return []

    @api.multi
    def _get_source_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            # if self.target_rail:
            #     domain.append(('id', '!=', self.target_rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    @api.multi
    def _get_target_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            # if self.source_rail:
            #     domain.append(('id', '!=', self.source_rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    state = fields.Selection(
        string='调车申请', selection=DISPATCH_STATE, default="draft")
    need_renew_notice = fields.Boolean(string="是否需要更新调车钩指令", default=False)
    display_status = fields.Char(
        string="状态", compute='_compute_display_status', help="由于权限不一样，显示状态了不一样")

    train = fields.Many2one(string='车', comodel_name='metro_park_dispatch.cur_train_manage',
                            help="此处为现车", domain=_get_default_domain, required=True)
    dev_type = fields.Many2one('metro_park_base.dev_type', string='车辆类型')
    base_train_no = fields.Char(
        string='车号', related='train.train_no', required=True)
    dispatch_date = fields.Date(string="调车日期", compute="_compute_dispatch_date",
                                store=True, default=fields.Date.context_today)
    start_time = fields.Datetime(
        string='开始时间', required=True, default=lambda self: datetime.now())
    finish_time = fields.Datetime(
        string='结束时间', required=True, default=lambda self: datetime.now())
    display_time = fields.Char(string="显示时间", compute="_compute_display_time")
    dispatch_type = fields.Selection(string='调车类型', selection=[(
        'own', '自身动力'), ('other_train', '工程车')], default="own")
    is_wash = fields.Boolean(string='洗车', default=False)
    source_rail = fields.Many2one(string='起始股道', comodel_name='metro_park_base.rails_sec',
                                  required=True, domain=_get_source_rail_domain)
    target_rail = fields.Many2one(string='目标股道', comodel_name='metro_park_base.rails_sec',
                                  domain=_get_target_rail_domain, required=True)
    work_content = fields.Text(string='作业内容')
    request_time = fields.Datetime(
        string='申请时间', default=lambda self: datetime.now())
    request_user = fields.Many2one(
        string='申请人', comodel_name='funenc.wechat.user')
    requirements = fields.Many2many(comodel_name="metro_park_dispatch.dispatch_requirement",
                                    relation="dispatch_and_requirement_rel",
                                    column1="dispatch_id",
                                    column2="requirement_id",
                                    string="调车作业要求")
    show_iron_shoe_inputs = fields.Boolean(
        string="是否显示铁鞋", default=False, compute="_compute_show_iron_shoe")
    iron_shoe_no = fields.Char(string='铁鞋号')
    iron_shoe_place = fields.Char(string='铁鞋位置')
    btns = fields.Char(string="操作")

    # 调车通知单id, 调车通知单里面包含调车命令
    notice_id = fields.Many2one(
        string="调车通知单", comodel_name="metro_park_dispatch.dispatch_notice")
    operation_log = fields.One2many(string="操作日志", comodel_name="metro_park_dispatch.dispatch_request_operation_log",
                                    inverse_name="request_id")
    remark = fields.Text(string='备注')
    # 增加工程车
    engineering_vehicle_id = fields.Many2one(string='工程车', comodel_name='metro_park_dispatch.cur_train_manage',
                                             help="当调车类型为工程车时，选择具体的工程车辆", domain=_get_default_domain)
    engineering_vehicle_rail = fields.Many2one(string='工程车股道', comodel_name='metro_park_base.rails_sec',
                                               domain=_get_source_rail_domain)
    # 将调车作业字段改为Selection
    isolate_switch = fields.Selection(
        string="停车前隔离开关是否断开", selection=SHUNTING_CLAIM, default='n')
    ground_wire = fields.Selection(
        string="停车股道是否接地线", selection=SHUNTING_CLAIM, default='n')
    is_incursive = fields.Selection(
        string="转入轨道是否入侵", selection=SHUNTING_CLAIM, default='n')
    suspend_system_is_normal = fields.Selection(
        string="悬挂系统是否正常", selection=SHUNTING_CLAIM, default='y')
    prohibit_battery_powe = fields.Selection(
        string="禁止蓄电池通电", selection=SHUNTING_CLAIM, default='n')
    need_iron_shoe = fields.Selection(
        string="是否放置铁鞋子", selection=SHUNTING_CLAIM, default='n')

    @api.onchange('train')
    def set_train_type(self):
        self.dev_type = self.train.train_type

    @api.onchange('engineering_vehicle_id')
    def _onchange_engineering_vehicle_id(self):
        """
        当前选择了工程车后，默认将工程车位置读取出来
        :return:
        """
        for res in self:
            res.engineering_vehicle_rail = res.engineering_vehicle_id.cur_rail.id or False

    @api.onchange("dispatch_type")
    def onchange_route_type(self):
        '''
        更改进路类型, 限制domain
        :return:
        '''

        # 当前位置
        cur_location = self.env.user.cur_location
        if not cur_location:
            raise exceptions.Warning('当前用户没有配置场段')
        cur_location_id = cur_location.id

        # 限制只能在当前所处的车辆段调车
        return {
            "domain": {
                "train": [('cur_location.id', '=', cur_location_id)]
            }
        }

    @api.onchange("train")
    def onchange_route_type(self):
        '''
        更改进路类型, 限制domain
        :return:
        '''
        self.source_rail = self.train.cur_rail

    @api.depends('start_time')
    def _compute_dispatch_date(self):
        '''
        计算调车日期，以开始时间的日期为准
        日期必需要加8小时，不然会有时区问题
        :return:
        '''
        for record in self:
            if record.start_time:
                start_time = pendulum.parse(str(record.start_time))
                # 日期必需要加8小时，不然会有时区问题
                record.dispatch_date = start_time.add(
                    hours=8).format('YYYY-MM-DD')
            else:
                record.dispatch_date = False

    @api.multi
    def write_log(self, content):
        '''
        写入新的日志
        :return:
        '''
        self.operation_log.write((0, 0, {
            content: content
        }))

    @api.model
    def update_state(self, plan_state):
        '''
        更新计划状态
        :return:
        '''
        if plan_state['state'] not in [item[0] for item in DISPATCH_STATE]:
            _logger.error("状态不正确")
        record = self.browse(plan_state['id'])
        if not record:
            _logger.error("计划不存在")
            raise exceptions.ValidationError("计划不存在")
        if record.state != plan_state['state']:
            if plan_state['state'] == 'executing':
                record.start_time = datetime.now()
            elif plan_state['state'] == 'finished':
                record.finish_time = datetime.now()
        record.state = plan_state['state']
        if 'detail_state' in plan_state:
            self.env['metro_park_dispatch.dispatch_detail'].sudo(
            ).update_state(plan_state['detail_state'])

    # @api.one
    # @api.constrains('source_rail', 'target_rail')
    # def _check_description(self):
    #     if self.source_rail.id == self.target_rail.id:
    #         raise exceptions.ValidationError("调车起始股道和目标股道不能相同")

    # @api.one
    # @api.constrains('start_time', 'finish_time')
    # def _check_description(self):
    #     '''
    #     开始时间必需大于结束时间
    #     :return:
    #     '''
    #     if str(self.start_time) > str(self.finish_time):
    #         raise exceptions.ValidationError("开始时间必需小于结束时间")

    @api.multi
    def view_request_detail(self):
        '''
        跳转求详情页面
        :return:
        '''
        view_id = self.env.ref('metro_park_dispatch.dispatch_request_form').id
        res_id = self.id
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.dispatch_request",
            'view_mode': 'form',
            "name": "调车详情",
            "mode": "read_only",
            "target": "new",
            'context': {},
            'res_id': res_id,
            "views": [[view_id, "form"]]
        }

    @api.multi
    def edit_request(self):
        '''
        跳转编辑页面, 这个时候要限定domain才行
        :return:
        '''
        view_id = self.env.ref(
            'metro_park_dispatch.dispatch_request_edit_form').id
        res_id = self.id
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.dispatch_request",
            'view_mode': 'form',
            'context': {'form_view_initial_mode': 'edit'},
            'res_id': res_id,
            "target": "new",
            "views": [[view_id, "form"]]
        }

    @api.multi
    def view_execute_detail(self):
        '''
        跳转到执行情况界面
        :return:
        '''
        view_id = self.env.ref('metro_park_dispatch.view_dispatch_notice_implementation_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.dispatch_notice",
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.notice_id.id,
            'context': {},
            "views": [[view_id, "form"]]
        }

    @api.multi
    def _compute_display_status(self):
        '''
        根据不同的权限进行不同的显示和操作
        只有场调和检调才有相应的权限进行查看
        :return:
        '''
        pass

    @api.model
    def get_dispatch_request_audit_action(self):
        '''
        取得调车计划动作
        只能查看当前处于已经上报状态的
        :return:
        '''
        # 获取当前位置
        local_site = self.env.user.cur_location.id
        group_id = self.env.user.cur_role.id
        groups = self.env['ir.model.data'] \
            .search([('model', '=', 'res.groups'),
                     ('res_id', 'in', [group_id]),
                     ('module', '=', 'metro_park_base')])

        action = self.env.ref(
            'metro_park_dispatch.dispatch_audit_act_window').read()[0]
        action['context'] = {"groups": groups.mapped('name')}
        action['domain'] = [
            ('state', 'in', ['wait_accept', 'accepted',
                             'wait_executing', 'executing']),
            ('source_rail.location', '=', local_site)]
        return action

    @api.model
    def get_dispatch_request_action(self):
        '''
        取得调车计划动作, 只能看到自己填写的, 状态只能看到特定的几个状态
         selection=[('draft', '草稿'),
            ('wait_accept', '待审核'),
            ('accepted', '已通过'),
            ('wait_executing', '待执行'),
            ('executing', '执行中'),
            ('rebacked', '已驳回'),
            ('canceled', '已撤回'),
            ('finished', '结束')],
        :return:
        '''
        local_site = self.env.user.cur_location.id
        group_id = self.env.user.cur_role.id
        groups = self.env['ir.model.data'] \
            .search([('model', '=', 'res.groups'),
                     ('res_id', 'in', [group_id]),
                     ('module', '=', 'metro_park_base')])

        tree_id = self.env.ref(
            'metro_park_dispatch.dispatch_request_list').id
        form_id = self.env.ref(
            'metro_park_dispatch.dispatch_request_form').id

        action = self.env.ref(
            'metro_park_dispatch.request_act_window').read()[0]
        action['views'] = [[tree_id, "tree"], [form_id, "form"]]
        action['context'] = {"groups": groups.mapped('name')}
        action['domain'] = [('source_rail.location', '=', local_site)]

        return action

    @api.multi
    def view_dispatch_detail(self):
        '''
        查看调车执行情况
        :return:
        '''
        form_id = self.env.ref(
            'metro_park_dispatch.excute_detail_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "metro_park_dispatch.dispatch_notice",
            "name": "调车通知单",
            "res_id": self.notice_id.id,
            "target": "new",
            "views": [[form_id, "form"]],
            'flags': {
                'initial_mode': 'edit'
            }
        }

    @api.multi
    def get_change_plan_action(self):
        '''
        查看调车执行情况
        :return:
        '''
        form_id = self.env.ref(
            'metro_park_dispatch.dispatch_notice_change_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "metro_park_dispatch.dispatch_notice",
            "name": "变更计划",
            "res_id": self.notice_id.id,
            "target": "new",
            "views": [[form_id, "form"]],
            'flags': {
                'initial_mode': 'edit'
            }
        }

    @api.one
    def make_dispatch_detail(self):
        '''
        调车详情, 这里建找默认进路
        :return:
        '''
        if not self.notice_id:
            # 创建调车通知单, 基础的命令使用默认值的方式添加
            record = self.env['metro_park_dispatch.dispatch_notice'].create({
                'request_id': self.id,
                'batch_no': self.env['ir.sequence'].next_by_code('dispatch.notice.number')
            })

            self.notice_id = record.id

    @api.model
    def break_routes(self, tmp_route_array):
        rst_routes = []

        rail_type_pull_out_id = self.env.ref(
            'metro_park_base.rail_type_pull_out').id
        for tmp_index, tmp_route in enumerate(tmp_route_array):
            if tmp_route.start_rail.rail_type.id == rail_type_pull_out_id:
                if tmp_index != 0:
                    rst_routes.append({
                        'source_rail': tmp_route_array[0].start_rail.id,
                        'rail': tmp_route_array[tmp_index - 1].end_rail.id,
                        'interlock_routes':
                            [(0, 0, {"index": i, "route_id": tmp_route_array[i].id}) for i in range(
                                tmp_index)]
                    })
                    rst_routes.append({
                        'source_rail': tmp_route_array[tmp_index].start_rail.id,
                        'rail': tmp_route_array[-1].end_rail.id,
                        'interlock_routes':
                            [(0, 0, {"index": i, "route_id": tmp_route_array[i].id})
                             for i in range(tmp_index, len(tmp_route_array))]
                    })

        if not rst_routes:
            rst_routes.append({
                'source_rail': tmp_route_array[0].start_rail.id,
                'rail': tmp_route_array[-1].end_rail.id,
                'interlock_routes': [(0, 0, {
                    "index": tmp_index,
                    "route_id": tmp_route.id
                }) for tmp_index, tmp_route in enumerate(tmp_route_array)]
            })

        return rst_routes

    @api.model
    def search_route(self, location, source_rail, target_rail):
        inter_locker_model = self.env['metro_park.interlock.route']
        cur_location = self.source_rail.location.id

        # 查看是否能直接找到
        routes = inter_locker_model.search_route(
            cur_location, source_rail, target_rail, "dispatch")

        start_route = None
        end_route = None
        if not routes:
            # 找取B到A的路由，更新终起点为A
            if source_rail.port == 'B':
                reverse_rail = source_rail.reverse_port
                route = inter_locker_model \
                    .search_route(location=cur_location,
                                  start_rail=source_rail,
                                  end_rail=reverse_rail,
                                  route_type="dispatch")
                if not route:
                    raise exceptions.Warning("没有找到B-A的路由")
                start_route = route
                source_rail = reverse_rail

            # 找到A到B的路由, 同时更新终点为A
            if target_rail.port == "B":
                reverse_rail = target_rail.reverse_port
                route = inter_locker_model \
                    .search_route(location=cur_location,
                                  start_rail=reverse_rail,
                                  end_rail=target_rail,
                                  route_type="dispatch")
                if not route:
                    raise exceptions.Warning("没有找到B-A路由")
                end_route = route
                target_rail = reverse_rail

                routes = inter_locker_model \
                    .search_dispatch_route(cur_location, source_rail, target_rail)

        if not routes:
            routes = inter_locker_model.search_dispatch_route(
                cur_location, source_rail, target_rail)

        true_routes = []
        for route in routes:
            if start_route:
                route = start_route[0] + route
            if end_route:
                route = route + end_route[0]
            true_routes.append(route)

        return true_routes

    @api.multi
    def open_dispatch_detail_action(self):
        '''
        编制调车通知单
        :return:
        '''
        self.ensure_one()

        form_id = self.env.ref(
            'metro_park_dispatch.dispatch_notice_form').id

        dispatch_detail = []

        if self.need_renew_notice or not self.notice_id:
            rails_sec_model = self.env['metro_park_base.rails_sec']
            cur_location = self.source_rail.location.id
            location_alias = self.source_rail.location.alias

            # 有工程车信息，需先调工程车到开始位置
            if self.dispatch_type == "other_train":
                if not self.engineering_vehicle_id or not self.engineering_vehicle_rail:
                    raise exceptions.Warning("工程车调车信息不完整！")

                to_start_rail_routes = self.search_route(
                    cur_location, self.engineering_vehicle_rail, self.source_rail)

                for route_array in to_start_rail_routes:
                    for index, route in enumerate(self.break_routes(route_array)):
                        dispatch_detail.append((0, 0, dict({
                            'sequence': len(dispatch_detail) + 1,
                            'display_sequence': len(dispatch_detail) + 1,
                        }, **route)))
                    break

            if self.is_wash:
                wash_rail = rails_sec_model.search([
                    ('alias', '=', '洗车线'),
                    ('location', '=', cur_location)
                ])
                if not wash_rail:
                    raise exceptions.Warning("未找到洗车线！")

                to_wash_routes = []
                wash_back_rotues = []

                # 高大路洗车特殊处理，需先找到到洗车牵出线的路径，再到牵2的途中洗车，再回到目的地
                if location_alias == "gaodalu":
                    wash_pull_out_rail = rails_sec_model.search([
                        ('usage', '=', '洗车牵出线'),
                        ('location', '=', cur_location)
                    ])
                    if not wash_pull_out_rail:
                        raise exceptions.Warning("未找到洗车牵出线！")
                    to_wash_routes = self.search_route(
                        cur_location, self.source_rail, wash_pull_out_rail)
                    wash_back_rotues = self.search_route(
                        cur_location, wash_pull_out_rail, self.target_rail)
                    if not to_wash_routes or not wash_back_rotues:
                        raise exceptions.Warning("未找到路径！")
                else:
                    # 起点为洗车线
                    if self.source_rail.id == wash_rail.id:
                        wash_back_rotues = self.search_route(
                            cur_location, wash_rail, self.target_rail)
                    # 终点为洗车线
                    elif self.target_rail == wash_rail:
                        to_wash_routes = self.search_route(
                            cur_location, self.source_rail, wash_rail)
                    # 正常的情况
                    else:
                        to_wash_routes = self.search_route(
                            cur_location, self.source_rail, wash_rail)
                        wash_back_rotues = self.search_route(
                            cur_location, wash_rail, self.target_rail)
                        if not to_wash_routes or not wash_back_rotues:
                            raise exceptions.Warning("未找到路径！")

                for to_wash_route in to_wash_routes:
                    for index, route in enumerate(self.break_routes(to_wash_route)):
                        dispatch_detail.append((0, 0, dict({
                            'sequence': len(dispatch_detail) + 1,
                            'display_sequence': len(dispatch_detail) + 1,
                        }, **route)))
                    break
                for wash_back_rotue in wash_back_rotues:
                    for index, route in enumerate(self.break_routes(wash_back_rotue)):
                        dispatch_detail.append((0, 0, dict({
                            'sequence': len(dispatch_detail) + 1,
                            'display_sequence': len(dispatch_detail) + 1,
                        }, **route)))
                    break
            else:
                true_routes = self.search_route(
                    cur_location, self.source_rail, self.target_rail)
                for route_array in true_routes:
                    for index, route in enumerate(self.break_routes(route_array)):
                        dispatch_detail.append((0, 0, dict({
                            'sequence': len(dispatch_detail) + 1,
                            'display_sequence': len(dispatch_detail) + 1,
                        }, **route)))
                    break
            self.need_renew_notice = False

        if not self.notice_id:
            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "metro_park_dispatch.dispatch_notice",
                "name": "调车通知单",
                "target": "new",
                "views": [[form_id, "form"]],
                "context": {
                    "default_request_id": self.id,
                    "default_dispatch_detail": dispatch_detail,
                    "default_batch_no": self.env['ir.sequence'].next_by_code('dispatch.notice.number'),
                },
                'flags': {
                    'initial_mode': 'edit'
                }
            }
        else:
            if dispatch_detail:
                self.notice_id.write({
                    "dispatch_detail": [(6, 0, [])]
                })
                self.notice_id.write({
                    "dispatch_detail": dispatch_detail
                })
            for item in self.notice_id.dispatch_detail:
                item.state = "wait_accept"
            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "metro_park_dispatch.dispatch_notice",
                "name": "调车通知单",
                "res_id": self.notice_id.id,
                "target": "new",
                "views": [[form_id, "form"]],
                'flags': {
                    'initial_mode': 'edit'
                }
            }

    @api.depends("start_time", "finish_time")
    def _compute_display_time(self):
        '''
        计算显示时间
        :return:
        '''
        for record in self:
            start_time = pendulum.parse(str(record.start_time))
            end_time = pendulum.parse(str(record.finish_time))
            record.display_time = "{start_time}~{end_time}" \
                .format(start_time=start_time.format("HH:mm:ss"),
                        end_time=end_time.format("HH:mm:ss"))

    @api.multi
    def reback_publish(self):
        '''
        发布撤回
        :return:
        '''
        self.state = 'accepted'

    @api.multi
    def submit_request(self):
        '''
        检调提交申请
        :return:
        '''
        self.state = 'wait_accept'

    @api.multi
    def canceled_request(self):
        '''
        检调撤回
        :return:
        '''
        self.state = 'canceled'

    @api.multi
    def accept_request(self):
        '''
        场调同意, 在这里生成最基本的调车计划
        :return:
        '''
        self.state = 'accepted'
        self.need_renew_notice = True

    @api.multi
    def reback_request(self):
        '''
        场调驳回
        :return:
        '''
        self.state = 'rebacked'

    @api.model
    def reback_plan(self, id):
        '''
        退回dispatch
        :return:
        '''
        dispatch = self.browse(id)

        # 只发送给信号楼
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "reback_plan",
            "location": dispatch.notice_id.get_location_spell(),
            "msg_data": [{
                'type': 'train_dispatch',
                "id": id
            }]
        }, room="xing_hao_lou")

        dispatch.state = 'canceled'
        return True

    @api.model
    def import_plan(self):
        '''
        导入计划
        :return:
        '''
        pass

    @api.depends("requirements")
    def _compute_show_iron_shoe(self):
        '''
        计算是否显示铁鞋
        :return:
        '''
        tmp_id = self.env.ref("metro_park_dispatch.requirement_need_iron_shoe")
        for record in self:
            if tmp_id in record.requirements.ids:
                record.show_iron_shoe_inputs = True
            else:
                record.show_iron_shoe_inputs = False

    @api.multi
    def write(self, vals):
        '''
        重写，检查命令是否重复
        :param vals:
        :return:
        '''
        super(DispatchRequest, self).write(vals)

    @api.multi
    def unlink(self):
        '''
        重写删除函数，通知前段删除对应数据
        '''
        records = self.filtered(
            lambda x: x.state == 'draft' or x.state == 'rebacked' or x.state == 'canceled')
        if len(records) != len(self):
            raise exceptions.Warning('只有被草稿或是被退回的计划才能被删除!')
        if records:
            all_datas = []
            for record in records:
                # 此处为单个场调的操作，肯定是属于一个场段的计划，若不是，需在筛选出做处理
                if record.notice_id:
                    location = record.notice_id.get_location_spell()
                    all_datas.append(
                        {'id': record.notice_id.id, 'type': 'train_dispatch', 'location': location})
                super(DispatchRequest, record).unlink()

            for data in all_datas:
                self.trigger_up_event("funenc_socketio_server_msg", data={
                    "msg_type": "delete_plan",
                    "location": data['location'],
                    "msg_data": [data]
                }, room="xing_hao_lou")

    # TODO 需要实现和补全从信号楼检查单据计划等逻辑
    @api.multi
    def document_return_operation(self):
        """
        当点击退回按钮后，需要在信号楼中检查该单据生成的通知和计划并撤销。
        从信号楼检查确认无误后，将单据状态修改为："待审核（wait_accept）"
        :return:
        """
        # --------------
        # 这里待完善 调用信号楼api或接口代码检查该单据已发布的计划
        # --------------
        # 修改状态为待审核
        self.write({'state': 'wait_accept'})
