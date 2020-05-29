odoo.define('funenc.left_tree_list', function (require) {
    "use strict";

    var BasicView = require('web.BasicView');
    var core = require('web.core');
    var left_tree_render = require('funenc.left_tree_render');
    var left_tree_controller = require('funenc.left_tree_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var left_tree_list = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: left_tree_render,
            Controller: left_tree_controller
        }), 
        viewType: 'list'
    });

    view_registry.add('left_tree_list', left_tree_list)

    return left_tree_list;
});
