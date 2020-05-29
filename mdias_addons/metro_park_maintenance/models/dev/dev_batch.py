
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DevBatch(models.Model):
    '''
    设备批次
    '''
    _name = 'metro_park_maintenance.dev_batch'
    _description = '设备批次管理，计划是按批次来进行的'
    _rec_name = 'batch_no'
    _track_log = True
    
    batch_no = fields.Char(string='批次')
    start_date = fields.Date(string="开始日期")
    train_devs = fields.One2many(string='设备',
                                 comodel_name='metro_park_maintenance.train_dev',
                                 inverse_name='batch_no')
    remark = fields.Char(string='备注')

    _sql_constraints = [('dev_batch_no_constrain', 'UNIQUE(batch_no)', "批次号不能重复")]

