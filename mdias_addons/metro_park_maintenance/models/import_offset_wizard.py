
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import xlrd


class ImportOffsetWizard(models.Model):
    '''
    导入偏移
    '''
    _name = 'metro_park_maintenance.import_offset_wizard'
    
    file = fields.Binary(string='文件')

    @api.multi
    def on_ok(self):
        '''
        导入偏移
        :return:
        '''

        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        tmp_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []

        # 不要第一行, 前边两行不要，一行是标题栏, 一行是表格头
        for row in range(1, tmp_sheet.nrows):
            all_data.append(tmp_sheet.row_values(row))
        datas = all_data[1:]

        # 缓存原有数据
        records = self.env["metro_park_maintenance.balance_rule_offset"].search([])
        cache = {record.dev.dev_no: record for record in records}

        # 缓存设备
        devs = self.env["metro_park_maintenance.train_dev"].search([])
        dev_cache = {dev.dev_no: dev.id for dev in devs}

        years = self.env["metro_park_maintenance.year"].search([])
        year_cache = {year.name: year.id for year in years}
        months = self.env["metro_park_maintenance.month"].search([])
        month_cache = {month.name: month.id for month in months}

        vals = []
        for data in datas:
            dev_no = data[0]
            year = data[1]
            month = data[2]
            offset_num = data[3]
            if dev_no in cache:
                record = cache[dev_no]
                record.year = year_cache[str(int(year))]
                record.month = month_cache[str(int(month))]
                record.offset_num = offset_num
            else:
                vals.append({
                    "dev": dev_cache[dev_no],
                    "year": year,
                    "month": month,
                    "offset_num": offset_num
                })

        if len(vals) > 0:
            self.env["metro_park_maintenance.balance_rule_offset"].create(vals)
