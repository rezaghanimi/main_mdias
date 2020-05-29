/**
 * form controller extend, add save and exit
 */
odoo.define('funenc.FormControllerExtend', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var Dialog = require('web.Dialog');
    var core = require("web.core")
    var qweb = core.qweb

    FormController.include({
        /**
         * 重写这个函数，扩展增加save_and_exit功能，让返回时带让保存的record,
         * 这在写自写义组件的时候做表单特别有用
         * @param {*} event 
         */
        _onButtonClicked: function (event) {
            // stop the event's propagation as a form controller might have other
            // form controllers in its descendants (e.g. in a FormViewDialog)
            event.stopPropagation();

            var self = this;
            var def;

            this._disableButtons();

            function saveAndExecuteAction() {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    // we need to reget the record to make sure we have changes made
                    // by the basic model, such as the new res_id, if the record is
                    // new.
                    var record = self.model.get(event.data.record.id);
                    return self._callButtonAction(attrs, record);
                });
            }

            function SaveAndExit() {
                return self.saveRecord(self.handle, {
                    stayInEdit: true,
                }).then(function () {
                    // we need to reget the record to make sure we have changes made
                    // by the basic model, such as the new res_id, if the record is
                    // new.
                    var record = self.model.get(event.data.record.id);
                    // 返回当前的record, infos作为参数会传入到onclose里面
                    var action = { type: 'ir.actions.act_window_close', infos: record }
                    return self.do_action(action, {})
                });
            }

            var attrs = event.data.attrs;
            if (attrs.confirm) {
                var d = $.Deferred();
                Dialog.confirm(this, attrs.confirm, {
                    confirm_callback: saveAndExecuteAction,
                }).on("closed", null, function () {
                    d.resolve();
                });
                def = d.promise();
            } else if (attrs.special === 'cancel') {
                def = this._callButtonAction(attrs, event.data.record);
            } else if (attrs.special === 'save_and_exit') {
                def = SaveAndExit();
            } else if (!attrs.special || attrs.special === 'save') {
                def = saveAndExecuteAction();
            }

            //  启用按扭
            def.always(this._enableButtons.bind(this));
        },

        /**
         * 是否是通过表单弹出
         */
        is_list_popup: function() {
            var record = this.model.get(this.handle, { raw: true })
            var context = record.context
            if (context.list_pop_form) {
                return true
            }
            return false
        },

        /**
         * 如果是列表弹出则直接关掉，不要再进入编辑模式
         */
        _close_list_pop_form: function () {
            if (this.is_list_popup()) {
                var record = this.model.get(this.handle, { raw: true })
                var action = { type: 'ir.actions.act_window_close', infos: record }
                this.do_action(action, {})
            }
        },

        _onSave: function (ev) {
            ev.stopPropagation(); // Prevent x2m lines to be auto-saved
            var self = this;
            this._disableButtons();
            this.saveRecord().then(function () {
                self._close_list_pop_form();
            }).always(function () {
                self._enableButtons();
            });
        },

        _onDiscard: function () {
            this._discardChanges();
            this._close_list_pop_form()
        },

        /**
         * 重写，如果是列表弹出的话不要创建按扭
         * @param {*} $node 
         */
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
                this.$buttons.append(qweb.render("FormView.buttons", { widget: this }));
                // 隐藏创建按扭
                if (this.is_list_popup()) {
                    this.$buttons.find(".o_form_button_create").hide()
                }
                this.$buttons.on('click', '.o_form_button_edit', this._onEdit.bind(this));
                this.$buttons.on('click', '.o_form_button_create', this._onCreate.bind(this));
                this.$buttons.on('click', '.o_form_button_save', this._onSave.bind(this));
                this.$buttons.on('click', '.o_form_button_cancel', this._onDiscard.bind(this));
                this._assignSaveCancelKeyboardBehavior(this.$buttons.find('.o_form_buttons_edit'));
                this.$buttons.find('.o_form_buttons_edit').tooltip({
                    delay: { show: 200, hide: 0 },
                    title: function () {
                        return qweb.render('SaveCancelButton.tooltip');
                    },
                    trigger: 'manual',
                });
                this._updateButtons();
            }
            this.$buttons.appendTo($node);
        },
    })

    return FormController;
});
