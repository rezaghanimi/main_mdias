# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RouteInfo(models.Model):
    '''
    进路信息
    '''
    _name = 'metro_park_dispatch.route_info'
    _track_log = True

    index = fields.Char(string='索引')
    route = fields.Many2one(string='进路',
                            comodel_name="metro_park.interlock.route")
    state = fields.Selection(string='状态',
                             selection=[('finished', '已完成'),
                                        ('executing', '执行中'),
                                        ('wait', '待执行')], default="wait")
