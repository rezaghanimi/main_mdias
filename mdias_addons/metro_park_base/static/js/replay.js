/**
 * 操作回放
 */
odoo.define('metro_park.rrweb_replay', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var rrweb_replay = AbstractAction.extend({
        template: 'metro_park_base.rr_player',
        cssLibs: [
            '/metro_park_base/static/css/rrweb.min.css',
            '/metro_park_base/static/css/rrweb-player.css'
        ],

        jsLibs: [
            '/metro_park_base/static/js/rrweb-player.js'
        ],

        events: [],

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.record_id = action.context.active_id || action.params.active_id
        },

        willStart: function () {
            var self = this
            return this._rpc({
                "model": "metro_park_base.rrweb_events",
                "method": "get_events",
                "args": [this.record_id]
            }).then(function (rst) {
                self.events = rst
            })
        },

        // 绑定计划
        on_attach_callback: function () {
            this.player = new rrwebPlayer({
                target: this.$('.player_box')[0],
                data: {
                    events: this.events,
                    autoPlay: false
                }
            });
        },

        /**
         * 销毁
         */
        destroy: function () {
            if (this.player) {
                try {
                    this.player.pause()
                } catch (error) {}   
            }
            this._super.apply(this, arguments)
        }
    });

    core.action_registry.add('rrweb_replay', rrweb_replay);
    return rrweb_replay;
});