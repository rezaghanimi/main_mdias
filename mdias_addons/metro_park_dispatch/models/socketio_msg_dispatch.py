# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class SocketMsgDispatch(models.Model):
    '''
    封装，便于访问后端
    '''
    _inherit = "funenc.socket_io"
    _description = '消息收发客户端'

    @api.model
    def deal_custom_event(self, sid, data):
        '''
        处理自定义的event, 其它模块调用这个函数进行扩展
        子类调用的时候注意调用父类消息处理函数
        :return:
        '''
        # 先调用父类处理消息
        super(SocketMsgDispatch, self).deal_custom_event()

        # 消息类型
        msg_type = data.get("msg_type", False)
        if not msg_type:
            return

    @api.model
    def get_all_unfinished_plan(self, location_alias):
        '''
        取得所有未完成计划
        :return:
        '''

        # 调车计划
        dispatch_plans = self.env["metro_park_dispatch.dispatch_notice"] \
            .get_unfinished_plans(location_alias)

        # 收发车计划
        day_plan_datas = self.env['metro_park_dispatch.day_run_plan'] \
            .get_unfinished_plans(location_alias)

        return dispatch_plans + day_plan_datas

    @api.model
    def update_plan_state(self, plan_state):
        '''
        通知计划改变状态
        :param plan_state:
        :return:
        '''
        plan_type = plan_state["type"]
        if plan_type == "train_dispatch":
            self.env["metro_park_dispatch.dispatch_request"]\
                .sudo()\
                .update_state(plan_state)
        elif plan_type == "train_back":
            self.env["metro_park_dispatch.train_back_plan"]\
                .sudo()\
                .update_state(plan_state)
        elif plan_type == "train_out":
            self.env["metro_park_dispatch.train_out_plan"]\
                .sudo()\
                .update_state(plan_state)
        else:
            _logger.info("数据错误，指令类型不正确! {plan}".format(plan=plan_state))

    @api.model
    def log_operation_data(self, log_data):
        '''
        记录信号楼数据, 暂时没有保存
        :param log_data:
        :return:
        '''
        _logger.info(log_data)
