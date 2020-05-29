
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import xlrd
import base64
import pendulum
import re
from odoo.addons.odoo_operation_log.model_extend import LogManage

INDEX_COL = 0
TRAIN_NO_COL = 1
PLAN_OUT_LOCATION_COL = 2
PLAN_OUT_TIME_COL = 3
PLAN_BACK_LOCATION_COL = 4
PLAN_BACK_TIME_COL = 5


class ImportTimeTable(models.Model):
    '''
    每条线重写这个函数进行处理
    '''
    _inherit = 'metro_park_dispatch.import_time_table'

    @api.multi
    def on_ok(self):
        '''
        导入运行图
        :return:
        '''
        cur_location = self.env.user.cur_location
        if not cur_location:
            raise exceptions.ValidationError("当前用户没有配置位置信息。")

        main_line = self.env.ref("metro_park_base_data_6.main_line_location").id
        hui_long = self.env.ref("metro_park_base_data_6.hui_long").id
        pi_tong = self.env.ref("metro_park_base_data_6.pi_tong").id

        time_table_model = self.env['metro_park_base.time_table']
        locations_model = self.env['metro_park_base.location']
        time_table_data_model = self.env['metro_park_base.time_table_data']

        # 分为从时刻表导入和从运行图概要导入
        if self.type == 'run_plan':
            time_table = time_table_model.create({
                'no': self.no,
                'time_table_type': self.time_table_type,
            })

            datas = self.read_excel()

            # 检查表头
            if len(datas) < 2:
                raise exceptions.ValidationError('数据表格式不正确，行数小于2')

            # 检查表头
            header_row = datas[0]
            if header_row[INDEX_COL] != '序号':
                raise exceptions.Warning('表头"序号"不正确, 请修正后再导入!')

            if header_row[TRAIN_NO_COL] != '车底ID':
                raise exceptions.Warning('表头"车底ID"不正确, 请修正后再导入!')

            if header_row[PLAN_OUT_LOCATION_COL] != '出库位置':
                raise exceptions.Warning('表头"出库位置"不正确, 请修正后再导入!')

            if header_row[PLAN_OUT_TIME_COL] != '出车场时间':
                raise exceptions.Warning('表头"出车场时间"不正确, 请修正后再导入!')

            if header_row[PLAN_BACK_LOCATION_COL] != '入库位置':
                raise exceptions.Warning('表头"入库位置"不正确, 请修正后再导入!')

            if header_row[PLAN_BACK_TIME_COL] != '回车场时间':
                raise exceptions.Warning('表头"回车场时间"时间不正确, 请修正后再导入!')

            # 取得所有的场段名称
            valid_rows = []
            locations_ar = []
            for row in datas:
                if len(row) > 1:
                    index = row[0]
                    if re.match(r'^\d+(.0)?$', str(index)):
                        valid_rows.append(row)
                        locations_ar.append(row[PLAN_OUT_LOCATION_COL])
                        locations_ar.append(row[PLAN_BACK_LOCATION_COL])

            locations = locations_model.search([('name', 'in', locations_ar)])
            if len(locations) == 0:
                raise exceptions.ValidationError("没有找到位置数据!")

            location_cache = {location['name']: location['id'] for location in locations}

            vals = []
            for row in valid_rows:
                out_location = row[PLAN_OUT_LOCATION_COL].strip()
                back_location = row[PLAN_BACK_LOCATION_COL].strip()
                # 只要有一个就添加数据
                if out_location in location_cache or back_location in location_cache:
                    if out_location not in location_cache:
                        out_location = main_line
                    else:
                        out_location = location_cache.get(out_location)
                    if back_location not in location_cache:
                        back_location = main_line
                    else:
                        back_location = location_cache.get(back_location)

                    # 转换为utc时间
                    plan_out_time = pendulum.parse('2019-01-01 ' + str(row[PLAN_OUT_TIME_COL]))
                    plan_out_time = plan_out_time.subtract(hours=8)

                    plan_back_time = pendulum.parse('2019-01-01 ' + str(row[PLAN_BACK_TIME_COL]))
                    plan_back_time = plan_back_time.subtract(hours=8)

                    # 时间格式检验
                    vals.append({
                        'sequence': int(row[INDEX_COL]),
                        'train_no': str(row[TRAIN_NO_COL]),
                        'out_location': out_location,
                        'plan_out_time': plan_out_time.format('YYYY-MM-DD HH:mm:ss'),  # 这里时间查询时要注意
                        'plan_in_time': plan_back_time.format('YYYY-MM-DD HH:mm:ss'),  # 这里时间查询时要注意
                        'back_location': back_location,
                        'time_table_id': time_table['id']
                    })

            if len(vals) == 0:
                raise exceptions.ValidationError('没有导入任何数据，请检查文件是否正确')

            time_table_data_model.create(vals)
            LogManage.put_log(content='导入运行图', mode='import_diagram')
            return False
        else:
            time_table = time_table_model.create({
                'no': self.no,
                'time_table_type': self.time_table_type,
            })

            bin_data = base64.b64decode(self.xls_file)
            workbook = xlrd.open_workbook(file_contents=bin_data)
            sheet = workbook.sheet_by_index(0)
            vals = []
            for i in range(1, sheet.nrows):
                data = sheet.row_values(i)
                if data[4] == "回龙停车场":
                    out_location = hui_long
                elif data[4] == "郫筒":
                    out_location = pi_tong
                else:
                    out_location = main_line
                if data[5] == "回龙停车场":
                    back_location = hui_long
                elif data[5] == "郫筒":
                    back_location = pi_tong
                else:
                    back_location = main_line
                plan_out_time = pendulum.parse('2019-01-01 ' + str(data[6]))
                plan_out_time = plan_out_time.subtract(hours=8)

                plan_back_time = pendulum.parse('2019-01-01 ' + str(data[8]))
                if plan_back_time.hour < 3:
                    plan_back_time = pendulum.parse('2019-01-03 ' + str(data[8]))
                plan_back_time = plan_back_time.subtract(hours=8)

                vals.append({
                    'sequence': data[0],
                    'train_no': data[1],
                    'out_location': out_location,
                    'plan_out_time': plan_out_time.format('YYYY-MM-DD HH:mm:ss'),  # 这里时间查询时要注意
                    'plan_in_time': plan_back_time.format('YYYY-MM-DD HH:mm:ss'),  # 这里时间查询时要注意
                    'back_location': back_location,
                    'time_table_id': time_table['id'],
                    'miles': data[11]
                })
            if len(vals) == 0:
                raise exceptions.ValidationError('没有导入任何数据，请检查文件是否正确')

            time_table_data_model.create(vals)
            LogManage.put_log(content='导入车底运用指标', mode='import_diagram')
