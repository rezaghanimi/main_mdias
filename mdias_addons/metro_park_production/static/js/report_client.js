odoo.define('report_client', function(require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var report_client = AbstractAction.extend({
        template: 'report_client',
        MODEL_NAME: 'metro_park_production.statistics_report',
        REFRESH_FREQUENCY: 60 * 60 * 1000,
        init: function(parent, action, options) {
            this._super.apply(this, arguments)
        },
        start: function() {
            var self = this
            document.title = "BI看板"
            self._rpc({
                model: 'metro_park_production.statistics_report',
                method: 'echart_report',
                args: [self.id]
            }).then(function(data) {
                setTimeout(function() {
                    var myChart14 = self.$el.find('#chart14')[0]
                    self.Chart14 = echarts.init(myChart14, 'light')
                    self.Chart14.setOption({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                lineStyle: {
                                    color: 'white'
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

                            axisTick: {
                                alignWithLabel: true
                            },
                            type: 'category',
                            data: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00']
                        },
                        dataZoom: [{
                            fillerColor: 'rgba(0,130,200,0.3)',
                            realtime: false,
                            dataBackground: {
                                areaStyle: {
                                    color: 'blue'
                                }
                            },
                            borderColor: '#0ac4f7',
                            type: 'slider',
                            show: true,
                            xAxisIndex: 0,
                            textStyle: {
                                color: '#0ac4f7'
                            }
                        }],
                        yAxis: {
                            name: '计划数量',
                            nameLocation: 'center',
                            nameGap: 30,
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
                            type: 'value'
                        },
                        series: data.series_14
                    });
                    var myChart10 = self.$el.find('#chart10')[0]
                    self.Chart10 = echarts.init(myChart10, 'light')
                    var myChart9 = self.$el.find('#chart9')[0]
                    self.Chart9 = echarts.init(myChart9, 'light')

                    var myChart5 = self.$el.find('#chart5')[0]
                    self.Chart5 = echarts.init(myChart5, 'light')

                    var myChart3 = self.$el.find('#chart3')[0]
                    self.Chart3 = echarts.init(myChart3, 'light')
                    self.Chart10.setOption({
                        grid: {
                            left: '3%',
                            right: '4%',
                            bottom: '3%',
                            containLabel: true
                        },
                        xAxis: {
                            axisLabel: {
                                color: '#0ac4f7',
                                interval: 0,
                                rotate: 30,
                            },
                            axisLine: {
                                lineStyle: {
                                    color: '#0ac4f7'
                                }
                            },
                            axisTick: {
                                alignWithLabel: true
                            },
                            type: 'category',
                            data: data.department_data
                        },
                        yAxis: {
                            name: '时间使用率',
                            nameLocation: 'center',
                            nameGap: 30,
                            axisLabel: {
                                color: '#0ac4f7'
                            },
                            minInterval: 1,
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
                            type: 'value'
                        },
                        series: [{
                            label: {
                                show: true,
                                position: 'top'
                            },
                            areaStyle: {
                                color: {
                                    type: 'linear',
                                    x: 0,
                                    y: 0,
                                    x2: 0,
                                    y2: 1,
                                    colorStops: [{
                                        offset: 0,
                                        color: '#0077f7' // 0% 处的颜色
                                    }, {
                                        offset: 1,
                                        color: '#0ac4f7' // 100% 处的颜色
                                    }]
                                }
                            },
                            itemStyle: {
                                color: '#0ea2e2'
                            },
                            barCategoryGap: '70%',
                            data: data.data_10,
                            type: 'line'
                        }]
                    })
                    self.Chart9.setOption({
                        legend: {
                            type: 'scroll',
                            orient: 'vertical',
                            right: 10,
                            top: 'middle',
                            bottom: 20,
                            textStyle: {
                                color: 'white'
                            },
                            data: data.department_data
                        },
                        series: [{
                            legendHoverLink: false,
                            name: '访问来源',
                            type: 'pie',
                            radius: ['50%', '70%'],
                            avoidLabelOverlap: false,
                            label: {

                                show: false,
                                formatter: "{b}\n{d}%",
                                position: 'center',

                                emphasis: {
                                    show: true,
                                    textStyle: {
                                        fontSize: '30',
                                        fontWeight: 'bold'
                                    }
                                }
                            },

                            data: [{
                                    value: data.data_9.value1,
                                    name: data.department_data[0]
                                },
                                {
                                    value: data.data_9.value2,
                                    name: data.department_data[1]
                                },
                                {
                                    value: data.data_9.value3,
                                    name: data.department_data[2]
                                },
                                {
                                    value: data.data_9.value4,
                                    name: data.department_data[3]
                                },
                                {
                                    value: data.data_9.value5,
                                    name: data.department_data[4]
                                },
                                {
                                    value: data.data_9.value6,
                                    name: data.department_data[5]
                                },
                                {
                                    value: data.data_9.value7,
                                    name: data.department_data[6]
                                },
                                {
                                    value: data.data_9.value8,
                                    name: data.department_data[7]
                                },

                            ]
                        }]
                    })
                    self.Chart9.on('mouseover', function(params) {
                        if (params.name != data.department_data[0]) {
                            self.Chart9.dispatchAction({
                                type: 'downplay',
                                name: data.department_data[0]
                            })
                        }

                    })
                    self.Chart9.dispatchAction({
                        type: 'highlight',
                        name: data.department_data[0]
                    });
                    self.Chart5.setOption({
                        grid: {
                            right: 100,
                        },
                        legend: {
                            type: 'scroll',
                            orient: 'vertical',
                            right: 10,
                            top: 'middle',
                            bottom: 20,
                            textStyle: {
                                color: 'white'
                            },
                            data: ['A', 'B', 'C']
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
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
                            axisTick: {
                                alignWithLabel: true
                            },
                            type: 'category',
                            data: ['一车间', '二车间', '三车间', ]
                        },
                        yAxis: {
                            name: '计划类型&计划数量',
                            nameLocation: 'center',
                            nameGap: 30,
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
                            type: 'value'
                        },
                        series: [{
                                name: 'A',
                                type: 'bar',
                                barCategoryGap: '20%',
                                label: {
                                    show: true,
                                    position: 'top'
                                },
                                data: data.series_5.data1
                            },
                            {
                                name: 'B',
                                type: 'bar',
                                barCategoryGap: '20%',
                                label: {
                                    show: true,
                                    position: 'top'
                                },
                                data: data.series_5.data2
                            },
                            {
                                name: 'C',
                                type: 'bar',
                                barCategoryGap: '20%',
                                label: {
                                    show: true,
                                    position: 'top'
                                },
                                data: data.series_5.data3
                            }
                        ]
                    });
                    self.Chart3.setOption({
                        grid: {
                            right: 100,
                        },
                        legend: {
                            type: 'scroll',
                            orient: 'vertical',
                            right: 10,
                            top: 'middle',
                            bottom: 20,
                            textStyle: {
                                color: 'white'
                            },
                            data: data.repair_process
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'shadow'
                            }
                        },
                        xAxis: {
                            axisLabel: {
                                color: '#0ac4f7',
                                rotate: 30,
                                interval: 0
                            },
                            axisLine: {
                                lineStyle: {
                                    color: '#0ac4f7'
                                }
                            },
                            axisTick: {
                                alignWithLabel: true
                            },
                            type: 'category',
                            data: data.repair_team
                        },
                        yAxis: {
                            name: '修程&计划数量',
                            nameLocation: 'center',
                            nameGap: 30,
                            minInterval: 1,
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
                            type: 'value'
                        },
                        series: data.data_3.series
                    })
                    window.onresize = function(e) {
                        let i = 1
                        while (i <= 15) {
                            if (self.hasOwnProperty('Chart' + i)){
                                self['Chart' + i].resize()
                            }
                            i++
                        }
                    }
                }, 300)
            })
            document.title = "BI看板";
            setTimeout(function() {
                self._init_chat()
            });
            return self._super.apply(this, arguments)
        },
        _init_chat: function() {
            var self = this;
            self._init_dispatch_train_production_indicator();
            self._init_dispatch_class_task_perform_state();
            self._init_dispatch_phase_work_demand();
            self._init_repair_schedule_equilibrium_statistics();
            self._init_construction_department_finished_and_unfinished();
            self._init_construction_plan_type_num();
            self._init_dispatch_train_time_distribute();
            self._init_construction_area_top();
            self._init_train_use_condition();
        },
        _call_statistics_rpc: function(method_name, callback) {
            var self = this;
            var call = function() {
                self._rpc({
                    model: self.MODEL_NAME,
                    method: method_name,
                    args: [],
                    kwargs: {}
                }).then(function(data) {
                    callback(data)
                });
            };
            setInterval(call, self.REFRESH_FREQUENCY)
            call();
        },
        _init_dispatch_train_time_distribute: function() {
            var self = this;
            var myChart13 = self.$el.find('#chart13')[0]
            self.Chart13 = echarts.init(myChart13, 'light');
            this._call_statistics_rpc('request_dispatch_cmds', function(data) {
                self.Chart13.setOption({
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            lineStyle: {
                                color: 'white'
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

                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data.xtime
                    },
                    dataZoom: [{
                        fillerColor: 'rgba(0,130,200,0.3)',
                        realtime: false,
                        dataBackground: {
                            areaStyle: {
                                color: 'blue'
                            }
                        },
                        borderColor: '#0ac4f7',
                        type: 'slider',
                        show: true,
                        xAxisIndex: 0,
                        textStyle: {
                            color: '#0ac4f7'
                        }
                    }],
                    yAxis: {
                        name: '计划数量',
                        nameLocation: 'center',
                        nameGap: 30,
                        axisLabel: {
                            color: '#0ac4f7'
                        },
                        minInterval: 1,
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
                        type: 'value'
                    },
                    series: [{
                        label: {
                            show: true,
                            position: 'top'
                        },
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0,
                                    color: '#0077f7' // 0% 处的颜色
                                }, {
                                    offset: 1,
                                    color: '#0ac4f7' // 100% 处的颜色
                                }]
                            }
                        },
                        itemStyle: {
                            color: '#0ea2e2'
                        },
                        barCategoryGap: '70%',
                        data: data.data,
                        type: 'line'
                    }]
                });
            });
        },
        _init_dispatch_train_production_indicator: function() {
            var self = this;
            var myChart12 = self.$el.find('#chart12')[0]
            self.Chart12 = echarts.init(myChart12, 'light');
            this._call_statistics_rpc('dispatch_train_production_indicator', function(data) {
                self.Chart12.setOption({
                    series: [{
                        center: ["20%", "50%"],
                        hoverAnimation: false,
                        startAngle: 270,
                        legendHoverLink: false,
                        name: '访问来源',
                        type: 'pie',
                        radius: ['40%', '50%'],
                        avoidLabelOverlap: false,
                        label: {
                            fontSize: 18,
                            formatter: params => {
                                if (params.name === 'off') {
                                    return ''
                                }
                                return '发车计划完成率' + '\n' + params.percent + '%'
                            },
                            position: 'center',
                        },
                        data: [{
                                value: data.train_out_percent,
                                name: '发车计划完成率'
                            },
                            {
                                itemStyle: {
                                    color: 'gray'
                                },
                                value: 1 - data.train_out_percent,
                                name: 'off'
                            }
                        ]
                    }, {
                        center: ["48%", "50%"],
                        hoverAnimation: false,
                        startAngle: 270,
                        legendHoverLink: false,
                        name: '访问来源',
                        type: 'pie',
                        radius: ['40%', '50%'],
                        avoidLabelOverlap: false,
                        label: {
                            fontSize: 18,
                            formatter: params => {
                                if (params.name === 'off') {
                                    return ''
                                }
                                return '收车计划完成率' + '\n' + params.percent + '%'
                            },
                            position: 'center',
                        },
                        data: [{
                                value: data.train_back_percent,
                                name: '收车计划完成率'
                            },
                            {
                                itemStyle: {
                                    color: 'gray'
                                },
                                value: 1 - data.train_back_percent,
                                name: 'off'
                            }
                        ]
                    }, {
                        center: ["77%", "50%"],
                        hoverAnimation: false,
                        startAngle: 270,
                        legendHoverLink: false,
                        name: '访问来源',
                        type: 'pie',
                        radius: ['40%', '50%'],
                        avoidLabelOverlap: false,
                        label: {
                            fontSize: 18,
                            formatter: params => {
                                if (params.name === 'off') {
                                    return ''
                                }
                                return '调车完成率' + '\n' + params.percent + '%'
                            },
                            position: 'center',
                        },
                        data: [{
                                value: data.dispatch_percent,
                                name: '调车完成率'
                            },
                            {
                                itemStyle: {
                                    color: 'gray'
                                },
                                value: 1 - data.dispatch_percent,
                                name: 'off'
                            }
                        ]
                    }]
                })
            });
        },

        _init_construction_department_finished_and_unfinished: function() {
            var self = this;
            var myChart11 = self.$el.find('#chart11')[0]
            self.Chart11 = echarts.init(myChart11, 'light')
            this._call_statistics_rpc('construction_department_finished_and_unfinished', function(data) {
                self.Chart11.setOption({
                    grid: {
                        right: 100,
                    },

                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    yAxis: {
                        axisLabel: {
                            color: '#0ac4f7',
                            rotate: 40,
                            interval: 0,
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data.department_data,

                    },
                    xAxis: {
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
                        type: 'value'
                    },
                    series: [{
                        name: '已完成',
                        type: 'bar',
                        barCategoryGap: '70%',
                        stack: '总量',
                        label: {
                            normal: {
                                show: true,
                                position: 'inside'
                            }
                        },
                        data: data.finished_data
                    }]
                });
            });
        },
        _init_construction_plan_type_num: function() {
            var self = this;
            var myChart6 = self.$el.find('#chart6')[0]
            self.Chart6 = echarts.init(myChart6, 'light')
            this._call_statistics_rpc('construction_plan_type_num', function(data) {
                self.Chart6.setOption({
                    grid: {
                        left: '3%',
                        right: '4%',
                        bottom: '3%',
                        containLabel: true
                    },

                    legend: {

                        bottom: 1,
                        textStyle: {
                            color: 'white'
                        },
                        data: ['月计划', '周计划', '日计划', '临补计划']
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'shadow'
                        }
                    },
                    xAxis: {
                        axisLabel: {
                            color: '#0ac4f7',
                            interval: 0,
                            rotate: 30,

                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data.department_names
                    },
                    yAxis: {
                        name: '各部门计划类型数量',
                        nameLocation: 'center',
                        nameGap: 30,
                        minInterval: 1,
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
                        type: 'value'
                    },
                    series: [{
                            name: '月计划',
                            type: 'bar',
                            barCategoryGap: '20%',
                            label: {
                                show: true,
                                position: 'top'
                            },
                            data: data.monthly_data
                        },
                        {
                            name: '周计划',
                            type: 'bar',
                            barCategoryGap: '20%',
                            label: {
                                show: true,
                                position: 'top'
                            },
                            data: data.weekly_data
                        },
                        {
                            name: '日计划',
                            type: 'bar',
                            barCategoryGap: '20%',
                            label: {
                                show: true,
                                position: 'top'
                            },
                            data: data.day_data
                        },
                        {
                            name: '临补计划',
                            type: 'bar',
                            barCategoryGap: '20%',
                            label: {
                                show: true,
                                position: 'top'
                            },
                            data: data.temp_data
                        },
                    ]
                })
            });
        },
        _init_construction_area_top: function() {
            var self = this;
            var myChart7 = self.$el.find('#chart7')[0]
            self.Chart7 = echarts.init(myChart7, 'light')
            this._call_statistics_rpc('construction_area_top', function(data) {
                self.Chart7.setOption({
                    xAxis: {
                        axisLabel: {
                            interval: 0,
                            rotate: 30,
                            color: '#0ac4f7'
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data.xaixs
                    },
                    yAxis: {
                        name: '作业次数',
                        nameLocation: 'center',
                        nameGap: 30,
                        minInterval: 1,
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
                        type: 'value'
                    },
                    series: [{
                        label: {
                            show: true,
                            position: 'top'
                        },
                        itemStyle: {
                            color: '#0ea2e2'
                        },
                        barCategoryGap: '70%',
                        data: data.data,
                        type: 'bar'
                    }]
                });
            });
        },
        _init_train_use_condition: function() {
            var self = this;
            var myChart8 = self.$el.find('#chart8')[0]
            self.Chart8 = echarts.init(myChart8, 'light')
            this._call_statistics_rpc('train_use_condition', function(data) {
                self.Chart8.setOption({
                    legend: {
                        x: 'center',
                        left: 10,
                        orient: 'vertical',
                        top: 20,
                        data: ['故障', '检修', '用车'],
                        textStyle: {
                            color: '#FFFFFF'
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },

                    series: [{
                        name: '用车情况',
                        type: 'pie',
                        center: ['50%', '55%'],
                        label: {
                            normal: {
                                show: true,
                                formatter: "{b}:{d}%",
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        lableLine: {
                            normal: {
                                show: true
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data: data.data

                    }]
                })
            });

        },

        _init_dispatch_class_task_perform_state: function() {
            var self = this;
            var myChart4 = self.$el.find('#chart4')[0]
            self.Chart4 = echarts.init(myChart4, 'light')
            this._call_statistics_rpc('class_task_perform_state', function(data) {
                self.Chart4.setOption({
                    xAxis: {
                        axisLabel: {
                            interval: 0,
                            rotate: 30,
                            color: '#0ac4f7'
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data[1]
                    },
                    yAxis: {
                        name: '任务数量',
                        nameLocation: 'center',
                        nameGap: 30,
                        minInterval: 1,
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
                        type: 'value',
                    },
                    series: [{
                        label: {
                            show: true,
                            position: 'top'
                        },
                        itemStyle: {
                            color: '#0ea2e2'
                        },
                        barCategoryGap: '70%',
                        data: data[0],
                        type: 'bar'
                    }]
                })
            });
        },
        _init_dispatch_phase_work_demand: function() {
            var self = this;
            var myChart1 = self.$el.find('#chart1')[0]
            self.Chart1 = echarts.init(myChart1, 'light')
            this._call_statistics_rpc('phase_work_demand', function(data) {
                self.Chart1.setOption({
                    xAxis: {
                        axisLabel: {
                            color: '#0ac4f7'
                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data[1],

                    },
                    yAxis: {
                        name: '计划数量',
                        nameLocation: 'center',
                        nameGap: 30,
                        axisLabel: {
                            color: '#0ac4f7'
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        minInterval: 1,
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        type: 'value'
                    },
                    series: [{
                        label: {
                            show: true,
                            position: 'top'
                        },
                        itemStyle: {
                            color: '#0ea2e2'
                        },
                        barCategoryGap: '70%',
                        data: data[0],
                        type: 'bar'
                    }]
                })
            });
        },
        _init_repair_schedule_equilibrium_statistics: function() {
            var self = this;
            var myChart2 = self.$el.find('#chart2')[0]
            self.Chart2 = echarts.init(myChart2, 'light')
            this._call_statistics_rpc('repair_schedule_equilibrium_statistics', function(data) {

                self.Chart2.setOption({
                    xAxis: {
                        axisLabel: {
                            color: '#0ac4f7',
                            interval: 0,
                            rotate: 30,

                        },
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        axisTick: {
                            alignWithLabel: true
                        },
                        type: 'category',
                        data: data[0],

                    },
                    yAxis: {
                        name: '修程均衡数量',
                        nameLocation: 'center',
                        nameGap: 30,
                        axisLabel: {
                            color: '#0ac4f7'
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        minInterval: 1,
                        axisLine: {
                            lineStyle: {
                                color: '#0ac4f7'
                            }
                        },
                        type: 'value'
                    },
                    series: [{
                        label: {
                            show: true,
                            position: 'top'
                        },
                        itemStyle: {
                            color: '#0ea2e2'
                        },
                        barCategoryGap: '70%',
                        data: data[1],
                        type: 'bar'
                    }]
                })
            });
        }
    });
    core.action_registry.add('report_client', report_client);
    return { 'report_client': report_client };


});
