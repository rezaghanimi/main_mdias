odoo.define('metro_park_dispatch.inter_lock_table', function (require) {
    "use strict";

    var BasicView = require('web.BasicView');
    var ListRenderer = require('web.ListRenderer');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView')
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.fnt_table_render")
    var BasicModel = require('web.BasicModel');
    var core = require("web.core")
    var qweb = core.qweb

    // 控制器
    var inter_lock_table_controller = ListController.extend({
        buttons_template: 'metro_park.interlock.table.buttons',

        renderButtons: function ($node) {
            this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
            this.$buttons.find('[name="import_time_table"]').on('click', this._on_import_interlock_table.bind(this))
            this.$buttons.appendTo($node);
        },

        _on_import_interlock_table: function (event) {
            var self = this
            this._rpc({
                "model": "metro_park.interlock.import_wizard",
                "method": "get_import_interlock_table_wizard",
                "args": []
            }).then(function (action) {
                self.do_action(action, {
                    on_close: function (res) {
                        self.reload();
                    }
                })
            })
        }
    })
    

    // 重写，自定义搜索
    var inter_lock_table_model = BasicModel.extend({})

    // 重写，渲染列表视图
    var inter_lock_table_render = ListRenderer.extend({})

    // 扩展、重新配置list
    var inter_lock_table = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Model: inter_lock_table_model,
            Renderer: inter_lock_table_render,
            Controller: inter_lock_table_controller,
        })
    });

    view_registry.add("inter_lock_table", inter_lock_table);

    return inter_lock_table;
});
