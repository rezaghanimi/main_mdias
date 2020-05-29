
# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class RouteCache(models.Model):
    '''
    路由缓存
    '''
    _name = 'interlock_table.route_cache'

    route_type = fields.Char(string='类型')
    location = fields.Many2one(
        string="地点", comodel_name="metro_park_base.location")
    start_rail = fields.Many2one(
        string='起点', comodel_name="metro_park_base.rails_sec")
    end_rail = fields.Many2one(
        string='终点', comodel_name="metro_park_base.rails_sec")
    route_info = fields.Many2many(string='路由信息',
                                  comodel_name='interlock_table.sub_route_info',
                                  relation='route_cache_sub_route_info',
                                  col1='cache_id',
                                  col2='info_id')

    @api.model
    def get_route_cache(self, location, start_rail, end_rail, route_type):
        '''
        查找进路缓存
        :return:
        '''
        rst = []
        records = self.search([('location', '=', location),
                               ('route_type', '=', route_type),
                               ('start_rail', '=', start_rail),
                               ('end_rail', '=', end_rail)])
        if records:
            for record in records:
                routes = record.route_info.search(
                    [('id', 'in', record.route_info.ids)], order="index asc")
                rst.append(routes.mapped('route'))
            return rst

        return False
