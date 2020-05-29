odoo.define('funenc.malfunction.repair.btn', function (require) {
    'use strict';

    var ListView = require("web.ListView");
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.fnt_table_render");
    var core = require('web.core');
    var ListController = require('funenc.fnt_table_controller');
    var qweb = core.qweb;
    var maintaince_order_render = ListRenderer.extend({});

    var maintaince_order_Controller = ListController.extend({
        buttons_template: 'malfunction_repair_tree_template',
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
                this.$buttons.on('click', '.test_send', this._test_send.bind(this));
                this.$buttons.on('click', '.test_result', this._test_result.bind(this));
                this.$buttons.appendTo($node);
            }
        },
        _test_send: function () {
            var self = this;
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'funenc.malfunction.repair',
                method: 'test_send',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

        _test_result: function () {
            var self = this;
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'funenc.malfunction.repair',
                method: 'test_result',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

    });

    var maintaince_order_btn = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: maintaince_order_render,
            Controller: maintaince_order_Controller
        }),
        viewType: "list"
    });

    view_registry.add("malfunction_repair_tree_class", maintaince_order_btn);
});