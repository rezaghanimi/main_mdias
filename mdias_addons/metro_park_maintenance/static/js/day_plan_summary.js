/**
 * 日计划详情
 */
odoo.define('funenc.day_plan_summary', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var day_plan_summary = AbstractAction.extend({
        rules: [],
        plan_datas: [],
        devs: [],
        template: 'day_plan_summary',

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .add_day_plan": "_add_day_plan_click",
            "click .del_day_data": "_on_del_day_data",
            "click .plan_rail": "_on_plan_rail"
        }),

        weeks: [],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.day_plan_id = action.context.active_id || action.params.active_id
        },

        /**
         * 添加日计划
         */
        _add_day_plan_click: function (event) {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.add_day_plan_data_wizard",
                target: 'new',
                views: [[false, 'form']],
            }, {
                    on_close: function (res) {

                        if (!res || res == 'special') {
                            return
                        }

                        var target = event.target
                        var dev_id = parseInt($(target).attr('dev-id'))

                        var rule = false
                        var temp_rule = false
                        if (res.rule) {
                            rule = res.data.rule.data.id
                        }

                        if (res.data.temp_rule) {
                            temp_rule = res.data.temp_rule.data.id
                        }

                        // 添加临时数据
                        self.add_temp_data({
                            dev_id: dev_id,
                            plan_date: self.plan_date,
                            start_time: res.data.start_time,
                            end_time: res.data.end_time,
                            plan_type: res.data.plan_type,
                            rule: rule,
                            temp_rule: temp_rule,
                            remark: res.data.remark
                        });

                    }
                });
        },

        /**
         * 添加临时数据
         */
        add_temp_data: function (data) {
            this._rpc({
                "model": "metro_park_maintenance.add_day_plan_data_wizard",
                "method": "add_day_plan_data",
                "args": [data]
            }).then(function (rst) {})
        },

        start: function () {
            this._super.apply(this, arguments)
            this.$el.css("margin", "10px")
        },

        // 获取日计划数据
        willStart: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                var def = $.Deferred();
                self._rpc({
                    model: 'metro_park_maintenance.plan_data',
                    method: 'get_day_plan_info',
                    args: [self.day_plan_id]
                }).then(function (res) {
                    self.plan_datas = res.plan_datas
                    self.devs = res.devs
                    self.rules = res.rules
                    self.plan_date = res.plan_date
                    def.resolve()
                })
                return def;
            })
        },

        /**
         * 取得规程
         * @param {*} dev_id 
         * @param {*} date 
         */
        get_rules: function (dev_id, date) {
            var key = dev_id + "_" + date;
            if (key in this.plan_datas) {
                return this.plan_datas[key]['rules']
            } else {
                return []
            }
        },

        /**
         * 安排轨道位置
         */
        _on_plan_rail: function() {
            // 先取得相关的info
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "get_rail_plan_info",
                "args": [day_plan_id]
            })
        },

        /**
         * 取得规程名称
         * @param {*} rule 
         */
        get_rule_name: function (rule) {
            var ar = rule.split(',')
            if (ar.length > 0) {
                return ar[0]
            } else {
                return ''
            }
        },

        /**
         * 取得日计划数据
         */
        get_day_plan_data: function (dev_id) {
            var data = this.plan_datas[dev_id] || undefined
            if (data) {
                return data.plan_data.rule_infos
            } else {
                return []
            }
        },

        /**
         * 删除日计划数据
         */
        _on_del_day_data: function () { 

        }
    });

    core.action_registry.add('day_plan_summary', day_plan_summary);
    return day_plan_summary;
});