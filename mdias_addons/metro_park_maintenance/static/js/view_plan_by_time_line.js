odoo.define('funenc.view_plan_by_time_line', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var view_plan_by_time_line = AbstractAction.extend({
        year: undefined,
        items: [],
        groups: [],
        time_line: [],
        template: 'funenc.view_plan_by_time_line',

        jsLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.js'],
        cssLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.css'],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.year = action.context.year || action.params.year
        },

        /**
         * 
         */
        on_attach_callback: function () {
            // Configuration for the Timeline
            var options = {
                start: this.start_date,
                end: this.end_date,
                height: "600px"
            };

            // Create a Timeline
            this.time_line = new vis.Timeline(this.$(".time_line")[0]);

            // 不加timeout会有问题
            this.time_line.setOptions(options);
            this.time_line.setGroups(self.groups);
            this.time_line.setItems(self.items);
        },

        start: function () {
            this._super.apply(this, arguments)
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
            return this._super.apply(this, arguments).then(function () {

                // return self._rpc({
                //     "model": "metro_park_maintenance.plan_data",
                //     "method": "get_plan_data",
                //     "args": [self.year_plan_id]
                // }).then(function (rst) {
                //     self.items = rst.items
                //     self.start_date = rst.start
                //     self.end_date = rst.end
                //     self.groups = rst.groups
                // })
                
            });
        }
    });

    core.action_registry.add('view_plan_by_time_line', view_plan_by_time_line);

    return view_plan_by_time_line;
});