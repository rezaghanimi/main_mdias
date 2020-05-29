# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BackupElectricAreaInfo(models.Model):
    '''
    备用供电分区信息
    '''
    _name = 'metro_park_base.backup_electric_area_info'
    _track_log = True

    electric_area_id = fields.Many2one(string="代电分区",
                                       comodel_name="metro_park_base.electric_area")
    switch_no = fields.Char(string='开关编号')
    electric_area = fields.Many2one(string='供电分区',
                                    comodel_name="metro_park_base.electric_area")
