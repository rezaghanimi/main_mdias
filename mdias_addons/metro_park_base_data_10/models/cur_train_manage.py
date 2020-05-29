# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, exceptions

_logger = logging.getLogger(__name__)

CUR_TRAIN_STATUS = [('fault', '故障'),
                    ('repair', '检修'),
                    ('detain', '扣车'),
                    ('wait', '待命')]


class CurTrainManage(models.Model):
    '''
    现车列表, 这里并没有车的轨迹跟踪
    '''

    _inherit = 'metro_park_dispatch.cur_train_manage'

    @api.multi
    def mock_train_arrive(self):
        '''
        模拟车辆到达
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.Warning('当前用户没有配置所属场段')

        if location.alias == 'gaodalu':
            rail_no = 'T2617G'
        elif location.alias == 'banqiao':
            rail_no = 'T1714G'

        self.trigger_up_event("funenc_socketio_server_msg", data={
            "msg_type": "notice_no_plan",
            "location": location.alias,
            "msg_data": {
                'train_id': self.id,
                'rail_no':  rail_no
            }
        })

    # @api.depends("cur_rail", "cur_switch")
    # def compute_cur_location(self):
    #     '''
    #     计算现车位置
    #     :return:
    #     '''
    #     main_line_location = self.env.ref("metro_park_base_data_10.main_line_location").id
    #     main_line_rail = self.env.ref("metro_park_base_data_10.main_line_sec").id
    #
    #     for record in self:
    #         if record.cur_rail:
    #             record.cur_location = record.cur_rail.location.id
    #             record.park_uid = record.cur_rail.no
    #         if record.cur_switch:
    #             record.cur_location = record.cur_switch.location.id
    #             record.park_uid = record.cur_switch.name
    #         if not record.cur_rail and not record.cur_switch:
    #             record.cur_location = main_line_location
    #             record.park_uid = main_line_rail
