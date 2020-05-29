
# -*- coding: utf-8 -*-

from odoo import models, fields


class ReportPointDetail(models.Model):
    '''
    报点信息
    '''
    _name = 'metro_park_dispatch.report_point_detail'

    _description = '报点信息'
    _track_log = True

    train_id = fields.Many2one(string="列车",
                               comodel_name="metro_park_dispatch.report_point_detail")

    report_time = fields.Datetime(string="报点时间")

    report_type = fields.Selection(string='报点类型',
                                   selection=[('arrive', '到达'), ('leave', '离开')])
    rail_sec_id = fields.Many2one(string='股道',
                                  comodel_name='metro_park_base.rails_sec',
                                  domain="[('is_track', '=', True)]")

    rail_no = fields.Char(string='股道号', related='rail_sec_id.no')
