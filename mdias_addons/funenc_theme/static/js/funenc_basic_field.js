odoo.define('funenc.basic_fields', function (require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var InputField = basic_fields.InputField
    var FieldText = basic_fields.FieldText

    /**
     * 扩展,增加在没输入值的时候显示无
     */
    InputField.include({
        /**
         * Resets the content to the formated value in readonly mode.
         *
         * @override
         * @private
         */
        _renderReadonly: function () {
            var txt = this._formatValue(this.value);
            if (!txt || txt == '') {
                txt = this.nodeOptions.place_holder || '无'
            }
            this.$el.text(txt);
        },
    })

    /**
     * 文本框
     */
    FieldText.include({
        start: function () {
            if (this.mode === 'edit') {
                this.$el.css("height", "100%")
                this.$el = this.$el.add(this._renderTranslateButton());
            }
            return InputField.prototype.start.apply(this, arguments);
        }
    })

})