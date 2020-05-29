
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DevImportWizard(models.Model):
    '''
    车辆公里数录入向导
    '''
    _name = 'metro_park_maintenance.dev_import_wizard'
    _description = '车辆公里数录入向导'
    
    xls_file = fields.Binary(string='文件')
    file_name = fields.Char(string='文件名称')

    @api.multi
    def update_insert_miles(self):
        '''
        录入车辆公里数
        :return:
        '''
        pass

