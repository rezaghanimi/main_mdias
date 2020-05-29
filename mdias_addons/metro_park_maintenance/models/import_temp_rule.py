# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import xlrd
import logging

_logger = logging.getLogger(__name__)


class RepairTmpRuleImport(models.TransientModel):
    '''
    检技通导入
    '''
    _name = 'metro_park_maintenance.repair_tmp_rule_import'
    _description = '检技通导入'

    file = fields.Binary(string='导入文件')

    @api.multi
    def import_data_rec(self):
        '''
        导入检技通
        :return:
        '''
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)
        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始

        trains = []
        # 结合修程
        repair_rules = []
        for row in range(1, sheet.nrows):
            data = sheet.row_values(row)
            val = dict()
            val['no'] = data[0]
            val['name'] = data[1]
            val['content'] = data[2]
            try:
                val['start_date'] = xlrd.xldate.xldate_as_datetime(data[5], 1)
                val['end_date'] = xlrd.xldate.xldate_as_datetime(data[6], 1)
            except Exception as e:
                _logger.info(e)
                # 处理时间格式
                if data[5]:
                    val['start_date'] = data[5]
                if data[6]:
                    val['end_date'] = data[6]
            # 记录ID
            rec_id = self.env['metro_park_maintenance.repair_tmp_rule'].create(val)
            for trains_list in data[3].split(','):
                trains_data_id = self.env['metro_park_maintenance.train_dev'].search(
                    [('dev_name', '=', trains_list)]).id
                if trains_data_id:
                    trains.append(trains_data_id)
            for repair_rules_list in data[4].split(','):
                repair_rules_id = self.env['metro_park_maintenance.repair_rule'].search(
                    [('no', '=', repair_rules_list)]).id
                if repair_rules_id:
                    repair_rules.append(repair_rules_id)
            rec_id.write({'trains': [(6, 0, trains)]})
            rec_id.write({'repair_rules': [(6, 0, repair_rules)]})
