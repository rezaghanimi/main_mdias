odoo.define('funenc.dispatch_plan_cmd_action', function (require) {
    "use strict";

    var core = require('web.core');

    var ListController = require('web.ListController');
    var AbstractAction = require('web.AbstractAction');
    var sub_list_widget = require('funenc.sub_list_widget');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    var qweb = core.qweb;

    var base_plan_controller = ListController.extend({
        start: function () {
            this._super.apply(this, arguments)
            // 表格内部下拉菜单处理
            this.initAbsoluteDropdown(this.$el);
        },

        initAbsoluteDropdown: function (el) {
            var dropdown_menu;
            var self = this;
            el.on("show.bs.dropdown", function (event) {
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
                            var record = self.model.get(data_id, {raw: true})
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
            })
        },
    })

    var in_out_plan_controller = base_plan_controller.extend({

    });

    var dispatch_controller = base_plan_controller.extend({

    });

    /**
     * 调车计划管理, 包括收发车计划和调车计划
     */
    var dispatch_plan_cmd_action = AbstractAction.extend(ControlPanelMixin, {
        template: 'dispatch_instructions_box',
        top_list: undefined,
        bottom_list: undefined,
        $buttons: undefined,

        start: function () {
            this._super.apply(this, arguments)

            var top_left_box = this.$(".top_left_box")
            var top_right_box = this.$(".top_right_box");

            //收发车计划指令
            this.in_out_plan = new sub_list_widget(this, {
                'controller_class': in_out_plan_controller,
                'domain': [['dispatch_type', 'in', ['in_plan', 'out_plan']]],
                'res_model': 'metro_park_dispatch.dispatch_plan_cmd'
            })
            this.in_out_plan.appendTo(top_left_box)

            // 调车计划指令
            this.dispatch = new sub_list_widget(this, {
                'controller_class': dispatch_controller,
                'domain': [['dispatch_type', '=', 'dispatch']],
                'res_model': 'metro_park_dispatch.dispatch_plan_cmd'
            })
            this.dispatch.appendTo(top_right_box)

            // 控制面版
            this._renderButtons();
            this._updateControlPanel();
        },

        do_show: function () {
            this._updateControlPanel();
        },

        _renderButtons: function () {
            this.$buttons = $(qweb.render('dispatch_plan_btns'));
        },

        _updateControlPanel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        }
    });

    core.action_registry.add('dispatch_plan_cmd_action', dispatch_plan_cmd_action);

    return dispatch_plan_cmd_action;
});