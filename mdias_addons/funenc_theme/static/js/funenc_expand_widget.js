odoo.define('funenc.expand_widget', function (require) {
  "use strict";

  /**
   * 展开箭头
   */
  var Widget = require('web.Widget');
  var widgetRegistry = require('web.widget_registry');

  var expand_widget = Widget.extend({
    template: 'funenc.expand_widget',
    is_reverse: true,
    
    events: {
      'click': '_onArrowClick'
    },

    /**
     * 初始化
     * @param {*} parent 
     * @param {*} options 
     */
    init: function (parent, options) {
      this._super.apply(this, arguments);
      this.is_reverse = options.is_reverse || true
    },

    /**
     *  开始
     */
    start: function () {
      this._super.apply(this, arguments)
      this.$el.prop('special_click', true)
      this.$("*").prop('special_click', true)
    },

    /**
     *  箭头点击
     */
    _onArrowClick: function (event) {
      if (this.is_reverse) {
        this.$('.o_dropdown_arrow ').removeClass("is-reverse");
        this.is_reverse = false;
      } else {
        this.$('.o_dropdown_arrow ').addClass("is-reverse")
        this.is_reverse = true;
      }
      this.trigger_up('arrow_direct_changed', { is_reverse: this.is_reverse });
    }
  });

  widgetRegistry.add('expand_widget', expand_widget);

  return expand_widget;
});
