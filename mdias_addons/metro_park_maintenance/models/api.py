# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import AccessDenied
import pendulum
import json
import logging

_logger = logging.getLogger(__name__)


class API(models.AbstractModel):
    '''
    汇辙接口
    '''

    _name = 'metro.park.interface'
    _description = '调试接口'

    @api.model
    def get_user_groups(self, user_id):
        '''
        取得当前用户的所有权限
        :return:
        '''
        user = self.env.user.browse(user_id)
        groups_ids = self.env['res.groups'].search([('id', 'in', user.groups_id.ids), ('atomic', '=', True)]).ids
        groups = self.env['ir.model.data'].sudo() \
            .search([('model', '=', 'res.groups'),
                     ('res_id', 'in', groups_ids)
                     ])
        return groups.read(fields=["id", "name"])

    @api.model
    def getUserData(self, **kwargs):
        '''
        所有用户信息
        :param kwargs:
        :return:
        '''
        if 'userId' in kwargs.keys():
            users = self.env['funenc.wechat.user'] \
                .sudo() \
                .search_read([('user_id', '=', int(kwargs['userId']))])
        else:
            users = self.env['funenc.wechat.user'] \
                .sudo() \
                .search_read([('user_id', '!=', False)])
        rst = []
        if users:

            for user in users:
                rst.append({
                    'userId': user['user_id'][0],
                    'userName': user['name'],
                    'userWxid': user['wx_userid'],
                    'lineId': str(user['cur_location'][0]) if user['cur_location'] else '',
                    'lineName': user['cur_location'][1] if user['cur_location'] else '',
                    'operateDepartId': '',
                    'operateDepartName': '',
                    'groups': self.get_user_groups(user['user_id'][0])
                })
        return rst

    @api.model
    def getUserData(self, **kwargs):
        '''
        所有用户信息
        :param kwargs:
        :return:
        '''
        if 'userId' in kwargs.keys():
            users = self.env['funenc.wechat.user'] \
                .sudo() \
                .search_read([('user_id', '=', int(kwargs['userId']))])
        else:
            users = self.env['funenc.wechat.user'] \
                .sudo() \
                .search_read([('user_id', '!=', False)])
        rst = []
        if users:

            for user in users:
                rst.append({
                    'userId': user['user_id'][0],
                    'userName': user['name'],
                    'userWxid': user['wx_userid'],
                    'lineId': str(user['cur_location'][0]) if user['cur_location'] else '',
                    'lineName': user['cur_location'][1] if user['cur_location'] else '',
                    'operateDepartId': '',
                    'operateDepartName': '',
                    'groups': self.get_user_groups(user['user_id'][0])
                })
        return rst

    @api.model
    def getLoginData(self, **kwargs):
        '''
        所有用户信息
        :param kwargs:
        :return:
        '''
        dbname = self.env.cr.dbname
        login = kwargs['login']
        password = kwargs['password']
        user = self.env['res.users'].search([('login', '=', login)])
        if not user:
            return {
                'status': 401,
                'data': {
                    'msg': '用户不存在'
                }
            }
        try:
            user = self.env['res.users'].search([('login', '=', login)])
            uid = user._login(dbname, login, password)
            rst = []
            if uid:
                users = self.env['funenc.wechat.user'] \
                    .sudo() \
                    .search_read([('user_id', '=', user.id)])
            else:
                users = self.env['funenc.wechat.user'] \
                    .sudo() \
                    .search_read([('user_id', '!=', False)])
            if users:
                for user in users:
                    rst.append({
                        'userId': user['user_id'][0],
                        'userName': user['name'],
                        'userWxid': user['wx_userid'],
                        'lineId': str(user['cur_location'][0]) if user['cur_location'] else '',
                        'lineName': user['cur_location'][1] if user['cur_location'] else '',
                        'operateDepartId': '',
                        'operateDepartName': '',
                        'groups': self.get_user_groups(user['user_id'][0])
                    })
            return {
                'data': rst,
                'status': 200
            }
        except AccessDenied:
            return {
                'status': 401,
                'data': {
                    'msg': '用户或密码错误'
                }
            }

    @api.model
    def getDepartmentUserData(self, **kwargs):
        '''
        根据部门查询用户信息
        :param kwargs:
        :return:
        '''
        domain = []
        res = []
        if kwargs and 'departId' in kwargs.keys():
            domain.append(('department_ids', '=', int(kwargs['departId'])))
        if kwargs and 'userName' in kwargs.keys():
            domain.append(('user_id.name', '=', kwargs['userName']))
        users = self.env['funenc.wechat.user'].sudo().search_read(domain=domain)
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
        return res

    @api.model
    def getPhoneUserData(self, **kwargs):
        '''
        根据电话号码查用户信息
        :param mobile:
        :return:
        '''
        if kwargs and 'mobile' in kwargs.keys():
            domain = [('mobile', '=', kwargs['mobile'])]
            res = []
            users = self.env['funenc.wechat.user'].sudo().search_read(domain=domain)
            if users:
                for user in users:
                    res.append({
                        'userId': user['user_id'][0],
                        'userName': user['user_id'][1],
                        'userWxId': user['wx_userid'],
                        'userEmployeeId': '',
                        'departId': user['first_department_id'][0],
                        'departName': user['first_department_id'][1],
                    })
            return res
        else:
            raise exceptions.ValidationError(string="参数不正确")

    @api.model
    def getDepartmentData(self, **kwargs):
        '''
        所有部门信息
        :param kwargs:
        :return:
        '''
        domain = []
        res = []
        if kwargs and 'parentDepartId' in kwargs.keys():
            domain.append(('parent_id', '=', int(kwargs['parentDepartId'])))
        else:
            domain.append(('parent_id', '=', False))
        departments = self.env['funenc.wechat.department'].sudo().search_read(domain)
        if departments:
            for department in departments:
                val = {
                    'departId': department['id'],
                    'departName': department['name']
                }
                res.append(val)
        return res

    @api.model
    def getOperationDepartmentData(self):
        '''
        所有作业单位部门
        :param kwargs:
        :return:
        '''
        res = []
        operation = self.env['funenc_wechat.property'].sudo().search([('name', '=', '作业单位')])
        if operation:
            department = self.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                res = self.datetime_handle(department)
        return res

    @api.model
    def getWorkshopDepartmentData(self):
        '''
        所有作业车间部门
        :param kwargs:
        :return:
        '''
        data = []
        operation = self.env['funenc_wechat.property'].sudo().search([('name', '=', '作业车间')])
        if operation:
            department = self.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                data = self.datetime_handle(department)
        return data

    @api.model
    def getMaintenanceDepartmentData(self):
        '''
        所有检修班组部门
        :param kwargs:
        :return:
        '''
        data = []
        operation = self.env['funenc_wechat.property'].sudo().search([('name', '=', '作业工班')])
        if operation:
            department = self.env['funenc.wechat.department'].sudo().search_read(
                [('properties', 'in', operation.id)])
            if department:
                data = self.datetime_handle(department)
        return data

    @api.model
    def getTrainTypesData(self):
        '''
        车辆型号
        :param kwargs:
        :return:
        '''
        data = []
        train_types = self.env['metro_park_base.dev_standard'].sudo().search_read()
        if train_types:
            for dev_type in train_types:
                val = {
                    'vehicleTypeId': dev_type['id'],
                    'vehicleTypeName': dev_type['name'],
                }
                data.append(val)
        return data

    @api.model
    def getTrainDevData(self, **kwargs):
        '''
        车辆设备，同时返回设备批次开始的时间
        :param kwargs:
        :return:
        '''
        domain = []
        if kwargs and 'vehicleTypeId' in kwargs.keys():
            domain.append(('dev_type', '=', int(kwargs['vehicleTypeId'])))
        if kwargs and 'lineId' in kwargs.keys():
            domain.append(('line', '=', int(kwargs['lineId'])))
        data = []
        trains = self.env['metro_park_maintenance.train_dev'].search(domain)
        train_cache = {train.id: train for train in trains}
        train_devs = trains.read(['dev_name', 'dev_no', 'dev_type', 'start_use_time', 'line'])
        for train in train_devs:
            val = {
                'vehicleDeviceNo': train['dev_no'],
                'vehicleName': train['dev_name'],
                'vehicleTypeId': train['dev_type'][0],
                'vehicleTypeName': train['dev_type'][1],
                'lineId': train['line'][0],
                'lineName': train['line'][1],
                'startOperationDate': str(train_cache[train["id"]].batch_no.start_date)
            }
            data.append(val)
        return data

    @api.model
    def getLineData(self):
        '''
        获取线别
        :param kwargs:
        :return:
        '''
        rail_types = self.env['metro_park_base.line'].sudo().search_read(fields=['id', 'name', 'code'])
        return rail_types

    @api.model
    def getLocationData(self, **kwargs):
        '''
        厂段信息
        :param kwargs:
        :return:
        '''
        data = []
        domain = []
        if kwargs and 'lineId' in kwargs.keys():
            domain.append(('line', '=', int(kwargs['lineId'])))
        train_devs = self.env['metro_park_base.location'].sudo().search_read(domain)
        for train in train_devs:
            val = {
                'id': train['id'],
                'name': train['name'],
                'lineId': train['line'][0],
            }
            data.append(val)
        return data

    @api.model
    def getWarehouseData(self, **kwargs):
        '''
        作业区域
        :param kwargs:
        :return:
        '''
        warehouse = self.env['metro_park_base.warehouse'].sudo().search_read(fields=['id', 'name'])
        return warehouse

    @api.model
    def getRailTypeData(self, **kwargs):
        '''
        作业区域要求
        :param kwargs:
        :return:
        '''
        rail_types = self.env['metro_park_base.rail_type'].sudo().search_read(fields=['id', 'name'])
        return rail_types

    @api.model
    def getRailProperty(self, **kwargs):
        '''
        取得轨道属性
        :return:
        '''
        railProperty = self.env['metro_park_base.rail_property']\
            .sudo()\
            .search_read(fields=['id', 'name'])
        return railProperty

    @api.model
    def getRailsByLineId(self, **kwargs):
        '''
        通过线别取得股道
        :return:
        '''
        lineId = kwargs.get("lineId", None)
        if lineId:
            rails = self.env['metro_park_base.rails_sec']\
                .sudo()\
                .search([('location.line.id', '=', lineId)])
        else:
            rails = self.env['metro_park_base.rails_sec']\
                .sudo()\
                .search([])
        rail_cache = {rail.id: rail for rail in rails}
        rail_records = rails.read()
        for rail in rail_records:
            rail["railProps"] = rail_cache[rail["id"]].rail_property.read(["id", "name"])
        return rail_records

    @api.model
    def getTrainTodayPredictMiles(self, **kwargs):
        '''
        取得公里数预估数据
        :return:
        '''
        vehicleDeviceNo = kwargs.get("vehicleDeviceNo", None)
        today = pendulum.today("UTC")
        record = self.env["metro_park_maintenance.history_miles"].sudo()\
            .search([("dev_no", "=", vehicleDeviceNo),
                     ("year", '=', today.year),
                     ("month", "=", today.month)])
        return {"estimateMileage": record["day{day}".format(today.day)]}

    @api.model
    def getTrainMilesData(self, **kwargs):
        '''
        列车里程公里数
        :param kwargs:
        :return:
        '''
        domain = []
        data = []
        history = self.env['metro_park_maintenance.history_miles']
        today = pendulum.today('UTC')
        year = today.year
        month = today.month
        day = today.day
        if kwargs and 'vehicleDeviceNo' not in kwargs.keys():
            return json.dumps('参数 vehicleDeviceNo 车辆设备号必填!', ensure_ascii=False)
        elif kwargs and 'vehicleDeviceNo' in kwargs.keys():
            dev_no = kwargs['vehicleDeviceNo']
        elif kwargs and 'operateDate' in kwargs.keys():
            operate_date = pendulum.parse(kwargs['operateDate'])
            year = operate_date.year
            month = operate_date.month
            day = operate_date.day
        date_str = '{year}-{month}-{day}'.format(year=year, month=month, day=day)
        domain.append(('year', '=', year))
        domain.append(('month', '=', month))
        train = self.env['metro_park_maintenance.train_dev'].sudo().search([('dev_no', '=', dev_no)])
        if train:
            domain.append(('train_dev', '=', train.id))
            train_miles = history.sudo().search_read(domain)
            if train_miles:
                for miles in train_miles:
                    val = {
                        'vehicleDeviceNo': kwargs['vehicleDeviceNo'],
                        'operateDate': date_str,
                        'totalMileage': miles['total_miles']
                    }
                    data.append(val)
        return data

    @api.model
    def getTimeTableData(self, **kwargs):
        '''
        获取运行图概要
        :return:
        '''
        data = []
        if not kwargs.get('operateDate', False):
            raise exceptions.ValidationError("参数不正确")

        # 取得当天配置的时刻表
        time_table_id = self.env['metro_park_dispatch.nor_time_table_config']\
            .get_date_config(kwargs.get('operateDate', False))
        if not time_table_id:
            raise exceptions.ValidationError('当天没有配置运行图，请先在运行图管理模块中配置运行图')
        tmp_model = self.env['metro_park_base.time_table_data']
        time_table_datas = tmp_model.search([('time_table_id', '=', time_table_id)])
        rst = []
        for data in time_table_datas:
            val = {
                'seq': data['train_no'],
                'outSectionId': data['out_location'].id,
                'outSectionName': data['out_location'].name,
                'outTime': data['plan_out_time'].strftime('%H:%M:%S') if data['plan_out_time'] else '',
                'inSectionId': data['back_location'].id,
                'inSectionName': data['back_location'].name,
                'inTime': data['plan_in_time'].strftime('%H:%M:%S') if data['plan_in_time'] else '',
                'inPark': data['high_time_train'],
                'runMileage': ''
            }
            rst.append(val)
        return rst

    @api.model
    def getTimeTableInformationData(self, **kwargs):
        '''
        获取所有时刻表 详细信息
        :return:
        '''
        data = []
        time_tables = self.env['metro_park_base.time_table'].sudo().search_read()
        for table in time_tables:
            val = {
                'scheduleTableName': '',
                'scheduleTableNo': table['no'],
                'scheduleTableId': table['id'],
            }
            data.append(val)
        return data
