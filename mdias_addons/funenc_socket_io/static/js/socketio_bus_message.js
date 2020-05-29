odoo.define('socketio_bus.bus_message', function (require) {
    "use strict";

    let Widget = require('web.Widget');
    let WebClient = require('web.WebClient');
    let ServicesMixin = require('web.ServicesMixin');
    // 这个需要引用，保证加载顺序
    let funenc_socket_socket_io = require('funenc.socket_io');

    let SocketIOBusMessage = Widget.extend(ServicesMixin, {
        dependencies: ['local_storage'],

        start: function () {
            let self = this;

            let def = this._super.apply(this, arguments)
            this.on_bus('bus_message', function (data, call) {
                self._notify(data.data);
                call(true)
            });
            return def
        },

        _notify: function (message) {
            this.sendNotification(message, function () {
            })
        },

        sendNotification: function (message, callback) {
            let title = message.message_title;
            let content = message.message_body;
            if (window.Notification && Notification.permission === "granted") {
                this._sendNativeNotification(title, content, callback);
            } else {
                let self = this;
                let params = {
                    title: title,
                    message: content,
                };
                let action = message.action;
                if (!!action) {
                    let click_call = () => {
                        self.do_action(action, {
                            on_close: function () {
                                self.do_action({
                                    type: 'ir.actions.act_window_close'
                                })
                            }
                        })
                    };

                    let button = {
                        click: click_call,
                        primary: true,
                        text: action.name,
                        class_names: action.class_names
                    };
                    params['buttons'] = [button]

                }
                this.do_notify(params);
            }
        },

        do_notify: function (params) {
            return this.call('notification', 'notify', params)
        },

        _beep: function () {
            if (typeof (Audio) !== "undefined") {
                if (!this._audio) {
                    this._audio = new Audio();
                    let ext = this._audio.canPlayType("audio/ogg; codecs=vorbis") ? ".ogg" : ".mp3";
                    let session = this.getSession();
                    this._audio.src = session.url("/websocket_bus/static/audio/ting" + ext);
                }
                this._audio.play();
            }
        },

        _sendNativeNotification: function (title, content, callback) {
            var notification = new Notification(title, {body: content});
            notification.onclick = function () {
                window.focus();
                if (this.cancel) {
                    this.cancel();
                } else if (this.close) {
                    this.close();
                }
                if (callback) {
                    callback();
                }
            };
        },
    });

    let LoadActionBus = Widget.extend(ServicesMixin, {
        start: function () {
            let self = this;
            let def = this._super.apply(this, arguments)
            this.on_bus('on_action', function (data) {
                self.do_action(data.data)
            });
            return def
        },

    });

    WebClient.include({
        start: function () {
            let def = this._super.apply(this, arguments)
            this.socketio_message = new SocketIOBusMessage(this);
            this.load_action_bus = new LoadActionBus(this);
            this.socketio_message.start();
            this.load_action_bus.start();
            return def
        }
    });

    return SocketIOBusMessage
});