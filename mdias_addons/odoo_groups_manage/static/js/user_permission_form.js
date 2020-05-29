/**
 * Created by artorias on 2019/2/19.
 */
odoo.define('user_permission_form', function (require) {
    'use strict';

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var UserPermissionForm = AbstractAction.extend({
        init: function () {
            this._super.apply(this, arguments);
            this.$vue = null;
            this.groups = [];
            this.params = arguments[1].params;
            this.load_groups();
        },
        load_groups: function () {
            var self = this;
            return self._rpc({
                model: 'res.groups',
                method: 'get_group_data',
                args: [self.id]
            }).then(function (data) {
                if (data) {
                    self.groups = data;
                    self._render()
                }
            });
        },

        _render: function () {
            var self = this;
            if (!this.$vue) {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    kwargs: {
                        module_name: 'odoo_groups_manage',
                        template_name: 'permission'
                    }
                }).then(function (el) {
                    self._replaceElement($(el));
                    self._rpc({
                        model: 'res.users',
                        method: 'search_read',
                        args: [[['id', '=', self.params.id]], ['groups_id']]
                    }).then(function (data) {
                        var exist_groups = [];
                        _.each(data[0].groups_id, function (grp_id) {
                            exist_groups.push(grp_id + '-group')
                        });
                        self.$vue = new Vue({
                            el: '#app',
                            data() {
                                var groups = self.groups;
                                return {
                                    groups: groups,
                                    defaultProps: {
                                        children: 'children',
                                        label: 'name',
                                        disabled: function () {
                                            return true
                                        }
                                    },
                                    checked: exist_groups
                                }
                            },
                            methods: {
                                onCancel: function () {
                                    self.do_action({'type': 'ir.actions.act_window_close'})
                                }
                            }
                        })
                    })
                });
            }
        },
    });

    core.action_registry.add('UserPermissionForm', UserPermissionForm);

    return {
        UserPermissionForm: UserPermissionForm
    }
});
