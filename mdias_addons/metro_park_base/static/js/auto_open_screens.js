odoo.define('metro_park.auto_screen', function (require) {
    "use strict";

    var WebClient = require('web.WebClient');

    var AutoScreen = WebClient.include({

        /**
         * 根据是否为pop来确定是否打开新窗口
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                if (window.cefQuery) {
                    window.cefQuery({
                        request: JSON.stringify({
                            cmd: "is_popup"
                        }),
                        persistent: false,
                        onSuccess: function (response) {
                            if (response == "false") {
                                self.show_screens();
                            }
                        },
                        onFailure: function (error_code, error_message) {}
                    })
                }
            })
        },

        /**
         * 自动打开大屏
         */
        show_screens: function () {
            var self = this;
            if (window.cefQuery) {
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "get_auto_screen_info"
                    }),
                    persistent: false,
                    onSuccess: function (info) {
                        info = JSON.parse(info);

                        // BI看板
                        if (info.bi) {
                            self.do_action({
                                "type": "ir.actions.act_url",
                                "url": '/web?#action=report_client',
                                "target": "new"
                            });
                        }

                        // 现车监控
                        if (info.cur_train) {
                            self._rpc({
                                "model": "metro_park_dispatch.cur_train_manage",
                                "method": "get_user_location",
                                "args": []
                            }).then(function (location) {
                                if (location) {
                                    var host_url = "\\metro_park_dispatch\\static\\graph_viewer\\cur_train_manage.html?show_type=bigscreen&location=" + location;
                                    self.do_action({
                                        "type": "ir.actions.act_url",
                                        "url": host_url,
                                        "target": "new"
                                    });
                                }
                            })
                        }
                    },
                    onFailure: function (error_code, error_message) {}
                })
            }
        }
    });

    return AutoScreen;
});