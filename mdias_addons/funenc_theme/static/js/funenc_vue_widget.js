/** 
 * 使用方式如下，目的是为了简化vue组件的使用, 使用模板如下
 * 
odoo.define('funenc.Apartment', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var vue_widget = require('funenc.vue_widget');
    var VueWidget = vue_widget.VueWidget
    var gen_vue_widget_id = vue_widget.gen_vue_widget_id

    var qweb = core.qweb;

    var ApartmentAction = AbstractAction.extend({
        vue_widget: undefined,
        dom_id: ,

        willStart: function () {
            this._super.apply(this)
            return this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                args: []
            }).then(function(res) {
                self.template = res
            })
        },

        init: function() {
            
        },

        start: function () {
            this._super.apply(this, arguments)
            this.$el.attr('id', self.dom_id)
            this.vue_widget = new VueWidget(this, 'funenc_apartment', 'apartment', this.init_vue)
            this.vue_widget.appendTo(this.$el);
        },

        init_vue: function (widget) {
            
            return new Vue({
                el: "#" + gen_vue_widget_id(),
                data() {
                    return {

                    };
                },

                methods: {
                    
                }
            });
        }
    });

    core.action_registry.add('ApartmentAction', ApartmentAction);
    return ApartmentAction;
});
*/

odoo.define('funenc.vue_widget', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var widget_id = 1
    function gen_vue_widget_id() {
        return 'vue_widget_id_' + widget_id++
    }

    /**
     * apartment_client
     */
    var VueWidget = Widget.extend({
        metro_parks: [],
        vue_template: undefined,
        vue_init_js: undefined,
        template_data: undefined,
        app: undefined,

        init: function(parent, mod, template, vue_init_js) {
            this.module = mod
            this.vue_template = template
            this.vue_init_js = vue_init_js
            this._super.apply(this, arguments)
        },

        /**
         * 初始化数据
         */
        willStart: function() {
            var self = this
            return this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                args: [this.module, this.vue_template]
            }).then(function(res) {
                self.template_data = res
            })
        },

        /**
         * 渲染
         */
        start: function() {
            var self = this
            this._super.apply(this, arguments)
            this.$el.css('width', '100%');
            this.$el.css('height', '100%');
            this.$el.append($(this.template_data))
            setTimeout(function(){
                self.app = self.vue_init_js(self)
            }, 0);
        },

        get_app: function() {
            return this.app;
        }
    });

    return {
        VueWidget: VueWidget,
        gen_vue_widget_id: gen_vue_widget_id
    };
});
