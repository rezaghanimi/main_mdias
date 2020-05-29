/**
 * Created by artorias on 2019/2/19.
 */
odoo.define('field_group_tree', function (require) {
    'use strict';
    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var field_groups = AbstractField.extend({
        supportedFieldTypes: ['many2many'],
        specialData: "_fetchSpecialRelation",

        init: function () {
            this._super.apply(this, arguments);
            this.m2mValues = this.record.specialData[this.name];
            this.id = this.record.res_id;
            this.active = this.record.data.active;
            this.vue_data = {
                groups_data: []
            };
            this.$vue = null;

        },
        isSet: function () {
            return true;
        },


        load_groups: function () {
            var self = this;
            return self._rpc({
                model: 'res.groups',
                method: 'get_group_data',
            }).then(function (data) {
                if (data) {

                    self.vue_data.groups_data = data;
                }
            });
        },

        _render: function () {
            this._super.apply(this, arguments);
            var self = this;
            if (!this.$vue) {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    kwargs: {
                        module_name: 'odoo_groups_manage',
                        template_name: 'field_groups'
                    }
                }).then(function (el) {
                    self._replaceElement($(el));
                    self.load_groups().then(function () {
                        self.$vue = new Vue({
                            el: '#app',
                            data() {
                                var checked_groups_ids = [];
                                if (self.value) {
                                    _.each(self.value.res_ids, function (id) {
                                        checked_groups_ids.push(id + '-group')
                                    })
                                }
                                var group_data = self.vue_data.groups_data;
                                return {
                                    checked_groups_ids: [],
                                    groups_data: group_data,
                                    mode: self.mode,
                                    defaultProps: {
                                        children: 'children',
                                        label: 'name',
                                        disabled: function () {
                                            return self.mode === 'readonly'
                                        }
                                    },
                                    filterText: '',
                                    checked: checked_groups_ids
                                }
                            },
                            methods: {

                                updateValue: function () {

                                    var checks = [];
                                    var keys = this.$refs.tree.getCheckedKeys();

                                    _.each(keys, function (k) {
                                        var info = k.split('-');
                                        if (info && info.length === 2 && info[1] === 'group') {
                                            checks.push(parseInt(info[0]));
                                        }
                                    });

                                    this.checked_groups_ids = checks;
                                },

                                filterGroup(value, data) {
                                    if (!value) return true;
                                    return data.path.indexOf(value) !== -1;
                                }
                            },

                            watch: {
                                checked_groups_ids: function (value) {
                                    self._setValue({
                                        operation: 'REPLACE_WITH',
                                        ids: value,
                                    });
                                },

                                filterText: function (val) {
                                    this.$refs.tree.filter(val);
                                }
                            },
                        })
                    });

                })
            }

        },


    });

    field_registry.add('field_groups', field_groups);

    return {
        field_groups: field_groups
    }
});
