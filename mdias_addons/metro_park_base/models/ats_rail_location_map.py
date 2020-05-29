
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AtsRailLocationMap(models.Model):
    '''
    轨道、区段对应表
    '''
    _name = 'metro_park_base.ats_rail_location_map'
    _track_log = True
    
    index = fields.Char(string='序号')
    rail_sec_name = fields.Char(string='区段名称')
    rail_sec = fields.Many2one(string="区段",
                               compute="compute_rail_sec",
                               store=True)
    line = fields.Many2one(string="线别",
                           comodel_name="metro_park_base.line")
    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location',
                               domain="[('line.id', '=', line)]")

    @api.depends('rail_sec_name')
    def compute_rail_sec(self):
        '''
        计算轨道区段
        :return:
        '''
        main_line_rail = \
            self.env.ref("metro_park_base.main_line_rail").id
        rail_secs = \
            self.env["metro_park_base.rails_sec"].search([])
        rail_sec_cache = {rail.no: rail.id for rail in rail_secs}
        for record in self:
            if record.rail_sec_name:
                rail_sec = rail_sec_cache.get(record.rail_sec_name, None)
                if rail_sec:
                    record.rail_sec = rail_sec
                else:
                    record.rail_sec = main_line_rail
