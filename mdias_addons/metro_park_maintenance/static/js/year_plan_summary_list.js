/**
 * 年计划汇部显示
 */
odoo.define('funenc.year_plan_summary_list', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var core = require('web.core')
    var qweb = core.qweb
    var utility = require('metro_park_maintenance.utility')

    var year_plan_summary_list_render = ListRenderer.extend({})

    var year_plan_summary_list_controller = ListController.extend({
        data_list: undefined,
        buttons_template: 'Funenc.YearPlan.buttons',

        events: _.extend({}, ListController.prototype.events, {
            "click .o_list_recompute": "_on_recompute_btn_click",
            "click .view_by_time_line": "_view_by_time_line",
            "click .publish_plan": "_publish_plan",
        }),

        _on_import_btn_click: function () {
            var self = this
            this.do_action({
                name: '年计划向导',
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "year_plan_import_wizard",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    // 重新加载
                    self.trigger_up('reload');
                }
            });
        },

        /**
         * 先弹出让用户选择月份
         */
        _on_recompute_btn_click: function () {
            var self = this
            $.when(this._rpc({
                "model": "year_plan_compute_wizard",
                "method": "get_work_class_count",
                "args": []
            }), this._rpc({
                "model": "year_plan_compute_wizard",
                "method": "get_compute_host",
                "args": []
            })).then(function (work_class_count, calc_host) {
                return self.do_action({
                    name: '编制计划',
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: "year_plan_compute_wizard",
                    target: 'new',
                    context: {
                        "default_work_class_count": work_class_count,
                        "default_calc_host": calc_host
                    },
                    views: [[false, 'form']],
                }, {
                    on_close: function (res) {
                        if (!res || res == 'special') {
                            return
                        }
                        // 如果当前计划已经发布则不能再进行计算
                        self.gen_plan(res)
                    }
                });
            })
        },

        /**
         * 初始化，保存年份
         */
        init: function () {
            this._super.apply(this, arguments);
            var record = this.model.get(this.handle, { raw: true })
            var context = record.getContext();
            this.record = record
            this.year = context.year;
            this.year_plan_id = context.active_id
        },

        /**
         * 开始
         */
        willStart: function () {
            return this._super.apply(this, arguments)
        },

        /**
         * 渲染按扭
         * @param {*} $node 
         * @param {*} info 
         */
        _render_btns: function ($node, info) {
            this.$buttons = $(qweb.render(this.buttons_template, {
                widget: this, info: info
            }));
            this.$buttons.appendTo($node);
        },

        /**
         * 渲染按扭
         * @param {*} $node 
         */
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                var self = this
                this._rpc({
                    "model": "metro_park_maintenance.year_plan",
                    "method": "get_year_plan_info",
                    "args": [this.year]
                }).then(function (info) {
                    self._render_btns($node, info)
                    self.trigger_up('reload')
                })
            }
        },

        /**
         * 通过时间轴进行查看
         */
        _view_by_time_line: function () {
            this.do_action({
                type: 'ir.actions.client',
                tag: 'year_plan_time_line',
                name: '年计划' + this.year,
                context: {
                    "year_plan_id": this.year_plan_id,
                },
                "params": {
                    "active_id": this.year_plan_id
                }
            });
        },

        /**
         * 发布计划
         */
        _publish_plan: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.year_plan",
                "method": "publish_plan",
                "args": [this.year_plan_id]
            }).then(function (rst) {
                self.do_warn('提示', '发布计划成功', true);
            })
        },

        /**
         * 生成计划, 直接从前端通过websocket调用算法生成计划
         */
        gen_plan: function (res) {
            if (this.year && this.year != '') {
                var self = this
                var plan_info = undefined
                this._rpc({
                    "model": "year_plan_compute_wizard",
                    "method": "get_wizard_data",
                    "args": [res.res_id]
                }).then(function (rst) {
                    var info = rst
                    info.year = self.year
                    info.year_plan_id = self.year_plan_id
                    info.detail_id = self.year_plan_id
                    return self._rpc({
                        "model": "metro_park_maintenance.year_plan",
                        "method": "get_year_plan_data",
                        "args": [info]
                    })
                }).then(function (rst) {
                    var data = rst.data
                    var calc_host = data.calc_host
                    if (!_.str.startsWith(calc_host, "ws://")) {
                        calc_host = "ws://" + calc_host
                    }
                    plan_info = data
                    return utility.do_plan_by_websocket(calc_host, rst);
                }).then(function (rst) {
                    return self._rpc({
                        "model": "metro_park_maintenance.year_plan",
                        "method": "deal_plan_data",
                        "args": [plan_info, rst]
                    })
                }).then(function () {
                    self.do_warn('提示', '年计划生成成功!', true);
                    self.trigger_up('reload');
                }).fail(function (error) {
                    self.do_warn('提示', '计算出错!' + error, true);
                })
            }
        }
    })

    var year_plan_summary_list = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: year_plan_summary_list_render,
            Controller: year_plan_summary_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('year_plan_summary_list', year_plan_summary_list);

    return year_plan_summary_list;
});