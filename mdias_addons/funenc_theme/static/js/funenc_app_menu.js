/**
 * main menu
 */
odoo.define('funenc.AppMenu', function (require) {
    "use strict";

    var Widget = require('web.Widget');
    var ThemeColor = require('funenc.ThemeColor')
    var ThemeColorPicker = require('funenc.ThemeColorPicker')
    var core = require('web.core')
    var qweb = core.qweb

    var FunencAppMenu = Widget.extend({
        template: 'AppsMenu',

        /**
         * 初始化数据
         * @param {*} parent
         * @param {*} menuData
         */
        init: function (parent, menuData) {
            this._activeApp = undefined;
            // 顶级菜单项, 使用这个进行渲染
            this._apps = _.map(menuData.children, function (appMenuData) {
                return {
                    actionID: parseInt(appMenuData.action.split(',')[1]),
                    menuID: appMenuData.id,
                    name: appMenuData.name,
                    xmlID: appMenuData.xmlid,
                    font_icon: appMenuData.font_icon,
                    children: appMenuData.children,
                    id: appMenuData.id,
                    action: appMenuData.action
                };
            });
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this
            this._super.apply(this, arguments).then(function () {
                // 大小改变的时候处理菜单
                $(window).on('resize', function () {
                    setTimeout(_.bind(self.checkMenu, self), 100)
                });
                setTimeout(_.bind(self.checkMenu, self), 300)
            })

            this.$('.view_more').click(function () {
                core.bus.trigger('main_window');
                self.$('.view_more > div > a').removeClass('active');
            });

            this.$('.nav-item').click(function () {
                core.bus.trigger('main_window');
                self.$('.view_more > div > a').removeClass('active');
            })
        },

        /**
         * view more 处理
         */
        checkMenu: function () {
            var view_more_width = this.$('.view_more').outerWidth(true);
            var max_width = this.$el.width();
            var total_width = view_more_width
            this.$('.nav-item').each(function () {
                total_width += $(this).outerWidth(true);
            });

            // 超出总的宽度
            if (total_width > max_width) {
                // 移除掉项目
                var self = this;
                this.$('.view_more > div > a').remove();
                var cur_width = view_more_width;
                this.$('.nav-item').show().each(function () {
                    if (cur_width + $(this).outerWidth(true) < max_width) {
                        cur_width += $(this).outerWidth(true);
                    } else {
                        var link = $(this).find('.nav-link')
                        var link_title = $(this).find('.nav-link-title')
                        var name = link_title.text()

                        var action_id = link.data('action-id')
                        var menu_id = link.data('menu-id')
                        var xml_id = link.data('menu-xmlid')

                        var item = $(qweb.render('funenc.more_item', {
                            action_id: action_id,
                            menu_id: menu_id,
                            xml_id: xml_id,
                            name: name
                        }))

                        // 添加项进去
                        self.$('.view_more > div').append(item);
                        $(this).hide();
                    }
                });
                this.$('.view_more').show();
            } else {
                this.$('.nav-item').show();
                this.$('.view_more').hide();
            }
        },

        /**
         * 打开第一个app, 选中第一个app
         * @param {*} app
         */
        _setActiveApp: function (app) {
            var $newActiveApp = this.$('.nav-link[data-action-id="' + app.actionID + '"]');
            $newActiveApp.tab('show')
        },

        /**
         *
         * @param {*} menu_id
         */
        setActiveAppByMenuId: function (menu_id) {
            var $newActiveApp = this.$('.nav-link[data-action-id="' + app.actionID + '"]');
            $newActiveApp.tab('show')
        },

        /**
         * 是否有某个app
         * @param {} menu_id
         */
        has_app: function (menu_id) {
            return _.find(this._apps, function (app) {
                return app.menuID == menu_id
            })
        },

        /**
         * 通过action进行查找
         * @param {} actionID
         */
        get_app_by_action_id: function (actionID) {
            return _.find(this._apps, function (app) {
                return app.actionID == actionID
            })
        },

        /**
         * Open the first app in the list of apps
         */
        openAppByMenuId: function (menu_id) {
            var $app = this.$('.nav-link[data-menu-id="' + menu_id + '"]');
            $app.tab('show');
        },

        /**
         * 取得内容宽度
         */
        getContentWidth: function () {
            var total_width = 0;
            this.$('.pm-links > li').each(function () {
                total_width += $(this).outerWidth(true);
            });
            return total_width;
        },

        /**
         * get default icon
         */
        get_default_icon: function (menu) {
            var icon = "fa fa-book"
            switch (menu.name) {
                case 'Apps':
                    icon = "fa fa-book"
                    break;
                case 'Settings':
                    icon = "fa fa-cog"
                    break;
            }
            return icon;
        },


        /**
         * @returns {Object[]}
         */
        getApps: function () {
            return this._apps;
        },

        /**
         * Open the first app in the list of apps
         */
        openFirstApp: function () {
            if (!this._apps.length) {
                return
            }
            var firstApp = this._apps[0];
            this._openApp(firstApp);
            this._setActiveApp(firstApp);
            return firstApp.menuID;
        },

        /**
         * @private
         * @param {Object} app
         */
        _openApp: function (app) {

            var $oldActiveApp = this.$('.o_app.active');
            $oldActiveApp.removeClass('active');
            var $newActiveApp = this.$('.o_app[data-action-id="' + app.actionID + '"]');
            $newActiveApp.addClass('active');
        }
    });

    /**
     * 菜单颜色选择
     */
    var AppMenuColorPicker = ThemeColorPicker.extend({
        title: '一级菜单栏颜色:',
        color: '#1aa7b9',
        cls_key: 'o_main_navbar',
        css_key: 'background',
        sequence: 50,  // 用于排序
    })

    // 注册颜色设置
    ThemeColor.Items.push(AppMenuColorPicker);

    return FunencAppMenu;
});


