odoo.define('funenc.notification', function (require) {
    var Notification = require('web.Notification');

    Notification.include({
        template: 'ThemeNotification'
    });
});