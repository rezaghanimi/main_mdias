
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CurTrainOperationLog(models.Model):
    '''
    现车管理日志
    '''
    _name = 'metro_park_dispatch.cur_train_operation_log'
    _description = '现车日志管理'
    _track_log = True
    
    no = fields.Char(string='编号', compute='compute_no')
    operation_time = fields.Datetime(string='操作时间')
    operation_status = fields.Selection(string='状态',
                                        selection=[('success', '成功'), ('fail', '失败')])
    target = fields.Many2one(string='对象',
                             comodel_name='metro_park_maintenance.train_dev')
    operation_type = fields.Selection(string='操作类型',
                                      selection=[('retain', '扣车'),
                                                 ('deretain', '解除扣车'),
                                                 ('report_fault', '车辆故报')])
    operation_content = fields.Text(string='操作内容')
    user = fields.Many2one(string='用户',
                           comodel_name='funenc.wechat.user')
    ip = fields.Char(string='ip')
    remark = fields.Text(string='备注')
    worker = fields.Many2one(string='操作人',
                             comodel_name='funenc.wechat.user')

    def compute_no(self):
        '''
        计算编号
        :return:
        '''
        pass

