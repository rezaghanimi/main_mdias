odoo.define('funenc.train_in_out_action', function (require) {
    "use strict";

    var core = require('web.core');

    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var sub_list_widget = require('funenc.sub_list_widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var Dialog = require('web.Dialog');
    var config = require('web.config');

    var qweb = core.qweb;

    var base_plan_controller = ListController.extend({

        start: function () {
            this._super.apply(this, arguments)
            // 表格内部下拉菜单处理
            this.initAbsoluteDropdown(this.$el);
        },

        events: _.extend({}, ListController.prototype.events, {
            "click a[type='action']": "on_menu_click"
        }),

        _updateButtons: function (mode) {
        },

        /**
         * 下拉菜单
         * @param {*} el
         */
        initAbsoluteDropdown: function (el) {
            var dropdown_menu;
            var self = this;
            var dropdown_el 
            el.on("show.bs.dropdown", function (event) {
                event.stopPropagation()
                dropdown_el = $(event.target)
                dropdown_menu = $(event.target).find(".dropdown-menu");
                var $tr = $(dropdown_menu).parents('tr').first()
                var data_id = $tr.data('id')
                $("body").append(dropdown_menu.detach());
                dropdown_menu.css("display", "block");
                dropdown_menu.position({
                    my: "right top",
                    at: "right bottom",
                    of: $(event.relatedTarget)
                })
                // 下拉菜单点击响应
                $(dropdown_menu).find('a[type="action"]').on('click', function (event) {
                    var target = event.target;
                    var model = $(target).data('model')
                    var method = $(target).data('method')
                    if (model && method) {
                        if (data_id) {
                            var record = self.model.get(data_id, { raw: true })
                            var res_id = record.res_id
                            self._rpc({
                                "model": model,
                                "method": method,
                                "args": [res_id]
                            }).then(function (rst) {
                                if (rst) {
                                    self.do_action(rst)
                                } else {
                                    self.trigger_up("reload");
                                }
                            })
                        }
                    }
                })
            })

            el.on("hide.bs.dropdown", function (event) {
                $(event.target).append(dropdown_menu.detach())
                dropdown_menu.hide()
                dropdown_menu = undefined
            }),

            $(document).click(function (event) {
                if(dropdown_menu) {
                    dropdown_el.append(dropdown_menu.detach())
                    dropdown_menu.hide()   
                }
            });
        },

        on_menu_click: function (event) {
            var self = this;
            var target = event.target;
            var model = $(target).data('model')
            var method = $(target).data('method')

            var data_id = $(target).parents("tr").first().data("id")
            if (model && method) {
                if (data_id) {
                    var record = self.model.get(data_id, { raw: true })
                    var res_id = record.res_id
                    self._rpc({
                        "model": model,
                        "method": method,
                        "args": [res_id]
                    }).then(function (rst) {
                        if (rst) {
                            self.do_action(rst)
                        } else {
                            self.trigger_up("reload");
                        }
                    })
                }
            }
            return false
        }
    })

    // 发车列表
    var out_plan_controller = base_plan_controller.extend({});

    // 收车列表
    var back_plan_controller = base_plan_controller.extend({});

    // 日志
    var log_controller = ListController.extend({
        start: function () {
            this._super.apply(this, arguments)
        },
    });

    /**
     * 收发车监控页面
     */
    var train_in_out_plan = AbstractAction.extend(ControlPanelMixin, {
        $buttons: undefined,
        template: 'run_plan_monitor_box',
        view_ids: undefined,
        location_alias: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .add_out_plan": "_add_out_plan",
            "click .add_back_plan": "_add_back_plan",
            "click .publish_plan": "_publish_plan",
            "click .import_run_plan": "_syn_run_chart",
            'click .gen_test_plan_data': "_gen_test_plan_data",
            'click .btn-export-plan': '_export_plan'
        }),

        start: function () {
            this._super.apply(this, arguments);
        },

        /**
         * 取得资源id
         */
        willStart: function () {
            var self = this
            var def = $.Deferred();
            layui.use('laydate', function () {
                def.resolve()
            });
            return def.then(function () {
                return self._rpc({
                    "model": "metro_park_dispatch.day_run_plan",
                    "method": "get_view_ids",
                    "args": []
                })
            }).then(function (rst) {
                self.view_ids = rst
                return self._rpc({
                    "model": "metro_park_dispatch.day_run_plan",
                    "method": "get_cur_location_alias",
                    "args": []
                }).then(function (rst) {
                    self.location_alias = rst
                })
            })
        },

        /**
         * 重新加载发车计划
         */
        _reload_train_out_plan: function () {
            var self = this;
            var value = this.$('.plan_date').val();
            var controller = self.out_plan.get_controller();
            controller.reload(_.extend({ offset: 0 }, {
                domain: [['date', '=', value], ['plan_out_location.alias', '=', this.location_alias]]
            }));
        },

        /**
         * 重新加载收车计划
         */
        _reload_train_back_plan: function () {
            var self = this;
            var value = this.$('.plan_date').val();
            var controller = self.back_plan.get_controller();
            controller.reload(_.extend({ offset: 0 }, {
                domain: [['date', '=', value], ['plan_back_location.alias', '=', this.location_alias]]
            }));
        },

        on_attach_callback: function () {

            // 登亡socketio msg
            this.register_socketio_msg()

            // 车到达转换轨
            window._on_train_arrive = this._on_train_arrive

            // 日期选择框, 默认为当日
            var now = moment();
            var cur_date = now.format('YYYY-MM-DD')
            var laydate = layui.laydate
            laydate.render({
                'elem': this.$('.plan_date')[0],
                'type': 'date',
                'value': now.format('YYYY-MM-DD'),
                'done': function (value, date, endDate) {
                    // 发车计划
                    self._reload_train_out_plan()
                    // 收车计划
                    self._reload_train_back_plan()
                }
            });

            var self = this;
            var top_left_box = this.$el.find(".top_left_box")
            var top_right_box = this.$el.find(".top_right_box");
            var log_box = this.$el.find(".log_box");

            // 发车作业
            this.out_plan = new sub_list_widget(this, {
                'controller_class': out_plan_controller,
                'res_model': 'metro_park_dispatch.train_out_plan',
                'domain': [['date', '=', cur_date], ['plan_out_location.alias', '=', this.location_alias]],
                'list_view_id': this.view_ids.train_out_plan,
                'hide_toolbar': true
            })

            // 收车作业
            this.back_plan = new sub_list_widget(this, {
                'controller_class': back_plan_controller,
                'res_model': 'metro_park_dispatch.train_back_plan',
                'domain': [['date', '=', cur_date], ['plan_back_location.alias', '=', this.location_alias]],
                'list_view_id': this.view_ids.train_back_plan,
                'hide_toolbar': true
            })

            // 日志记录
            this.bottom_list = new sub_list_widget(this, {
                'controller_class': log_controller,
                'res_model': 'metro_park_dispatch.train_in_out_log',
                'list_view_id': this.view_ids.train_in_out_log,
                'hide_toolbar': true
            })

            this.out_plan.appendTo(top_left_box)
            this.back_plan.appendTo(top_right_box)
            this.bottom_list.appendTo(log_box)

            // 渲染
            this._renderButtons();

            this._super.apply(this, arguments);
        },

        /**
         * 处理socketio msg, 需要看到地点
         * @param {*} msg
         */
        deal_socket_io_msg: function (msg) {
            var msg_type = msg.data.msg_type
            var location_alias = msg.data.location_alias
            if (location_alias != this.location_alias) {
                return;
            }
            switch (msg_type) {
                case 'update_train_back_plan_state':
                    this.back_plan.reload();
                    break;

                case 'update_train_out_plan_state':
                    this.out_plan.reload();
                    break;

                case 'plan_status_changed':
                    this.out_plan.reload();
                    this.back_plan.reload();
                    break;
            }
        },

        _add_out_plan: function () {
            var self = this
            self.do_action({
                name: "新增发车",
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'metro_park_dispatch.add_new_out_plan',
                views: [[false, 'form']],
                target: "new",
                domain: []
            }, {
                on_close: function () {
                    self.out_plan.reload();
                    self.bottom_list.reload();
                }
            });
        },

        _add_back_plan: function () {
            var self = this
            self.do_action({
                name: "新增收车",
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                target: "new",
                res_model: 'metro_park_dispatch.add_new_back_plan',
                views: [[false, 'form']],
                domain: []
            }, {
                on_close: function () {
                    self.back_plan.reload();
                    self.bottom_list.reload();
                }
            });
        },

        /**
         * 发布计划, 发布只能发布当前日期的计划
         */
        _publish_plan: function () {
            var value = this.$('.plan_date').val();
            value = moment(value).format('YYYY-MM-DD')
            var self = this
            self._rpc({
                "model": "metro_park_dispatch.day_run_plan",
                "method": "publish_plan",
                "args": [value]
            }).then(function (data){
                self.reload()
            })
        },

        /**
         * 生成测试数据, 生成当天轨道的测试数据
         */
        _gen_test_plan_data: function () {
            var self = this
            this._rpc({
                "model": "metro_park_dispatch.day_run_plan",
                "method": "gen_test_plan_data",
                "args": []
            }).then(function () {
                self.reload()
            })
        },

        _renderButtons: function () {
            this.$buttons = $(qweb.render('train_in_out_btns', {
                debug: config.debug
            }));
            this.$buttons.prependTo(this.$('.btn_box'));
        },

        /**
         * 同步运行图概要
         */
        _syn_run_chart: function () {
            var self = this;
            Dialog.confirm(this, "此功能不考虑检修计划? 请确定是否真的同步", {
                confirm_callback: function () {
                    this.destroy();
                    self.do_action({
                        name: '导入计划',
                        type: 'ir.actions.act_window',
                        view_type: 'form',
                        view_mode: 'form',
                        res_model: "metro_park_dispatch.import_run_plan_wizard",
                        target: 'new',
                        views: [[false, 'form']],
                    }, {
                        size: 'normal',
                        on_close: function (res) {
                            if (!res || res == 'special') {
                                return
                            }
                            // 重新加载
                            self.reload()
                        }
                    });
                }
            });
        },
        reload: function () {
            this.back_plan.reload();
            this.out_plan.reload();
        },
        _export_plan: function () {
            this.do_action({
                name: '导出计划',
                type: 'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: "metro_park_dispatch.wizard.plan_export",
                target: 'new',
                views: [[false, 'form']],
                context: {
                    dialog_size: 'medium'
                }
            });
        }
    });

    core.action_registry.add('train_in_out_plan', train_in_out_plan);

    return train_in_out_plan;
});