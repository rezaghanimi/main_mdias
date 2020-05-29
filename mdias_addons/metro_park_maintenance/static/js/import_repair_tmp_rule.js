odoo.define('metro_park_dispatch.import_repair_tmp_rule', function (require) {
    "use strict";

    var BasicView = require('web.BasicView');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView')
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.fnt_table_render")
    var BasicModel = require('web.BasicModel');
    var core = require("web.core")
    var qweb = core.qweb
    var Dialog = require('web.Dialog');

    // 控制器
    var import_tree_button_controller = ListController.extend({

        buttons_template: 'metro_park_maintenance.import_data_repair_tmp_rule_button',
        renderButtons: function ($node) {
            this.par = this.searchView.action.par
            this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
            this.$buttons.find('[name="import_data_repair_tmp_rule"]').on('click', this.import_data_repair_tmp_rule.bind(this))
            this.$buttons.find('[name="export_data_repair_tmp_rule"]').on('click', this.export_data_repair_tmp_rule.bind(this))
            this.$buttons.find('[name="manual_sync"]').on('click', this.manual_sync.bind(this))
            this.$buttons.find('[name="create_data_rec"]').on('click', this.create_data_rec.bind(this))
            this.$buttons.appendTo($node);
        },

        manual_sync: function () {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'manual_sync',
            }).then(function (data) {
                if (data == 'fail') {
                    new Dialog(this, {
                        size: 'medium',
                        title: '警告',
                        $content: '<div>和PMS通信失败，请查看配置或者联系管理员</div>'
                    }).open({shouldFocusButtons: true});
                } else {
                    self.reload();
                }
            })
        },

        import_data_repair_tmp_rule: function (data) {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'import_data_repair_tmp_rule',
            }).then(function (data) {
                self.do_action(data, {
                    on_close: function (res) {
                        self.reload();
                    }
                })
            })
        },

        export_data_repair_tmp_rule: function (data) {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'export_data_repair_tmp_rule',
            }).then(function (data) {
                self.do_action(data, {
                    on_close: function (res) {
                        self.reload();
                    }
                })
            })
        },
        create_data_rec: function (data) {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'create_data_rec',
            }).then(function (data) {
                self.do_action(data, {
                    on_close: function (res) {
                        self.reload();
                    }
                })
            })
        },
    })


    // 重写，自定义搜索
    var import_tree_button_model = BasicModel.extend({})

    // 重写，渲染列表视图
    var import_tree_button_render = ListRenderer.extend({})

    // 扩展、重新配置list
    var import_repair_tmp_rule = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Model: import_tree_button_model,
            Renderer: import_tree_button_render,
            Controller: import_tree_button_controller,
        })
    });

    view_registry.add("import_repair_tmp_rule", import_repair_tmp_rule);

    return import_repair_tmp_rule;
});
