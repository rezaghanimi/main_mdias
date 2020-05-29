odoo.define('metro_park_maintenance.tcms_export_tree_button', function (require) {
    "use strict";

    var BasicView = require('web.BasicView');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView')
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.fnt_table_render")
    var BasicModel = require('web.BasicModel');
    var core = require("web.core")
    var qweb = core.qweb

    // 控制器
    var export_tree_button_controller = ListController.extend({

        buttons_template: 'tcms_export_tree_button',
        renderButtons: function ($node) {
            this.par = this.searchView.action.par
            this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
            this.$buttons.find('[name="model_export"]').on('click', this.model_export.bind(this))
            this.$buttons.appendTo($node);
        },

        model_export: function (data) {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'export_data_rec',
            }).then(function (data) {
                self.do_action(data)
            })
        },
    })


    // 重写，自定义搜索
    var export_tree_button_model = BasicModel.extend({})

    // 重写，渲染列表视图
    var export_tree_button_render = ListRenderer.extend({})

    // 扩展、重新配置list
    var tcms_export_tree_button = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Model: export_tree_button_model,
            Renderer: export_tree_button_render,
            Controller: export_tree_button_controller,
        })
    });

    view_registry.add("tcms_export_tree_button", tcms_export_tree_button);

    return tcms_export_tree_button;
});
