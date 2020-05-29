odoo.define('funenc.left_tree_render', function (require) {
    "use strict";

    /**
     * render for user_tree
     */
    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');
    var BasicRenderer = require('web.BasicRenderer');

    var _lt = core._lt;

    var left_tree_render = ListRenderer.extend({
        
        $left_tree: undefined,
        $tree_box: undefined,
        $table: undefined,

        /**
         * 重写渲染视图
         */
        _renderView: function () {
            console.log(this)
            if (!this.tree_box) {
                this.$tree_box = $(core.qweb.Render('FunencLeftTreeList'))
                this.$el.append(this.tree_box);
                this.$left_tree = tree_box.find(".left_tree")
                this.$right_list = tree_box.find(".right_list")
                this.$table = right_list.find("table")
                this._render_left_tree()
            }
            this._render_table();
            return BasicRenderer.prototype._renderView.apply(this);
        },

        /**
         * 取得left_tree_data 
         */
        _render_left_tree: function() {
            // this._rpc({
            //     model: "odoo_modeler.model_tables",
            //     method: "del_table",
            //     args: [this.table_info.id]
            // }).then(function (res) {
            //     // 先删除连接到自向的connection
            //     core.bus.trigger('funec_modeler_remove_dest_table_con', {
            //         table_id: self.table_info.id
            //     });
            //     self.destroy()
            // })
        },

        _render_table: function() {
            this.$table.removeClass('table-responsive').empty();

            // destroy the previously instantiated pagers, if any
            _.invoke(this.pagers, 'destroy');
            this.pagers = [];

            var displayNoContentHelper = !this._hasContent() && !!this.noContentHelp;
            // display the no content helper if there is no data to display
            if (displayNoContentHelper) {
                this.right_list.html(this._renderNoContentHelper());
                return BasicRenderer.prototype._renderView.apply(this);
            }

            // 这里后面添个属性来控制
            this._computeAggregates();
            this.$table.toggleClass('o_list_view_grouped', this.isGrouped);
            this.$table.toggleClass('o_list_view_ungrouped', !this.isGrouped);
            this.hasHandle = this.state.orderedBy.length === 0 ||
                this.state.orderedBy[0].name === this.handleField;
            if (this.isGrouped) {
                this.$table
                    .append(this._renderHeader(true))
                    .append(this._renderGroups(this.state.data))
            } else {
                this.$table
                    .append(this._renderHeader())
                    .append(this._renderBody())
            }
            if (this.selection.length) {
                var $checked_rows = $table.find('tr').filter(function (index, el) {
                    return _.contains(self.selection, $(el).data('id'));
                });
                $checked_rows.find('.o_list_record_selector input').prop('checked', true);
            }
            this._render_pager();
        }
    });

    return left_tree_render;
});
