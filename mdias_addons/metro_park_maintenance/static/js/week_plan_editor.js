/**
 * 周计划编辑
 */
odoo.define('metro_park.week_plan_editor', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var utility = require('metro_park_maintenance.utility')

    var week_plan_editor = AbstractAction.extend({
        rules: [],
        plan_datas: [],
        devs: [],
        repair_counts: [],
        template: 'week_plan_editor',

        // 记录相关操作
        last_rule_id: undefined,
        last_operation: undefined,
        last_move_obj: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .recompute": "_on_recompute_btn_click",
            "click .clear_week_data": "_on_clear_plan",
            "click .import_month_plan": "_on_import_plan",
            "click .download_plan_template": "_on_download_template",
            "click .dev_item": "_on_dev_item_click",
            "click .history_info": "_on_view_history_info",
            "click .get_month_plan_data": "_get_month_plan_data",
            "click .syn_month_info": "_on_syn_month_info",
            "click .clear_week_info": "_on_clear_week_plan"
        }),

        /**
         * 初始化
         * @param {*} parent
         * @param {*} action
         */
        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.week_plan_id = action.context.week_plan_id || action.params.active_id
        },

        /**
         * 同步月计划信息
         */
        _on_syn_month_info: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.week_plan",
                "method": "syn_month_info",
                "args": [this.week_plan_id]
            }).then(function (rst) {
                self._reload()
            })
        },

        /**
         * 清除周计划
         */
        _on_clear_week_plan: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.week_plan",
                "method": "clear_week_data",
                "args": [this.week_plan_id]
            }).then(function (rst) {
                self._reload()
            })
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

        /**
         * 格式化日期
         * @param {*} date_str
         */
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

        /**
         *
         * 导入计划
         */
        _on_import_plan: function () {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.month_plan_import_wizard",
                target: 'new',
                context: {
                    "week_plan_id": this.week_plan_id
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
                'url': '/metro_park_maintenance/get_week_plan_template',
            })
        },

        /**
         * 先弹出让用户选择月份
         */
        _on_recompute_btn_click: function () {
            var self = this
            $.when(this._rpc({
                "model": "metro_park_maintenance.week_plan",
                "method": "get_compute_host",
                "args": []
            })).then(function (calc_host) {
                var info = {}
                info.week_plan_id = self.week_plan_id
                info.detail_id = self.week_plan_id
                info.calc_host = calc_host
                return self._rpc({
                    "model": "metro_park_maintenance.week_plan",
                    "method": "get_week_plan_compute_data",
                    "args": [info]
                }).then(function (rst) {
                    var data = rst.data
                    var calc_host = data.calc_host
                    if (!_.str.startsWith(calc_host, "ws://")) {
                        calc_host = "ws://" + calc_host
                    }
                    return utility.do_plan_by_websocket(calc_host, rst).then(function (rst) {
                        return {
                            calc_result: rst,
                            plan_info: data
                        }
                    });
                }).then(function (rst) {
                    return self._rpc({
                        "model": "metro_park_maintenance.week_plan",
                        "method": "deal_compute_result",
                        "args": [rst.plan_info, rst.calc_result]
                    })
                }).then(function () {
                    self.do_warn('提示', '周计划生成成功!', true);
                    self._reload()
                }).fail(function (error) {
                    self.do_warn('提示', '计算出错!' + error, true);
                })
            })
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

            // tip提示
            this.$("[data-toggle='popover']").popover({
                "trigger": "hover",
                "placement": "top",
                "html": true
            });

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

                // source上面不会带rule_id, 一个td上有多个rule
                var rule_id = self.last_rule_id

                source.attr("dev-id", dev_id)

                // 移动, 有rule_title是拖进来的标识
                if (!source.hasClass("rule_title")) {
                    // 移动，更换日期和设备
                    var old_target = $(self.last_move_obj)
                    var old_rule_id = self.last_rule_id
                    var old_dev_id = target.attr("dev-id")
                    var plan_id = "metro_park_maintenance.year_plan, " + self.year_plan_id
                    var rule_info_id = old_target.attr("plan-id")

                    self._rpc({
                        "model": "metro_park_maintenance.rule_info",
                        "method": "update_rule_info",
                        "args": [{
                            old_info: {
                                "dev_id": parseInt(old_dev_id),
                                "plan_date": old_target.attr("plan-date"),
                                "rule_id": parseInt(old_rule_id),
                                "rule_info_id": rule_info_id,
                                "plan_id": parseInt(plan_id)
                            }, new_info: {
                                "dev_id": parseInt(dev_id),
                                "plan_date": plan_date,
                                "rule_id": parseInt(rule_id),
                                "plan_id": parseInt(plan_id)
                            }
                        }]
                    }).then(function (rst) {
                        self.get_rules(dev_id)
                        self.sync_row_height();
                        self._reload_day_plan_count(old_target, 'reduction')
                        self._reload_month_sumarry(old_target.attr("plan-date"))
                        self._reload_day_plan_count(target, 'add')
                        self._reload_month_sumarry(plan_date)
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
                            "data_source": "week",
                            "plan_id": "metro_park_maintenance.week_plan, " + dev_id,
                        }]
                    }).then(function (data) {
                        var rule_item = $(target.find('.redips-drag'))
                        rule_item.attr("dev-id", dev_id)
                        rule_item.attr("plan-date", plan_date)
                        rule_item.attr("rule-id", self.last_rule_id)
                        rule_item.attr("plan-id", data.id)
                        self.sync_row_height();
                        self._reload_day_plan_count(target, 'add')
                        self._reload_month_sumarry(plan_date)
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
         * 取得月计划数据
         */
        _get_month_plan_data: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.year_plan_detail",
                "method": "get_month_data",
                "args": [this.week_plan_id]
            }).then(function (rst) {
                self._reload()
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

            this._rpc({
                "model": "metro_park_maintenance.rule_info",
                "method": "del_plan_info",
                "args": [{
                    "dev_id": parseInt(dev_id),
                    "rule_id": parseInt(rule_id),
                    "plan_date": plan_date,
                    "rule_info_id": rule_info_id,
                    'data_source': 'week',
                    "plan_id": "metro_park_maintenance.week_plan, " + dev_id,
                }]
            }).then(function () {
                self.get_rules(dev_id)
                self.sync_row_height();
                self._reload_day_plan_count(target, 'reduction')
                self._reload_month_sumarry(plan_date)
            })
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        /**
         * 重新载入
         */
        _reload: function () {
            var self = this
            this._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_week_plan_info',
                args: [self.week_plan_id]
            }).then(function (res) {
                self.rules = res.rules
                self.plan_datas = res.plan_datas
                self.dates = res.dates
                self.devs = res.devs
                self.repair_counts = res.repair_counts
                // 重新渲染并替换
                self.renderElement();
                self.on_attach_callback();
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

        _reload_month_sumarry: function (plan_date) {
            var self = this
            self._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_week_plan_info',
                args: [self.week_plan_id]
            }).then(function (res) {
                console.log(res)
                self.plan_datas = res.plan_datas
                setTimeout(function () {
                    self.calculated_week_plan(plan_date)
                })
            })
        },

        /**
         * 重新计算周计划统计
         */
        calculated_week_plan: function (plan_date) {
            var self = this;
            var str_summary_count = self.get_week_summary(plan_date)
            var week_element = $('.layui-show div .flex-fill .fixed_right_body > tbody > tr .week_summary')
            for (var date in self.dates) {
                if (self.dates[date].date == plan_date) {
                    week_element.eq(date).html(str_summary_count)
                    break
                }
            }

        },

        // 取得当年的计划
        willStart: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    model: 'metro_park_maintenance.plan_data',
                    method: 'get_week_plan_info',
                    args: [self.week_plan_id]
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
            return "<div class='rule_info_tip'><p>修次:" + rule.repair_num + "</p>" +
                "<p>第" + rule.repair_day + "天</p></div>"
        },

        get_week_summary: function (plan_date) {
            var self = this
            var summary_count = {}
            for (var plan_data in self.plan_datas) {
                var date = plan_data.split('_')[1]
                if (date == plan_date) {
                    for (var rule in self.plan_datas[plan_data].rules) {
                        if (self.plan_datas[plan_data].rules[rule].no in summary_count) {
                            summary_count[self.plan_datas[plan_data].rules[rule].no] += 1
                        } else {
                            summary_count[self.plan_datas[plan_data].rules[rule].no] = 1
                        }

                    }

                }
            }
            // 汇总
            summary_count['总数'] = 0
            for (var total in  summary_count) {
                if (total == '总数') {
                    break
                }
                summary_count['总数'] += summary_count[total]
            }
            var str_summary_count = ''
            for (var str in summary_count) {
                str_summary_count += str + ':' + summary_count[str] + ' '
            }
            return str_summary_count
        },

        /**
         * 清除计划
         */
        _on_clear_plan: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.week_plan",
                "method": "clear_plan_data",
                "args": [this.week_plan_id]
            }).then(function (rst) {
                self._reload()
            })
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
                    "default_plan_id": "metro_park_maintenance.year_plan, " + this.year_plan_id
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

    core.action_registry.add('week_plan_editor', week_plan_editor);
    return week_plan_editor;
});