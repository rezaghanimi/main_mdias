odoo.define("funenc.abstruct_view", function (require) {
    "use strict";

    var AbstractView = require('web.AbstractView')

    // 初始初始化，让controller能获取到arch和option信息
    AbstractView.include({
        init: function () {
            this._super.apply(this, arguments)
            // 将arch传入到controller中
            this.controllerParams['arch'] = this.arch;
        }
    });
})
