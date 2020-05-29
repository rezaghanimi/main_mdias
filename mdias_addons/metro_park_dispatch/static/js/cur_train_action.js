odoo.define('funenc.cur_train_action', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('funenc.fnt_table_controller');
    var AbstractAction = require('web.AbstractAction');
    var sub_list_widget = require('funenc.sub_list_widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var qweb = core.qweb;

    var cur_train_manage_controller = ListController.extend({});

    var log_controller = ListController.extend({});

    /**
     * 现车管理页面
     */
    var cur_train_manage = AbstractAction.extend(ControlPanelMixin, {
        template: 'two_list_template',
        top_list: undefined,
        bottom_list: undefined,
        $buttons: undefined,
        start: function () {
            this._super.apply(this, arguments)

            var top_list_box = this.$(".top_box")
            var bottom_list_box = this.$(".bottom_box");

            // 上方列表
            this.top_list = new sub_list_widget(this, {
                'controller_class': cur_train_manage_controller,
                'res_model': 'metro_park_dispatch.cur_train_manage'
            })
            this.top_list.appendTo(top_list_box)

            // 下方列表
            this.bottom_list = new sub_list_widget(this, {
                'controller_class': log_controller,
                'res_model': 'metro_park_dispatch.cur_train_operation_log'
            })
            this.bottom_list.appendTo(bottom_list_box)

            // control panel
            this._renderButtons();
            this._updateControlPanel();
        },

        do_show: function () {
            this._updateControlPanel();
        },

        _renderButtons: function () {
            this.$buttons = $(qweb.render('cur_train_manage_buttons'));
            // this.$buttons.on('click', ...);
        },

        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        }
    });

    core.action_registry.add('cur_train_manage', cur_train_manage);

    return cur_train_manage;
});