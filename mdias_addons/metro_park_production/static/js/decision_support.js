odoo.define('decision_support', function (require) {
    "use strict";
    var core = require('web.core');
    var Widget = require('web.Widget');
    var AbstractAction = require('web.AbstractAction');

    var decision_support = AbstractAction.extend({
        init: function (parent, action) {
            var self = this;
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            self.get_other_data()
            self.get_histogram_data()
            self.get_pie_data()

            this._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {module_name: 'metro_park_production', template_name: 'decision_support'}
            }).then(function (res) {
                self.$el.append(res)

                // var char_data = self.get_histogram_data()
                var echart_data = {
                    tabIndex1: 1,
                    tabIndex2: 0,
                    tags: [
                        {name: '今天', actived: true, tabIndex: 0},
                        {name: '近一周', actived: false, tabIndex: 1},
                        {name: '近一月', actived: false, tabIndex: 2},
                        {name: '近两月', actived: false, tabIndex: 3},
                        {name: '近半年', actived: false, tabIndex: 4},
                        {name: '近一年', actived: false, tabIndex: 5}
                    ],
                    headcss: {'background-color': '#cccccc'},
                    input: '',
                    input1: '',
                    input2: '',
                    input3: '',
                    input4: '',
                    value6: [new Date(), new Date()],
                    value1: new Date(),
                    activeName: 'dc',
                    errordata: [
                        {carno: 13579, content: '半年保洁', finish: '已完成'}
                    ],
                    leaderdata: [
                        {content: ''}
                    ],
                    safedata: [
                        {content: ''}
                    ],
                    jiaobandata: [
                        {content: ''}
                    ],
                    chartData: self.chart_data,
                    pieData: self.pie_data,
                }
                echart_data['finish1'] = self.other_data.finish1
                echart_data['finish2'] = self.other_data.finish2
                echart_data['finish3'] = self.other_data.finish3
                echart_data['finish4'] = self.other_data.finish4
                echart_data['total1'] = self.other_data.total1
                echart_data['total2'] = self.other_data.total2
                echart_data['total3'] = self.other_data.total3
                echart_data['total4'] = self.other_data.total4
                echart_data['tableData'] = self.other_data.tableData
                echart_data['waterData'] = self.other_data.waterData
                var vue = new Vue({
                    el: '#decision_support',
                    data() {
                        this.waterheight = "150px";
                        this.chartSettings = {
                            stack: {
                                '调车计划': ['已调车数', '未调车数'],
                                '发车计划': ['已发车数', '未发车数'],
                                '收车计划': ['未收车数', '已收车数'],
                                '检修计划': ['未检车数', '已检车数']
                            }
                        };

                        return echart_data
                    },

                    methods: {
                        toggleTag1(item, index) {
                            this.tabIndex1 = index
                            const end = new Date()
                            const start = new Date()
                            if (index === 1) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
                            }
                            if (index === 0) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 0)
                            }
                            if (index === 2) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
                            }
                            if (index === 3) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 60)
                            }
                            if (index === 4) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 182)
                            }
                            if (index === 5) {
                                start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
                            }
                            this.value6 = [start, end]
                        },
                        toggleTag2(item, index) {
                            this.tabIndex2 = index
                            console.log(item)
                            console.log(index)
                        },
                        selecttag() {
                            console.log('你点击了选择日期')
                        },
                        handleClick(tab, event) {
                            console.log(tab, event)
                        },
                    },

                });
            })
        },
        //获取柱状图数据
        get_histogram_data: function () {
            var self = this;
            this._rpc({
                model: 'metro_park_production.decision_support',
                method: 'get_histogram_data',
                args: [self.id]
            }).then(function (data) {
                self.chart_data = JSON.parse(data)
            })

        },
        //获取饼状图数据
        get_pie_data: function () {
            var self = this;
            this._rpc({
                model: 'metro_park_production.decision_support',
                method: 'get_pie_data',
                args: [self.id]
            }).then(function (data) {
                self.pie_data = JSON.parse(data)
            })

        },
        //获取其他数据
        get_other_data: function () {
            var self = this;
            this._rpc({
                model: 'metro_park_production.decision_support',
                method: 'get_other_data',
                args: [self.id]
            }).then(function (data) {
                self.other_data = JSON.parse(data)
            })

        }


    });

    core.action_registry.add('decision_support', decision_support);
    return {'decision_support': decision_support};


});