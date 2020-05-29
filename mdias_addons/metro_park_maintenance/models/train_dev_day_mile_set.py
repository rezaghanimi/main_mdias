# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainDevDayMileSet(models.Model):
    '''
    设备公里数设置
    '''
    _name = 'metro_park_maintenance.train_dev_day_mile_set'
    _description = '车辆公里数设置'
    
    user_id = fields.Many2one(string='指定用户',
                              comodel_name='funenc.wechat.user')
    miles = fields.Char(string='公里数')
    date = fields.Date(string='日期')
    remark = fields.Char(string='备注')
