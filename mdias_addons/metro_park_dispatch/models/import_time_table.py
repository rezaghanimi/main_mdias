
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
import xlrd
import base64
import pendulum
import re
from ...odoo_operation_log.model_extend import LogManage

LogManage.register_type('import_diagram', '导入运行图')

INDEX_COL = 0
TRAIN_NO_COL = 1
PLAN_OUT_LOCATION_COL = 2
PLAN_OUT_TIME_COL = 3
PLAN_BACK_LOCATION_COL = 4
PLAN_BACK_TIME_COL = 5
PLAN_TOTAL_MILES_COL = 6


class ImportTimeTable(models.Model):
    '''
    导入时刻表
    '''
    _name = 'metro_park_dispatch.import_time_table'
    _description = '导入时刻表'
    _track_log = True

    def _default_sequence(self):
        '''
        取得默认的序号
        :return:
        '''
        return self.env['ir.sequence'].next_by_code('time_table.number')

    no = fields.Char(string='运行图编号', default=_default_sequence)
    type = fields.Selection(string='类型',
                            selection=[('run_plan', '运行图概要'),
                                       ('time_table', '时刻表')], required=True)
    xls_file = fields.Binary(string='文件')
    file_name = fields.Char(string='文件名称')
    time_table_type = fields.Many2one(
        string='运行图类型', comodel_name="metro_park_dispatch.time_table_type")

    def read_excel(self):
        '''
        从 excel 中读取数据
        :return:
        '''
        # 获取execl中数据
        bin_data = base64.b64decode(self.xls_file)
        workbook = xlrd.open_workbook(file_contents=bin_data)
        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []
        for row in range(0, sheet.nrows):
            all_data.append(sheet.row_values(row))
        return all_data

    @api.multi
    def on_ok(self):
        '''
        导入运行图, 放到具体的场段线路基础数据处理
        :return:
        '''
        pass
