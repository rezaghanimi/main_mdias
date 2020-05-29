/**
 * Created by artorias on 2019/8/16.
 */
odoo.define('statistical_report_client', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var statistical_report_client = AbstractAction.extend({
        init: function () {
            this._super.apply(this, arguments);
            document.title = 'BI看板'
            this.vue_data = {
                browse_vehicle_maintenance_plan: false,  // 能浏览车辆检修计划统计图表
                browse_construction_tasks: false,  // 能浏施工任务统计图表
                browse_scheduling_plan: false,  // 能浏览调度计划统计图表
                pickerOptions: {
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 8);
                            start.setTime(end.getTime() - 3600 * 1000 * 24 * 6);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 8);
                            start.setTime(end.getTime() - 3600 * 1000 * 24 * 30);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            end.setTime(end.getTime() + 3600 * 1000 * 8);
                            start.setTime(end.getTime() - 3600 * 1000 * 24 * 90);
                            picker.$emit('pick', [start, end]);
                        }
                    }]
                },
                value1: '',
                value2: [new Date(), new Date()],
                activeName: 'first',
                myChartData: [0, 0, 0, 0],
                quota: {'dispatch': [0, 0], 'receive': [0, 0], 'send': [0, 0]},
                car_trend: {'date': [], 'receive': [], 'send': [], 'route': []},
                myChart1: null,
                myChart1Data: [
                    {'登顶1': 123},
                    {'登顶2': 123},
                    {'登顶3': 123}
                ],
                myChart12: null,
                myCharts12: null,
                myChartss12: null,
                myCharts14: null,
                myCharts14Data: [
                    {
                        name: '调车勾计划',
                        data: [{
                            key: '10:00',
                            value: 120
                        }, {
                            key: '11:00',
                            value: 120
                        }, {
                            key: '12:00',
                            value: 120
                        }, {
                            key: '13:00',
                            value: 66
                        }, {
                            key: '14:00',
                            value: 66
                        }, {
                            key: '15:00',
                            value: 3
                        }]
                    }
                ],
                myChart14: null,
                myChart14Data: [
                    {
                        name: '收车量',
                        data: [{
                            key: '10:00',
                            value: 120
                        }, {
                            key: '11:00',
                            value: 0
                        }]
                    },
                    {
                        name: '发车量',
                        data: [{
                            key: '10:00',
                            value: 120
                        }, {
                            key: '11:00',
                            value: 120
                        }, {
                            key: '12:00',
                            value: 120
                        }, {
                            key: '13:00',
                            value: 66
                        }, {
                            key: '14:00',
                            value: 120
                        }, {
                            key: '15:00',
                            value: 120
                        }]
                    }
                ],
                myChart7: null,
                myChart7Data: [{
                    value: 335,
                    name: '机电一部'
                },
                    {
                        value: 310,
                        name: '机电二部'
                    },
                    {
                        value: 234,
                        name: '机电三部'
                    },
                    {
                        value: 135,
                        name: '机电四部'
                    },
                    {
                        value: 234,
                        name: '机电三1部'
                    },
                    {
                        value: 135,
                        name: '机电四2部'
                    },
                    {
                        value: 1548,
                        name: '机电5部'
                    }
                ],
                charts1: null,
                charts1Data: {
                    '检修一班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                    '检修二班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                    '检修三班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                },
                myChart11: null,
                myChart11Data: {
                    '检修一班': {
                        '完成': 123,
                        '未完成': 123
                    },
                    '检修二班': {
                        '完成': 123,
                        '未完成': 123
                    },
                    '检修三班': {
                        '完成': 123,
                        '未完成': 123
                    },
                },
                myCharts6: null,
                myCharts6Data: {
                    '检修一班': {
                        'A': 123,
                        'B': 123,
                        'C': 123
                    },
                    '检修二班': {
                        'A': 123,
                        'B': 123,
                        'C': 123
                    },
                    '检修三班': {
                        'A': 123,
                        'B': 123,
                        'C': 123
                    },
                },
                myChart6: null,
                myChart6Data: {
                    '检修一班': {
                        '日补': 123,
                        '月补': 123,
                        '临补': 123
                    },
                    '检修二班': {
                        '日补': 123,
                        '月补': 123,
                        '临补': 123
                    },
                    '检修三班': {
                        '日补': 123,
                        '月补': 123,
                        '临补': 123
                    },
                },
                myChart8: null,
                myChart8Data: [{
                    name: '兑现率',
                    value: [0],
                    maintance: ['无计划'],
                    label: {
                        show: true,
                        color: '#ffffff',
                        padding: 3,
                        borderRadius: 5,
                        backgroundColor: '#069cd1'
                    }
                }],
                myChart4: null,
                myChart4Data: {
                    '检修一班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                    '检修二班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                    '检修三班': {
                        '作废': 123,
                        '完成': 123,
                        '派工': 123,
                        '关闭': 123,
                        '待发布': 123
                    },
                },
                myChart10: null,
                myChart10Data: [{
                    value: 334,
                    name: '机电一部',
                    len: 12
                },
                    {
                        value: 310,
                        name: '机电二部'
                    },
                    {
                        value: 234,
                        name: '机电三部'
                    },
                    {
                        value: 135,
                        name: '机电四部'
                    },
                    {
                        value: 234,
                        name: '机电三1部'
                    },
                    {
                        value: 135,
                        name: '机电四2部'
                    },
                    {
                        value: 1548,
                        name: '机电5部'
                    }
                ],

                myChart9: null,
                myChart9Data: [{
                    value: 335,
                    name: '机电一部'
                },
                    {
                        value: 310,
                        name: '机电二部'
                    },
                    {
                        value: 234,
                        name: '机电三部'
                    },
                    {
                        value: 135,
                        name: '机电四部'
                    },
                    {
                        value: 234,
                        name: '机电三1部'
                    },
                    {
                        value: 135,
                        name: '机电四2部'
                    },
                    {
                        value: 1048,
                        name: '机电5部'
                    }
                ],
                myChart2: null,
                myChart2Data: [
                    {'销售1': 2300},
                    {'销售2': 4300},
                    {'销售3': 24300},
                    {'销售4': 5300},
                    {'销售5': 14300},
                ],
            }
        },

        willStart: function () {
            var self = this;
            // 在这里取得数据并变更this.vue_data对应的数据, rpc的model或者method需变更

            self.get_data = function () {

                return self._rpc({
                    model: 'metro_park_production.report_data',
                    method: 'static_report',
                    kwargs: {'period': self.vue_data.value2}
                })
            }
            return $.when(self.get_data()).then(function (result1) {
                self.vue_data.myChart1Data = result1.myChart1Data
                self.vue_data.myChart2Data = result1.myChart2Data
                self.vue_data.myChart4Data = result1.myChart4Data
                self.vue_data.myChart6Data = result1.myChart6Data
                self.vue_data.myChart7Data = result1.myChart7Data
                self.vue_data.myChart9Data = result1.myChart9Data
                self.vue_data.myChart8Data[0]['value'] = result1.myChart8Data['value']
                self.vue_data.myChart8Data[0]['maintance'] = result1.myChart8Data['maintance']
                self.vue_data.myChart11Data = result1.myChart11Data
                self.vue_data.myChart10Data = result1.myChart10Data
                self.vue_data.charts1Data = result1.charts1Data
                self.vue_data.myCharts6Data = result1.myCharts6Data
                self.vue_data.myChartData = result1.myChartData
                self.vue_data.quota = result1.quota
                self.vue_data.car_trend = result1.car_trend
                self.vue_data.browse_vehicle_maintenance_plan = result1.table1
                self.vue_data.browse_construction_tasks = result1.table2
                self.vue_data.browse_scheduling_plan = result1.table3
            })
        },

        start: function () {
            var self = this;
            return self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_production', template_name: 'tem_statistical_report_client'}
            }).then(function (el) {
                self._replaceElement($(el))
            })
        },

        on_attach_callback: function () {
            var self = this;
            var app = new Vue({
                el: '#statistical_report_client_app',
                data: function () {
                    return self.vue_data
                },
                mounted() {
                    //初始化渲染第一屏
                    var next_func = function () {
                    };
                    if (this.browse_vehicle_maintenance_plan) {
                        this.activeName = 'first';
                        next_func = this.renderFirst
                    } else if (this.browse_construction_tasks) {
                        this.activeName = 'second';
                        next_func = this.renderSecond
                    } else if (this.browse_scheduling_plan) {
                        this.activeName = 'third';
                        next_func = this.renderThird
                    }
                    this.$nextTick(() => {
                        next_func()
                    })
                },
                methods: {
                    handleClick(tab, event) {
                        //tab切换好后才能渲染echart
                        if (tab.name == 'second') {
                            this.$nextTick(() => {
                                this.renderSecond()
                            })
                        }
                        if (tab.name == 'third') {
                            this.$nextTick(() => {
                                this.renderThird()
                            })
                        }
                    },
                    renderThird() {
                        this.myChart12 = echarts.init(document.querySelector('#chart12'), 'light')
                        this.myChart12.setOption({
                            series: [{
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
                                        if (params.name == 'off') {
                                            return ''
                                        }
                                        return '调车完成率' + '\n' + params.percent + '%'
                                    },
                                    position: 'center',
                                },
                                data: [{
                                    value: app.quota['dispatch'][0],
                                    name: '调车完成率'
                                },
                                    {
                                        itemStyle: {
                                            color: 'gray'
                                        },
                                        value: app.quota['dispatch'][1],
                                        name: 'off'
                                    }
                                ]
                            }]
                        })


                        this.myCharts12 = echarts.init(document.querySelector('#charts12'), 'light')
                        this.myCharts12.setOption({
                            series: [{
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
                                        if (params.name == 'off') {
                                            return ''
                                        }
                                        return '收车计划准点率' + '\n' + params.percent + '%'
                                    },
                                    position: 'center',
                                },
                                data: [{
                                    value: app.quota['receive'][0],
                                    name: '收车计划准点率'
                                },
                                    {
                                        itemStyle: {
                                            color: 'gray'
                                        },
                                        value: app.quota['receive'][1],
                                        name: 'off'
                                    }
                                ]
                            }]
                        })


                        this.myChartss12 = echarts.init(document.querySelector('#chartss12'), 'light')
                        this.myChartss12.setOption({
                            series: [{
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
                                        if (params.name == 'off') {
                                            return ''
                                        }
                                        return '发车计划准点率' + '\n' + params.percent + '%'
                                    },
                                    position: 'center',
                                },
                                data: [{
                                    value: app.quota['send'][0],
                                    name: '发车计划准点率'
                                },
                                    {
                                        itemStyle: {
                                            color: 'gray'
                                        },
                                        value: app.quota['send'][1],
                                        name: 'off'
                                    }
                                ]
                            }]
                        })


                        this.myChart14 = echarts.init(document.querySelector('#chart14'), 'light')
                        this.myChart14.setOption({
                            tooltip: {
                                trigger: 'axis',
                                position: function (pt) {
                                    return [pt[0], '10%'];
                                }
                            },
                            title: {
                                left: 'center',
                                text: '收/发车趋势图',
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
                                boundaryGap: false,
                                data: app.car_trend['date']
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
                                type: 'value',
                                boundaryGap: [0, '100%']
                            },
                            dataZoom: [{
                                type: 'inside',
                                start: 0,
                                end: 100
                            }, {
                                start: 0,
                                end: 100,

                            }],
                            series: [
                                {
                                    name: '收车量',
                                    type: 'line',
                                    smooth: true,
                                    symbol: 'none',
                                    sampling: 'average',
                                    itemStyle: {
                                        color: 'rgb(255, 210, 82)'
                                    },
                                    data: app.car_trend['receive']
                                },
                                {
                                    name: '发车量',
                                    type: 'line',
                                    smooth: true,
                                    symbol: 'none',
                                    sampling: 'average',
                                    itemStyle: {
                                        color: 'rgb(50, 153, 213)'
                                    },
                                    data: app.car_trend['send']
                                }
                            ]
                        })

                        this.myCharts14 = echarts.init(document.querySelector('#charts14'), 'light')
                        this.myCharts14.setOption({
                            tooltip: {
                                trigger: 'axis',
                                position: function (pt) {
                                    return [pt[0], '10%'];
                                }
                            },
                            title: {
                                left: 'center',
                                text: '调车钩计划数量分布',
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
                                boundaryGap: false,
                                data: app.car_trend['date']
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
                                type: 'value',
                                boundaryGap: [0, '100%']
                            },
                            dataZoom: [{
                                type: 'inside',
                                start: 0,
                                end: 100
                            }, {
                                start: 0,
                                end: 100,

                            }],
                            series: [
                                {
                                    name: '调车钩计划',
                                    type: 'line',
                                    smooth: true,
                                    symbol: 'none',
                                    sampling: 'average',
                                    itemStyle: {
                                        color: 'rgb(50, 153, 213)'
                                    },
                                    data: app.car_trend['route']
                                }
                            ]
                        })

                        var receive = document.getElementById('receive')
                        receive.innerHTML = app.myChartData[0]
                        var send = document.getElementById('send')
                        send.innerHTML = app.myChartData[1]
                        var dispatch_num = document.getElementById('dispatch_num')
                        dispatch_num.innerHTML = app.myChartData[2]
                        var route_num = document.getElementById('route_num')
                        route_num.innerHTML = app.myChartData[3]
                    },
                    renderSecond() {

                        this.myChart7 = echarts.init(document.querySelector('#chart7'), 'light')
                        this.myChart7.setOption({
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
                                data: this.myChart7Data.map(x => x.name)
                            },
                            yAxis: {
                                name: '计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                                data: this.myChart7Data.map(x => x.value),
                                type: 'bar'
                            }]
                        })


                        this.myCharts6 = echarts.init(document.querySelector('#charts6'), 'light')
                        this.myCharts6.setOption({
                            grid: {
                                right: 100,
                            },
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: Object.keys(this.myCharts6Data[Object.keys(this.myCharts6Data).shift()])
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
                                data: Object.keys(this.myCharts6Data)
                            },
                            yAxis: {
                                name: '计划类型&计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                            series: Object.keys(this.myCharts6Data[Object.keys(this.myCharts6Data).shift()]).map(name => {
                                return {
                                    name,
                                    type: 'bar',
                                    barCategoryGap: '70%',
                                    stack: '总量',
                                    label: {
                                        normal: {
                                            show: true,
                                            position: 'inside'
                                        }
                                    },
                                    data: Object.keys(this.myCharts6Data).map((series, i) => {
                                        return [i, this.myCharts6Data[series][name]]
                                    })
                                }

                            })
                        })


                        this.myChart10 = echarts.init(document.querySelector('#chart10'), 'light')
                        this.myChart10.setOption({
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
                                data: this.myChart10Data.map(x => x.name)
                            },
                            yAxis: {
                                name: '时间使用率',
                                nameLocation: 'center',
                                nameGap: 40,
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
                                data: this.myChart10Data.map(x => x.value),
                                type: 'line'
                            }]
                        })


                        this.myChart11 = echarts.init(document.querySelector('#chart11'), 'light')
                        this.myChart11.setOption({
                            grid: {
                                right: 100,
                            },
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: Object.keys(this.myChart11Data[Object.keys(this.myChart11Data).shift()])
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
                                data: Object.keys(this.myChart11Data)
                            },
                            yAxis: {
                                name: '完成情况&计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                            series: Object.keys(this.myChart11Data[Object.keys(this.myChart11Data).shift()]).map(name => {
                                return {
                                    name,
                                    type: 'bar',
                                    barCategoryGap: '70%',
                                    stack: '总量',
                                    label: {
                                        normal: {
                                            show: true,
                                            position: 'inside'
                                        }
                                    },
                                    data: Object.keys(this.myChart11Data).map((series, i) => {
                                        return [i, this.myChart11Data[series][name]]
                                    })
                                }

                            })
                        })


                        this.myChart6 = echarts.init(document.querySelector('#chart6'), 'light')
                        this.myChart6.setOption({
                            grid: {
                                right: 100,
                            },
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: Object.keys(this.myChart6Data[Object.keys(this.myChart6Data).shift()])
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
                                data: Object.keys(this.myChart6Data)
                            },
                            yAxis: {
                                name: '计划类型&计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                            series: Object.keys(this.myChart6Data[Object.keys(this.myChart6Data).shift()]).map(name => {
                                return {
                                    name,
                                    type: 'bar',
                                    barCategoryGap: '70%',
                                    stack: '总量',
                                    label: {
                                        normal: {
                                            show: true,
                                            position: 'inside'
                                        }
                                    },
                                    data: Object.keys(this.myChart6Data).map((series, i) => {
                                        return [i, this.myChart6Data[series][name]]
                                    })
                                }

                            })
                        })


                        this.myChart8 = echarts.init(document.querySelector('#chart8'), 'light')
                        let maxIndicate = 0
                        this.myChart8Data.map(x => {
                            x.value.map(y => {
                                if (maxIndicate < y) {
                                    maxIndicate = y
                                }
                            })
                        })
                        this.myChart8.setOption({
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: this.myChart8Data.map(x => x.name)
                            },
                            radar: {
                                axisLine: {
                                    lineStyle: {
                                        color: ['#206aa4']
                                    }
                                },
                                splitLine: {
                                    lineStyle: {
                                        color: ['#206aa4']
                                    }
                                },
                                splitArea: {
                                    areaStyle: {
                                        color: ['#032058', '#001b46']
                                    }
                                },
                                radius: '65%',
                                name: {
                                    textStyle: {
                                        color: '#0ac4f7',
                                    }
                                },
                                indicator: app.myChart8Data[0].maintance
                            },
                            series: [{
                                type: 'radar',
                                itemStyle: {
                                    borderType: 'solid',
                                    borderWidth: 4
                                },
                                lineStyle: {
                                    width: 3
                                },
                                data: this.myChart8Data
                            }]
                        })

                        this.myChart9 = echarts.init(document.querySelector('#chart9'), 'light')
                        this.myChart9.setOption({
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: this.myChart9Data.map(x => x.name)
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

                                data: this.myChart9Data
                            }]
                        })

                    },
                    renderFirst() {
                        this.myChart2 = echarts.init(document.querySelector('#chart2'), 'light')
                        this.myChart2.setOption({
                            radar: {
                                axisLine: {
                                    lineStyle: {
                                        color: ['#206aa4']
                                    }
                                },
                                splitLine: {
                                    lineStyle: {
                                        color: ['#206aa4']
                                    }
                                },
                                splitArea: {
                                    areaStyle: {
                                        color: ['#032058', '#001b46']
                                    }
                                },
                                radius: '65%',
                                name: {
                                    textStyle: {
                                        color: '#0ac4f7',
                                    }
                                },
                                indicator: this.myChart2Data.map(d => {
                                    return {
                                        name: Object.keys(d),
                                        max: this.myChart2Data.map(x => x[Object.keys(x)]).sort((a, b) => b - a)[0]
                                    }
                                })
                            },
                            series: [{
                                type: 'radar',
                                itemStyle: {
                                    borderType: 'solid',
                                    borderWidth: 4
                                },
                                lineStyle: {
                                    width: 3
                                },
                                data: [{
                                    value: this.myChart2Data.map(x => x[Object.keys(x)]),
                                    label: {
                                        show: true,
                                        color: '#ffffff',
                                        padding: 3,
                                        borderRadius: 5,
                                        backgroundColor: '#069cd1'
                                    }
                                }]
                            }]
                        })


                        this.myChart1 = echarts.init(document.querySelector('#chart1'), 'light')
                        this.myChart1.setOption({
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
                                data: this.myChart1Data.map(x => Object.keys(x))
                            },
                            yAxis: {
                                name: '计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                                data: this.myChart1Data.map(x => x[Object.keys(x)]),
                                type: 'bar'
                            }]
                        })

                        this.myChart4 = echarts.init(document.querySelector('#chart4'), 'light')
                        this.myChart4.setOption({
                            grid: {
                                right: 100,
                            },
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: Object.keys(this.myChart4Data[Object.keys(this.myChart4Data).shift()])
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
                                data: Object.keys(this.myChart4Data)
                            },
                            yAxis: {
                                name: '计划状态&计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                            series: Object.keys(this.myChart4Data[Object.keys(this.myChart4Data).shift()]).map(name => {
                                return {
                                    name,
                                    type: 'bar',
                                    barCategoryGap: '70%',
                                    stack: '总量',
                                    label: {
                                        normal: {
                                            show: true,
                                            position: 'inside'
                                        }
                                    },
                                    data: Object.keys(this.myChart4Data).map((series, i) => {
                                        return [i, this.myChart4Data[series][name]]
                                    })
                                }

                            })
                        })

                        this.charts1 = echarts.init(document.querySelector('#charts1'), 'light')
                        this.charts1.setOption({
                            grid: {
                                right: 100,
                            },
                            legend: {
                                type: 'scroll',
                                orient: 'vertical',
                                right: 10,
                                top: 'middle',
                                bottom: 20,
                                data: Object.keys(this.charts1Data[Object.keys(this.charts1Data).shift()])
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
                                data: Object.keys(this.charts1Data)
                            },
                            yAxis: {
                                name: '修程&计划数量',
                                nameLocation: 'center',
                                nameGap: 40,
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
                            series: Object.keys(this.charts1Data[Object.keys(this.charts1Data).shift()]).map(name => {
                                return {
                                    name,
                                    type: 'bar',
                                    barCategoryGap: '70%',
                                    stack: '总量',
                                    label: {
                                        normal: {
                                            show: true,
                                            position: 'inside'
                                        }
                                    },
                                    data: Object.keys(this.charts1Data).map((series, i) => {
                                        return [i, this.charts1Data[series][name]]
                                    })
                                }

                            })
                        })
                    }
                },
                watch: {
                    value2(val) {
                        var $that = this;
                        self.get_data().then(function (res) {
                            $that.myChart1Data = res.myChart1Data
                            $that.myChart2Data = res.myChart2Data
                            $that.myChart4Data = res.myChart4Data
                            $that.charts1Data = res.charts1Data
                            $that.renderFirst()
                            $that.myChart6Data = res.myChart6Data
                            $that.myChart7Data = res.myChart7Data
                            $that.myChart8Data[0]['value'] = res.myChart8Data['value']
                            $that.myChart8Data[0]['maintance'] = res.myChart8Data['maintance']
                            $that.myChart9Data = res.myChart9Data
                            $that.myChart10Data = res.myChart10Data
                            $that.myChart11Data = res.myChart11Data
                            $that.charts1Data = res.charts1Data
                            $that.charts6Data = res.charts6Data
                            $that.renderSecond()
                            $that.myChartData = res.myChartData
                            $that.quota = res.quota
                            $that.car_trend = res.car_trend
                            $that.renderThird()
                        })
                    }
                }
            })
        }
    });
    core.action_registry.add('statistical_report_client', statistical_report_client);
    return statistical_report_client
});