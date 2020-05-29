# -*- coding: utf-8 -*-

from odoo import models, api
from .code_tables.hui_long import codes as pi_tong_codes
from .code_tables.pi_tong import codes as hui_long_codes


class InitCodeTable(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_6.init_code_table'

    @api.model
    def init_code_table(self):
        '''
        初始化按扭表
        :return:
        '''
        records = self.search([])
        if len(records) > 0:
            return

        location_huilong = self.env.ref("metro_park_base_data_6.hui_long").id
        location_pitong = self.env.ref("metro_park_base_data_6.pi_tong").id

        vals = []
        for key, items in pi_tong_codes.items():
            for item in items:
                vals.append({
                    "index": item["index"],
                    "code": item["code"],
                    "location": location_huilong,
                    "code_type": key.rstrip("es") if key.endswith("es") else key.rstrip("s")
                })

        for key, items in hui_long_codes.items():
            for item in items:
                vals.append({
                    "index": item["index"],
                    "code": item["code"],
                    "location": location_pitong
                })

        self.create(vals)
