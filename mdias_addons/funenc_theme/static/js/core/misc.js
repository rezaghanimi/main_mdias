odoo.define('funenc.framework', function (require) {
    "use strict";
    var core = require('web.core');

    function reloadController(parent, options) {
        var widgets = [];
        var action_ids = options.action_ids || [];
        if (action_ids.length > 0) {
            var update_controller_ids = [];
            _.each(parent.actions, function (action) {
                if (action_ids.indexOf(action.id) >= 0) {
                    update_controller_ids.push(action.controllerID)
                }
            });
            _.each(parent.controllers, function (controller, key) {
                if (update_controller_ids.indexOf(key) >= 0) {
                    widgets.push(controller.widget)
                }
            })
        } else {
            _.each(parent.controllers, function (controller) {
                widgets.push(controller.widget)
            });
        }
        _.each(widgets, function (widget) {
            if (widget.reload)
                widget.reload()
        });
    }

    function reloadCurrentContent(parent, action) {
        reloadController(parent, action.params)
    }

    function ReloadControllerAndClose(parent, action) {
        reloadController(parent, action.params);
        parent.do_action({
            'type': 'ir.actions.act_window_close'
        })
    }

    core.action_registry.add("ReloadController", reloadCurrentContent);
    core.action_registry.add("ReloadControllerAndClose", ReloadControllerAndClose);
});