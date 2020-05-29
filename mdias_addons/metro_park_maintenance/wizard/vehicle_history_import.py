# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api, exceptions
import pendulum
import xlrd
import base64
import logging

_logger = logging.getLogger(__name__)


class VehicleHistoryImport(models.TransientModel):
    _name = 'maintenance.vehicle.history.import'
    _description = '历史公里数导入'
    _rec_name = 'start_date'

    start_date = fields.Date(string='开始日期')
    end_date = fields.Date(string='结束日期')
    file = fields.Binary(string='导入文件')

    @api.multi
    def start_import(self):
        '''
        设备公里数导入
        :return:
        '''
        self.ensure_one()
        # 防止重复导入相同日期的数据，在导入前先清除已存在时间段内的历史记录
        sql = """delete from funenc_tcms_vehicle_data where date >= '%s' and date < '%s'""" % (self.start_date, self.end_date)
        self._cr.execute(sql)
        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)
        # 根据sheet索引或者名称获取sheet内容
        sheet_date = pendulum.parse(str(self.start_date))
        sheet_name = sheet_date.format('YYYY年M月')
        sheet_names = workbook.sheet_names()
        if sheet_name not in sheet_names:
            sheet_name = sheet_date.format('YYYY年MM月')
            if sheet_name not in sheet_names:
                raise exceptions.ValidationError(
                    '没有找到{date}对应的sheet!'.format(date=self.start_date))
        table = workbook.sheet_by_name(sheet_name)  # sheet索引从0开始
        rows = []
        for row in range(0, table.nrows):
            rows.append(table.row_values(row))
        if len(rows) < 3:
            raise exceptions.Warning("数据错误！请检查格式是否正确")
        start_date = self.start_date
        end_date = self.end_date
        while True:
            _logger.info("import date:{}".format(start_date))
            if start_date > end_date:
                break
            try:
                self.import_file_by_date(rows, start_date)
            except Exception as error:
                _logger.info(error)
                break
            start_date = start_date + timedelta(days=1)
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def import_file_by_date(self, rows, date):
        update_time = import_date = pendulum.parse(str(date))
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
        today_train = get_column('当日公里数')

        if mile_col == -1:
            raise exceptions.ValidationError('没有找到公里数列')
        if drag_energy_col == -1:
            raise exceptions.ValidationError('没有找到牵引能耗列')
        if auxiliary_energy == -1:
            raise exceptions.ValidationError('没有找到辅助能耗列')
        if renewable_energy == -1:
            raise exceptions.ValidationError('没有找到再生能量列')
        if today_train == -1:
            raise exceptions.ValidationError('没有找到当日里程数列')

        rows = rows[2:]
        vehicle_list = list()
        for row in rows:
            dev_no = str(int(row[0]))
            vehicle_list.append({
                'name': dev_no,
                'today_mileage': row[today_train],  # 当日里程
                'total_mileage': row[mile_col],     # 公里数
                'traction_consumption': row[drag_energy_col],       # 牵引能耗
                'auxiliary_consumption': row[auxiliary_energy],     # 辅助能耗
                'regeneration_consumption': row[renewable_energy],  # 再生能量
                'update_time': update_time,                         # 更新时间
            })
        self.env['funenc.tcms.vehicle.data'].create(vehicle_list)
