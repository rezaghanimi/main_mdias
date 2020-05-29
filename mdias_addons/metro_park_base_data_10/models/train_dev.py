# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum


class TrainDev(models.Model):
    '''
    车辆设备, 说明，由于初期设计原因，多了一堆的废弃字段
    '''
    _inherit = 'metro_park_maintenance.train_dev'

    @api.depends()
    def _compute_last_repair_info(self):
        '''
        计算上次里程修信息
        :return:
        '''
        today_str = pendulum.today('UTC').format('YYYY-MM-DD')
        info = self.inner_compute_last_repair_info(today_str)
        last_repair_info = info["last_repair_info"]
        info_cache = info["info_cache"]

        for record in self:
            if record.id in last_repair_info:
                record.last_mile_repair_date = last_repair_info[record.id]

        for record in self:
            if record.id in last_repair_info:
                key = '{dev_no}_{date}'.format(
                    dev_no=record.dev_no, date=str(record.last_mile_repair_date))
                if key in info_cache:
                    record.last_repair_miles = info_cache[key].total_mileage

    @api.multi
    def inner_compute_last_repair_info(self, date_str):
        '''
        计算最终的修程信息
        :return:
        '''
        # 计算上一次的检修日期
        dates = []
        # 由于里程修会被结合，所以还要找均衡修
        mile_rule_id = self.env.ref('metro_park_base_data_10.repair_rule_l').id
        rules = self.env['metro_park_maintenance.repair_rule'].search(
            [('target_plan_type', '=', 'year')])
        rule_ids = rules.ids
        rule_ids.append(mile_rule_id)

        last_repair_info = \
            self.env['metro_park_maintenance.rule_info'].get_last_repair_date(
                rule_ids, date_str)

        for record in self:
            dev_id = record.id
            if dev_id in last_repair_info:
                if last_repair_info[dev_id]:
                    dates.append(str(last_repair_info[dev_id]))

        info_cache = dict()
        dev_nos = self.search([]).mapped('dev_no')
        infos = self.env["funenc.tcms.vehicle.data"].search(
            [('name', 'in', dev_nos), ('date', 'in', dates)])
        for info in infos:
            key = '{dev_no}_{date}'.format(dev_no=info.name, date=str(info.date))
            info_cache[key] = info

        return {
            "last_repair_info": last_repair_info,
            "info_cache": info_cache
        }
