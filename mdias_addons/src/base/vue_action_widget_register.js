export function actionRegister(widgetName, component, domainName = 'Vue') {
    odoo.define(domainName + '.' + widgetName, function (require) {
        let core = require('web.core');
        let VueCom = require('Vue.ComWidget');

        let Widget = VueCom.extend({
            vue_component: component,
        }).extend(component.widget);
        core.action_registry.add(widgetName, Widget);
    });
}



