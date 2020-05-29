
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TempRulePlanHistory(models.Model):
    '''
    检技通安排信息
    '''
    _name = 'metro_park_maintenance.temp_rule_plan_history'
    
    temp_rule_id = fields.Many2one(string='检技通',
                                   comodel_name="metro_park_maintenance.repair_tmp_rule")
    rule_info_id = fields.Many2one(string='规程安排信息',
                                   comodel_name='metro_park_maintenance.rule_info')
    date = fields.Date(string="日期", related='rule_info_id.date')
    dev = fields.Many2one(string='设备',
                          comodel_name='metro_park_maintenance.train_dev')
    key = fields.Char(string="key", help="用于标认设备检技通",
                      compute='_compute_temp_rule')

    @api.depends()
    def _compute_temp_rule(self):
        '''
        计算检技通key
        :return:
        '''
        for record in self:
            record.key = '{rule_id}_{dev_id}'.format(
                rule_id=record.temp_rule_id.id, dev_id=record.dev.id)

