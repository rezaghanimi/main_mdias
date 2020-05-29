odoo.define('metro_park_dispatch.client_notify', function (require) {
    "use strict";
    
    var WebClient = require('web.WebClient');
    
    /**
     * 扩展client,
     */
    WebClient.include({

        start: function () {
            this._super.apply(this, arguments)
            this.register_socketio_msg()
        },

        /**
         * 处理socketio msg, 需要看到地点
         * @param {*} msg
         */
        deal_socket_io_msg: function (msg) {
            var self = this
            var msg_type = msg.data.msg_type
            var location_alias = msg.data.location_alias
            if (location_alias != this.location_alias) {
                return;
            }
            switch (msg_type) { 
                // 通知场调选择
                case 'notice_no_plan':
                    self._on_receive_no_plan(msg)
                    break;
            }
        },

        _on_receive_no_plan: function(msg) {
            var self = this
            var msg_data = msg.data.msg_data
            var location_alias = msg.data.location

            this._rpc({
                "model": "metro_park_dispatch.chose_pos_wizard",
                "method": "get_position_wizard",
                "kwargs": {
                    train_id: msg_data.train_id,
                    rail_no: msg_data.rail_no,
                    location_alias: location_alias
                }
            }).then(function (rst) {
                if (rst) {
                    self.do_action(rst)
                }
            })
        }
    })
});
