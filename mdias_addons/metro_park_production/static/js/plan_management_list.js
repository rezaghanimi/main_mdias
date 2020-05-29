odoo.define('funenc.plan_management_list_view', function (require) {
    "use strict";

    /**
     * 自定义树
     */
    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var plan_management_list_render = ListRenderer.extend({})

    var plan_management_list_controller = ListController.extend({})

    var plan_management_list_view = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: plan_management_list_render,
            Controller: plan_management_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('plan_management_list_view', plan_management_list_view);

    return plan_management_list_view;
});