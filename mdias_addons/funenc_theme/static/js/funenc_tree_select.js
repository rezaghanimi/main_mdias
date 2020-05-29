/**
 * jquery 多级部门列表
 */
odoo.define("funenc.department_field", function (require) {
  "use strict";

  var department_field = FieldMany2One.extend({
    supportedFieldTypes: ['many2one'],
    template: 'FieldMany2One',
    custom_events: _.extend({}, FieldMany2One.prototype.custom_events, {
      'field_changed': '_onFieldChanged',
    }),
    events: _.extend({}, FieldMany2One.prototype.events, {
      'click input': '_onInputClick',
    }),

    start: function () {
      this.floating = false;
      this.$input = this.$('input');
      return this._super.apply(this, arguments);
    },

    getFocusableElement: function () {
      return this.mode === 'edit' && this.$input || this.$el;
    },

    reinitialize: function (value) {
      this.isDirty = false;
      this.floating = false;
      return this._setValue(value);
    },

    reset: function (record, event) {
      this._reset(record, event);
      if (!event || event === this.lastChangeEvent) {
        this.isDirty = false;
      }
      if (this.isDirty) {
        return $.when();
      } else {
        return this._render();
      }
    },

    _getSearchBlacklist: function () {
      return [];
    },

    _getDisplayName: function (value) {
      return value.split('\n')[0];
    },

    _onFieldChanged: function (event) {
      this.lastChangeEvent = event;
    },

    _renderEdit: function () {
      var value = this.m2o_value;
      if (this.nodeOptions.always_reload) {
        value = this._getDisplayName(value);
      }
      this.$input.val(value);
      if (!this.autocomplete_bound) {
        this._bindAutoComplete();
      }
    },

    _renderReadonly: function () {
      var value = _.escape((this.m2o_value || "").trim()).split("\n").join("<br/>");
      this.$el.html(value);
      if (!this.noOpen && this.value) {
        this.$el.attr('href', _.str.sprintf('#id=%s&model=%s', this.value.res_id, this.field.relation));
        this.$el.addClass('o_form_uri');
      }
    },

    /**
     * @private
     */
    _reset: function () {
      this._super.apply(this, arguments);
      this.floating = false;
      this.m2o_value = this._formatValue(this.value);
    },

    _onClick: function (event) {
      var self = this;
      if (this.mode === 'readonly' && !this.noOpen) {
        event.preventDefault();
        event.stopPropagation();
        this._rpc({
          model: this.field.relation,
          method: 'get_formview_action',
          args: [[this.value.res_id]],
          context: this.record.getContext(this.recordParams),
        })
          .then(function (action) {
            self.trigger_up('do_action', { action: action });
          });
      }
    },

    _onInputClick: function () {

    }
  });

  return department_field;
});
