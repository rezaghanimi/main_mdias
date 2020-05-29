/**
    年计划列表
**/
odoo.define('funenc.year_plan_list', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var core = require('web.core')
    
    var qweb = core.qweb
    
    var year_plan_list_render = ListRenderer.extend({})

    var year_plan_list_controller = ListController.extend({
        data_list: undefined,
        buttons_template: 'metro_park_maintaince.year_plan_list_buttons',
        events: _.extend({}, ListController.prototype.events, {
            "click .add_year_plan": "_add_new_year_plan",
            "click .import_year_plan": "_on_import_year_plan",
            "click .download_year_plan_template": "_download_year_plan_template",
            "click .balance_rule_offset": "_balance_rule_offset",
        }),

        renderButtons: function ($node) {
            this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
            this.$buttons.appendTo($node);
        },

        _balance_rule_offset: function() {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                name: "修次管理",
                res_model: "metro_park_maintenance.balance_rule_offset",
                views: [[false, 'list'], [false, 'form']],
            });
        },

        _on_import_year_plan: function() {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.year_plan_import_wizard",
                "method": "import_year_plan",
                "args": []
            }).then(function (action) {
                self.do_action(action)
            })
        },

        _download_year_plan_template: function() {
            this.do_action({
                'type': 'ir.actions.act_url',
                'url': '/metro_park_maintenance/get_year_plan_template',
            })
        },

        /**
         * 添加新的年计划
         */
        _add_new_year_plan: function () {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "year_plan_wizard",
                target: 'new',
                views: [[false, 'form']],
            }, {
                    on_close: function (res) {
                        self.trigger_up('reload');
                    }
                });
        },

        /**
         * 生成计划，直接从前端调用算法生成计划
         */
        gen_plan: function () {
            this._rpc({
                "model": "metro_park_maintenance.year_plan_detail",
                "method": "do_rpc_plan",
                "args": [this.cur_year]
            })
        },

        /**
         * 重写，进入查看模式 
         * @param {*} event 
         */
        // _onOpenRecord: function (event) {
        //     event.stopPropagation();
        //     var self = this;
        //     var record = this.model.get(event.data.id, {raw: true});
        //     this._rpc({
        //         "model": "metro_park_maintenance.year_plan",
        //         "method": "view_year_plan_summary_action",
        //         "args": [record.res_id]
        //     }).then(function(action) {
        //         if (action) {
        //             self.do_action(action)
        //         }
        //     })
        // }
    })

    var year_plan_list = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: year_plan_list_render,
            Controller: year_plan_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('year_plan_list', year_plan_list);

    return year_plan_list;
});