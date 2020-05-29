odoo.define('funenc.log_tree_render', function (require) {
    "use strict";

    /**
     * render for fnt_table
     */

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');

    var _lt = core._lt;

    var log_tree_render = ListRenderer.extend({
        tree_grid: undefined,
        /**
         * 渲染视图
         */
        _renderView: function () {
            var self = this;
            var def = this._super();
            this.tree_grid = this.$('.o_list_view').treegrid({
                treeColumn: 1
            });
            // 禁止点击的时候跳转record
            this.$('.treegrid-expander').prop('special_click', true)
            this.$("tr").attr("style", "")
            return def;
        },

        /**
         * 重写, 添加层级关系
         * @param {*} record 
         */
        _renderRow: function (record) {
            var self = this;
            this.defs = [];
            var $cells = _.map(this.columns, function (node, index) {
                return self._renderBodyCell(record, node, index, { mode: 'readonly' });
            });
            delete this.defs;

            // 构造tree_grid
            var class_str = 'o_data_row';
            class_str += " treegrid-" + record.data.id;
            if (record.data.parent_id) {
                class_str += " treegrid-parent-" + record.data.parent_id.data.id;
            }

            var $tr = $('<tr/>', { class: class_str })
                .data('id', record.id)
                .append($cells);
            if (this.hasSelectors) {
                $tr.prepend(this._renderSelector('td', !record.res_id));
            }
            this._setDecorationClasses(record, $tr);
            return $tr;
        },
    });

    return log_tree_render;
});
