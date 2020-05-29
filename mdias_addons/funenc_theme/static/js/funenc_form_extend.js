odoo.define('funenc.FormRenderer', function (require) {
    "use strict";

    var FormRenderer = require('web.FormRenderer');
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');

    var _t = core._t;
    var qweb = core.qweb;

    FormRenderer.include({
        /**
         * 事件
         */
        events: _.extend({}, FormRenderer.prototype.events, {
            'click .o_form_label': '_onClickLable',
        }),

        /**
         * 点击标签
         */
        _onClickLable: function (event) {
            // event.stopPropagation();
            // var target = event.currentTarget;
            // var for_attr = $(target).attr('for');
            // // 如果是radio选择或者是many2many字段则允许
            // return $(target).parent().hasClass('o_radio_item') || _.str.startsWith(for_attr, 'o_many2many_')
        },

        /**
         * 扩展，标签出错的时候进行打印
         */
        _renderTagLabel: function (node) {
            var self = this;
            var text;
            var fieldName = node.tag === 'label' ? node.attrs.for : node.attrs.name;
            if ('string' in node.attrs) { // allow empty string
                text = node.attrs.string;
            } else if (fieldName) {
                try {
                    text = this.state.fields[fieldName].string;
                } catch (error) {
                    console.log('fieldName')
                }
            } else {
                return this._renderGenericTag(node);
            }
            var $result = $('<label>', {
                class: 'o_form_label',
                // 去除标签绑定
                //for: this._getIDForLabel(fieldName),
                text: text,
            });
            if (node.tag === 'label') {
                this._handleAttributes($result, node);
            }
            var modifiersOptions;
            if (fieldName) {
                modifiersOptions = {
                    callback: function (element, modifiers, record) {
                        var widgets = self.allFieldWidgets[record.id];
                        var widget = _.findWhere(widgets, {name: fieldName});
                        if (!widget) {
                            return; // FIXME this occurs if the widget is created
                                    // after the label (explicit <label/> tag in the
                                    // arch), so this won't work on first rendering
                                    // only on reevaluation
                        }
                        element.$el.toggleClass('o_form_label_empty', !!( // FIXME condition is evaluated twice (label AND widget...)
                            record.data.id
                            && (modifiers.readonly || self.mode === 'readonly')
                            && !widget.isSet()
                        ));
                    },
                };
            }
            // FIXME if the function is called with a <label/> node, the registered
            // modifiers will be those on this node. Maybe the desired behavior
            // would be to merge them with associated field node if any... note:
            // this worked in 10.0 for "o_form_label_empty" reevaluation but not for
            // "o_invisible_modifier" reevaluation on labels...
            this._registerModifiers(node, this.state, $result, modifiersOptions);
            return $result;
        },
    })
})