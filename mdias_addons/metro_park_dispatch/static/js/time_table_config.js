odoo.define('funenc.time_table_config', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var sub_list_widget = require('funenc.sub_list_widget');

    var nor_config_controller = ListController.extend({});
    var special_config_controller = ListController.extend({});

    /**
     * 施工调度信息页面
     */
    var time_table_config_action = AbstractAction.extend(ControlPanelMixin, {
        template: 'time_table_config',
        top_list: undefined,
        bottom_list: undefined,
        events: {
            'click .add_special': '_onAddSpecialClick'
        },
        start: function () {
            this._super.apply(this, arguments)

            var top_list_box = this.$(".nor_box")
            var bottom_list_box = this.$(".special_box");

            // 日常配置
            this.top_list = new sub_list_widget(this, {
                'controller_class': nor_config_controller,
                'res_model': 'metro_park_dispatch.nor_time_table_config'
            })
            this.top_list.appendTo(top_list_box)

            // 特殊日期配置
            this.bottom_list = new sub_list_widget(this, {
                'controller_class': special_config_controller,
                'res_model': 'metro_park_dispatch.special_days_config',
                'custom_area_template': 'time_table_special.buttons'
            })
            this.bottom_list.appendTo(bottom_list_box)

            // control panel
            this._renderButtons();
            this._updateControlPanel();
        },

        willStart: function () {
            return this._super.apply(this, arguments);
        },

        do_show: function () {
            this._updateControlPanel();
        },

        _onAddSpecialClick: function () {
            var self = this
            this._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'metro_park_dispatch.special_days_config_form' },
            }).then(function (res) {
                self.do_action({
                    type: 'ir.actions.act_window',
                    name: '特殊日期',
                    target: 'new',
                    res_model: 'metro_park_dispatch.special_days_config',
                    // 使用默认视图 
                    views: [[res, 'form']]
                }, {
                        size: 'normal',
                        on_close: function () {
                            self.bottom_list.reload();
                        }
                    })
            })
        },

        /**
         * 渲染buttons
         */
        _renderButtons: function () {
            // this.$buttons = $(qweb.render('construction_button'));
            // this.$buttons.on('click .manual_syn', function (event) {
            //     self._do_auto_sync();
            // });
            // var self = this;
            // this.$buttons.on('change .auto_sync', function (event) {
            //     var checked = self.$buttons.find('.auto_sync').prop("checked");
            //     self._rpc({
            //         model: 'metro_park_base.system_config',
            //         method: 'set_auto_pull_construction_data',
            //         args: [checked]
            //     }).then(function (result) {
            //         console.log('update config succes!');
            //     });
            // })
        },

        /**
         * 自动同步
         */
        _do_auto_sync: function () {

        },

        /**
         * 刷新控制面版
         */
        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        }
    });

    core.action_registry.add('time_table_config_action', time_table_config_action);

    return time_table_config_action;
});