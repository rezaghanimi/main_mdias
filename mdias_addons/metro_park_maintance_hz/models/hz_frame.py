
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HzFrame(models.Model):
    '''
    框架
    '''
    _name = 'metro_park_maintance_hz.hz_frame'
    
    name = fields.Char(string='名称')
