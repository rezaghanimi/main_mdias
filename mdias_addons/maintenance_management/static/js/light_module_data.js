odoo.define('light_module_data', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var light_module_data = AbstractAction.extend({
        init: function (parent, params) {
            this.zabbix_judge = true
            this.vue = new Vue({});
            var self = this;
            if (params.send_data) {
                sessionStorage.setItem('send_data', params.send_data)
            }
            if (sessionStorage.getItem('send_data')) {
                self.send_data = sessionStorage.getItem('send_data')
            } else {
                self.send_data = params.send_data
            }
            self._super(parent, params);
            self.all_data = {
                sites: [],
                cpu: 0,
                memory: 0,
                temperature: 0,
            }
        },

        willStart: function () {
            var self = this;
            var rec = self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'get_light_models',
                args: [self.send_data]
            }).then(function (data) {
                if (data == '数据获取失败') {
                    if (self.zabbix_judge) {
                        self.vue.$message({
                            dangerouslyUseHTMLString: true,
                            offset: 500,
                            duration: 3000,
                            center: true,
                            showClose: true,
                            customClass: '信息错误',
                            message: '<div style="text-align: center;color: red">数据获取失败</div>'
                        });

                    }
                } else {
                    self.all_data.sites = data[0]
                    self.all_data.cpu = data[1][0]
                    self.all_data.memory = data[1][1]
                    self.all_data.temperature = data[1][2]
                }
            })
            return rec
        },

        on_attach_callback: function () {
            var self = this;
            setTimeout(function () {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    args: ['maintenance_management', 'light_module_data']
                }).then(function (data) {
                    self.$el.append(data);
                    new Vue({
                        el: '#light_module_data',
                        data: function () {
                            return self.all_data
                        },
                        methods: {
                            button_click: function (data) {
                                self.do_action({
                                    'type': 'ir.actions.client',
                                    'tag': 'transmission_channel_monitoring',
                                    'node_name': data,
                                    'args_name': self.send_data,
                                })
                            }
                        },
                        mounted: function () {
                            this.$nextTick(function () {
                            })
                        },
                    });
                });
            })
        },
        destroy: function () {
            this.zabbix_judge = false
        }
    });

    core.action_registry.add('light_module_data', light_module_data);
    return {light_module_data: light_module_data}
});
