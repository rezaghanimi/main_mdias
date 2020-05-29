
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OtherInterlock(models.Model):
    '''
    联锁表
    '''
    _name = 'metro_park_base.other_interlock'

    name = fields.Char(string='名称')
    remark = fields.Char(string='备注')
