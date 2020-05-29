odoo.define('funenc.production_list_view', function (require) {
    "use strict";


    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var production_list_render = ListRenderer.extend({})

    var production_list_controller = ListController.extend({
        buttons_template: 'production.ListView.buttons',
        /**
         * 重写，添加渲染按扭
         * @param {} $node
         */
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
                this.$buttons.on('click', '.dispatch_button', this._dispatch_button.bind(this));
                this.$buttons.on('click', '.construction_button', this._construction_button.bind(this));
                this.$buttons.appendTo($node);
            }
        },

        /**
         *调度计划
         */
        _dispatch_button: function () {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'action_construction',
                args: [self.id]
            }).then(function (action) {
                self.do_action(action,
                    {
                        clear_breadcrumbs: true
                    })
            })

        },
        _construction_button: function () {
            var self = this
            self._rpc({
                model: self.modelName,
                method: 'action_scheduling',
                args: [self.id]
            }).then(function (action) {
                self.do_action(action, {clear_breadcrumbs: true})
            })
        }

    })

    var production_list_view = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: production_list_render,
            Controller: production_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('production_list_view', production_list_view);

    return production_list_view;
});