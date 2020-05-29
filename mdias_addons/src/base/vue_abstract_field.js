import {VueMixin}from './VueMixin'

odoo.define('Vue.AbstractField', function (require) {
    let AbstractField = require("web.AbstractField");
    return AbstractField.extend(VueMixin, {
        start: function () {
            this._super();
            this._bind_vue(this.$el, this, require);

        }
    });
});