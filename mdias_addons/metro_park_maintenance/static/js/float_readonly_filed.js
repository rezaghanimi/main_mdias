odoo.define('funenc.float_readonly_filed', function (require) {
    "use strict";
    var BasicFields = require('web.basic_fields');

    var ExtendFloatField = BasicFields.FieldFloat.extend({
        init: function () {
            this._super().apply(arguments)
        }
    })


});
