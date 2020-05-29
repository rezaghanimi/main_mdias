/**
 * 年计划详情
 */
odoo.define('funenc.driver_plan_client', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var iFrame = require('funenc.AppIFrameWidget')
    var session = require('web.session');

    // 司机排班客户端
    var driver_plan_client = AbstractAction.extend({
        frame_window: undefined,
        host_url: "172.21.0.5:8082/index.html?id=" + session.uid,
        // host_url: "http://cs2.huiztech.cn/shift-schedule/app/index.html?id=" + session.uid,

        init: function (parent, action) {

            this._super.apply(this, arguments)
        },

        start: function () {
            var self = this;
            this._super.apply(this, arguments).then(function () {
                self.$el.css("width", "100%");
                self.$el.css("height", "100%");
                self.$el.css("overflow", "hidden");
                try {
                    self.frame_window = new iFrame(this, self.host_url);
                self.frame_window.appendTo(self.$el);
                }catch (e) {
                    console.log(e);
                }
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
                self.host_url = rst["driver_plan_host"] || self.host_url
            })
        }
    });

    core.action_registry.add('driver_plan_client', driver_plan_client);
    return driver_plan_client;
});


