# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum, base64, xlrd
import logging

_logger = logging.getLogger(__name__)


class ImportDayPlans(models.TransientModel):
    _name = 'metro_park_maintenance.import_day_plans'
    _description = '导入日计划向导'

    file = fields.Binary(string='导入文件')
    day_plan_id = fields.Many2one(string='日计划', comodel_name='metro_park_maintenance.day_plan')

    # TODO 暂时不处理，格式处理逻辑不对应，太难了~~~
    def start_import(self):
        """
        开始导入
        由于格式限制，只能导入正线运营的列表。
        :return:
        """
        self.ensure_one()
        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        tmp_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []

        # 不要第一行, 前边两行不要，一行是标题栏, 一行是表格头
        for row in range(1, tmp_sheet.nrows):
            all_data.append(tmp_sheet.row_values(row))

        dev_no = ''
        for data in all_data[2:]:
            _logger.info(data)
            # 车号
            dev_no = data[0]
            dev_id = self.env['metro_park_maintenance.train_dev'].search([('dev_no', '=', dev_no)], limit=1)
            if not dev_id:
                raise exceptions.ValidationError('系统中不存在设备号：{}，请检查后再试！'.format(dev_no))
            # 作业时间
            work_time = data[1]
            # 这里可以加上一个条件，容错处理，可能时间隔开符号为~  也可能为-
            try:
                split_work_time = work_time.split('~')
                if len(split_work_time) == 1:
                    split_work_time = work_time.split('-')
                work_start_time = split_work_time[0]
                work_end_time = split_work_time[1]
            except Exception as e:
                raise exceptions.ValidationError('导入作业时间格式错误：{}，Error:{}！'.format(work_time, str(e)))
        day_plan = self.env["metro_park_maintenance.day_plan"].browse(self.day_plan_id.id)

