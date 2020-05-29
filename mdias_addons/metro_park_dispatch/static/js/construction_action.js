odoo.define('funenc.construction_dispatch_action', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var sub_list_widget = require('funenc.sub_list_widget');
    var qweb = core.qweb;
    var _t = core._t;

    var construction_dispatch_controller = ListController.extend({
        renderButtons: function ($node) {

        }
    });
    var log_controller = ListController.extend({});

    /**
     * 施工调度信息页面
     */
    var construction_dispatch_action = AbstractAction.extend(ControlPanelMixin, {
        template: 'construction_list_template',
        top_list: undefined,
        bottom_list: undefined,
        start: function () {
            this._super.apply(this, arguments)

            var top_list_box = this.$(".top_box")
            var bottom_list_box = this.$(".bottom_box");

            // 上方列表
            var top_list = new sub_list_widget(this, {
                'controller_class': construction_dispatch_controller,
                'res_model': 'metro_park_dispatch.construction_dispatch'
            })
            top_list.appendTo(top_list_box)

            // 下方列表
            var bottom_list = new sub_list_widget(this, {
                'controller_class': log_controller,
                'res_model': 'metro_park_dispatch.construction_sync_record'
            })
            bottom_list.appendTo(bottom_list_box)

            // control panel
            this._renderButtons();
        },

        manual_sync: function () {
            this._rpc({
                "model": "metro_park_dispatch.construction_dispatch",
                "method": "manual_sync",
                "args": []
            })
        },

        /**
         * 渲染buttons
         */
        _renderButtons: function () {
            this.$buttons = $(qweb.render('metro_park_dispatch.construction_button'));
            this.$buttons.on('click .manual_syn', function (event) {
                self.manual_sync();
            });
            var self = this;
            this.$buttons.on('change .auto_sync', function (event) {
                var checked = self.$buttons.find('.auto_sync').prop("checked");
                self._rpc({
                    model: 'metro_park_base.system_config',
                    method: 'set_auto_pull_construction_data',
                    args: [checked]
                }).then(function (result) {
                    console.log('update config succes!');
                });
            })
            this.$buttons.prependTo(this.$('.btns_box'))
        }
    });

    core.action_registry.add('construction_dispatch_action', construction_dispatch_action);

    return construction_dispatch_action;
});