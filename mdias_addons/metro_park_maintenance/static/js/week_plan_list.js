odoo.define('funenc.week_plan_list', function (require) {
    "use strict";

    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var core = require('web.core')
    var qweb = core.qweb

    var week_plan_list_render = ListRenderer.extend({})
    
    var week_plan_list_controller = ListController.extend({
        data_list: undefined,

        year: undefined,
        week: undefined,

        events: _.extend({}, ListController.prototype.events, {}),
        
        init: function() {
            this._super.apply(this, arguments);
        },

        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.$buttons.on('click', '.o_list_button_add', this._add_new_week_plan.bind(this));

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
         * 添加新的周计划，这里先从后端去获获取action是为了动态domain, 不然odoo会进行缓存
         */
        _add_new_week_plan: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.week_plan_wizard",
                "method": "get_week_plan_action",
                "args": []
            }).then(function (rst) {
                self.do_action(rst, {
                    on_close: function (res) {
                        self.trigger_up('reload');
                    }
                })
            })
        }
    })

    var week_plan_list = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: week_plan_list_render,
            Controller: week_plan_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('week_plan_list', week_plan_list);

    return week_plan_list;
});