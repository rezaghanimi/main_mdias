
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging

_logger = logging.getLogger(__name__)

from odoo.addons.odoo_operation_log.model_extend import LogManage
LogManage.register_type('plan_operation_log', "信号楼日志")


class DayRunPlan(models.Model):
    '''
    运行计划, 这里只包括计划运营的内容
    '''
    _name = 'metro_park_dispatch.day_run_plan'
    _description = '运行计划'
    _rec_name = 'train'
    _track_log = True

    # 指定现车
    train = fields.Many2one(
        string='车辆', comodel_name='metro_park_dispatch.cur_train_manage')

    date = fields.Date(string="日期")

    train_back_plan = fields.Many2one(
        string='收车作业',
        comodel_name='metro_park_dispatch.train_back_plan')

    train_out_plan = fields.Many2one(
        string='发车作业',
        comodel_name='metro_park_dispatch.train_out_plan')

    # 发车从转换轨1出
    exchange_rail_time1 = fields.Integer(string='转换轨1时间',
                                         related='train_out_plan.exchange_rail_time',
                                         store=True)

    # 收车从转换轨2进
    exchange_rail_time2 = fields.Integer(string='转换轨2时间',
                                         related='train_back_plan.exchange_rail_time',
                                         store=True)

    real_out_time = fields.Integer(
        string='实际出库时间',
        related='train_out_plan.real_out_time',
        store=True)

    plan_out_time = fields.Integer(
        string='计划出库时间',
        related='train_out_plan.plan_out_time',
        store=True)

    out_plan_rail_sec = fields.Many2one(
        string='计划发车位置',
        related='train_out_plan.plan_out_rail',
        store=True)

    out_real_train_no = fields.Char(
        string='实际发车车次',
        related='train_out_plan.real_train_no',
        store=True)

    out_plan_train_no = fields.Char(
        string='计划发车车次',
        related='train_out_plan.plan_train_no',
        store=True)

    back_plan_train_no = fields.Char(
        string='收计计划车次',
        related='train_back_plan.plan_train_no',
        store=True)

    plan_back_time = fields.Integer(
        string='计划回库时间',
        related='train_back_plan.plan_back_time',
        store=True)

    plan_back_rail = fields.Many2one(
        string='计划接车位置',
        related='train_back_plan.plan_back_rail',
        store=True)

    real_back_rail = fields.Many2one(
        string='实际接车位置',
        related='train_back_plan.real_back_rail',
        store=True)

    repair_plan = fields.Many2one(
        string='检修类型',
        related='train_back_plan.repair_plan',
        store=True)

    # 回库时是否洗车
    wash = fields.Boolean(string='洗车',
                          related='train_back_plan.wash',
                          store=True)

    work_requirement = fields.Text(
        string='段内作业要求',
        related='train_back_plan.work_requirement_txt',
        store=True)

    dispatch = fields.Boolean(string='是否需要调车',
                              related='train_back_plan.dispatch',
                              store=True)

    remark = fields.Text(string='备注')

    @api.model
    def get_plan_preview_plans(self, date_str):
        '''
        取得计划演练的计划
        :return:
        '''
        today = pendulum.today('UTC').add(hours=8)
        today_str = today.format('YYYY-MM-DD')

        rail_type = self.env.ref('metro_park_base.rail_type_stop_and_check')
        rails = self.env['metro_park_base.rails_sec'].search([('rail_type', '=', rail_type.id)])

        # train_out_plans = self.env['metro_park_dispatch.train_out_plan']\
        #     .search([('date', '=', today_str)])
        # train_back_plans = self.env['metro_park_dispatch.train_back_plan']\
        #     .search([('date', '=', today_str)])
        # dispatch_plans = self.env['metro_park_dispatch.dispatch_request']\
        #     .search(['dispatch_date', '=', today_str])

        groups = []
        for rail in rails:
            groups.append({
                'id': rail.id,
                'content': rail.alias if rail.alias else rail.no
            })

        items = []

        return {
            'groups': groups,
            'items': items,
            'start_date': pendulum.now('UTC').add(hours=8).format('YYYY-MM-DD'),
            'end_date': pendulum.now('UTC').add(days=1, hours=8).format('YYYY-MM-DD')
        }

    @api.model
    def publish_plan(self, date):
        '''
        发布计划, 直接通过socketio发送数据, 信号楼收到以后这边才更新状态
        :return:
        '''

        # 收车计划
        datas = []
        records = self.env['metro_park_dispatch.train_back_plan']\
            .search([('state', 'in', ['unpublish', 'preparing']),
                     ('date', '=', date)])
        for record in records:
            if not record.plan_back_rail:
                continue

            try:
                data = record.get_plan_data(publish=True)
                if data:
                    datas.append(data)
            except Exception as e:
                _logger.info(e)

        # 发车计划
        records = self.env['metro_park_dispatch.train_out_plan']\
            .search([('state', 'in', ['unpublish', 'preparing']),
                     ('date', '=', date)])
        for record in records:
            if not record.plan_out_rail:
                continue

            try:
                data = record.get_plan_data(publish=True)
                if data:
                    datas.append(data)
            except Exception as e:
                # raise exceptions.Warning('获取过路信息出错! {error}'.format(error=e))
                _logger.info(e)

        # 只发送给信号楼, 子消息的方式避免客户端挂一堆on, 注意，这里是add_plans, 消息中没有带location
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "add_plan",
            "msg_data": datas
        }, room="xing_hao_lou", callback_name="notify_publish_plan_success")

    @api.model
    def notify_publish_plan_success(self, datas, location_alias):
        '''
        通知发送成功
        :return:
        '''
        train_out_ids = []
        train_back_ids = []

        for data in datas:
            if data["type"] == "train_out":
                train_out_ids.append(data["id"])
            else:
                train_back_ids.append(data["id"])

        if train_out_ids:
            train_out_plans = self.env["metro_park_dispatch.train_out_plan"]\
                .browse(train_out_ids)
            train_out_plans.write({
                "state": "preparing"
            })
        if train_back_ids:
            train_back_plans = self.env["metro_park_dispatch.train_back_plan"]\
                .browse(train_back_ids)
            train_back_plans.write({
                "state": "preparing"
            })

        # 通知场调客户端
        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "plan_status_changed",
            "location_alias": location_alias
        })

    @api.model
    def get_unfinished_plans(self, alias):
        '''
        取得未完成计划, 只取当日, 给信号楼发信息, 暂时没有限制当天
        :return:
        '''
        # 收车计划
        datas = []
        records = self.env['metro_park_dispatch.train_back_plan']\
            .search([('state', 'in', ['preparing', 'executing']),
                     ('plan_back_rail.location.alias', '=', alias)])
        for record in records:
            if not record.plan_back_rail:
                continue

            data = record.get_plan_data()
            if data:
                datas.append(data)

        # 发车计划
        records = self.env['metro_park_dispatch.train_out_plan']\
            .search([('state', 'in', ['preparing', 'executing']),
                     ('plan_out_rail.location.alias', '=', alias)])
        for record in records:
            if not record.plan_out_rail:
                continue

            data = record.get_plan_data()
            if data:
                datas.append(data)

        return datas

    @api.model
    def get_view_ids(self):
        '''
        取得前端页面的资源id
        :param alias:
        :return:
        '''
        return {
            "train_out_plan":
                self.env.ref(
                    "metro_park_dispatch.train_out_plan_monitor_list").id,
            "train_back_plan":
                self.env.ref(
                    "metro_park_dispatch.train_back_plan_monitor_list").id,
            "train_in_out_log":
                self.env.ref(
                    "metro_park_dispatch.train_in_out_log_list").id,
        }

    @api.model
    def gen_test_plan_data(self):
        '''
        生成当日的测试数据
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError('当前用户没有设置场段!')

        self.env["metro_park_dispatch.train_out_plan"].create_test_data()
        self.env["metro_park_dispatch.train_back_plan"].create_test_data()

    @api.model
    def get_cur_location_alias(self):
        '''
        取得地点别名
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.Warning('当前用户没用配置所属地点')
        return location.alias

    @api.model
    def add_plan_operation_log(self, location):
        '''
        添加信号楼日志
        :return:
        '''
        LogManage.put_log(content="消息回调处理异常{error}".format(error=callback_error),
                          mode="socketio_log")


