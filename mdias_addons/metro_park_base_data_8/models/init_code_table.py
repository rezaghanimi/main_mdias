
# -*- coding: utf-8 -*-

from odoo import models, api
from .code_tables.ban_qiao import codes as ban_qiao_codes
from .code_tables.gao_da_lu import codes as gao_da_lu_codes


class InitCodeTable(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_8.init_code_table'

    @api.model
    def init_code_table(self):
        '''
        初始化按扭表
        :return:
        '''
        records = self.search([])
        if len(records) > 0:
            return

        location_banqiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        location_gaodalu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        vals = []
        for key, items in ban_qiao_codes.items():
            for item in items:
                vals.append({
                    "index": item["index"],
                    "code": item["code"],
                    "location": location_banqiao,
                    "code_type": key.rstrip("es") if key.endswith("es") else key.rstrip("s")
                })

        for key, items in gao_da_lu_codes.items():
            for item in items:
                vals.append({
                    "index": item["index"],
                    "code": item["code"],
                    "location": location_gaodalu
                })

        self.create(vals)