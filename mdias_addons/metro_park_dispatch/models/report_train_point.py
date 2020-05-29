
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime


class ReportTrainPoint(models.Model):
    '''
    列车报点
    '''
    _name = 'metro_park_dispatch.report_train_point'
    _description = '列车报点'
    _track_log = True

    train_dev = fields.Many2one(string="列车",
                                comodel_name="metro_park_dispatch.cur_train_manage")

    rail_sec_id = fields.Many2one(string='报点位置',
                                  comodel_name='metro_park_base.rails_sec')

    report_type = fields.Selection(selection=[("arrive", "到达"), ("leave", "离开")],
                                   string="报点类型")

    report_time = fields.Datetime(string="时间",
                                  default=lambda self: datetime.now())

    @api.model
    def request_point_by_sec_no(self, dev_name, rail_no):
        '''
        跳转到添加页面,指定plan_type用于区分计划类型
        :return:
        '''
        train_dev = self.env["metro_park_dispatch.cur_train_manage"]\
            .search([("train.dev_name", "=", dev_name)], limit=1)
        rail_sec = self.env["metro_park_base.rails_sec"]\
            .search([("no", '=', rail_no)])
        if train_dev and rail_sec:
            return {
                "type": "ir.actions.act_window",
                "res_model": "metro_park_dispatch.report_train_point",
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_rail_sec_id': rail_sec.id,
                    'default_train_dev': train_dev.id,
                },
                "views": [[
                    self.env.ref(
                        'metro_park_dispatch.report_train_point_form').id, "form"]]
            }
        else:
            raise exceptions.Warning("车辆信息或位置信息不正确")

