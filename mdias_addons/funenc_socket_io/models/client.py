# -*- coding: utf-8 -*-

import logging
import threading
from queue import Queue

from odoo.addons.odoo_operation_log.model_extend import LogManage

from odoo import models, api
from odoo import registry
from odoo.models import SUPERUSER_ID
from odoo.service.server import server
from odoo.tools import config

LogManage.register_type('socketio_client_log', "socketio client日志")

_logger = logging.getLogger(__name__)
message_queue = Queue()
client_transfer_channel = config.get('client_transfer_channel', 'FJJQLTKZLRMVXKDHGLEBRVUX')
allow_models = config.get('allow_socketio_models', '').strip().split(',')
namespace = '/' + client_transfer_channel

client_io = None
web_socket_client = None
msg_stack = []
model_env = None


if getattr(server, 'main_thread_id') \
        == threading.currentThread().ident:

    import socketio
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client_io = socketio.AsyncClient(reconnection_delay=5)


async def background_work_thread(msg_que):
    '''
    后台任务线程
    :return:
    '''
    while True:
        await client_io.sleep(0.01)
        msg = msg_que.get()
        await client_io.emit('app_mdias_info', msg, namespace=namespace)


def start_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(background_work_thread(message_queue))
    loop.run_forever()


async def start_server():
    socket_host = config.options.get('socket_io_app_server', '') or '0.0.0.0:9080'
    url = 'http://' + socket_host
    _logger.info('await client_io.connect{url}'.format(url=url))
    await client_io.connect(url)
    _logger.info('await client_io.connect')
    await client_io.wait()


class ClientThread(threading.Thread):
    '''
    服务器线程
    '''

    def __init__(self, db_registry, *args, **kwargs):
        self.db_registry = db_registry
        super(ClientThread, self).__init__(args=args, kwargs=kwargs)

    def run(self):
        @client_io.on('connect')
        async def on_connect():
            '''
            连接成功
            :return:
            '''
            _logger.info('connect to app server success!')
            LogManage.put_log(content="socketio 客户端已经联接", mode="socketio_client_log")

        @client_io.on('disconnect')
        async def disconnect():
            '''
            断开连接
            :return:
            '''
            _logger.info('the app server connect is dropped!')
            LogManage.put_log(content="socketio 客户端断开!", mode="socketio_client_log")

        @client_io.on('transfer_to_server_client', namespace=namespace)
        async def socket_info_data(data):
            """
                接受中转服务器的消息
            :param data:
            :return:
            """
            result = self.deal_event(data)
            _logger.info('接收中专服务器消息:{data}'.format(data=result))
            return result

        _logger.info('启动服务')
        loop.run_until_complete(start_server())

    @staticmethod
    async def inner_run():
        '''
        内部运行
        :return:
        '''
        socket_host = config.options.get('socket_io_app_server', '') or '0.0.0.0:9080'
        url = 'http://' + socket_host
        _logger.info('connect to socketio server, address %s' % url)
        LogManage.put_log(content='connect to socketio server, address %s' % url, mode="socketio_client_log")

        # 服务端有可能还没启动，client_io在第一次连接成功以后才会重联
        connected = False
        await client_io.connect(url)
        await client_io.wait()
        LogManage.put_log(content="客户退退出!", mode="socketio_client_log")

    def deal_event(self, data=None):
        """
            处理事件消息，类似rpc
        :param data:
        :return:
        """
        LogManage.put_log(content="收到中转服务器请求", mode="socketio_client_log")
        try:
            with api.Environment.manage(), self.db_registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                model_name = data.get('model', False)
                model = env[model_name]

                args = data.get('args', [])
                kwargs = data.get('kwargs', {})
                data_rec = getattr(model, data.get('method'))(*args, **kwargs)
                LogManage.put_log(content="socketio客户端数据处理完成", mode="socketio_client_log")
                return data_rec
        except Exception as error:
            LogManage.put_log(content="处理中转服务器请求出错{error}".format(error=error),
                              mode="socketio_client_log")
            return False


class FunencSocketIo(models.Model):
    '''
    富能通 socket io
    '''
    _name = 'funenc.socket_io_client'

    def _register_hook(self):
        '''
        启动服务, 如果为安装模式则不启动
        :return:
        '''
        if getattr(server, 'main_thread_id') \
                != threading.currentThread().ident:
            return

        global web_socket_client
        db_name = config.options['db_name']
        db_registry = registry(db_name)
        web_socket_client = ClientThread(db_registry).start()
        threading.Thread(target=start_task).start()

    @api.model
    def post_message_to_app_server(self, data):
        '''
            给app服务发送消息
            :return:
        '''
        message_queue.put(data)
