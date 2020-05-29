/**
 * 调车详情列表，保存前需要排下序号
 */
odoo.define('metro_park_dispatch.dispatchs_detail_table', function(require) {
    "use strict";

    var core = require('web.core')
    var ListRenderer = require('web.ListRenderer');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var BasicModel = require('web.BasicModel');
    var view_registry = require('web.view_registry');

    var list_model = BasicModel.extend({
        /**
         * 重写sequence默认给一个值
         * @param {*} modelName 
         * @param {*} params 
         */
        init: function(viewInfo, params) {
            this._super.apply(this, arguments);
            this.model = params.model;
        }
    })

    var list_render = ListRenderer.extend({

    })

    var list_controller = ListController.extend({
        init: function(parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },

        _addRecord: function() {
            var self = this;
            this._disableButtons();
            return this.renderer.unselectRow().then(function() {
                return self.model.addDefaultRecord(self.handle, {
                    position: self.editable,
                });
            }).then(function(recordID) {
                var state = self.model.get(self.handle);
                self.renderer.updateState(state, {});
                self.renderer.editRecord(recordID);
                self._updatePager();
            }).always(this._enableButtons.bind(this));
        },
    })

    var dispatch_detail_table = ListView.extend({
        config: {
            Model: list_model,
            Renderer: list_render,
            Controller: list_controller
        },
        viewType: 'list'
    });

    view_registry.add('dispatch_detail_table', dispatch_detail_table);

    return dispatch_detail_table;
});