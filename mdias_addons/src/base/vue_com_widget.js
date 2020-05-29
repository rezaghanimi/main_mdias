import {VueMixin} from './VueMixin'

odoo.define('Vue.ComWidget', function (require) {
    let AbstractAction = require('web.AbstractAction');
    return AbstractAction.extend(VueMixin, {
        start: function () {
            this._super();
            this._bind_vue(this.$el, this, require);
        },

    });
});