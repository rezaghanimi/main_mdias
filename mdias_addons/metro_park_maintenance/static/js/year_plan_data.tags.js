odoo.define('funenc.plan_data_tags', function (require) {
    "use strict";

    var core = require('web.core');
    var ListRenderer = require('web.ListRenderer');
    var qweb = core.qweb
    var config = require('web.config');
    var core = require('web.core');
    var dom = require('web.dom');
    var field_utils = require('web.field_utils');
    var pyUtils = require('web.py_utils');
    var FunencPager = require('funenc.pager');

    var _lt = core._lt;
    var _t = core._t;

    var FieldMany2ManyTags = AbstractField.extend({
        tag_template: "FieldMany2ManyTag",
        className: "o_field_many2manytags",
        supportedFieldTypes: ['many2many'],
        custom_events: _.extend({}, AbstractField.prototype.custom_events, {
            field_changed: '_onFieldChanged',
        }),
        events: _.extend({}, AbstractField.prototype.events, {
            'click .o_delete': '_onDeleteTag',
        }),
        fieldsToFetch: {
            display_name: { type: 'char' },
        },

        /**
         * @constructor
         */
        init: function () {
            this._super.apply(this, arguments);

            if (this.mode === 'edit') {
                this.className += ' o_input';
            }

            this.colorField = this.nodeOptions.color_field;
        },

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * @override
         */
        activate: function () {
            return this.many2one ? this.many2one.activate() : false;
        },
        /**
         * @override
         * @returns {jQuery}
         */
        getFocusableElement: function () {
            return this.many2one ? this.many2one.getFocusableElement() : $();
        },
        /**
         * @override
         * @returns {boolean}
         */
        isSet: function () {
            return !!this.value && this.value.count;
        },
        /**
         * Reset the focus on this field if it was the origin of the onchange call.
         *
         * @override
         */
        reset: function (record, event) {
            this._super.apply(this, arguments);
            if (event && event.target === this) {
                this.activate();
            }
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {any} data
         */
        _addTag: function (data) {
            if (!_.contains(this.value.res_ids, data.id)) {
                this._setValue({
                    operation: 'ADD_M2M',
                    ids: data
                });
            }
        },
        /**
         * Get the QWeb rendering context used by the tag template; this computation
         * is placed in a separate function for other tags to override it.
         *
         * @private
         * @returns {Object}
         */
        _getRenderTagsContext: function () {
            var elements = this.value ? _.pluck(this.value.data, 'data') : [];
            return {
                colorField: this.colorField,
                elements: elements,
                readonly: this.mode === "readonly",
            };
        },
        /**
         * @private
         * @param {any} id
         */
        _removeTag: function (id) {
            var record = _.findWhere(this.value.data, { res_id: id });
            this._setValue({
                operation: 'FORGET',
                ids: [record.id],
            });
        },
        /**
         * @private
         */
        _renderEdit: function () {
            var self = this;
            this._renderTags();
            if (this.many2one) {
                this.many2one.destroy();
            }
            this.many2one = new FieldMany2One(this, this.name, this.record, {
                mode: 'edit',
                noOpen: true,
                viewType: this.viewType,
                attrs: this.attrs,
            });
            // to prevent the M2O to take the value of the M2M
            this.many2one.value = false;
            // to prevent the M2O to take the relational values of the M2M
            this.many2one.m2o_value = '';

            this.many2one._getSearchBlacklist = function () {
                return self.value.res_ids;
            };
            return this.many2one.appendTo(this.$el);
        },
        /**
         * @private
         */
        _renderReadonly: function () {
            this._renderTags();
        },
        /**
         * @private
         */
        _renderTags: function () {
            this.$el.html(qweb.render(this.tag_template, this._getRenderTagsContext()));
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} event
         */
        _onDeleteTag: function (event) {
            event.preventDefault();
            event.stopPropagation();
            this._removeTag($(event.target).parent().data('id'));
        },
        /**
         * Controls the changes made in the internal m2o field.
         *
         * @private
         * @param {OdooEvent} ev
         */
        _onFieldChanged: function (ev) {
            if (ev.target !== this.many2one) {
                return;
            }
            ev.stopPropagation();
            var newValue = ev.data.changes[this.name];
            if (newValue) {
                this._addTag(newValue);
                this.many2one.reinitialize(false);
            }
        },
        /**
         * @private
         * @param {KeyboardEvent} ev
         */
        _onKeydown: function (ev) {
            if (ev.which === $.ui.keyCode.BACKSPACE && this.$('input').val() === "") {
                var $badges = this.$('.badge');
                if ($badges.length) {
                    this._removeTag($badges.last().data('id'));
                    return;
                }
            }
            this._super.apply(this, arguments);
        },
        /**
         * @private
         * @param {OdooEvent} event
         */
        _onQuickCreate: function (event) {
            this._quickCreate(event.data.value);
        },
    });
})