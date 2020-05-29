odoo.define('funenc.electric_area', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var sub_list_widget = require('funenc.sub_list_widget');
    var qweb = core.qweb;
    var _t = core._t;

    var electric_area_controller = ListController.extend({

    });
    /**
     * 施工调度信息页面
     */
    var construction_dispatch_action = AbstractAction.extend(ControlPanelMixin, {
        template: 'two_list_template',
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
            this._updateControlPanel();
        },

        do_show: function () {
            this._updateControlPanel();
        },

        _renderButtons: function () {
            this.$buttons = $(qweb.render('construction_button'));
            this.$buttons.on('click .manual_syn', function(event) {
                console.log(event);
            });
        },

        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        }
    });

    core.action_registry.add('construction_dispatch_action', construction_dispatch_action);

    return construction_dispatch_action;
});