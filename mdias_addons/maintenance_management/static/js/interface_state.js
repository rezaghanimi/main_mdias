/**
 * Created by artorias on 2018/12/10.
 */
odoo.define('interface_state', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var interface_state = AbstractAction.extend({
        init: function (parent, params) {
            var self = this;
            self._super(parent, params);
            if (params.send_data) {
                sessionStorage.setItem('act_button', params.send_data)
            }
            if (sessionStorage.getItem('act_button')) {
                self.act_button = sessionStorage.getItem('act_button')
            } else {
                self.act_button = params.send_data
            }
        },

        willStart: function () {
            var self = this;
            if (self.act_button == 'ATS_m') {
                self.return_data = 'get_ats_m_data'
            } else if (self.act_button == 'ATS_s') {
                self.return_data = 'get_ats_s_data'
            } else if (self.act_button == 'CI_m') {
                self.return_data = 'get_ci_m_data'
            } else if (self.act_button == 'CI_s') {
                self.return_data = 'get_ci_s_data'
            } else if (self.act_button == 'PSCADA_m') {
                self.return_data = 'get_pscada_m_data'
            } else if (self.act_button == 'PSCADA_s') {
                self.return_data = 'get_pscada_s_data'
            } else if (self.act_button == 'gdl_pscada_m') {
                self.return_data = 'get_gdl_pscada_data'
            } else if (self.act_button == 'gdl_ci_s') {
                self.return_data = 'get_gdl_ci_data'
            } else if (self.act_button == 'gdl_ci_m') {
                self.return_data = 'get_gdl_ci_data'
            } else {
                self.return_data = 'get_none_data'
            }
            var self = this;
            var rec = self._rpc({
                model: 'maintenance_management.server_state',
                method: self.return_data,
                args: [self.act_button]
            }).then(function (data) {
                self.send = data[0]
                self.recv = data[1]
                self.time = data[2]
            })
            return rec
        },
        on_attach_callback: function () {
            var self = this;
            setTimeout(function () {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    args: ['maintenance_management', 'interface_state']
                }).then(function (data) {
                    self.$el.append(data);

                    new Vue({
                        el: '#interface_state',
                        data: function () {
                            return {}
                        },
                        mounted: function () {
                            this.$nextTick(function () {
                                var dashboard1 = echarts.init(document.getElementById('dashboard1'));
                                var dashboard2 = echarts.init(document.getElementById('dashboard2'));
                                // var dashboard3 = echarts.init(document.getElementById('dashboard3'));
                                var option1 = {
                                    tooltip: {
                                        trigger: 'axis',
                                        axisPointer: {
                                            type: 'cross',
                                            label: {
                                                backgroundColor: '#6a7985'
                                            }
                                        }
                                    },
                                    xAxis: {
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                        name: '时间',
                                        type: 'category',
                                        data: self.time
                                    },
                                    yAxis: {
                                        name: '流量',
                                        type: 'value',
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        splitLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    series: [{
                                        data: self.send,
                                        type: 'line',
                                        smooth: true
                                    }]
                                };
                                dashboard1.setOption(option1);
                                var option2 = {
                                    tooltip: {
                                        trigger: 'axis',
                                        axisPointer: {
                                            type: 'cross',
                                            label: {
                                                backgroundColor: '#6a7985'
                                            }
                                        }
                                    },
                                    xAxis: {
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                        name: '时间',
                                        type: 'category',
                                        data: self.time
                                    },
                                    yAxis: {
                                        name: '流量',
                                        type: 'value',
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        splitLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    series: [{
                                        data: self.recv,
                                        type: 'line',
                                        smooth: true
                                    }]
                                };
                                dashboard2.setOption(option2);
                                // var option3 = {
                                //     xAxis: {
                                //         type: 'category',
                                //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                                //     },
                                //     yAxis: {
                                //         type: 'value'
                                //     },
                                //     series: [{
                                //         data: [820, 932, 901, 934, 1290, 1330, 1320],
                                //         type: 'line'
                                //     }]
                                // };
                                // dashboard3.setOption(option3);
                            })
                        }
                    });
                });
            })
        }
    });

    core.action_registry.add('interface_state', interface_state);
    return {interface_state: interface_state}
});
