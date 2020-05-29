
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OffsetInfo(models.TransientModel):
    '''
    偏移信息
    '''
    _name = 'metro_park_maintenance.offset_info'

    index = fields.Char(string='索引')
    rule = fields.Many2one(string='规程',
                           comodel_name='metro_park_maintenance.repair_rule')
    dev_id = fields.Many2one(string='设备',
                             comodel_name='metro_park_maintenance.train_dev')
