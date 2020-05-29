odoo.define('metro_park_maintenance.week_plan_table', function (require) {
    "use strict";
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var week_plan_table_render = ListRenderer.extend({})

    var week_plan_table_controller = ListController.extend({
        buttons_template: 'week_create_btns_template',

        events: _.extend({}, ListController.prototype.events, {
            "click .week_create": "_on_week_create",
        }),

        /**
         * 添加
         */
        _on_week_create: function () {
            var self = this
            debugger
            self._rpc({
                model: 'metro_park_maintenance.rule_info',
                method: 'week_create_data',
                context: {
                    'active_id': this.initialState.context.active_id,
                    'active_model': 'metro_park_maintenance.week_plan',
                },
            }).then(function (data) {
                self.do_action(data, {
                    on_close: function () {
                        self.reload()
                    }
                });
            });
        },
    })

    var week_plan_table = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: week_plan_table_render,
            Controller: week_plan_table_controller
        })
    });

    view_registry.add('week_plan_table', week_plan_table);

    return week_plan_table;
});
