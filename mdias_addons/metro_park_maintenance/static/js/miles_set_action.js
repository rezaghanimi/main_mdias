odoo.define('funenc.miles_set_action', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var dialogs = require('web.view_dialogs')
    var sub_list_widget = require('funenc.sub_list_widget');
    var qweb = core.qweb;

    var _t = core._t;

    var miles_set_controller = ListController.extend({});

    var log_controller = ListController.extend({});

    /**
     * 公里数设置
     */
    var miles_set_action = AbstractAction.extend(ControlPanelMixin, {
        buttons_template: 'miles_set_btn',
        template: 'miles_set_template',
        top_list: undefined,
        bottom_list: undefined,
        tree_id: undefined,
        events: {
            // 'click .btn_action_miles': '_onActionMilesClick',
            // 'click .btn_add_miles': '_onAddMilesClick',
            // 'click .btn_import_miles': '_onImportMilesInfo',
            'click .btn_export_miles': '_onExportMilesClick',
            'click .btn_sync_manual': '_onSyncManualClick',
            'click .btn_history_import': '_onImportHistoryBut',
            'click .btn_all_history': '_onHistoryButOpen',
        },
        start: function () {
            var self = this;
            self._super.apply(this, arguments);
            self._renderButtons();
            self._updateControlPanel();

            var top_list_box = self.$(".top_box");
            var bottom_list_box = self.$(".bottom_box");
            var get_data = function () {
                return self._rpc({
                    model: 'ir.model.data',
                    method: 'xmlid_to_res_id',
                    args: ['metro_park_maintenance.train_miles_list'],
                })
            };
            return $.when(get_data()).then(function (result1) {
                self.top_list = new sub_list_widget(self, {
                    'controller_class': miles_set_controller,
                    'res_model': 'metro_park_maintenance.train_dev',
                    'list_view_id': result1,
                });
                self.top_list.appendTo(top_list_box);
                // 日志
                self.bottom_list = new sub_list_widget(self, {
                    'controller_class': log_controller,
                    'res_model': 'metro_park_maintenance.operation_record'
                });
                self.bottom_list.appendTo(bottom_list_box)
            })
        },

        /**
         * 渲染buttons
         */
        _renderButtons: function () {
            this.$buttons = $(qweb.render('miles_set_btn'));
            this.$buttons.appendTo(this.$('.btns_box'));
        },

        _onActionMilesClick: function () {
            var self = this;
            self._rpc({
                model: 'metro_park_maintenance.history_miles',
                method: 'get_miles_predict_action',
                args: [self.id, false]
            }).then(function (res) {
                self.do_action(res)
            })
        },

        _onAddMilesClick: function (e) {
            var self = this
            self._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'metro_park_maintenance.train_miles_set_wizard_form' },
            }).then(function (res) {
                self.do_action({
                    type: 'ir.actions.act_window',
                    name: '公里数录入',
                    target: 'new',
                    res_model: 'metro_park_maintenance.train_miles_set_wizard',
                    // 使用默认视图
                    views: [[res, 'form']]
                }, {
                    // 返回时调用
                    on_close: function () {
                        self.top_list.reload();
                        self.bottom_list.reload();
                    }
                })
            })
        },

        _onImportMilesInfo: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_dispatch.train_miles_import",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    self.top_list.reload();
                }
            });
        },

        _onExportMilesClick: function () {
            var self = this
            var d = new dialogs.FormViewDialog(self, {
                res_model: 'metro_park_maintenance.train_miles_export_wizard',
                buttons: [{
                    text: "导出",
                    classes: "btn btn-primary",
                    click: function () {
                        var year = d.$el.find('.o_field_widget[name=year] input').val()
                        var month = d.$el.find('.o_field_widget[name=month] input').val()
                        self.do_action({
                            name: '公里统计数导出',
                            type: 'ir.actions.act_url',
                            url: '/get_miles_export_wizard/' + year + '/' + month
                        })
                        d.close()
                    }
                }, {
                    text: "取消",
                    classes: "btn-secondary",
                    close: true
                }]
            });
            d.open()
        },

        _onSyncManualClick: function () {
            var self = this
            self._rpc({
                model: 'metro_park_maintenance.train_dev',
                method: 'sync_manual_miles',
            }).then(function () {
                self.top_list.reload();
            })
        },

        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        },

        /***
         * 历史公里数导入
         * @private
         */
        _onImportHistoryBut: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "maintenance.vehicle.history.import",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    self.top_list.reload();
                }
            });
        },

        /***
         * 跳转到所有的车辆的公里数列表
         */
        _onHistoryButOpen: function () {
            var self = this;
            self._rpc({
                model: 'metro_park_maintenance.train_dev',
                method: 'open_vehicle_data_action',
                args: [self.id, false]
            }).then(function (res) {
                self.do_action(res)
            })
        }

    });

    core.action_registry.add('miles_set_action', miles_set_action);

    return miles_set_action;
});