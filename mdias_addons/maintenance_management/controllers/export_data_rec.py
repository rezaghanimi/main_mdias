# -*- coding: utf-8 -*-
from odoo import fields, models, api, http
from odoo.http import request
import io
import xlwt
import datetime


class ExportDateRec(http.Controller):
    @http.route('/maintenance_management/call_api_task/export_data', type='http', auth='public', csrf=False)
    def call_api_task_export(self, **kwargs):
        '''
        :param kwargs:
        :return:
        '''
        one_row_ch = [
            '记录时间', '地点', '位置', '设备', '内容', 'IP地址',
            '维护建议'
        ]
        field_key = [
            'write_date', 'place', 'site', 'equipment',
            'content', 'ip_site', 'maintenance_advice',
        ]
        all_data = request.env['maintenance_management.call_record'].search_read([])
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        for heard_key, heard_val in enumerate(one_row_ch):
            table.write(0, heard_key, heard_val)
        for data_key, data_val in enumerate(all_data):
            for fields_key, fields_val in enumerate(field_key):
                if fields_key == 'write_date':
                    value = data_val.get(fields_key)
                    value = (value + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                    table.write(data_key + 1, fields_val, value if value else '')
                else:
                    value = data_val.get(fields_key)
                    table.write(data_key + 1, fields_val, value if value else '')

        # 文件储存在内存中
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '报警记录数据.xls'
        response = request.make_response(data,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition', 'attachment; filename={}'.format(
                                                      name.encode().decode('latin-1')))],
                                         cookies={'fileToken': 'plan'})
        return response

    @http.route('/maintenance_management/diagnosis_record/export_data', type='http', auth='public', csrf=False)
    def diagnosis_record_export(self, **kwargs):
        '''
        项目与服务诉求统计表
        :param kwargs:
        :return:
        '''
        one_row_ch = [
            '记录时间', '地点', '位置', '设备', '内容', 'IP地址',
            '维护建议'
        ]
        field_key = [
            'write_date', 'place', 'site', 'equipment',
            'content', 'ip_site', 'maintenance_advice',
        ]
        all_data = request.env['maintenance_management.diagnosis_record'].search_read([])
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        for head_key, head_val in enumerate(one_row_ch):
            table.write(0, head_key, head_val)
        for search_key, search_key_val in enumerate(all_data):
            for fields_key, fields_val in enumerate(field_key):
                if fields_val == 'write_date':
                    value = search_key_val.get(fields_val)
                    value = (value + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
                    table.write(search_key + 1, fields_key, value if value else '')
                else:
                    value = search_key_val.get(fields_val)
                    table.write(search_key + 1, fields_key, value if value else '')

        # 文件储存在内存中
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '诊断日志.xls'
        response = request.make_response(data,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition', 'attachment; filename={}'.format(
                                                      name.encode().decode('latin-1')))],
                                         cookies={'fileToken': 'plan'})
        return response
