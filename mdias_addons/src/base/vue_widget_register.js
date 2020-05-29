export function widgetRegister(widgetName, component, depends, domainName = 'Vue') {
    let required_widget = ['web.Widget', 'web.widget_registry', 'Vue.ComWidgetRegister'];
    let deps_widget;
    if (depends instanceof Array) {
        deps_widget = depends.concat(required_widget)
    } else {
        deps_widget = required_widget;
    }
    odoo.define(domainName + '.' + widgetName, deps_widget, function (require) {
        let widget_registry = require('web.widget_registry');
        let VueComWidgetRegister = require('Vue.ComWidgetRegister');

        let Widget = VueComWidgetRegister.extend({
            vue_component: component,
            init: function () {
                this.$required = require;
                return this._super.apply(this, arguments);
            },
            start: function () {
                this._super(require);
            }
        }).extend(component.widget);
        widget_registry.add(widgetName, Widget);
    });
}