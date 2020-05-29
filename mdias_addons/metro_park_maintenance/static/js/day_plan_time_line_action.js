odoo.define('funenc.day_plan_time_line', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    /**
     * 日计划时间轴
     */
    var day_plan_time_line = AbstractAction.extend(ControlPanelMixin, {
        top_list: undefined,
        bottom_list: undefined,
        year: undefined,
        start_date: undefined,
        end_date: undefined,
        items: [],
        groups: [],
        time_line: [],
        template: 'funenc.day_plan_time_line_template',

        jsLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.js'],
        cssLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.css'],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.year_plan_id = action.context.active_id || action.params.active_id
        },

        start: function () {
            this._super.apply(this, arguments)

            // Configuration for the Timeline
            var options = {
                start: this.start_date,
                end: this.end_date,
                height: "100%"
            };

            // Create a Timeline
            var self = this
            this.time_line = new vis.Timeline(this.$(".time_line")[0]);

            self.time_line.setGroups(self.groups);
            self.time_line.setItems(self.items);

            var self = this;
            $(window).resize(function () {
                var height = self.$el.height()
                // Configuration for the Timeline
                var tmp_option = {
                    height: height
                };
                self.time_line.setOptions(tmp_option);
            })
        },

        _scaleCurrentWindow: function (factor) {
            if (this.time_line) {
                this.current_window = this.time_line.getWindow();
                this.current_window.end = moment(this.current_window.start).add(factor, 'hours');
                this.time_line.setWindow(this.current_window);
            }
        },

        willStart: function () {
            var self = this
            // return this._super.apply(this, arguments).then(function () {
            //     return self._rpc({
            //         "model": "metro_park_maintenance.plan_data",
            //         "method": "get_plan_data",
            //         "args": [self.year_plan_id]
            //     }).then(function (rst) {
            //         self.items = rst.items
            //         self.start_date = rst.start
            //         self.end_date = rst.end
            //         self.groups = rst.groups
            //     })
            // });
            return this._super.apply(this, arguments)
        }
    });

    core.action_registry.add('day_plan_time_line', day_plan_time_line);

    return day_plan_time_line;
});