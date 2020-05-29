/**
 * 继承web.IFrameWidget 捕捉跨域错误
 */
odoo.define('funenc.AppIFrameWidget', function (require) {
    "use strict";


    var IFrameWidget = require('web.IFrameWidget')

    var AppIFrameWidget = IFrameWidget.extend({
        _bindEvents: function () {
            try {
                this.$el.contents().click(this._onIFrameClicked.bind(this));
            } catch (e) {
                console.log(e);
            }

        }
    })


    return AppIFrameWidget;
});


