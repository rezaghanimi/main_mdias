odoo.define('funenc.fnt_tree_grid', function (require) {
    "use strict";

    /**
     * tree grid
     */
    var BasicView = require('web.BasicView');
    var fnt_tree_grid_render = require('funenc.fnt_tree_grid_render');
    var fnt_tree_grid_controller = require('funenc.fnt_tree_grid_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    
    var fnt_tree_grid = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: fnt_tree_grid_render,
            Controller: fnt_tree_grid_controller
        }),
        viewType: 'list'
    });

    view_registry.add('fnt_tree_grid', fnt_tree_grid);
    
    return fnt_tree_grid;
});
