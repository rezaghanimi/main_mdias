
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RouteCommand(models.Model):
    '''
    进路指令
    '''
    _name = 'metro_park_dispatch.route_command'
    _description = '进路指令'
    _track_log = True
    
    dispatch_route_detail = fields.Many2one(string='钩计划详情',
                                            comodel_name='metro_park_dispatch.dispatch_route_detail')
    start_rail = fields.Many2one(string='源股道',
                                 comodel_name='metro_park_base.rails_sec',
                                 domain="[('is_track', '=', True)]")
    dest_rail = fields.Many2one(string='目标股道', comodel_name='metro_park_base.rails_sec',
                                domain="[('is_track', '=', True)]")
    status = fields.Selection(string='状态',
                              selection=[('finished', '已结束'),
                                         ('executing', '执行中'),
                                         ('wait_execute', '待执行'),
                                         ('pushed', '已推入'),
                                         ('reback', '已退回')])
    

