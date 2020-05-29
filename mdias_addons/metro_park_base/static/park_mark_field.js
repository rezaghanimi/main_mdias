/**
 * 站场图
 */
odoo.define('funenc.park_map_field', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var MapWidget = require('funenc.metro_park.map_widget');
    var registry = require('web.field_registry');

    /**
     * 场段图字段
     */
    var ParkMapField = AbstractField.extend({
        park_map_id: undefined,
        map: undefined,

        start: function() {
            this._super.apply(this);
        },

        willStart: function() {
            return this._super.apply(this);
        },

        // 付值reset的时候会调用这个_render
        _render: function () {
            if (this.attrs.decorations) {
                this._applyDecorations();
            }

            // controller
            var controller = this.getParent().getParent()
            var model = controller.model;

            if (model.isNew(this.record.id)) {
                if(!this.map) {
                    this.map = new MapWidget(this, this.value? Base64.decode(this.value) : undefined);
                    this.map.appendTo(this.$el)
                }
    
                if (this.value) {
                    this.map.reload_map(Base64.decode(this.value));
                }
            } else {
                var self = this
                return this._rpc({
                    model: this.model,
                    method: 'search_read',
                    fields: [this.name],
                    domain: [['id', '=', this.res_id]],
                    context: {
                        'bin_size': false // 获取实际文件数据
                    }
                }).then(function (res) {
                    var data = res[0][self.name]
                    if(!self.map) {
                        self.map = new MapWidget(self, data? Base64.decode(data) : undefined);
                        self.map.appendTo(self.$el)
                    }
                })
            }
        }
    });

    registry.add('ParkMapField', ParkMapField);

    return ParkMapField;
});
