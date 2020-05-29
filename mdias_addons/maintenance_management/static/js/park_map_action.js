/**
 * 站场图
 */
odoo.define('funenc.metro_park.park_map', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var MapWidget = require('funenc.metro_park.map_widget');

    /**
     * 建模工具客户端
     */
    var ParkMap = AbstractAction.extend({
        park_map_id: undefined,
        map: undefined,
        map_info: undefined,

        events: {
            // 'click .add_table': '_on_add_table',
            // 'click .export_table': '_on_export_table'
        },

        /**
         * 初始化
         * @param {} parent 
         * @param {*} action 
         */
        init: function (parent, action) {
            this.park_map_id = action.context.active_id || action.params.active_id;
            this._super.apply(this, arguments);
        },

        /**
         * 渲染结束，组件初始化
         */
        start: function () {
            this._super.apply(this, arguments);
            if (this.map_info) {
                // mx_graph引入了一个base
                this.map = new MapWidget(this, Base64.decode(this.map_info.xml));
                this.map.appendTo(this.$el)
            }
        },

        /**
         * 加载模型数据
         */
        willStart: function () {
            var self = this
            return this._rpc({
                model: 'metro_park_base.park_map',
                method: 'get_map_info',
                args: [this.park_map_id]
            }).then(function (res) {
                if (res && res instanceof Array) {
                    self.map_info = res[0]
                }
            })
        }
    });

    core.action_registry.add('ParkMap', ParkMap);

    return ParkMap;
});
