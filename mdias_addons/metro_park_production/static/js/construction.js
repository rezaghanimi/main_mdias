odoo.define('construction', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');

    var construction = Widget.extend({
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_production', template_name: 'construction'}
            }).then(function (res) {
                self.$el.append(res)
                var vue = new Vue({
                    el: '#construction',
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
                            datetimeRange: "",
                            option1: {
                                title: {
                                    text: "计划分布图",
                                    x: "left"
                                },
                                color: [
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                tooltip: {
                                    trigger: "item",
                                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                                },
                                legend: {
                                    bottom: 10,
                                    data: [
                                        "工电一部",
                                        "机电一部",
                                        "通号一部",
                                        "乘务一部",
                                        "客运一部",
                                        "车辆一部",
                                        "其他"
                                    ]
                                },
                                series: [
                                    {
                                        name: "计划分布图",
                                        type: "pie",
                                        radius: ["40%", "60%"],
                                        center: ["50%", "50%"],
                                        avoidLabelOverlap: false,
                                        label: {
                                            normal: {
                                                show: false,
                                                position: "center"
                                            },
                                            emphasis: {
                                                show: true,
                                                textStyle: {
                                                    fontSize: "20",
                                                    fontWeight: "bold"
                                                }
                                            }
                                        },
                                        labelLine: {
                                            normal: {
                                                show: false
                                            }
                                        },
                                        data: [
                                            {value: 335, name: "工电一部"},
                                            {value: 310, name: "机电一部"},
                                            {value: 234, name: "通号一部"},
                                            {value: 135, name: "乘务一部"},
                                            {value: 1548, name: "客运一部"},
                                            {value: 135, name: "车辆一部"},
                                            {value: 1548, name: "其他"}
                                        ]
                                    }
                                ]
                            },
                            option2: {
                                title: {
                                    text: "各部门计划数量",
                                    x: "left"
                                },
                                color: [
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                tooltip: {
                                    trigger: "axis",
                                    axisPointer: {
                                        type: "shadow"
                                    }
                                },
                                legend: {
                                    bottom: 10,
                                    data: ["临补", "日补", "月计划"]
                                },
                                grid: {
                                    left: "5%",
                                    right: "6%",
                                    bottom: "13%",
                                    containLabel: true
                                },
                                xAxis: [
                                    {
                                        type: "category",
                                        data: [
                                            "工电一部",
                                            "机电一部",
                                            "通号一部",
                                            "乘务一部",
                                            "客运一部",
                                            "车辆一部"
                                        ]
                                    }
                                ],
                                yAxis: [
                                    {
                                        type: "value"
                                    }
                                ],
                                series: [
                                    {
                                        name: "临补",
                                        type: "bar",
                                        data: [320, 332, 301, 334, 390, 330],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    },
                                    {
                                        name: "日补",
                                        type: "bar",
                                        data: [120, 132, 101, 134, 90, 230],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    },
                                    {
                                        name: "月计划",
                                        type: "bar",
                                        data: [220, 182, 191, 234, 290, 330],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            option3: {
                                title: {
                                    text: "时间使用率",
                                    x: "left"
                                },
                                color: [
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
                                        "工电一部",
                                        "机电一部",
                                        "通号一部",
                                        "乘务一部",
                                        "客运一部",
                                        "车辆一部",
                                        "外单位",
                                        "其他"
                                    ],
                                    axisLabel: {
                                        rotate: 45
                                    }
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
                                series: [
                                    {
                                        data: [820, 932, 901, 934, 1290, 1330, 178, 1320],
                                        type: "line",
                                        areaStyle: {},
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
                            option4: {
                                title: {
                                    text: "计划兑现率",
                                    x: "left"
                                },
                                color: [
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                tooltip: {},
                                legend: {
                                    data: ["月兑现率", "日兑现率", "临兑现率"],
                                    bottom: 10
                                },
                                radar: {
                                    center: ["50%", "50%"],
                                    radius: "50%",
                                    name: {
                                        textStyle: {
                                            color: "#fff",
                                            backgroundColor: "#999",
                                            borderRadius: 3,
                                            padding: [3, 5]
                                        }
                                    },
                                    indicator: [
                                        {name: "工电一部"},
                                        {name: "机电一部"},
                                        {name: "通号一部"},
                                        {name: "乘务一部"},
                                        {name: "客运一部"},
                                        {name: "车辆一部"},
                                        {name: "外单位"},
                                        {name: "其他"}
                                    ]
                                },
                                series: [
                                    {
                                        name: "兑现率",
                                        type: "radar",
                                        data: [
                                            {
                                                value: [4300, 10000, 28000, 35000, 50000, 19000, 4500, 2333],
                                                name: "月兑现率"
                                            },
                                            {
                                                value: [5000, 14000, 28000, 31000, 42000, 21000, 4600, 2433],
                                                name: "日兑现率"
                                            },
                                            {
                                                value: [3600, 14000, 28000, 31000, 42000, 21000, 4400, 2533],
                                                name: "临兑现率"
                                            }
                                        ]
                                    }
                                ]
                            },
                            option5: {
                                title: {
                                    text: "各部门完成情况",
                                    x: "left"
                                },
                                color: [
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                tooltip: {
                                    trigger: "axis",
                                    axisPointer: {
                                        type: "shadow"
                                    }
                                },
                                legend: {
                                    bottom: 20,
                                    data: ["已完成", "未完成"]
                                },
                                grid: {
                                    left: "8%",
                                    right: "10%",
                                    bottom: "13%",
                                    containLabel: true
                                },
                                xAxis: {
                                    type: "value"
                                },
                                yAxis: {
                                    type: "category",
                                    data: [
                                        "工电一部",
                                        "机电一部",
                                        "通号一部",
                                        "乘务一部",
                                        "客运一部",
                                        "车辆一部",
                                        "外单位",
                                        "其他"
                                    ]
                                },
                                series: [
                                    {
                                        name: "已完成",
                                        type: "bar",
                                        stack: "总量",
                                        label: {
                                            normal: {
                                                show: true,
                                                position: "insideRight"
                                            }
                                        },
                                        data: [150, 212, 201, 154, 190, 330, 410, 390]
                                    },
                                    {
                                        name: "未完成",
                                        type: "bar",
                                        stack: "总量",
                                        label: {
                                            normal: {
                                                show: true,
                                                position: "insideRight"
                                            }
                                        },
                                        data: [820, 832, 901, 934, 1290, 1330, 1320, 222]
                                    }
                                ]
                            },
                            option6: {
                                title: {
                                    text: "计划统计",
                                    x: "left"
                                },
                                color: [
                                    "#7cf979",
                                    "#f9e628",
                                    "#2eaffd",
                                    "#8dbc56",
                                    "#e27a3f",
                                    "#363d8d",
                                    "#cc2dfc"
                                ],
                                tooltip: {
                                    trigger: "axis",
                                    axisPointer: {
                                        type: "shadow"
                                    }
                                },
                                legend: {
                                    right: 10,
                                    data: ["A", "B", "C"]
                                },
                                grid: {
                                    left: "3%",
                                    right: "4%",
                                    bottom: "3%",
                                    containLabel: true
                                },
                                xAxis: [
                                    {
                                        type: "category",
                                        data: [
                                            "工电一部",
                                            "机电一部",
                                            "通号一部",
                                            "乘务一部",
                                            "客运一部",
                                            "车辆一部",
                                            "其他"
                                        ]
                                    }
                                ],
                                yAxis: [
                                    {
                                        type: "value"
                                    }
                                ],
                                series: [
                                    {
                                        name: "A",
                                        type: "bar",
                                        data: [320, 332, 301, 334, 390, 330, 200],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    },
                                    {
                                        name: "B",
                                        type: "bar",
                                        data: [120, 132, 101, 134, 90, 230, 230],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    },
                                    {
                                        name: "C",
                                        type: "bar",
                                        data: [220, 182, 191, 234, 290, 330, 180],
                                        itemStyle: {
                                            normal: {
                                                label: {
                                                    show: true,
                                                    position: "top"
                                                }
                                            }
                                        }
                                    }
                                ]
                            },
                            option7: {
                                title: {
                                    text: "作业区域分布",
                                    x: "left"
                                },
                                color: [
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
                                    data: [
                                        "会展中心站1",
                                        "会展中心站2",
                                        "会展中心站3",
                                        "会展中心站4",
                                        "会展中心站5",
                                        "会展中心站6",
                                        "会展中心站7",
                                        "会展中心站8",
                                        "会展中心站9",
                                        "会展中心站10",
                                        "会展中心站11",
                                        "会展中心站12",
                                        "会展中心站13",
                                        "会展中心站14"
                                    ],
                                    axisLabel: {
                                        rotate: 45
                                    }
                                },
                                yAxis: {
                                    type: "value"
                                },
                                dataZoom: [{type: 'inside', startValue: 0, endValue: 15, zoomLock: true}],
                                series: [
                                    {
                                        data: [
                                            120,
                                            200,
                                            150,
                                            80,
                                            70,
                                            110,
                                            130,
                                            120,
                                            200,
                                            150,
                                            80,
                                            70,
                                            110,
                                            130
                                        ],
                                        type: "bar"
                                    }
                                ]
                            }
                        };
                    },
                    methods: {
                        setECharts() {
                            let echart1 = echarts.init(document.getElementById("myChartPie1"));
                            let echart2 = echarts.init(document.getElementById("myChartBar1"));
                            let echart3 = echarts.init(document.getElementById("myChartLine1"));
                            let echart4 = echarts.init(document.getElementById("myChartRadar1"));
                            let echart5 = echarts.init(document.getElementById("myChartBar2"));
                            let echart6 = echarts.init(document.getElementById("myChartBar3"));
                            let echart7 = echarts.init(document.getElementById("myChartBar4"));
                            echart1.setOption(this.option1);
                            echart2.setOption(this.option2);
                            echart3.setOption(this.option3);
                            echart4.setOption(this.option4);
                            echart5.setOption(this.option5);
                            echart6.setOption(this.option6);
                            echart7.setOption(this.option7);
                        }
                    },
                    mounted() {
                        this.setECharts();
                    }
                });
            })
        },
    });

    core.action_registry.add('construction', construction);
    return {'construction': construction};


});