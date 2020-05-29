odoo.define('back_plan_form', function (require) {
    "use strict";

    /**
     * 内部有个自动关闭的机制
     */
    var FormView = require('web.FormView');
    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var view_registry = require('web.view_registry');

    var back_plan_alarm_form_controller = FormController.extend({})

    var back_plan_alarm_form_render = FormRenderer.extend({
        tip_info_btn: undefined,
        cur_left_seconds: 10,
        start: function () {
            this._super.apply(this)
            this.tip_info_btn = this.$('.accpet_btn')
            this.tip_info_btn.text('确认接车(10s)')
            var self = this
            setTimeout(function () {
                self.cur_left_seconds--;
                if (self.cur_left_seconds <= 0) {
                    self.do_action({ type: 'ir.actions.act_window_close' })
                }
                self.tip_info_btn.text('确认接车(' + self.cur_left_seconds + 's)')
            }, 10 * 1000);
        }
    })

    var back_plan_alarm_form = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Renderer: back_plan_alarm_form_render,
            Controller: back_plan_alarm_form_controller,
        })
    });

    view_registry.add("back_plan_alarm_form", back_plan_alarm_form);
    return back_plan_alarm_form;
});