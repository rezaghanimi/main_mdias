odoo.define('funenc.x2manyExtend', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var view_registry = require('web.view_registry');
    var ListController = require('web.ListController');
    var KanbanRenderer = require('web.KanbanRenderer');
    var ListRenderer = require('web.ListRenderer');

    /**
     * 重写，目的是为了使用注册的renderer
     */
    relational_fields.FieldOne2Many.include({
        _getRenderer: function () {
            if (this.view.arch.tag === 'tree') {
                if (this.view.arch.attrs.js_class) {
                    var key = this.view.arch.attrs.js_class
                    var View = view_registry.get(key || 'tree');
                    var renderer = View.prototype.config.Renderer;
                    return renderer;
                }
                return ListRenderer;
            }
            // 暂进没有处理kanban
            if (this.view.arch.tag === 'kanban') {
                return KanbanRenderer;
            }
        }
    });

    relational_fields.FieldMany2Many.include({
        _getRenderer: function () {
            if (this.view.arch.tag === 'tree') {
                if (this.view.arch.attrs.js_class) {
                    var key = this.view.arch.attrs.js_class
                    var View = view_registry.get(key || 'tree');
                    var renderer = View.prototype.config.Renderer;
                    return renderer;
                }
                return ListRenderer;
            }
            // 暂进没有处理kanban
            if (this.view.arch.tag === 'kanban') {
                return KanbanRenderer;
            }
        }
    });

    /**
     * 扩展many2one
     */
    relational_fields.FieldMany2Many.include({
        _getRenderer: function () {
            if (this.view.arch.tag === 'tree') {
                if (this.view.arch.attrs.js_class) {
                    var key = this.view.arch.attrs.js_class
                    var View = view_registry.get(key || 'tree');
                    var renderer = View.prototype.config.Renderer;
                    return renderer;
                }
                return ListRenderer;
            }
            // 暂进没有处理kanban
            if (this.view.arch.tag === 'kanban') {
                return KanbanRenderer;
            }
        }
    });
});