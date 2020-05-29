odoo.define('funenc.mdias.test_client', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var socket_io = require('funenc.socket_io');
    /**
     * 测试客户端
     */
    var MDiasTestClient = AbstractAction.extend({
        start: function () {
            this._super.apply(this, arguments)
            this.register_socketio_msg()
        },

        /**
         * 重写消息处理
         * @param {*} msg 
         */
        deal_socket_io_msg: function (msg) {
            console.log('get socket io msg by client', msg);
        },
    });

    core.action_registry.add('MDiasTestClient', MDiasTestClient);

    return MDiasTestClient;
});