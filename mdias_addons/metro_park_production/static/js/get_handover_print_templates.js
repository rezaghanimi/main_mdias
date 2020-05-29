odoo.define('get_handover_print_templates', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var get_handover_print_templates = AbstractAction.extend({
        init: function (parent, action) {
            this._super.apply(this, arguments);
            console.log(action.context.vue_data)
            this.vue_data = action.context.vue_data
            this.templates = action.context.vue_data.template_name
        },

        willStart: function () {
            var self = this;
            // 在这里取得数据并变更this.vue_data对应的数据, rpc的model或者method需变更

            self.get_data = function () {
                return
            }
            return $.when(self.get_data()).then(function (result1) {
            })
        },

        start: function () {
            var self = this;
            // self._rpc({
            //
            // })
            return self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_production', template_name: self.templates}
            }).then(function (el) {
                self._replaceElement($(el))
            })
        },

        on_attach_callback: function () {
            var self = this;
            var app = new Vue({
                el: '#' + self.templates,
                data: function () {
                    return self.vue_data
                }
            })
        }
    });
    core.action_registry.add('get_handover_print_templates', get_handover_print_templates);
    return get_handover_print_templates
});