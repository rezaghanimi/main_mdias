/**
 * 周计划统计
 */
odoo.define('metro_park_maintenance.week_plan_static', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var Dialog = require('web.Dialog');

    /**
     * 周计划统计
     */
    var week_plan_static = AbstractAction.extend(ControlPanelMixin, {
        week_plan_id: undefined,
        template: 'metro_park_maintenance.week_plan_static',

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.data = undefined
            this.xs = undefined
            this.week_plan_id = action.context.active_id || action.params.active_id || action.week_plan_id
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        on_attach_callback: function () {
            var self = this;
            setTimeout(() => {
                self.xs = x.spreadsheet(
                    self.$('.week-spreadsheet')[0], {
                    showToolbar: true,
                    showGrid: true,
                    view: {
                        height: function () {
                            return self.$el.height()
                        },
                        width: function () {
                            return self.$el.width()
                        }
                    },
                }).loadData(self.data)
            }, 0);
        },

        willStart: function () {
            var self = this
            return this._rpc({
                "model": "metro_park_maintenance.week_plan",
                "method": "get_week_plan_static_data",
                "args": [this.week_plan_id]
            }).then(function (data) {
                self.data = data
            })
        }
    });

    core.action_registry.add('week_plan_static', week_plan_static);

    return week_plan_static;
});