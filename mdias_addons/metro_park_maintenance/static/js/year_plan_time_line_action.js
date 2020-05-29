odoo.define('funenc.year_plan_time_line', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var Dialog = require('web.Dialog');

    /**
     * 看计划时间轴
     */
    var year_plan_time_line = AbstractAction.extend(ControlPanelMixin, {
        year: undefined,
        start_date: undefined,
        end_date: undefined,
        items: [],
        groups: [],
        time_line: [],
        template: 'funenc.year_plan_time_line_template',

        jsLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.js'],
        cssLibs: ['/metro_park_maintenance/static/lib/vis/vis-timeline-graph2d.min.css'],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.year_plan_id = action.context.active_id || action.params.active_id || action.year_plan_id
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        /**
         * 需要禁止编辑
         */
        set_debounce: function () {
            var self = this;
            var change_timeline = function (item) {
                var start_date = moment(item.start);
                var end_date = moment(item.end);
                var days = end_date.diff(start_date, 'days');
                var rule_info_id = item.id.split('_')[item.id.split('_').length - 1];
                self._rpc({
                    model: 'metro_park_maintenance.rule_info',
                    method: 'write',
                    args: [[parseInt(rule_info_id)], {'date': start_date.format('YYYY-MM-DD'), 'repair_days': days}]
                })
            };
            return _.debounce(function (item) {
                change_timeline(item)
            }, 1000);
        },

        on_attach_callback: function () {
            // Configuration for the Timeline
            var debounce = this.set_debounce();
            var options = {
                start: this.start_date,
                end: this.end_date,
                height: '100%',
                // 设置最小单位为天
                zoomMin: 1000 * 60 * 60 * 24 * 6,
                zoomMax: 1000 * 60 * 60 * 24 * 6,
                editable: {
                    remove: true, // 允许删除
                    updateTime: true, // 运行拖拽
                    add: true,
                },

                onMoving: function (item, callback) {
                    var start_date = moment(item.start);
                    var end_date = moment(item.end);
                    item.end = moment(item.start).add(1, 'd')
                    if (start_date.get('hour') !== 0 || end_date.get('hour') !== 0 || end_date.diff(start_date, 'days') <= 0) {
                        callback(null)
                    } else {
                        callback(item);
                        debounce(item);
                    }
                },
                
                onRemove: function (item, callback) {
                    Dialog.confirm(self, '确定删除此检修计划？', {
                        title: '提示',
                        confirm_callback: function () {
                            callback(item);
                            var rule_info_id = item.id.split('_')[item.id.split('_').length - 1];
                            self._rpc({
                                model: 'metro_park_maintenance.rule_info',
                                method: 'unlink',
                                args: [parseInt(rule_info_id)]
                            })
                        },
                        cancel_callback: function () {
                            callback(null)
                        }
                    });
                }
            };

            // Create a Timeline
            this.time_line = new vis.Timeline(this.$(".time_line")[0]);
            this.time_line.setOptions(options);
            this.time_line.setGroups(this.groups);
            this.time_line.setItems(this.items);

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
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    "model": "metro_park_maintenance.plan_data",
                    "method": "get_year_plan_data",
                    "args": [self.year_plan_id]
                }).then(function (rst) {
                    self.items = rst.items
                    self.start_date = rst.start_date
                    self.end_date = rst.end_date
                    self.groups = rst.groups
                })
            });
        }
    });

    core.action_registry.add('year_plan_time_line', year_plan_time_line);

    return year_plan_time_line;
});