# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OperationRecord(models.Model):
    '''
    车辆运行公里数操作记录
    '''
    _name = 'metro_park_maintenance.operation_record'
    _description = '车辆运行公里数操作记录'
    _rec_name = 'record_no'
    
    record_no = fields.Char(string='编号')
    tm = fields.Date(string='时间')
    manipulate_type = fields.Selection(string='操作方式',
                                       selection=[('auto', '自动'), ('manual', '手动')])
    train = fields.Many2one(string='车辆',
                            comodel_name='metro_park_maintenance.train_dev')
    last_miles = fields.Float(string='上次运行公理数')
    inc_miles = fields.Float(string='增加公里数')
    cur_miles = fields.Float(string='当前公里数')
    ip_address = fields.Char(string='ip地址')

