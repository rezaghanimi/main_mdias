/**
 * 供电分区
 */
odoo.define('metro_park_base.electric_area', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var iFrame = require("web.IFrameWidget")

    // 司机排班客户端
    var electric_area = AbstractAction.extend({
        frame_window: undefined,
        host_url: "",
        iframe: undefined,

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.location_id = action.context.active_id || action.params.active_id
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments).then(function () {
                // 让页面占满所有空间
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
            var self = this
            this._rpc({
                "model": "metro_park_base.location",
                "method": "get_location_alias",
                "args": [this.location_id]
            }).then(function (rst) {
                self.host_url = "\\metro_park_dispatch\\static\\park_map\\parkmap\\electric.html?mapname=";
                if (location.location_alias === "gaodalu") {
                    self.host_url += "gaodalu";
                } else {
                    self.host_url += "banqiao";
                }
            })
        },

        on_attach_callback: function () {
            // Register now the postMessage event handler. We only want to listen to ~trusted
            // messages and we can only filter them by their origin, so we chose to ignore the
            // messages that do not come from `web.base.url`.
            $(window).on('message', this, this.on_message_received);
        },

        on_detach_callback: function () {
            $(window).off('message', this.on_message_received);
        },

        _on_iframe_loaded: function () {

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

    core.action_registry.add('electric_area', electric_area);
    return electric_area;
});