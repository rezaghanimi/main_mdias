
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PlanImportWizard(models.Model):
    '''
    计划导入向导
    '''
    _name = 'metro_park_dispatch.plan_import_wizard'
    _description = '计划导入向导'
    _track_log = True
    
    file_data = fields.Binary(string='文件')
    file_name = fields.Char(string='文件名称')
