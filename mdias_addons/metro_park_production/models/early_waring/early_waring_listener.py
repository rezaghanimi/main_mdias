# -*- coding: utf-8 -*-

import pendulum
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

from odoo import models
from odoo.models import DEFAULT_SERVER_DATETIME_FORMAT


class ListenerMinx(object):
    _name = 'metro_park_production.listener'

    def post_early_waring_info(self, message_type, message_content, message_remark, action):
        template = self.env.ref('metro_park_production.early_waring_message', raise_if_not_found=True)

        content = template.render({
            'message': {
                'type_description': message_type,
                'content': message_content,
                'remark': message_remark,
                'data': pendulum.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
            },
        }, engine='ir.qweb', minimal_qcontext=True, ).decode()
        title = '预警提醒'
        self.env['res.users'].post_bus_message(
            content, callback_name='callback_name', title=title, action=action)

    def listen_update_state(self, record, state, running_id):
        '''
        监听状态更新
        :param record:
        :param state:
        :param running_id:
        :return:
        '''
        if state != 'finished' or not record:
            return record

        train_sequence = record.real_train_no
        table_data = self.env['metro_park_base.time_table_data'].search(
            [('train_no', '=', train_sequence), ('time_table_id', '=', running_id)],
            limit=1)
        time_distance = (pendulum.parse(str(table_data.plan_in_time))
                         - pendulum.now()).total_minutes()
        retard_second = self.env['res.config.settings'].get_values().get('retard_second', 60)
        ahead_second = self.env['res.config.settings'].get_values().get('ahead_second', 60)
        message_type = '发车误点预警'
        message_content = "%s   计划发车车次：%s次 %s" % (
            record.train_id.train_name, train_sequence, record.real_out_time)
        if -ahead_second >= time_distance or time_distance >= retard_second:
            message_remark = '%s: %s'
            minute = abs(time_distance / 60)
            if time_distance < 0:
                message_remark = message_remark % ('延误', minute)
            else:
                message_remark = message_remark % ('提前', minute)
        else:
            return record

        action = {
            'name': '查看用户',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'res_model': 'res.users',
            'target': 'new',
            'views': [(self.env.ref('base.change_password_wizard_view').id, 'form')],
            'class_names': 'btn-sm btn-link',
        }
        self.post_early_waring_info(message_type, message_content, message_remark, action)


class TrainOutExtend(models.Model, ListenerMinx):
    """
        发车监听,如果满足预警条件就进行预警
    """
    _inherit = 'metro_park_dispatch.train_out_plan'

    # def update_state(self, plan_id, state):
    #     week_count = datetime.now().isoweekday()
    #     running_id = self.env['metro_park_dispatch.nor_time_table_config'].search(
    #         [('day_type', '=', week_count)]).time_table.id
    #     try:
    #
    #         record = super(self, TrainOutExtend).update_state(plan_id, state)
    #         self.listen_update_state(record, state, running_id)
    #
    #     except Exception as e:
    #         _logger.info("发车监听出错" + e)


class TrainBackPlanExtend(models.Model, ListenerMinx):
    """
        收车监听,如果满足预警条件就进行预警
    """
    _inherit = 'metro_park_dispatch.train_back_plan'

    # def update_state(self, plan_id, state):
    #     '''
    #     更新状态
    #     :param plan_id:
    #     :param state:
    #     :return:
    #     '''
    #     week_count = datetime.now().isoweekday()
    #     running_id = self.env['metro_park_dispatch.nor_time_table_config'].search(
    #         [('day_type', '=', week_count)]).time_table.id
    #     try:
    #         record = super(self, TrainBackPlanExtend).update_state(plan_id, state)
    #         self.listen_update_state(record, state, running_id)
    #     except Exception as e:
    #         _logger.info("发车监听出错" + e)
