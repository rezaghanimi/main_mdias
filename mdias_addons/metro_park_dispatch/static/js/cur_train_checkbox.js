odoo.define('metro_park_dispatch.cur_train_manay2many', function (require) {
    "use strict";

    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;
    var relational_fields = require('web.relational_fields');
    var FieldMany2ManyCheckBoxes = relational_fields.FieldMany2ManyCheckBoxes
    var fieldRegistry = require('web.field_registry');

    /**
     * 现车checkbox
     */
    var cur_train_manay2many = FieldMany2ManyCheckBoxes.extend({
        template: 'cur_train_manay2many',
        cur_train_infos: [],

        /**
         * 重新获取一次
         */
        willStart: function () {
            var self = this
            var ids = _.map(this.m2mValues, function(val){
                return val[0]
            })
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    "model": "metro_park_dispatch.cur_train_manage",
                    "method": "get_cur_train_info",
                    "args": [ids]
                }).then(function (rst) {
                    self.cur_train_infos = rst
                })
            })
        },

        /**
         * 重新获取
         */
        _reset: function () {
            console.log('the filed is reset')
            this._super.apply(this, arguments);
        },
    });

    fieldRegistry.add('cur_train_manay2many', cur_train_manay2many);

    return cur_train_manay2many;
});