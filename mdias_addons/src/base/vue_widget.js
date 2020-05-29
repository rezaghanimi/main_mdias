
odoo.define('Vue.Widget', function (require) {
    "use strict";
    let Widget = require('web.Widget');
    let VueWidget = Widget.extend({
        init: function (parent, action) {
            this._super(parent, action);
        },
    });
    return VueWidget
});

