/**
 * Created by artorias on 2018/6/12.
 */
odoo.define("change_title", function(require) {
    "use strict";

    var AbstractWebClient = require('web.AbstractWebClient');
    var concurrency = require('web.concurrency');
    var mixins = require('web.mixins');

    AbstractWebClient.include({
        init: function(parent) {
            this.client_options = {};
            mixins.ServiceProvider.init.call(this);
            this._super(parent);
            this.origin = undefined;
            this._current_state = null;
            this.menu_dm = new concurrency.DropMisordered();
            this.action_mutex = new concurrency.Mutex();
            this.set('title_part', { "zopenerp": "funenc" });
        },
        
        set_title_part: function(part, title) {
            var tmp = _.clone(this.get("title_part"));
            tmp[part] = title;
            tmp.zopenerp = 'funenc';
            this.set("title_part", tmp);
        }
    })
});