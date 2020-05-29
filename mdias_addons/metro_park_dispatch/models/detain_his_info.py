
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DetainHisInfo(models.Model):
    '''
    扣车记录
    '''
    _name = 'metro_park_dispatch.detain_his_info'
    _track_log = True

    cur_train = fields.Many2one(string='现车',
                                comodel_name='metro_park_dispatch.cur_train_manage')

    start_date = fields.Date(string='开始日期')
    end_date = fields.Date(string="结束日期")

    un_detain_date = fields.Date(string='解除日期')
    state = fields.Selection(selection=[('detaining', '扣车中'), ('finished', '已解除')], default="detaining")
    type = fields.Selection(selection=[("detain", "扣车"), ('un_detain', "解除扣车")], string="类型")
    reason = fields.Text(string='原因')
