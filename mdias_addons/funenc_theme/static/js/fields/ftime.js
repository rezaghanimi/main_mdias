odoo.define('funenc.ftime', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var DAY_SECOND = 24 * 60 * 60;
    
    var FTime = AbstractField.extend({

        template: 'lay_time_for_ftime',
        className: 'filed-ftime',
        supportedFieldTypes: ['integer', 'float'],
        day_type: 'today',

        init: function() {
            this._super.apply(this, arguments)
            if(this.value >= DAY_SECOND){
                this.day_type = 'tomorrow'
            }else {
                this.day_type = 'today'
            }
        },

        isSet: function () {
            return this.value === 0 || this._super.apply(this, arguments);
        },

        willStart: function() {
            var def = $.Deferred()
            layui.use('laydate', function () {
                def.resolve();
            });
            return $.when(this._super.apply(this), def);
        },

        _renderEdit: function () {
            var laydate = layui.laydate;
            laydate.render({
                elem: this.$('input')[0],
                type: 'time',
                done: this._done_select.bind(this),
                zIndex: 99999999
            });

            var time = new Date(this.value * 1000);
            this.$('input').val(this._format_time(time));
            this.$('select').select2()
            this.$('select').val(this.day_type)
            this.$('select').on('change', this._on_day_type_onchange.bind(this))
        },

        _get_day_type: function () {
            return this.$('.select_day_type').val();
        },

        _getValue: function () {
            return this.value;
        },

        _done_select: function (value, time) {
            var utime = time.hours * 60 * 60 + time.minutes * 60 + time.seconds;
            var day_type = this._get_day_type();
            if (day_type === 'tomorrow') {
                utime += 24 * 60 * 60;
            }
            this._setValue(utime.toString());
            this.value = utime;
        },
        
        _renderReadonly() {
            var time = new Date(this.value * 1000);
            var day_type = '';
            if (this.value >= DAY_SECOND) {
                day_type = '<次日> ';
            }
            this.$el.html(day_type + this._format_time(time));
        },

        _format_time: function (time) {
            return moment(time).utc().format('HH:mm:ss');
        },

        _on_day_type_onchange(data) {
            var day_type = data.val
            if (this.day_type == day_type) {
                return
            }
            var utime = this.value;
            if (day_type === 'tomorrow') {
                utime += DAY_SECOND
            } else if (utime !== 0) {
                utime -= DAY_SECOND
            }
            this._setValue(utime.toString())
            this.day_type = day_type
        }
    });

    field_registry.add('FTime', FTime);

    return {
        ftime: FTime
    }
});