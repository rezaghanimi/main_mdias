odoo.define('funenc.dev_buttons', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var search_panel_default = require('funenc.search_panel_default');


    var py_utils = require('web.py_utils');
 
    var widgetRegistry = require('web.widget_registry');

    var dev_buttons = search_panel_default.include({
        events: _.extend({}, search_panel_default.prototype.events, {

            'click .o_list_button_add': '_onCreateRecord',
            'click .funenc_import_dev': '_onImportDev',
        }),

        _onImportDev: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'metro_park_maintenance.dev_import_wizard',
                views: [[false, 'form']]
            })
        },
        _onCreateRecord:function () {
                this.do_action({
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: 'metro_park_maintenance.train_dev',
                    views: [[false, 'form']]
                })
            },


    });

    widgetRegistry.add("dev_buttons", dev_buttons)

    return dev_buttons
});