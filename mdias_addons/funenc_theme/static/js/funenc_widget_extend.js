/**
 * 扩展增加权限判断函数
 */
odoo.define('funenc.widget', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var web_client = require('web.web_client');

    var FunencWidget = Widget.include({
        has_group: function(xml_id) {
            return web_client.has_group(xml_id)
        }
    });

    return FunencWidget;
});