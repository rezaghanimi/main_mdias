odoo.define('metro_park_dispatch.construction', function (require) {
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
    var import_tree_button_controller = ListController.extend({

        buttons_template: 'construction.import_tree_button',
        renderButtons: function ($node) {
            this.par = this.searchView.action.par
            this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
            this.$buttons.find('[name="model_import"]').on('click', this.model_import.bind(this))
            this.$buttons.appendTo($node);
        },

        model_import: function (data) {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'import_data_rec',
            }).then(function (data) {
                self.do_action(data, {
                    on_close: self.trigger_up.bind(self, 'reload'),
                })
            })
        },
    })


    // 重写，自定义搜索
    var import_tree_button_model = BasicModel.extend({})

    // 重写，渲染列表视图
    var import_tree_button_render = ListRenderer.extend({})

    // 扩展、重新配置list
    var construction_import_tree_button = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Model: import_tree_button_model,
            Renderer: import_tree_button_render,
            Controller: import_tree_button_controller,
        })
    });

    view_registry.add("construction_import_tree_button", construction_import_tree_button);

    return construction_import_tree_button;
});
