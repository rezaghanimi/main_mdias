
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchDetailRouteInfo(models.Model):
    '''
    子进路信息， 勾计划子表
    '''
    _name = 'metro_park_dispatch.dispatch_detail_route_info'
    _order = "index"

    index = fields.Char(string='序号')
    route_id = fields.Many2one(string='联锁进路',
                               comodel_name='metro_park.interlock.route',
                               default=None)
    detail_id = fields.Many2one(string='调车通知单',
                                comodel_name='metro_park_dispatch.dispatch_detail',
                                default=None)
    back_out_plan_id = fields.Many2one(string='收发车勾详情',
                                       comodel_name='metro_park_dispatch.train_back_out_detail',
                                       default=None)
    active = fields.Boolean(string="存档", default=True)

    @api.multi
    def unlink(self):
        for record in self:
            record.active = False
