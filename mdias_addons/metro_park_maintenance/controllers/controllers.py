# -*- coding: utf-8 -*-
import calendar

from odoo import http
import xlrd
import time
import json
import io
from datetime import datetime
from datetime import timedelta
from datetime import date
import pendulum
from odoo.http import request
from odoo.tools.misc import xlwt
from xlutils.copy import copy
import os


def get_many2many_content(m2m, field):
    """
    获取多对多字段的打印文本
    :param m2m: Many2Many的字段
    :param field: 想要获取的文本字段
    :return: 遍历字段后拼接field的str
    """
    if not m2m:
        return '--'

    m2m_list = []
    for order in m2m:
        m2m_list.append(str(getattr(order, field)))
    return '、'.join(m2m_list)


class MaintenanceController(http.Controller):

    @http.route('/maintenance/train_dev/data', type='http', auth='public', csrf=False)
    def history_miles_export(self, **kwargs):
        '''
        导出 公里数预估
        :param kwargs:
        :return:
        '''
        all_rec = request.env['metro_park_maintenance.train_dev'].search_read([])
        one_row = [
            '设备名称', '设备编码', '运行公里数', '单位'
        ]
        field_list = ['dev_name', 'dev_no', 'miles', 'unit']
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
        name = '设备公里数.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @staticmethod
    def datetime_handle(data):
        for i in data:
            i['create_date'] = i['create_date'].strftime('%Y-%m-%d %H:%M:%S')
            i['write_date'] = i['write_date'].strftime('%Y-%m-%d %H:%M:%S')
            i['__last_update'] = i['__last_update'].strftime('%Y-%m-%d %H:%M:%S')
        return data

    @http.route('/getUserData', type='http', auth='public', csrf=False)
    def get_user_data(self, **kwargs):
        '''
        所有用户信息
        :param kwargs:
        :return:
        '''
        if 'userId' in kwargs.keys():
            users = request.env['funenc.wechat.user'].sudo().search_read([('user_id', '=', int(kwargs['userId']))])
        else:
            users = request.env['funenc.wechat.user'].sudo().search_read([('user_id', '!=', False)])
        res = []
        if users:
            for user in users:
                val = {
                    'userId': user['user_id'][0],
                    'userName': user['name'],
                    'userWxid': user['wx_userid'],
                    'lineId': str(user['cur_location'][0]) if user['cur_location'] else '',
                    'lineName': user['cur_location'][1] if user['cur_location'] else '',
                    'operateDepartId': '',
                    'operateDepartName': '',
                }
                res.append(val)
            return json.dumps(res, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getDepartmentUserData', type='http', auth='public', csrf=False)
    def get_department_users_data(self, **kwargs):
        '''
        所有用户信息 根据部门查询
        :param kwargs:
        :return:
        '''
        domain = []
        res = []
        if kwargs and 'departId' in kwargs.keys():
            domain.append(('department_ids', 'in', [int(kwargs['departId'])]))
        if kwargs and 'userName' in kwargs.keys():
            domain.append(('user_id.name', '=', kwargs['userName']))
        users = request.env['funenc.wechat.user'].sudo().search_read(domain=domain)
        if users:
            for user in users:
                val = {
                    'userId': user['user_id'][0],
                    'userName': user['user_id'][1],
                    'userWxId': user['wx_userid'],
                    'userEmployeeId': '',
                    'departId': user['first_department_id'][0],
                    'departName': user['first_department_id'][1],
                }
                res.append(val)
            return json.dumps(res, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getPhoneUserData', type='http', auth='public', csrf=False)
    def get_phone_users_data(self, mobilePhon, **kwargs):
        '''
        所有用户信息 根据电话查,
        :param kwargs:
        :return:
        '''
        domain = [('mobile', '=', mobilePhon)]
        res = []
        users = request.env['funenc.wechat.user'].sudo().search_read(domain=domain)
        if users:
            for user in users:
                val = {
                    'userId': user['user_id'][0],
                    'userName': user['user_id'][1],
                    'userWxId': user['wx_userid'],
                    'userEmployeeId': '',
                    'departId': user['first_department_id'][0],
                    'departName': user['first_department_id'][1],
                }
                res.append(val)
            return json.dumps(res, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getDepartmentData', type='http', auth='public', csrf=False)
    def get_department_data(self, **kwargs):
        '''
        所有部门信息
        :param kwargs:
        :return:
        '''
        domain = []
        data = []
        if kwargs and 'parentDepartId' in kwargs.keys():
            domain.append(('parent_id', '=', int(kwargs['parentDepartId'])))
        else:
            domain.append(('parent_id', '=', False))
        departments = request.env['funenc.wechat.department'].sudo().search_read(domain)
        if departments:
            for department in departments:
                val = {
                    'departId': department['id'],
                    'departName': department['name']
                }
                data.append(val)
            return json.dumps(data, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getOperationDepartmentData', type='http', auth='public', csrf=False)
    def get_operation_department_data(self, **kwargs):
        '''
        所有作业单位部门
        :param kwargs:
        :return:
        '''
        operation = request.env['funenc_wechat.property'].sudo().search([('name', '=', '作业单位')])
        if operation:
            department = request.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                data = self.datetime_handle(department)
                return json.dumps(data, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getWorkshopDepartmentData', type='http', auth='public', csrf=False)
    def get_workshop_department_data(self, **kwargs):
        '''
        所有作业车间部门
        :param kwargs:
        :return:
        '''
        operation = request.env['funenc_wechat.property'].sudo().search([('name', '=', '作业车间')])
        if operation:
            department = request.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                data = self.datetime_handle(department)
                return json.dumps(data)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getMaintenanceDepartmentData', type='http', auth='public', csrf=False)
    def get_maintenance_department_data(self, **kwargs):
        '''
        所有检修班组部门
        :param kwargs:
        :return:
        '''
        operation = request.env['funenc_wechat.property'].sudo().search([('name', '=', '作业工班')])
        if operation:
            department = request.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                data = self.datetime_handle(department)
                return json.dumps(data)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getTrainTypesData', type='http', auth='public', csrf=False)
    def get_train_types_data(self, **kwargs):
        '''
        车辆型号
        :param kwargs:
        :return:
        '''
        data = []
        train_types = request.env['metro_park_base.dev_standard'].sudo().search_read()
        if train_types:
            for tmp_train_type in train_types:
                val = {
                    'vehicleTypeId': tmp_train_type['id'],
                    'vehicleTypeName': tmp_train_type['name'],
                }
                data.append(val)
            return json.dumps(data, ensure_ascii=False)
        return json.dumps('没有找到对应信息', ensure_ascii=False)

    @http.route('/getTrainDevData', type='http', auth='public', csrf=False)
    def get_train_dev_data(self, **kwargs):
        '''
        车辆设备
        :param kwargs:
        :return:
        '''
        domain = []
        if kwargs and 'vehicleTypeId' in kwargs.keys():
            domain.append(('dev_type', '=', int(kwargs['vehicleTypeId'])))
        if kwargs and 'lineId' in kwargs.keys():
            domain.append(('line', '=', int(kwargs['lineId'])))
        data = []
        train_devs = request.env['metro_park_maintenance.train_dev'].sudo().search_read(
            domain, fields=['dev_name', 'dev_no', 'dev_type', 'start_use_time', 'line'])
        for train in train_devs:
            val = {
                'vehicleDeviceNo': train['dev_no'],
                'vehicleName': train['dev_name'],
                'vehicleTypeId': train['dev_type'][0],
                'vehicleTypeName': train['dev_type'][1],
                'startOperationDate': train['start_use_time'].strftime('%Y-%m-%d') if train['start_use_time'] else '',
                'lineId': train['line'][0],
                'lineName': train['line'][1],
            }
            data.append(val)
        return json.dumps(data, ensure_ascii=False)

    @http.route('/getLineData', type='http', auth='public', csrf=False)
    def get_line_data(self, **kwargs):
        '''
        获取线别
        :param kwargs:
        :return:
        '''
        rail_types = request.env['metro_park_base.line'].sudo().search_read(fields=['id', 'name', 'code'])
        return json.dumps(rail_types, ensure_ascii=False)

    @http.route('/getLocationData', type='http', auth='public', csrf=False)
    def get_loction_data(self, **kwargs):
        '''
        厂段信息
        :param kwargs:
        :return:
        '''
        data = []
        domain = []
        if kwargs and 'lineId' in kwargs.keys():
            domain.append(('line', '=', int(kwargs['lineId'])))
        train_devs = request.env['metro_park_base.location'].sudo().search_read(domain)
        for train in train_devs:
            val = {
                'id': train['id'],
                'name': train['name'],
                'lineId': train['line'][0],
            }
            data.append(val)
        return json.dumps(data, ensure_ascii=False)

    @http.route('/getWarehouseData', type='http', auth='public', csrf=False)
    def get_warehouse_data(self, **kwargs):
        '''
        作业区域
        :param kwargs:
        :return:
        '''
        warehouse = request.env['metro_park_base.warehouse'].sudo().search_read(fields=['id', 'name'])
        return json.dumps(warehouse, ensure_ascii=False)

    @http.route('/getRailTypeData', type='http', auth='public', csrf=False)
    def get_rail_type_data(self, **kwargs):
        '''
        作业区域要求
        :param kwargs:
        :return:
        '''
        rail_types = request.env['metro_park_base.rail_type'].sudo().search_read(fields=['id', 'name'])
        return json.dumps(rail_types, ensure_ascii=False)

    @http.route('/getTrainMilesData', type='http', auth='public', csrf=False)
    def get_train_miles_data(self, **kwargs):
        '''
        列车里程公里数
        :param kwargs:
        :return:
        '''
        domain = []
        data = []
        history = request.env['metro_park_maintenance.history_miles']
        _, year, month, day = history.get_year_month_day()
        if kwargs and 'vehicleDeviceNo' not in kwargs.keys():
            return json.dumps('参数 vehicleDeviceNo 车辆设备号必填!', ensure_ascii=False)
        elif kwargs and 'vehicleDeviceNo' in kwargs.keys():
            dev_no = kwargs['vehicleDeviceNo']
        elif kwargs and 'operateDate' in kwargs.keys():
            operateDate = datetime.strptime(kwargs['operateDate'], '%Y-%m-%d')
            year = operateDate.year
            month = operateDate.month
            day = operateDate.day
        operateDatestr = str(year) + '-' + str(month) + '-' + str(day)
        domain.append(('year', '=', year))
        domain.append(('month', '=', month))
        train = request.env['metro_park_maintenance.train_dev'].sudo().search([('dev_no', '=', dev_no)])
        if train:
            domain.append(('train_dev', '=', train.id))
            train_miles = history.sudo().search_read(domain)
            if train_miles:
                for miles in train_miles:
                    val = {
                        'vehicleDeviceNo': kwargs['vehicleDeviceNo'],
                        'operateDate': operateDatestr,
                        'totalMileage': miles['total_miles']
                    }
                    data.append(val)
            return json.dumps(data, ensure_ascii=False)
        return json.dumps('没有对应信息!', ensure_ascii=False)

    @http.route('/getTimeTableData', type='http', auth='public', csrf=False)
    def get_time_table_list_data(self, **kwargs):
        '''
        获取运行图概要
        :return:
        '''
        domain = []
        data = []
        if kwargs and 'operateDate' in kwargs.keys():
            date = datetime.strptime(kwargs['operateDate'], '%Y-%m-%d')
            year = date.year
            month = date.month
            WEEKS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
            # 获取特殊时刻表
            others = request.env['metro_park_dispatch.special_days_config'].sudo().search([])
            # 月初
            year_month = pendulum.datetime(year, month, 1, tz='UTC')
            # 本月天数
            days = year_month.days_in_month
            for day in range(days):
                day_time = pendulum.datetime(year, month, day + 1, tz='UTC')
                day_week = day_time.day_of_week
                day_date = datetime.date(datetime.strptime(day_time.format('YYYY-MM-DD'), '%Y-%m-%d'))
                special_available = \
                    others.filtered(lambda x: x.start_date <= day_date and x.end_date >= day_date)
                if special_available:
                    domain.append(('time_table_id', '=', special_available.time_table.id))
                else:
                    default = request.env['metro_park_dispatch.nor_time_table_config'].sudo().search(
                        [('day_type.name', '=', WEEKS[day_week])])
                    if default:
                        domain.append(('time_table_id', '=', default.time_table.id))

        time_table = request.env['metro_park_base.time_table_data'].sudo().search_read(domain)
        for t in time_table:
            val = {
                'seq': t['train_no'],
                'outSectionId': t['out_location'][0] if t['out_location'] else '',
                'outSectionName': t['out_location'][1] if t['out_location'] else '',
                'outTime': t['plan_out_time'].strftime('%H:%M:%S') if t['plan_out_time'] else '',
                'inSectionId': t['back_location'][0] if t['back_location'] else '',
                'inSectionName': t['back_location'][1] if t['back_location'] else '',
                'inTime': t['plan_in_time'].strftime('%H:%M:%S') if t['plan_in_time'] else '',
                'inPark': t['high_time_train'],
                'runMileage': ''
            }
            data.append(val)
        return json.dumps(data, ensure_ascii=False)

    @http.route('/getTimeTableInformationData', type='http', auth='public', csrf=False)
    def get_time_table_information_data(self):
        '''
        获取所有时刻表 详细信息
        :return:
        '''
        # 时刻表id
        data = []
        time_tables = request.env['metro_park_base.time_table'].sudo().search_read()
        for table in time_tables:
            val = {
                'scheduleTableName': '',
                'scheduleTableNo': table['no'],
                'scheduleTableId': table['id'],
            }
            data.append(val)
        return json.dumps(data, ensure_ascii=False)

    @http.route('/getPlanDataImportWizard/<int:year>', type='http', auth='public', csrf=False)
    def get_plan_data_import_wizard(self, year, **kwargs):
        """
        导出年计划表格
        :param year:
        :param kwargs:
        :return:
        """
        week = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}
        rules = set()
        rule_infos = request.env['metro_park_maintenance.rule_info'] \
            .search([('date', '<=', '%s-12-31' % year), ('date', '>=', '%s-01-01' % year)])
        # 将所有设备号取出，去重排序
        # 取消电客车
        car_type_id = request.env['metro_park_base.dev_type'].search([('name', '=', '电客车')])[0].id
        for i in request.env['metro_park_maintenance.train_dev'].search([('dev_type', '=', car_type_id)]):
            if i.dev_name:
                rules.add(i.dev_name)
        rules = sorted(list(rules))
        #  index 为设备号在表格中的索引
        index = 2
        # 生成设备号的字典，与日期的字典形成坐标系，方便填充数据
        rule_dict = {}
        for i in rules:
            rule_dict[i] = index
            index += 1

        boder = xlwt.Borders()
        boder.left = 1
        boder.right = 1
        boder.top = 1
        boder.bottom = 1
        font = xlwt.Font()
        font.colour_index = i
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                            'font: name 等线,height 180, bold True;')
        style.borders = boder
        alignment = xlwt.Alignment()
        alignment.horz = 2
        alignment.vert = 1
        month_style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                                  'font: name Arial,height 180, bold True;'
                                  'pattern: pattern solid, fore_colour pale_blue;')
        month_boder = xlwt.Borders()
        month_boder.top = 1
        month_style.alignment = alignment
        month_style.borders = month_boder

        week_style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                                 'font: name Arial,height 180, bold True;'
                                 'pattern: pattern solid, fore_colour green;')
        week_style.borders = boder

        rule_style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                                 'font: name Arial,height 180, bold True;'
                                 'pattern: pattern solid, fore_colour pale_blue;')
        rule_style.borders = boder

        date_dict = self.date_dict(year)
        # 为表格添加边框
        for row in range(len(rules) + 6):
            if len(rules) + 3 == row:
                continue
            for col in range(len(date_dict.items()) + 1):
                table.write_merge(col, col, row, row, '', style)
        # 初始化表格
        table.write_merge(0, 0, 0, 0, '日期', style)
        table.write_merge(0, 0, 1, 1, '星期', style)
        table.write_merge(0, 0, 2, 2, '天数', style)
        for key, value in date_dict.items():
            table.write_merge(value, value, 0, 0, key, style)
            weekday = datetime.weekday(datetime.strptime(key, '%Y/%m/%d'))
            if week[weekday] in ['六', '日']:
                table.write_merge(value, value, 1, 1, week[weekday], week_style)
            else:
                table.write_merge(value, value, 1, 1, week[weekday], style)
            table.write_merge(value, value, 2, 2, date_dict[key], style)
        for key, value in rule_dict.items():
            table.write_merge(0, 0, value + 1, value + 1, key, rule_style)
        # 根据建立的坐标系填充数据
        day_summary = {}
        month_summary = {}
        for i in rule_infos:
            if datetime.strftime(i.date, "%Y/%m/%d") in day_summary:
                day_summary[datetime.strftime(i.date, "%Y/%m/%d")] += 1
            else:
                day_summary[datetime.strftime(i.date, "%Y/%m/%d")] = 1

            date_key = datetime.strftime(i.date, "%Y/%m/%d").split('/')[1]
            if month_summary.get(date_key):
                if month_summary[date_key].get(i.rule.no):
                    month_summary[date_key][i.rule.no] += 1
                else:
                    month_summary[date_key][i.rule.no] = 1
            else:
                month_summary[date_key] = {i.rule.no: 1}
            table.write_merge(date_dict[datetime.strftime(i.date, "%Y/%m/%d")],
                              date_dict[datetime.strftime(i.date, "%Y/%m/%d")],
                              rule_dict[i.dev.dev_name] + 1 if i.dev else "",
                              rule_dict[i.dev.dev_name] + 1 if i.dev else "", i.rule.no, style)
        # 初始化月份，合并单元格，智能判断过于麻烦，这里直接写死
        table.write_merge(1, 31, len(rules) + 3, len(rules) + 3, '1', month_style)  # 1月
        table.write_merge(32, 59, len(rules) + 3, len(rules) + 3, '2', month_style)  # 2月
        table.write_merge(60, 90, len(rules) + 3, len(rules) + 3, '3', month_style)  # 3月
        table.write_merge(91, 120, len(rules) + 3, len(rules) + 3, '4', month_style)  # 4月
        table.write_merge(121, 151, len(rules) + 3, len(rules) + 3, '5', month_style)  # 5月
        table.write_merge(152, 181, len(rules) + 3, len(rules) + 3, '6', month_style)  # 6月
        table.write_merge(182, 212, len(rules) + 3, len(rules) + 3, '7', month_style)  # 7月
        table.write_merge(213, 243, len(rules) + 3, len(rules) + 3, '8', month_style)  # 8月
        table.write_merge(244, 273, len(rules) + 3, len(rules) + 3, '9', month_style)  # 9月
        table.write_merge(274, 304, len(rules) + 3, len(rules) + 3, '10', month_style)  # 10月
        table.write_merge(305, 334, len(rules) + 3, len(rules) + 3, '11', month_style)  # 11月
        table.write_merge(335, 365, len(rules) + 3, len(rules) + 3, '12', month_style)  # 12月
        table.write_merge(0, 0, len(rules) + 4, len(rules) + 4, '统计', style)
        table.write_merge(0, 0, len(rules) + 5, len(rules) + 5, '月统计', style)
        # 获取每天的统计数量
        for key, value in day_summary.items():
            table.write_merge(date_dict[key],
                              date_dict[key],
                              len(rules) + 4,
                              len(rules) + 4, value, style)
        # 获取月计划合计
        for summary_key, summary_val in month_summary.items():
            month_summary[summary_key]['合计'] = 0
            for site_key, site_val in summary_val.items():
                if site_key == '合计':
                    break
                month_summary[summary_key]['合计'] += site_val
        for month_key, month_val in month_summary.items():
            month_site = date_dict[str(year) + '/' + month_key + '/' + '01']
            repairing = 0
            for plan_key, plan_val in month_val.items():
                table.write_merge(month_site + repairing,
                                  month_site + repairing,
                                  len(rules) + 5,
                                  len(rules) + 5, plan_key, style)
                repairing_val = repairing + 1
                table.write_merge(month_site + repairing + 1,
                                  month_site + repairing + 1,
                                  len(rules) + 5,
                                  len(rules) + 5, plan_val, style)
                repairing = repairing_val + 1
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '%s年生产计划.xls' % year
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    def date_dict(self, year, month=None):
        """
        生成当年所有日期的字典，key为日期，value为在表格中的位置
        :param year:
        :param month:
        :return:
        """
        if month:
            if len(month) == 1:
                month = '0' + month
            start_time = '%s/%s/01' % (year, month)
            end_time = '%s/%s/31' % (year, month)
        else:
            start_time = '%s/01/01' % year
            end_time = '%s/12/31' % year
        date_dict = {}
        dt = datetime.strptime(start_time, "%Y/%m/%d")
        date = start_time[:]
        index = 1
        while date <= end_time:
            date_dict[date] = index
            index += 1
            dt = dt + timedelta(1)
            date = dt.strftime("%Y/%m/%d")
        return date_dict

    @http.route('/get_miles_export_wizard/<string:year>/<string:month>', type='http', auth='public', csrf=False)
    def get_miles_export_wizard(self, year, month, **kwargs):
        """
        导出公里数统计表
        :param year:
        :param month:
        :param kwargs:
        :return:
        """
        # 当月所有日期
        date_dict = self.date_dict(year, month=month)
        # 获取当月内的所有公里数记录
        year = int(year)
        month = int(month)
        start_date = pendulum.date(year, month, 1)
        week_day, month_count_day = calendar.monthrange(year, month)
        end_date = pendulum.date(year, month, month_count_day)
        domain = [('date', '>=', start_date), ('date', '<=', end_date)]
        vehicle_datas = request.env['funenc.tcms.vehicle.data'].search(domain)
        if not vehicle_datas:
            return json.dumps({'status': 400, 'error': '本月数据为空！'}, ensure_ascii=False)

        # 获取所有车辆信息
        vehicle_list = set()
        for vehicle_data in vehicle_datas:
            if vehicle_data.name:
                vehicle_list.add(vehicle_data.name)
        vehicle_list = sorted(list(vehicle_list))
        vehicle_len = len(vehicle_list)    # 列表总长度

        # 封装一个含有所有信息的字典
        vehicle_table = dict()
        for vehicle in vehicle_list:
            for key, value in date_dict.items():
                for vehicle_data in vehicle_datas:
                    if vehicle == vehicle_data.name and key == vehicle_data.date.strftime('%Y/%m/%d'):
                        vehicle_table["{}_{}_1".format(vehicle, key)] = vehicle_data.traction_consumption
                        vehicle_table["{}_{}_2".format(vehicle, key)] = vehicle_data.auxiliary_consumption
                        vehicle_table["{}_{}_3".format(vehicle, key)] = vehicle_data.regeneration_consumption
                        vehicle_table["{}_{}_4".format(vehicle, key)] = vehicle_data.total_mileage
                        vehicle_table["{}_{}_5".format(vehicle, key)] = vehicle_data.today_mileage

        # 生成设备号的字典
        vehicle_dict = {}
        index = 1
        for vehicle in vehicle_list:
            vehicle_dict[index] = vehicle
            index += 1

        file = xlwt.Workbook()
        boder = xlwt.Borders()
        boder.left = 1
        boder.right = 1
        boder.top = 1
        boder.bottom = 1
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                            'font: name 宋体,height 180, bold True;')
        style.borders = boder

        # 初始化表格
        table.write_merge(0, 0, 0, 0, "车号 \ 日期", style)
        # 第一行写入日期以及标题
        col_list = ["牵引能耗", "辅助能耗", "再生能耗", "公里数", "当日里程"]
        col_num = 1  # 列
        for key, value in date_dict.items():
            for col in col_list:
                table.write_merge(0, 0, col_num, col_num, key, style)
                table.write_merge(1, 1, col_num, col_num, col, style)
                col_num += 1

        # 第二行开始写入数据
        row_num = 2         # 从下标2行开始写入
        vehice_index = 1    # 车辆index
        col_index = 1       # 每行中的列 每写入一个单元格后+1，直到改行结束，恢复为1
        while vehice_index <= vehicle_len:
            vehicle = vehicle_dict[vehice_index]  # 车辆号
            table.write_merge(row_num, row_num, 0, 0, vehicle, style)   # 写入车辆号
            table_line = 1   # 用于判断1-5的单元格，分别写入col_list的值
            for key, value in date_dict.items():
                for col in col_list:
                    if table_line > 5:
                        table_line = 1
                    result = vehicle_table.get("{}_{}_{}".format(vehicle, key, table_line))  # 拼接字典key
                    if not result:
                        table.write_merge(row_num, row_num, col_index, col_index, "", style)
                    else:
                        table.write_merge(row_num, row_num, col_index, col_index, result, style)
                    table_line += 1
                    col_index += 1
            col_index = 1
            vehice_index += 1
            row_num += 1
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '{}年{}月公里数统计表.xls'.format(year, month)
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}".format(name.encode().decode('latin-1'))
        return response

    @http.route('/funenc_tcms_vehicle_data_export', type='http', auth='public', csrf=False)
    def funenc_tcms_vehicle_data_export(self, **kwargs):
        """
        导出公里数统计表
        :param year:
        :param month:
        :param kwargs:
        :return:
        """
        """
        导出公里数统计表
        :param year:
        :param month:
        :param kwargs:
        :return:
        """
        dev_info_miles = request.env['funenc.tcms.vehicle.data'].search_read([])
        if dev_info_miles:
            # 生成设备号的字典，与日期的字典形成坐标系，方便填充数据
            file = xlwt.Workbook()
            table = file.add_sheet('sheet', cell_overwrite_ok=True)
            style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                                'font: name 宋体,height 180, bold True;')
            field_key = ['date', 'update_time', 'name', 'today_mileage', 'total_mileage', 'traction_consumption',
                         'auxiliary_consumption', 'regeneration_consumption']
            field_val = ['日期', '更新时间', '车辆号', '当日里程', '公里数', '牵引能耗', '辅助能耗', '再生能耗']
            for key, value in enumerate(field_val):
                table.write_merge(0, 0, key, key, value, style)
            # 根据建立的坐标系填充数据
            for info_key, info_val in enumerate(dev_info_miles):
                for field_k, field_va in enumerate(field_key):
                    if field_va == 'date':
                        val = datetime.strftime(info_val.get(field_va), '%Y-%m-%d')
                        table.write_merge(info_key + 1, info_key + 1, field_k, field_k, val, style)
                    elif field_va == 'update_time':
                        val = datetime.strftime(
                            info_val.get(field_va)
                            + timedelta(hours=8), '%Y-%m-%d %H:%M:%S')
                        table.write_merge(info_key + 1, info_key + 1, field_k, field_k, val, style)
                    else:
                        table.write_merge(info_key + 1, info_key + 1, field_k, field_k, info_val.get(field_va), style)

            fp = io.BytesIO()
            file.save(fp)
            fp.seek(0)
            data = fp.read()
            fp.close()
            name = '车辆历史公里数.xls'
            response = request.make_response(data)
            response.headers['Content-Type'] = 'application/vnd.ms-excel'
            response.headers["Content-Disposition"] = "attachment; filename={}". \
                format(name.encode().decode('latin-1'))
            return response

        else:
            return json.dumps({'status': 400, 'error': '数据为空'}, ensure_ascii=False)

    @http.route('/metro_park_maintenance/get_year_plan_template', type='http', auth="user")
    def get_year_plan_template(self, **kwargs):
        '''
        取得年计划模板
        :param token:
        :return:
        '''
        app_dir = os.path.dirname(os.path.dirname(__file__))
        workbook = xlrd.open_workbook(app_dir + "/static/templates/year_plan_template.xls")
        name = 'attachment; filename=年计划(模板).xls'.encode().decode('latin-1')
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition', name)])
        new_excel = copy(workbook)
        new_excel.save(response.stream)
        return response

    @http.route('/metro_park_maintenance/get_month_plan_template', type='http', auth="user")
    def get_month_plan_template(self, **kwargs):
        '''
        打开文件并保存然后下载
        :param token:
        :return:
        '''
        app_dir = os.path.dirname(os.path.dirname(__file__))
        workbook = xlrd.open_workbook(app_dir + "/static/templates/month_plan_template.xls")
        name = 'attachment; filename=月计划(模板).xls'.encode().decode('latin-1')
        response = request.make_response(None,
                                         headers=[('Content-Type', 'application/vnd.ms-excel'),
                                                  ('Content-Disposition', name)])
        new_excel = copy(workbook)
        new_excel.save(response.stream)
        return response

    @http.route('/export_day_plan/<int:day_plan_id>', type='http', auth='public', csrf=False)
    def get_day_plan_data(self, *args, **kwargs):
        """
        导出日计划表格
        :param date: 传递过来的时间
        :return:
        """
        day_plan_id = kwargs.get('day_plan_id')
        day_plan = http.request.env['metro_park_maintenance.day_plan'].browse(day_plan_id)
        plan_date = day_plan.plan_date

        file = xlwt.Workbook()
        cell_border = xlwt.Borders()
        cell_border.left = 1
        cell_border.right = 1
        cell_border.top = 1
        cell_border.bottom = 1
        table = file.add_sheet('sheet', cell_overwrite_ok=True)

        style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                            'font: name 宋体, height 200, bold True')
        style.borders = cell_border

        # 车号
        table.col(0).width = 256 * 12
        # 作业时间
        table.col(1).width = 256 * 20
        # 作业内容
        table.col(2).width = 256 * 20
        # 作业备注
        table.col(3).width = 256 * 35
        # 作业场段
        table.col(4).width = 256 * 15
        # 回库场段
        table.col(5).width = 256 * 15
        # 次日作业
        table.col(6).width = 256 * 12
        # 作业地点
        table.col(7).width = 256 * 12
        # 段内作业要求
        table.col(8).width = 256 * 12
        # 检修人员
        table.col(9).width = 256 * 15
        # 修程
        table.col(10).width = 256 * 15
        # 车辆状态
        table.col(11).width = 256 * 15
        # 备注
        table.col(12).width = 256 * 52

        # 标题
        plan_date_str = pendulum.parse(str(day_plan.plan_date)).format('YYYY-MM-DD')
        table.write_merge(0, 1, 0, 12, "运营二分公司检修四车间日生产计划  {plan_date}".format(
            plan_date=plan_date_str), style)

        table.row(0).height_mismatch = True
        table.row(0).height = 256 * 2

        cur_row = 2
        table.write_merge(cur_row, cur_row, 0, 0, '车号', style)
        table.write_merge(cur_row, cur_row, 1, 1, '作业时间', style)
        table.write_merge(cur_row, cur_row, 2, 2, '作业内容', style)
        table.write_merge(cur_row, cur_row, 3, 3, '作业备注', style)
        table.write_merge(cur_row, cur_row, 4, 4, '作业场段', style)
        table.write_merge(cur_row, cur_row, 5, 5, '回库场段', style)
        table.write_merge(cur_row, cur_row, 6, 6, '次日作业', style)
        table.write_merge(cur_row, cur_row, 7, 7, '作业地点', style)
        table.write_merge(cur_row, cur_row, 8, 8, '段内作业需求', style)
        table.write_merge(cur_row, cur_row, 9, 9, '检修人员', style)
        table.write_merge(cur_row, cur_row, 10, 10, '修程', style)
        table.write_merge(cur_row, cur_row, 11, 11, '车辆状态', style)
        table.write_merge(cur_row, cur_row, 12, 12, '备注', style)

        table.row(cur_row).height_mismatch = True
        table.row(cur_row).height = 256 * 2
        cur_row = cur_row + 1

        # 修程
        rule_infos = request.env['metro_park_maintenance.rule_info'].search(
            [('plan_id', '=', 'metro_park_maintenance.day_plan, {plan_id}'.format(plan_id=day_plan_id))])
        # 通过设备进行分组
        dev_rule_cache = dict()
        for rule_info in rule_infos:
            if rule_info.dev:
                dev_rule_cache.setdefault(rule_info.dev.dev_no, []).append(rule_info)

        for dev_no in dev_rule_cache:
            rule_infos = dev_rule_cache[dev_no]
            table.write_merge(cur_row, cur_row + len(rule_infos) - 1, 0, 0, dev_no, style)
            for rule_info in rule_infos:
                # 作业时间
                table.write_merge(cur_row, cur_row, 1, 1, "{work_time}".format(work_time=rule_info.work_time), style)

                # 规程
                table.write_merge(cur_row, cur_row, 2, 2, rule_info.rule_name if rule_info.rule_name else "——", style)

                # 作业备注, 正线运营将作业车次放进去
                if rule_info.rule_name == '正线运营':
                    table.write_merge(cur_row, cur_row, 3, 3, rule_info.train_no, style)
                else:
                    table.write_merge(cur_row, cur_row, 3, 3, rule_info.remark if rule_info.remark else "——", style)

                # 作业场段
                table.write_merge(
                    cur_row, cur_row, 4, 4, rule_info.rail.location.name if rule_info.rail.location.name else '——',
                    style)

                # 回库场段
                table.write_merge(
                    cur_row, cur_row, 5, 5, rule_info.next_day_work_location.name if
                    rule_info.next_day_work_location else '——', style)

                # 次日作业
                table.write_merge(cur_row, cur_row, 6, 6,
                                  get_many2many_content(
                                      rule_info.next_day_work, 'rule_name') if rule_info.rule else "——", style)
                # 作业地点
                table.write_merge(cur_row, cur_row, 7, 7, "——", style)

                # 段内作业需求
                table.write_merge(cur_row, cur_row, 8, 8,
                                  get_many2many_content(
                                      rule_info.rule.work_requirement, 'name') if rule_info.rule else "——", style)
                # 检修人员
                table.write_merge(cur_row, cur_row, 9, 9,
                                  rule_info.work_class.name if rule_info.work_class else "——", style)

                # 修程
                if rule_info.rule:
                    if rule_info.rule.target_plan_type in ['year']:
                        table.write_merge(cur_row, cur_row, 10, 10,
                                          "计划性检修", style)
                    elif rule_info.rule_name in ['里程检', '登顶', '洗车']:
                        table.write_merge(cur_row, cur_row, 10, 10, "常规性检修", style)
                    else:
                        table.write_merge(cur_row, cur_row, 10, 10, "", style)
                else:
                    table.write_merge(cur_row, cur_row, 10, 10, "——", style)

                # 车辆状态
                table.write_merge(cur_row, cur_row, 11, 11, "", style)

                # 作业备注
                table.write_merge(cur_row, cur_row, 12, 12, "", style)

                # 设置行高
                table.row(cur_row).height_mismatch = True
                table.row(cur_row).height = 256 * 2

                cur_row += 1

        # table.write_merge(2, len(rules) + 1, 12, 12, "", style)
        table.write_merge(cur_row, cur_row, 0, 0, "值班情况", style)
        table.write_merge(cur_row, cur_row, 1, 5, "白班值班情况：", style)
        table.write_merge(cur_row, cur_row, 6, 12, "夜班值班情况：", style)
        table.row(cur_row).height_mismatch = True
        table.row(cur_row).height = 256 * 2

        cur_row = cur_row + 1
        table.write_merge(cur_row, cur_row, 0, 0, "安全告知", style)
        table.write_merge(cur_row, cur_row, 1, 12, "班组使用五防系统操作隔离开关时，请加强监护，规范操作，"
                                                   "库内作业请注意安全,加强库内安全巡查。", style)
        table.row(cur_row).height_mismatch = True
        table.row(cur_row).height = 256 * 2

        # 编制、审核行
        cur_row = cur_row + 1
        table.write_merge(cur_row, cur_row, 0, 1, "", style)
        table.write_merge(cur_row, cur_row, 2, 3, "编制：", style)
        table.write_merge(cur_row, cur_row, 4, 5, "", style)
        table.write_merge(cur_row, cur_row, 6, 8, "审核：", style)
        table.write_merge(cur_row, cur_row, 9, 11, "", style)
        table.write_merge(cur_row, cur_row, 12, 12, "", style)
        table.row(cur_row).height_mismatch = True
        table.row(cur_row).height = 256 * 2

        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '日生产计划%s.xls' % plan_date
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @http.route('/export_month_plan/<int:month_plan_id>', type='http', auth='public', csrf=False)
    def get_month_plan_data(self, *args, **kwargs):
        """
        导出月计划
        :param date:
        :return:
        """
        month_plan_id = kwargs.get('month_plan_id', None)
        if not month_plan_id:
            raise Exception('参数错误')
        month_plan = http.request.env['metro_park_maintenance.month_plan'].browse(month_plan_id)
        weeks = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 0: '日'}
        devs = set()
        rule_infos = request.env['metro_park_maintenance.rule_info'].search(
            [('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(plan_id=month_plan_id))])
        # 将所有设备号取出，去重排序
        for info in rule_infos:
            devs.add(info.dev.dev_no)
        devs = sorted(list(devs))

        import os
        base_path = os.path.dirname(os.path.dirname(__file__))
        template_excel = xlrd.open_workbook(
            os.path.join(base_path, 'static/templates/month_plan_template.xls'), formatting_info=True)
        new_excel = copy(template_excel)
        sheet = new_excel.get_sheet(0)

        style = xlwt.easyxf('alignment: horizontal center, vertical center, wrap True;'
                            'font: name 宋体, height 280;')

        borders = xlwt.Borders()
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        style.borders = borders

        day = pendulum.date(month_plan.year, month_plan.month, 1)
        days = day.days_in_month
        title_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体, height 480;')
        title = '{year}年{month}月运营二分公司车辆检修四车间10号线生产计划'.format(
            year=month_plan.year, month=month_plan.month)
        sheet.write_merge(0, 0, 1, days, title, title_style)
        sheet.write_merge(1, 2, 0, 0, '车号/日期', style)

        # 生成设备号的字典
        row_index = 3
        dev_row_index_dict = {}
        for dev_no in devs:
            dev_row_index_dict[dev_no] = row_index
            for col in range(0, 32):
                sheet.write(row_index, col, '', style)
            row_index += 1

        # 初始化表格
        for day in range(1, days + 1):
            # 写入天
            sheet.write_merge(1, 1, day, day, day, style)
            # 写入周
            sheet.write_merge(2, 2, day, day, weeks[pendulum.date(
                month_plan.year, month_plan.month, day).day_of_week], style)

        # 写入设备编号
        for key in dev_row_index_dict:
            sheet.write_merge(dev_row_index_dict[key], dev_row_index_dict[key], 0, 0, key, style)

        # 填充数据
        for record in rule_infos:
            if record.rule:
                sheet.write_merge(dev_row_index_dict[record.dev.dev_no], dev_row_index_dict[record.dev.dev_no],
                                  record.day, record.day, record.rule.no, style)

        # 清除多余的列
        for day in range(days, 32):
            sheet.write(1, day, '', style)
            sheet.write(2, day, '', style)

        fp = io.BytesIO()
        new_excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '月生产计划{}年{}月.xls'.format(month_plan.year, month_plan.month)
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @http.route('/GetTrainDevImportExcel', type='http', auth='public', csrf=False)
    def get_train_dev_import_excel(self, *args, **kwargs):
        file = xlwt.Workbook()
        table = file.add_sheet('sheet', cell_overwrite_ok=True)
        style = xlwt.easyxf('alignment: horizontal center, vertical center,wrap True;'
                            'font: name 宋体,height 180, bold True;')
        # 初始化表格
        table.write_merge(0, 0, 0, 0, '设备名称', style)
        table.write_merge(0, 0, 1, 1, '设备编码', style)
        table.write_merge(0, 0, 2, 2, '批次号', style)
        table.write_merge(0, 0, 3, 3, '所属专业', style)
        table.write_merge(0, 0, 4, 4, '位置', style)
        table.write_merge(0, 0, 5, 5, '线别', style)
        table.write_merge(0, 0, 6, 6, '线段', style)
        table.write_merge(0, 0, 7, 7, '设备类型', style)
        table.write_merge(0, 0, 8, 8, '型号规格', style)
        table.write_merge(0, 0, 9, 9, '资产名称', style)
        fp = io.BytesIO()
        file.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '车辆设备导入.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))
        return response

    @http.route('/export_produce_plan/<int:export_wizard_id>', type='http', auth='public', csrf=False)
    def export_produce_plan(self, *args, **kwargs):
        """
        导出月计划
        :param date:
        :return:
        """
        wizard_id = kwargs.get("export_wizard_id", False)
        model = http.request.env["metro_park_maintenance.export_produce_plan_wizard"]
        record = model.browse(wizard_id)

        info_model = http.request.env["metro_park_maintenance.rule_info"]

        start_year = record.start_year.val
        start_month = record.start_month.val

        end_year = record.end_year.val
        end_month = record.end_month.val

        start_date = pendulum.date(start_year, start_month, 1)
        end_date = pendulum.date(end_year, end_month, 1)
        end_date = pendulum.date(end_year, end_month, end_date.days_in_month)
        infos = info_model.search(
            [('date', '>=', start_date.format('YYYY-MM-DD')),
             ('date', '<=', end_date.format('YYYY-MM-DD')),
             ('data_source', '=', 'week')], order="date asc")

        balance_rules = model.env["metro_park_maintenance.repair_rule"].search(
            [('target_plan_type', '=', 'year')])
        balance_rule_ids = balance_rules.ids

        rule_cache = {}
        color_cell = {}
        for info in infos:
            key = "{dev_id}_{date}".format(dev_id=info.dev.id, date=info.date)
            rule_cache.setdefault(key, []).append(info.rule.no)
            if info.rule.id in balance_rule_ids:
                color_cell[key] = True

        dev_type_electric_train = model.env.ref('metro_park_base.dev_type_electric_train')
        devs = model.env["metro_park_maintenance.train_dev"].search(
            [('dev_type', '=', dev_type_electric_train.id)], order='dev_no asc')
        dev_ids = devs.ids

        import os
        base_path = os.path.dirname(os.path.dirname(__file__))
        template_excel = xlrd.open_workbook(
            os.path.join(base_path, 'static/templates/produce_template.xls'), formatting_info=True)
        new_excel = copy(template_excel)
        sheet = new_excel.get_sheet(0)

        weeks = ['日', '一', '二', '三', '四', '五', '六']

        border = xlwt.Borders()
        border.left = 1
        border.right = 1
        border.top = 1
        border.bottom = 1
        month_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 280;')
        month_style.borders = border
        cell_style = xlwt.easyxf('alignment: horizontal center, vertical center, wrap True; font: name 宋体')
        cell_style.borders = border

        # add new colour to palette and set RGB colour value
        xlwt.add_palette_colour("custom_colour", 0x21)
        new_excel.set_colour_RGB(0x21, 255, 0, 0)
        color_cell_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体; '
            'pattern: pattern solid, fore_colour custom_colour')
        color_cell_style.borders = border

        # 先写月份
        cur_row = 5
        while start_date < end_date:
            sheet.write_merge(cur_row, cur_row, 0, len(devs) + 1, start_date.format('YYYY年MM月'), month_style)
            days = start_date.days_in_month
            for day in range(1, days + 1):
                tmp_date = start_date.add(days=day - 1)
                cur_row += 1
                sheet.write(cur_row, 0, str(day), cell_style)
                sheet.write(cur_row, 1, str(weeks[tmp_date.day_of_week]), cell_style)
                for col in range(2, len(devs) + 2):
                    dev_id = dev_ids[col - 2]
                    key = '{dev_id}_{date}'.format(dev_id=dev_id, date=tmp_date.format('YYYY-MM-DD'))
                    rules = rule_cache.get(key, [])
                    rule_txt = ''.join(rules)
                    if color_cell.get(key, False):
                        sheet.write(cur_row, col, rule_txt, color_cell_style)
                    else:
                        sheet.write(cur_row, col, rule_txt, cell_style)
                sheet.row(cur_row).height_mismatch = True
                sheet.row(cur_row).height = 256 * 2

            start_date = start_date.add(months=1)
            cur_row += 1

        fp = io.BytesIO()
        new_excel.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '生产计划.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))

        return response

    @http.route('/export_week_plan/<int:week_plan_id>', type='http', auth='public', csrf=False)
    def export_week_plan(self, *args, **kwargs):
        '''
        导出周计划
        :param args:
        :param kwargs:
        :return:
        '''
        week_plan_id = kwargs.get("week_plan_id", False)
        week_plan = \
            http.request.env['metro_park_maintenance.week_plan'].browse(week_plan_id)

        info_model = \
            http.request.env["metro_park_maintenance.rule_info"]
        # 取得本周的所有数据
        infos = info_model.search(
            [('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'.format(
                plan_id=week_plan_id))], order='date asc')

        # 取得本周和本周之前的数据
        start_date = pendulum.parse(str(week_plan.start_date)).subtract(days=10)
        end_date = pendulum.parse(str(week_plan.end_date))
        tmp_infos = info_model.search(
            [('data_source', '=', 'week'),
             ('date', '>=', start_date.format('YYYY-MM-DD')), ('date', '<=', end_date.format('YYYY-MM-DD'))])
        all_infos = infos + tmp_infos
        date_rule_cache = {'{date}_{rule_id}'.format(
            date=info.date, rule_id=info.rule.id): True for info in all_infos}
        compute_name_cache = {}
        for info in infos:
            if not info.rule:
                continue
            repair_days = 0
            tmp_date = pendulum.parse(str(info.date))
            key = '{date}_{rule_id}'.format(date=tmp_date.format('YYYY-MM-DD'), rule_id=info.rule.id)
            while key in date_rule_cache:
                repair_days += 1
                tmp_date = tmp_date.subtract(days=1)
                key = '{date}_{rule_id}'.format(date=tmp_date.format('YYYY-MM-DD'),
                                                rule_id=info.rule.id)
            if repair_days > 1:
                compute_name_cache[info.id] = "{name}(第{day}天)".format(name=info.rule.name, day=repair_days)
            else:
                compute_name_cache[info.id] = "{name}".format(name=info.rule.name)

        mile_work_class_info = week_plan.mile_work_class_info
        work_class_info_cache = {
            str(info.date): info.work_class_name for info in mile_work_class_info}
        remark_cache = {str(info.date): info.remark for info in mile_work_class_info}
        # 先按日期分组
        data_cache = dict()
        for info in infos:
            data_cache.setdefault(str(info.date), []).append(info)

        # 再每个分组里去进行处理
        groups = {}
        for key in data_cache:
            infos = data_cache[key]
            sub_groups = dict()
            groups[key] = sub_groups
            for info in infos:
                # 按修程、工班、作业区域来分组, 里程\\综合工班轮换着来
                rule_name = compute_name_cache.get(info.id, "")
                if info.work_class_name:
                    work_class = info.work_class_name
                else:
                    work_class = work_class_info_cache[str(info.date)]
                # 作业地点是根据工班来决定的
                if info.work_class_location:
                    locations = [info.work_class_location.name]
                else:
                    locations = ['板桥车辆段', '高大路停车场']

                locations = '/'.join(locations)
                total_key = '{rule_name}_{work_class}_{locations}'.format(
                    rule_name=rule_name,
                    work_class=work_class,
                    locations=locations)
                sub_groups.setdefault(total_key, []).append(info)

        # 输出excel
        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet('修次', cell_overwrite_ok=True)

        border = xlwt.Borders()
        border.left = 1
        border.right = 1
        border.top = 1
        border.bottom = 1
        month_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 280;')
        month_style.borders = border

        cell_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体, height 200;')
        cell_style.borders = border

        cell_end_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体, height 200;')

        title_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 240, bold True; ')
        title_style.borders = border

        xlwt.add_palette_colour("custom_colour", 0x21)
        work_book.set_colour_RGB(0x21, 255, 0, 0)
        color_cell_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体; '
            'pattern: pattern solid, fore_colour custom_colour')
        color_cell_style.borders = border

        # 写入标题
        cur_row = 0
        start_date = pendulum.parse(str(week_plan.start_date))
        end_date = pendulum.parse(str(week_plan.end_date))
        title = '运营二分公司车辆检修四车间10号线周生产计划({start_date}-{end_date})'.format(
            start_date=start_date.format('MM.DD'), end_date=end_date.format('MM.DD'))
        sheet.row(cur_row).height_mismatch = True
        sheet.row(cur_row).height = 500
        sheet.write_merge(cur_row, 0, cur_row, 7, title, title_style)

        # 写入序号
        cur_row = cur_row + 1
        table_no = pendulum.today().format("编号YYYYMMDD   ")
        table_no_style = xlwt.easyxf(
            'alignment: horizontal right, vertical center, wrap True; font: name 宋体, height 160;')
        table_no_style.borders = border
        sheet.row(cur_row).height_mismatch = True
        sheet.row(cur_row).height = 400
        sheet.write_merge(cur_row, cur_row, 0, 7, table_no, table_no_style)

        # 写入列头
        cur_row = cur_row + 1
        sheet.write(cur_row, 0, "日期", cell_style)
        sheet.write_merge(cur_row, cur_row, 1, 2, "工作内容", cell_style)
        sheet.write(cur_row, 3, "列车/设备号", cell_style)
        sheet.write(cur_row, 4, "作业区域", cell_style)
        sheet.write(cur_row, 5, "作业人", cell_style)
        sheet.write(cur_row, 6, "备注", cell_style)
        sheet.write(cur_row, 7, "其它", cell_style)
        sheet.row(cur_row).height_mismatch = True
        sheet.row(cur_row).height = 400

        sheet.col(0).width = 256 * 15
        sheet.col(1).width = 256 * 15
        sheet.col(2).width = 256 * 20
        sheet.col(3).width = 256 * 50
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20
        sheet.col(7).width = 256 * 20

        # 循环输入每个大项
        start_row = cur_row + 1

        weeks = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
        for key in groups:
            tmp_date = pendulum.parse(key)
            sub_groups = groups[key]
            rows = len(sub_groups) or 1

            sub_row = start_row
            for sub_key in sub_groups:
                infos = sub_groups[sub_key]

                tmp_ar = sub_key.split('_')
                rule_no = tmp_ar[0]
                work_class = tmp_ar[1]
                location = tmp_ar[2]

                trains = []
                for info in infos:
                    trains.append(info.dev_no)

                train_names = ','.join(trains)
                sheet.write(sub_row, 2, rule_no, cell_style)
                sheet.write(sub_row, 3, train_names, cell_style)
                sheet.write(sub_row, 4, location, cell_style)
                sheet.write(sub_row, 5, work_class, cell_style)
                sheet.write(sub_row, 6, "------", cell_style)
                sheet.write(sub_row, 7, "", cell_style)
                sheet.write(sub_row, 8, "", cell_end_style)

                sheet.row(sub_row).height_mismatch = True
                sheet.row(sub_row).height = 600

                sub_row += 1

            # 写入日期
            date_str = '{date}\n({week_name})'.format(
                date=tmp_date.format("YYYY-MM-DD"),
                week_name=weeks[tmp_date.day_of_week])

            sheet.write_merge(start_row, start_row + rows - 1, 0, 0, date_str, cell_style)
            sheet.write_merge(start_row, start_row + rows - 1, 1, 1, "电客车", cell_style)

            # 合并备注栏
            remark = remark_cache[tmp_date.format('YYYY-MM-DD')]
            sheet.write_merge(start_row, start_row + rows - 1, 7, 7, remark, cell_style)
            start_row = start_row + rows

        # 写入最后两行
        sheet.write(start_row, 0, "备注", cell_style)

        remark = '''
        1、场段施工计划涉及大区停电详见施工调度系统以及施工类交办表；
        2、加强调度正线故障应急处置能力、信息报送能力；
        3、加强电客车洗车周期卡控，严格按规章制度执行，异常情况及时上报；
        4、加强现场检查管理工作，卡控安全注意事项；
        '''
        footer_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体, height 200, bold True;')
        footer_style.borders = border
        sheet.write_merge(start_row, start_row, 1, 7, remark, footer_style)
        sheet.row(start_row).height_mismatch = True
        sheet.row(start_row).height = 1600
        start_row += 1

        sheet.write(start_row, 0, '编制:', cell_style)
        sheet.write_merge(start_row, start_row, 1, 3, '', cell_style)
        sheet.write(start_row, 4, "审批:", cell_style)
        sheet.write_merge(start_row, start_row, 5, 7, '', cell_style)
        sheet.row(start_row).height_mismatch = True
        sheet.row(start_row).height = 600
        start_row += 1

        sheet.write(start_row, 0, '时间:', cell_style)
        sheet.write_merge(start_row, start_row, 1, 3, '', cell_style)
        sheet.write(start_row, 4, "审批:", cell_style)
        sheet.write_merge(start_row, start_row, 5, 7, '', cell_style)
        sheet.row(start_row).height_mismatch = True
        sheet.row(start_row).height = 600
        start_row += 1

        fp = io.BytesIO()
        work_book.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '{year}年第{week}周计划.xls'.format(year=week_plan.year, week=week_plan.week)
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))

        return response

    @http.route('/export_balance_offset', type='http', auth='public', csrf=False)
    def export_balance_offset(self, *args, **kwargs):
        '''
        导出偏移
        :param args:
        :param kwargs:
        :return:
        '''
        # 取得数据
        records = http.request.env["metro_park_maintenance.balance_rule_offset"].search([])

        # 输出excel
        work_book = xlwt.Workbook()
        sheet = work_book.add_sheet('修次', cell_overwrite_ok=True)

        border = xlwt.Borders()
        border.left = 1
        border.right = 1
        border.top = 1
        border.bottom = 1
        month_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 280;')
        month_style.borders = border

        cell_style = xlwt.easyxf('alignment: horizontal center, vertical center, wrap True; font: name 宋体')
        cell_style.borders = border

        title_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 360;')
        title_style.borders = border

        xlwt.add_palette_colour("custom_colour", 0x21)
        work_book.set_colour_RGB(0x21, 255, 0, 0)
        color_cell_style = xlwt.easyxf(
            'alignment: horizontal center, vertical center, wrap True; font: name 宋体; '
            'pattern: pattern solid, fore_colour custom_colour')
        color_cell_style.borders = border

        title = '修次管理'
        sheet.write_merge(0, 0, 0, 3, title, title_style)

        sheet.write(1, 0, '设备', cell_style)
        sheet.write(1, 1, '年', cell_style)
        sheet.write(1, 2, '月', cell_style)
        sheet.write(1, 3, '修次', cell_style)
        sheet.write(1, 4, '修程', cell_style)

        cur_row = 2
        for record in records:
            sheet.write(cur_row, 0, record.dev.dev_no, cell_style)
            sheet.write(cur_row, 1, record.year.val, cell_style)
            sheet.write(cur_row, 2, record.month.val, cell_style)
            sheet.write(cur_row, 3, record.offset_num, cell_style)
            sheet.write(cur_row, 4, record.rule.no, cell_style)
            sheet.row(cur_row).height_mismatch = True
            sheet.row(cur_row).height = 300
            cur_row += 1

        fp = io.BytesIO()
        work_book.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '修次.xls'
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))

        return response

    @http.route('/repair_tmp_rule/export_data_repair_tmp_rule', type='http', auth='public', csrf=False)
    def export_data_repair_tmp_rule(self, *args, **kwargs):
        # 取得数据
        records = http.request.env["metro_park_maintenance.repair_tmp_rule"].search_read([])
        # 输出excel
        work_book = xlwt.Workbook()
        cell_border = xlwt.Borders()
        cell_border.left = 1
        cell_border.right = 1
        cell_border.top = 1
        cell_border.bottom = 1
        sheet = work_book.add_sheet('检技通', cell_overwrite_ok=True)
        border = xlwt.Borders()
        border.left = 1
        border.right = 1
        border.top = 1
        border.bottom = 1
        month_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 280;')
        month_style.borders = border

        cell_style = xlwt.easyxf('alignment: horizontal center, vertical center, wrap True; font: name 宋体')
        cell_style.borders = border

        title_style = xlwt.easyxf('alignment: horizontal center, vertical center, '
                                  'wrap True; font: name 宋体, height 360;')
        title_style.borders = border
        one_row = [
            '检技通号', '名称', '详细内容', '针对车辆', '结合修程', '开始日期', '结束日期'
        ]
        field_name = ['no', 'name', 'content', 'trains', 'repair_rules', 'start_date', 'end_date']
        for head_key, head_sheet in enumerate(one_row):
            sheet.write(0, head_key, head_sheet, cell_style)
        for rec_key, data in enumerate(records):
            for row in range(len(field_name)):
                if field_name[row] == 'trains':
                    dev = ''
                    dev_name = request.env['metro_park_maintenance.train_dev'].search(
                        [('id', 'in', data.get(field_name[row], ''))])
                    for dev_rec in dev_name:
                        dev += dev_rec.dev_name + ','
                    if dev:
                        table_value = dev[:-1]
                    else:
                        table_value = ''
                elif field_name[row] == 'repair_rules':
                    repair_rules = ''
                    repair_rule = request.env['metro_park_maintenance.repair_rule'].search(
                        [('id', 'in', data.get(field_name[row], ''))])
                    for rule in repair_rule:
                        repair_rules += rule.no + ','
                    if repair_rules:
                        table_value = repair_rules[:-1]
                    else:
                        table_value = ''
                elif field_name[row] == 'start_date':
                    table_value = str(data.get(field_name[row], '') if data.get(field_name[row], '') else '')
                    print(table_value)
                elif field_name[row] == 'end_date':
                    table_value = str(data.get(field_name[row], '') if data.get(field_name[row], '') else '')
                    print(table_value)
                else:
                    table_value = data.get(field_name[row], '')
                sheet.write(rec_key + 1, row, table_value, cell_style)
        fp = io.BytesIO()
        work_book.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        name = '检技通{}.xls'.format(date.today())
        response = request.make_response(data)
        response.headers['Content-Type'] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = "attachment; filename={}". \
            format(name.encode().decode('latin-1'))

        return response
