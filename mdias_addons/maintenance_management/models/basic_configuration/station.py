# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class MaintenanceStation(models.Model):
    _inherit = 'metro_park_base.location'

    place = fields.One2many('maintenance_place', 'station', string='站点下面的区域')
