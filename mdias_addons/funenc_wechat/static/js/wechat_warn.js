odoo.define('wechat_warn', function (require) {
    "use strict";

    var BasicView = require('web.BasicView');
    var fnt_table_render = require('funenc.fnt_table_render');
    var fnt_table_controller = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var wechat_list_render = fnt_table_render.extend({
        init: function () {
            var self = this;
            this._super.apply(this, arguments);
            self._rpc({
                model: 'funenc.wechat.account',
                method: 'is_syning'
            }).then(function (data) {
                if (data) {
                    var timing_tasks = function () {
                        self._rpc({
                            model: 'funenc.wechat.account',
                            method: 'is_syning'
                        }, {
                            shadow:true
                        }).then(function (data) {
                            var result = $(self.$el.children("div").get(0)).hasClass('right_top');
                            if (data) {
                                if (!result) {
                                    self.$el.prepend('<div class="right_top" style="color: red;font-size:15px;padding-left: 15px;">正在同步中...!</div>')
                                }
                            } else {
                                if (result) {
                                    $(self.$el.children("div").get(0)).html('同步完成!');
                                    window.clearInterval(window.setInterval(timing_tasks, 15000));
                                }
                            }
                        });
                    };
                    setInterval(timing_tasks, 15000);
                }
            })
        },

        on_attach_callback: function () {
            this.$el.addClass('wechat_account');
        },

        _renderButton: function (record, node) {
            var self = this;
            var $button = this._renderButtonFromNode(node, {
                extraClass: node.attrs.icon ? 'o_icon_button' : undefined,
                textAsTitle: !!node.attrs.icon
            });
            this._handleAttributes($button, node);
            this._registerModifiers(node, record, $button);

            if (record.res_id) {
                $button.on("click", function (e) {
                    e.stopPropagation();
                    if (node.attrs.name !== 'sync_wechat') {
                        self.trigger_up('button_clicked', {
                            attrs: node.attrs,
                            record: record
                        });
                    } else {
                        self.trigger_up('button_clicked', {
                            attrs: node.attrs,
                            record: record
                        });
                        var timing_tasks = function () {
                            self._rpc({
                                model: 'funenc.wechat.account',
                                method: 'is_syning'
                            }, {
                                shadow:true
                            }).then(function (data) {
                                var result = $(self.$el.children("div").get(0)).hasClass('right_top');
                                if (data) {
                                    if (!result) {
                                        self.$el.prepend('<div class="right_top" style="color: red;font-size:15px;padding-left: 15px;">正在同步!</div>')
                                    }
                                } else {
                                    if (result) {
                                        $(self.$el.children("div").get(0)).html('同步完成!');
                                        window.clearInterval(window.setInterval(timing_tasks, 15000));
                                    }
                                }
                            });
                        };
                        window.setInterval(timing_tasks, 15000);
                    }
                });
            } else {
                if (node.attrs.options.warn) {
                    $button.on("click", function (e) {
                        e.stopPropagation();
                        self.do_warn(_t("Warning"), _t('Please click on the "save" button first.'));
                    });
                } else {
                    $button.prop('disabled', true);
                }
            }

            return $button;
        }
    });

    var wechat_list_controller = fnt_table_controller.extend({
        init: function () {
            this._super.apply(this, arguments);
        }
    });

    var wechat_warn = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: wechat_list_render,
            Controller: wechat_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('wechat_warn', wechat_warn);

    return wechat_warn;
});
