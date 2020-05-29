
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConstructionSyncRecord(models.Model):
    '''
    施工计划同步日志
    '''
    _name = 'metro_park_dispatch.construction_sync_record'
    _description = '施工计划同步日志'
    _track_log = True
    
    no = fields.Char(string='编号')
    sync_tm = fields.Datetime(string='同步时间')
    syn_method = fields.Selection(string='同步方式',
                                  selection=[('auto', '自动'),
                                             ('manual', '人工')])
    syn_result = fields.Selection(string='状态',
                                  selection=[('success', '成功'),
                                             ('fail', '失败')])
