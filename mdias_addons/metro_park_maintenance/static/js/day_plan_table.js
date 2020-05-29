/**
 * 日计划显示列表, 这里为实际的rule的列表
 */
odoo.define('metro_park_maintenance.day_plan_table', function (require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var core = require('web.core');
    var qweb = core.qweb
    var core = require('web.core');
    var utility = require('metro_park_maintenance.utility')
    var dialogs = require('web.view_dialogs');

    var day_plan_table_render = ListRenderer.extend({})

    var day_plan_table_controller = ListController.extend({

        buttons_template: 'metro_park_maintenance.day_plan_table_btns',

        events: _.extend({}, ListController.prototype.events, {
            "click .publish_plan": "_on_publish_plan",
            'click .add_normal_plan': "_on_add_normal_plan",
            'click .add_temp_plan': "_on_add_temp_plan",
            "click .plan_rail": "plan_rail",
            "click .plan_train": "plan_train",
            "click .plan_miles": "plan_miles",
            "click .plan_high_run_train": "plan_high_run_train",
            "click .manage_run_trains": "manage_run_trains",
            "click .pre_day_trains_manage": "pre_day_trains_manage",
            "click .simulate_train_info": "simulate_train_info",
            "click .import_mile_info": "_import_mile_info",
            "click .import_day_plans": "_import_day_plans"
        }),

        /**
         * 重写，添加渲染按扭
         * @param {} node 
         */
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.$buttons.appendTo($node);
            }
            // 再渲染一点别信息\
            // var plan_id = this.initialState.context.plan_id
            // this._rpc({
            //     "model": "metro_park_maintenance.day_plan",
            //     "method": "get_plan_info",
            //     "args": [plan_id]
            // }).then(function (rst) {
            //     var info = rst.info
            //     var $info = $("<div style='display: inline-block; margin-left: 10px'>" + info + "</di>")
            //     $info.appendTo($node)
            // })
        },

        /**
         * 添加常规规程
         */
        _on_add_normal_plan: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id

            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.add_day_plan_data_wizard",
                target: 'new',
                context: {
                    'day_plan_id': plan_id,
                    'default_date': this.initialState.context.plan_date,
                    'default_rule_type': 'normal'
                },
                views: [
                    [false, 'form']
                ],
            }, {
                on_close: function (res) {
                    self.reload()
                }
            });
        },

        /**
         * 添加检技通
         */
        _on_add_temp_plan: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id

            var ids = self.getSelectedIds();
            if (ids.length == 0) {
                self.do_warn('错误', '当前没有选中要安排检技通的车辆!', true);
                return
            }

            this._rpc({
                "model": "metro_park_maintenance.rule_info",
                "method": "get_selected_devs_temp_rule_ids",
                "context": {
                    "plan_id": plan_id
                },
                "args": [ids]
            }).then(function (rule_ids) {
                new dialogs.SelectCreateDialog(self, {
                    res_model: 'metro_park_maintenance.repair_tmp_rule',
                    title: '选择检技通',
                    no_create: true,
                    disable_multiple_selection: false,
                    context: {
                        "tree_view_ref": "metro_park_maintenance.repair_tmp_rule_pop_list"
                    },
                    domain: [['id', 'in', rule_ids]],
                    on_selected: function (records) {
                        var temp_rule_ids = _.pluck(records, 'id');
                        self._rpc({
                            "model": "metro_park_maintenance.rule_info",
                            "method": "add_selected_temp_rules",
                            "args": [],
                            "kwargs": {
                                "day_plan_id": plan_id,
                                "select_ids": ids,
                                "temp_rule_ids": temp_rule_ids
                            }
                        }).then(function () {
                            self.trigger_up('reload');
                        })
                    }
                }).open();
            })
        },

        /**
         * 处理数据
         * @param {*} deal_data 
         */
        deal_data: function (deal_data) {
            return this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "deal_plan_data",
                "args": [deal_data, []]
            })
        },

        /**
         * 发布计划，计划发布之后安排轨道
         */
        _on_publish_plan: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "publish_plan_to_park_dispatch",
                "args": [plan_id]
            }).then(function () {
                self.reload()
            })
        },

        plan_rail: function () {
            var self = this
            this._on_plan_rail().then(function () {
                self.reload()
            })
        },

        /**
         * 安排轨道位置
         */
        _on_plan_rail: function () {
            var plan_id = this.initialState.context.plan_id

            var self = this
            var plan_data = undefined

            var def = $.Deferred()
            // 先取得相关的info
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "get_rail_plan_info",
                "args": [plan_id]
            }).then(function (data) {
                plan_data = data
                // 取得服务器配置
                return self._rpc({
                    "model": "metro_park_base.system_config",
                    "method": "get_configs",
                    "args": []
                })
            }).then(function (config) {
                var calc_host = config.calc_host || "ws://172.16.109.196:9520"
                if (!_.str.startsWith('ws://')) {
                    calc_host = "ws://" + calc_host
                }
                return utility.do_plan_by_websocket(calc_host, {
                    "cmd": "plan_rail",
                    "data": plan_data
                });
            }).then(function (rst) {
                return self._rpc({
                    "model": "metro_park_maintenance.day_plan",
                    "method": "set_train_back_rail",
                    "args": [plan_data, rst]
                })
            }).then(function (rst) {
                def.resolve()
            }).fail(function (error) {
                def.reject(error);
            })

            return def;
        },

        plan_high_run_train: function (event) {
            this.plan_train(event, true)
        },

        /**
         * 安排车辆
         */
        plan_train: function (event) {
            event.preventDefault();
            event.stopPropagation();

            var plan_id = this.initialState.context.plan_id

            var self = this
            var plan_data = undefined

            // 先取得相关的info
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "plan_train",
                "context": {
                    "plan_high_run": false
                },
                "args": [plan_id]
            }).then(function (data) {
                plan_data = data
                // 取得服务器配置
                return self._rpc({
                    "model": "metro_park_base.system_config",
                    "method": "get_configs",
                    "args": []
                })
            }).then(function (config) {
                var calc_host = config.calc_host || "ws://172.16.109.196:9520"
                if (!_.str.startsWith('ws://')) {
                    calc_host = "ws://" + calc_host
                }
                return utility.do_plan_by_websocket(calc_host, {
                    "cmd": "plan_train",
                    "data": plan_data
                });
            }).then(function (rst) {
                return self._rpc({
                    "model": "metro_park_maintenance.day_plan",
                    "method": "deal_train_plan_data",
                    "args": [plan_id, plan_data, rst]
                })
            }).then(function (rst) {
                self.reload()
            }).fail(function (error) {
                console.log(error)
                self.do_warn('提示', '日计划生成出错!' + error, true);
            })
        },

        /**
         * 管理现车
         */
        manage_run_trains: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "get_manage_run_train_action",
                "args": [plan_id]
            }).then(function (rst) {
                self.do_action(rst)
            })
        },

        pre_day_trains_manage: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "get_pre_date_train_infos_action",
                "args": [plan_id]
            }).then(function (rst) {
                self.do_action(rst)
            })
        },

        simulate_train_info: function () {
            var self = this
            var plan_id = this.initialState.context.plan_id
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "simulate_train_info",
                "args": [plan_id]
            }).then(function (rst) { })
        },

        plan_miles: function (event) {
            var self = this
            event.preventDefault();
            event.stopPropagation();
            var plan_id = this.initialState.context.plan_id
            this._rpc({
                "model": "metro_park_maintenance.day_plan",
                "method": "get_train_info_ids",
                "args": [plan_id]
            }).then(function (ids) {
                new dialogs.SelectCreateDialog(self, {
                    res_model: 'metro_park_maintenance.pre_date_train_infos',
                    title: '选择里程修的车',
                    no_create: true,
                    disable_multiple_selection: false,
                    context: {
                        "tree_view_ref": "metro_park_maintenance.pre_date_train_infos_pop_list"
                    },
                    domain: [['id', 'in', ids]],
                    on_selected: function (records) {
                        if (!records) {
                            return
                        }
                        var tmp_ids = _.pluck(records, 'id');
                        self._rpc({
                            "model": "metro_park_maintenance.day_plan",
                            "method": "add_miles_plan",
                            "args": [],
                            "kwargs": {
                                "plan_id": plan_id,
                                "train_info_ids": tmp_ids,
                            }
                        }).then(function () {
                            self.trigger_up('reload');
                        })
                    }
                }).open();
            })
        },

        _import_mile_info: function () {
            var plan_id = this.initialState.context.plan_id
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.import_pre_day_miles_info",
                target: 'new',
                context: {
                    "default_day_plan_id": plan_id,
                },
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    this.trigger_up('reload');
                }
            });
        },

        /**
         * 导入日计划
         * @private
         */
        _import_day_plans: function () {
            var plan_id = this.initialState.context.plan_id
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.import_day_plans",
                target: 'new',
                context: {
                    "default_day_plan_id": plan_id,
                },
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    this.trigger_up('reload');
                }
            });
        }
    })

    var day_plan_table = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: day_plan_table_render,
            Controller: day_plan_table_controller
        })
    });

    view_registry.add('day_plan_table', day_plan_table);

    return day_plan_table;
});