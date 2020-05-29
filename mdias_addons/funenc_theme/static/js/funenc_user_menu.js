odoo.define('funenc.UserMenu', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var UserMenu = require('web.UserMenu');

    var _t = core._t;
    var QWeb = core.qweb;

    var FuenncUserMenu = UserMenu.include({
        template: 'FunencUserMenu',

        /**
         * @override
         * @returns {Deferred}
         */
        start: function () {
            var self = this;
            var session = this.getSession();
            // 绑定事件
            this.$el.on('click', '[data-menu]', function (ev) {
                ev.preventDefault();
                var menu = $(this).data('menu');
                self['_onMenu' + menu.charAt(0).toUpperCase() + menu.slice(1)]();
            });
            return $.when().then(function () {
                var $avatar = self.$('.oe_topbar_avatar');
                if (!session.uid) {
                    $avatar.attr('src', $avatar.data('default-src'));
                    return $.when();
                }
                var topbar_name = session.name;
                if (session.debug) {
                    topbar_name = _.str.sprintf("%s (%s)", topbar_name, session.db);
                }
                self.$('.oe_topbar_name').text(topbar_name);
                var avatar_src = session.url('/web/image', {
                    model: 'res.users',
                    field: 'image_small',
                    id: session.uid,
                });
                $avatar.attr('src', avatar_src);
            });
        },

        /**
         * @private
         */
        _onMenuLogout: function () {
            this.trigger_up('clear_uncommitted_changes', {
                callback: this.do_action.bind(this, 'logout'),
            });
        },
        /**
         * @private
         */
        _onMenuSettings: function () {
            var self = this;
            var session = this.getSession();
            this.trigger_up('clear_uncommitted_changes', {
                callback: function () {
                    self._rpc({
                        route: "/web/action/load",
                        params: {
                            action_id: "base.action_res_users_my",
                        },
                    })
                        .done(function (result) {
                            result.res_id = session.uid;
                            self.do_action(result);
                        });
                },
            });
        },

        _onMenuChangePassword: function () {
            this.do_action({
                'name': '修改密码',
                'type': 'ir.actions.client',
                'tag': 'change_password',
                'target': 'new'
            })
        },

        /**
         * @private
         */
        _onMenuSupport: function () {
            window.open('https://www.funenc.com', '_blank');
        },

        /**
         * @private
         */
        _onMenuShortcuts: function () {
            new Dialog(this, {
                size: 'large',
                dialogClass: 'o_act_window',
                title: _t("Keyboard Shortcuts"),
                $content: $(QWeb.render("UserMenu.shortcuts"))
            }).open();
        }

    });

    return FuenncUserMenu;
});
