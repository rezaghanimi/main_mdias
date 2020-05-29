odoo.define('funenc.search_extend', function (require) {
    "use strict";

    /**
     * 如果提供了自定义模板则走自定义模板，如果没有则走配置, 主要目的是为了取得domain
     */
    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var Registry = require('web.Registry');

    var search_extend = Widget.extend({
        className: 'lay_custom_search layui-form',
        search_view: undefined,

        /**
         * 初始化
         * @param {*} parent 父元素
         * @param {*} fields  搜索的字段
         * @param {*} template 模板
         * @param {*} search_pannel_js_class 模板类
         * @param {*} search_view 搜索
         */
        init: function (parent, fields, template, search_pannel_js_class, search_view) {
            this.propositions = [];
            this.custom_filters_open = false;
            this.fields = fields

            // 不直接使用template，这样会闪烁
            this.pannel_template = template
            this.search_pannel_js_class = search_pannel_js_class
            this.search_view = search_view
            // 需要提供一个唯一id来标识
            this.controller_id = parent.controllerID || 'custom_random_controller_' + Math.ceil(Math.random()*100);
            this._super(parent);
        },

        start: function () {
            this.props = []
            this.$el.attr('lay-filter', 'custom_search_' + this.controller_id);
            var js_class = this.search_pannel_js_class
            if (!js_class || js_class == '') {
                js_class = 'custom_search_pannel'
            }
            var search_pannel = widgetRegistry.get(js_class)
            if (search_pannel) {
                var pannel = new search_pannel(this, this.fields, this.pannel_template, this.search_view)
                pannel.appendTo(this.$el);
                this.pannel = pannel;
                this.search_fields = pannel.search_fields;
            } else {
                console.log("can not find the search widget");
            }
        }
    });
    
    return {
        search_extend: search_extend,
        funenc_search_registry: new Registry(),
        funenc_propation_registry: new Registry(),
    }
});