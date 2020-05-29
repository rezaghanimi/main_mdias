/**
 * 月计划详情
 */
odoo.define('metro_park.month_month_plan_editor', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var utility = require('metro_park_maintenance.utility')

    var month_month_plan_editor = AbstractAction.extend({
        rules: [],
        plan_datas: [],
        devs: [],
        repair_counts: [],
        template: 'month_plan_editor',

        last_rule_id: undefined,
        last_operation: undefined,
        last_move_obj: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .recompute": "on_click_compute",
            "click .plan_work_class": "_on_compute_plan_work_class",
            "click .clear_month_data": "_on_clear_plan",
            "click .import_month_plan": "_on_import_plan",
            "click .download_plan_template": "_on_download_template",
            "click .history_info": "_on_view_history_info",
            "click .syn_year_info": "_on_syn_year_info",
            "click .view_delta": "_on_view_delta",
            "click .clear_duplicate": "_on_clear_duplicate",
            "click .import_work_class_info": "_on_import_work_class_info"
        }),

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.month_plan_id = action.context.active_id || action.params.active_id
        },

        _on_view_history_info: function () {
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.year_plan_history_info",
                context: {},
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
        },

        /**
         * 同步年计划信息
         */
        _on_syn_year_info: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "syn_year_info",
                "args": [this.month_plan_id]
            }).then(function (rst) {
                self._reload()
            })
        },

        /**
         * 清除计划
         */
        _on_clear_plan: function () {
            var self = this
            this.do_action({
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_maintenance.month_plan_clear_wizard",
                target: 'new',
                views: [[false, 'form']],
            }, {
                on_close: function (res) {
                    if (!res || res == 'special') {
                        return
                    }
                    var res_id = res.res_id
                    self._rpc({
                        "model": "metro_park_maintenance.month_plan_clear_wizard",
                        "method": "clear_month_and_week_datas",
                        "args": [res_id, self.month_plan_id]
                    }).then(function (rst) {
                        self._reload()
                    })
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
                    "month_plan_id": this.month_plan_id
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

        is_holiday: function (plan_date) {
            return plan_date.week == "日" || plan_date.week == "六"
        },

        /**
         * 下载模板
         */
        _on_download_template: function () {
            this.do_action({
                'type': 'ir.actions.act_url',
                'url': '/metro_park_maintenance/get_month_plan_template',
            })
        },

        /**
         * 安排工班
         */
        _on_compute_plan_work_class: function () {
            var self = this
            return self._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "get_plan_work_class_data",
                "args": [this.month_plan_id]
            }).then(function (rst) {
                var calc_host = rst.calc_host || "ws://127.0.0.1:9520"
                if (!_.str.startsWith('ws://')) {
                    calc_host = "ws://" + calc_host
                }
                return utility.do_plan_by_websocket(calc_host, {
                    "cmd": "plan_work_class",
                    "data": rst
                }).then(function (calc_rst) {
                    return {
                        "plan_data": rst,
                        "calc_rst": calc_rst
                    }
                })
            }).then(function (rst) {
                return self._rpc({
                    "model": "metro_park_maintenance.month_plan",
                    "method": "deal_plan_work_class_result",
                    "args": [rst.plan_data, rst.calc_rst]
                })
            }).then(function () {
                self._reload()
            });
        },

        /**
         * 重新计算月计划
         */
        on_click_compute: function () {
            var self = this
            // 弹出向导框
            this._rpc({
                "model": "metro_park_maintenance.month_plan_compute_wizard",
                "method": "get_default_info",
                "args": [self.month_plan_id]
            }).then(function (info) {
                // 向导
                var def = $.Deferred()
                self.do_action({
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: "metro_park_maintenance.month_plan_compute_wizard",
                    target: 'new',
                    context: {
                        "default_work_class_count": info.work_class_count,
                        "default_calc_host": info.calc_host,
                        "default_plan_kt": info.plan_kt,
                        "default_kt_month": info.plan_kt_month
                    },
                    views: [
                        [false, 'form']
                    ],
                }, {
                    on_close: function (res) {
                        if (!res || res == 'special') {
                            def.reject("计算取消！")
                            return
                        }
                        def.resolve(res)
                    }
                });
                return def
            }).then(function (res) {
                // 传入向导数据id
                return self._rpc({
                    "model": "metro_park_maintenance.month_plan",
                    "method": "get_month_plan_data",
                    "args": [self.month_plan_id, res.res_id]
                })
            }).then(function (rst) {
                var calc_host = rst.calc_host || "ws://127.0.0.1:9520"
                if (!_.str.startsWith('ws://')) {
                    calc_host = "ws://" + calc_host
                }
                return utility.do_plan_by_websocket(calc_host, {
                    "cmd": "plan_month",
                    "data": rst
                }).then(function (result) {
                    return {
                        "plan_data": rst,
                        "result": result
                    }
                });
            }).then(function (rst) {
                return self._rpc({
                    "model": "metro_park_maintenance.month_plan",
                    "method": "deal_month_plan_data",
                    "args": [self.month_plan_id, rst.plan_data, rst.result]
                })
            }).then(function () {
                self.do_warn('提示', '月计划生成成功!', true);
                self._reload();
            }).fail(function (error) {
                self.do_warn('提示', '计算出错!' + error, true);
            })
        },

        sync_row_height: function () {

            var main_body_rows = this.$('.main_table tr')
            var left_fixed_rows = this.$('.fixed_left_body tr')
            var right_fixed_rows = this.$('.fixed_right_body tr')

            _.each(main_body_rows, function (row, index) {
                var tmp_row = $(row)
                var tmp_fixed_row = $(left_fixed_rows.eq(index))
                tmp_fixed_row.css('height', tmp_row.height() + 'px')
                tmp_fixed_row = $(right_fixed_rows.eq(index))
                tmp_fixed_row.css('height', tmp_row.height() + 'px')
            })

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

        _on_rd_dropped: function () {
            var self = this

            var rd = REDIPS.drag;
            var target = $(rd.td.target)
            var source = $(rd.td.source)

            // 如果源和目标相同则过滤掉
            if (target == source)
                return

            var dev_id = target.attr("dev-id")
            var plan_date = target.attr("plan-date")

            source.attr("dev-id", dev_id)

            var rule_id = $(self.last_move_obj).attr("rule-id")
            if (!source.hasClass("rule_title")) {
                var old_target = $(self.last_move_obj)
                var old_rule_id = self.last_rule_id
                var old_dev_id = target.attr("dev-id")
                var old_plan_date = target.attr("plan-date")
                var plan_id = "metro_park_maintenance.month_plan, " + self.month_plan_id
                var rule_info_id = old_target.attr("plan-id")
                self._rpc({
                    "model": "metro_park_maintenance.rule_info",
                    "method": "update_rule_info",
                    "args": [{
                        old_info: {
                            "dev_id": parseInt(old_dev_id),
                            "plan_date": old_plan_date,
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
                    self.sync_row_height()
                    self._deal_day_count($(self.last_move_obj), 'reduction')
                    self._deal_day_count(target, 'add')

                    var rule_item = $(target.find('.redips-drag'))
                    rule_item.attr("dev-id", dev_id)
                    rule_item.attr("plan-date", plan_date)
                    rule_item.attr("rule-id", self.last_rule_id)

                    self._reload().then(function () {
                        self._calc_every_day_plan_count()
                    })

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
                        "data_source": "month",
                        "plan_id": "metro_park_maintenance.month_plan, " + self.month_plan_id,
                    }]
                }).then(function (data) {
                    var rule_item = $(target.find('.redips-drag'))
                    rule_item.attr("dev-id", dev_id)
                    rule_item.attr("plan-date", plan_date)
                    rule_item.attr("rule-id", self.last_rule_id)
                    rule_item.attr("plan-id", data.id)
                    self.sync_row_height();
                    self._deal_day_count(target, 'add')
                    self._calc_month_summary()
                    self._calc_every_day_plan_count()
                })
            }
        },

        // 绑定dom的时候使用
        on_attach_callback: function () {

            var self = this;

            var rd = REDIPS.drag;
            rd.style.borderDisabled = 'solid';
            rd.style.opacityDisabled = 60;

            rd.init(this.$el[0]);

            rd.event.moved = function (event) {
                self.last_operation = "moved"
                self.last_move_obj = rd.obj
            };

            rd.event.dropped = _.bind(this._on_rd_dropped, this)
            rd.event.cloned = function (cloned) {
                self.last_operation = "cloned"
                var target = $(rd.obj)
                self.last_rule_id = target.attr("rule-id")
            };

            rd.event.deleted = function (event) {
                self._on_del_rule_info(rd.obj)
                // self._reload_month_sumarry()
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

            // 计算每一天的汇总
            this._calc_month_summary()
            this._calc_every_day_plan_count()
        },

        _calc_month_summary: function () {
            // 清除汇总
            var month_el = this.$('tr .month_summary')
            for (var style_plan in month_el) {
                month_el.eq(style_plan).html('')
            }

            var count_info = {}
            for (var plan_date in this.plan_datas) {
                var plan_data = this.plan_datas[plan_date]
                for (var rule = 0; rule < plan_data.rules.length; rule++) {
                    var rule_info = plan_data.rules[rule]
                    var name = rule_info.rule_no
                    if (name in count_info) {
                        count_info[name] += 1
                    } else {
                        count_info[name] = 1
                    }
                }
            }

            // 汇总所有的数据
            count_info['合计'] = 0
            for (var key in count_info) {
                if (key == '合计') {
                    break
                }
                count_info['合计'] += count_info[key]
            }

            var repairing = 0
            var repairing_val = 0
            for (var key in count_info) {
                month_el.eq(parseInt(repairing)).html(key)
                repairing_val = repairing + 1
                month_el.eq(parseInt(repairing + 1)).html(count_info[key])
                repairing = repairing_val + 1
            }
        },

        _calc_every_day_plan_count: function () {
            var self = this;
            var el_day_date_summary = this.$('.date_summary')
            var day_summary_count = this.$('.day_summary_count')
            day_summary_count.eq(0).html('')
            for (var el_dau in el_day_date_summary) {
                el_day_date_summary.eq(el_dau).html('')
            }
            var date_summary = {}
            for (var date_data in self.dates) {
                for (var plan in self.plan_datas) {
                    if (self.dates[date_data].date == self.plan_datas[plan].date) {
                        for (var rule in self.plan_datas[plan].rules) {
                            if (Object.keys(date_summary).length == 0) {
                                date_summary[date_data] = 1
                            } else {
                                if (date_data in date_summary) {
                                    date_summary[date_data] += 1
                                } else {
                                    date_summary[date_data] = 1
                                }
                            }
                        }
                    }
                }
            }

            // 汇总
            var summary_sum = 0
            for (var summary_date in date_summary) {
                summary_sum += date_summary[summary_date]
            }

            for (var data in date_summary) {
                el_day_date_summary.eq(data).html(date_summary[data])
            }
            day_summary_count.eq(0).html(summary_sum)
        },

        // 汇总当日的数量
        _deal_day_count: function (target, method) {
            if (method == 'add') {
                var add_count = 1
            } else {
                var add_count = -1
            }
            var day_el = this.$('tr .day_summary')
            var rule_item = $(target.find('.redips-drag'))
            var line = rule_item.context.getAttribute('dev-id')
            for (var date_count in this.devs) {
                if (date_count == line - 1) {
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

        /**
         * 删除计划信息
         */
        _on_del_rule_info: function (obj) {
            var self = this
            var target = $(obj)
            var old_target = $(self.last_move_obj)
            var rule_item = $(target.find('.redips-drag'))
            var dev_id = target.attr("dev-id")
            var rule_id = target.attr("rule-id")
            var plan_date = target.attr("plan-date")
            var rule_info_id = old_target.attr("plan-id")
            rule_item.attr("dev-id", dev_id)
            rule_item.attr("plan-date", plan_date)
            rule_item.attr("rule-id", self.last_rule_id)
            this._rpc({
                "model": "metro_park_maintenance.rule_info",
                "method": "del_plan_info",
                "args": [{
                    "dev_id": parseInt(dev_id),
                    "rule_id": parseInt(rule_id),
                    "plan_date": plan_date,
                    "rule_info_id": rule_info_id,
                    'data_source': 'month',
                    "plan_id": self.month_plan_id,
                }]
            }).then(function () {
                self._deal_day_count(target, 'reduction')
                self._calc_month_summary()
                self._calc_every_day_plan_count()
                self.sync_row_height();
            })
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        format_date: function (date) {
            return moment(date).date()
        },

        /**
         * 重新载入
         */
        _reload: function () {
            var self = this
            return this._rpc({
                model: 'metro_park_maintenance.plan_data',
                method: 'get_month_plan_info',
                args: [self.month_plan_id]
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

        // 获取月计划数据
        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    model: 'metro_park_maintenance.plan_data',
                    method: 'get_month_plan_info',
                    args: [self.month_plan_id]
                }).then(function (res) {
                    self.rules = res.rules
                    self.plan_datas = res.plan_datas
                    self.dates = res.dates
                    self.devs = res.devs
                    self.repair_counts = res.repair_counts
                    self.state = res.state
                })
            })
        },

        /**
         * 取得规程
         * @param {*} dev_id
         * @param {*} date
         */
        get_rules: function (dev, date) {
            var key = dev.id + "_" + date;
            if (key in this.plan_datas) {
                return this.plan_datas[key]['rules'] || []
            } else {
                return []
            }
        },

        get_counts_data: function (data) {
            var lis = []
            for (var plan_data in this.plan_datas) {
                if (this.plan_datas[plan_data].dev == data) {
                    for (var rule in this.plan_datas[plan_data].rules) {
                        lis.push(rule)
                    }
                }
            }
            if (lis) {
                return lis
            } else {
                return []
            }
        },

        get_counts: function (data) {
            var self = this
            var count = self.get_counts_data(data);
            return count.length
        },

        _on_view_delta: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "view_delta",
                "args": [this.month_plan_id]
            }).then(function (rst) {
                self.do_action(rst)
            })
        },

        /**
         * 清除重复的项
         */
        _on_clear_duplicate: function () {
            var self = this;
            this._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "clear_duplicate",
                "args": [self.month_plan_id]
            }).then(function (rst) {
                self._reload()
            })
        },

        /**
         * 导入生产说明
         */
        _on_import_work_class_info: function () {
            var self = this
            this._rpc({
                "model": "metro_park_maintenance.month_plan",
                "method": "import_work_class_info",
                "args": [this.month_plan_id]
            }).then(function (rst) {
                self.do_action(rst, {
                    on_close: function (res) {
                        self._reload()
                    }
                })
            }).fail(function (rst) {
                self.do_warn('提示', '导入生产说明失败!', true);
            })
        }
    });

    core.action_registry.add('month_month_plan_editor', month_month_plan_editor);
    return month_month_plan_editor;
});