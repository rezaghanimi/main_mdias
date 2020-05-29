odoo.define('funenc.custom_search_pannel', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var py_utils = require('web.py_utils');
    var widgetRegistry = require('web.widget_registry');
    var searchExtend = require('funenc.search_extend');

    var custom_search_pannel = Widget.extend({

        // 提供了默认的行为绑定
        events: {
            'click .search_extend_reset': 'reset_search',
            'click .search_extend_apply': 'commit_search',
            'keyup .o_searchview_extended_prop_value': function (ev) {
                if (ev.which === $.ui.keyCode.ENTER) {
                    this.commit_search();
                }
            },
        },

        reset_search: function () {

            _.each(this.search_fields, function (search_field) {
                if (search_field.reset) {
                    search_field.reset()
                }
            })

            // flag中没有search_view的时候不显示搜索
            if (this.search_view) {
                this.search_view.query.reset();
            } else {
                this.commit_search();
            }
        },

        init: function (parent, fields, pannel_template, search_view) {
            this.fields = fields;
            this.pannel_template = pannel_template;
            this.search_view = search_view
            this.search_fields = []
            this._super(parent, arguments);
        },

        /**
         * 读取模板，同时读取属性并构造搜索对象
         */
        start: function () {
            this._super.apply(this, arguments)
            var $el;
            // 查看是否有默认搜索，区别于odoo自带的用_开头
            var _searchDefaults = {};
            if (this.search_view) {
                _.each(this.search_view.action.context, function (value, key) {
                    var match = /^_search_default_(.*)$/.exec(key);
                    if (match) {
                        _searchDefaults[match[1]] = value;
                    }
                });
                this.search_view._search_defaults = _searchDefaults;
            }
            if (this.pannel_template) {
                $el = $(core.qweb.render(this.pannel_template, {
                    widget: this
                }).trim());
                var fields_place_holders = $el.find("[for]")
                for (var i = 0; i < fields_place_holders.length; i++) {
                    var holder = fields_place_holders[i]

                    // 如果有名称的话则使用字段，如果没有的话则自定义
                    var filed_name = $(holder).attr('for')

                    var option = $(holder).attr('option') || "{}"
                    option = py_utils.py_eval(option)

                    var field = this.fields[filed_name]
                    if (field) {
                        var type = field.type;
                        option.name = filed_name;
                        // 生成组件
                        var FiledClass = searchExtend.funenc_search_registry.getAny([type, "char"]);
                        var tmp_field = new FiledClass(this, field, option);
                        tmp_field.name = filed_name;
                        tmp_field.appendTo(holder);
                        this.search_fields.push(tmp_field);
                    }
                }
            }

            $el.appendTo(this.$el);
            this.do_show();
        },

        on_attach_callback: function () {
            var self = this;
            _.invoke(this.search_fields, 'on_attach_callback');
            if (this.search_view && Object.keys(this.search_view._search_defaults).length > 0) {
                setTimeout(function () {
                    self.commit_search()
                }, 200)
            }
        },

        /**
         * 提交搜索
         */
        commit_search: function () {
            var domains = []
            _.each(this.search_fields, function (field) {
                var operator = field.operators[0].value || 'like'
                var domain = field.get_domain(field, {
                    "value": operator
                })
                if (!domain || !domain[0][2]) {
                    return
                }
                // 最多也就normalize一下, 这里要验证下odoo自向是否会处理
                domains = domains.concat(domain)
            })
            this.trigger_up('search', {
                domains: [domains]
            });
        }
    });

    widgetRegistry.add("custom_search_pannel", custom_search_pannel)

    return custom_search_pannel
});