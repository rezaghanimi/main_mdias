odoo.define("funenc.tree_button", function (require) {
    "use strict";

    var Widget = require("web.Widget");
    var registry = require("web.widget_registry");
    var listRenderer = require("web.ListRenderer");
    var core = require("web.core");
    var Dialog = require('web.Dialog');

    listRenderer.include({
        _renderHeaderCell: function (node) {
            var name = node.attrs.name;
            var field = this.state.fields[name];
            var $th = $("<th>");
            if (!field) {
                if ((name === "treebtns")) {
                    $th.text(node.attrs.string).data("name", node.attrs.string);
                }
                return $th;
            }
            return this._super.apply(this, arguments)
        }
    });

    var TreeButtons = Widget.extend({
        events: _.extend(Widget.prototype.events, {
            "click button.sign_button": "signClick"
        }),
        init: function (parent, record, node) {
            this._super(parent);
            this.record = record;
            this.attrs = node.attrs;

            this.template = this.attrs.template;
            if (!this.template) {
                console.log(
                    "the template for template widget is undfined, please set the template attrs"
                );
            }
        },

        disable_btns: function () {
            this.$('button').attr('disabled', true);
        },

        enable_btns: function () {
            this.$('button').removeAttr('disabled');
        },

        // 按钮触发
        trigger_button: function (e) {
            e.stopPropagation();
            var self = this;
            var controller = this.getParent().getParent();

            if (controller._callButtonAction) {
                var param = {
                    type: $(e.currentTarget).attr("type"),
                    name: $(e.currentTarget).attr("name"),
                    context: {}
                };
                if ($(e.currentTarget).attr("context")) {
                    param.context = JSON.parse($(e.currentTarget).attr("context"));
                }
                if (param.context && this.record.data._compute_task_id) {
                    param.context.taskKeys = [
                        [this.record.res_id, this.record.data._compute_task_id]
                    ];
                }

                self.disable_btns();
                controller._callButtonAction(param, this.record).then(function (rst) {
                    core.bus.trigger("update_bage_num");
                    if (!rst) {
                        self.trigger_up("reload");
                    } else if (rst.action) {
                        // 查找哪些是通过action来重新加载的
                        self.trigger_up("reload");
                    } else if (rst.reload) {
                        // 让列表重新加载而不是当前这条数据重新加载
                        controller.reload({domain: rst.reload.domain});
                    }
                    self.enable_btns();
                }).fail(function () {
                    self.enable_btns();
                });
            } else {

                self.trigger_up("button_clicked", {
                    attrs: {
                        type: $(e.currentTarget).attr("type"),
                        name: $(e.currentTarget).attr("name")
                    },
                    record: this.record
                });
            }
        },


        confirmClick: function (e) {
            var self = this;
            var confirm  = $(e.currentTarget).attr("confirm");
            e.stopPropagation();
            var disabled = false;
            Dialog.confirm(self, confirm, {
                title: '提示',
                confirm_callback: function () {
                    if (!disabled) {
                        disabled = true;
                        self.trigger_button(e);
                    }
                },
                cancel_callback: function () {

                }
            });
        },


        start: function () {
            this._super();
            var serverbtns = [];
            var confirmBtns = [];
            this.$("button").each(function (index, item) {
                if (!$(item).attr("js_func")) {
                    if ($(item).attr("confirm")) {
                        confirmBtns.push(item);
                    } else {
                        serverbtns.push(item);
                    }
                }
                if ($(item).hasClass("tippy-btn")) {
                    serverTipBnts.push(item);
                }
            });
            $(serverbtns).on("click", this.trigger_button.bind(this));
            $(confirmBtns).on("click", this.confirmClick.bind(this));
        },
        renderElement: function () {
            var $el;
            var self = this;
            if (this.template) {
                $el = $(core.qweb.render(this.template, {widget: this}).trim());
            } else {
                $el = this._makeDescriptive();
            }
            $el.find("button").each(function (index, item) {
                var groups = $(item).attr("groups");
                var defer;
                if (groups) {
                    defer = self._rpc({
                        model: 'res.users',
                        method: 'user_has_groups',
                        args: [groups]
                    });
                } else {
                    defer = $.Deferred().resolve(true);
                }
                defer.then(function (has_group) {
                    if (has_group) {
                        return true
                    } else {
                        item.remove()
                    }
                });
            });

            this._replaceElement($el);
        },

    });

    registry.add("TreeButtons", TreeButtons);

    return {
        TreeButtons: TreeButtons
    };
});
