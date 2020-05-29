
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainNum(models.Model):
    '''
    车辆设备数量, 用于勾计划
    '''
    _name = 'metro_park_dispatch.train_num'
    _order = "index"
    _rec_name = "value"

    index = fields.Integer(string='序号')
    value = fields.Integer(string='值')

    _sql_constraints = [('value_unique', 'UNIQUE(value)', "值不能重复"),
                        ('index_unique', 'UNIQUE(index)', "序号不能重复")]

