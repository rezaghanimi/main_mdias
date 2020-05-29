odoo.define('metro_park_dispatch.work_shop_day_plan_data_list', function(require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var work_shop_day_plan_render = ListRenderer.extend({})

    var work_shop_day_plan_controller = ListController.extend({
        buttons_template: 'work_shop_day_plan_list.btns',

        events: _.extend({}, ListController.prototype.events, {
            "click .set_run_trains": "set_run_trains",
            "click .plan_rails": "plan_rails",
            "click .publish_plan": "publish_plan"
        }),

        // context中传过来的是work_shop_day_plan的类容
        set_run_trains: function() {
            var self = this
            var work_shop_day_plan_id = this.initialState.context.work_shop_day_plan_id
            this._rpc({
                "model": "metro_park_dispatch.work_shop_day_plan",
                "method": "set_run_trains",
                "args": [work_shop_day_plan_id]
            }).then(function(rst) {
                self.do_action(rst)
            })
        },

        plan_rails: function() {
            var self = this
            var work_shop_day_plan_id = this.initialState.context.work_shop_day_plan_id
            this._rpc({
                "model": "metro_park_dispatch.work_shop_day_plan",
                "method": "plan_rails",
                "args": [work_shop_day_plan_id]
            }).then(function(rst) {
                self.reload()
            })
        },

        publish_plan: function() {
            var self = this
            var work_shop_day_plan_id = this.initialState.context.work_shop_day_plan_id
            this._rpc({
                "model": "metro_park_dispatch.work_shop_day_plan",
                "method": "publish_plan",
                "args": [work_shop_day_plan_id]
            }).then(function(rst) {
                self.reload()
            })
        },

        /**
         * 重写，添加渲染按扭
         * @param {} node 
         */
        renderButtons: function(node) {
            if (!this.noLeaf && this.hasButtons) {
                this.buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.buttons.appendTo(node);
            }
        }
    })

    var work_shop_day_plan_list = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: work_shop_day_plan_render,
            Controller: work_shop_day_plan_controller
        }),
        viewType: 'list'
    });

    view_registry.add('work_shop_day_plan_list', work_shop_day_plan_list);

    return work_shop_day_plan_list;
});