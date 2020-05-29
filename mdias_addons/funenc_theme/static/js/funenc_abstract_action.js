odoo.define('funenc.AbstractAction', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var AbstractAction = require('web.AbstractAction');

    /**
     * 扩展
     */
    AbstractAction.include({
        template: 'funenc_abstract_action',
        btn_box: undefined,

        start: function () {
            this._super.apply(this, arguments);
            this._render_buttons();
        },

        /**
         * 渲染按钮
         */
        _render_buttons: function () {
            this.renderButtons()
            this._update_buttons();
        },

        _update_buttons: function () {

        }
    });

    return AbstractAction;
});
