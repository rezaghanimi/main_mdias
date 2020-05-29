# -*- coding: utf-8 -*-

import logging

from odoo import models, api
from odoo.exceptions import AccessDenied
from odoo.models import SUPERUSER_ID
import datetime

_logger = logging.getLogger(__name__)

# 直接odoo命名空间中去获取
from odoo.addons.odoo_operation_log.model_extend import LogManage
LogManage.register_type('mobile_api_log', "调车终端日志")


class MobileApi(models.AbstractModel):
    '''
    调车终端api
    '''
    _name = 'metro_park_dispatch.mobile_api'

    @api.model
    def get_user_groups(self, user_id):
        '''
        取得当前用户的所有权限
        :return:
        '''
        user = self.env.user.browse(user_id)
        groups_ids = self.env['res.groups'].search([('id', 'in', user.groups_id.ids), ('atomic', '=', True)]).ids
        groups = self.env['ir.model.data'].sudo() \
            .search([('model', '=', 'res.groups'),
                     ('res_id', 'in', groups_ids)
                     ])
        group_data =[]
        for name in groups.read(fields=["id", "name"]):
            group_data.append(name.get('name', False))

        return group_data

    def get_executing_work_info(self, user_id, location=None):
        """
            移动端获取待执行和正在执行计划列表数据接口
        :param user_id:
        :param location:
        :return:
        """
        shunting_of_test_line = []  # 存放试车线调车
        shunting_non_test_line = []  # 存放非试车线调车
        plans = []
        user = self.env.user.browse(user_id)
        groups = self.get_user_groups(user.id)
        domain = [("request_id.state", "in", ["wait_executing", "executing", 'finished']),
                  ('driver_finished', '=', False), ('dispatch_date', '>=', datetime.date.today())]

        type_id = self.env.ref('metro_park_base.dev_type_electric_train').id
        if location:
            domain.append(('source_rail.location.id', '=', location))
        dispatch_plans = self.env['metro_park_dispatch.dispatch_notice'].search(domain, order='id desc')
        # 根据权限要求对结果集进行分组
        for dispatch_plan in dispatch_plans:
            on_off = True
            # 是电客车
            if dispatch_plan.request_id.dev_type.id == type_id:
                on_off = False
            if on_off:
                shunting_non_test_line.append(dispatch_plan)
            else:
                shunting_of_test_line.append(dispatch_plan)
        # 对应权限输出对应的结果集
        if 'group_dispatch_car_shunting_of_test_line' in groups and \
                'group_dispatch_car_dispatch_car_hunting_on_non_test_line' not in groups:
            for plan in shunting_of_test_line:
                plans.append(plan.get_detail_cmd())
        elif 'group_dispatch_car_shunting_of_test_line' not in groups and \
                'group_dispatch_car_dispatch_car_hunting_on_non_test_line' in groups:
            for plan in shunting_non_test_line:
                plans.append(plan.get_detail_cmd())
        elif 'group_dispatch_car_shunting_of_test_line' in groups and \
                'group_dispatch_car_dispatch_car_hunting_on_non_test_line' in groups:
            for plan in dispatch_plans:
                plans.append(plan.get_detail_cmd())

        data = {
            'plans': plans
        }
        return {
            'status': 200,
            'data': data
        }

    def get_history_works(self, user_id, offset, limit=10, location=None):
        """
            获取历史执行调车计划记录
        :param user_id:
        :param offset:
        :param limit:
        :param location:
        :return:
        """

        domain = [("request_id.state", "=", "finished")]
        if location:
            domain.append(('source_rail.location.id', '=', location))
        records = self.env['metro_park_dispatch.dispatch_notice'].search(
            domain, offset=offset, limit=limit)
        plans = []
        for record in records:
            plans.append(record.get_detail_cmd())
        return {
            'status': 200,
            'data': plans
        }

    def login(self, login, password):
        dbname = self.env.cr.dbname
        user = self.env['res.users'].search([('login', '=', login)])
        if not user:
            return {
                'status': 401,
                'data': {
                    'msg': '用户不存在'
                }
            }
        try:
            uid = user._login(dbname, login, password)
            user = self.env['res.users'].browse(uid)
            return {
                'status': 200,
                'data': {
                    'uid': uid,
                    'login': login,
                    'name': user.name,
                    'location_id': user.cur_location.id,
                    'location_name': user.cur_location.name,

                }
            }
        except AccessDenied:
            return {
                'status': 401,
                'data': {
                    'msg': '用户或密码错误'
                }
            }

    def query_works(self, search_value, location=None):
        """
            查询历史调车计划
        :param search_value:
        :param location
        :return:
        """
        domain = [('driver_finished', '=', True), '|', ('dispatch_driver.name', 'ilike', search_value),
                  ('batch_no', 'ilike', search_value)]
        if location:
            domain = [('source_rail.location.id', '=', location)] + domain
        records = self.env['metro_park_dispatch.dispatch_notice']. \
            search(domain)
        data = []
        for record in records:
            if record:
                data.append(record.get_detail_cmd())
        return {
            'status': 200,
            'data': data
        }

    def execute_dispatch_cmd(self, request_id, cmd_type, cmd_id, execute_user_id=None):
        """
        执行调车计划命令
        :param request_id:
        :param cmd_type:
        :param cmd_id:
        :param execute_user_id: 执行计划用户id
        :return: 返回执行状态
        """
        if not execute_user_id:
            execute_user_id = SUPERUSER_ID
        if not cmd_id:
            return
        result = self.env['metro_park_dispatch.dispatch_detail'].sudo(
            execute_user_id).request_start_plan({
            "cmd_type": cmd_type,
            "request_id": request_id,
            "instruct_id": cmd_id
        })
        if result:
            record = self.env['metro_park_dispatch.dispatch_detail'].browse(cmd_id)
            if cmd_type == 'execute_request_dispatch':
                value = {
                    'driver_state': 'wait_signal_open'
                }
            elif cmd_type == 'execute_finished_dispatch' and record.state == 'finished':
                value = {
                    'driver_state': 'finished'
                }

            else:
                return False
            record.write(value)
            # 判断是否有待执行计划，有就将计划解锁
            if cmd_type == 'execute_finished_dispatch' and record.state == 'finished':
                cmd = record.notice_id.wait_execute_command
                if cmd:
                    message = '%s->%s命令等待请求执行' % (cmd.source_rail.no, cmd.rail.no)
                    cmd.write({
                        'driver_state': 'wait_dispatch'
                    })
                    self.notify_to_mobile(message)
                else:
                    record.notice_id.write({
                        'driver_finished': True
                    })
            return True
        return False

    def get_dispatch_plan_by_id(self, plan_id):
        plan = None
        if plan_id:
            plan = self.env['metro_park_dispatch.dispatch_request'].browse(int(plan_id))
            if plan and plan.notice_id:
                plan = plan.notice_id.get_detail_cmd()
            else:
                plan = {}
        return {
            'status': 200,
            'data': plan
        }

    def notify_to_mobile(self, message):
        self.env['funenc.socket_io'].post_message_to_app_server({
            'bus_type': 'notify',
            'data': {
                'message': message
            }
        })

    def replay_cmd_state_to_request(self, cmd_id):
        """
            恢复信号开放至等待调车状态
        :param cmd_id:
        :return:
        """
        logging.info('手持端状态更新，更新勾计划{id}'.format(id=cmd_id))
        cmd = self.env['metro_park_dispatch.dispatch_detail'].browse(cmd_id)
        if cmd and cmd.driver_state == 'wait_signal_open' and cmd.state == 'wait_accept':
            cmd.write({
                'driver_state': 'wait_dispatch'
            })


class DispatchDetailExtend(models.Model):
    _inherit = 'metro_park_dispatch.dispatch_detail'

    @api.model
    def update_state(self, detail_state):
        record = super(DispatchDetailExtend, self).update_state(detail_state)
        if record.state == 'executing':
            record.driver_state = 'executing'
            message = '%s->%s信号已开放' % (record.source_rail.no, record.rail.no)
            self.env['metro_park_dispatch.mobile_api'].notify_to_mobile(message)
        if not record.notice_id:
            return record
        self.env['funenc.socket_io'].post_message_to_app_server({
            'bus_type': 'refresh_pages'
        })
        return record


class DispatchRequestNotice(models.Model):
    _inherit = 'metro_park_dispatch.dispatch_notice'

    def notify_publish_notice_success(self, *args, **kwargs):
        result = super(DispatchRequestNotice, self) \
            .notify_publish_notice_success(*args, **kwargs)
        self.env['funenc.socket_io'].post_message_to_app_server({
            'bus_type': 'refresh_pages'
        })
        return result
