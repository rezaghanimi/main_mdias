/**
 * Created by artorias on 2019/5/24.
 */
odoo.define("change_title", function(require) {
    "use strict";

    var AbstractWebClient = require('web.AbstractWebClient');

    AbstractWebClient.include({
        init: function(parent) {
            this._super(parent);
            this.set('title_part', {"zopenerp": "Funenc"});
        },

        set_title_part: function(part, title) {
            var tmp = _.clone(this.get("title_part"));
            tmp[part] = title;
            tmp.zopenerp = 'Funenc';
            this.set("title_part", tmp);
        }
    })
});