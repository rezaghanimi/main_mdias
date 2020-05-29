odoo.define('funenc.web_client', function (require) {
    "use strict";

    var WebClient = require('web.WebClient');

    // var ThemeColor = require('funenc.ThemeColor');
    var core = require('web.core');
    var config = require('web.config');
    var session = require('web.session');

    var _t = core._t;

    var FunencWebClient = WebClient.include({
        theme_color: undefined,
        user_groups: [],

        custom_events: _.extend({}, WebClient.prototype.custom_events, {
            has_group: 'on_has_group',
            open_home: '_openHomePage'
        }),

        load_groups: function () {
            var self = this
            return self._rpc({
                "model": "res.users",
                "method": "get_user_xml_groups",
                "args": []
            }).then(function (rst) {
                self.user_groups = rst
            })
        },

        start: function () {
            var self = this;
            // we add the o_touch_device css class to allow CSS to target touch
            // devices.  This is only for styling purpose, if you need javascript
            // specific behaviour for touch device, just use the config object
            // exported by web.config
            this.$el.toggleClass('o_touch_device', config.device.touch);
            this.on("change:title_part", this, this._title_changed);
            this._title_changed();

            return session.is_bound
                .then(function () {
                    self.$el.toggleClass('o_rtl', _t.database.parameters.direction === "rtl");
                    self.bind_events();
                    return $.when(
                        self.set_action_manager(),
                        self.set_loading(),
                        self.load_groups()
                    );
                }).then(function () {
                    if (session.session_is_valid()) {
                        return self.show_application();
                    } else {
                        // database manager needs the webclient to keep going even
                        // though it has no valid session
                        return $.when();
                    }
                }).then(function () {
                    // Listen to 'scroll' event and propagate it on main bus
                    self.action_manager.$el.on('scroll', core.bus.trigger.bind(core.bus, 'scroll'));
                    core.bus.trigger('web_client_ready');
                    odoo.isReady = true;
                    if (session.uid === 1) {
                        self.$el.addClass('o_is_superuser');
                    }
                });
        },

        /**
         * 通过xml判断用户是否有权限
         */
        has_group: function (xml_id) {
            return this.user_groups[xml_id] || false
        },

        /**
         * 当地址发生改变的时候, 实际点击的时候没有走这条支线，实际点击的时候走的是
         * @param {*} event
         */
        on_hashchange: function (event) {

            if (this._ignore_hashchange) {
                this._ignore_hashchange = false;
                return $.when();
            }

            var self = this;
            return this.clear_uncommitted_changes().then(function () {
                var stringstate = $.bbq.getState(false);
                if (!_.isEqual(self._current_state, stringstate)) {
                    var state = $.bbq.getState(true);
                    if (state.action || (state.model && (state.view_type || state.id))) {
                        // 这里打开action, 打开完成之后选择对应的菜单
                        return self.action_manager.loadState(state, !!self._current_state).then(function () {
                            var action = self.action_manager.getCurrentAction();
                            if (action) {
                                var menu_id = self.menu.find_menu_by_action_id(action.id);
                                if (menu_id) {
                                    self.menu.chose_menu(menu_id);
                                }
                            }
                        });
                    } else if (state.menu_id) {
                        var action_id = self.menu.menu_id_to_action_id(state.menu_id);
                        return self.do_action(action_id, {clear_breadcrumbs: true}).then(function () {
                            self.menu.chose_menu(state.menu_id);
                        });
                    } else {
                        self.menu.openFirstApp();
                    }
                }
                self._current_state = stringstate;
            }, function () {
                if (event) {
                    self._ignore_hashchange = true;
                    window.location = event.originalEvent.oldURL;
                }
            });
        },
        show_application: function () {
            var self = this;
            this.set_title();

            return this.instanciate_menu_widgets().then(function () {
                $(window).bind('hashchange', self.on_hashchange);

                // If the url's state is empty, we execute the user's home action if there is one (we
                // show the first app if not)
                if (_.isEmpty($.bbq.getState(true))) {
                    return self._rpc({
                        model: 'res.users',
                        method: 'read',
                        args: [session.uid, ["action_id"]],
                    })
                        .then(function (result) {
                            var data = result[0];
                            if (data.action_id) {
                                return self.do_action(data.action_id[0]).then(function () {
                                    self.menu.change_menu_section(self.menu.action_id_to_primary_menu_id(data.action_id[0]));
                                });
                            } else {
                                if (!!core.home_client_action) {
                                    self.trigger_up('open_home')
                                } else {
                                    self.menu.openFirstApp();
                                }
                            }
                        });
                } else {
                    return self.on_hashchange();
                }
            });
        },

        _openHomePage: function () {
            if (!!core.home_client_action) {
                var action = Object.assign({}, core.home_client_action);
                // core.bus.trigger('main_max');
                this.do_action(action);
            }
        }
    });

    return FunencWebClient;
});
