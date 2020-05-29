import { VueMixin } from './VueMixin'

odoo.define('Vue.ComWidgetRegister' ,function (require) {
    let Widget = require('web.Widget');
    return Widget.extend(VueMixin, {
        init: function () {
            this._super.apply(this, arguments);
            this.$args = arguments;
        },
        start: function ($require) {
            this._super();
            this._bind_vue(this.$el, this, $require);
        },
    });
});