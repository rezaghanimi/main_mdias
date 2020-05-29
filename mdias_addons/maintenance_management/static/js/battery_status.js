odoo.define("maintenance_management.battery_status", function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var battery_status = AbstractAction.extend({

        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.zabbix_judge = true
            this.vue = new Vue({});
            var self = this;
            self.act_button = params.parameter
            if (!sessionStorage.getItem('act_button')) {
                sessionStorage.setItem('act_button', params.parameter)
            } else {

            }

            if (params.parameter) {
                sessionStorage.setItem('act_button', params.parameter)
            }
            if (sessionStorage.getItem('act_button')) {
                self.act_button = sessionStorage.getItem('act_button')
            } else {
                self.act_button = params.parameter
            }
            self.parameter = params.parameter
            self.all_data = {
                options: [{
                    value: '电池组1',
                    label: '电池组1'
                }, {
                    value: '电池组2',
                    label: '电池组2'
                }, {
                    value: '电池组3',
                    label: '电池组3'
                }, {
                    value: '电池组4',
                    label: '电池组4'
                }, {
                    value: '电池组5',
                    label: '电池组5'
                }, {
                    value: '电池组6',
                    label: '电池组6'
                }, {
                    value: '电池组7',
                    label: '电池组7'
                }, {
                    value: '电池组8',
                    label: '电池组8'
                }, {
                    value: '电池组9',
                    label: '电池组9'
                }, {
                    value: '电池组10',
                    label: '电池组10'
                }, {
                    value: '电池组11',
                    label: '电池组11'
                }, {
                    value: '电池组12',
                    label: '电池组12'
                }, {
                    value: '电池组13',
                    label: '电池组13'
                }, {
                    value: '电池组14',
                    label: '电池组14'
                }, {
                    value: '电池组15',
                    label: '电池组15'
                }, {
                    value: '电池组16',
                    label: '电池组16'
                }, {
                    value: '电池组17',
                    label: '电池组17'
                }, {
                    value: '电池组18',
                    label: '电池组18'
                }, {
                    value: '电池组19',
                    label: '电池组19'
                }, {
                    value: '电池组20',
                    label: '电池组20'
                }, {
                    value: '电池组21',
                    label: '电池组21'
                }, {
                    value: '电池组22',
                    label: '电池组22'
                }, {
                    value: '电池组23',
                    label: '电池组23'
                }, {
                    value: '电池组24',
                    label: '电池组24'
                }, {
                    value: '电池组25',
                    label: '电池组25'
                }, {
                    value: '电池组26',
                    label: '电池组26'
                }, {
                    value: '电池组27',
                    label: '电池组27'
                }, {
                    value: '电池组28',
                    label: '电池组28'
                }, {
                    value: '电池组29',
                    label: '电池组29'
                },],
                value: '',
                value1: '',
                ups_option: [{
                    value: 'UPS输出电压',
                    label: 'UPS输出电压'
                }, {
                    value: 'UPS输入电流',
                    label: 'UPS输入电流'
                }, {
                    value: 'UPS输出频率',
                    label: 'UPS输出频率'
                }, {
                    value: 'UPS电池电流',
                    label: 'UPS电池电流'
                }, {
                    value: 'UPS电池电压',
                    label: 'UPS电池电压'
                }, {
                    value: 'UPS整流器输入电压',
                    label: 'UPS整流器输入电压'
                }, {
                    value: 'UPS整流器输入电流',
                    label: 'UPS整流器输入电流'
                }, {
                    value: 'UPS整流器输入频率',
                    label: 'UPS整流器输入频率'
                }, {
                    value: 'UPS温度',
                    label: 'UPS温度'
                }],
                ups_value: '',
                ups_value1: '',
                ups_side_option: [{
                    value: 'UPS旁路输入RS电压',
                    label: 'UPS旁路输入RS电压'
                }, {
                    value: 'UPS旁路输入ST电压',
                    label: 'UPS旁路输入ST电压'
                }, {
                    value: 'UPS旁路输入RT电压',
                    label: 'UPS旁路输入RT电压'
                }, {
                    value: 'UPS旁路输入R相电压',
                    label: 'UPS旁路输入R相电压'
                }, {
                    value: 'UPS旁路输入S相电压',
                    label: 'UPS旁路输入S相电压'
                }, {
                    value: 'UPS旁路输入T相电压',
                    label: 'UPS旁路输入T相电压'
                }, {
                    value: 'UPS旁路输入频率',
                    label: 'UPS旁路输入频率'
                }],
                ups_side_value: '',
                ups_side_value1: '',
                battery_voltage: [],
                battery_internal_resistance: [],
                battery_temperature: [],
                search_data_resistance_ceiling: [],
                voltage_difference_ceiling: [],
                cell_communication: [],
                battery_date: [],
                ups_side_date: [],
                ups_side_rs: [],
                ups_side_st: [],
                ups_side_rt: [],
                ups_side_r: [],
                ups_side_s: [],
                ups_side_t: [],
                ups_side_frequency: [],
                ups_output_rs_voltage: [],
                ups_output_st_voltage: [],
                ups_output_rt_voltage: [],
                ups_output_r_phase_voltage: [],
                ups_output_s_phase_voltage: [],
                ups_output_t_phase_voltage: [],
                ups_output_r_phase_current: [],
                ups_output_s_phase_current: [],
                t_phase_current_output_from_ups: [],
                ups_output_frequency: [],
                ups_battery_current: [],
                ups_battery_voltage: [],
                ups_rectifier_input_uv_voltage: [],
                the_ups_rectifier_inputs_vw_voltage: [],
                ups_rectifier_input_uw_voltage: [],
                ups_rectifier_input_u_phase_current: [],
                ups_rectifier_input_v_phase_current: [],
                ups_rectifier_input_w_phase_current: [],
                ups_rectifier_input_frequency: [],
                ups_inverter_r_temperature: [],
                ups_inverter_s_temperature: [],
                temperature_of_ups_inverter_t: [],
                ups_rectifier_temperature: [],
                ups_ambient_temperature: [],
                ups_date: [],
                act_button: ''
            }
        },

        on_attach_callback: function () {
            var self = this;
            if (sessionStorage.getItem('act_button') == 'ups_m') {
                self.act_button = '板桥'
            } else if (sessionStorage.getItem('act_button') == 'tpy_ups') {
                self.act_button = '太平园'
            } else if (sessionStorage.getItem('act_button') == 'gdl_ups') {
                self.act_button = '高大路'
            }
            setTimeout(function () {
                self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    args: ['maintenance_management', 'battery']
                }).then(function (data) {
                    self.$el.append(data);

                    new Vue({
                        el: '#battery',
                        data: function () {
                            return self.all_data
                        },
                        methods: {
                            ups_choose_data: function (data) {
                                if (data === 'UPS输出电压') {
                                    $('#ups_1').show()
                                    this.ups_1()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS输入电流') {
                                    $('#ups_2').show()
                                    this.ups_2()
                                    $('#ups_1').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS输出频率') {
                                    $('#ups_3').show()
                                    this.ups_3()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS电池电流') {
                                    $('#ups_4').show()
                                    this.ups_4()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS电池电压') {
                                    $('#ups_5').show()
                                    this.ups_5()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS整流器输入电压') {
                                    $('#ups_6').show()
                                    this.ups_6()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS整流器输入电流') {
                                    $('#ups_7').show()
                                    this.ups_7()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_8').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS整流器输入频率') {
                                    $('#ups_8').show()
                                    this.ups_8()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_9').hide()
                                } else if (data === 'UPS温度') {
                                    $('#ups_9').show()
                                    this.ups_9()
                                    $('#ups_1').hide()
                                    $('#ups_2').hide()
                                    $('#ups_3').hide()
                                    $('#ups_4').hide()
                                    $('#ups_5').hide()
                                    $('#ups_6').hide()
                                    $('#ups_7').hide()
                                    $('#ups_8').hide()
                                }
                            },
                            ups_side_choose: function (data) {
                                if (data === 'UPS旁路输入RS电压') {
                                    $('#ups_side_1').show()
                                    this.ups_side_1(self)
                                    $('#ups_side_2').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_6').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入ST电压') {
                                    $('#ups_side_2').show()
                                    this.ups_side_2(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_6').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入RT电压') {
                                    $('#ups_side_3').show()
                                    this.ups_side_3(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_2').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_6').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入R相电压') {
                                    $('#ups_side_4').show()
                                    this.ups_side_4(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_2').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_6').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入S相电压') {
                                    $('#ups_side_5').show()
                                    this.ups_side_5(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_2').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_6').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入T相电压') {
                                    $('#ups_side_6').show()
                                    this.ups_side_6(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_2').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_7').hide()
                                } else if (data === 'UPS旁路输入频率') {
                                    $('#ups_side_7').show()
                                    this.ups_side_7(self)
                                    $('#ups_side_1').hide()
                                    $('#ups_side_2').hide()
                                    $('#ups_side_3').hide()
                                    $('#ups_side_4').hide()
                                    $('#ups_side_5').hide()
                                    $('#ups_side_6').hide()
                                }
                            },
                            handleClick: function (data) {
                            },
                            // 电源搜索按钮
                            search_data(data) {
                                var self_value = this;
                                self._rpc({
                                    model: 'maintenance_management.server_state',
                                    method: 'get_battery_data',
                                    args: [self.all_data.value, self.all_data.value1, self.act_button]
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
                                        }
                                    }
                                    self.all_data.battery_voltage = data[0]
                                    self.all_data.battery_internal_resistance = data[1]
                                    self.all_data.battery_temperature = data[2]
                                    self.all_data.battery_date = data[3]
                                    self_value.dashboard1()
                                    self_value.dashboard2()
                                    self_value.dashboard3()
                                })
                            },

                            // ups搜索按钮
                            search_data_ups(data) {
                                self._rpc({
                                    model: 'maintenance_management.server_state',
                                    method: 'get_ups_data',
                                    args: [self.all_data.ups_value, self.all_data.ups_value1, self.act_button]
                                }).then(function (data) {
                                    self.all_data.ups_output_rs_voltage = data[0]
                                    self.all_data.ups_output_st_voltage = data[1]
                                    self.all_data.ups_output_rt_voltage = data[2]
                                    self.all_data.ups_output_r_phase_voltage = data[3]
                                    self.all_data.ups_output_s_phase_voltage = data[4]
                                    self.all_data.ups_output_t_phase_voltage = data[5]
                                    self.all_data.ups_output_r_phase_current = data[6]
                                    self.all_data.ups_output_s_phase_current = data[7]
                                    self.all_data.t_phase_current_output_from_ups = data[8]
                                    self.all_data.ups_output_frequency = data[9]
                                    self.all_data.ups_battery_current = data[10]
                                    self.all_data.ups_battery_voltage = data[11]
                                    self.all_data.ups_rectifier_input_uv_voltage = data[12]
                                    self.all_data.the_ups_rectifier_inputs_vw_voltage = data[13]
                                    self.all_data.ups_rectifier_input_uw_voltage = data[14]
                                    self.all_data.ups_rectifier_input_u_phase_current = data[15]
                                    self.all_data.ups_rectifier_input_v_phase_current = data[16]
                                    self.all_data.ups_rectifier_input_w_phase_current = data[17]
                                    self.all_data.ups_rectifier_input_frequency = data[18]
                                    self.all_data.ups_inverter_r_temperature = data[19]
                                    self.all_data.ups_inverter_s_temperature = data[20]
                                    self.all_data.temperature_of_ups_inverter_t = data[21]
                                    self.all_data.ups_rectifier_temperature = data[22]
                                    self.all_data.ups_ambient_temperature = data[23]
                                    self.all_data.ups_date = data[24]
                                })
                            },

                            //ups旁路搜索按钮
                            search_data_ups_side(data) {
                                self._rpc({
                                    model: 'maintenance_management.server_state',
                                    method: 'get_ups_side_data',
                                    args: [self.all_data.ups_side_value, self.all_data.ups_side_value1,
                                        self.act_button]
                                }).then(function (data) {
                                    self.all_data.ups_side_rs = data[0]
                                    self.all_data.ups_side_st = data[1]
                                    self.all_data.ups_side_rt = data[2]
                                    self.all_data.ups_side_r = data[3]
                                    self.all_data.ups_side_s = data[4]
                                    self.all_data.ups_side_t = data[5]
                                    self.all_data.ups_side_frequency = data[6]
                                    self.all_data.ups_side_date = data[7]
                                })
                            },

                            dashboard1: function () {
                                var dashboard1 = echarts.init(document.getElementById('dashboard1'));
                                var option1 = {
                                    title: {
                                        textStyle: {
                                            color: '#0ac4f7'
                                        },
                                        text: '电池电压'

                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['电池电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.battery_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: '电池电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.battery_voltage
                                        },
                                    ]
                                };
                                dashboard1.setOption(option1);
                            },
                            dashboard2: function () {
                                var dashboard2 = echarts.init(document.getElementById('dashboard2'));
                                var option2 = {
                                    title: {
                                        text: '电池内阻',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['电池内阻']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.battery_date,
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
                                        name: 'Ω',
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
                                    series: [
                                        {
                                            name: '电池内阻',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.battery_internal_resistance
                                        },
                                    ]
                                };
                                dashboard2.setOption(option2);
                            },
                            dashboard3: function () {
                                var dashboard3 = echarts.init(document.getElementById('dashboard3'));
                                var option3 = {
                                    title: {
                                        text: '电池温度',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['电池温度']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.battery_date,
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
                                        name: '℃',
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
                                    series: [
                                        {
                                            name: '电池温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.battery_temperature
                                        },
                                    ]
                                };
                                dashboard3.setOption(option3);
                            },
                            ups_side_1: function () {
                                var ups_side_1 = echarts.init(document.getElementById('ups_side_1'));
                                var ups_side_option_1 = {
                                    title: {
                                        text: 'UPS旁路输入RS电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入RS电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: "时间",
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入RS电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_rs
                                        },
                                    ]
                                };
                                ups_side_1.setOption(ups_side_option_1);
                            },
                            ups_side_2: function () {
                                var ups_side_2 = echarts.init(document.getElementById('ups_side_2'));
                                var ups_side_option_2 = {
                                    title: {
                                        text: 'UPS旁路输入ST电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入ST电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入ST电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_st
                                        },
                                    ]
                                };
                                ups_side_2.setOption(ups_side_option_2);
                            },
                            ups_side_3: function () {
                                var ups_side_3 = echarts.init(document.getElementById('ups_side_3'));
                                var ups_side_option_3 = {
                                    title: {
                                        text: 'UPS旁路输入RT电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入RT电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入RT电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_rt
                                        },
                                    ]
                                };
                                ups_side_3.setOption(ups_side_option_3);
                            },
                            ups_side_4: function () {
                                var ups_side_4 = echarts.init(document.getElementById('ups_side_4'));
                                var ups_side_option_4 = {
                                    title: {
                                        text: 'UPS旁路输入R相电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入R相电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入R相电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_r
                                        },
                                    ]
                                };
                                ups_side_4.setOption(ups_side_option_4);
                            },
                            ups_side_5: function () {
                                var ups_side_5 = echarts.init(document.getElementById('ups_side_5'));
                                var ups_side_option_5 = {
                                    title: {
                                        text: 'UPS旁路输入S相电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入S相电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入S相电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_s
                                        },
                                    ]
                                };
                                ups_side_5.setOption(ups_side_option_5);
                            },
                            ups_side_6: function () {
                                var ups_side_6 = echarts.init(document.getElementById('ups_side_6'));
                                var ups_side_option_6 = {
                                    title: {
                                        text: 'UPS旁路输入T相电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入T相电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入频率',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_t
                                        },
                                    ]
                                };
                                ups_side_6.setOption(ups_side_option_6);
                            },
                            ups_side_7: function () {
                                var ups_side_7 = echarts.init(document.getElementById('ups_side_7'));
                                var ups_side_option_7 = {
                                    title: {
                                        text: 'UPS旁路输入频率',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS旁路输入频率']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_side_date,
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
                                        name: '频率',
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
                                    series: [
                                        {
                                            name: 'UPS旁路输入频率',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_side_frequency
                                        },
                                    ]
                                };
                                ups_side_7.setOption(ups_side_option_7);
                            },
                            ups_1: function () {
                                var ups_1 = echarts.init(document.getElementById('ups_1'));
                                var ups_option_1 = {
                                    title: {
                                        text: 'UPS输出电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS输出RS电压', 'UPS输出ST电压', 'UPS输出RT电压', 'UPS输出R相电压',
                                            'UPS输出S相电压', 'UPS输出T相电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS输出RS电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_rs_voltage
                                        },
                                        {
                                            name: 'UPS输出ST电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_st_voltage
                                        },
                                        {
                                            name: 'UPS输出RT电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_rt_voltage
                                        },
                                        {
                                            name: 'UPS输出R相电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_r_phase_voltage
                                        },
                                        {
                                            name: 'UPS输出S相电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_s_phase_voltage
                                        },
                                        {
                                            name: 'UPS输出T相电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_t_phase_voltage
                                        },
                                    ]
                                };
                                ups_1.setOption(ups_option_1);
                            },
                            ups_2: function () {
                                var ups_2 = echarts.init(document.getElementById('ups_2'));
                                var ups_option_2 = {
                                    title: {
                                        text: 'UPS输出电流',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS输出R相电流', 'UPS输出S相电流', 'UPS输出T相电流']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'A',
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
                                    series: [
                                        {
                                            name: 'UPS输出R相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_r_phase_current
                                        },
                                        {
                                            name: 'UPS输出S相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_s_phase_current
                                        },
                                        {
                                            name: 'UPS输出T相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.t_phase_current_output_from_ups
                                        },
                                    ]
                                };
                                ups_2.setOption(ups_option_2);
                            },
                            ups_3: function () {
                                var ups_3 = echarts.init(document.getElementById('ups_3'));
                                var ups_option_3 = {
                                    title: {
                                        text: 'UPS输出频率',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS输出频率']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: '频率',
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
                                    series: [
                                        {
                                            name: 'UPS输出频率',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_output_frequency
                                        },
                                    ]
                                };
                                ups_3.setOption(ups_option_3);
                            },
                            ups_4: function () {
                                var ups_4 = echarts.init(document.getElementById('ups_4'));
                                var ups_option_4 = {
                                    title: {
                                        text: 'UPS电池电流',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS电池电流']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'A',
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
                                    series: [
                                        {
                                            name: 'UPS电池电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_battery_current
                                        },
                                    ]
                                };
                                ups_4.setOption(ups_option_4);
                            },
                            ups_5: function () {
                                var ups_5 = echarts.init(document.getElementById('ups_5'));
                                var ups_option_5 = {
                                    title: {
                                        text: 'UPS电池电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS电池电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS电池电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_battery_voltage
                                        },
                                    ]
                                };
                                ups_5.setOption(ups_option_5);
                            },
                            ups_6: function () {
                                var ups_6 = echarts.init(document.getElementById('ups_6'));
                                var ups_option_6 = {
                                    title: {
                                        text: 'UPS整流器输入电压',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS整流器输入UV电压', 'UPS整流器输入VW电压', 'UPS整流器输入UW电压']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS整流器输入UV电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_uv_voltage
                                        }, {
                                            name: 'UPS整流器输入VW电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.the_ups_rectifier_inputs_vw_voltage
                                        }, {
                                            name: 'UPS整流器输入UW电压',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_uw_voltage
                                        },
                                    ]
                                };
                                ups_6.setOption(ups_option_6);
                            },
                            ups_7: function () {
                                var ups_7 = echarts.init(document.getElementById('ups_7'));
                                var ups_option_7 = {
                                    title: {
                                        text: 'UPS整流器输入电流',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS整流器输入U相电流', 'UPS整流器输入V相电流', 'UPS整流器输入W相电流']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: 'V',
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
                                    series: [
                                        {
                                            name: 'UPS整流器输入U相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_u_phase_current
                                        }, {
                                            name: 'UPS整流器输入V相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_v_phase_current
                                        }, {
                                            name: 'UPS整流器输入W相电流',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_w_phase_current
                                        },
                                    ]
                                };
                                ups_7.setOption(ups_option_7);
                            },
                            ups_8: function () {
                                var ups_8 = echarts.init(document.getElementById('ups_8'));
                                var ups_option_8 = {
                                    title: {
                                        text: 'UPS整流器输入频率',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS整流器输入频率']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: '频率',
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
                                    series: [
                                        {
                                            name: 'UPS整流器输入频率',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_input_frequency
                                        }
                                    ]
                                };
                                ups_8.setOption(ups_option_8);
                            },
                            ups_9: function () {
                                var ups_9 = echarts.init(document.getElementById('ups_9'));
                                var ups_option_9 = {
                                    title: {
                                        text: 'UPS温度',
                                        textStyle: {
                                            color: '#0ac4f7'
                                        }
                                    },
                                    tooltip: {
                                        trigger: 'axis'
                                    },
                                    legend: {
                                        data: ['UPS逆变器R温度', 'UPS逆变器S温度', 'UPS逆变器T温度', 'UPS整流器温度', 'UPS环境温度']
                                    },
                                    grid: {
                                        left: '3%',
                                        right: '4%',
                                        bottom: '3%',
                                        containLabel: true
                                    },
                                    toolbox: {
                                        feature: {
                                            saveAsImage: {}
                                        }
                                    },
                                    xAxis: {
                                        name: '时间',
                                        type: 'category',
                                        boundaryGap: false,
                                        data: self.all_data.ups_date,
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
                                        name: '℃',
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
                                    series: [
                                        {
                                            name: 'UPS逆变器R温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_inverter_r_temperature
                                        }, {
                                            name: 'UPS逆变器S温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_inverter_s_temperature
                                        }, {
                                            name: 'UPS逆变器T温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.temperature_of_ups_inverter_t
                                        }, {
                                            name: 'UPS整流器温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_rectifier_temperature
                                        }, {
                                            name: 'UPS环境温度',
                                            type: 'line',
                                            stack: '总量',
                                            data: self.all_data.ups_ambient_temperature
                                        }
                                    ]
                                };
                                ups_9.setOption(ups_option_9);
                            },
                        },

                        mounted: function () {
                            this.$nextTick(function () {
                                this.dashboard1()
                                this.dashboard2()
                                this.dashboard3()
                            })
                        }
                    });
                });
            })
        },
        destroy: function () {
            this.zabbix_judge = false
        }
    })

    core.action_registry.add('battery_status', battery_status);
    return {battery_status: battery_status}
});

