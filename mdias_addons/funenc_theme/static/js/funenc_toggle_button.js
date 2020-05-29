odoo.define('layui_theme_toggle_button', function(require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');
    
    var ToggleButton = basic_fields.BooleanToggle.extend({
        _render: function () {
            var $checkbox = dom.renderCheckbox({
                prop: {
                    checked: this.value,
                    disabled: true,
                },
            });
            this.$input = $checkbox.find('input');
            this._renderToggleSwitch();
        },
    });

    registry.add('lay_toggle_button', ToggleButton)

    return ToggleButton;
});