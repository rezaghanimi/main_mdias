odoo.define("funenc.switch_button", function (require) {
    "use strict";

    var AbstractField = require("web.AbstractField");
    var registry = require("web.field_registry");
    var core = require('web.core');
    var qweb = core.qweb;

    var switch_button = AbstractField.extend({
        switch_btn: undefined,
        theme_color: "rgb(100, 189, 99)",
        showOn: function () {
            this.switch_btn.removeClass("switch_button_off").addClass("switch_button_on");
        },

        showOff: function () {
            this.switch_btn.removeClass("switch_button_on").addClass("switch_button_off");
        },

        // 由于 _render_edit 和 _render_read_only会调用这个函数
        _do_render: function () {
            var tmp = qweb.render('funenc_switch_button', {
                widget: this
            })
            this.$el.html(tmp)

            var self = this;
            this.switch_btn = this.$(".switch_button")
            if (this.mode === 'readonly') {
                this.switch_btn.addClass('switch_button_disabled')
            } else {
                this.switch_btn.removeClass('switch_button_disabled')
            }

            // 处理按扭点击事件, 没有按照odoo的写法
            this.switch_btn.click(function () {
                if ($(this).hasClass("switch_button_disabled")) {
                    return;
                }
                if ($(this).hasClass("switch_button_off")) {
                    self.showOn();
                    self._setValue(true)
                } else {
                    self.showOff();
                    self._setValue(false)
                }
            });
        },

        isSet: function () {
            return true;
        },

        _renderEdit: function () {
            this._do_render()
        },

        _renderReadonly: function () {
            this._do_render()
        },

        getValue: function () {
            if ($(this).hasClass('switch_button_on')) {
                return true;
            } else {
                return false;
            }
        }
    });

    registry.add("switch_button", switch_button);

    return { switch_button: switch_button };
});
