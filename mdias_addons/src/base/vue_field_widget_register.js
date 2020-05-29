
export function abstractFieldRegister(widgetName, component, domainName = 'Vue') {
    odoo.define(domainName + '.' + widgetName, function (require) {
        let FieldRegistry = require("web.field_registry");
        let VueAbstractField = require('Vue.AbstractField');

        let LinePathwayField = VueAbstractField.extend({
            vue_component: component,
        }).extend(component.widget);
        FieldRegistry.add(widgetName, LinePathwayField);
    });
}



