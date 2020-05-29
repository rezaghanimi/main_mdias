/**
 * 富能通socket io, funenc_socketio_server_msg 服务端消息，服务端消息
 */
odoo.define('funenc.socket_io', function (require) {
    "use strict";
    var rpc = require('web.rpc');
    var Class = require('web.Class');
    var mixins = require('web.mixins');
    var ServicesMixin = require('web.ServicesMixin');
    var core = require('web.core');
    var Widget = require('web.Widget');

    /**
     * 说明，必需要放在client实例化这前进行初始化
     * @class SocketIO
     */
    var FunencSocketIO = Class.extend(mixins.EventDispatcherMixin, ServicesMixin, {

        socketio: undefined,

        init: function (parent) {
            this.wait_ons = [];
            mixins.EventDispatcherMixin.init.call(this);
            this.setParent(parent);
            core.bus.on("web_client_ready", this, this.instance_socketio);
        },

        instance_socketio: function () {
            var self = this;
            return this.get_config().then(function (config) {
                var host = config.websocket_host + ':' + config.websocket_port + '/'
                console.log(host);
                var socketio = io(host, {rememberUpgrade: true, transports: ['websocket', 'long-polling'], 'upgrade': true});
                self.socketio = socketio;
                self._register_event()

                socketio.on('connect', function () {
                    console.log('funenc_socket_io_connected', socketio.connected);
                    core.bus.trigger('funenc_socket_io_connected');
                });

                socketio.on('disconnect', function () {
                    console.log('funenc_socket_io_disconect');
                    core.bus.trigger('funenc_socket_io_disconect');
                });

                socketio.on('connect_error', function (error) {
                    core.bus.trigger('funenc_socket_io_error', error);
                });

                socketio.on('funenc_socketio_server_msg', function (msg) {
                    console.log("get msg");
                    core.bus.trigger('funenc_socketio_server_msg', msg);
                });
            })
        },

        _register_event() {
            if (this.socketio) {
                while (this.wait_ons.length > 0) {
                    var event = this.wait_ons.pop();
                    this.socketio.on(event[0], event[1]);
                }
                return true
            }
        },

        on_bus: function (event_name, call_back, once = false) {
            //事件注册写入队列，保证事件注册成功
            this.wait_ons.push([event_name, call_back, once])
            this._register_event();
            return true
        },

        remove_on_bus: function (event_name, lister) {
            try {
                if (this.socketio) {
                    var event_names = this.socketio.eventNames;
                    if (!!event_names) {
                        return false
                    }
                    if (event_names.find(event_name) < 0) {
                        return false
                    }
                    this.socketio.removeListener(event_name, lister)
                    return true
                }
                return false
            }catch (e) {
                console.log('Cannot read property \'find\' of undefined')
            }
        },

        /**
         * 取得服务器配置
         */
        get_config: function () {
             return rpc.query({
                "model": "funenc.socket_io",
                "method": "get_config",
                "args": []
            })
        }
    });

    var socket_io = new FunencSocketIO(this);

    /**
     * 扩展组件
     */
    Widget.include({
        init: function () {
            var self = this;
            self.registed_socketio_msg = false
            this._bus_event_poll = {};
            this._super.apply(this, arguments)
        },

        /**
         * 注册mdias消息
         */
        register_socketio_msg: function () {
            if (!this.registed_socketio_msg) {
                // 先解绑
                core.bus.off("funenc_socketio_server_msg", this, this._on_socket_io_server_msg)
                // 再注册
                core.bus.on('funenc_socketio_server_msg', this, this._on_socket_io_server_msg);

                this.registed_socketio_msg = true
            }
        },

        /**
         * 消息处理函数，组件重写这个函数进行消息处理
         * @param {*} msg
         */
        _on_socket_io_server_msg: function (event) {
            this.deal_socket_io_msg(event)
        },

        /**
         * 重写这个函数
         * @param {*} msg
         */
        deal_socket_io_msg: function (msg) {
            console.log('get socket io msg', msg);
        },

        on_bus: function (event_name, callback, once) {
            if (event_name === undefined || callback === undefined) {
                throw new Error("socketio event name undefined");
            }
            socket_io.on_bus(event_name, callback, once);
            //保存已经注册的事件，当组件销毁的时候取消监听
            this._bus_event_poll[event_name] = callback

        },

        remove_on_bus: function (event_name, lister) {
            socket_io.remove_on_bus(event_name, lister);
        },

        /**
         * 解绑消息
         */
        destroy: function () {
            var self = this;
            core.bus.off("funenc_socketio_server_msg", this, this._on_socket_io_server_msg);
            //取消事件监听
            _.each(this._bus_event_poll, (call, event_name) => {
                self.remove_on_bus(event_name, call);
            });
            return this._super.apply(this, arguments)
        },
    });

    return FunencSocketIO
});
