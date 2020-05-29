
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainInOutLog(models.Model):
    '''
    收发车计划日志
    '''
    _name = 'metro_park_dispatch.train_in_out_log'
    _track_log = True
    _order = "id desc"

    type = fields.Selection(selection=[('in_plan', '收车计划'), ('out_plan', '发车计划')],
                            string="类型")
    train_dev = fields.Many2one(string="车辆",
                                comodel_name='metro_park_maintenance.train_dev')
    operation = fields.Char(string="操作")
    result = fields.Char(string="执行结果")
