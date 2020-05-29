/**
 * Created by artorias on 2019/9/16.
 */
odoo.define("judge_change_password", function (require) {
    "use strict";

    var AbstractWebClient = require('web.AbstractWebClient');
    var Dialog = require('web.Dialog');

    AbstractWebClient.include({
        set_action_manager: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                // 去掉密码超3个月未修改提示
                // self.judge_change_password();  
                self.on_bus('sso_login', function (data, call) {
                    window.location.href = "/web/session/logout?redirect=/web/login?sso_login=true";
                });
            });
        },

        judge_change_password: function () {
            var self = this;
            self._rpc({
                model: 'res.users',
                method: 'judge_change_password'
            }).then(function (result) {
                if (result) {
                    Dialog.confirm(self, '密码已经超过3个月未修改，请修改密码', {
                        title: '提示',
                        confirm_callback: function () {
                            self.do_action({
                                'name': '修改密码',
                                'type': 'ir.actions.client',
                                'tag': 'change_password',
                                'target': 'new'
                            })
                        },
                        cancel_callback: function () {
                        }
                    });
                }
            })
        }
    })
});