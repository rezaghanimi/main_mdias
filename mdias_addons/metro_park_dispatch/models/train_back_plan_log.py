
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TrainBackPlanLog(models.Model):
    '''
    收车日志
    '''
    _name = 'metro_park_dispatch.train_back_plan_log'
    _order = 'id desc'

    train_no = fields.Char(string='车号')
    location = fields.Text(string='位置')
    rail = fields.Char(string="股道")
    remark = fields.Text(string='内容')
