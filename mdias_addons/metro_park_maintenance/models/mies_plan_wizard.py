
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MiesPlanWizard(models.Model):
    '''
    自动安排里程检向导
    '''
    _name = 'metro_park_maintenance.mies_plan_wizard'
    
    trains = fields.Many2many(string='车辆',
                              comodel_name='metro_park_maintenance.import_pre_day_miles_info',
                              relation='miles_wizard_and_train_rel',
                              col1='wizard_id',
                              col2='dev_id')

