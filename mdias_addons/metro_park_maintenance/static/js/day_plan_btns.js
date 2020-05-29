odoo.define("funenc.day_plan_btns", function (require) {
    "use strict";

    var registry = require("web.widget_registry");
    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var filed_registry = require('web.field_registry');
    var Callback_Registry = require('funenc.callback_registry');
    var AbstractField = require('web.AbstractField');
    var config = require('web.config')
    var templateWidget = require('funenc.template_widget')

    var qweb = core.qweb;

    var day_plan_btns = templateWidget.extend({
        _button_clicked: function (event) {   
            var self = this
            var call_back = $(event.currentTarget).attr("call_back")
            // 取得回调函数, 绑定的this为当前对象
            if (call_back) {
                call_back = Callback_Registry.get(call_back)
            }
            var confirm = $(event.currentTarget).attr("confirm")
            if (confirm) {
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
    });

    filed_registry.add("day_plan_btns", day_plan_btns);
    return day_plan_btns
});

