/**
 * 现车监控, 只作投屏使用
 */
window.set_global_state = function () {}

odoo.define('metro_park_dispatch.cur_train_map_monitor', function (require) {
    "use strict";

    var park_dispatch_action = require('metro_park_dispatch.park_dispatch_action');
    var core = require('web.core');

    // 现车管理界面
    var cur_train_map_monitor = park_dispatch_action.extend({
        template: 'cur_train_map_action',
        location: undefined,

        init: function () {
            this._super.apply(this, arguments)
        },

        /**
         * 设置标题
         */
        start: function () {
            document.title = '站场监控与现车'
            return this._super.apply(this, arguments)
        },

        /**
         * 获取服务器地址
         */
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    "model": "metro_park_dispatch.cur_train_manage",
                    "method": "get_user_location",
                    "args": []
                })
            }).then(function (location) {
                if (location) {
                    self.location_alias = location
                    self.host_url = "\\metro_park_dispatch\\static\\graph_viewer\\cur_train_manage.html?location=" + location;
                    if (location == 'yuanhua') {
                        self.host_url = "\\metro_park_dispatch\\static\\park_map\\parkmap\\cur_train_monitor.html?mapname=" + location;
                    }
                }
            })
        },

        notify_window_load_finished: function () {
            if (window.cefQuery) {
                // 通知壳子页面加载完毕, 避免所有的窗口都发送相同的数据
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "load_finish",
                        data: {
                            'title': '站场监控与现车'
                        }
                    }),
                    persistent: false,
                    onSuccess: function (response) {},
                    onFailure: function (error_code, error_message) {}
                })
            }
        },

        on_message_received: function (ev) {
            var data = ev.originalEvent.data;

            switch (data.action) {
                case 'metro_park_dispatch:report_point':
                    break;

                case 'metro_park_dispatch:load_finished':
                    // 请求联锁发送数据
                    window.set_global_state = _.bind(this.set_global_state, this)

                    // 通知壳子页面加载完毕, 壳子端做了个缓存机制，
                    // 必需要发送load_finish之后再进行通知
                    this.notify_window_load_finished();

                    // 页面加载完成的时候，通过后端请求一次全局变化
                    this.request_map_state();

                    // 请求当前车的信息
                    // this.get_cur_train_map_info();

                    break;
            }
        },

        on_attach_callback: function () {
            this.register_socketio_msg()
            document.title = '站场监控与现车';
            this._super.apply(this)
        },

        on_detach_callback: function () {
            this._super.apply(this, arguments)
            if (window.cefQuery) {
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "window_closed",
                        data: {
                            'title': '站场监控与现车'
                        }
                    }),
                    persistent: false,
                    onSuccess: function (response) {},
                    onFailure: function (error_code, error_message) {}
                })
            }
        },

        /**
         * 通过后端请求一次全局变化
         */
        request_map_state: function () {
            this._rpc({
                "model": "metro_park_dispatch.msg_client",
                "method": "request_map_state",
                "args": [this.location]
            }).fail(function () {
                console.log("请求全局数据出错")
            })
        },

        /**
         * 调车
         */
        dispatch_train_wizard: function (currenttrain, target_rail) {
            var self = this
            this._rpc({
                "model": "metro_park_dispatch.cur_train_manage",
                "method": "dispatch_wizard",
                "args": [currenttrain, target_rail]
            }).then(function (rst) {
                if (rst) {
                    self.do_action(rst)
                }
            })
        },

        set_currenttrain_state: function (state) {
            this.iframe.contentWindow.ngname.set_currenttrain_state(state)
        },

        /**
         * 更改车辆位置
         */
        update_cur_train_pos: function (cur_train, new_rail) {
            var self = this
            this._rpc({
                "model": "metro_park_dispatch.cur_train_manage",
                "method": "update_train_position",
                "args": [parseInt(cur_train), new_rail]
            }).then(function (rst) {
                if (rst) {
                    self.iframe.contentWindow.ngname.set_currenttrain_state(rst)
                }
            })
        },

        /**
         * 处理上下文菜单
         * @param {*} data
         */
        deal_context_menu: function (data) {
            switch (data.menu) {
                case "reportpoint":
                    this.report_point(JSON.parse(data.train))
                    break;
                    // 查看调车计划
                case "viewShuntPlan":
                    this.view_dispatch_plans();
                    break;
            }
        },

        /**
         * 查看调车计划
         */
        view_dispatch_plans: function () {
            var self = this
            this._rpc({
                "model": "metro_park_dispatch.cur_train_manage",
                "method": "view_dispatch_plans",
                "args": []
            }).then(function (action) {
                self.do_action(action)
            })
        },

        /**
         * 列车报点
         */
        report_point: function (train) {
            // 传递就是train_name
            var train_name = train.name;
            var rail_sec = train.position;
            rail_sec = rail_sec.replace("_", "/")
            var self = this;
            this._rpc({
                "model": "metro_park_dispatch.report_train_point",
                "method": "request_point_by_sec_no",
                "args": [train_name, rail_sec]
            }).then(function (action) {
                self.do_action(action, {
                    on_close: function (res) {
                        if (!res || res == 'special') {
                            return
                        }
                    }
                });
            })
        },

        /**
         * 中转设置全局状态
         * @param {*} state
         */
        set_global_state: function (state) {
            // 联锁消息转发
            this.iframe.contentWindow.ngname.set_global_state(state)
        },

        /**
         * 加载现车数据
         */
        // get_cur_train_map_info: function () {
        //     var self = this;
        //     this._rpc({
        //         "model": "metro_park_dispatch.cur_train_manage",
        //         "method": "get_cur_train_map_info",
        //         "args": []
        //     }).then(function (rst) {
        //         // 设置现车状态
        //         self.iframe.contentWindow.ngname.set_currenttrain_state(rst)
        //     })
        // },

        /**
         * 处理socketio msg, 需要看到地点
         * @param {*} msg
         */
        // deal_socket_io_msg: function (msg) {
        //     var self = this
        //     var msg_type = msg.data.msg_type
        //     var location_alias = msg.data.location_alias
        //     if (location_alias != this.location_alias) {
        //         return;
        //     }
        //     switch (msg_type) {
        //         case 'update_train_position':
        //             var state = msg.data.msg_data
        //             self.iframe.contentWindow.ngname.set_currenttrain_state(state)
        //             break;
        //     }
        // },
    });

    core.action_registry.add('cur_train_map_monitor', cur_train_map_monitor);
    return cur_train_map_monitor;
});