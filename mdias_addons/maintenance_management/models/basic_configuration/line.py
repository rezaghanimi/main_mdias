# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class MaintenanceLine(models.Model):
    _inherit = 'metro_park_base.line'

    station = fields.One2many('metro_park_base.location', 'line', string='线路下面的站点')
