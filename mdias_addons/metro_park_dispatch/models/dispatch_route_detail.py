# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchRouteDetail(models.Model):
    '''
    进路指令
    '''
    _name = 'metro_park_dispatch.dispatch_route_detail'
    _description = '调车指令'
    _track_log = True
    
    rail = fields.Many2one(string='股道号码',
                           comodel_name='metro_park_base.rails_sec',
                           domain="[('is_track', '=', True)]")
    supend = fields.Boolean(string='摘挂(+-)')
    train_num = fields.Char(string='车数')
    notice_detail = fields.Text(string='注意事项')
    plan_name = fields.Char(string='计划名称')
    start_time = fields.Datetime(string='开始时间')
    end_time = fields.Datetime(string='结束时间')
    display_time = fields.Char(string='显示时间', compute='compute_display_time')
    status = fields.Selection(string='状态',
                              selection=[('finished', '已结束'),
                                         ('executing', '执行中'),
                                         ('pushed', '已推入'),
                                         ('reback', '已撤回')])
    dispatch_job_ticket_id = fields.Many2one(string='调车作业单',
                                             comodel_name='metro_park_dispatch.dispatch_job_ticket')

    @api.depends('start_time', 'end_time')
    def compute_display_time(self):
        pass

