
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SubRouteInfo(models.Model):
    '''
    子路由信息
    '''
    _name = 'interlock_table.sub_route_info'
    _order = 'index asc'
    
    route = fields.Many2one(string='进路',
                            comodel_name='metro_park.interlock.route')
    index = fields.Char(string='序号', default=0)
