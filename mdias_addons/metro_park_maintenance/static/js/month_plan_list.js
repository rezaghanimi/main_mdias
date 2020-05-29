odoo.define('metro_park.month_plan_with_wizard', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var core = require('web.core')
    var qweb = core.qweb

    var month_plan_list_render = ListRenderer.extend({})
    var month_plan_list_controller = ListController.extend({
        data_list: undefined,

        events: _.extend({}, ListController.prototype.events, {
            "click .export_produce_plan": "export_produce_plan"
        }),

        /**
         * 导出生产系
         */
        export_produce_plan: function() {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "export_produce_plan",
                "args": []
            }).then(function(action){
                self.do_action(action)
            })
        },

        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.$buttons.on('click', '.o_list_button_add', this._add_new_month_plan.bind(this));

                this._assignCreateKeyboardBehavior(this.$buttons.find('.o_list_button_add'));
                this.$buttons.find('.o_list_button_add').tooltip({
                    delay: { show: 200, hide: 0 },
                    title: function () {
                        return qweb.render('CreateButton.tooltip');
                    },
                    trigger: 'manual',
                });
                this.$buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
                var $extra_btn = $(qweb.render("metro_park_maintenance.export_produce_plan"))
                $extra_btn.appendTo(this.$buttons)
                this.$buttons.appendTo($node);
            }
        },

        /**
         * 添加新的月计划
         */
        _add_new_month_plan: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.month_plan_wizard",
                "method": "get_month_plan_action",
                "args": []
            }).then(function (rst) {
               if (rst) {
                   self.do_action(rst, {
                        on_close: function (res) {
                            // 重新加载
                            self.trigger_up('reload');
                        }
                   })
               }
            })
        },

        /**
         * 生成计划，直接从前端调用算法生成计划
         */
        gen_plan: function () {
            if (!this.cur_year || this.cur_year == '') {
                return
            }
            this._rpc({
                "model": "metro_park_maintenance.year_plan_detail",
                "method": "do_rpc_plan",
                "args": [this.cur_year]
            })
        }
    })

    var month_plan_with_wizard = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: month_plan_list_render,
            Controller: month_plan_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('month_plan_with_wizard', month_plan_with_wizard);

    return month_plan_with_wizard;
});