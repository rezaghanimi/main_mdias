odoo.define('funenc.datepicker', function (require) {
    "use strict";

    /**
     * 时间选择器，扩展添加箭头
     */
    var basic_fields = require("web.basic_fields");
    var session = require("web.session");
    var Widget = require('web.Widget');
    var field_utils = require('web.field_utils');
    var basic_fields_extend = require('funenc.basic_fields');

    /**
     * 时间组件, 由于odoo的时间格式化和layui的时间格式不一样，所以会有个转换
     */
    var FunencDateWidget = Widget.extend({
        template: 'funenc.datepicker',
        range: false,
        control_type: 'datetime',
        fmt: "yyyy-MM-dd",
        min_max: undefined,
        lay_control_type: undefined,
        btns: ["clear", "now", "confirm"],
        widget_def: $.Deferred(),

        init: function (parent, control_type, options) {
            this.control_type = control_type;

            // 扩展
            this.options = _.extend(options, parent.attrs && parent.attrs.options);
            this.name = parent.name;

            if (options && options.btns) {
                this.btns = options.btns;
            }

            // 取得context, 根据context中的内容动态设置范围, 由于很多时候需要动太设置，所以要通过context传入
            if (parent.record) {
                var context = parent.record.getContext(parent.recordParams);
                if (this.name + "_min_max" in context) {
                    this.min_max = context[this.name + "_min_max"];
                }
            }

            // 如果context里找不到再从options里面去找, 这个一般用于搜索
            if (this.options && this.options.range) {
                this.range = "~";
            }

            // 从控件获取配置属性
            this.lay_control_type = this.options.control_type || this.control_type;

            // 转换成为时间格式化, 由于时间格式化不一至引起
            if (this.control_type == 'datetime') {
                if (this.lay_control_type == "time") {
                    this.fmt = "HH:mm:ss";
                } else if (this.lay_control_type == "datetime") {
                    this.fmt = "yyyy-MM-dd HH:mm:ss";
                } else if (this.lay_control_type == "year") {
                    this.fmt = "yyyy";
                } else if (this.lay_control_type == "month") {
                    this.fmt = "yyyy-MM";
                } else if (this.lay_control_type == 'date') {
                    this.fmt = "yyyy-MM-dd";
                }
            } else {
                if (this.lay_control_type == "time") {
                    throw new Error('error, the date control has no time part');
                } else if (this.lay_control_type == "datetime") {
                    throw new Error('invalidate, the date has no time part');
                } else if (this.lay_control_type == "year") {
                    this.fmt = "yyyy";
                } else if (this.lay_control_type == "month") {
                    this.fmt = "yyyy-MM";
                } else if (this.lay_control_type == 'date') {
                    this.fmt = "yyyy-MM-dd"
                }
            }

            this._super.apply(this, arguments);
        },

        /**
         * 重写，引入layui相关js, 异步引入，再好不过
         */
        willStart: function () {
            var def = $.Deferred()
            layui.use("laydate", function () {
                def.resolve();
            })
            return def;
        },

        /**
         * 弹出层关闭
         */
        _on_datetime_picker_closed: function () {

        },

        /*
        * 弹了层打开
        */
        _on_date_time_picker_opened: function () {

        },

        focus: function() {
            this.$('input').focus()
        },

        start: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                var vaule = self.system_val_to_lay(self.options.value || '')
                self.$('input').val(vaule)
                var lang = session.user_context.lang === 'en_US' ? 'en' : 'cn'
                var config = {
                    elem: self.$('input')[0],
                    lang: lang,
                    format: self.fmt,
                    type: self.lay_control_type,
                    range: self.range, // 是否是范围选择
                    btns: self.btns,
                    value: vaule,
                    show: false,
                    trigger: 'click',
                    ready: function (date) {
                        self.$('.o_dropdown_arrow').removeClass('is-reverse')
                    },
                    done: function (value, date) {
                        self.$('.o_dropdown_arrow').addClass('is-reverse')
                        self.changeDatetime(value, date, null);
                        self._on_datetime_picker_closed();
                    }
                }

                if (self.min_max) {
                    // 这里还是通过min, max传回来比较好, 有时需要单独控制
                    var min_max_ar = self.min_max.split("~");
                    config.min = min_max_ar[0]
                    config.max = min_max_ar[1]
                }

                this.date_picker = layui.laydate.render(config)
            })
        },

        /**
         * set datetime value
         */
        changeDatetime: function (value, date, endDate) {
            if (this.isValid(value, date, endDate)) {
                var oldValue = this.getValue();
                var raw_value = value
                var value = value || false;
                if (value) {
                    if (this.control_type == 'date') {
                        if (this.lay_control_type == "time") {
                            console.log('error, the date has no time part');
                        } else if (this.lay_control_type == "year") {
                            value = value + "-01-01";
                        } else if (this.lay_control_type == "month") {
                            value = value + "-01";
                        }
                    } else if (this.control_type == 'datetime') {
                        if (this.lay_control_type == "time") {
                            value = "1987-01-01 " + value;
                        } else if (this.lay_control_type == "year") {
                            value = value + "-01-01 00:00:00";
                        } else if (this.lay_control_type == "month") {
                            value = value + "-01 00:00:00";
                        }
                    }
                }

                // 自身由于是文本转换在为moment对象
                var mValue = moment(value)
                this.set({
                    value: mValue
                });
                this.$('input').val(raw_value)
                var newValue = this.getValue();
                var hasChanged = oldValue !== newValue;
                if (oldValue && newValue) {
                    if (!this.range) {
                        var formattedOldValue = oldValue.format(
                            this.fmt.replace("dd", "DD").replace("yyyy", "YYYY")
                        );
                        var formattedNewValue = newValue.format(
                            this.fmt.replace("dd", "DD").replace("yyyy", "YYYY")
                        );
                        if (formattedNewValue !== formattedOldValue) {
                            hasChanged = true;
                        }
                    } else {
                        if (oldValue != newValue) {
                            hasChanged = true;
                        }
                    }
                }
                if (hasChanged) {
                    this.trigger_up("datetime_changed");
                }
            }
        },

        /**
         * 取得值
         */
        getValue: function () {
            var value = this.get("value");
            if (!this.range) {
                return value && value.clone();
            } else {
                return value;
            }
        },

        _parseClient: function (v) {
            return field_utils.parse[this.control_type](v, null, { timezone: false });
        },

        isValid: function (value) {
            if (this.range) {
                return true;
            } else {
                if (this.control_type == 'datetime') {
                    if (this.lay_control_type == "time") {
                        value = "1987-01-01 " + value;
                    } else if (this.lay_control_type == "year") {
                        value = value + "-01-01";
                    } else if (this.lay_control_type == "month") {
                        value = value + "-01";
                    }
                } else if (this.control_type == 'date') {
                    if (this.lay_control_type == "time") {
                        console.log('error, the date control has no time part');
                        throw new Error('error, the date control has no time part');
                    } else if (this.lay_control_type == "year") {
                        value = value + "-01-01";
                    } else if (this.lay_control_type == "month") {
                        value = value + "-01";
                    }
                } else {
                    return false
                }

                if (value === "") {
                    return true;
                } else {
                    try {
                        this._parseClient(value);
                        return true;
                    } catch (e) {
                        return false;
                    }
                }
            }
        },

        system_val_to_lay: function (value) {
            var self = this;
            if (!value) {
                return '';
            }
            var formatted_value
            if (self.lay_control_type === "datetime") {
                formatted_value = value ? value.format("YYYY-MM-DD HH:mm:ss") : null;
            } else if (self.lay_control_type == "time") {
                formatted_value = value ? value.format("HH:mm:ss") : null;
            } else if (self.lay_control_type == "year") {
                formatted_value = value ? value.format("YYYY") : null;
            } else if (self.lay_control_type == "month") {
                formatted_value = value ? value.format("YYYY-MM") : null;
            } else if (self.lay_control_type == "date") {
                // date
                formatted_value = value ? value.format("YYYY-MM-DD") : null;
            }
            return formatted_value;
        }
    });

    /**
     * 格式化时间显示
     */
    basic_fields.FieldDate.include({
        control_type: 'date',

        custom_events: _.extend({}, basic_fields.FieldDate.prototype, {
            'datetime_changed': '_on_date_changed',
        }),

        _on_date_changed: function () {
            // 重新去datetime picker里去获取
            var value = this._getValue();
            // 防目转换成为utc时间
            value = value.add(session.getTZOffset(this.value), "minutes")
            if ((!value && this.value) || (value && !value.isSame(this.value))) {
                // 设置组件的值
                this._setValue(value);
            }
        },

        /**
         * 组件开始, start开始以后才会调用renderedit
         */
        start: function () {
            var def;
            if (this.mode === 'edit') {
                this.datewidget = this._makeDatePicker();
                def = this.datewidget.appendTo('<div>');
            }
            return $.when(def, this._super.apply(this, arguments));
        },

        _render: function () {
            if (this.attrs.decorations) {
                this._applyDecorations();
            }
            if (this.mode === 'edit') {
                return this._renderEdit();
            } else if (this.mode === 'readonly') {
                return this._renderReadonly();
            }
        },

        _renderReadonly: function () {
            var options = (this.attrs && this.attrs.options) || {};

            if (options && options.control_type == "year" && this.value) {
                var value = this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes")
                    .format("YYYY年");
                this.$el.html(value);
            } else if (options && options.control_type == "month" && this.value) {
                var value = this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes")
                    .format("YYYY年MM月");
                this.$el.html(value);
            } else {
                var value = this.value ? this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes").format("YYYY年MM月DD日")
                    : ''
                this.$el.html(value);
            }
        },

        /**
         * Instantiates a new DateWidget datepicker.
         *
         * @private
         */
        _makeDatePicker: function () {
            return new FunencDateWidget(this, this.control_type, {
                value: this.value
            });
        },

        /**
         * date 不需要转换, datetime需要转换成为utc时间
         */
        _getValue: function () {
            return this.datewidget.getValue();
        },

        _reset: function () {
            this._super.apply(this, arguments);
        },

        _renderEdit: function () {
            console.log('it is rend edit')
         },

         isFocusable: function() {
             return true
         },

         activate: function () {
            if (this.isFocusable() && this.datewidget) {
                this.datewidget.focus();
                return true;
            }
            return false;
        },
    });

    /**
     * 日期时间组件
     */
    basic_fields.FieldDateTime.include({
        control_type: 'datetime',
        origin_date: undefined,

        custom_events: _.extend({}, basic_fields.FieldDate.prototype, {
            'datetime_changed': '_on_date_changed',
        }),

        _on_date_changed: function () {
            var value = this._getValue();
            if ((!value && this.value) || (value && !value.isSame(this.value))) {
                this._setValue(value);
            }
        },

        start: function () {
            var def;
            if (this.mode === 'edit') {
                this.datewidget = this._makeDatePicker();
                def = this.datewidget.appendTo('<div>');
            }
            return $.when(def, this._super.apply(this, arguments));
        },

        _render: function () {
            if (this.attrs.decorations) {
                this._applyDecorations();
            }
            if (this.mode === 'edit') {
                return this._renderEdit();
            } else if (this.mode === 'readonly') {
                return this._renderReadonly();
            }
        },

        /**
         * 时间组件可以显示到分、秒
         */
        _renderReadonly: function () {
            var options = (this.attrs && this.attrs.options) || {};
            if (options && options.control_type == "time" && this.value) { 
                // 需要配合date一起使用
                var value = this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes")
                    .format("HH:mm:ss");
                this.$el.html(value);
            } else if (options && options.control_type == "year" && this.value) {
                var value = this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes")
                    .format("YYYY年");
                this.$el.html(value);
            } else if (options && options.control_type == "month" && this.value) {
                var value = this.value
                    .clone()
                    .add(session.getTZOffset(this.value), "minutes")
                    .format("YYYY年M月");
                this.$el.html(value);
            } else {
                this.$el.html(this._formatValue(this.value));
            }
        },

        /**
         * Instantiates a new DateWidget datepicker.
         *
         * @private
         */
        _makeDatePicker: function () {
            console.log(this.value)
            var value = this.value  && this.value.clone()
            .add(this.getSession().getTZOffset(this.value), 'minutes');
            return new FunencDateWidget(this, this.control_type, {
                value: value
            });
        },

        /**
         * 转换成为utc时间, 时间范围由于不是moment对象, 所以直接返回
         */
        _getValue: function () {
            var value = this.datewidget.getValue();
            if (value instanceof moment) {
                return value.utc();
            } else {
                return value;
            }
        },

        _renderEdit: function () { 
            // var value = this._getValue();
            // console.log(this.value)
            // this.datewidget.setValue(value)
        }
    });

    return FunencDateWidget;
});