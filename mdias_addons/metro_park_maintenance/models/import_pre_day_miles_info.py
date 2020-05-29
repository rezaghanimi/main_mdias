
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum, base64, xlrd


class ImportPreDayMilesInfo(models.TransientModel):
    '''
    公里数历史导入向导
    '''
    _name = 'metro_park_maintenance.import_pre_day_miles_info'
    
    file = fields.Binary(string='文件')
    day_plan_id = fields.Many2one(string='日计划',
                                  comodel_name='metro_park_maintenance.day_plan')

    @api.multi
    def on_ok(self):
        '''
        导入生产说明
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
        datas = all_data[3:]

        day_plan = self.env["metro_park_maintenance.day_plan"].browse(self.day_plan_id.id)
        plan_date = pendulum.parse(str(day_plan.plan_date)).subtract(days=1)
        month_txt = plan_date.format('M月')
        plan_day = plan_date.day

        train_infos = day_plan.train_infos
        train_info_cache = {info.train.dev_no: info for info in train_infos}
        # 反向查找月份
        start_row = -1
        for index, row in enumerate(datas):
            if row[1] == month_txt:
                start_row = index
                break

        if start_row == -1:
            raise exceptions.ValidationError('没有找到当月数据')
        start_row = start_row + 1

        for index in range(start_row, start_row + len(train_info_cache)):
            row_data = datas[index]
            dev_no = str(row_data[1])
            dev_no = dev_no.replace('.0', '')
            if not dev_no:
                raise exceptions.ValidationError('没有找到车号, {row}'.format(row=index))

            # 排计划的前一天
            mile_index = 1 + plan_day - 1
            miles = row_data[mile_index]
            last_repair_miles = row_data[1 + 32]
            miles_after_last_repair = row_data[1 + 33]

            if dev_no not in train_info_cache:
                raise exceptions.ValidationError('没有找到设备{dev_no}'.format(dev_no=dev_no))

            info = train_info_cache[dev_no]
            info.miles = miles
            info.last_repair_miles = last_repair_miles
            info.miles_after_last_repair = miles_after_last_repair
