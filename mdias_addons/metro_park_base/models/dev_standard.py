
# -*- coding: utf-8 -*-

from odoo import models, fields


class DevStandard(models.Model):
    '''
    设备规格型号
    '''
    _name = 'metro_park_base.dev_standard'
    _description = '设备规格型号'
    _track_log = True
    
    name = fields.Char(string='名称')
    dev_type = fields.Many2one(string='设备类型',
                               comodel_name="metro_park_base.dev_type")
    remark = fields.Char(string='备注')
