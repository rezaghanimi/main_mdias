odoo.define('funenc.fnt_tree_grid_render', function (require) {
    "use strict";

    /**
     * render for fnt_table, 说明，由于特殊原因，对jquery tree grid 进行了修改
     */
    var ListRenderer = require('funenc.fnt_table_render');
    var pyUtils = require('web.py_utils');

    var fnt_tree_grid_render = ListRenderer.extend({
        tree_grid: undefined,
        treeColumn:  0,

        init: function() {
            this._super.apply(this, arguments)
            if (this.arch.attrs.options) {
                this.treeColumn = pyUtils.py_eval(this.arch.attrs.options.treeColumn || '0')
            }
        },

        _renderView: function () {
            var def = this._super();
            this.tree_grid = this.$('.layui-table-body .layui-table').treegrid({
                treeColumn: this.treeColumn
            });
            // 更改默认行为, 禁止点击的时候跳转record
            this.$('.treegrid-expander').prop('special_click', true)
            return def;
        },

        _renderRow: function (record, index) {
            var $row = this._super.apply(this, arguments);
            var class_str = null;
            if (record.data.parent_id) {
                // 这个类只能渲染在前面
                class_str = "treegrid-" + record.data.id;
                class_str += " treegrid-parent-" + record.data.parent_id.data.id;
            } else {
                class_str = "treegrid-" + record.data.id;
            }
            $row.addClass(class_str)
            return $row;
        }
    });

    return fnt_tree_grid_render;
});
