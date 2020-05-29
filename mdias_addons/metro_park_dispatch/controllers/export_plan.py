# -*- coding: utf-8 -*-
from io import BytesIO

import pendulum
import xlsxwriter

from odoo import http
from odoo.http import request


class ExportPlan(object):

    def __init__(self, plan_date):
        self.output = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output)
        self.plan_date = plan_date

    @property
    def plan_object(self):
        return request.env['metro_park_dispatch.day_run_plan']

    def _write_table_header(self, sheet, row):
        '''
        写入表头
        :param sheet:
        :param row:
        :return:
        '''
        header_values = ['序号', '车次', '车号', '出库股道', '开始整备',
                         '列车整备时间', '整备完成', '出库时间',
                         '转换轨I道', '回库时间（板桥)', '回库时间（高大路）', '洗车', '计划维修类型', '高峰情况', '备注']
        fmt = self.workbook.add_format({'align': 'center',
                                        'bold': True,
                                        'border': 1,
                                        'font_size': 15,
                                        'valign': 'vcenter'
                                        })
        sheet.set_row(row, 30)
        for col, val in enumerate(header_values, 0):
            sheet.write(row, col, val, fmt)

    def _write_matrix_data_to_excel(self, matrix_data, sheet):
        '''
        写入矩阵
        :param matrix_data:
        :param sheet:
        :return:
        '''
        locations = request.env['metro_park_base.location']. \
            search([('id', 'in', list(matrix_data.keys()))], order='alias')
        start_row = 2

        merge_format_center = self.workbook.add_format({'align': 'center',
                                                        'bold': True,
                                                        'border': 1,
                                                        'font_size': 14
                                                        })
        format_val = {'align': 'center',
                      'bold': True,
                      'border': 1,
                      'font_size': 14}

        normal_format_cell = self.workbook.add_format(format_val)
        time_format = self.workbook.add_format(format_val)
        time_format.set_num_format('hh:mm:ss')
        for local in locations:
            sheet.merge_range('A{row}:O{row}'.format(row=start_row + 1), local.name, merge_format_center)
            start_row += 1
            self._write_table_header(sheet, start_row)
            row_data = matrix_data[local.id]
            for row in row_data:
                start_row += 1
                for index, col in enumerate(row, 0):
                    fmt = normal_format_cell
                    if index in [5, 7, 8, 9, 10]:
                        fmt = time_format
                    sheet.write(start_row, index, col, fmt)

    @classmethod
    def _set_cell_format(cls, sheet):
        sheet.set_column('C:C', 16)
        sheet.set_column('F:F', 16)
        sheet.set_column('D:D', 16)
        sheet.set_column('H:K', 16)

    def _make_export_data(self):
        def fun_key(record):
            out_plan = record.train_out_plan
            if not out_plan:
                return False
            location = out_plan.plan_out_location
            if not location:
                return False
            return location.id

        worksheet = self.workbook.add_worksheet('test')
        worksheet.set_default_row(16)
        self._write_sheet_header(worksheet)
        plan_data_outs = request.env["metro_park_dispatch.train_out_plan"] \
            .search([('date', '=', self.plan_date)])
        for plan_data_out in plan_data_outs:
            train_back_plans = request.env["metro_park_dispatch.train_back_plan"] \
                .search([('date', '=', self.plan_date), ('train_id', '=', plan_data_out.train_id.id)])
            if train_back_plans: train_back_plan = train_back_plans[0]
            if not request.env["metro_park_dispatch.day_run_plan"]. \
                    search([('date', '=', self.plan_date), ('train', '=', train_back_plan.train_id.id)]):
                request.env["metro_park_dispatch.day_run_plan"].create([{
                    'train': train_back_plan.train_id.id,
                    'date': self.plan_date,
                    'train_back_plan': train_back_plan.id,
                    'train_out_plan': plan_data_out.id,
                }])
        plan_data = self.plan_object.search([('date', '=', self.plan_date)]).group_by(fun_key)
        matrix_data = self._make_data_matrix(plan_data, self.plan_date)
        self._write_matrix_data_to_excel(matrix_data, worksheet)
        self._set_cell_format(worksheet)

    def _write_sheet_header(self, sheet):
        merge_format_center = self.workbook.add_format({'align': 'center',
                                                        'bold': True,
                                                        'border': 1,
                                                        'font_size': 16
                                                        })
        sheet.merge_range('A1:O1', 'T1009运营日计划', merge_format_center)
        date_str = pendulum.parse(str(self.plan_date)).format("YY年MM月DD日")

        sheet.merge_range('A2:C2', date_str)
        sheet.set_row(1, 18)
        sheet.write('G2', '检修调度')
        sheet.write('I2', '车场调度')
        sheet.write('M2', '车场调度签章')

    @classmethod
    def _compute_back_park_time_and_position(cls, plan):
        """
            计算回库时间和位置
        :param plan:
        :return:
        """
        default = ['', '']
        if not plan.train_back_plan:
            return default
        if not plan.train_back_plan.real_back_tm:
            return default
        back_rail = plan.train_back_plan.real_back_rail
        if not back_rail:
            return default
        location = back_rail.location
        if not location:
            return default
        back_out_time = pendulum.parse(plan.train_back_plan.real_back_tm).time()
        if location.alias == 'banqiao':
            return [back_out_time, '']
        else:
            return ['', back_out_time]

    @classmethod
    def _make_data_matrix(cls, plan_data, plan_date):
        """
            生成数据矩阵
        :param plan_data:
        :return:
        """
        _result = {}
        for location in plan_data:
            if not location:
                break
            plans = plan_data[location]
            if not plans:
                break
            index = 0
            _result.setdefault(location, [])
            for plan in plans:
                # 相对应收发车计划
                if not (plan.train_out_plan and plan.train_back_plan):
                    break
                index += 1
                out_rail = None
                if plan.train_out_plan.plan_out_end_rail:
                    out_rail = plan.train_out_plan.plan_out_end_rail.alias
                if not out_rail:
                    break
                if not plan.train_out_plan.exchange_rail_time:
                    break
                # 转换轨时间
                out_rail_time = pendulum.parse(plan_date).add(seconds=plan.train_out_plan.exchange_rail_time).time()
                # out_rail_time = pendulum.parse(str(plan.train_out_plan.exchange_rail_time)).time()
                train_ready_datetime = out_rail_time.subtract(minutes=20)
                out_park_time = pendulum.parse(plan_date).add(seconds=plan.train_out_plan.plan_out_time).time()
                # out_park_time = pendulum.parse(str(plan.train_out_plan.plan_out_time)).time()
                back_park_times = cls._compute_back_park_time_and_position(plan)
                is_wash = ''
                if plan.train_back_plan.wash:
                    is_wash = '√'
                val = [index,
                       plan.out_real_train_no,
                       plan.train.train_no,
                       out_rail,
                       '√',
                       train_ready_datetime,
                       '√',
                       out_park_time,
                       out_rail_time,
                       back_park_times[0],
                       back_park_times[1],
                       is_wash,
                       '修程',
                       '',
                       '']
                _result[location].append(val)
        return _result

    def export_excel_value(self):
        self._make_export_data()
        self.workbook.close()
        return self.output.getvalue()


class ExportControl(http.Controller):

    @http.route(['/metro_park_dispatch/export_train_plan'],
                type='http',
                auth='public',
                csrf=False)
    def export_train_plan(self, plan_date, **kwargs):
        """
            导出车辆计划
        """
        # 采用xlsx的文件后缀形式，否则打开excel会警告
        name = '%s运营计划.xlsx' % plan_date
        workbook = ExportPlan(plan_date)
        data = workbook.export_excel_value()
        response = \
            request.make_response(
                data, headers=[('Content-Type', 'application/vnd.ms-excel'),
                               ('Content-Disposition', 'attachment; filename={}'.format(
                                   name.encode().decode('latin-1')))],
                cookies={'fileToken': 'plan'})
        return response
