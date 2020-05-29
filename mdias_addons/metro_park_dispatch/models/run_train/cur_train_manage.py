# -*- coding: utf-8 -*-

import logging

import pendulum
from odoo import models, fields, api, exceptions
from odoo.addons.odoo_operation_log.model_extend import LogManage
from odoo.tools import config

LogManage.register_type('synchronous_vehicles', '同步车辆')
LogManage.register_type('manual_sync', '手动同步')
LogManage.register_type('cur_train_position_change', '车辆位置跟踪')

_logger = logging.getLogger(__name__)

CUR_TRAIN_STATUS = [('fault', '故障'),
                    ('repair', '检修'),
                    ('detain', '扣车'),
                    ('wait', '待命')]


class CurTrainManage(models.Model):
    '''
    现车列表, 这里并没有车的轨迹跟踪
    '''

    _name = 'metro_park_dispatch.cur_train_manage'
    _rec_name = 'train_name'
    _description = '现车管理'
    _track_log = True

    train = fields.Many2one(string='车辆',
                            comodel_name='metro_park_maintenance.train_dev')
    train_no = fields.Char(string='现车', related='train.dev_no')
    train_name = fields.Char(string="车号", related='train.dev_name')
    train_type = fields.Many2one(string='车辆类型', related='train.dev_type')
    owner_location = fields.Many2one(string='车辆归属场段', related='train.location')
    location = fields.Many2one(string='当天回库场段',
                               comodel_name='metro_park_base.location',
                               compute="_compute_goback_location")
    # 根据轨道就可以知道位置
    cur_rail = fields.Many2one(
        string="当前轨道",
        comodel_name="metro_park_base.rails_sec")

    cur_switch = fields.Many2one(
        string="当前道岔",
        comodel_name="metro_park_base.switches")

    park_uid = fields.Char(
        string="场段唯一表示",
        compute='compute_cur_location',
        help="用于站场定位")

    ats_position = fields.Char(string="ats位置",
                               help="ats推断的位置, 用于当联锁推断不出来的时候")

    prev_train = fields.Many2one(comodel_name='metro_park_dispatch',
                                 string="前一辆车",
                                 help="用于一条轨道上面停了多组车的情况")

    carriage_index = fields.Integer(string="序号", help="用于工程车拖动的情况", default=0)
    drag_train_no = fields.Char(string='牵引列车', help="牵引列车编号", default="")
    is_drag_train = fields.Boolean(
        string="是否牵引车", compute="_compute_is_drag_train")
    group_index = fields.Integer(string="分组编号", default=0)

    cur_location = fields.Many2one(string='当前车辆位置',
                                   comodel_name='metro_park_base.location',
                                   compute="compute_cur_location")

    detain = fields.Boolean(string="是否扣车", default=False,
                            compute="_compute_detain", store=True)
    train_status = fields.Selection(string='状态',
                                    selection=CUR_TRAIN_STATUS,
                                    default="wait")
    display_status = fields.Char(string="显示状态", help='由于扣车和检修等需要计算显示')
    operation_btn = fields.Char(string="操作按扭", help="操作界面的按扭")

    _sql_constraints = [('train_unique', 'UNIQUE(train)', "设备不能重复")]

    @api.model
    def get_status_name(self, status):
        '''
        取得状态名称
        :return:
        '''
        for item in CUR_TRAIN_STATUS:
            if status == item[0]:
                return item[1]
        return None

    @api.model
    def reset_position(self):
        '''
        重置位置
        :return:
        '''
        records = self.search([])
        records.write({
            "cur_rail": False,
            "cur_switch": False
        })

    @api.depends('carriage_index')
    def _compute_is_drag_train(self):
        '''
        计算是否为牵引车
        :return:
        '''
        for record in self:
            if record.carriage_index == 0:
                record.is_drag_train = False
            else:
                record.is_drag_train = False

    @api.depends("cur_rail", "cur_switch")
    def compute_cur_location(self):
        '''
        计算现车位置
        :return:
        '''
        for record in self:
            if record.cur_rail:
                record.cur_location = record.cur_rail.location.id
                record.park_uid = record.cur_rail.no
            if record.cur_switch:
                record.cur_location = record.cur_switch.location.id
                record.park_uid = record.cur_switch.name
            if not record.cur_rail and not record.cur_switch:
                record.cur_location = False
                record.park_uid = False

    def _compute_detain(self):
        '''
        计算当前是否在扣车状态
        :return:
        '''
        now_date = pendulum.today()
        detain_infos = self.env['metro_park_dispatch.detain_his_info'].search(
            [('start_date', "<=", now_date.format('YYYY-MM-DD')),
             ('end_date', '>=', now_date.format('YYYY-MM-DD')), ('state', '=', 'detaining')])
        detain_trains = detain_infos.mapped("cur_train.id")
        for record in self:
            if record.id in detain_trains:
                record.detain = True
            else:
                record.detain = False

    @api.model
    def get_cur_train_info(self, ids):
        '''
        取得现车信息
        :return:
        '''
        dev_list = []
        train_type_name = self.search([('id', 'in', ids)]).mapped(
            'train_type').mapped('name')
        for name in train_type_name:
            records = self.search_read([('id', 'in', ids), ('train_type.name', '=', name)],
                                       fields=['id', 'train_status', 'train', 'cur_rail', 'detain'])
            res = sorted(records, key=lambda record: record['train_status'])
            for item in res:
                item["train_status"] = self.get_status_name(
                    item['train_status'])
            val = {
                'name': name + ':',
                'train': res
            }
            dev_list.append(val)
        return dev_list

    @api.model
    def get_train_status(self, train_type, status):
        '''
        取得前端显示的车辆状态, 站场图上显示的状态
        :param status:
        :param train_type:
        :return:
        '''
        dev_type_electric_train_id = self.env.ref(
            "metro_park_base.dev_type_electric_train").id
        dev_type_engine_train_id = self.env.ref(
            "metro_park_base.dev_type_engine_train").id
        dev_type_platform_train_id = self.env.ref(
            "metro_park_base.dev_type_platform_train").id

        if train_type == dev_type_electric_train_id:
            if status == 'repair':
                return 'service'
            elif status == 'park_fault' or status == 'main_line_fault' or status == 'detain':
                return 'malfunction'
            elif status == 'wait' or status == 'hot_backup':
                return 'plan'
            else:
                return 'normal'
        elif train_type == dev_type_engine_train_id:
            if status == 'repair':
                return 'service'
            elif status == 'park_fault' or status == 'main_line_fault' or status == 'detain':
                return 'malfunction'
            elif status == 'wait' or status == 'hot_backup':
                return 'plan'
            else:
                return 'normal'
        elif train_type == dev_type_platform_train_id:
            return "normal"

    @api.multi
    def write(self, vals):
        '''
        重写，如果改变了轨道或是改变了switch则通知
        :param vals:
        :return:
        '''
        super(CurTrainManage, self).write(vals)
        self._cr.commit()
        list_pop_form = self.env.context.get('list_pop_form', False)
        if list_pop_form and ('cur_switch' in vals or 'cur_rail' in vals):
            for record in self:
                record.notify_train_position_changed()
        return True

    @api.model
    def get_train_type(self, train_type):
        '''
        取得车辆类型
        :param train_type:
        :return:
        '''
        dev_type_electric_train_id = self.env.ref(
            "metro_park_base.dev_type_electric_train").id
        dev_type_engine_train_id = self.env.ref(
            "metro_park_base.dev_type_engine_train").id
        dev_type_platform_train_id = self.env.ref(
            "metro_park_base.dev_type_platform_train").id

        if train_type == dev_type_electric_train_id:
            return 'normal'
        elif train_type == dev_type_engine_train_id:
            return 'engine'
        elif train_type == dev_type_platform_train_id:
            return 'platform'

    @api.model
    def dispatch_wizard(self, info, target_rail):
        '''
        调车向导
        :return:
        '''
        cur_train = self.browse(info["id"])

        cur_rail_no = info["position"].replace("_", "/")
        cur_trail = self.env["metro_park_base.rails_sec"] \
            .search(['|', ('no', '=', cur_rail_no), ('alias', '=', cur_rail_no)])

        target_rail_no = target_rail.replace("_", "/")
        target_rail = self.env["metro_park_base.rails_sec"] \
            .search(['|', ('no', '=', target_rail_no), ('alias', '=', target_rail_no)])

        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.dispatch_request",
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_train': cur_train.id,
                'default_source_rail': cur_trail.id,
                'default_target_rail': target_rail.id,
            },
            "views": [[self.env.ref('metro_park_dispatch.dispatch_request_form').id, "form"]]
        }

    @api.multi
    def detain_train(self):
        '''
        扣车, 扣车了之后就没法用作运营车了
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.detain_wizard",
            'view_mode': 'form',
            "target": 'new',
            'context': {
                'default_cur_train': self.id,
            },
            "views": [[self.env.ref('metro_park_dispatch.detain_wizard_form').id, "form"]]
        }

    @api.multi
    def report_train_fault(self):
        '''
        车辆故报，说明，做的向导是用的设备
        :return:
        '''
        form_id = self.env.ref(
            'metro_park_dispatch.dev_fault_report_form').id

        tmp_cur_rail = None
        main_line_rail_id = self.env.ref('metro_park_base.main_line_rail').id
        if not self.cur_rail or not self.cur_switch:
            tmp_cur_rail = main_line_rail_id
        elif self.cur_rail:
            tmp_cur_rail = self.cur_rail.id
        elif self.cur_switch:
            tmp_cur_rail = self.cur_switch.rail_sec_id.id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_dispatch.dev_fault_report",
            "name": "车辆故报",
            "target": "new",
            "context": {
                "default_cur_train": self.id,
                "default_cur_rail": tmp_cur_rail
            },
            "views": [[form_id, "form"]]
        }

    @api.multi
    def un_detain_train(self):
        '''
        解除扣车, 还原原有的状态
        :return:
        '''
        records = self.env["metro_park_dispatch.detain_his_info"].search(
            [('cur_train', '=', self.id)])
        if records:
            records.write({
                "state": "finished",
                'un_detain_date': pendulum.today("UTC").format('YYYY-MM-DD')
            })

    @api.model
    def init_cur_train(self):
        '''
        初始化现车, 这里应当是调用ats的现车信息
        :return:
        '''
        trains = self.env['metro_park_maintenance.train_dev'].search([])
        train_cache = {train.id: train for train in trains}
        train_ids = trains.ids
        records = self.search([])
        # 当前车辆的id
        cur_train_ids = records.mapped("train.id")
        vals = []
        for tmp_id in train_ids:
            if tmp_id not in cur_train_ids:
                val = {
                    'train': tmp_id,
                    'train_status': 'wait',
                    'cur_location': train_cache[tmp_id].location.id,
                    'old_status': 'wait',
                }
                vals.append(val)
        self.create(vals)
        LogManage.put_log(content='同步车辆', mode='synchronous_vehicles')

    @api.model
    def sync_manual(self):
        '''
        手动同步, 与ats进行同步
        {
            cmd: "get_time_table",
            data: {
                "date": '2019-08-13'
            }
        },
        {
            cmd: "get_cur_train_info",
            data: {
                "location": 99, # 99 高大路， 98板桥
            }
        }
        :return:
        '''
        today_obj = pendulum.today("UTC").add(hours=8)
        today_str = today_obj.format("YYYY-MM-DD")
        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        self.env["metro_park_dispatch.msg_client"] \
            .get_time_tables([{
                "location": ban_qiao,
                "date": today_str
            }, {
                "location": gao_da_lu,
                "date": today_str
            }])

        LogManage.put_log(content='手动同步', mode='manual_sync')
        raise exceptions.Warning("命令已发送，请等待ats回传信息")

    @api.multi
    def set_cur_rail(self):
        '''
        设置当前车辆的具体位置
        :return:
        '''
        form_id = self.env.ref(
            'metro_park_dispatch.set_cur_location_wizard_form').id
        location = self.owner_location.id
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "metro_park_dispatch.set_cur_location_wizard",
            "name": "当前位置",
            "target": 'new',
            "context": {
                'default_location': location
            },
            "views": [[form_id, "form"]]
        }

    @api.model
    def simulation_location(self):
        '''
        模拟现车位置, 只安排电客车，其它车辆先手动
        :return:
        '''
        return

        if not config.options.get('local_debug', False):
            return

        # 只能在所有位置都没有设置的情况下使用
        trains = self.search(
            [('cur_rail', '!=', False), ('cur_switch', '!=', False)])
        if len(trains) > 0:
            raise exceptions.Warning('当前已经有车辆设置位置!')

        # 只设置电动车
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train').id
        trains = self.search(
            [('train.dev_type', '=', dev_type_electric_train)])

        rail_type_ids = [
            self.env.ref("metro_park_base.rail_type_stop_and_check").id,
        ]

        # 先设置板桥
        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        # 取得所有的停车列检线, 然后将车放到停车列检线上面去
        rails = self.env["metro_park_base.rails_sec"] \
            .search([("rail_type.id", "in", rail_type_ids), ('location', '=', ban_qiao)])
        rail_cache = [rail.id for rail in rails]

        # 板桥23个车,
        for record in trains[:23]:
            if len(rail_cache) > 0:
                record.cur_rail = rail_cache.pop(0)

        # 高大路22个
        rails = self.env["metro_park_base.rails_sec"] \
            .search([("rail_type.id", "in", rail_type_ids), ('location', '=', gao_da_lu)])
        rail_cache = [rail.id for rail in rails]
        for record in trains[23:]:
            if len(rail_cache) > 0:
                record.cur_rail = rail_cache.pop(0)

    @api.depends("train")
    def _compute_goback_location(self):
        '''
        计算当天回库场段
        :return:
        '''
        pass

    @api.model
    def get_user_location(self):
        '''
        取得用户所在位置
        :return:
        '''
        if not self.env.user.cur_location:
            raise exceptions.Warning("当前用户没有配置位置")

        record = self.env.user.cur_location.read()[0]

        return record['alias']

    @api.model
    def get_cur_train_map_info(self, location_alia=None):
        '''
        取得当前的现车数据，用于站场展示
        [{
                type: 2, //类型,
                name: '1233', //名称
                position: '50', //位置’
                status: 1, //状态
            },
            {
                type: 1, //类型,
                name: '1231', //名称
                position: '11ag', //位置’
                status: 1, //状态
            },
        ]

        type ：
            1 电客车   normal
            2 工程车   engine
            2 平板车   platform
        电客车 status ：
            1  检修车 service
            2  正常车 normal
            3  计划车 plan
            4  故障车 malfunction
        平板车 status ：
            1  计划车 plan
            2  故障车 malfunction ：红色 , 检修车：红色+修程代号（大概5位字母）
            3  正常车 normal
        '''

        if not location_alia:
            if not self.env.user.cur_location:
                raise exceptions.Warning("当前用户没有配置当前位置信息")
            location_id = self.env.user.cur_location.id
        else:
            location = self.env['metro_park_base.location'].search(
                [('alias', '=', location_alia)])
            if not location:
                return []
            else:
                location_id = location.id

        # 取得当前位置的车辆信息
        records = self.search([])
        records = records.filtered(
            lambda tmp: tmp.cur_location.id == location_id)

        rst = []
        for record in records:
            if record.cur_rail or record.cur_switch:
                rst.append(record.make_position_info())

        return rst

    def make_position_info(self):
        '''
        生成位置信息
        :return:
        '''

        position = None
        switch = None
        # 当前在轨道上
        if self.cur_rail:
            position = self.cur_rail.no.replace("/", "_")

        # 当前在道岔上, 转换成为区段名称
        if self.cur_switch:
            # 转换成为轨道区段
            position = self.cur_switch.rail_sec_id.no.replace("/", "_")
            switch = self.cur_switch.name

        park_uid = self.park_uid.replace('/', '_') if self.park_uid else False
        return {
            "id": self.id,
            "type": self.get_train_type(self.train_type.id),
            "status": self.get_train_status(self.train_type.id, self.train_status),
            "name": self.train_name,
            "train_no": self.train_no,
            "position": position,
            "switch": switch,
            "carriage_index": self.carriage_index,
            "park_uid": park_uid,
            "uid":  park_uid,
            'delete': 0 if position else 1,
            "drag_train_no": self.drag_train_no,
            "group_index": self.group_index if self.group_index else 0
        }

    def make_position_info_v2(self):
        '''
        生成位置信息，新版使用的是道岔
        :return:
        '''

        position = None
        switch = None
        # 当前在轨道上
        if self.cur_rail:
            position = self.cur_rail.no.replace("/", "_")

        # 当前在道岔上, 转换成为区段名称
        if self.cur_switch:
            position = self.cur_switch.name.replace("/", "_")
            switch = self.cur_switch.name

        park_uid = self.park_uid.replace('/', '_')
        return {
            "id": self.id,
            "type": self.get_train_type(self.train_type.id),
            "status": self.get_train_status(self.train_type.id, self.train_status),
            "name": self.train_name,
            "train_no": self.train_no,
            "position": position,
            "switch": switch,
            "carriage_index": self.carriage_index,
            "park_uid": park_uid,
            "uid":  park_uid,
            'delete': 0 if position else 1,
            "drag_train_no": self.drag_train_no,
            "group_index": self.group_index if self.group_index else 0
        }

    @api.model
    def view_dispatch_plans(self):
        '''
        查看调车计划
        :return:
        '''
        tree_id = self.env.ref(
            'metro_park_dispatch.dispatch_request_list').id
        form_id = self.env.ref(
            'metro_park_dispatch.dispatch_request_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_dispatch.dispatch_request",
            "name": "调车计划",
            "target": "new",
            "views": [[tree_id, "tree"], [form_id, "form"]]
        }

    @api.model
    def jump_to_monitor_action(self):
        '''
        跳转到监控页面
        :return:
        '''
        cur_location = self.env.user.cur_location
        if not cur_location:
            raise exceptions.Warning('当前用户没有配置场段')

        url = '/metro_park_dispatch/static/graph_viewer/cur_train_manage.html?location=' + \
            cur_location.alias
        if cur_location.alias == 'yuanhua':
            url = '/metro_park_dispatch/static/park_map/parkmap/cur_train_monitor.html?mapname=' + \
                cur_location.alias
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    @api.model
    def jump_to_map_operate_action(self):
        '''
        查看日读划请情
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "tag": "cur_train_map_operate"
        }

    @api.multi
    def mock_train_arrive(self):
        '''
        模拟车辆到达
        :return:
        '''
        raise exceptions.Warning('没有实现mock_train_arrive函数, 请在后端实现!')

    @api.multi
    def notify_train_position_changed(self, rail_location=None):
        '''
        模拟车辆到达
        :return:
        '''
        self.ensure_one()

        if self.cur_switch or self.cur_rail:
            alias = self.cur_location.alias
            state = self.make_position_info()
            self.trigger_up_event('funenc_socketio_server_msg', data={
                "msg_type": "update_train_position",
                "location_alias": alias,
                "msg_data": [state]
            })
            LogManage.put_log(content='通知车{name}到达位置{position}'.format(
                name=state["name"],
                position=state["position"]),
                mode='cur_train_position_change')
        else:
            try:
                # 可能是后台来的，没法区分用户
                alias = self.env.user.cur_location.alias or rail_location
                state = self.make_position_info()
                self.trigger_up_event('funenc_socketio_server_msg', data={
                    "msg_type": "update_train_position",
                    "location_alias": alias,
                    "msg_data": [state]
                })
                LogManage.put_log(content='通知移除{name}位置'.format(
                    name=state["name"]),
                    mode='cur_train_position_change')
            except Exception as error:
                _logger.info(
                    "update position error!{error}".format(error=error))

    def create_run_train(self, dev_no, location_id):
        '''
        创建可运行车辆， 车辆可能没有在现车中
        :param dev_no:
        :param location_id:
        :return:
        '''
        location = self.env["metro_park_base.location"].browse(location_id)
        train_record = self.env["metro_park_maintenance.train_dev"].create({
            "dev_name": 'system_train_' + dev_no,
            "dev_no": dev_no,
            "location": location_id,
            "line": location.line.id,
            "line_seg": location.line.line_segment.id
        })

        record = self.create([{
            "train": train_record.id,
        }])
        return record

    @api.multi
    def mock_train_position(self):
        '''
        模拟现车位置
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.ats_position_wizard",
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "default_train_id": self.train.id
            },
            "views": [[False, "form"]]
        }

    @api.multi
    def view_detain_history(self):
        '''
        查看扣车历史
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.detain_his_info",
            'view_mode': 'form',
            'context': {},
            "target": 'new',
            "domain": {
                "cur_train": [('id', '=', self.id)]
            },
            "views": [[self.env.ref('metro_park_dispatch.detain_his_info_list').id, "tree"]]
        }

    @api.multi
    def view_report_history(self):
        '''
        查看车辆故报历史
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.detain_his_info",
            'view_mode': 'form',
            'context': {
                'temp_plan_type': self.temp_plan_type,
                'temp_date': self.temp_date,
                'default_p_work_date': self.temp_date,
                'temp_reason': self.temp_reason,
                'plan_type': 'temp',
            },
            "views": [[self.env.ref('metro_park_dispatch.detain_his_info_list').id, "tree"]]
        }

    def update_position(self, location, dev_no, rail_no):
        '''
        更新现车位置
        :param location:
        :param dev_no:
        :param rail_no:
        :return:
        '''
        run_train = self.search([("train.dev_no", "=", dev_no)])
        if not run_train:
            # 没有就创建车辆
            run_train = self.create_run_train(dev_no, run_train)

        # 为了防止车号被行调删除(出现过被正线行调强行删除的情况，真是坑)，直接返回，使用联锁进行判断
        if not rail_no:
            return run_train.id

        rail = self.env["metro_park_base.rails_sec"]\
            .search([('no', '=', rail_no), ('location', '=', location)])
        if rail:
            # 由于ATS B股可能会出错，所以这里避开
            if rail.port and rail.port == "B":
                return run_train.id

            rail_type_back_sec_id = self.env.ref(
                "metro_park_base.rail_type_back_sec").id
            rail_type_out_sec_id = self.env.ref(
                "metro_park_base.rail_type_out_sec").id

            LogManage.put_log(content='车{name}到达出{position}, ATS记录，不改变位置'.format(
                name=run_train["train_no"],
                position=rail["no"]),
                mode='cur_train_position_change')

            # 到达迁出线时删除车号
            if rail.rail_type.id == rail_type_back_sec_id \
                    or rail.rail_type.id == rail_type_out_sec_id:

                # 两个都给清除掉
                run_train.cur_switch = False
                run_train.cur_rail = False

                # 提前提交，防止别的线程访问不到数据, 这里是因为socketio的这个机制是要等侍回调返回,
                # 而别的地方使用的是另外的cursor，所以会访问不到数据
                self._cr.commit()
                run_train.notify_train_position_changed(rail.location.alias)

                # 通知前端位置发生变化, 清除了无法知道位置
                LogManage.put_log(content='车{name}到达{position}, 清除位置, ATS'.format(
                    name=run_train["train_no"],
                    position=rail["no"]),
                    mode='cur_train_position_change')
            else:
                # 只有在转换轨道的时候才更新位置
                rail_type_exchange_id = \
                    self.env.ref("metro_park_base.rail_type_exchange").id
                if rail.rail_type.id == rail_type_exchange_id:
                    # 有可能联锁占压判断以后，它发又车还原回去了，所以只能车原来在转换轨道的时候发送
                    # 出去的时候无所谓,出去全部由mdias判断, 转换轨不设置车位置，所以车辆的当状轨道
                    # 和道岔只能为空
                    if not (run_train.cur_rail and run_train.cur_switch):
                        run_train.cur_rail = rail.id
                        run_train.cur_switch = False
                        # 到达转换轨
                        LogManage.put_log(content='车{name}到达{position}, 到达转换轨-ATS'.format(
                            name=run_train["train_no"],
                            position=rail["no"]),
                            mode='cur_train_position_change')
                        # 提前提交，防止别的线程访问不到数据
                        self._cr.commit()
                        # 通知前端位置发生变化
                        run_train.notify_train_position_changed()
                    else:
                        LogManage.put_log(content='车{name}到达{position}, 但原车已经在在场内-ATS'.format(
                            name=run_train["train_no"],
                            position=rail["no"]),
                            mode='cur_train_position_change')
                else:
                    # 记录, 用于联锁推断不出来的时候使用ats来更正
                    run_train.ats_position = rail_no

        return run_train.id

    @api.model
    def get_train_locations(self):
        '''
        取得现车位置
        :return:
        '''
        records = self.search([])
        rst = dict()
        for record in records:
            rst[record.train.id] = record.cur_location.id

        return rst

    @api.model
    def get_cur_trains(self):
        '''
        取得当前所有的现车
        :return:
        '''
        rst = []
        cur_trains = self.search([])
        for cur_train in cur_trains:
            if cur_train.train_type.name == '电客车':
                train_type = 'electric_train'
            elif cur_train.train_type.name == '工程车':
                train_type = 'engine_train'
            else:
                train_type = 'platform_train'

            rst.append({
                "id": cur_train.id,
                "train_no": cur_train.train_no,
                "train_name": cur_train.train_name,
                "train_type": train_type,
                "cur_rail": cur_train.cur_rail.no,
                "cur_switch": cur_train.cur_switch.name
            })

        return rst

    @api.model
    def get_cur_train_action(self):
        '''
        检查现车是否已经同步过来
        :return:
        '''
        self.init_cur_train()

        tree_id = self.env.ref(
            'metro_park_dispatch.cur_train_manage_list').id
        form_id = self.env.ref(
            'metro_park_dispatch.cur_train_manage_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_dispatch.cur_train_manage",
            "name": "现车管理",
            "views": [[tree_id, "tree"], [form_id, "form"]]
        }

    @api.model
    def get_cur_train_info_v2(self, location_alias=None):
        '''
        取得现车信息v2, 支持多车顺序
        :param location_alias:
        :return:
        '''
        if not location_alias:
            if not self.env.user.cur_location:
                raise exceptions.Warning("当前用户没有配置当前位置信息")
            location_id = self.env.user.cur_location.id
        else:
            location = self.env['metro_park_base.location'].search(
                [('alias', '=', location_alias)])
            if not location:
                return []
            else:
                location_id = location.id

        # 取得当前位置的车辆信息, 由于是计算字段，不能直接搜索
        records = self.search([], order="group_index asc, carriage_index asc")
        records = records.filtered(
            lambda tmp: tmp.cur_location.id == location_id)

        # 按照位置进行分组
        rst = {}
        for record in records:
            rst.setdefault(record.park_uid, []).append(
                record.make_position_info())

        for key in rst:
            infos = rst[key]
            groups = {}
            for info in infos:
                if not info["drag_train_no"]:
                    groups.setdefault(info["train_no"], []).append(info)
                    info['drag_train_no'] = info['train_no']
                else:
                    groups.setdefault(info["drag_train_no"], []).append(info)
            rst[key] = groups

        return rst

    @api.model
    def update_train_info(self, infos, location_alias):
        '''
        更新列车位置
        :return:
        '''
        location = self.env['metro_park_base.location'].search(
            [('alias', '=', location_alias)])
        if not location:
            return []
        else:
            location_id = location.id

        drag_trains = []
        for info in infos:
            train_no = info["train_no"]
            uid = info["uid"]
            uid = uid.replace('_', '/')
            drag_train_no = info["drag_train_no"]
            carriage_index = info["carriage_index"]
            group_index = info.get('group_index', 0)

            record = self.search([('train.dev_no', '=', train_no)])
            if record:
                rail = self.env['metro_park_base.rails_sec'].search(
                    [('no', '=', uid)])
                if rail:
                    record.write({
                        "cur_rail": rail.id,
                        "cur_switch": None,
                        "drag_train_no": drag_train_no,
                        "carriage_index": carriage_index,
                        "group_index": group_index
                    })
                    drag_trains.append(drag_train_no)
                else:
                    switch = self.env['metro_park_base.switches'].search(
                        [('name', '=', uid)])
                    if switch:
                        record.write({
                            "cur_switch": switch.id,
                            "cur_rail": None,
                            "drag_train_no": drag_train_no,
                            "carriage_index": carriage_index,
                            "group_index": group_index
                        })
                        drag_trains.append(drag_train_no)

        if len(drag_trains) > 0:
            # 取得当前位置的车辆信息, 由于是计算字段，不能直接搜索
            records = self.search([('drag_train_no', 'in', drag_trains)],
                                  order="carriage_index asc")
            records = records.filtered(
                lambda tmp: tmp.cur_location.id == location_id)

            # 按照位置进行分组
            rst = dict()
            for record in records:
                uid = str(record.park_uid)
                rst.setdefault(uid.replace('/', '_'), []).append(
                    record.make_position_info())

            for key in rst:
                infos = rst[key]
                groups = {}
                for info in infos:
                    if not info["drag_train_no"]:
                        groups.setdefault(info["train_no"], []).append(info)
                        info['drag_train_no'] = info
                    else:
                        groups.setdefault(
                            info["drag_train_no"], []).append(info)
                rst[key] = groups

            # v2 版本
            self.trigger_up_event('funenc_socketio_server_msg', data={
                "msg_type": "update_train_group_position",
                "location_alias": location_alias,
                "msg_data": rst
            })

    @api.model
    def remove_train_position(self, train_no):
        '''
        移除车辆位置
        :param train_no:
        :return:
        '''
        record = self.search([('train.dev_no', '=', train_no)], limit=1)
        if record:
            drag_train_no = record.drag_train_no
            group_index = record.group_index
            carriage_index = record.carriage_index
            # 更新carraige index
            group_trains = self.search([('drag_train_no', '=', drag_train_no),
                                        ('group_index', '=', group_index),
                                        ('carriage_index', '>', carriage_index)])
            for tmp_train in group_trains:
                tmp_train.carriage_index = tmp_train.carriage_index - 1
            record.write({
                'cur_rail': False,
                'cur_switch': False
            })
        return 'success'

    @api.model
    def update_train_position(self, infos):
        '''
        更新现车位置
        :return:
        '''
        for info in infos:
            train_no = info.get('train_no', False)
            carrige_index = info.get('carrige_index', False)
            uid = info.get('uid', False)
            if not train_no or not uid:
                continue

            cur_train = self.search([('train.dev_no', '=', train_no)])
            if not cur_train:
                continue

            # 通知其它地方位置更改
            rail = self.env["metro_park_base.rails_sec"].search(
                [('no', '=', uid)], limit=1)
            if rail:
                cur_train.write({
                    'cur_rail': rail.id,
                    'carrige_index': carrige_index
                })
                return

            switch = self.env['metro_park_base.switches'].search(
                [('name', '=', uid)], limit=1)
            if switch:
                cur_train.write({
                    'cur_switch': switch.id,
                    'carrige_index': carrige_index
                })
                return
