odoo.define('funenc.Dialog', function (require) {
    "use strict";

    var dialog = require('web.Dialog');
    var core = require('web.core');
    var SelectCreateDialog = require('web.view_dialogs').SelectCreateDialog;
    var _t = core._t;

    dialog.include({
        xmlDependencies: ['/funenc_theme/static/xml/dialog.xml'],

        willStart: function () {
            this.title = this.title === _t('Odoo') ? 'Funenc' : this.title;
            return this._super()
        },

        get_max_z_index: function () {
            var modals = $(document.body).children('div.modal-backdrop');
            // many2one等下拉选择是1051，所以只能用小于1051的数字
            if (modals.length === 0) {
                return 1001
            } else {
                var max_z_index_madal = _.max(modals, function (el) {
                    return $(el).css('z-index')
                });
                return parseInt($(max_z_index_madal).css('z-index')) + 1
            }
        },

        open: function (options) {
            $('.tooltip').remove(); 
            // remove open tooltip if any to prevent them staying when modal is opened
            // 获取当前modal的最高z-index，然后+1
            var max_z_index = this.get_max_z_index();
            var self = this;
            this.appendTo($('<div/>')).then(function () {
                self.$modal.find(".modal-body").replaceWith(self.$el);
                self.$modal.attr('open', true);
                self.$modal.removeAttr("aria-hidden");
                self.$modal.modal('show');
                // 添加z-index
                self.$modal.css('z-index', max_z_index);
                self.$modal.prev().css('z-index', max_z_index);
                self._opened.resolve();
                if (options && options.shouldFocusButtons) {
                    self._onFocusControlButton();
                }
            });
            return self;
        },
    });

    SelectCreateDialog.include({
        set_buttons: function (buttons) {
            if (this.$el && this.$('.noOpen').length > 0) {
                this.$('.noOpen').removeClass('noOpen')
            }
            this._super(buttons);
        }
    })
});
