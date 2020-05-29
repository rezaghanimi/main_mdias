# -*- coding: utf-8 -*-
from odoo import http
from pprint import pprint
import json
import xlrd
import io
from odoo.http import request, route
from odoo.tools.misc import xlwt


class MainController(http.Controller):
    '''
    测试接口
    '''
    @ http.route(['/dispatch/download/time_table/<int:time_table_id>'], type='http', auth='public', csrf=False)
    def download_time_table(self, time_table_id, **kwargs):
        '''
        下载运行图
        :param kwargs:
        :param time_table_id:
        :return:
        '''
        records = request.env['metro_park_base.time_table_data'].search_read(
            [('time_table_id', '=', time_table_id)])
        if not records:
            return
        one_row = [
            '序号', '回库车次', '车号', '换轨时间', '接车股道', '变更股道', '洗车', '检修计划', '备注'
        ]
        field_list = ['dev_name', 'dev_no', 'miles', 'unit']
        # 新建一个excel文件
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        for data_i, head_sheet in enumerate(one_row):
            table.write(0, data_i, head_sheet)
        for i, data in enumerate(records):
            for j in range(len(field_list)):
                table.write(i + 1, j, data.get(field_list[j], ''))
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '运行图模版.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @http.route('/dispatch/download_attachment', type='http', auth='public', csrf=False)
    def download_attachment(self):
        '''
        下载附件
        :return:
        '''
        all_rec = request.env['metro_park_base.time_table_data'].search_read([
        ])
        one_row = [
            '序号', '所属时刻表', '车次', '出场场段', '入场场段', '计划回库时间', '计划出库时间', '高峰时段'
        ]
        field_list = ['sequence', 'time_table_id', 'train_no',
                      'out_location', 'back_location', 'plan_in_time',
                      'plan_out_time', 'high_time_train']
        # 新建一个excel文件
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        for data_i, head_sheet in enumerate(one_row):
            table.write(0, data_i, head_sheet)
        for i, data in enumerate(all_rec):
            for j in range(len(field_list)):
                table.write(i + 1, j, data.get(field_list[j], ''))
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '运行图附件.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @http.route('/metro_park_dispatch/get_cur_train_data/', auth='public', type='http')
    def get_dispatch_plans(self, **kw):
        '''
        取得现车数据
        :param kw:
        :return:
        '''
        location_id = request.params.get('location_id', None)
        model = http.request.env['metro_park_dispatch.cur_train_map_display']
        return model.get_cur_train_data(location_id)


