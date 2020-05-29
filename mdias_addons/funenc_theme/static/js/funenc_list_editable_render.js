odoo.define('funenc.ListEditableRender', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var config = require('web.config');
    var BasicRenderer = require('web.BasicRenderer');

    ListRenderer.include({
        /**
         * 渲染头部
         * @param {*} isGrouped 
         */
        _renderHeader: function (isGrouped) {
            var $tr = $('<tr>')
                .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
            if (this.hasSelectors) {
                $tr.prepend(this._renderSelector('th'));
            }
            if (this.addTrashIcon) {
                $tr.append($('<th>'));
            }
            return $('<thead>').append($tr);
        },

        _renderView: function () {
            var self = this;

            this.$el
                .removeClass('table-responsive')
                .empty();

            // destroy the previously instantiated pagers, if any
            _.invoke(this.pagers, 'destroy');
            this.pagers = [];

            var displayNoContentHelper = !this._hasContent() && !!this.noContentHelp;
            // display the no content helper if there is no data to display
            if (displayNoContentHelper) {
                this.$el.html(this._renderNoContentHelper());
                return this._super();
            }

            var $table = $('<table>').addClass('o_list_view table table-bordered table-hover');
            this.$el.addClass('table-responsive')
                .append($table);
            this._computeAggregates();
            $table.toggleClass('o_list_view_grouped', this.isGrouped);
            $table.toggleClass('o_list_view_ungrouped', !this.isGrouped);
            this.hasHandle = this.state.orderedBy.length === 0 ||
                this.state.orderedBy[0].name === this.handleField;
            if (this.isGrouped) {
                $table
                    .append(this._renderHeader(true))
                    .append(this._renderGroups(this.state.data))
                    .append(this._renderFooter());
            } else {
                $table
                    .append(this._renderHeader())
                    .append(this._renderBody())
                    .append(this._renderFooter());
            }
            if (this.selection.length) {
                var $checked_rows = this.$('tr').filter(function (index, el) {
                    return _.contains(self.selection, $(el).data('id'));
                });
                $checked_rows.find('.o_list_record_selector input').prop('checked', true);
            }

            return $.when();
        },
    });
});
