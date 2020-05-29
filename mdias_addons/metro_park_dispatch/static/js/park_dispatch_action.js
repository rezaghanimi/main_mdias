/**
 * 场调视图
 */
odoo.define('metro_park_dispatch.park_dispatch_action', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var iFrame = require("web.IFrameWidget")
    var session = require("web.session")

    // 司机排班客户端
    var park_dispatch_action = AbstractAction.extend({
        frame_window: undefined,
        host_url: "",
        iframe: undefined,

        init: function (parent, action) {
            this._super.apply(this, arguments)
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments).then(function () {
                // 此页面占满所有空间
                self.$el.css("width", "100%");
                self.$el.css("height", "100%");
                self.$el.css("overflow", "hidden");
                // 添加iframe
                self.frame_window = new iFrame(this, self.host_url);
                self.frame_window.appendTo(self.el);
                // 取得iframe对象
                self.iframe = self.frame_window.$el[0];
                // 绑定事件
                self.iframe.onload = function () {
                    self._on_iframe_loaded();
                };
            })
        },

        /**
         * 获取服务器地址
         */
        willStart: function () {
            this.host_url = "\\metro_park_dispatch\\static\\park_map\\parkmap\\manageindex.html"
            return this._super.apply(this, arguments);
        },

        on_attach_callback: function () {
            // Register now the postMessage event handler. We only want to listen to ~trusted
            // messages and we can only filter them by their origin, so we chose to ignore the
            // messages that do not come from `web.base.url`.
            console.log("bind the window message");
            $(window).on('message', this, this.on_message_received);
        },

        on_detach_callback: function () {
            $(window).off('message', this.on_message_received);
        },

        _on_iframe_loaded: function () {
            this._load_train_socketio_events()
        },
        _load_train_socketio_events: function () {
            this.on_bus('on_train_position', function (data) {
                var iframe = window.frames[0];
                if (iframe) {
                    iframe.ngname.set_currenttrain_state(data.data)
                }
            });
        },

        on_message_received: function (ev) {

            // Check the syntax of the received message.
            var message = ev.originalEvent.data;
            if (_.isObject(message)) {
                message = message.action;
            }

            if (!_.isString(message) || (_.isString(message))) {
                return;
            }

            switch (message) {
                case 'metro_park_dispatch:move':
                    break;
                default:
            }
        }
    });

    core.action_registry.add('park_dispatch_action', park_dispatch_action);
    return park_dispatch_action;
});