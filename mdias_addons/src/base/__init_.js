
if (window.load_vue_widget === undefined) {
    require('./vue_widget');
    require('./vue_abstract_field');
    require('./vue_com_widget');
    require('./vue_com_widget_registry');
    window.load_vue_widget  = true;
}

import {actionRegister} from './vue_action_widget_register'
import {abstractFieldRegister} from './vue_field_widget_register'
import {widgetRegister} from './vue_widget_register'

export const vueWidgetRegister = {
    'actionRegister': actionRegister,
    'fieldRegister': abstractFieldRegister,
    'widgetRegister': widgetRegister
};