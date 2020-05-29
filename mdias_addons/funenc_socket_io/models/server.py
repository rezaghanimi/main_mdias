# -*- coding: utf-8 -*-

import asyncio
import copy
import logging
import threading
from functools import partial
from queue import Queue

from odoo.addons.odoo_operation_log.model_extend import LogManage
from sanic import Sanic
try:
    from socketio import AsyncServer
except:
    pass

from odoo import models, api, tools
from odoo.http import root
from odoo.service.server import server
from odoo.tools import config
LogManage.register_type('socketio_log', "socketio日志")

# 过滤socketio日志
logging.getLogger('socketio').setLevel(logging.WARNING)
logging.getLogger('engineio').setLevel(logging.WARNING)

_logger = logging.getLogger(__name__)
message_queue = Queue()

sio = None
msg_stack = []
model_env = None


async def execute_msg(msg):
    '''
    后台任务发送消息
    :return:
    '''
    count = 0
    try:
        if msg["msg_type"] and msg["data"]:
            _logger.info("begin deal socketio msg...!")
            room = msg.get("room", None)
            callback_info = msg.get("callback_info", None)
            if callback_info:
                def call_back(_callback_info, *args, **kwargs):
                    try:
                        res_ids = _callback_info.get('ids', [])
                        context = _callback_info.get('context', [])
                        model_env.deal_event(data={
                            "msg_type": "call",
                            "uid": _callback_info.get("uid", None),
                            "room": room,
                            "model": _callback_info["model"],
                            "name": _callback_info["name"],
                            'res_ids': res_ids,
                            "args": args,
                            "kwargs": kwargs,
                            'context': context
                        })
                    except Exception as callback_error:
                        import traceback
                        traceback.print_exc()
                        _logger.error(callback_error)
                        LogManage.put_log(content="消息回调处理异常{error}".format(error=callback_error),
                                          mode="socketio_log")

                await sio.emit(msg["msg_type"],
                               data=msg["data"],
                               to=msg.get("sid", None),
                               callback=partial(call_back, copy.deepcopy(callback_info)),
                               room=room)
            else:
                await sio.emit(msg["msg_type"],
                               data=msg["data"], to=msg.get('sid', None), room=room)
            _logger.info("deal socketio msg finished...!")
            # 用于查看后台是否正常运行
            if count > 50:
                count = 0
                LogManage.put_log(content="socketio 后台服务处理数据完成!", mode="socketio_log")
            else:
                count += 1
    except Exception as tmp_error:
        import traceback
        traceback.print_exc()
        _logger.error(tmp_error)
        LogManage.put_log(content="消息处理异常{error}".format(error=tmp_error),
                          mode="socketio_log")


class WebSocketThread(threading.Thread):
    '''
    服务器线程
    '''

    def __init__(self, *args, **kwargs):
        # 这里会调用父类的所有有初始化方法
        super(WebSocketThread, self).__init__(args=args, kwargs=kwargs)

    async def client_queue_message(self):
        while True:
            await sio.sleep(0.01)
            while message_queue.qsize() > 0:
                msg = message_queue.get()
                await execute_msg(msg)

    def start_client_event(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            asyncio.ensure_future(self.client_queue_message())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def run(self):
        global sio
        global app

        if sio:
            return

        sio = AsyncServer(async_mode='sanic',
                          cors_allowed_origins=[],
                          allow_upgrades=True,
                          transports=['websocket'],
                          ping_interval=15,
                          ping_timeout=25,
                          engineio_logger=False)
        app = Sanic()
        sio.attach(app)

        @sio.on('funenc_socketio_client_msg')
        def mdias_event(sid, data):
            _logger.debug(
                "get mdias msg: {data} with sid {sid}".format(data=data, sid=sid))
            return model_env.deal_event(sid, data)

        @sio.event
        async def connect(sid, environ):
            return model_env.deal_user_connect(sid, environ)

        @sio.event
        async def disconnect(sid):
            model_env.deal_user_disconnect(sid)

        # 必需放在服务线程中, 否则会报utf8错误
        threading.Thread(target=self.start_client_event).start()
        port = 9080
        app.config['CORS_SUPPORTS_CREDENTIALS'] = True
        host = config['socket_io_host'] or '0.0.0.0'
        app.run(host=host, port=port, register_sys_signals=False)


class FunencSocketIo(models.Model):
    '''
    富能通 socket io
    '''
    _name = 'funenc.socket_io'

    def _register_hook(self):
        '''
        启动服务, 如果为安装模式则不启动
        :return:
        '''
        if getattr(server, 'main_thread_id') \
                != threading.currentThread().ident:
            return

        global model_env
        model_env = self

        WebSocketThread().start()

    @api.model
    def get_config(self):
        '''
        取得服务器配置
        :return:
        '''
        host = config['socket_io_host'] or '0.0.0.0'
        port = tools.config.get("socket_io_port", False) or "9080"
        return {
            "websocket_host": host,
            "websocket_port": port
        }

    @classmethod
    def get_sio_cookies(cls, environ):
        '''
        从sio取得cookie
        :param environ:
        :return:
        '''
        try:
            cookie = {}
            if 'HTTP_COOKIE' in environ and environ['HTTP_COOKIE']:
                http_cookie = environ['HTTP_COOKIE'].strip().split(';')
                for ck in http_cookie:
                    k, v = ck.strip().split('=')
                    cookie[k] = v
                return cookie
            return None
        except Exception as tmp_error:
            _logger.info(
                "can not get cookie: {environ}".format(environ=environ))
            LogManage.put_log(content='处理cookie发生错误 {error}'.format(error=tmp_error),
                              mode="socketio_log")

    @classmethod
    def get_uid_id_from_sio(cls, environ):
        '''
        取得session_id, 用于从odoo查询用户信息
        :param environ:
        :return:
        '''
        cookies = cls.get_sio_cookies(environ)
        if cookies:
            session_id = cookies.get("session_id", None)
            if not session_id:
                return False
            try:
                session_info = root.session_store.get(session_id)
                if not session_info:
                    _logger.info("the user is login out!")
                    return False
            except Exception as tmp_error:
                _logger.info("get session store error, {error}".format(error=tmp_error))
                LogManage.put_log(content='get session store error {error}'.format(error=tmp_error),
                                  mode="socketio_log")
            uid = session_info.get('context', {}).get("uid", False)
            return uid
        else:
            return False

    @classmethod
    def uid_to_sids(cls, uid):
        '''
        uid转化成为sid, 还可以根据这个做离线提示,
        可能存在单个用户多个地方登录的情况，所以返回的是个数组，同样，保存的时候也是一个数组
        :return:
        '''
        return sio.environ.get("mdias_uid_" + str(uid), False)

    @api.model
    def send_broadcast_msg(self, msg, callback_info=None, room=None):
        '''
        发送广播消息, 测试使用
        :return:
        '''
        msg = {
            "msg_type": 'funenc_socketio_server_msg',
            "data": msg,
            "room": room,
            "callback_info": callback_info
        }
        if not callback_info:
            del msg["callback_info"]

        message_queue.put(msg)

    @api.model
    def send_msg_to_user(self, msg, uid, callback_info=None):
        '''
        发送消息给用户, 如果有uid的话则发送给特定用户
        callback_info: 和rpc调用参数相同
        :return:
        '''
        sids = self.uid_to_sids(uid)

        for sid in sids:
            msg = {
                "msg_type": 'funenc_socketio_server_msg',
                "data": msg,
                "sid": sid,
                "uid": uid,
                "callback_info": callback_info
            }
            if not callback_info:
                del msg["callback_info"]
            message_queue.put(msg)

    @api.model
    def deal_user_connect(self, sid, environ):
        '''
        处理用户连接, 绑定uid, 如果有uid则进行绑定，如果没有的话则不处理, 兼容非odoo的连接
        :return: True, 不管如何样都返回True, 否则连接不会成功
        '''
        _logger.info('new connection {sid} with env: {env}'.format(
            sid=sid, env=environ))
        uid = self.get_uid_id_from_sio(environ)
        if uid:
            uid_key = "funenc_socket_io_uid_" + str(uid)
            old_sids = sio.environ.get(uid_key, False)
            if old_sids:
                sio.environ[uid_key].append(sid)
            else:
                sio.environ[uid_key] = [sid]
            sio.environ["funenc_socket_io_sid_" +
                        str(sid)] = "funenc_socket_io_uid_" + str(uid)

        # 通过querystring进入某个房间
        query_string = environ["QUERY_STRING"]
        params = query_string.split("&")
        for param in params:
            item = param.split("=")
            if len(item) > 0 and item[0] == "room" and item[1] and item[1] != "":
                sio.enter_room(sid, item[1])

        return True

    @api.model
    def deal_user_disconnect(self, sid):
        '''
        处理用户断开, 清除用户信息
        :return:
        '''
        sid_key = "funenc_socket_io_sid_" + str(sid)
        uid_key = sio.environ.get(sid_key, False)
        if uid_key:
            sids = sio.environ[uid_key]
            sids.remove(sid)
            del sio.environ[sid_key]

    @api.model
    def deal_custom_event(self, sid, data):
        '''
        处理自定义的event, 其它模块调用这个函数进行扩展
        子类调用的时候注意调用父类消息处理函数
        :return:
        '''
        _logger.info("deal custom msg {sid}, {data}".format(
            sid=sid, data=data))

    @api.model
    def deal_normal_socketio_msg(self, sid, data):
        '''
        处理自定义的event, 其它模块调用这个函数进行扩展
        子类调用的时候注意调用父类消息处理函数
        :return:
        '''
        _logger.info("deal custom msg {sid}, {data}".format(
            sid=sid, data=data))

    @api.model
    def deal_event(self, sid=None, data=None):
        '''
        处理消息
        :return:
        '''
        with api.Environment.manage():
            with self.pool.cursor() as new_cr:
                new_cr.autocommit(True)
                self = self.with_env(self.env(cr=new_cr))
                if 'model' in data and 'name' in data:
                    kwargs = data.get('kwargs', {})
                    args = data.get('args', [])
                    model = self.env[data["model"]]
                    res_ids = data.get('ids', [])

                    context = data.get('context', {})
                    cal_context = kwargs.get('context', {})
                    if cal_context and isinstance(cal_context, (dict,)):
                        context = context.update(cal_context)

                    if data.get("uid", False):
                        model = model.sudo(data.get('uid', False))
                    else:
                        model = model.sudo()

                    if res_ids:
                        model = model.browse(res_ids)

                    call = getattr(model.with_context(context), data['name'])
                    return call(*args, **kwargs)

                self.deal_custom_event(sid, data)

    @api.model
    def trigger_event_to_client(self, message):
        uid = message.get('uid', None)
        event_type = message['event_type']
        data = message['data']
        room = message.get("room", None)
        callback_info = message.get('callback_info', None)
        if uid:
            sids = self.uid_to_sids(uid)
        else:
            sids = None
        if sids:
            for sid in sids:
                msg = {
                    "msg_type": event_type,
                    "data": data,
                    "sid": sid,
                    "uid": uid,
                    "room": room,
                    "callback_info": callback_info
                }

                if not callback_info:
                    del msg["callback_info"]

                message_queue.put(msg)
        else:
            message_queue.put({
                "msg_type": event_type,
                "room": room,
                "data": data,
                "callback_info": callback_info
            })

