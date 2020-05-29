
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ElectricArea(models.Model):
    '''
    供电分区
    '''
    _name = 'metro_park_base.electric_area'
    _description = '带电区域'
    _track_log = True
    
    name = fields.Char(string='名称')
    location_id = fields.Many2one(string='位置', comodel_name='metro_park_base.location')
    breaker_id = fields.Char(string='断路器编号')
    switch_no = fields.Char(string='自动隔离开关编号')
    rail_secs = fields.Many2many(string='股道',
                                 comodel_name='metro_park_base.rails_sec',
                                 relation='electric_area_rail_sec_ref',
                                 col1='electric_area_id',
                                 col2='rail_sec_id')
    backup_electric_area = fields.One2many(string="备用供电分区",
                                           comodel_name="metro_park_base.backup_electric_area_info",
                                           inverse_name="electric_area_id")
    parent_electric_area = fields.Many2one(string="父级供电分区",
                                           comodel_name="metro_park_base.electric_area")
    remark = fields.Text(string='备注')

