odoo.define('funenc.theme_color_item', function (require) {
    "use strict";

    /**
     * 右侧颜色选项
     */
    var ThemeColorPicker = require('funenc.ThemeColorPicker')
    var ThemeColor = require('funenc.ThemeColor')

    /**
     * 主题配置选项
     */
    var theme_color_toggle = ThemeColorPicker.extend({
        title: '侧边栏:',
        color: 'red',
        cls_key: 'customizer-toggle',
        css_key: 'background',
        sequence: 51,  // 用于排序
    })

    // 注册颜色设置
    ThemeColor.Items.push(theme_color_toggle);

    return ThemeColorPicker;
});