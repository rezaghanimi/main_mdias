/**
 **传输通道质量监督
 **/
odoo.define('transmission_channel_monitoring', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var transmission_channel_monitoring = AbstractAction.extend({
        init: function (parent, params) {
            var self = this;
            self._super(parent, params);
            // 获取当前的交换机的端口号
            if (params.node_name) {
                sessionStorage.setItem('node_name', params.node_name)
            }
            if (sessionStorage.getItem('node_name')) {
                self.node_name = sessionStorage.getItem('node_name')
            } else {
                self.node_name = params.node_name
            }

            // 获取当前交换机的名称
            if (params.args_name) {
                sessionStorage.setItem('args_name', params.args_name)
            }
            if (sessionStorage.getItem('args_name')) {
                self.args_name = sessionStorage.getItem('args_name')
            } else {
                self.args_name = params.args_name
            }
            self.all_data = {
                radio: 1,
                switches_a: 400,
                // 用来隐藏其他的ECharts
                dis: self.act_button,
                value: self.value,
                options: self.option,
                temperature: [],
                temperature_time: [],
                current: [],
                current_time: [],
                voltage: [],
                voltage_time: [],
                transmission: [],
                transmission_time: [],
                receive: [],
                receive_time: [],
            }

        },

        willStart: function () {
            var self = this;
            var rec = self._rpc({
                model: 'maintenance_management.switch_log',
                method: 'choose_node_return_data',
                args: [self.args_name, self.node_name],
            }).then(function (data) {
                self.all_data.temperature = data[0][0]
                self.all_data.temperature_time = data[0][1]
                self.all_data.current = data[1][0]
                self.all_data.current_time = data[1][1]
                self.all_data.voltage = data[2][0]
                self.all_data.voltage_time = data[2][1]
                self.all_data.transmission = data[3][0]
                self.all_data.transmission_time = data[3][1]
                self.all_data.receive = data[4][0]
                self.all_data.receive_time = data[4][1]
            })
            return rec
        },

        on_attach_callback: function () {
            var self = this;
            setTimeout(function () {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    args: ['maintenance_management', 'transmission_channel_monitoring']
                }).then(function (data) {
                    self.$el.append(data);

                    new Vue({
                        el: '#transmission_channel_monitoring',
                        data: function () {
                            return self.all_data
                        },
                        methods: {},
                        mounted: function () {
                            this.$nextTick(function () {
                                var dashboard1 = echarts.init(document.getElementById('dashboard1'));
                                var option1 = {

                                    title: {
                                        text: '模块温度',
                                        x: 'center',
                                        align: 'right',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },

                                    tooltip: {
                                        trigger: 'axis'
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
                                        data: self.all_data.temperature_time
                                    },
                                    yAxis: {
                                        name: '°C',
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
                                        data: self.all_data.temperature,
                                        type: 'line'
                                    }]
                                };
                                dashboard1.setOption(option1);
                                var dashboard2 = echarts.init(document.getElementById('dashboard2'));
                                var option2 = {
                                    title: {
                                        text: '激光偏置电流',
                                        x: 'center',
                                        align: 'right',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
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
                                        data: self.all_data.current_time
                                    },
                                    yAxis: {
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
                                        name: 'uA',
                                        type: 'value'
                                    },
                                    series: [{
                                        data: self.all_data.current,
                                        type: 'line'
                                    }]
                                };
                                dashboard2.setOption(option2);
                                var dashboard3 = echarts.init(document.getElementById('dashboard3'));
                                var option3 = {
                                    title: {
                                        text: '供电电压',
                                        x: 'center',
                                        align: 'right',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
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
                                        data: self.all_data.voltage_time
                                    },
                                    yAxis: {
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
                                        name: 'mV',
                                        type: 'value'
                                    },
                                    series: [{
                                        data: self.all_data.voltage,
                                        type: 'line'
                                    }]
                                };
                                dashboard3.setOption(option3);
                                var dashboard4 = echarts.init(document.getElementById('dashboard4'));
                                var option4 = {
                                    title: {
                                        text: '发射光功率',
                                        x: 'center',
                                        align: 'right',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
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
                                        data: self.all_data.transmission_time
                                    },
                                    yAxis: {
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
                                        name: 'uW',
                                        type: 'value'
                                    },
                                    series: [{
                                        data: self.all_data.transmission,
                                        type: 'line'
                                    }]
                                };
                                dashboard4.setOption(option4);
                                var dashboard5 = echarts.init(document.getElementById('dashboard5'));
                                var option5 = {
                                    title: {
                                        text: '接收光功率',
                                        x: 'center',
                                        align: 'right',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
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
                                        data: self.all_data.receive_time
                                    },
                                    yAxis: {
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
                                        name: 'uW',
                                        type: 'value'
                                    },
                                    series: [{
                                        data: self.all_data.receive,
                                        type: 'line'
                                    }]
                                };
                                dashboard5.setOption(option5);
                            })
                        }
                    });
                });
            })
        }
    });

    core.action_registry.add('transmission_channel_monitoring', transmission_channel_monitoring);
    return {transmission_channel_monitoring: transmission_channel_monitoring}
});
