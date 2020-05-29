
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PlanConfigData(models.Model):
    '''
    排程规则数据
    '''
    _name = 'metro_park_maintenance.plan_config_data'
    _description = '计划配置数据'
    _order = 'index'
    _rec_name = 'rule'

    index = fields.Integer(string='修次')
    rule = fields.Many2one(string='规程',
                           comodel_name='metro_park_maintenance.repair_rule')
    repair_days = fields.Integer(string="检修天数", related="rule.repair_days")
    remark = fields.Text(string='备注')

    @api.model
    def get_next_repair_info(self, offset):
        offset = offset + 1
        records = self.search([])
        offset = offset % len(records)
        return records[offset]

