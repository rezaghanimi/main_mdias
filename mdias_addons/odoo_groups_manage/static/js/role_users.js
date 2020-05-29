/**
 * Created by artorias on 2019/2/18.
 */
odoo.define('role_user_list', function (require) {
    "use strict";

    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');
    var core = require('web.core');

    var role_user_list = Widget.extend({
        template: 'role_groups_operation_buttons',
        events: {
            'click': '_click_tree_buttons'
        },
        init: function (parent, record, node) {
            this._super(parent, record, node);
            this.id = record.res_id;
            this.record = record;
        },
        _click_tree_buttons: function (event) {
            var self = this;
            event.stopPropagation();
            var special = $(event.target).data('special');
            switch (special) {
                // 点击详情按鈕
                case 'permission':
                    self.do_action({
                        type: 'ir.actions.client',
                        name: '查看权限',
                        tag: 'UserPermissionForm',
                        target: 'new',
                        params: {
                            id: self.id
                        }
                    });
                    break;
                case 'role':
                    this._rpc({
                        model: 'ir.model.data',
                        method: 'xmlid_to_res_id',
                        kwargs: {xmlid: 'odoo_groups_manage.user_role_edit_form'},
                    }).then(function (res) {
                        self.do_action({
                                'name': '角色关联',
                                'type': 'ir.actions.act_window',
                                'res_model': 'res.users',
                                'res_id': self.id,
                                'views': [[res, 'form']],
                                'target': 'new',
                                'context': {
                                    dialog_size: 'medium'
                                }
                            });
                    });
                    break;
            }
        }
    });

    widgetRegistry.add("RoleUsersList", role_user_list);
    return {
        role_user_list: role_user_list
    }

});