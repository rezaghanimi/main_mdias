odoo.define('funenc.ListRender', function (require) {
    "use strict";

    var ListRenderer = require('web.ListRenderer');
    var config = require('web.config');

    var FunencListrenderer = ListRenderer.include({
        pager: undefined,

        /**
         *list 点击进入form当class为 noOpen
         */
        _onRowClicked: function (event) {
            var self = this;
            if ((this.arch.attrs.options && this.arch.attrs.options.disable_open_record) 
                || this.$el.hasClass("noOpen")) 
            {
                return false;
            }
            if (!$(event.target).prop("special_click")) {
                self._super(event)
            }
        },

        /**
         * 添加widget的表格头
         * @param node
         * @returns {*}
         * @private
         */
        _renderHeaderCell: function (node) {
            var name = node.attrs.name;
            var order = this.state.orderedBy;
            var isNodeSorted = order[0] && order[0].name === name;
            var field = this.state.fields[name];
            var $th = $('<th>');

            // 添加widget的string表格头
            if (node.tag === "widget" && node.attrs.string && !field) {
                return $th.text(node.attrs.string)
            } else if (!field) {
                return $th;
            }
            var description;
            if (node.attrs.widget) {
                description = this.state.fieldsInfo.list[name].Widget.prototype.description;
            }
            if (description === undefined) {
                description = node.attrs.string || field.string;
            }

            // 是否禁用sort
            var disable_sort = node.attrs.disable_sort == "1" || false
            $th.text(description)
                .data('name', name)
                .toggleClass('o-sort-down', isNodeSorted ? !order[0].asc : false)
                .toggleClass('o-sort-up', isNodeSorted ? order[0].asc : false)
                .addClass((field.sortable && !disable_sort) && 'o_column_sortable');

            if (isNodeSorted) {
                $th.attr('aria-sort', order[0].asc ? 'ascending' : 'descending');
            }

            if (field.type === 'float' || field.type === 'integer' || field.type === 'monetary') {
                $th.css({textAlign: 'right'});
            }

            if (config.debug) {
                var fieldDescr = {
                    field: field,
                    name: name,
                    string: description || name,
                    record: this.state,
                    attrs: node.attrs,
                };
                this._addFieldTooltip(fieldDescr, $th);
            }
            return $th;
        },
    });

    return FunencListrenderer;
});
