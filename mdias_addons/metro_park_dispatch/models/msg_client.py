# -*- coding: utf-8 -*-

import socket
import select
import time
import json
from odoo import models, api, exceptions
import logging
from functools import partial
from odoo.tools import config
from queue import Queue
import threading
import pendulum
from pprint import pprint

from odoo.service.server import server
from ...odoo_operation_log.model_extend import LogManage

if config.options.get('local_debug', False):
    from .data_test import park_train_back_conditions_map
else:
    from .data import park_train_back_conditions_map

LogManage.register_type('ats_log', "ats传输日志")
LogManage.register_type('interlock', "联锁日志")

inter_lock_lock = threading.Lock()
msg_lock = threading.Lock()

_logger = logging.getLogger(__name__)

inited = False

model_env = None
sio = None
app = None
thread = None
msg_stack = []

time_table_request_stack = []
time_table_data = []

global_train_cache = {}
global_sdi_info = {}

cur_line_code = None
cur_line_info = None


class TransitClient:

    def __init__(self, server_addr, log_type):
        self.log_type = log_type
        self.read_callback = None
        self.running = False
        self.write_list = Queue()
        self.deal_msg_list = Queue()
        self.server_addr = server_addr
        self.socket = None
        self.cache_recv_msg = b''
        self.last_heartbeat = pendulum.now('UTC').format('YYYY-MM-DD HH:mm:ss')
        self.heartbeat_thread = None
        self.heartbeat_detect_thread = None
        self.heartbeat_lock = None
        self.deal_content_thread = None
        self.heart_beat_count = 0

    def start_heartbeat_thread(self):
        '''
        启用心跳线程
        :return:
        '''

        def loop():
            while self.running:
                self.write('heartbeat')
                time.sleep(1)

        self.heartbeat_thread = threading.Thread(target=loop, args=())
        self.heartbeat_thread.start()

    def start_deal_content_thread(self):
        '''
        启用心跳线程
        :return:
        '''
        def loop():
            count = 0
            while self.running:
                try:
                    if count > 50:
                        count = 0
                        LogManage.put_log(content="处理数据{address}, 剩余消息{count}"
                                          .format(address=self.server_addr,
                                                  count=self.deal_msg_list.qsize()),
                                          mode=self.log_type)
                    else:
                        count += 1
                    content = self.deal_msg_list.get()
                    if self.read_callback:
                        self.read_callback(content)
                except Exception as error:
                    try:
                        LogManage.put_log(
                            content="处理数据出错{address}, {error}".format(
                                address=self.server_addr, error=error), mode=self.log_type)
                    except Exception as error:
                        _logger.info(
                            "put log error! {error}".format(error=error))

        self.deal_content_thread = threading.Thread(target=loop, args=())
        self.deal_content_thread.start()

    def start_heartbeat_detect_thread(self):
        '''
        启用心跳线程
        :return:
        '''
        def loop():
            while self.running:
                try:
                    self.heartbeat_lock.acquire()
                    now_time = pendulum.now('UTC')
                    last_heartbeat = pendulum.parse(self.last_heartbeat)
                    delta = now_time - last_heartbeat
                    if delta.seconds > 30:
                        _logger.info('the heartbeat start time is {start_time}, '
                                     'and the end time is: {end_time} and the delta is {delta}'
                                     .format(start_time=last_heartbeat.format('mm:ss'),
                                             end_time=now_time.format('mm:ss'),
                                             delta=delta.seconds))
                    self.heartbeat_lock.release()
                    if delta.seconds > 30:
                        # 这个里边如果再去join是不会成功的
                        self.do_close(False)
                        break
                except Exception as error:
                    _logger.info(
                        'deal heartbeat error! {error}'.format(error=error))
                time.sleep(1)

        self.heartbeat_detect_thread = threading.Thread(target=loop, args=())
        self.heartbeat_detect_thread.start()

    def do_connect(self):
        try:
            _logger.info("begin connect host!")
            LogManage.put_log(content="开始连接服务器{address}"
                              .format(address=self.server_addr),
                              mode=self.log_type)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_addr)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.setblocking(0)
            self.running = True
            self.last_heartbeat = pendulum.now(
                'UTC').format('YYYY-MM-DD HH:mm:ss')
            self.heartbeat_lock = threading.Lock()
            self.start_heartbeat_thread()
            self.start_heartbeat_detect_thread()
            self.start_deal_content_thread()
            _logger.info("连接服务器{address}成功!".format(address=self.server_addr))
            LogManage.put_log(content="连接服务器{address}成功!".format(address=self.server_addr),
                              mode=self.log_type)
            return True
        except Exception as error:
            # 关闭socket时有可能会出错
            try:
                if self.socket:
                    self.socket.close()
                LogManage.put_log(content="连接服务器出错{address}, {error}"
                                  .format(address=self.server_addr, error=error),
                                  mode=self.log_type)
            except Exception as error:
                LogManage.put_log(content="关闭socket出错{address}, {error}"
                                  .format(address=self.server_addr, error=error),
                                  mode=self.log_type)
            return False

    def connect_server(self):
        while not self.do_connect():
            time.sleep(1)

    def do_close(self, join_detect_thread=True):
        '''
        关闭通道
        :return:
        '''
        LogManage.put_log(content="关闭连接{address}"
                          .format(address=self.server_addr),
                          mode=self.log_type)
        self.running = False
        self.write_list.empty()
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
        except Exception as error:
            LogManage.put_log(content="关闭socket出错{address}, {error}"
                              .format(address=self.server_addr, error=error), mode=self.log_type)
        self.cache_recv_msg = b''
        self.deal_msg_list.put('')
        self.heartbeat_thread.join()
        self.deal_content_thread.join()

        if join_detect_thread:
            self.heartbeat_detect_thread.join()
        LogManage.put_log(content="关闭连接成功{address}"
                          .format(address=self.server_addr),
                          mode=self.log_type)

    def set_read_callback(self, callback):
        self.read_callback = callback

    def write(self, msg):
        self.write_list.put(msg)

    def do_write(self):
        try:
            if self.write_list.qsize() > 0 and self.running:
                msg = self.write_list.get()
                send_data = bytes(self.format_msg(msg), 'utf-8')
                self.socket.send(send_data)
            return True
        except socket.error as identifier:
            # 如果是已经重启则不再报错，略过
            if not self.running:
                return True
            LogManage.put_log(content="写入数据出错!{error}".format(
                error=identifier), mode=self.log_type)
            _logger.info('send data error {identifier}'.format(
                identifier=identifier))
            return False

    def do_read(self):
        try:
            data = self.socket.recv(4096)
            self.cache_recv_msg += data
            self.parse_data()
            return True
        except Exception as e:
            LogManage.put_log(content="读取数据出错!{error}"
                              .format(error=e), mode=self.log_type)
            return False

    @staticmethod
    def format_msg(msg):
        return '%d|%s' % (len(msg), msg)

    def parse_data(self):
        try:
            pos = self.cache_recv_msg.find('|'.encode())
            if pos == -1:
                return
            size = int(self.cache_recv_msg[: pos])
            need_size = size + pos + 1
            if need_size <= len(self.cache_recv_msg):
                content = self.cache_recv_msg[pos +
                                              1: size + pos + 1].decode('utf-8')
                # 特殊处理心跳消息
                self.heartbeat_lock.acquire()
                # 防止对象在多线程中使用出
                self.last_heartbeat = pendulum.now(
                    'UTC').format('YYYY-MM-DD HH:mm:ss')
                self.heartbeat_lock.release()

                if content == "heartbeat":
                    # 每隔3分钟记录一次日志
                    if self.heart_beat_count > 60:
                        self.heart_beat_count = 0
                        LogManage.put_log(content="收到心跳消息!{address}"
                                          .format(address=self.server_addr), mode=self.log_type)
                    else:
                        self.heart_beat_count += 1
                elif self.read_callback:
                    self.deal_msg_list.put(content)
                else:
                    print('receive data:', content)

                self.cache_recv_msg = self.cache_recv_msg[need_size:]

                self.parse_data()
        except Exception as e:
            try:
                LogManage.put_log(content="解析数据出错，重新连接服务器!{error}"
                                  .format(error=e), mode=self.log_type)
                _logger.info("解析数据出错，重新连接服务器, {error}".format(error=e))
                self.do_close()
            except Exception as error:
                _logger.info(error)
            self.connect_server()

    def run(self):
        while True:
            try:
                if self.running:
                    sock_read, sock_write, sock_error = select.select(
                        [self.socket], [self.socket], [self.socket])
                    ret = True
                    if sock_write and self.write_list.qsize() > 0:
                        ret = self.do_write()
                    if sock_read:
                        ret = self.do_read()
                    if sock_error or not ret:
                        LogManage.put_log(content="sock_error!{sock_error}"
                                          .format(sock_error=sock_error), mode=self.log_type)
                        self.running = False
                    time.sleep(0.01)
                else:
                    LogManage.put_log(content="网络select出错!",
                                      mode=self.log_type)
                    self.do_close()
                    self.connect_server()
            except Exception as error:
                try:
                    LogManage.put_log(
                        content="服务器非正常处理!{error}".format(error=error), mode=self.log_type)
                    self.do_close()
                except Exception as error:
                    _logger.info(error)
                self.connect_server()


class TransitThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        # 这里会调用父类的所有有初始化方法
        super(TransitThread, self).__init__(args=args, kwargs=kwargs)

        self.host = args[0]
        self.port = args[1]
        self.name = args[3]
        self.client = TransitClient((self.host, self.port), self.name)
        self.client.set_read_callback(args[2])

    def run(self):
        self.client.connect_server()
        self.client.run()

    def send_message(self, msg):
        '''
        写入消息
        :param msg:
        :return:
        '''
        self.client.write(msg)


class MsgClientModel(models.Model):
    '''
    封装，便于访问后端
    '''
    _name = 'metro_park_dispatch.msg_client'
    _description = '消息收发客户端'

    @api.model_cr
    def _register_hook(self):
        """
        stuff to do right after the registry is built
        """

        if getattr(server, 'main_thread_id') \
                != threading.currentThread().ident:
            return

        global cur_line_code
        global cur_line_info

        global inited
        if inited:
            return
        inited = True

        global model_env
        model_env = self

        line_records = self.env['metro_park_base.line'].search([])
        if line_records:
            cur_line_code = line_records[0].code
            cur_line_info = park_train_back_conditions_map[cur_line_code]
        else:
            _logger.info('线路基础数据未配置')
            return

        # ats客户端
        cur_line_info['ats_client']['instance'] = TransitThread(
            cur_line_info['ats_client']['host'], cur_line_info['ats_client']['port'], self.ats_msg_call_back, 'ats_log')
        cur_line_info['ats_client']['instance'].start()

        for park in cur_line_info['park_list']:
            park['model'] = self.env.ref(
                "metro_park_base_data_%s.%s" % (cur_line_code, park['rtu_name']))
            for client in park['interlock_client']:
                LogManage.register_type('%sinterlock_%s_log' % (
                    park['rtu_name'], client['tag']), "%s联锁%s机日志" % (park['name'], client['tag']))
                client['instance'] = \
                    TransitThread(client['host'], client['port'],
                                  partial(self.inter_lock_call_back, park['model'].id), '%s_interlock_%s_log' % (park['rtu_name'], client['tag']))
                client['instance'].start()
        pprint(cur_line_info)

    @api.model
    def get_time_tables(self, infos):
        '''
        取得所有的时刻表
        :return:
        '''
        global time_table_request_stack
        if len(time_table_request_stack) > 0:
            raise exceptions.ValidationError("正在获取时刻表，请稍候再试")

        time_table_request_stack = infos
        if len(infos) > 0:
            info = time_table_request_stack.pop(0)
            self.get_time_table(info["location"], info["date"])

    @api.model
    def get_time_table(self, location, date_string):
        '''
        获取时刻表, 由于这里有其它线路需要重写这个函数，时间原因，暂时没考虑其它更好的方法
        :return:
        '''
        for park in cur_line_info['park_list']:
            if location == park['model'].id:
                cur_line_info['ats_client']['instance'].send_message(json.dumps({
                    "cmd": "get_time_table",
                    "data": {
                        "date": date_string,
                        "location": park['rtu_id']
                    }
                }))
                break
        else:
            _logger.error("位置代码不正确")

    @api.model
    def request_map_state(self, location):
        '''
        请求站场全局信息, 由于不能区分哪个是主机，哪个是备机，所以两台机器都发送，由服务程序去处理
        '''
        for park in cur_line_info['park_list']:
            if location == park['model'].id:
                for client in park['interlock_client']:
                    client['instance'].send_message(json.dumps({
                        "cmd": "get_map_state",
                        "data": {}
                    }))
                break
        else:
            _logger.error("位置代码不正确")

    @api.model
    def get_cur_train_info(self, location):
        '''
        取得现车信息  # 99 高大路， 98板桥, 17 板桥部出入线段(双流西), 26 高大路出入段线(新平)
        :return:
        '''
        for park in cur_line_info['park_list']:
            if location == park['model'].id:
                cur_line_info['ats_client']['instance'].send_message(json.dumps({
                    "cmd": "get_cur_train_info",
                    "data": {
                        "location": park['rtu_id']
                    }
                }))
                break
        else:
            _logger.error("位置代码不正确")

    @staticmethod
    def ats_msg_call_back(state):
        '''
        ats消息回调
        {
            "Dev_name":"T1209",
            "Dev_type":5,
            "Driver_id":"000",
            "Global_id":"102",
            "MDIAS_window":0,
            "MDIAS_window_offset":0,
            "Rtu_id":13,
            "Train_id":"102",
            "Train_index":"",
            "msg_id":16,
            "rollingstock":0,
            "route_id":0,
            "speed":0,
            "type":2
        },
        "data_type":"DATA_ATS"}
        :return:
        '''
        if not state:
            return

        try:
            model_env.deal_ats_msg(state)
        except Exception as error:
            import traceback
            traceback.print_exc()
            _logger.info(error)
            LogManage.put_log(content="ats处理数据出错{error}".format(
                error=error), mode="ats_log")

    @staticmethod
    def inter_lock_call_back(location, msg):
        '''
        联销消息回调
        :param location:
        :param msg:
        :return:
        '''
        if not msg:
            return

        try:
            model_env.deal_interlock_msg(location, msg)
        except Exception as e:
            _logger.info('deal interlock msg error {error}'.format(error=e))

    @api.model
    def get_all_unfinished_plan(self, location_alias):
        '''
        取得所有的计划
        :return:
        '''
        # 调车计划
        dispatch_plans = self.env["metro_park_dispatch.dispatch_notice"] \
            .get_unfinished_plans(location_alias)

        # 收发车计划
        day_plan_datas = self.env['metro_park_dispatch.day_run_plan'] \
            .get_unfinished_plans(location_alias)

        return dispatch_plans + day_plan_datas

    @api.model
    def deal_ats_msg(self, state):
        '''
        处理ats信息
        :return:
        '''
        global time_table_data
        with api.Environment.manage():
            with self.pool.cursor() as new_cr:
                # 需要添下面这句, 不然多线程会出现事务同步错误
                new_cr.autocommit(True)
                self = self.with_env(self.env(cr=new_cr))
                state = json.loads(state)
                data = state["data"]
                if isinstance(data, dict):
                    datas = [data]
                else:
                    datas = data

                for data in datas:
                    msg_id = data["msg_id"]
                    # 处理列车位置
                    if msg_id == 9:
                        if data["trains"]:
                            self.set_trains_state(data["trains"])
                    elif msg_id == 16:
                        '''
                        这个是单列车的变更信息
                        {
                            'Dev_name': 'T1205',
                            'Dev_type': 5,
                            'Driver_id': '000',
                            'Global_id': '101', // 车次号
                            'MDIAS_window': 0,
                            'MDIAS_window_offset': 0,
                            'Rtu_id': 12,
                            'Train_id': '106', // 车组号
                            'Train_index': '',
                            'msg_id': 16,
                            'rollingstock': 0,
                            'route_id': 0,
                            'speed': 0,
                            'type': 2
                        }
                        '''
                        self.set_trains_state([data])
                    elif msg_id == 17:
                        pass
                    elif msg_id == 34 and data["sub_id"] == 1:
                        time_table_data = []
                        _logger.info("begin get time table data")
                    elif msg_id == 34 and data["sub_id"] == 2:
                        time_table_data.append(data)
                    elif msg_id == 34 and data["sub_id"] == 3:
                        _logger.info("finish get time table data")
                        if len(time_table_request_stack) > 0:
                            info = time_table_request_stack.pop(0)
                            self.get_time_table(info["location"], info["date"])
                        else:
                            self.env["metro_park_base.time_table"].deal_new_time_table_data(
                                time_table_data)

    @api.model
    def set_trains_state(self, trains):
        '''
        设置更车状态
        :return:
        '''
        for train in trains:
            Train_id = train["Train_id"]  # 车底号
            Rtu_id = train["Rtu_id"]
            Dev_name = train["Dev_name"]

            if len(Train_id) == 3:
                # ats的车底号是三位，场内的车底号是2位
                Train_id = '110' + Train_id[1:]

            cur_park = None
            for park in cur_line_info['park_list']:
                for rtu_rails in park['special_station_rails']:
                    if Dev_name in rtu_rails['rails'] and rtu_rails['rtu_id'] == Rtu_id:
                        if park['add_end_tag']:
                            Dev_name += "G"
                        cur_park = park
                        break
            if cur_park:
                Dev_name = Dev_name.upper()  # 位置
                Global_id = train["Global_id"]  # 车次号
                if 'model' in cur_park:
                    info = "{location} - {name} - {Train_id} - {Global_id}".format(
                        location=cur_park['model'].id,
                        name=Dev_name,
                        Train_id=Train_id,
                        Global_id=Global_id)
                    _logger.info(info)
                    LogManage.put_log(content=info, mode="ats_log")

                    # 在车场内, 放在try中，更新位置失败不影响收发车
                    try:
                        cur_train_id = self.env["metro_park_dispatch.cur_train_manage"]\
                            .update_position(cur_park['model'].id, Train_id, Dev_name)
                    except Exception as error:
                        LogManage.put_log(content="更新ats位置出错 {error}".format(error=error),
                                          mode="ats_log")
                        run_train = self.env["metro_park_dispatch.cur_train_manage"]\
                            .search([("train.dev_no", "=", Dev_name)])
                        if not run_train:
                            # 没有就创建车辆
                            run_train = self.env["metro_park_dispatch.cur_train_manage"]\
                                .create_run_train(Dev_name, cur_park['model'].id)
                        cur_train_id = run_train.id

                    # 检查车辆所处位置是否是出入段线，然后再检查照查状态，然后再检查计划信息
                    LogManage.put_log(content="开始检查车辆回库", mode="ats_log")
                    self.env["metro_park_dispatch.train_back_plan"]\
                        .check_train_back(cur_park, Dev_name, cur_train_id, Global_id)

    @api.model
    def deal_interlock_msg(self, location, state):
        '''
        处理联锁消息
        :return:
        '''
        with api.Environment.manage():
            with self.pool.cursor() as new_cr:
                try:
                    new_cr.autocommit(True)
                    self = self.with_env(self.env(cr=new_cr))
                    state = json.loads(state)
                    msg = state['data_type']
                    if msg in ['DATA_SDI', 'DATA_SDCI']:
                        _logger.info(
                            "begin deal inter lock msg: {location}".format(location=location))
                        datas = state["data"]
                        # 由于存在多个道岔同时更新的情况，所以，在处理车辆变动时，先更新状态，再检查车辆
                        for data in datas:
                            # 转换为大写
                            data['name'] = str(data['name']).upper()
                            data_type = data["type"]
                            if data_type == 1:  # 道岔
                                try:
                                    self.env["metro_park_base.switches"] \
                                        .update_status(location, data)
                                except Exception as tmp_error:
                                    LogManage.put_log(content="更新道岔信息出错{data}, {error}".format(
                                        data=data, error=tmp_error), mode="interlock")
                            elif data_type == 2:  # 区段
                                try:
                                    self.env["metro_park_base.rails_sec"] \
                                        .update_status(location, data)
                                except Exception as tmp_error:
                                    LogManage.put_log(content="更新区段信息出错{data}, {error}".format(
                                        data=data, error=tmp_error), mode="interlock")
                            elif data_type in [3, 4, 5]:  # 信号机
                                try:
                                    self.env["metro_park_base.signals"] \
                                        .update_status(location, data)
                                except Exception as tmp_error:
                                    LogManage.put_log(content="更新信号机出错{data}, {error}".format(
                                        data=data, error=tmp_error), mode="interlock")
                            elif data_type == 6:  # 表示灯(含照查灯信息)
                                try:
                                    self.env["metro_park_base.indicator_light"] \
                                        .update_status(location, data)
                                except Exception as tmp_error:
                                    LogManage.put_log(content="更新表示灯出错{data}, {error}".format(
                                        data=data, error=tmp_error), mode="interlock")

                        # 二次处理, 如果是全局数据, 那么替换成sdci数据
                        if msg == "DATA_SDI":
                            global global_sdi_info
                            first_init = False
                            if location not in global_sdi_info:
                                first_init = True
                            if location not in global_sdi_info:
                                global_sdi_info[location] = {}
                                for data in datas:
                                    index = data["index"]
                                    global_sdi_info[location][index] = data
                                if first_init:
                                    _logger.info(
                                        "deal inter lock msg finished!")
                                    return
                            else:
                                diff_datas = []
                                old_datas = global_sdi_info[location]
                                # 只关心道岔和区段的占压状态
                                for data in datas:
                                    data_type = data["type"]
                                    if data_type == 1 or data_type == 2:
                                        index = data["index"]
                                        if index in old_datas:
                                            old_data = old_datas[index]
                                            if old_data["hold"] != data["hold"]:
                                                # 取得不同数据
                                                diff_datas.append(data)
                                                # 更新全局数据
                                                old_datas[index] = data
                                        else:
                                            old_datas[index] = data
                                # 更新变化数据
                                datas = diff_datas
                        else:
                            # 更新变化数据到全局数据
                            for tmp_data in datas:
                                data_type = data["type"]
                                # 只关心道岔和区段的占压状态
                                if data_type == 1 or data_type == 2:
                                    old_datas = global_sdi_info[location]
                                    index = tmp_data["index"]
                                    old_datas[index] = tmp_data

                        # 局部更新
                        hold_switches = []
                        release_switches = []
                        for data in datas:
                            data_type = data["type"]
                            if data_type == 1:  # 道岔
                                name = data["name"]
                                name = name.replace('_', "/")
                                # 只关心hold状态的
                                if data["hold"] == 1:
                                    LogManage.put_log(content="联锁{name}被占压".format(
                                        name=name), mode="interlock")
                                    hold_switches.append(name)
                                else:
                                    LogManage.put_log(content="联锁{name}被释放".format(
                                        name=name), mode="interlock")
                                    release_switches.append(name)
                            elif data_type == 2:  # 区段
                                name = data["name"]
                                if data['hold'] == 1:
                                    LogManage.put_log(content="联锁{name}被占压".format(
                                        name=name), mode="interlock")
                                else:
                                    LogManage.put_log(content="联锁{name}被释放".format(
                                        name=name), mode="interlock")
                                # 更新位置
                                self.env["metro_park_base.rails_sec"] \
                                    .update_train_info(location, data)

                        # 由于道岔可能一次可能给多个出来，所以这里通过多次调用的形式来逐个递进
                        # 也有可能联锁给了多余的信息过来，但也不影响，最多多计算下
                        black_switches = []
                        # 处理占压的switch
                        for switch_name in hold_switches:
                            if switch_name in black_switches:
                                continue

                            # 需要找出同时占压的道岔, 所以将本批次的道岔全部放进去
                            self.env["metro_park_base.switches"] \
                                .update_train_info(location, switch_name, hold_switches, black_switches, True)

                        black_switches = []
                        for switch_name in release_switches:
                            if switch_name in black_switches:
                                continue
                            # 需要找出同时占压的道岔, 所以将本批次的道岔全部放进去
                            self.env["metro_park_base.switches"] \
                                .update_train_info(location, switch_name, release_switches, black_switches, False)

                        _logger.info("deal inter lock msg finished!")
                except Exception as error:
                    LogManage.put_log(content="some thing is error while deal interlock msg {error}"
                                      .format(error=error), mode="interlock")
                    raise error
