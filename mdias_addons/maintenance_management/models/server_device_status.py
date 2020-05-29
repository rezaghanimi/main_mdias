# -*- coding: utf-8 -*-

from odoo import api, models, fields
import datetime
import time

EightHours = datetime.timedelta(hours=8)


class ServerDeviceStatus(models.Model):
    _name = 'maintenance_management.server_state'
    _description = '服务器设备状态'

    name = fields.Char('name')

    def server_client(self):
        '''
        服务器设备状态
        :return:
        '''
        return {
            'type': 'ir.actions.client',
            'tag': 'server_client',
        }

    @api.model
    def get_values(self):
        return

    @api.model
    def get_battery_data(self, battery=False, time=False, place=False):
        '''
        搜索电源状态
        :param battery:
        :param time:
        :return:
        '''
        if time:
            start_time = time[0].split('T')[0] + ' ' + time[0].split('T')[1].split('.')[0]
            end_time = time[1].split('T')[0] + ' ' + time[1].split('T')[1][0:-1].split('.')[0]
            # 电池电压
            battery_voltage = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('place', '=', place),
                ('name', 'like', '电池电压'),
                ('name', 'like', battery),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # 电池内阻
            battery_internal_resistance = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', '电池内阻'),
                ('place', '=', place),
                ('name', 'like', battery),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # 电池温度
            battery_temperature = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', '电池温度'),
                ('place', '=', place),
                ('name', 'like', battery),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])
            # 时间
            return [
                [round(float(value.get('value')), 4) for value in battery_voltage],
                [round(float(value.get('value')), 4) for value in battery_internal_resistance],
                [round(float(value.get('value')), 4) for value in battery_temperature],
                [value.get('write_date') for value in battery_temperature],
            ]
        else:
            return [
                [],
                [],
                [],
                [],
            ]

    @api.model
    def get_ups_data(self, battery=False, time=False, place=False):
        '''
        获取ups数据
        :param battery:
        :param time:
        :return:
        '''
        if time:
            start_time = time[0].split('T')[0] + ' ' + time[0].split('T')[1].split('.')[0]
            end_time = time[1].split('T')[0] + ' ' + time[1].split('T')[1][0:-1].split('.')[0]

            name_data = ['UPS输出RS电压', 'UPS输出ST电压', 'UPS输出RT电压',
                         'UPS输出R相电压', 'UPS输出S相电压',
                         'UPS输出T相电压', 'UPS输出R相电流',
                         'UPS输出S相电流', 'UPS输出T相电流',
                         'UPS输出频率', 'UPS电池电流', 'UPS电池电压',
                         'UPS整流器输入UV电压', 'UPS整流器输入VW电压',
                         'UPS整流器输入UW电压', 'UPS整流器输入U相电流',
                         'UPS整流器输入V相电流', 'UPS整流器输入W相电流',
                         'UPS整流器输入频率', 'UPS逆变器R温度',
                         'UPS逆变器S温度', 'UPS逆变器T温度', 'UPS整流器温度',
                         'UPS环境温度']

            # 储存所有的UPS的数据
            lis_ups_data = []
            for data in name_data:
                ups_data = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                    ('name', 'like', data),
                    ('place', '=', place),
                    ('create_date', '>=', start_time),
                    ('create_date', '<=', end_time),
                ], ['value', 'write_date'])
                if data == name_data[-1]:
                    lis_ups_data.append([value.get('value') for value in ups_data])
                    lis_ups_data.append([value.get('write_date').strftime('%Y-%m-%d %H:%M:%S') for value in ups_data])
                lis_ups_data.append([value.get('value') for value in ups_data])
            return lis_ups_data
        else:
            lis = []
            for l in range(24):
                lis.append([])
            return lis

    @api.model
    def get_ups_side_data(self, battery=False, time=False, place=False):
        '''
        获取ups旁路数据
        :param battery:
        :param time:
        :return:
        '''
        if time:
            start_time = time[0].split('T')[0] + ' ' + time[0].split('T')[1].split('.')[0]
            end_time = time[1].split('T')[0] + ' ' + time[1].split('T')[1][0:-1].split('.')[0]
            # UPS旁路输入RS电压
            ups_side_rs = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入RS电压'),
                ('place', '=', place),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # UPS旁路输入ST电压
            ups_side_st = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入ST电压'),
                ('place', '=', place),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # UPS旁路输入RT电压
            ups_side_rt = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入ST电压'),
                ('place', '=', place),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # UPS旁路输入R电压
            ups_side_r = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入R电压'),
                ('place', '=', place),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # UPS旁路输入S相电压
            ups_side_s = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入ST电压'),
                ('place', '=', place),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            # UPS旁路输入T相电压
            ups_side_t = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入ST电压'),
                ('place', '=', place),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])

            #  UPS旁路输入频率
            ups_side_frequency = self.env['maintenance_management.battery_data_api_side'].sudo().search_read([
                ('name', 'like', 'UPS旁路输入频率'),
                ('place', '=', place),
                ('create_date', '>=', start_time),
                ('create_date', '<=', end_time),
            ], ['value', 'write_date'])
            return [
                [round(float(value.get('value')), 4) for value in ups_side_rs],
                [round(float(value.get('value')), 4) for value in ups_side_st],
                [round(float(value.get('value')), 4) for value in ups_side_rt],
                [round(float(value.get('value')), 4) for value in ups_side_r],
                [round(float(value.get('value')), 4) for value in ups_side_s],
                [round(float(value.get('value')), 4) for value in ups_side_t],
                [round(float(value.get('value')), 4) for value in ups_side_frequency],
                [value.get('write_date').strftime('%Y-%m-%d %H:%M:%S') for value in ups_side_frequency],
            ]
        else:
            return [
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            ]

    @api.model
    def get_ats_m_data(self, id):
        '''
        ATS 主机数据
        :param id:
        :return:
        '''
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '2'), ('create_date', '>=', old_date), ('create_date', '<=', now_date)],
            ['send_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('send_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))

        return [send_data, recv_data, write_date]

    @api.model
    def get_ats_s_data(self, id):
        '''
        ATS 备机数据
        :param id:
        :return:
        '''
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        send_data = []
        recv_data = []
        write_date = []
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '2'), ('create_date', '>=', old_date), ('create_date', '<=', now_date)],
            ['send_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('send_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_ci_m_data(self, id):
        '''
        CI 主机数据获取
        :param id:
        :return:
        '''
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        send_data = []
        recv_data = []
        write_date = []
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '1'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['recv_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('recv_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_ci_s_data(self, id):
        '''
        CI 备机数据获取
        :param id:
        :return:
        '''
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '1'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['send_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('send_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_pscada_m_data(self, id):
        '''
        PSCADA 主机 数据获取
        :param id:
        :return:
        '''
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '3'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['send_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('send_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_pscada_s_data(self, id):
        '''
        PSCADA 备机 数据获取
        :param id:
        :return:
        '''
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '3'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['send_count', 'recv_count', 'write_date'])
        for data in search_data:
            send_data.append(data.get('send_data'))
            recv_data.append(data.get('recv_data'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_gdl_pscada_data(self, id):
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '3'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['send_count', 'recv_count', 'write_date'])
        for data in search_data:
            send_data.append(data.get('send_data'))
            recv_data.append(data.get('recv_data'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_gdl_ci_data(self, id):
        if id in ['CI_s', 'CI_m', 'PSCADA_m']:
            place = '板桥'
        else:
            place = '高大路'
        '''
        CI 数据获取
        :param id:
        :return:
        '''
        send_data = []
        recv_data = []
        write_date = []
        now_date = datetime.datetime.now()
        old_date = datetime.datetime.now() - datetime.timedelta(hours=24)
        search_data = self.env['maintenance_management.interface_state'].search_read([
            ('type', '=', '1'), ('create_date', '>=', old_date), ('create_date', '<=', now_date),
            ('place', '=', place)],
            ['send_count', 'recv_count', 'write_date', 'tms'])
        for data in search_data:
            send_data.append(data.get('send_count'))
            recv_data.append(data.get('recv_count'))
            eight_hours = data.get('write_date') + EightHours
            write_date.append(eight_hours.strftime('%Y-%m-%d %H:%M:%S'))
        return [send_data, recv_data, write_date]

    @api.model
    def get_tcms_m_data(self, id):
        '''
        获取 PSCADA  主机 数据
        :param id:
        :return:
        '''
        pass

    @api.model
    def get_tcms_s_data(self, id):
        '''
        获取 PSCADA  备机 数据
        :param id:
        :return:
        '''
        pass

    @api.model
    def get_pms_m_data(self, id):
        '''
        获取 PMS 主机数据获取
        :param id:
        :return:
        '''
        pass

    @api.model
    def get_pms_s_data(self, id):
        '''
        获取 PMS 备机数据获取
        :param id:
        :return:
        '''
        pass

    @api.model
    def get_none_data(self):
        return [[], [], []]
