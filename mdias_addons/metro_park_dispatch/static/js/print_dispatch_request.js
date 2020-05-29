odoo.define('print_dispatch_request', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var print_dispatch_request = AbstractAction.extend({
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.vue_data = action.context.vue_data
        },

        start: function () {
            var self = this;
            return self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_dispatch', template_name: 'print_dispatch_request_template'}
            }).then(function (el) {
                self._replaceElement($(el))
            })
        },

        on_attach_callback: function () {
            var self = this;
            var app = new Vue({
                el: '#print_dispatch_request_template',
                data: function () {
                    return self.vue_data
                }
            })
        }
    });
    core.action_registry.add('print_dispatch_request', print_dispatch_request);
    return print_dispatch_request
});