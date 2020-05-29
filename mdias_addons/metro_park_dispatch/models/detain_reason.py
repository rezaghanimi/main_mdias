
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DetainReason(models.Model):
    '''
    扣车原因, 这里是可选择的原因
    '''
    _name = 'metro_park_dispatch.detain_reason'
    _track_log = True
    _rec_name = 'reason'
    
    reason = fields.Text(string='原因', required=True)

    _sql_constraints = [('reason_unique', 'UNIQUE(reason)', "参数名称不能重复")]

