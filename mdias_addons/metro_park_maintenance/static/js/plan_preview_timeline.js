odoo.define('funenc.plan_preview_timeline', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var Dialog = require('web.Dialog');

    /**
     * 看计划时间轴
     */
    var plan_preview_timeline = AbstractAction.extend(ControlPanelMixin, {
        year: undefined,
        start_date: undefined,
        end_date: undefined,
        items: [],
        groups: [],
        time_line: [],
        template: 'metro_park_meaintaince.plan_preview_timeline',

        jsLibs: [
            '/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.js',
            '/metro_park_maintenance/static/moment_with_locale.js'
        ],
        cssLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.css'],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.day_plan_id = action.context.active_id || action.params.active_id || action.day_plan_id
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        set_debounce: function () {
            var self = this;
            var change_timeline = function (item) {
                var start_date = moment(item.start);
                var end_date = moment(item.end);

                var days = end_date.diff(start_date, 'days');
                var rule_info_id = item.id.split('_')[item.id.split('_').length - 1];
            };
            return _.debounce(function (item) {
                change_timeline(item)
            }, 1000);
        },

        on_attach_callback: function () {
            // Configuration for the Timeline
            var options = {
                start: this.start_date,
                end: this.end_date,
                height: '100%',
                locale: 'zh-cn',
                zoomable: false,
                editable: {
                    remove: true, // 允许删除
                    updateTime: true // 运行拖拽
                },
                onMoving: function (item, callback) {

                },
                onRemove: function (item, callback) {

                }
            };

            // Create a Timeline
            this.time_line = new vis.Timeline(this.$(".time_line")[0]);
            this.time_line.setOptions(options);
            this.time_line.setItems(this.items);
            this.time_line.setGroups(this.groups);

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

        willStart: function () {
            var self = this
            var today = moment().format('YYYY-MM-DD')
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    "model": "metro_park_dispatch.day_run_plan",
                    "method": "get_plan_preview_plans",
                    "args": [today]
                }).then(function (rst) {
                    self.items = rst.items;
                    self.groups = rst.groups;
                    self.start_date = rst.start_date;
                    self.end_date = rst.end_date;
                })
            });
        }
    });

    core.action_registry.add('plan_preview_timeline', plan_preview_timeline);

    return plan_preview_timeline;
});