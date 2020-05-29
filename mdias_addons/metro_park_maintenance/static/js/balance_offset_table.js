odoo.define('metro_park.balance_offset_table', function (require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var balance_offset_table_render = ListRenderer.extend({})

    var balance_offset_table_controller = ListController.extend({
        buttons_template: "metro_park_maintenance.balance_offset_table.buttons",

        events: _.extend({}, ListController.prototype, {
            "click .init_offset": "_on_init_balance_offset",
            'click .update_year_month': '_update_year_month',
            'click .syn_from_repair': '_syn_from_repair',
            'click .syn_to_repair': '_syn_to_repair',
            "click .import_offset": "_import_offset",
            "click .export_offset": "_export_offset"
        }),

        /**
         * 初始化修程设置
         */
        _on_init_balance_offset: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.balance_rule_offset",
                "method": "init_balance_offset",
                "args": []
            }).then(function (rst) {
                self.trigger_up('reload');
            })
        },

        _update_year_month: function () {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.update_balance_offset",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    // 重新加载
                    self.trigger_up('reload');
                }
            });
        },

        /**
         * 导入修次
         */
        _import_offset: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.balance_rule_offset",
                "method": "import_offset",
                "args": []
            }).then(function (rst) {
                self.do_action(rst, {
                    on_close: function (res) {
                        self.trigger_up('reload');
                    }
                });
            })
        },

        /**
         * 导出偏移
         */
        _export_offset: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.balance_rule_offset",
                "method": "export_offset",
                "args": []
            }).then(function (rst) {
                self.do_action(rst);
            })
        },

        /**
         * 从检修同步
         */
        _syn_from_repair: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.balance_rule_offset",
                "method": "syn_from_repair",
                "args": []
            }).then(function () {
                self.trigger_up('warning', {
                    title: '提示',
                    message: '同步成功'
                });
            })
        },

        /**
         * 同步到检修
         */
        _syn_to_repair: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.balance_rule_offset",
                "method": "syn_to_repair",
                "args": []
            }).then(function () {
                self.trigger_up('warning', {
                    title: '提示',
                    message: '同步成功'
                });
            })
        }
    })

    var balance_offset_table_view = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: balance_offset_table_render,
            Controller: balance_offset_table_controller
        }),
        viewType: 'list'
    });

    view_registry.add('balance_offset_table_view', balance_offset_table_view);

    return balance_offset_table_view;
});
