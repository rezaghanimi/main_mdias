/**
 * 月生产说明, 这个里面要展示周计划的内容，但不计算周计划的内容
 */
odoo.define('metro_park.month_plan_works', function (require) {
    "use strict";

    var month_month_plan_editor = require('metro_park.month_month_plan_editor');
    var core = require('web.core');

    // 加载的数据有所不同
    var month_plan_works = month_month_plan_editor.extend({
        template: 'month_plan_works',

        events: _.extend({}, month_month_plan_editor.prototype.events, {
            "click .clear_month_data": "_on_clear_plan"
        }),

        /**
         * 重新载入
         */
        _reload: function () {
            var self = this
            this._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_month_work_info',
                args: [self.month_plan_id]
            }).then(function (res) {
                self.rules = res.rules
                self.plan_datas = res.plan_datas
                self.dates = res.dates
                self.devs = res.devs
                self.repair_counts = res.repair_counts
                // 重新渲染并替换
                self.renderElement();
                self.on_attach_callback();
            })
        },

        // 获取月计划数据
        willStart: function () {
            var self = this
            return this._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_month_work_info',
                args: [self.month_plan_id]
            }).then(function (res) {
                self.rules = res.rules
                self.plan_datas = res.plan_datas
                self.dates = res.dates
                self.devs = res.devs
                self.repair_counts = res.repair_counts
                self.state = res.state
            })
        },

        /**
         * 重写，只删除周计划的数据, 月计划的数据在月计划说明中去删除
         */
        _on_clear_plan: function () {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.month_plan_clear_wizard",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    // 这样写是为了解决
                    var res_id = res.res_id
                    self._rpc({
                        "model": "metro_park_maintenance.month_plan_clear_wizard",
                        "method": "clear_week_datas",
                        "args": [res_id, self.month_plan_id]
                    }).then(function (rst) {
                        self._reload()
                    })
                }
            });
        }
    });

    core.action_registry.add('month_plan_works', month_plan_works);
    return month_plan_works;
});