odoo.define('maintenance_print', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var maintenance_print = AbstractAction.extend({
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.vue_data = action.context.vue_data
            this.main_template = action.context.main_template
        },

        start: function () {
            var self = this;
            return self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'maintenance_management', template_name: self.main_template}
            }).then(function (el) {
                self._replaceElement($(el))
            })
        },

        on_attach_callback: function () {
            var self = this;
            console.log(self.template)
            new Vue({
                el: '#' + self.main_template,
                data: function () {
                    return self.vue_data
                }
            })
        }
    });
    core.action_registry.add('maintenance_print', maintenance_print);
    return maintenance_print
});