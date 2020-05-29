odoo.define('server_client', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var server_client = AbstractAction.extend({
        init: function (parent, params) {
            this.zabbix_judge = true
            this.vue = new Vue({});
            var self = this;
            if (params.params_data) {
                sessionStorage.setItem('act_button', params.params_data)
            }
            if (sessionStorage.getItem('act_button')) {
                self.act_button = sessionStorage.getItem('act_button')
            } else {
                self.act_button = params.params_data
            }
            self._super(parent, params);
            self.all_data = {
                cup_data_key: '',
                cup_data_value: '',
                memory_key: '',
                memory_value: '',
                network_time: '',
                network_out: '',
                network_in: '',
                system_uptime_data: '',
                processes_data: '',
                login_user_data: '',
                all_disk: '',
                use_dick: '',
                system_name: '',
            }
        },

        willStart: function () {
            var self = this;
            var rec = self._rpc({
                model: 'maintenance_management.database_data',
                method: 'link_database_data',
                args: [self.act_button]
            }).then(function (data) {
                if (self.zabbix_judge) {
                    if (data == '请检查配置是否错误') {
                        self.vue.$message({
                            dangerouslyUseHTMLString: true,
                            offset: 500,
                            duration: 3000,
                            center: true,
                            showClose: true,
                            customClass: '信息错误',
                            message: '<div style="text-align: center;color: red">请检查配置是否错误</div>'
                        });
                        return
                    } else if (data == '连接失败，没有获取到数据') {
                        self.vue.$message({
                            dangerouslyUseHTMLString: true,
                            offset: 500,
                            duration: 3000,
                            center: true,
                            showClose: true,
                            customClass: '信息错误',
                            message: '<div style="text-align: center;color: red">连接失败，没有获取到数据</div>'
                        });
                        return
                    }
                }
                self.all_data.cup_data_key = data.cpu_key
                self.all_data.cup_data_value = data.cpu_value
                self.all_data.memory_key = data.memory_key
                self.all_data.memory_value = data.memory_value
                self.all_data.memory_value = data.memory_value
                self.all_data.network_time = data.network_time
                self.all_data.network_out = data.network_out
                self.all_data.network_in = data.network_in
                self.all_data.system_uptime_data = data.system_uptime_data
                self.all_data.processes_data = data.processes_data
                self.all_data.login_user_data = data.login_user_data
                self.all_data.all_disk = data.all_disk
                self.all_data.use_dick = data.use_dick
                self.all_data.system_name = data.system_name
            })
            return rec
        },

        on_attach_callback: function () {
            var self = this;
            setTimeout(function () {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    args: ['maintenance_management', 'server_client']
                }).then(function (data) {
                    self.$el.append(data);

                    new Vue({
                        el: '#server_client',
                        data: function () {
                            return self.all_data
                        },
                        method: {},
                        mounted: function () {
                            this.$nextTick(function () {
                                var dashboard4 = echarts.init(document.getElementById('dashboard4'));
                                var dashboard5 = echarts.init(document.getElementById('dashboard5'));
                                var dashboard6 = echarts.init(document.getElementById('dashboard6'));
                                var dashboard7 = echarts.init(document.getElementById('dashboard7'));
                                var option4 = {
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
                                        name: '时间',
                                        type: 'category',
                                        data: self.all_data.cup_data_key,
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    yAxis: {
                                        type: 'value',
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    series: [{
                                        data: self.all_data.cup_data_value,
                                        type: 'line'
                                    }]
                                };
                                dashboard4.setOption(option4);
                                var option5 = {
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
                                        name: '时间',
                                        type: 'category',
                                        data: self.all_data.memory_key,
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    yAxis: {
                                        name: '%',
                                        type: 'value',
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    series: [{
                                        data: self.all_data.memory_value,
                                        type: 'line'
                                    }]
                                };
                                dashboard5.setOption(option5);
                                var option6 = {
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
                                        name: '时间',
                                        type: 'category',
                                        data: self.all_data.network_time,
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    yAxis: {
                                        name: '流量(b)',
                                        type: 'value',
                                        axisLabel: {
                                            color: '#0ac4f7'
                                        },
                                        axisLine: {
                                            lineStyle: {
                                                color: '#0ac4f7'
                                            }
                                        },
                                    },
                                    series: [{
                                        data: self.all_data.network_out,
                                        type: 'line',
                                        smooth: true
                                    }, {
                                        data: self.all_data.network_in,
                                        type: 'line',
                                        smooth: true
                                    }]
                                };
                                dashboard6.setOption(option6);
                                var option7 = {
                                    title: {
                                        text: '系统磁盘',
                                        subtext: '饼状图',
                                        x: 'center'
                                    },
                                    tooltip: {
                                        trigger: 'item',
                                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                                    },
                                    series: [
                                        {
                                            name: '访问来源',
                                            type: 'pie',
                                            radius: '55%',
                                            center: ['50%', '60%'],
                                            data: [
                                                {value: self.all_data.all_disk, name: '已用磁盘'},
                                                {value: self.all_data.all_disk - self.all_data.use_dick, name: '未使用磁盘'},
                                            ],
                                            itemStyle: {
                                                emphasis: {
                                                    shadowBlur: 10,
                                                    shadowOffsetX: 0,
                                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                                }
                                            }
                                        }
                                    ]
                                };
                                dashboard7.setOption(option7);
                            })
                        }
                    });
                });
            })
        },
        destroy: function () {
            this.zabbix_judge = false
        }
    });

    core.action_registry.add('server_client', server_client);
    return {server_client: server_client}
});
