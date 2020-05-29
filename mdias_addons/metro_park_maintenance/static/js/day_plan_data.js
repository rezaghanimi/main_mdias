/**
 * 日计划数据
 */
odoo.define('funenc.day_plan_data', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var day_plan_list_render = ListRenderer.extend({})
    var day_plan_list_controller = ListController.extend({
        data_list: undefined,
        buttons_template: 'day_plan_btns',

        willStart: function () {
            return this._super.apply(this, arguments)
        },

        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.$buttons.on('click', '.o_list_button_add', this._compute_day_plan.bind(this));

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

        start: function () {
            var self = this
            this._super.apply(this, arguments)
        },

        _compute_day_plan: function() {
            var record = this.model.get(this.handle, {raw: true})
            var id = record.data.id
            this._rpc({
                "model": "metro_park_maintenance.day_plan_total",
                "method": "do_rpc_plan",
                "args": [this.cur_year]
            })
        }
    })

    var day_plan_data_view = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: day_plan_list_render,
            Controller: day_plan_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('day_plan_data_view', day_plan_data_view);

    return day_plan_data_view;
});