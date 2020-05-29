odoo.define("funenc.template_widget", function (require) {
  "use strict";
  var registry = require("web.widget_registry");
  var Dialog = require('web.Dialog');
  var core = require('web.core');
  var filed_registry = require('web.field_registry');
  var Callback_Registry = require('funenc.callback_registry');
  var AbstractField = require('web.AbstractField');
  var config = require('web.config')

  var qweb = core.qweb;

  var template_widget = AbstractField.extend({

    events: _.extend({}, AbstractField.prototype.events, {
      'click .o_menu_item': '_onItemClick',
    }),

    init: function (parent, name, record, options) {
      this._super.apply(this, arguments);
      this.template = this.nodeOptions.template;
      if (!this.template) {
        console.log(
          "the template for template widget is undfined, please set the template attrs"
        );
      }
    },

    trigger_button: function (e) {
      e.stopPropagation();
      e.preventDefault();
      var self = this;
      var controller = this.getParent().getParent();

      if (controller._callButtonAction) {
        var param = {
          type: $(e.currentTarget).attr("type"),
          name: $(e.currentTarget).attr("name")
        };
        if ($(e.currentTarget).attr("context")) {
          param.context = JSON.parse($(e.currentTarget).attr("context"));
        }
        controller._callButtonAction(param, this.record).then(function (rst) {
          if (!rst) {
            self.trigger_up("reload");
          } else if (rst.reload_domain) {
            // 让列表重新加载而不是当前这条数据重新加载
            controller.reload({ "domain": rst.reload_domain })
          }
        });
      } else {
        // form 表单应当为record一类
        self.trigger_up("button_clicked", {
          attrs: {
            type: $(e.currentTarget).attr("type"),
            name: $(e.currentTarget).attr("name")
          },
          record: this.record
        });
      }
    },

    start: function () {
      this._super();
      this.$("button").on("click", this._button_clicked.bind(this))
    },

    _button_clicked: function (event) {
      var self = this
      var call_back = $(event.currentTarget).attr("call_back")
      // 取得回调函数, 绑定的this为当前对象
      if (call_back) {
        call_back = Callback_Registry.get(call_back)
      }
      var confirm = $(event.currentTarget).attr("confirm")
      if (confirm) {
        event.stopPropagation();
        Dialog.confirm(this, confirm, {
          confirm_callback: function () {
            if (call_back) {
              call_back.apply(this)
            } else {
              self.trigger_button(event)
            }
            this.destroy()
          }
        });
      } else {
        if (call_back) {
          call_back.apply(this)
        } else {
          self.trigger_button(event)
        }
      }
    },

    /**
     * 这个函数
     */
    isSet: function () {
      return true
    },

    _render: function () {
      var $el = undefined;
      if (this.nodeOptions.template) {
        $el = $(qweb.render(this.nodeOptions.template, { widget: this, debug: config.debug }));
      } else {
        $el = this._super.apply(this)
      }
      this._replaceElement($el);
      this.$('.dropdown-toggle').dropdown()
    },

    /**
     * 防止内部
     */
    _onItemClick: function (event) {
      event.preventDefault();
      event.stopPropagation();
    },
  });

  filed_registry.add("template_widget", template_widget);
  return template_widget
});
