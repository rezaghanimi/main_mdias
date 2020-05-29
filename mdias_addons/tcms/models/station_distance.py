# -*- coding: utf-8 -*-
from odoo import api, models, fields


class StationDistance(models.Model):
    _name = 'tcms.station_distance'
    _description = 'Tc1/Tc2车记录运行里程'

    name = fields.Char(string='车名')
    day_distance = fields.Char(string='当日运行里程数')
    total_mileage = fields.Char(string='总里程数')

    @api.multi
    def get_distance_day(self):
        data = []
        rec = self.sudo().search_read([('name', '!=', ''), ('day_distance', '!=', '')])
        for re in rec:
            data.append({'name': re.get('name'), 'day_distance': re.get('day_distance')})

        return data

    @api.multi
    def get_distance_days(self):
        data = []
        rec = self.sudo().search_read([('name', '!=', ''), ('total_mileage', '!=', '')])
        for re in rec:
            data.append({'name': re.get('name'), 'total_mileage': re.get('total_mileage')})

        return data
