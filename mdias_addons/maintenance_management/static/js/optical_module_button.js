odoo.define('metro_park_dispatch.optical_module_button', function (require) {
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
    var optical_module_button_controller = ListController.extend({

        buttons_template: 'maintenance_management.optical_module_button',
        renderButtons: function ($node) {
            this.par = this.searchView.action.par
            this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
            this.$buttons.find('[name="model_temperature"]').on('click', this.model_temperature.bind(this))
            this.$buttons.find('[name="model_current"]').on('click', this.model_current.bind(this))
            this.$buttons.find('[name="model_voltage"]').on('click', this.model_voltage.bind(this))
            this.$buttons.find('[name="model_transmission_power"]').on('click', this.model_transmission_power.bind(this))
            this.$buttons.find('[name="model_receive_power"]').on('click', this.model_receive_power.bind(this))
            this.$buttons.appendTo($node);
        },

        model_temperature: function () {
            var self = this
            self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'model_temperature',
                args: [self.par]
            }).then(function (data) {
                self.do_action(data)
            })
        },
        model_current: function () {
            var self = this
            self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'model_current',
                args: [self.par]
            }).then(function (data) {
                self.do_action(data)
            })
        },
        model_voltage: function () {
            var self = this
            self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'model_voltage',
                args: [self.par]
            }).then(function (data) {
                self.do_action(data)
            })
        },
        model_transmission_power: function () {
            var self = this
            self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'model_transmission_power',
                args: [self.par]
            }).then(function (data) {
                self.do_action(data)
            })
        },
        model_receive_power: function () {
            var self = this
            self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'model_receive_power',
                args: [self.par]
            }).then(function (data) {
                self.do_action(data)
            })
        },

    })


    // 重写，自定义搜索
    var optical_module_button_model = BasicModel.extend({})

    // 重写，渲染列表视图
    var optical_module_button_render = ListRenderer.extend({})

    // 扩展、重新配置list
    var optical_module_button = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Model: optical_module_button_model,
            Renderer: optical_module_button_render,
            Controller: optical_module_button_controller,
        })
    });

    view_registry.add("optical_module_button", optical_module_button);

    return optical_module_button;
});
