odoo.define('handover_tree_button', function (require) {
    "use strict";

    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');
    var core = require('web.core');

    var handover_tree_button = Widget.extend({
        template: 'handover_tree_button',
        events: {
            'click': '_click_tree_buttons'
        },
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.id = record.res_id;
            this.record = record;
        },
        start: function () {
            var $el = $(core.qweb.render(this.template, {
                widget: this
            }).trim());
            this._replaceElement($el);
            this.vue = new Vue({
                el: '#app',
                data() {
                    return {}
                }
            });
        },
        _click_tree_buttons: function (event) {
            var self = this;
            event.stopPropagation();
            var button_class = $(event.target).attr('class');
            switch (button_class) {
                // 点击详情按鈕
                case 'handover_tree':

                    var self = this
                    self._rpc({
                        model: 'metro_park_production.handover_management',
                        method: 'to_handover_form',
                        args: [self.id]
                    }).then(function (action) {
                        self.do_action(action)
                    })
                    break
            }
        }
    });

    widgetRegistry.add("handover_tree_button", handover_tree_button);

    return {
        res_groups_tree_button: handover_tree_button
    }

});