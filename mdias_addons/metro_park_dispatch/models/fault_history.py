
# -*- coding: utf-8 -*-

from odoo import models, fields, api

CUR_TRAIN_STATUS = [('fault', '故障'),
                    ('repair', '检修'),
                    ('detain', '扣车'),
                    ('wait', '待命')]


class FaultHistory(models.Model):
    '''
    车辆故报记录
    '''
    _name = 'metro_park_dispatch.fault_history'
    
    cur_train = fields.Many2one(string='车辆',
                                comodel_name='metro_park_dispatch.cur_train')
    fault_type = fields.Selection(string='故报类型',
                                  selection=CUR_TRAIN_STATUS)
    cur_rail = fields.Many2one(string='现车位置',
                               comodel_name='metro_park_base.rails_sec')
    reason = fields.Text(string='reason')
