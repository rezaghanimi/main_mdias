# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class MaintenanceEquipment(models.Model):
    _name = 'maintenance_equipment'

    name = fields.Char(string='设备')
    place = fields.Many2one('maintenance_place', string='区域')
