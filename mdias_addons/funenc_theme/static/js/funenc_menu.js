/**
 * main menu
 */
odoo.define('funenc.MainMenu', function (require) {
    "use strict";

    var Menu = require('web.Menu');
    var core = require('web.core');
    var SideBarMenu = require('funenc.SideBarMenu');
    var FunencAppsMenu = require('funenc.AppMenu');
    var SystrayMenu = require('web.SystrayMenu');

    /**
     * 重写，方式变化太大
     */
    var FunencMainMenu = Menu.include({
        sidebar_menu: undefined,
        current_primary_menu: undefined,
        current_secodary_menu: undefined,
        events: _.extend({}, Menu.prototype.events, {
            'click .logo_box': '_openHomePage',
        }),

        init: function (parent, menu_data) {
            // 所有的菜单数据
            this.menu_data = menu_data;
            this._super.apply(this, arguments);
        },

        start: function () {
            // Apps Menu
            this.$menu_apps = this.$('.o_menu_apps');

            // 项级菜单
            this._appsMenu = new FunencAppsMenu(this, this.menu_data);
            this._appsMenu.appendTo(this.$menu_apps);

            // Systray Menu
            this.systray_menu = new SystrayMenu(this);
            this.systray_menu.appendTo(this.$('.o_menu_systray'));

            // 二级菜单
            this.sidebar_menu = new SideBarMenu(this, this.menu_data);
            this.sidebar_menu.appendTo(this.$el);
        },

        /**
         * 取得当前主菜单
         */
        getCurrentPrimaryMenu: function () {
            return this.current_primary_menu;
        },

        /**
         * 打开第一个
         */
        openFirstApp: function () {
            var action_id = this._appsMenu.openFirstApp();
            this.sidebar_menu.open_first_menu_item(action_id);
        },

        /**
         *  这个是更改大的项
         * @param {*} primary_menu_id
         */
        chose_menu: function (menu_id) {
            if (this._appsMenu.has_app(menu_id)) {
                this._appsMenu.openAppByMenuId(menu_id);
                this.sidebar_menu.open_first_menu_item(menu_id);
                this.current_primary_menu = menu_id
            } else {
                var app_id = this.get_main_menu_id(menu_id);
                if (app_id != -1) {
                    this.current_primary_menu = app_id;
                    this._appsMenu.openAppByMenuId(app_id);
                    this.sidebar_menu.select_menu_item(menu_id);
                }
            }
        },

        /**
         * 通过mainmenu获取菜单
         * @param {} menu_id
         */
        get_main_menu_id: function (menu_id) {
            var self = this;
            var item = _.find(this.menu_data.children, function (menu_data) {
                return self.has_sub_menu_id(menu_data, menu_id);
            });
            return item ? item.id : undefined
        },

        /**
         * action id 转化成为menu id
         */
        action_id_to_menu_id: function (action_id) {
            var self = this;
            var item = _.find(this.menu_data.children, function (menu_data) {
                return self.has_sub_menu_id(menu_data, menu_id);
            })
            return item ? item.id : undefined
        },

        /**
         * 是否有子菜单
         * @param {} root
         * @param {*} menu_id
         */
        has_sub_menu_id: function (root, menu_id) {
            var self = this;
            if (root.id == menu_id) {
                return true
            } else if (root.children) {
                for (var i = 0; i < root.children.length; i++) {
                    var tmp = root.children[i];
                    if (self.has_sub_menu_id(tmp, menu_id)) {
                        return true;
                    }
                }
            }
            return false;
        },

        /**
         * find sub menu by action
         */
        find_menu_by_action_id: function (action_id) {
            var self = this;
            for (var i = 0; i < this.menu_data.children.length; i++) {
                var tmp = this.menu_data.children[i];
                var id = self._find_sub_menu_by_acton_id(tmp, action_id)
                if (id) {
                    return id;
                }
            }
            return undefined;
        },

        /**
         * internal method
         * @param {*} root
         * @param {*} action_id
         */
        _find_sub_menu_by_acton_id: function (root, action_id) {
            var self = this;
            if (root.action && root.action.split(',')[1] === String(action_id)) {
                return root.id;
            } else if (root.children) {
                for (var i = 0; i < root.children.length; i++) {
                    var tmp = root.children[i];
                    var id = self._find_sub_menu_by_acton_id(tmp, action_id)
                    if (id) {
                        return id;
                    }
                }
            }
            return undefined;
        },

        /**
         * get default icon
         */
        get_default_icon: function (app) {
            var icon = "fa fa-envelope-o"
            switch (app.name) {
                case 'Apps':
                    icon = "fa fa-envelope-o"
                    break;
                case 'Settings':
                    icon = "fa fa-cog"
                    break;
            }
            return icon;
        },
        _openHomePage: function () {
            this.trigger_up('open_home')
        },
    });

    return FunencMainMenu;
});
