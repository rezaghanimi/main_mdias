
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Line(models.Model):
    '''
    线别
    '''
    _name = 'metro_park_base.line'
    _description = '线路'
    _track_log = True
    
    name = fields.Char(string='线别名称', required=True)
    code = fields.Char(string='线别代码', required=True)

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "线别名称不能重复")]

    @api.multi
    def get_locations(self):
        '''
        取得本线路的车场
        :return:
        '''
        self.ensure_one()
        location_type = self.env.ref('metro_park_base.location_type_park')
        locations = self.env['metro_park_base.location'].search(
            [('line', '=', self.id),
             ('location_type', '=', location_type.id)])
        return locations.ids
