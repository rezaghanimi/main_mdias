# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import logging

_logger = logging.getLogger(__name__)


class RuleInfo(models.Model):
    '''
    日计划设备检修信息，包含计划内容和日常维护及运行内容
    '''
    _inherit = "metro_park_maintenance.rule_info"

    @api.model
    def _compute_is_mile(self):
        '''
        计算是否为公里数
        :return:
        '''
        mile_rule = self.env.ref('metro_park_base_data_8.repair_rule_l')
        for record in self:
            if record.rule and record.rule.id == mile_rule.id:
                record.is_mile = True

    @api.depends("plan_id", "dev")
    def _compute_last_repair_info(self):
        '''
        计算上次里程修信息
        :return:
        '''
        if len(self) == 0:
            return

        for record in self:
            if not record.plan_id or not record.dev:
                continue

            pre_date_train_info = record.plan_id.train_infos.filtered(
                lambda item: item.train.id == record.dev.id)
            if len(pre_date_train_info) > 1:
                pre_date_train_info = pre_date_train_info[0]

            record.prev_date_location = pre_date_train_info.location.id
            record.miles = pre_date_train_info.miles
            record.last_mile_repair_date = pre_date_train_info.last_mile_repair_date
            record.last_repair_miles = pre_date_train_info.last_repair_miles
            record.miles_after_last_repair = pre_date_train_info.miles_after_last_repair


