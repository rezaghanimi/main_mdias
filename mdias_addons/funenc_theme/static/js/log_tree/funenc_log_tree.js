odoo.define('funenc.log_tree', function (require) {
    "use strict";

    /**
     * log tree 带了一个日志记录的tree
     */
    var BasicView = require('web.BasicView');
    var log_tree_render = require('funenc.log_tree_render');
    var log_tree_controller = require('funenc.log_tree_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    
    var log_tree = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: log_tree_render,
            Controller: log_tree_controller
        }),
        viewType: 'list'
    });

    view_registry.add('log_tree', log_tree);
    
    return log_tree;
});
