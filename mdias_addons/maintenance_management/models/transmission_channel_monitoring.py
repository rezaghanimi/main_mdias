# -*- conding:utf-8 -*-

from odoo import api, models, fields
from pysnmp.hlapi import *
import time
import logging

LOGIN_URL = "login.cgi"
CONFIG_URL = "config.cgi"

_logger = logging.getLogger(__name__)


class TransmissionChannelMonitoring(models.Model):
    _name = 'maintenance_management.transmission_channel'
    _description = '传输通道质量监督'
    _track_log = True

    temperature = fields.Char(string='模块温度')
    current = fields.Char(string='激光篇置电流')
    voltage = fields.Char(string='供电电压')
    transmitted_light_power = fields.Char(string='发射光功率')
    received_light_power = fields.Char(string='接收光功率')
    switches = fields.Char(string='对应交换机')
    models_type = fields.Char(string='对应的类型')
    node_name = fields.Char(string='对应交换机的端口号')

    @api.model
    def get_switches_bq_jr_a(self, name):
        '''
        获取板桥接入交换机A的传输通道质量监督
        :return:
        :name:对应交换机的名称
        '''
        # 获取对应名称的所有的数据
        all_rec = self.search_read([
            ('switches', '=', name),
        ], fields=['temperature', 'current', 'voltage', 'transmitted_light_power', 'received_light_power'])

        return all_rec

    @api.multi
    def timing_task_get_switches_data(self):
        '''
        定时任务去获取传输通道质量监督的值
        :return:
        '''
        switches_names = ['板桥核心交换机A登录信息', '板桥核心交换机B登录信息', '板桥接入交换机A登录信息',
                          '板桥接入交换机B登录信息', '高大路接入交换机A登录信息', '高大路接入交换机B登录信息',
                          '太平园接入交换机A登录信息',
                          ]
        for switches_name in switches_names:
            try:
                ip_site_gdl_b = self.env['maintenance_management.database_data'].search_read(
                    [('name', '=', switches_name)])
                self.get_index_data(ip_site_gdl_b, switches_name[:-4])
            except Exception as e:
                _logger.error('交换机光模块未开放')

    @api.multi
    def get_index_data(self, ip_site, name):
        start_time = time.time()
        # 用来存放光模块的键值、
        data = []
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData('zabbix123', mpModel=0),
                                  UdpTransportTarget((ip_site[0].get('ip'), 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('1.3.6.1.2.1.47.1.1.1.1.7'))):
            if errorIndication or errorStatus:
                break
            else:
                for varBind in varBinds:
                    str_data = ' = '.join([x.prettyPrint() for x in varBind])
                    if 'XGigabitEthernet' in str_data:
                        # 可以根据 integer_type 的值找到对应的 光模块的值
                        integer_type = str_data.split('/')[-1]
                        value = str_data.split('.')[-1][:8]
                        data.append({
                            str(integer_type): value
                        })
                    if time.time() - start_time > 3:
                        self.get_timing_task_get_switches_data(data, ip_site, name)
                        return

    @api.multi
    def get_timing_task_get_switches_data(self, data, ip_site, name):
        '''
        获取所有的值并存放数据库
        :return:
        '''
        oid = [
            '1.3.6.1.4.1.2011.5.25.31.1.1.3.1.5',
            '1.3.6.1.4.1.2011.5.25.31.1.1.3.1.6',
            '1.3.6.1.4.1.2011.5.25.31.1.1.3.1.7',
            '1.3.6.1.4.1.2011.5.25.31.1.1.3.1.8',
            '1.3.6.1.4.1.2011.5.25.31.1.1.3.1.9',
        ]
        all_data = []
        start_time = time.time()
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in nextCmd(SnmpEngine(),
                                  CommunityData('zabbix123', mpModel=0),
                                  UdpTransportTarget((ip_site[0].get('ip'), 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('1.3.6.1.4.1.2011.5.25.31.1.1.3.1.5'))):
            if errorIndication or errorStatus:
                break
            else:
                for varBind in varBinds:
                    end_time = time.time()
                    if end_time - start_time > 10:
                        return self.create(all_data)
                    str_data = ' = '.join([x.prettyPrint() for x in varBind])
                    for intger, port_switch in enumerate(data):
                        if port_switch.get(str(intger + 1)) in str_data:
                            # 获取到对应的值
                            get_data = str_data.split('=')[-1]
                            if oid[0].split('4.1.')[1] in str_data:
                                if int(get_data.strip()) > 1:
                                    all_data.append({
                                        'temperature': get_data,
                                        'switches': name,
                                        'node_name': intger + 1,
                                    })
                            if oid[1].split('4.1.')[1] in str_data:
                                if int(get_data.strip()) > 1:
                                    all_data.append({
                                        'current': get_data,
                                        'switches': name,
                                        'node_name': intger + 1,
                                    })
                            if oid[2].split('4.1.')[1] in str_data:
                                if int(get_data.strip()) > 1:
                                    all_data.append({
                                        'voltage': get_data,
                                        'switches': name,
                                        'node_name': intger + 1,
                                    })
                            if oid[3].split('4.1.')[1] in str_data:
                                if int(get_data.strip()) > 1:
                                    all_data.append({
                                        'transmitted_light_power': get_data,
                                        'switches': name,
                                        'node_name': intger + 1,
                                    })
                            if oid[4].split('4.1.')[1] in str_data:
                                if int(get_data.strip()) > 1:
                                    all_data.append({
                                        'received_light_power': get_data,
                                        'switches': name,
                                        'node_name': intger + 1,
                                    })
