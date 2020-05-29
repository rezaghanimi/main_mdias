/**
 * 年计划编辑
 */
odoo.define('metro_park.year_plan_editor', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var utility = require('metro_park_maintenance.utility')
    var qweb = core.qweb

    var year_plan_editor_action = AbstractAction.extend({
        rules: [],
        plan_datas: [],
        start_month: 1,
        end_month: 2,
        devs: [],
        repair_counts: [],
        template: 'year_plan_editor',

        // 记录相关操作
        last_rule_id: undefined,
        last_operation: undefined,
        last_move_obj: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .recompute": "_on_recompute_btn_click",
            "click .clear_month_data": "_on_clear_plan",
            "click .download_plan_template": "_on_download_template",
            "click .dev_item": "_on_dev_item_click",
            "click .history_info": "_on_view_history_info",
            "click .import_year_plan": "_import_year_plan",
            "change .start_month": "_on_start_change",
            "change .end_month": "_on_end_change"
        }),

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.year_plan_id = action.context.active_id || action.params.active_id
        },

        /**
         * 清除计划
         */
        _on_clear_plan: function () {
            var self = this
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: 'metro_park_maintenance.year_plan_clear_wizard',
                target: 'new',
                views: [[false, 'form']],
                context: {
                    "year_plan_id": self.year_plan_id
                },
            },{
                on_reverse_breadcrumb: function () {
                    self._reload();
                },
                on_close: function () {
                    self._reload();
                }
             });
        },

        //滚动条补丁
        scrollPatch: function () {
            var main_box = this.$('.main_table_box')
            var scollWidth = main_box.width() - main_box.prop('clientWidth') // 纵向滚动条宽度
            var scollHeight = main_box.height() - main_box.prop('clientHeight') // 纵向滚动条宽度

            // header添加补丁
            var addHeaderPatch = function (elem) {
                if (scollWidth) {
                    elem = elem.eq(0);
                    if (!elem.find('.header-patch')[0]) {
                        var patchElem = $('<th class="header-patch"><div></div></th>'); //补丁元素
                        patchElem.find('div').css({
                            width: scollWidth
                        });
                        elem.find('tr').append(patchElem);
                    }
                } else {
                    elem.find('.header-patch').remove();
                }
            }

            var addFxiedPatch = function (elem) {
                if (scollHeight) {
                    elem = elem.eq(0);
                    if (!elem.find('.fixed-patch')[0]) {
                        var patchElem = $('<tr class="fixed-patch"><td><div></div></td></tr>'); //补丁元素
                        patchElem.find('div').css({
                            height: scollHeight
                        });
                        elem.find('tbody').append(patchElem);
                    }
                } else {
                    elem.find('.fixed-left-patch').remove();
                }
            }

            // header 打补丁
            addHeaderPatch(this.$('.fixed_header_table'));
            addFxiedPatch(this.$('.fixed_left_body'))
            addFxiedPatch(this.$('.fixed_right_body'))
        },

        format_date: function (date_str) {
            return date_str.substr(5)
        },

        _on_dev_item_click: function (event) {
            var self = this
            var target = $(event.target)
            var dev_id = target.attr('dev-id')
            this._rpc({
                "model": "metro_park_maintenance.year_plan",
                "method": "edit_dev_rules",
                "args": [this.year_plan_id, dev_id]
            }).then(function (action) {
                self.do_action(action)
            })
        },

        _on_start_change: function() {
            this.start_month = parseInt(this.$('.start_month').val());
            if (!this.start_month) {
                this.start_month = 1
            }
            this._reload()
        },

        _on_end_change: function() {
            this.end_month = parseInt(this.$('.end_month').val());
            if (!this.end_month) {
                this.end_month = 1
            }
            if (this.end_month < this.start_month) {
                this.end_month = this.start_month + 1
                if (this.end_month > 12) {
                    this.end_month = 12
                }
                this.$('.end_month').val(this.end_month)
            }
            this._reload()
        },

        /**
         * 年计划导入向导
         */
        _import_year_plan: function() {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.year_plan_import_wizard",
                target: 'new',
                context: {
                    "default_year_plan_id": this.year_plan_id
                },
                views: [
                    [false, 'form']
                ],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    self._reload()
                }
            });
        },

        get_week: function (plan_date) {
            var index = moment(plan_date).weekday()
            var ar = ['日', '一', '二', '三', '四', '五', '六']
            return ar[index]
        },

        /**
         * 下载模板
         */
        _on_download_template: function () {
            this.do_action({
                'type': 'ir.actions.act_url',
                'url': '/metro_park_maintenance/get_year_plan_template',
            })
        },

        /**
         * 先弹出让用户选择月份
         */
        _on_recompute_btn_click: function () {
            var self = this
            $.when(this._rpc({
                "model": "year_plan_compute_wizard",
                "method": "get_work_class_count",
                "args": []
            }), this._rpc({
                "model": "year_plan_compute_wizard",
                "method": "get_compute_host",
                "args": []
            })).then(function (work_class_count, calc_host) {
                return self.do_action({
                    name: '编制计划',
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: "year_plan_compute_wizard",
                    target: 'new',
                    context: {
                        "default_work_class_count": work_class_count,
                        "default_calc_host": calc_host,
                        "year_plan_id": self.year_plan_id
                    },
                    views: [
                        [false, 'form']
                    ],
                }, {
                    on_close: function (res) {
                        if (!res || res == 'special') {
                            return
                        }
                        // 如果当前计划已经发布则不能再进行计算
                        self.gen_plan(res)
                    }
                });
            })
        },

        /**
         * 生成计划, 直接从前端调用算法生成计划
         */
        gen_plan: function (res) {
            if (this.year_plan_id) {
                var self = this
                var plan_info = undefined
                this._rpc({
                    "model": "year_plan_compute_wizard",
                    "method": "get_wizard_data",
                    "args": [res.res_id]
                }).then(function (rst) {
                    var info = rst
                    info.year_plan_id = self.year_plan_id
                    info.detail_id = self.year_plan_id
                    return self._rpc({
                        "model": "metro_park_maintenance.year_plan",
                        "method": "get_year_plan_compute_data",
                        "args": [info]
                    })
                }).then(function (rst) {
                    var data = rst.data
                    var calc_host = data.calc_host
                    if (!_.str.startsWith(calc_host, "ws://")) {
                        calc_host = "ws://" + calc_host
                    }
                    plan_info = data
                    return utility.do_plan_by_websocket(calc_host, rst);
                }).then(function (rst) {
                    return self._rpc({
                        "model": "metro_park_maintenance.year_plan",
                        "method": "deal_plan_data",
                        "args": [plan_info, rst]
                    })
                }).then(function () {
                    self.do_warn('提示', '年计划生成成功!', true);
                    self._reload()
                }).fail(function (error) {
                    self.do_warn('提示', '计算出错!' + error, true);
                })
            }
        },

        sync_row_height: function () {
            var main_body_rows = this.$('.main_table tr')
            var left_fixed_rows = this.$('.fixed_left_body tr')
            var right_fixed_rows = this.$('.fixed_right_body tr')

            // 主体内容
            _.each(main_body_rows, function (row, index) {
                var tmp_row = $(row)
                var tmp_fixed_row = $(left_fixed_rows.eq(index))
                tmp_fixed_row.css('height', tmp_row.height() + 'px')
                tmp_fixed_row = $(right_fixed_rows.eq(index))
                tmp_fixed_row.css('height', tmp_row.height() + 'px')
            })

            // 右侧固定
            _.each(right_fixed_rows, function (row, index) {
                var tmp_row = $(row)
                var left_fixed_row = $(left_fixed_rows.eq(index))
                left_fixed_row.css('height', tmp_row.height() + 'px')
                var tmp_body_rows = $(main_body_rows.eq(index))
                tmp_body_rows.css('height', tmp_row.height() + 'px')
            })

            // 滚动条打补丁
            var self = this
            setTimeout(function () {
                self.scrollPatch()
            }, 0);
        },

        /**
         * 更新rule
         * @param {*} rule_id
         */
        edit_rule: function (rule_id) {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.rule_info",
                target: 'new',
                res_id: rule_id,
                views: [
                    [false, 'form']
                ],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                }
            });
        },

        // 绑定dom的时候使用
        on_attach_callback: function () {
            var self = this;

            tippy(this.$("[data-toggle='popover']").toArray(), {
                interactive: true,
                appendTo: document.body,
                theme: 'light-border'
            });

            this.$('.start_month').val(this.start_month)
            this.$('.start_month').select2()
            this.$('.end_month').val(this.end_month)
            this.$('.end_month').select2()

            var rd = REDIPS.drag;
            rd.style.borderDisabled = 'solid';
            rd.style.opacityDisabled = 60;

            rd.init(this.$el[0]);

            rd.event.moved = function (event) {
                self.last_operation = "moved"
                self.last_move_obj = rd.obj
            };

            rd.event.dropped = function (event) {
                var target = $(rd.td.target)
                var source = $(rd.td.source)
                // 如果源和目标相同则过滤掉
                if (target == source)
                    return

                var dev_id = target.attr("dev-id")
                var plan_date = target.attr("plan-date")

                source.attr("dev-id", dev_id)

                // 移动, 有rule_title是拖进来的标识
                if (!source.hasClass("rule_title")) {

                    // 移动，更换日期和设备
                    var old_target = $(self.last_move_obj)
                    var old_rule_id = old_target.attr("rule-id")
                    var old_dev_id = old_target.attr("dev-id")
                    var old_plan_date = old_target.attr("plan-date")
                    var new_plan_date = target.attr("plan-date")
                    var rule_info_id = old_target.attr("plan-id")
                    var plan_id = "metro_park_maintenance.year_plan, " + self.year_plan_id
                    self._rpc({
                        "model": "metro_park_maintenance.rule_info",
                        "method": "update_rule_info",
                        "args": [{
                            old_info: {
                                "dev_id": parseInt(old_dev_id),
                                "plan_date": old_plan_date,
                                "rule_id": old_rule_id,
                                "rule_info_id": rule_info_id,
                                "plan_id": plan_id
                            }, new_info: {
                                "dev_id": parseInt(dev_id),
                                "plan_date": new_plan_date,
                                "rule_id": old_rule_id,
                                "data_source": 'year',
                                "plan_id": plan_id
                            }
                        }]
                    }).then(function (rst) {
                        var start_date = old_target.attr("plan-date").split('-')[1]
                        var end_date = target.attr("plan-date").split('-')[1]
                        self._reload_day_plan_count($(self.last_move_obj), 'reduction')
                        self.sync_row_height()
                        self._reload_day_plan_count(target, 'add')
                        self._mobile_reload_month_sumarry(start_date, end_date)
                        var rule_item = $(target.find('.redips-drag'))
                        rule_item.attr("dev-id", dev_id)
                        rule_item.attr("plan-date", plan_date)
                        rule_item.attr("rule-id", self.last_rule_id)
                    })
                } else {
                    // 添加新的规程
                    self._rpc({
                        "model": "metro_park_maintenance.rule_info",
                        "method": "add_plan_info",
                        "args": [{
                            "dev_id": parseInt(dev_id),
                            "plan_date": plan_date,
                            "rule_id": self.last_rule_id,
                            "data_source": "year",
                            "plan_id": "metro_park_maintenance.year_plan, " + self.year_plan_id,
                        }]
                    }).then(function (data) {
                        var rule_item = $(target.find('.redips-drag'))
                        rule_item.attr("dev-id", dev_id)
                        rule_item.attr("plan-date", plan_date)
                        rule_item.attr("rule-id", self.last_rule_id)
                        rule_item.attr("plan-id", data.id)
                        self.sync_row_height();
                        self._reload_day_plan_count(target, 'add')
                        if (self.plan_datas[dev_id + '_' + plan_date]) {
                            self.plan_datas[dev_id + '_' + plan_date].rules =
                                [
                                    {
                                        'id': self.last_rule_id,
                                        'no': data.rule,
                                        'display': data.rule,
                                        'repair_num': 0,
                                        'state': "draft",
                                        'repair_day': 0,
                                        'plan_id': data.plan_id,
                                    }
                                ]

                        } else {
                            self.plan_datas[dev_id + '_' + plan_date] = {
                                'dev': parseInt(dev_id),
                                'date': plan_date,
                                'rules': [
                                    {
                                        'id': self.last_rule_id,
                                        'no': data.rule,
                                        'display': data.rule,
                                        'repair_num': 0,
                                        'state': "draft",
                                        'repair_day': 0,
                                        'plan_id': data.plan_id,
                                    }
                                ]
                            }
                        }
                        self.calculated_monthly_plan()

                    })
                }
            };

            rd.event.cloned = function (cloned) {
                self.last_operation = "cloned"
                var target = $(rd.obj)
                self.last_rule_id = target.attr("rule-id")
            };

            rd.event.deleted = function (event) {
                self._on_del_rule_info(rd.obj)
            };

            // 同步滚动条
            var self = this
            this.$('.right_table_body').on('scroll', function () {
                var othis = $(this)

                var scrollLeft = othis.scrollLeft();
                var scrollTop = othis.scrollTop();

                self.$('.table_header_body').scrollLeft(scrollLeft);
                self.$('.fixed_body_box').scrollTop(scrollTop);
            });

            // 同步表格高度
            var self = this;
            setTimeout(function () {
                self.sync_row_height()
            }, 0);

            $(window).resize(function () {
                self.sync_row_height();
            })
        },

        /**
         * 删除计划信息
         */
        _on_del_rule_info: function (obj) {
            var self = this
            var target = $(obj)
            var old_target = $(self.last_move_obj)
            var dev_id = target.attr("dev-id")
            var rule_id = target.attr("rule-id")
            var plan_date = target.attr("plan-date")
            var rule_info_id = old_target.attr("plan-id")
            self._rpc({
                "model": "metro_park_maintenance.rule_info",
                "method": "del_plan_info",
                "args": [{
                    "dev_id": parseInt(dev_id),
                    "rule_id": parseInt(rule_id),
                    "plan_date": plan_date,
                    "rule_info_id": rule_info_id,
                    'data_source': 'year',
                    "plan_id": "metro_park_maintenance.year_plan, " + self.year_plan_id,
                }]
            }).then(function () {
                self.get_rules(dev_id)
                self.sync_row_height();
                self._reload_day_plan_count(target, 'reduction')
                var del_recs = self.plan_datas[dev_id + '_' + plan_date]
                if (del_recs.rules.length == 1) {
                    delete self.plan_datas[dev_id + '_' + plan_date]
                } else {
                    for (var rule_re in del_re.rules) {
                        if (del_re.rules[rule_re].id == rule_info_id) {
                            self.plan_datas[dev_id + '_' + plan_date].rules.splice(rule_re)
                        }
                    }
                }
                self.calculated_monthly_plan()

            })
        },

        start: function () {
            var self = this
            this._super.apply(this, arguments)
            setTimeout(function () {
                self.calculated_monthly_plan()
            }, 8000)
        },

        /**
         * 重新载入
         */
        _reload: function () {
            var self = this
            this.yPos = this.$('.main_table_box').scrollTop()
            this.xPos = this.$('.main_table_box').scrollLeft()
            this._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_year_plan_info',
                args: [self.year_plan_id, self.start_month, self.end_month]
            }).then(function (res) {
                self.rules = res.rules
                self.plan_datas = res.plan_datas
                self.dates = res.dates
                self.devs = res.devs
                self.repair_counts = res.repair_counts
                // 重新渲染并替换
                self.renderElement();
                self.on_attach_callback();
                self.$('.main_table_box').scrollTop(self.yPos)
                self.$('.main_table_box').scrollLeft(self.xPos)
            })
        },

        _reload_day_plan_count: function (target, method) {
            if (method == 'add') {
                var add_count = 1
            } else {
                var add_count = -1
            }
            var day_el = $('.layui-show div .flex-fill .fixed_right_body > tbody > tr .day_summary')
            var rule_item = $(target.find('.redips-drag'))
            var line = rule_item.context.getAttribute('plan-date')
            for (var date_count in this.dates) {
                if (this.dates[date_count].date == line) {
                    var local_date = date_count
                    break
                }
            }
            var statistical_start_val = day_el.eq(
                parseInt(local_date)).text()
            if (parseInt(statistical_start_val) > -1) {
                day_el.eq(parseInt(local_date)).html(
                    (parseInt(statistical_start_val) + add_count))
            }
        },

        _mobile_reload_month_sumarry: function (start, end) {
            var self = this
            if (start == end) {
                self.calculated_monthly_plan()
            } else {
                var month_el = $('.layui-show div .flex-fill .fixed_right_body > tbody > tr .month_summary')
                for (var style_plan in month_el) {
                    month_el.eq(style_plan).html('')
                }
                self._rpc({
                    model: 'metro_park_maintenance.plan_data',
                    method: 'get_year_plan_info',
                    args: [self.year_plan_id, self.start_month, self.end_month]
                }).then(function (res) {
                    self.plan_datas = res.plan_datas
                    // 重新渲染并替换
                    for (var style_plan in month_el) {
                        month_el.eq(style_plan).html('')
                    }

                    setTimeout(function () {
                        self.calculated_monthly_plan()
                    })
                })
            }
        },

        _reload_month_sumarry: function () {
            var self = this
            var month_el = $('.layui-show div .flex-fill .fixed_right_body > tbody > tr .month_summary')
            self._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_year_plan_info',
                args: [self.year_plan_id]
            }).then(function (res) {
                self.plan_datas = res.plan_datas
                // 重新渲染并替换
                for (var style_plan in month_el) {
                    month_el.eq(style_plan).html('')
                }

                setTimeout(function () {
                    self.calculated_monthly_plan()
                })
            })
        },

        /**
         * 重新计算月份统计
         */
        calculated_monthly_plan: function () {
            var self = this;
            var count_info = {}
            // 统计每天的数据
            for (var i in self.plan_datas) {
                var plan_data = self.plan_datas[i]
                var date = plan_data.date
                var month = date.split('-')[1]
                for (var j = 0; j < plan_data.rules.length; j++) {
                    var rule_info = plan_data.rules[j]
                    var name = self.rule_cache[rule_info.id].name
                    if (month in count_info) {
                        if (name in count_info[month]) {
                            count_info[month][name] += 1
                        } else {
                            count_info[month][name] = 1
                        }
                    } else {
                        // 变量作为字典的key
                        count_info[month] = {
                            [name]: 1
                        }
                    }

                }
            }

            // 每个月的第一个日期标识为site
            for (var i in self.dates) {
                var date = self.dates[i].date
                var month = date.split('-')[1]
                if (month in count_info) {
                    if (!count_info[month]['site']) {
                        count_info[month]['site'] = i
                    }
                }
            }

            // 汇总所有的数据
            for (var key in count_info) {
                count_info[key]['合计'] = 0
                for (var name in count_info[key]) {
                    if (name == 'site') {
                        break
                    }
                    count_info[key]['合计'] += count_info[key][name]
                }
            }

            for (var key in count_info) {
                var el_data = $('.fixed_right_body > tbody > tr .month_summary')
                var repairing = 0
                var repairing_val = 0
                for (var repairing_data in count_info[key]) {
                    if (repairing_data != 'site') {
                        el_data.eq(parseInt(count_info[key].site) + repairing).html(repairing_data)
                        repairing_val = repairing + 1
                        el_data.eq(parseInt(count_info[key].site) + repairing + 1).html(count_info[key][repairing_data])
                        repairing = repairing_val + 1
                    }
                }
            }
        },

        // 取得当年的计划
        willStart: function () {
            var self = this
            return self._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_year_plan_info',
                args: [self.year_plan_id, self.start_month, self.end_month]
            }).then(function (res) {
                self.rules = res.rules
                self.plan_datas = res.plan_datas
                self.dates = res.dates
                self.devs = res.devs
                self.repair_counts = res.repair_counts
                self.months = res.months
                self.state = res.state
                self.rule_cache = res.rule_cache
            })
        },

        /**
         * 取得规程
         * @param {*} dev_id
         * @param {*} date
         */
        get_rules: function (dev_id, date) {
            var key = dev_id.id + "_" + date;
            if (key in this.plan_datas) {
                return this.plan_datas[key]['rules'] || []
            } else {
                return []
            }
        },

        is_holiday: function (plan_date) {
            return plan_date.week == "日" || plan_date.week == "六"
        },

        /**
         * 生成提示信息
         */
        gen_tip_content: function (rule) {
            return qweb.render("metro_park_maintenance.tip-content", {
                rule: rule
            })
        },

        /**
         * 取得某天的年计划
         */
        get_day_rule_count: function (plan_date) {
            var count = 0;
            var self = this
            for (var i = 0; i < this.devs.length; i++) {
                var dev = this.devs[i]
                count += self.get_rules(dev, plan_date).length;
            }
            return count
        },

        /**
         * 查看历史信息
         */
        _on_view_history_info: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.year_plan_history_info",
                context: {
                    "default_plan_id": this.year_plan_id
                },
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    // 重新加载
                    this.trigger_up('reload');
                }
            });
        }
    });

    core.action_registry.add('year_plan_editor_action', year_plan_editor_action);
    return year_plan_editor_action;
});