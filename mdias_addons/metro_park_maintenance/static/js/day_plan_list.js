/**
 * 日计划, 重写list, 改变创建按扭的行为
 */
odoo.define('funenc.day_plan_list', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var core = require('web.core')
    var qweb = core.qweb

    var day_plan_list_render = ListRenderer.extend({})

    var day_plan_list_controller = ListController.extend({
        data_list: undefined,

        events: _.extend({}, ListController.prototype.events, {}),

        /**
         * 渲染按扭
         * @param {*} $node 
         */
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.$buttons.on('click', '.o_list_button_add', this._add_new_day_plan.bind(this));

                this._assignCreateKeyboardBehavior(this.$buttons.find('.o_list_button_add'));
                this.$buttons.find('.o_list_button_add').tooltip({
                    delay: { show: 200, hide: 0 },
                    title: function () {
                        return qweb.render('CreateButton.tooltip');
                    },
                    trigger: 'manual',
                });

                this.$buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
                this.$buttons.appendTo($node);
            }
        },

        /**
         * 添加日计划
         */
        _add_new_day_plan: function (event) {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.day_plan_wizard",
                "method": "get_day_plan_action",
                "args": []
            }).then(function (rst) {
                if (rst) {
                    self.do_action(rst, {
                        on_close: function (res) {
                            self.reload();
                        }
                    })
                }
            })
        },

        /**
         * 生成计划，直接从前端调用算法生成计划
         */
        gen_plan: function () {
            var self = this;
            if (!this.cur_year || this.cur_year == '') {
                return
            }
            this._rpc({
                "model": "metro_park_maintenance.day_plan_detail",
                "method": "do_rpc_plan",
                "args": [this.cur_year]
            }).then(function (rst) {
                self.reload();
            })
        }
    })

    var day_plan_list = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: day_plan_list_render,
            Controller: day_plan_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('day_plan_list', day_plan_list);

    return day_plan_list;
});