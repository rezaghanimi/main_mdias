# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class MaintenancePlace(models.Model):
    _name = 'maintenance_place'

    name = fields.Char(string='区域')
    station = fields.Many2one('metro_park_base.location', string='站点')
    place = fields.One2many('maintenance_equipment', 'place', string='区域下面的设备')
