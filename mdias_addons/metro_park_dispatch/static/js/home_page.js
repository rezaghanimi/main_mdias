/**
 * 系统主页
 */
odoo.define('metro_park.home_page', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');

    var home_page = AbstractAction.extend({
        template: 'home_page',
        datas: [],

        init: function (parent, action, options) {
            this._super.apply(this, arguments)
            var self = this;

            self.datas = ''
            self.window = window
        },

        events: {
            'click #button_shunting': 'button_shunting',
            'click #button_start': 'button_start',
            'click #button_collect': 'button_collect',
            'click #button_maintenance': 'button_maintenance',
        },

        on_attach_callback: function () {
            var self = this
            this._rpc({
                "model": "metro_park_dispatch.home_page",
                "method": "search_home_page_info",
                "args": [moment().subtract(6, 'days'), moment()]
            }).then(function (rst) {
                self.datas = rst;
                var dispatch_info_all = self.datas.dispatch_info.all_summary ? self.datas.dispatch_info.all_summary : 0
                var dispatch_info_day = self.datas.dispatch_info.finished_summary ? self.datas.dispatch_info.finished_summary : 0
                var out_plan_info_all = self.datas.out_plan_info.all_summary ? self.datas.out_plan_info.all_summary : 0
                var out_plan_info_day = self.datas.out_plan_info.finished_summary ? self.datas.out_plan_info.finished_summary : 0
                var back_plan_info_all = self.datas.back_plan_info.all_summary ? self.datas.back_plan_info.all_summary : 0
                var back_plan_info_day = self.datas.back_plan_info.finished_summary ? self.datas.back_plan_info.finished_summary : 0
                var repair_plan_all = self.datas.repair_plan_info.all_summary ? self.datas.repair_plan_info.all_summary : 0
                var repair_plan_day = self.datas.repair_plan_info.finished_summary ? self.datas.repair_plan_info.finished_summary : 0
                var all_rec = parseInt(dispatch_info_all) + parseInt(out_plan_info_all) +
                    parseInt(back_plan_info_all) + parseInt(repair_plan_all)
                var complete_rec = parseInt(dispatch_info_day) + parseInt(out_plan_info_day) +
                    parseInt(back_plan_info_day) + parseInt(repair_plan_day)
                if (all_rec == 0) {
                    all_rec = 1
                }
                self.$('#shunting_plan').html(dispatch_info_day + '/' + dispatch_info_all)
                self.$('#start_plan').html(out_plan_info_day + '/' + out_plan_info_all)
                self.$('#collect_plan').html(back_plan_info_day + '/' + back_plan_info_all)
                self.$('#maintenance_plan').html(repair_plan_day + '/' + repair_plan_all)
                self.$('#all_plan').html((complete_rec / all_rec * 100).toFixed(0) + '%')

                // 车辆运行情况的数据
                self._rpc({
                    "model": "metro_park_dispatch.home_page",
                    "method": "search_vehicle_running_status",
                    "args": [moment().subtract(6, 'days'), moment()]
                }).then(function (rst) {
                    // 重新渲染图表
                    self.vehicle_running(rst)
                })
                // 初始绑定调车计划
                self.dispatch_info = echarts.init(self.$('#dispatch_info')[0], 'light')
                self.dispatch_info.setOption({
                    grid: {
                        top: 10,
                        left: '5%',
                        right: '1%'
                    },
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
                        // 每一天的数据
                        data: self.datas.dispatch_info.days
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
                    // 每天的的调车完成情况
                    series: [{
                        name: '调车完成数',
                        stack: '调车计划',
                        data: self.datas.dispatch_info.all,
                        type: 'bar'
                    }, {
                        name: '调车总量',
                        stack: '调车计划',
                        data: self.datas.dispatch_info.finished,
                        type: 'bar'
                    }]
                })
                setTimeout(function () {
                    self.dispatch_info.resize();
                }, 10)

                // 将当前按扭设置成为primary, 这个的作用是切换视图
                self.$('.plan_type button').on('click', function () {
                    $('.plan_type button').attr('class', 'btn btn-default')
                    $(this).attr('class', 'btn btn-primary')
                })

                // 时间范围选择
                self.$('#date_range').daterangepicker({
                    "ranges": {
                        '今天': [moment(), moment()],
                        '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                        '近一周': [moment().subtract(6, 'days'), moment()],
                        '近一月': [moment().subtract(29, 'days'), moment()],
                        '近半年': [moment().subtract(180, 'days'), moment()],
                        '近一年': [moment().subtract(365, 'days'), moment()],
                    },
                    locale: {
                        format: 'YYYY/MM/DD'
                    },
                    "alwaysShowCalendars": true,
                    "startDate": moment().subtract(6, 'days'),
                    "endDate": moment()
                }, function (start, end, label) {
                    self._rpc({
                        "model": "metro_park_dispatch.home_page",
                        "method": "search_home_page_info",
                        "args": [start, end]
                    }).then(function (rst) {
                        self.datas = rst
                        // 重新渲染图表
                    })
                });

                // 车辆信息
                self.$('#train_info_time_range').daterangepicker({
                    "ranges": {
                        '今天': [moment(), moment()],
                        '昨天': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                        '近一周': [moment().subtract(6, 'days'), moment()],
                        '近一月': [moment().subtract(29, 'days'), moment()],
                        '近半年': [moment().subtract(180, 'days'), moment()],
                        '近一年': [moment().subtract(365, 'days'), moment()],
                    },
                    locale: {
                        format: 'YYYY/MM/DD'
                    },
                    "alwaysShowCalendars": true,
                    "startDate": moment().subtract(6, 'days'),
                    "endDate": moment()
                }, function (start, end, label) {
                    // 重新获取车辆信息
                    self._rpc({
                        "model": "metro_park_dispatch.home_page",
                        "method": "search_vehicle_running_status",
                        "args": [start, end]
                    }).then(function (rst) {
                        // 重新渲染图表
                        self.vehicle_running(rst)
                    })
                });
            })
            self.window.onresize = function () {
                self.button_shunting()
            }
            core.bus.on('main_max', self, self.button_shunting.bind(self));
            core.bus.on('main_window', self, self.button_shunting.bind(self));
        },

        // 车辆运行情况
        vehicle_running: function (rst) {
            var self = this
            // 车辆使用情况
            if (rst.all_status > 0) {
                var train_usage = self.$el.find('#train_usage')[0]
                self.train_usage = echarts.init(train_usage, 'light')
                self.train_usage.setOption({
                    series: [{
                        legendHoverLink: false,
                        name: '访问来源',
                        type: 'pie',
                        avoidLabelOverlap: false,
                        data: [{
                            value: rst.standby[0],
                            name: '备用车' + (rst.standby[0] / rst.all_status * 100).toFixed(2) + '%'
                        },
                            {
                                value: rst.inspection[0],
                                name: '日检车' + (rst.inspection[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.wash[0],
                                name: '洗车安排' + (rst.wash[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.top[0],
                                name: '登顶车' + (rst.top[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.defective[0],
                                name: '故常维修车' + (rst.defective[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.unserviceable[0],
                                name: '不可运用车' + (rst.unserviceable[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.special[0],
                                name: '专业作业车' + (rst.special[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                            {
                                value: rst.scheduled[0],
                                name: '计划维修车' + (rst.scheduled[0] / rst.all_status * 100).toFixed(2) + '%'
                            },
                        ]
                    }]
                })
                setTimeout(function () {
                    self.train_usage.resize();
                }, 10)
                self.$('#standby_count').html(rst.standby[0])
                self.$('#standby_id').html(JSON.stringify(rst.standby[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#inspection_count').html(rst.inspection[0])
                self.$('#inspection_id').html(JSON.stringify(rst.inspection[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#wash_count').html(rst.wash[0])
                self.$('#wash_id').html(JSON.stringify(rst.wash[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#top_count').html(rst.top[0])
                self.$('#top_id').html(JSON.stringify(rst.top[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#defective_count').html(rst.defective[0])
                self.$('#defective_id').html(JSON.stringify(rst.defective[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#unserviceable_count').html(rst.unserviceable[0])
                self.$('#unserviceable_id').html(JSON.stringify(rst.unserviceable[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#special_count').html(rst.special[0])
                self.$('#Special_id').html(JSON.stringify(rst.special[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
                self.$('#scheduled_count').html(rst.scheduled[0])
                self.$('#Scheduled_id').html(JSON.stringify(rst.scheduled[1]).slice(2, -2).replace(/"([^"]*)"/g, "$1"))
            } else {
                var train_usage = self.$el.find('#train_usage')[0]
                self.train_usage = echarts.init(train_usage, 'light')
                self.train_usage.setOption({
                    series: [{
                        legendHoverLink: false,
                        name: '访问来源',
                        type: 'pie',
                        avoidLabelOverlap: false,
                        data: [{
                            value: 0,
                            name: '没有对应的数据'
                        }]
                    }]
                })
                setTimeout(function () {
                    self.train_usage.resize();
                }, 10)
                self.$('#standby_count').html('0')
                self.$('#standby_id').html('无')
                self.$('#inspection_count').html('0')
                self.$('#inspection_id').html('无')
                self.$('#wash_count').html('0')
                self.$('#wash_id').html('无')
                self.$('#top_count').html('0')
                self.$('#top_id').html('无')
                self.$('#defective_count').html('0')
                self.$('#defective_id').html('无')
                self.$('#unserviceable_count').html('0')
                self.$('#unserviceable_id').html('无')
                self.$('#special_count').html('0')
                self.$('#Special_id').html('无')
                self.$('#scheduled_count').html('0')
                self.$('#Scheduled_id').html('无')
                self.$('#other_id').html('无')
            }
        },

        echarts_data: function (data) {
            self.dispatch_info = echarts.init(this.$('#dispatch_info')[0], 'light')
            self.dispatch_info.setOption({
                grid: {
                    top: 10,
                    left: '5%',
                    right: '1%'
                },
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
                    // 每一天的数据
                    data: data.days
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
                // 每天的的调车完成情况
                series: [{
                    name: '调车完成数',
                    stack: '调车计划',
                    data: data.all,
                    type: 'bar'
                }, {
                    name: '调车总量',
                    stack: '调车计划',
                    data: data.finished,
                    type: 'bar'
                }]
            })
            setTimeout(function () {
                self.dispatch_info.resize();
            }, 10)
        },

        // 调车计划
        button_shunting: function () {
            var self = this;
            self.echarts_data(self.datas.dispatch_info)
        },

        // 发车计划
        button_start: function () {
            var self = this;
            self.echarts_data(self.datas.out_plan_info)
        },

        // 收车计划
        button_collect: function () {
            var self = this;
            self.echarts_data(self.datas.back_plan_info)
        },

        // 检修计划
        button_maintenance: function () {
            var self = this;
            self.echarts_data(self.datas.repair_plan_info)
        }
    });

    core.action_registry.add('home_page', home_page);

//    core.home_client_action = {
//        'type': 'ir.actions.client',
//        'tag': 'home_page',
//        'name': '首页'
//    };

    return {
        'home_page': home_page
    };
});