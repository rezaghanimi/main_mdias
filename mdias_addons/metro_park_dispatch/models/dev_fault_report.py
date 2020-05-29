
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class DevFaultReport(models.TransientModel):
    '''
    设备故障报告
    '''
    _name = 'metro_park_dispatch.dev_fault_report'
    _track_log = True
    
    fault_type = fields.Selection(string='类型',
                                  selection=[('affect_plan', '影响运营'),
                                             ('affect_run', '影响行车'),
                                             ('affect_other', '其它')])
    cur_train = fields.Many2one(comodel_name="metro_park_dispatch.cur_train_manage",
                                string="车辆故报")
    cur_rail = fields.Many2one(string="当前位置",
                               comodel_name="metro_park_base.rails_sec")
    reason = fields.Text(string='原因')

    @api.model
    def on_ok(self):
        '''
        设备故报, 根据当前车辆的位置决定是正线故报还是库内故报
        :return:
        '''
        # 更新现车状态
        self.cur_train.train_status = 'fault'

        # 添加记录
        self.env["metro_park_dispatch.fault_history"].create({
            "cur_train": self.cur_train.id,
            "fault_type": self.fault_type,
            "cur_rail": self.cur_rail,
            "reason": self.reason
        })

