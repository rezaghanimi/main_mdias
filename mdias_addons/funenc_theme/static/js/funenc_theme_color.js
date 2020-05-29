odoo.define('funenc.ThemeColor', function (require) {
    "use strict";

    /**
     * 右侧颜色选项
     */
    var Widget = require('web.Widget');

    /**
     * 主题颜色
     */
    var ThemeColor = Widget.extend({
        template: 'funenc_theme_color',
        style: {}, // 字典，保存的时候也是保存这个字典
        items: [],
        widgets: [],
        $color_box: undefined,
        style_id: 'funenc_theme_style_id',

        events: {
            'click .customizer-toggle': '_on_custom_toggle_click'
        },

        custom_events: {
            'funenc_theme_color_changed': '_on_theme_color_changed'
        },

        /**
         * 加载颜色style, 从系统获取用户颜色，如果没有则使用主题自带的
         */
        willStart: function () {
            var self = this;
            return this._rpc({
                "model": "funenc_theme.funenc_theme_style",
                "method": "get_user_style",
                "args": [{
                    year: this.year
                }]
            }).then(function (style) {
                self.style = style || {}
            })
        },

        /**
         * 开始
         */
        start: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                self.$color_box = self.$('.color_box')

                // 1、加载颜色项
                self._loadItems();

                // 2、初始化颜色样式
                self.update_style();
            });
        },

        /**
         * 转换成为json
         */
        get_style: function () {
            var style_txt = ''
            _.each(this.widgets, function (item) {
                style_txt += item.get_style()
            });
            return style_txt
        },

        /**
         * 主题颜色发生改变
         * @param {} option 
         */
        _on_theme_color_changed: function (event) {
            var new_color = event.data.new_color
            var cls_key = event.data.cls_key
            this.style[cls_key] = new_color
            this.update_style();
            this.update_user_style();
        },

        /**
         * 更新样式, client加载的时候初始化一次颜色
         */
        update_style: function (refresh) {
            var style_id = 'funenc_theme_style_id';
            var $body = $('body')
            var styleText = this.get_style();
            var style = document.getElementById(style_id);

            // 添加主题样式
            if (style.styleSheet) {
                style.setAttribute('type', 'text/css');
                style.styleSheet.cssText = styleText;
            } else {
                style.innerHTML = styleText;
            }
            style.id = style_id;

            style && $body[0].removeChild(style);
            $body[0].appendChild(style);
        },

        /**
         * 更新样式到系统
         */
        update_user_style: function () {
            this._rpc({
                "model": "funenc_theme.funenc_theme_style",
                "method": "update_user_style",
                "args": [this.style]
            })
        },

        /**
         * 展开
         */
        _on_custom_toggle_click: function (event) {
            event.stopPropagation();
            this.$el.toggleClass("open")
        },

        /**
         * Instantiate items, using the classes located in SystrayMenu.items.
         */
        _loadItems: function () {
            var self = this;

            // 进行一次排序
            _.sortBy(ThemeColor.Items, function (colorItem) {
                return !_.isUndefined(colorItem.prototype.sequence) ? colorItem.prototype.sequence : 50;
            });

            _.each(ThemeColor.Items, function (colorItem) {
                var item_widget = new colorItem(self)
                item_widget.appendTo(self.$color_box)
                self.widgets.push(item_widget)
            });
        },
    });

    // 其它组件引用这个, 然后添加自己到面版面, 这样就能实现扩展, 样式为
    // [{'title' : 'xxx', 'color': 'xxx' }]
    ThemeColor.Items = [];
    return ThemeColor;
});

/**
 * 需要配置颜色的类需要继承这个类, cls_key需要和对应的组件配对
 */
odoo.define('funenc.ThemeColorPicker', function (require) {
    "use strict";

    var Widget = require('web.Widget')
    var core = require('web.core')

    var ThemeColorPicker = Widget.extend({
        template: 'funenc_theme_color.item',
        title: '颜色',
        cls_key: undefined,
        css_key: undefined,
        color: undefined,
        sequence: 50,  // 用于排序
        color_manager: undefined,

        color_item: undefined,
        pickr: undefined,

        /**
         * 需要重写这个函数
         */
        get_style: function () {
            var style_txt = core.qweb.render('funenc_theme_css_template',
                {
                    cls_key: this.cls_key,
                    css_key: this.css_key,
                    color: this.color
                })
            return style_txt
        },

        /**
         * 初始化
         * @param {*} parent 
         * @param {*} color_manager 
         */
        init: function (parent) {
            this._super.apply(this, arguments)
            this.color = parent.style[this.cls_key] || this.color
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.color-picker').colorpicker({
                    format: 'rgb',
                    useAlpha: true
                }).on('colorpickerChange', function (e) {
                    if (!e.color || !e.color.isValid()) {
                        return;
                    }

                    var old_color = self.color
                    var new_color = e.color.string();
                    if (new_color == old_color) {
                        return;
                    }

                    if (!self.cls_key || !self.css_key) {
                        return
                    }

                    self.trigger_up('funenc_theme_color_changed', {
                        old_color: old_color,
                        new_color: new_color,
                        cls_key: self.cls_key
                    });
                    self.color = new_color;
                });
            })
        }
    });

    return ThemeColorPicker;
});