# -*- coding: utf-8 -*-
from odoo import api, models, fields
import json
from urllib import request
import time
import socket
import logging
from ..models.zabbix_configuration import TEN_CONFIGURATION_DATA_POSITIVE
from ..models.zabbix_configuration import TEN_CONFIGURATION_DATA_REVERSE
from ..models.zabbix_configuration import TEN_CONFIGURATION_NAME
from ..models.zabbix_configuration import TEN_ZABBIX_IP
from ..models.zabbix_configuration import TEN_DATAS
from ..models.zabbix_configuration import Ten_ZABBIX_KEY

ZABBIX_SERVER = 'ZABBIX服务器'
ZABBIX_PHP = 'http://{}/zabbix/api_jsonrpc.php'
HEADER = {"Content-Type": "application/json"}
ERROR_CONFIG = '请检查配置是否错误'
DISK_SPACE = '清理磁盘空间'

_logger = logging.getLogger(__name__)


class DatabaseDataMaintenance(models.Model):
    _name = 'maintenance_management.database_data'
    _description = '服务器监控'
    _track_log = True

    name = fields.Char(string='名称', required=True)
    ip = fields.Char(string='IP地址')
    zabbix = fields.Char(string='ZABBIX键值')
    other = fields.Char(string='其他')

    @api.model
    def link_database_data(self, arg):
        '''
        链接
        :return:
        '''
        try:
            ip_site = self.search_read([('name', '=', ZABBIX_SERVER)], ['ip'])
            url = ZABBIX_PHP.format(ip_site[0].get('ip'))
            auth = self.zabbix_login()
            host_id = self.get_host(url, HEADER, auth, TEN_CONFIGURATION_DATA_REVERSE.get(arg))
            data = self.get_itemids(url, host_id, auth, HEADER, TEN_CONFIGURATION_DATA_REVERSE.get(arg))
            return data
        except IndexError as f:
            _logger.error('link_database_data 96 {}'.format(str(f)))
            return '连接失败，没有获取到数据'
        except Exception as f:
            _logger.error('link_database_data 99 {}'.format(str(f)))
            return ERROR_CONFIG

    @api.multi
    def zabbix_login(self):
        ip_site = self.search_read([('name', '=', ZABBIX_SERVER)], ['ip'])
        url = ZABBIX_PHP.format(ip_site[0].get('ip'))
        username = 'Admin'
        password = 'zabbix'
        data = {'jsonrpc': '2.0',
                'method': 'user.login',
                'params': {
                    'user': username,
                    'password': password
                },
                'id': 1
                }
        value = json.dumps(data).encode('utf-8')
        req = request.Request(url, headers=HEADER, data=value)
        # 打开包装过的url
        try:
            result = request.urlopen(req, timeout=4)
            response = result.read()
            # 上面获取的是bytes类型数据，故需要decode转化成字符串
            page = response.decode('utf-8')
            # 将此json字符串转化为python字典
            page = json.loads(page)
            auth = page['result']
            result.close()
            return auth
        except Exception as f:
            _logger.error('配置信息错误，zabbix登录失败 {}'.format(str(f)))

    @api.multi
    def get_host(self, url, header, auth, data_reverse):
        '''
        获取数据信息
        :param url:
        :param header: 请求头
        :param auth: 信息数据
        :return:
        '''
        neirong = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": 1,
            "auth": auth
        }
        page = self.get_response_data(url, neirong, header)
        for host in page.get('result'):
            if host.get('host') == data_reverse:
                host_id = host.get('hostid')
                break
        return host_id

    @api.multi
    def get_items_data(self, host_id, cpu_value, auth):
        '''
        获取items
        :return:
        :host_id: hostid
        :cpu_value: CPU 的值
        :auth: 登录的携带信息
        '''
        items = {"jsonrpc": "2.0",
                 "method": "item.get",
                 "params": {"output": "itemids",
                            "hostids": host_id,
                            "search": {"key_": cpu_value}},
                 "auth": auth,
                 "id": 1
                 }

        return items

    @api.multi
    def get_itemids(self, url, host_id, auth, header, data_reverse):
        '''
        获取项目数据
        :param url:
        :param host_id:
        :param auth:
        :param header:
        :return:
        '''
        date_str = "%Y-%m-%d %H:%M:%S"
        # 获取对应的名字
        zabbix_value = self.search_read([
            ('name', 'like', TEN_CONFIGURATION_NAME.get(data_reverse)),
        ], ['name', 'zabbix', 'other'])
        # 获取对应的值
        value = self.deal_zabbix_name_info(zabbix_value, data_reverse)

        cpu = self.get_items_data(host_id, value.get('cpu_value'), auth)

        available_memory = self.get_items_data(host_id, value.get('available_memory_value'), auth)

        memory = self.get_items_data(host_id, value.get('memory_value'), auth)

        network_out = self.get_items_data(host_id, value.get('network_out_value'), auth)

        network_in = self.get_items_data(host_id, value.get('network_in_value'), auth)

        number_processes = self.get_items_data(host_id, value.get('number_processes_value'), auth)

        login_user_number = self.get_items_data(host_id, value.get('login_user_number_value'), auth)

        system_uptime = self.get_items_data(host_id, value.get('system_uptime_value'), auth)

        disk_space_total = self.get_items_data(host_id, value.get('disk_space_total_value'), auth)

        disk_space_use = self.get_items_data(host_id, value.get('disk_space_use_value'), auth)

        # 获取cpu的数据
        cpu_data_rec = self.get_response_data(url, cpu, header).get('result')[0].get('itemid')
        cpu_data_id_rec = self.get_item_data(url, header, auth, cpu_data_rec, value.get('cpu_value'))
        cpu_key = []
        cpu_value = []
        for cpu_rec_one in cpu_data_id_rec.get('result'):
            cpu_key.append(
                time.strftime(date_str, time.localtime(float(cpu_rec_one.get('clock')) + 28800))[10:])
            cpu_value.append(cpu_rec_one.get('value'))

        # 获取总内存的数据
        memory_data_rec = self.get_response_data(url, memory, header).get('result')[0].get('itemid')
        memory_data_id_rec = self.get_item_data(url, header, auth, memory_data_rec, value.get('memory_value'))
        memory_data_value = float(memory_data_id_rec.get('result')[0].get('value')) / 1024 / 1024

        # 获取可用内存的数据
        available_memory_data_rec = self.get_response_data(url, available_memory, header).get('result')[0].get('itemid')
        available_memory_data_id_rec = self.get_item_data(url, header, auth, available_memory_data_rec,
                                                          available_memory)
        memory_key = []
        memory_value = []
        for available_memory_data_one in available_memory_data_id_rec.get('result'):
            memory_key.append(time.strftime(date_str,
                                            time.localtime(float(available_memory_data_one.get('clock')) + 28800))[10:])
            memory_value.append((1 - (
                round(float(available_memory_data_one.get('value')) / 1024 / 1024 / memory_data_value,
                      2))) * 100)

        # 获取网络接口流量出口状况
        network_time = []
        network_out_rec = []
        try:
            network_out_data_rec = self.get_response_data(url, network_out, header).get('result')[0].get('itemid')
            network_out_id_rec = self.get_item_data(url, header, auth, network_out_data_rec,
                                                    value.get('network_out_value'))
            for network_one in network_out_id_rec.get('result'):
                network_time.append(time.strftime(date_str,
                                                  time.localtime(float(network_one.get('clock')) + 28800))[10:])
                network_out_rec.append(-float(network_one.get('value')))
        except Exception as e:
            _logger.info('流量出口状况为0 {}'.format(str(e)))

        # 获取网络接口流量入口状况
        network_in_rec = []
        try:
            network_in_data_rec = self.get_response_data(url, network_in, header).get('result')[0].get('itemid')
            network_in_id_rec = self.get_item_data(url, header, auth, network_in_data_rec,
                                                   value.get('network_in_value'))
            for network_in_in in network_in_id_rec.get('result'):
                network_in_rec.append(network_in_in.get('value'))
        except Exception as e:
            _logger.info('流量出口状况为0 {}'.format(str(e)))

        # 获取当前系统的进程数量
        number_processes_data_rec = self.get_response_data(url, number_processes, header).get('result')[0].get('itemid')
        number_processes_id_rec = self.get_item_data(url, header, auth, number_processes_data_rec, number_processes)
        processes_data = number_processes_id_rec.get('result')[-1].get('value')  # 获取最后的进程的数量

        # 获取当前登录的用户数量
        try:
            login_user_number_data_rec = self.get_response_data(url, login_user_number,
                                                                header).get('result')[0].get('itemid')
            login_user_number_id_rec = self.get_item_data(url, header, auth, login_user_number_data_rec,
                                                          'net.if.out[enp0s5]')
            login_user_data = login_user_number_id_rec.get('result')[-1].get('value')  # 获取当前系统的进程数量
        except Exception as f:
            _logger.error('get_itemids 330{}'.format(str(f)))
            login_user_data = 1

        # 系统正常运行时间
        system_uptime_data_rec = self.get_response_data(url, system_uptime, header).get('result')[0].get('itemid')
        system_uptime_id_rec = self.get_item_data(url, header, auth, system_uptime_data_rec,
                                                  value.get('system_uptime_value'))
        # 系统正常运行时间
        system_uptime_data = round(float(system_uptime_id_rec.get('result')[-1].get('value')) / 3600, 2)

        # 磁盘的总空间
        disk_data_rec = self.get_response_data(url, disk_space_total, header).get('result')[0].get('itemid')
        disk_id_rec = self.get_item_data(url, header, auth, disk_data_rec, disk_space_total)
        all_disk = disk_id_rec.get('result')[0].get('value')

        # 磁盘的使用空间
        disk_use_data_rec = self.get_response_data(url, disk_space_use, header).get('result')[0].get('itemid')
        disk_use_id_rec = self.get_item_data(url, header, auth, disk_use_data_rec, disk_space_use)
        use_dick = disk_use_id_rec.get('result')[-1].get('value')

        return {
            'cpu_key': cpu_key,
            'cpu_value': cpu_value,
            'memory_key': memory_key,
            'memory_value': memory_value,
            'network_time': network_time,
            'network_out': network_out_rec,
            'network_in': network_in_rec,
            'processes_data': processes_data,
            'login_user_data': login_user_data,
            'system_uptime_data': system_uptime_data,
            'all_disk': all_disk,
            'use_dick': use_dick,
            'system_name': TEN_CONFIGURATION_NAME.get(data_reverse),
        }

    @api.multi
    def deal_zabbix_name_info(self, zabbix_value, data_reverse):
        '''
        获取zabbix 对应的数据
        :param zabbix_value:
        :param data_reverse:
        :return:
        '''
        cpu_value = ''
        available_memory_value = ''
        memory_value = ''
        network_out_value = ''
        network_in_value = ''
        number_processes_value = ''
        login_user_number_value = ''
        system_uptime_value = ''
        disk_space_total_value = ''
        disk_space_use_value = ''
        for value in zabbix_value:
            if value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '处理器':
                cpu_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '可用内存':
                available_memory_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '总内存':
                memory_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '流量出口':
                network_out_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '流量入口':
                network_in_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '当前进程数':
                number_processes_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '登录用户数量':
                login_user_number_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '系统正常运行时间':
                system_uptime_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '磁盘总空间':
                disk_space_total_value = value.get('zabbix')
            elif value.get('name') == TEN_CONFIGURATION_NAME.get(data_reverse) + '磁盘使用空间':
                disk_space_use_value = value.get('zabbix')

        return {
            'cpu_value': cpu_value,
            'available_memory_value': available_memory_value,
            'memory_value': memory_value,
            'network_out_value': network_out_value,
            'network_in_value': network_in_value,
            'number_processes_value': number_processes_value,
            'login_user_number_value': login_user_number_value,
            'system_uptime_value': system_uptime_value,
            'disk_space_total_value': disk_space_total_value,
            'disk_space_use_value': disk_space_use_value,
        }

    @api.multi
    def get_item_data(self, url, header, auth, item_id, history_data):
        new_date_end = time.time()
        new_date_start = time.time() - 3600
        if history_data == 'system.cpu.util[,user]' or history_data == 'system.cpu.load[percpu,avg15]':
            history = 0
        else:
            history = 3

        item = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {"history": history,
                       "itemids": [item_id],
                       "time_from": new_date_start,
                       "time_till": new_date_end,
                       "output": "extend"},
            "auth": auth,
            "id": 1
        }
        page = self.get_response_data(url, item, header)
        return page

    @api.multi
    def get_response_data(self, url, item, header):
        '''
        获取response的数据
        :param url:
        :param item:
        :param header:
        :return:
        '''
        response = request.Request(url, data=json.dumps(item).encode('utf-8'), headers=header)
        response_data = request.urlopen(response, timeout=4)
        return eval(response_data.read().decode('utf-8'))

    @api.multi
    def get_battery_data(self):
        try:
            bq = self.search_read([('name', '=', '板桥电源')])
            self.get_battery_data_all(bq, '板桥', '板桥中心机房')
        except Exception as e:
            _logger.error('get_battery_data 405{}'.format(str(e)))
        try:
            gsl = self.search_read([('name', '=', '高大路电源')])
            self.get_battery_data_all(gsl, '高大路', '高大路中心机房')
        except Exception as e:
            _logger.error('get_battery_data 410 {}'.format(str(e)))

    # 接收信息
    cache_recv_msg = b''

    # 判断是否退出循环
    lis_ba = []

    @api.multi
    def get_battery_data_all(self, data, place, site):
        state_env = self.env['maintenance_management.equipment_state']
        s = socket.socket()
        key_site = {
            '板桥': 'bq_battery_line',
            '高大路': 'gdl_battery_line',
        }
        try:
            s.connect((data[0].get('ip'), int(data[0].get('other'))))
            time.sleep(2)
            # 用来改变DRWA.IO图的连接线的颜色
            if state_env.search(
                    [('line', '=', key_site.get(place))]).state == 'disconnect':
                state_env.search(
                    [('line', '=', key_site.get(place))]).state = 'connection'
                self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                self.env.cr.commit()
            global lis_ba
            lis_ba = []
            try:
                self.get_battery_data_all_continue(s, data, place, site, b'')
            except Exception as f:
                _logger.error('get_battery_data_all 436 {}'.format(str(f)))
                return ERROR_CONFIG
        except Exception as e:
            _logger.error('get_battery_data_all 439 {}'.format(str(e)))
            # 发送错误的信心修改连接线的颜色
            time.sleep(2)
            if state_env.search(
                    [('line', '=', key_site.get(place))]).state == 'connection':
                self.env.cr.commit()
                if key_site[place] == 'bq_battery_line':
                    self.trigger_up_event('connect_waring_prompt', '板桥电源')
                    self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                elif key_site[place] == 'gdl_battery_line':
                    self.trigger_up_event('connect_waring_prompt', '高大路电源')
                    self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
            if state_env.search(
                    [('line', '=', key_site.get(place))]).state == 'connection':
                state_env.search(
                    [('line', '=', key_site.get(place))]).write({'state': 'disconnect'})
                self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                self.env.cr.commit()

    @api.multi
    def get_battery_data_all_continue(self, s, data, place, site, cache_recv_msg):
        self.cache_recv_msg = cache_recv_msg
        err = ''
        battery_err_data = {}
        while True:
            s.send('heartbeat'.encode())
            requ = s.recv(4096)
            self.cache_recv_msg = self.cache_recv_msg + requ
            pos = self.cache_recv_msg.find('|'.encode())
            if pos == -1:
                return self.get_battery_data_all_continue(s, data, place, site, b'')
            elif pos == 0:
                pos = self.cache_recv_msg.decode()[1:].find('|')
            try:
                time.sleep(0.5)
                if '}' in self.cache_recv_msg[: pos].decode():
                    size = int(self.cache_recv_msg[: pos].decode().split('}')[1])
                else:
                    size = int(self.cache_recv_msg[: pos])
            except Exception as e:
                logging.error('407 {}'.format(str(e)))
                return
            need_size = size + pos + 1
            if need_size <= len(self.cache_recv_msg):
                content = eval(self.cache_recv_msg[pos + 1: size + pos + 1].decode('utf-8'))
                lis_ba.append(content)
                if len(lis_ba) >= 5:
                    break
                if content.get('type') == 4:
                    all_rec = self.env['maintenance_management.battery_data_api'].sudo().create(
                        content.get('data'))
                    all_rec.write({'place': place})
                    err = [err_data for err_data in content.get('data') if err_data.get('value') > 0]
                    battery_err_data = {
                        'err_info': err,
                        'custom_module': True
                    }
                elif content.get('type') == 5:
                    all_rec_1 = self.env['maintenance_management.battery_data_api_side'].sudo().create(
                        list(map(self.deal_battery_value, content.get('data'))))
                    all_rec_1.write({'place': place})
                    return self.get_battery_data_all_continue(s, data, place, site, b'')
                else:
                    return self.get_battery_data_all_continue(s, data, place, site, b'')
            else:
                return self.get_battery_data_all_continue(s, data, place, site, self.cache_recv_msg)
        # 如果有信息就发送信息
        if err:
            for err_data in battery_err_data.get('err_info'):
                if 'many processes' in err_data.get('value'):
                    maintenance_advice = '进程太多请清理进程'
                elif 'swap space' in err_data.get('value'):
                    maintenance_advice = DISK_SPACE
                else:
                    maintenance_advice = '忽略'
                self.env['maintenance_management.call_record'].sudo().create({
                    'place': place,
                    'content': err_data.get('name'),
                    'site': site,
                    'equipment': '电源',
                    'maintenance_advice': maintenance_advice,
                    'ip_site': data[0].get('ip'),
                })
            message = [("battery_err_data", battery_err_data)]
            time.sleep(2)
            self.trigger_up_event('battery_err_data', message)

    @api.multi
    def deal_battery_value(self, value):
        value['value'] = round(value.get('value'), 4)
        return value

    @api.multi
    def equipment_monitoring(self):
        '''
        监控设备接口状态
        :return:
        '''
        try:
            bq_ats = self.search_read([('name', '=', '板桥接口状态ATS')])
            self.equipment_monitoring_all(bq_ats, '2', '板桥')
        except Exception as e:
            _logger.error('equipment_monitoring 528{}'.format(str(e)))
        try:
            bq_ci = self.search_read([('name', '=', '板桥接口状态CI')])
            self.equipment_monitoring_all(bq_ci, '1', '板桥')
        except Exception as e:
            _logger.error('equipment_monitoring 533{}'.format(str(e)))
        try:
            bq_pscada = self.search_read([('name', '=', '板桥接口状态PSCADA')])
            self.equipment_monitoring_all(bq_pscada, '3', '板桥')
        except Exception as e:
            _logger.error('equipment_monitoring 538{}'.format(str(e)))
        try:
            gdl_ci = self.search_read([('name', '=', '高大路接口状态CI')])
            self.equipment_monitoring_all(gdl_ci, '1', '高大路')
        except Exception as e:
            _logger.error('equipment_monitoring 543{}'.format(str(e)))
        try:
            gdl_pscada = self.search_read([('name', '=', '高大路接口状态PSCADA')])
            self.equipment_monitoring_all(gdl_pscada, '3', '高大路')
        except Exception as e:
            _logger.error('equipment_monitoring 548{}'.format(str(e)))

    # 判断是否退出循环
    lis_mon = []

    # 接收socket
    cache_recv_msg_mon = b''

    @api.multi
    def equipment_monitoring_all(self, data, number, place):
        state_env = self.env['maintenance_management.equipment_state']
        key_state = {
            '板桥': 'bq_state',
            '高大路': 'gdl_state',
        }
        try:
            s = socket.socket()
            s.connect((data[0].get('ip'), int(data[0].get('other'))))
            state_connects = state_env.search(
                [('line', '=', key_state.get(place))])
            for state_connect in state_connects:
                if state_connect.state == 'disconnect':
                    state_connect.write({'state': 'connection'})
                    self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                    state_connect.env.cr.commit()
            global lis_mon
            lis_mon = []
            try:
                self.equipment_monitoring_all_continue(s, data, place, b'', number)
            except Exception as f:
                _logger.error('equipment_monitoring_all 573{}'.format(str(f)))
                return ERROR_CONFIG
        except Exception as e:
            logging.info('521 {}'.format(str(e)))
            # 用来提示
            connect_state = ''
            _logger.error('equipment_monitoring_all 576')
            equipment_states = state_env.search(
                [('line', '=', key_state.get(place))])
            for equipment_state in equipment_states:
                if equipment_state.state == 'connection':
                    connect_state = '1'
                    equipment_state.env.cr.commit()
            if connect_state and key_state.get(place) == 'bq_state':
                self.trigger_up_event('connect_waring_prompt', '板桥ATS，CI，PSCADA')
                self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
            elif connect_state and key_state.get(place) == 'gdl_state':
                self.trigger_up_event('connect_waring_prompt', '高大路CI，PSCADA')
                self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
            equipment_disconnects = state_env.search(
                [('line', '=', key_state.get(place))])
            for equipment_disconnect in equipment_disconnects:
                if equipment_disconnect.state == 'connection':
                    equipment_disconnect.write({'state': 'disconnect'})
                    self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                    self.env.cr.commit()
                self.env.cr.commit()

    @api.multi
    def equipment_monitoring_all_continue(self, s, data, place, b, number):
        try:
            # 用来退出循环
            global lis_mon
            global cache_recv_msg_mon
            self.cache_recv_msg_mon = b
            while True:
                s.send('heartbeat'.encode())
                requ = s.recv(4096)
                self.cache_recv_msg_mon += requ
                pos = self.cache_recv_msg_mon.find('|'.encode())
                if pos == -1:
                    return self.equipment_monitoring_all_continue(s, data, place, b'', number)
                elif pos == 0:
                    pos = self.cache_recv_msg.decode()[1:].find('|')
                try:
                    time.sleep(0.5)
                    if '}' in self.cache_recv_msg_mon[:pos].decode():
                        size = int(self.cache_recv_msg_mon[:pos].decode().split('}')[1])
                    else:
                        size = int(self.cache_recv_msg_mon[:pos].decode())
                except Exception as f:
                    logging.error('567 {}'.format(str(f)))
                    return
                need_size = size + pos + 1
                if need_size <= len(self.cache_recv_msg_mon):
                    content = eval(self.cache_recv_msg_mon[pos + 1: size + pos + 1].decode('utf-8'))
                    lis_mon.append(content)
                    if len(lis_mon) > 3:
                        break
                    if content.get('type') == int(number):
                        content['place'] = place
                        self.env['maintenance_management.interface_state'].sudo().create(content)
                        return self.equipment_monitoring_all_continue(s, data, place, b'', number)
                else:
                    return self.equipment_monitoring_all_continue(s, data, place, self.cache_recv_msg_mon, number)
        except Exception as f:
            _logger.error('equipment_monitoring_all_continue 623{}'.format(str(f)))
            return ERROR_CONFIG

    @api.multi
    def monitor_all_equipment(self):
        '''
        监控所有的zabbix服务的设备中的告警错误
        :return:
        '''
        call_rec_env = self.env['maintenance_management.call_record']
        try:
            ip_site = self.search_read([('name', '=', ZABBIX_SERVER)], ['ip'])
            url = ZABBIX_PHP.format(ip_site[0].get('ip'))
            username = 'Admin'
            password = 'zabbix'
            data = {'jsonrpc': '2.0',
                    'method': 'user.login',
                    'params': {
                        'user': username,
                        'password': password
                    },
                    'id': 1
                    }
            value = json.dumps(data).encode('utf-8')
            req = request.Request(url, headers=HEADER, data=value)
            # 打开包装过的url
            result = request.urlopen(req, timeout=4)
            response = result.read()
            # 上面获取的是bytes类型数据，故需要decode转化成字符串
            page = response.decode('utf-8')
            # 将此json字符串转化为python字典
            page = json.loads(page)
            auth = page['result']
            neirong = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": [
                        "hostid",
                        "host"
                    ],
                    "selectInterfaces": [
                        "interfaceid",
                        "ip"
                    ]
                },
                "id": 1,
                "auth": auth
            }
            # 存放错误的数据
            all_warning_data = []
            page = self.get_response_data(url, neirong, HEADER)
            if page.get('result'):
                for zabbix_data in page.get('result'):
                    hostid = zabbix_data.get('hostid')
                    host = zabbix_data.get('host')
                    # 报警数据
                    warning_data = {
                        "jsonrpc": "2.0",
                        "method": "trigger.get",
                        "params": {
                            "output": [
                                "triggerid",
                                "description",
                                "status",
                                "value",
                                "priority",
                                "lastchange",
                                "recovery_mode",
                                "hosts",
                                "state"
                            ],
                            "filter": {
                                "value": 1
                            },
                            "hostids": hostid,
                            "min_severity": 2,
                        },
                        "auth": auth,
                        "id": 1
                    }
                    # 获取告警记录
                    warning_data_rec = self.get_response_data(url, warning_data, HEADER)
                    warning_list = warning_data_rec.get('result')
                    for warning_data_rec in warning_list:
                        equipment = self.env['maintenance_equipment'].search(
                            [('name', '=', Ten_ZABBIX_KEY.get(host))]).id
                        # 获取当前服务的报警数据
                        des = warning_data_rec.get('description').replace('on {HOST.NAME}', '')
                        if warning_data_rec.get('priority') == '2':
                            if 'many processes' in des:
                                maintenance_advice = '进程太多请清理进程'
                                equipment_des = '进程太多'
                            elif 'swap space' in des:
                                maintenance_advice = DISK_SPACE
                                equipment_des = '磁盘空间占用过高'
                            elif 'Free disk space' in des:
                                maintenance_advice = DISK_SPACE
                                equipment_des = '空闲磁盘空间过小'
                            else:
                                maintenance_advice = '忽略'
                                equipment_des = des
                            failure_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                                float(warning_data_rec.get('lastchange'))))
                            data_search = call_rec_env.search([
                                ('failure_time', '=', failure_time),
                                ('content', '=', equipment_des),
                                ('equipment', '=', equipment),
                            ])
                            if not data_search:
                                call_rec_env.create({
                                    'equipment': equipment,
                                    'content': equipment_des,
                                    'maintenance_advice': maintenance_advice,
                                    'ip_site': TEN_ZABBIX_IP.get(host),
                                    'failure_time': failure_time,
                                })
                                # 新增的报警数据
                                all_warning_data.append({
                                    'name': Ten_ZABBIX_KEY.get(host),
                                    'msg': equipment_des,
                                    'zbx': TEN_CONFIGURATION_DATA_POSITIVE.get(host),
                                })
                        else:
                            data_search_call_record = self.env['maintenance_management.diagnosis_record'].search([
                                ('equipment', '=', equipment),
                                ('content', '=', des),
                                ('ip_site', '=', TEN_ZABBIX_IP.get(host)),
                            ])
                            if not data_search_call_record and equipment:
                                self.env['maintenance_management.diagnosis_record'].create({
                                    'equipment': equipment,
                                    'content': des,
                                    'ip_site': TEN_ZABBIX_IP.get(host),
                                    'failure_time': failure_time,
                                })
            result.close()
        except Exception as f:
            _logger.error('monitor_all_equipment 849 {}'.format(str(f)))
            return ERROR_CONFIG

    @api.multi
    def change_zabbix_connect_state(self):
        '''
        用来修改zabbix 的连接状态
        :return:
        '''
        state_env = self.env['maintenance_management.equipment_state']
        ip_site = self.search_read([('name', '=', ZABBIX_SERVER)], ['ip'])
        url = ZABBIX_PHP.format(ip_site[0].get('ip'))
        auth = self.zabbix_login()
        err_image = []
        time.sleep(2)
        for data in TEN_DATAS:
            try:
                host_id = self.get_host(url, HEADER, auth, data.get('zabbix'))
                item_data = self.get_items_data(host_id, 'net.tcp.listen[10050]', auth)
                items_rec = self.get_response_data(url, item_data, HEADER).get('result')[0].get('itemid')
                get_data = self.get_item_data(url, HEADER, auth, items_rec, 'net.tcp.listen[10050]')
                if get_data['result'] and get_data['result'][-1].get('value') == '0' or not get_data['result']:
                    if state_env.search(
                            [('name', '=', data.get('image_change'))]).state == 'connection':
                        self.trigger_up_event('connect_waring_prompt', data.get('server_name'))
                        state_env.search(
                            [('name', '=', data.get('image_change'))]).write({'state': 'disconnect'})
                        self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                        self.env.cr.commit()
                        err_image.append(
                            {'image_change': data.get('image_change'), 'server_name': data.get('server_name')})
                else:
                    if state_env.search(
                            [('name', '=', data.get('image_change'))]).state == 'disconnect':
                        state_env.search(
                            [('name', '=', data.get('image_change'))]).state = 'connection'
                        self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                        self.env.cr.commit()
            except Exception as e:
                _logger.error('change_zabbix_connect_state 961{}'.format(str(e)))
                if state_env.search(
                        [('name', '=', data.get('image_change'))]).state == 'connection':
                    self.trigger_up_event('connect_waring_prompt', data.get('server_name'))
                    state_env.search(
                        [('name', '=', data.get('image_change'))]).write({'state': 'disconnect'})
                    self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
                    self.env.cr.commit()
                    err_image.append(
                        {'image_change': data.get('image_change'), 'server_name': data.get('server_name')})
        if err_image:
            for err_data in err_image:
                equipment = self.env['maintenance_equipment'].search(
                    [('name', '=', err_data.get('server_name'))]).id
                self.env['maintenance_management.call_record'].create([{
                    'equipment': equipment,
                    'content': '通信中断',
                    'maintenance_advice': '连接失败请查看',
                    'alarm_level': '高',
                }])
                self.env.cr.commit()


class BatteryDataApi(models.Model):
    _name = 'maintenance_management.battery_data_api'
    _description = '电池组UPS数据获取'

    index = fields.Char(string='索引')
    name = fields.Char(string='组名称')
    value = fields.Char(string='值')
    place = fields.Char(string='地点')


class BatteryDataApiSide(models.Model):
    _name = 'maintenance_management.battery_data_api_side'
    _description = '电池组UPS数据获取'

    channel = fields.Char(string='通道')
    index = fields.Char(string='索引')
    name = fields.Char(string='组名称')
    span = fields.Char(string='跨度')
    span_type = fields.Char(string='跨度类型')
    value = fields.Char(string='值')
    warning_value = fields.Char(string='警告值')
    place = fields.Char(string='地点')
