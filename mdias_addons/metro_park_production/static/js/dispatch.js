odoo.define('dispatch', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var dispatch = Widget.extend({
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            self.get_all_data()
            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_production', template_name: 'dispatch'}
            }).then(function (res) {
                self.$el.append(res)
                self.option1 ={
                    title: {
                        text: "收/发车趋势图"
                    }
                ,
                    color: ["#e49588", "#87c3cb"],
                        tooltip
                :
                    {
                        trigger: "axis"
                    }
                ,
                    legend: {
                        data: ["发车量", "收车量"]
                    }
                ,
                    grid: {
                        left: "3%",
                            right
                    :
                        "4%",
                            bottom
                    :
                        "3%",
                            containLabel
                    :
                        true
                    }
                ,
                    toolbox: {
                        feature: {
                            saveAsImage: {
                            }
                        }
                    }
                ,
                    xAxis: {
                        type: "category",
                            boundaryGap
                    :
                        false,
                            data
                    :
                        [
                            // 用选择的时间替换
                            "11:00",
                            "11:30",
                            "12:00",
                            "12:30",
                            "13:00",
                            "13:30",
                            "14:00",
                            "14:30",
                            "15:00",
                            "15:30",
                            "16:00",
                            "16:30",
                            "17:00",
                            "17:30",
                            "18:00"
                        ]
                    }
                ,
                    yAxis: {
                        type: "value"
                    }
                ,
                    series: [
                        {
                            name: "发车量",
                            type: "line",
                            stack: "总量",
                            data: [
                                120,
                                132,
                                101,
                                134,
                                90,
                                230,
                                210,
                                120,
                                132,
                                101,
                                134,
                                90,
                                230,
                                210,
                                190
                            ]
                        },
                        {
                            name: "收车量",
                            type: "line",
                            stack: "总量",
                            data: [
                                220,
                                182,
                                191,
                                234,
                                290,
                                330,
                                310,
                                220,
                                182,
                                191,
                                234,
                                290,
                                330,
                                310,
                                290
                            ]
                        }
                    ]
                }

                self.option2 = {
                    title: {
                        text: "调车钩计划数量分布",
                        x: "left"
                    },
                    color: [
                        "#87c3cb",
                        "#7cf979",
                        "#f9e628",
                        "#2eaffd",
                        "#8dbc56",
                        "#e27a3f",
                        "#363d8d",
                        "#cc2dfc"
                    ],
                    xAxis: {
                        type: "category",
                        boundaryGap: false,
                        data: [
                            // 用选择的时间替换
                            "11:00",
                            "11:30",
                            "12:00",
                            "12:30",
                            "13:00",
                            "13:30",
                            "14:00",
                            "14:30",
                            "15:00",
                            "15:30",
                            "16:00",
                            "16:30",
                            "17:00",
                            "17:30",
                            "18:00"
                        ]
                    },
                    yAxis: {
                        type: "value"
                    },
                    tooltip: {
                        trigger: "axis",
                        axisPointer: {
                            type: "shadow"
                        }
                    },
                    dataZoom: [
                        {type: "inside", startValue: 0, endValue: 13, zoomLock: true}
                    ],
                    series: [
                        {
                            data: [
                                820,
                                932,
                                901,
                                934,
                                1290,
                                1330,
                                1320,
                                820,
                                932,
                                901,
                                934,
                                1290,
                                1330,
                                1320,
                                820
                            ],
                            type: "line",
                            areaStyle: {},
                            smooth: true,
                            itemStyle: {
                                normal: {
                                    label: {
                                        show: true,
                                        position: "top",
                                        textStyle: {
                                            color: "black"
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
                self.option3 = {
                    title: {
                        text: "发车计划准点率",
                        x: "left"
                    },
                    tooltip: {
                        formatter: "{a} <br/>{b} : {c}%"
                    },
                    series: [
                        {
                            name: "发车计划准点率",
                            type: "gauge",
                            radius: "65%",
                            center: ["50%", "60%"],
                            detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                            data: [{value: 50, name: "完成率"}],
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: [[1, "#4394e5"]],
                                    width: 20
                                }
                            }
                        }
                    ]
                }
                self.option4 = {
                    title: {
                        text: "收车计划准点率",
                        x: "left"
                    },
                    tooltip: {
                        formatter: "{a} <br/>{b} : {c}%"
                    },
                    series: [
                        {
                            name: "收车计划准点率",
                            type: "gauge",
                            radius: "65%",
                            center: ["50%", "60%"],
                            detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                            data: [{value: 60, name: "完成率"}],
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: [[1, "#4394e5"]],
                                    width: 20
                                }
                            }
                        }
                    ]
                }
                self.option5 = {
                    title: {
                        text: "调车完成率",
                        x: "left"
                    },
                    tooltip: {
                        formatter: "{a} <br/>{b} : {c}%"
                    },
                    series: [
                        {
                            name: "调车完成率",
                            type: "gauge",
                            radius: "65%",
                            center: ["50%", "60%"],
                            detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                            data: [{value: 70, name: "完成率"}],
                            axisLine: {
                                show: true,
                                lineStyle: {
                                    color: [[1, "#4394e5"]],
                                    width: 20
                                }
                            }
                        }
                    ]
                }
                setTimeout(function () {
                    var echart1 = self.$el.find('#myChartLine1')[0]
                    var echart2 = self.$el.find('#myChartLine2')[0]
                    var echart3 = self.$el.find('#myChartGauge1')[0]
                    var echart4 = self.$el.find('#myChartGauge2')[0]
                    var echart5 = self.$el.find('#myChartGauge3')[0]
                    self.echart1 = echarts.init(echart1, 'light')
                    self.echart2 = echarts.init(echart2, 'light')
                    self.echart3 = echarts.init(echart3, 'light')
                    self.echart4 = echarts.init(echart4, 'light')
                    self.echart5 = echarts.init(echart5, 'light')
                    self.echart1.setOption(self.option1);
                    self.echart2.setOption(self.option2);
                    self.echart3.setOption(self.option3);
                    self.echart4.setOption(self.option4);
                    self.echart5.setOption(self.option5);

                },300)
                var vue = new Vue({
                    el: '#dispatch',
                    data() {
                        return {
                            pickerOptions: {
                                shortcuts: [
                                    {
                                        text: "今天",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 1);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    },
                                    {
                                        text: "最近一周",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    },
                                    {
                                        text: "最近两周",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 14);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    },
                                    {
                                        text: "最近一个月",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    },
                                    {
                                        text: "最近半年",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 180);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    },
                                    {
                                        text: "最近一年",
                                        onClick(picker) {
                                            const end = new Date();
                                            const start = new Date();
                                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 360);
                                            picker.$emit("pick", [start, end]);
                                        }
                                    }
                                ]
                            },
                            tableData: [{jieche: "11", fache: "22", liangshu: "33", goushu: "44"}],
                            datetimeRange: "",
                            datetimeRange2: "",
                            datetimeRange3: "",
                            option1: {
                                title: {
                                    text: "收/发车趋势图"
                                },
                                color: ["#e49588", "#87c3cb"],
                                tooltip: {
                                    trigger: "axis"
                                },
                                legend: {
                                    data: ["发车量", "收车量"]
                                },
                                grid: {
                                    left: "3%",
                                    right: "4%",
                                    bottom: "3%",
                                    containLabel: true
                                },
                                toolbox: {
                                    feature: {
                                        saveAsImage: {}
                                    }
                                },
                                xAxis: {
                                    type: "category",
                                    boundaryGap: false,
                                    data: [
                                        // 用选择的时间替换
                                        "11:00",
                                        "11:30",
                                        "12:00",
                                        "12:30",
                                        "13:00",
                                        "13:30",
                                        "14:00",
                                        "14:30",
                                        "15:00",
                                        "15:30",
                                        "16:00",
                                        "16:30",
                                        "17:00",
                                        "17:30",
                                        "18:00"
                                    ]
                                },
                                yAxis: {
                                    type: "value"
                                },
                                series: [
                                    {
                                        name: "发车量",
                                        type: "line",
                                        stack: "总量",
                                        data: [
                                            120,
                                            132,
                                            101,
                                            134,
                                            90,
                                            230,
                                            210,
                                            120,
                                            132,
                                            101,
                                            134,
                                            90,
                                            230,
                                            210,
                                            190
                                        ]
                                    },
                                    {
                                        name: "收车量",
                                        type: "line",
                                        stack: "总量",
                                        data: [
                                            220,
                                            182,
                                            191,
                                            234,
                                            290,
                                            330,
                                            310,
                                            220,
                                            182,
                                            191,
                                            234,
                                            290,
                                            330,
                                            310,
                                            290
                                        ]
                                    }
                                ]
                            },
                            option2: {
                                title: {
                                    text: "调车钩计划数量分布",
                                    x: "left"
                                },
                                color: [
                                    "#87c3cb",
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                xAxis: {
                                    type: "category",
                                    boundaryGap: false,
                                    data: [
                                        // 用选择的时间替换
                                        "11:00",
                                        "11:30",
                                        "12:00",
                                        "12:30",
                                        "13:00",
                                        "13:30",
                                        "14:00",
                                        "14:30",
                                        "15:00",
                                        "15:30",
                                        "16:00",
                                        "16:30",
                                        "17:00",
                                        "17:30",
                                        "18:00"
                                    ]
                                },
                                yAxis: {
                                    type: "value"
                                },
                                tooltip: {
                                    trigger: "axis",
                                    axisPointer: {
                                        type: "shadow"
                                    }
                                },
                                dataZoom: [
                                    {type: "inside", startValue: 0, endValue: 13, zoomLock: true}
                                ],
                                series: [
                                    {
                                        data: [
                                            820,
                                            932,
                                            901,
                                            934,
                                            1290,
                                            1330,
                                            1320,
                                            820,
                                            932,
                                            901,
                                            934,
                                            1290,
                                            1330,
                                            1320,
                                            820
                                        ],
                                        type: "line",
                                        areaStyle: {},
                                        smooth: true,
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top",
                                                    textStyle: {
                                                        color: "black"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            option3: {
                                title: {
                                    text: "发车计划准点率",
                                    x: "left"
                                },
                                tooltip: {
                                    formatter: "{a} <br/>{b} : {c}%"
                                },
                                series: [
                                    {
                                        name: "发车计划准点率",
                                        type: "gauge",
                                        radius: "65%",
                                        center: ["50%", "60%"],
                                        detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                                        data: [{value: 50, name: "完成率"}],
                                        axisLine: {
                                            show: true,
                                            lineStyle: {
                                                color: [[1, "#4394e5"]],
                                                width: 20
                                            }
                                        }
                                    }
                                ]
                            },
                            option4: {
                                title: {
                                    text: "收车计划准点率",
                                    x: "left"
                                },
                                tooltip: {
                                    formatter: "{a} <br/>{b} : {c}%"
                                },
                                series: [
                                    {
                                        name: "收车计划准点率",
                                        type: "gauge",
                                        radius: "65%",
                                        center: ["50%", "60%"],
                                        detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                                        data: [{value: 60, name: "完成率"}],
                                        axisLine: {
                                            show: true,
                                            lineStyle: {
                                                color: [[1, "#4394e5"]],
                                                width: 20
                                            }
                                        }
                                    }
                                ]
                            },
                            option5: {
                                title: {
                                    text: "调车完成率",
                                    x: "left"
                                },
                                tooltip: {
                                    formatter: "{a} <br/>{b} : {c}%"
                                },
                                series: [
                                    {
                                        name: "调车完成率",
                                        type: "gauge",
                                        radius: "65%",
                                        center: ["50%", "60%"],
                                        detail: {formatter: "{value}%", fontSize: 20, color: "black"},
                                        data: [{value: 70, name: "完成率"}],
                                        axisLine: {
                                            show: true,
                                            lineStyle: {
                                                color: [[1, "#4394e5"]],
                                                width: 20
                                            }
                                        }
                                    }
                                ]
                            }
                        };
                    },
                    methods: {
                        setECharts() {
                            let echart1 = echarts.init(document.getElementById("myChartLine1"));
                            let echart2 = echarts.init(document.getElementById("myChartLine2"));
                            let echart3 = echarts.init(document.getElementById("myChartGauge1"));
                            let echart4 = echarts.init(document.getElementById("myChartGauge2"));
                            let echart5 = echarts.init(document.getElementById("myChartGauge3"));
                            echart1.setOption(this.option1);
                            echart2.setOption(this.option2);
                            echart3.setOption(this.option3);
                            echart4.setOption(this.option4);
                            echart5.setOption(this.option5);
                        }
                    },
                    mounted() {
                        this.setECharts();
                    }
                });

            })
        },
        //获取其他数据
        get_all_data: function () {
            var self = this;
            this._rpc({
                model: 'metro_park_production.decision_support',
                method: 'get_dispatch_data',
                args: [self.id]
            }).then(function (data) {
                self.other_data = JSON.parse(data)
            })
        }

    });

    core.action_registry.add('dispatch', dispatch);
    return {'dispatch': dispatch};


});