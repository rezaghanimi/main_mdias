odoo.define('funenc.month_miles_list_view', function (require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb;

    var month_miles_list_render = ListRenderer.extend({})

    var month_miles_list_controller = ListController.extend({
        buttons_template: 'history_miles_set_btn',

        events: _.extend({}, ListController.prototype.events, {
            'click .btn_miles_set_rule': '_set_year_miles'
        }),

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.id = params.initialState.context.id;
            this.params = params;
            this.model_base = params.modelName;
        },

        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, {
                    widget: this,
                }));
                this.$buttons.appendTo($node);
            }
        },
        
        _set_year_miles: function () {
            var self = this;
            self._rpc({
                model: 'metro_park_maintenance.history_miles',
                method: 'set_year_miles',
            }).then(function (res) {
                self.do_action(res, {
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        }
    });


    var month_miles_list_view = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: month_miles_list_render,
            Controller: month_miles_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('month_miles_list_view', month_miles_list_view);

    return month_miles_list_view;
});