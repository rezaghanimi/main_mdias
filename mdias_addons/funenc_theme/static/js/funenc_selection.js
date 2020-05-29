odoo.define('funenc.selection_extend', function (require) {
    "use strict";

    var Fields = require("web.relational_fields")

    Fields.FieldSelection.include({
        template: 'funenc.selection',

        _renderEdit: function () {
            this.$el.empty();
            for (var i = 0 ; i < this.values.length ; i++) {
                this.$el.append($('<option/>', {
                    value: JSON.stringify(this.values[i][0]),
                    text: this.values[i][1]
                }));
            }
            var value = this.value;
            if (this.field.type === 'many2one' && value) {
                value = value.data.id;
            }
            this.$el.val(JSON.stringify(value));
            var self = this
            setTimeout(() => {
                if (self.mode === 'edit') {
                    if (self.attrs.placeholder) {
                        self.$el.select2({
                            id: false,
                            text: this.attrs.placeholder
                        });
                    } else {
                        self.$el.select2();
                    }
                }
            }, 0);
        },
    });
});