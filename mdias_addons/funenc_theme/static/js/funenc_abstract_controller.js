odoo.define('funenc.abstract_controller', function (require) {
    "use strict";

    var AbstractController = require('web.AbstractController');
    var AbstractAction = require('web.AbstractAction');
    var config = require('web.config');
    var core = require('web.core')
    var qweb = core.qweb

    AbstractController.include({

        /**
         * 扩展增按扭的点击事件，这样省得单独去处理action事件
         */
        events: _.extend({}, AbortController.prototype.events, {
            'click button[type="action"]': '_onActionClicked',
        }),

        /**
         * 扩展通过context来判定某个动作是否被支持
         * @param {*} action 
         */
        is_action_enabled: function (action) {
            var context = this.model.get(this.handle).getContext()
            return this.activeActions[action] | context[action];
        }
    })
})