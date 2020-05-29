
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class Location(models.Model):
    '''
    位置管理
    '''
    _inherit = 'metro_park_base.location'

    max_repair_info = fields.One2many(string="最大检修信息",
                                      comodel_name="metro_park_maintenance.max_repair_info",
                                      inverse_name="location")

    @api.model
    def init_max_repair_info(self):
        '''
        初始化最大修程修息
        :return:
        '''

        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao")
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu")

        repair_rule_dd = self.env.ref('metro_park_base_data_10.repair_rule_dd')
        repair_rule_xc = self.env.ref('metro_park_base_data_10.repair_rule_xc')
        repair_rule_l = self.env.ref('metro_park_base_data_10.repair_rule_l')

        location_banqiao.max_repair_info = \
            [(0, 0, {"rule_id": repair_rule_dd, "max_count": 4}),
             (0, 0, {"rule_id": repair_rule_l, "max_count": 4}),
             (0, 0, {"rule_id": repair_rule_xc, "max_count": 4})]

        location_gaodalu.max_repair_info = \
            [(0, 0, {"rule_id": repair_rule_dd, "max_count": 3}),
             (0, 0, {"rule_id": repair_rule_l, "max_count": 3}),
             (0, 0, {"rule_id": repair_rule_xc, "max_count": 3})]
