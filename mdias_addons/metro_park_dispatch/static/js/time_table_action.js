odoo.define('funenc.time_table_action', function (require) {
    "use strict";

    var core = require('web.core');
    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var sub_list_widget = require('funenc.sub_list_widget');

    var qweb = core.qweb;

    var time_table_action_controller = ListController.extend({

    });

    var log_controller = ListController.extend({});

    /**
     * 运行图管理
     */
    var time_table_action = AbstractAction.extend({
        template: 'time_table_template',
        top_list: undefined,
        bottom_list: undefined,
        $buttons: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .time_table_calendar": "_on_jump_time_table",
            "click .import_time_table": "_on_import_time_table",
            "click .manual_syn": "_on_manual_sync",
            "click .delete_time_table": "_on_delete_time_table",
        }),

        custom_events: _.extend({}, ListController.prototype.custom_events, {
            selection_changed: '_onSelectionChanged',
        }),

        _onSelectionChanged: function (event) {
            // console.log('the event is:', event)

            if (event.data.selection && event.data.selection.length > 0) {
                this.$(".delete_time_table").show()
            } else {
                this.$(".delete_time_table").hide()
            }
        },

        start: function () {
            this._super.apply(this, arguments)

            var top_list_box = this.$(".top_box")
            var bottom_list_box = this.$(".bottom_box");

            // 上方列表
            this.top_list = new sub_list_widget(this, {
                'controller_class': time_table_action_controller,
                'res_model': 'metro_park_base.time_table'
            })
            this.top_list.appendTo(top_list_box)

            // 下方列表
            this.bottom_list = new sub_list_widget(this, {
                'controller_class': log_controller,
                'res_model': 'metro_park_base.time_table_syn_log'
            })
            this.bottom_list.appendTo(bottom_list_box)

            // syn_run_chart

            // 渲染按扭
            this._renderButtons();
        },

        _on_jump_time_table: function (e) {
            this.do_action({
                'name': '运行图日历',
                'type': 'ir.actions.client',
                'tag': 'time_table_calendar',
                'target': 'current'
            });
        },

        _onSwitchView: function () {

        },

        _on_import_time_table: function (e) {
            var self = this
            this._rpc({
                model: 'ir.model.data',
                method: 'xmlid_to_res_id',
                kwargs: { xmlid: 'metro_park_dispatch.import_time_table_form' },
            }).then(function (res) {
                self.do_action({
                    type: 'ir.actions.act_window',
                    name: '导入运行图',
                    target: 'new',
                    res_model: 'metro_park_dispatch.import_time_table',
                    // 使用默认视图 
                    views: [[res, 'form']]
                }, {
                    on_close: function () {
                        self.top_list.reload()
                    }
                })
            })
        },

        /**
         * 添加手动同步
         * @param {*} e 
         */
        _on_manual_sync: function (e) {
            var self = this
            this._rpc({
                "model": "metro_park_base.time_table",
                "method": "sync_time_table",
                "args": []
            }).then(function (rst) {
                return self._rpc({
                    "model": "metro_park_base.time_table_syn_log",
                    "method": "add_log",
                    "args": [{
                        "content": "手动同步时刻表"
                    }]
                })
            }).then(function(){
                self.bottom_list.reload()
            })
        },

        _renderButtons: function () {
            this.$buttons = $(qweb.render('time_table_action_btns'));
            this.$buttons.prependTo(this.$('.btns_box'))
        },

        /**
         * 删除时刻表
         */
        _on_delete_time_table: function () {
            var controller = this.top_list.get_controller()
            if (controller) {
                controller._onDeleteSelectedRecords()
            }
        }
    });

    core.action_registry.add('time_table_action', time_table_action);

    return time_table_action;
});