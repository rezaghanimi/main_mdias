/**
 * hz 检修计划
 */
odoo.define('funenc.hz_maintaince_client', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var iFrame = require("web.IFrameWidget")

    // 司机排班客户端
    var hz_maintaince_client = AbstractAction.extend({
        frame_window: undefined,
        host_url: "http://127.0.0.1:8069/metro_park_maintance_hz/static/inde.html",
        init: function (parent, action) {
            this._super.apply(this, arguments)
        },

        start: function() {
            var self = this;
            this._super.apply(this, arguments).then(function(){
                self.$el.css("width", "100%");
                self.$el.css("height", "100%");
                self.$el.css("overflow", "hidden");
                self.frame_window = new iFrame(this, self.host_url);
                self.frame_window.appendTo(self.$el);
            })
        },

        /**
         * 获取服务器地址
         */
        willStart: function () {
            var self = this
            return this._rpc({
                "model": "metro_park_base.system_config",
                "method": "get_configs",
                "args": []
            }).then(function (rst) {
                self.host_url = rst["maintaince_host"] || self.host_url
            })
        }
    });

    core.action_registry.add('hz_maintaince_client', hz_maintaince_client);
    return hz_maintaince_client;
});