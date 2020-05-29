
# -*- coding: utf-8 -*-

from odoo import models, fields


class ReportPointHistory(models.Model):
    '''
    报点记录
    '''
    _name = 'metro_park_dispatch.report_point_history'
    _track_log = True
    
    report_time = fields.Datetime(string='报点时间')
    rail = fields.Many2one(string='股道',
                           comodel_name='metro_park_base.rails_sec')
    train = fields.Many2one(string='车号',
                            comodel_name='metro_park_dispatch.cur_train')
    report_type = fields.Selection(string='报点类型',
                                   selection=[('arrive', '到达'), ('leave', '离开')],
                                   required=True)
