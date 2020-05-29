
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import xlrd
import base64
import logging

_logger = logging.getLogger(__name__)


class TrainMilesImport(models.TransientModel):
    '''
    设备公里数导入
    '''
    _name = 'metro_park_dispatch.train_miles_import'
    
    date = fields.Date(string='日期')
    file = fields.Binary(string='文件')

    @api.multi
    def on_ok(self):
        '''
        设备公里数导入
        :return:
        '''

        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        sheet_date = pendulum.parse(str(self.date))
        sheet_name = sheet_date.format('YYYY年M月')
        sheet_names = workbook.sheet_names()
        if sheet_name not in sheet_names:
            sheet_name = sheet_date.format('YYYY年MM月')
            if sheet_name not in sheet_names:
                raise exceptions.ValidationError(
                    '没有找到{date}对应的sheet!'.format(date=self.date))
        table = workbook.sheet_by_name(sheet_name)  # sheet索引从0开始
        rows = []
        for row in range(0, table.nrows):
            rows.append(table.row_values(row))
        if len(rows) < 3:
            raise exceptions.Warning("数据错误！请检查格式是否正确")

        import_date = pendulum.parse(str(self.date))
        import_date = pendulum.date(import_date.year, import_date.month, import_date.day)
        date_row = rows[0]
        title_row = rows[1]

        def get_column(title):
            col = -1
            for index, data in enumerate(date_row):
                if index == 0:
                    continue
                if data and data != '':
                    try:
                        data = xlrd.xldate_as_tuple(data, 0)
                    except Exception as error:
                        _logger.info(error)
                        data = data.split('/')
                    tmp_date = pendulum.date(data[0], data[1], data[2])
                    tmp_title = title_row[index] or ''
                    tmp_title = tmp_title.strip()
                    if tmp_date == import_date and tmp_title == title:
                        col = index
                        break
            return col

        mile_col = get_column('公里数')
        drag_energy_col = get_column('牵引能耗')
        auxiliary_energy = get_column('辅助能耗')
        renewable_energy = get_column('再生电量')

        if mile_col == -1:
            raise exceptions.ValidationError('没有找到公里数列')

        if drag_energy_col == -1:
            raise exceptions.ValidationError('没有找到牵引能耗列')

        if auxiliary_energy == -1:
            raise exceptions.ValidationError('没有找到辅助能耗列')

        if renewable_energy == -1:
            raise exceptions.ValidationError('没有找到再生能量列')

        # 取得所有的设备
        devs = self.env["metro_park_maintenance.train_dev"].search([])
        dev_cache = {dev.dev_no: dev for dev in devs}

        rows = rows[2:]
        for row in rows:
            dev_no = str(int(row[0]))
            if dev_no in dev_cache:
                dev = dev_cache[dev_no]

                dev.miles = row[mile_col]
                dev.traction_energy = row[drag_energy_col]
                dev.renewable_energy = row[renewable_energy]
                dev.auxiliary_energy = row[auxiliary_energy]

