odoo.define('funenc_config_form', function (require) {
    "use strict";

    var FormView = require('web.FormView');
    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var view_registry = require('web.view_registry');
    var core = require("core.web")
    var qweb = core.qweb

    /**
     * 重写，表单没有取消按扭
     */
    var funenc_config_form_controller = FormController.extend({
        config_form_buttons: "funenc.config_buttons",

        renderButtons: function ($node) {
            var $footer = this.footerToButtons ? this.$('footer') : null;
            var mustRenderFooterButtons = $footer && $footer.length;
            if (!this.defaultButtons && !mustRenderFooterButtons) {
                return;
            }
            this.$buttons = $('<div/>');
            if (mustRenderFooterButtons) {
                this.$buttons.append($footer);
    
            } else {
                this.$buttons.append(qweb.render(config_form_buttons, {widget: this}));
                this.$buttons.on('click', '.o_form_button_edit', this._onEdit.bind(this));
                this.$buttons.on('click', '.o_form_button_save', this._onSave.bind(this));
                this._assignSaveCancelKeyboardBehavior(this.$buttons.find('.o_form_buttons_edit'));
                this.$buttons.find('.o_form_buttons_edit').tooltip({
                    delay: {show: 200, hide:0},
                    title: function(){
                        return qweb.render('SaveCancelButton.tooltip');
                    },
                    trigger: 'manual',
                });
                this._updateButtons();
            }
            this.$buttons.appendTo($node);
        },
    })

    var funenc_config_form_render = FormRenderer.extend({}) 

    var funenc_config_form = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Renderer: funenc_config_form_render,
            Controller: funenc_config_form_controller
        })
    });

    view_registry.add("funenc_config_form", funenc_config_form);
    return funenc_config_form;
});