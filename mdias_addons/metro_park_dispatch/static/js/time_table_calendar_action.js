odoo.define('funenc.time_table_calendar', function(require) {
    "use strict";

    var core = require('web.core');

    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    var _t = core._t;
    var qweb = core.qweb;

    var calendar_template =
        "<div class='clndr-controls'>" +
        "</div>" +
        "<table class='clndr-table' border='0' cellspacing='0' cellpadding='0'>" +
        "<thead>" +
        "<tr class='header-days'>" +
        "<% for(var i = 0; i < daysOfTheWeek.length; i++) { %>" +
        "<td class='header-day'><%= daysOfTheWeek[i] %></td>" +
        "<% } %>" +
        "</tr>" +
        "</thead>" +
        "<tbody>" +
        "<% for(var i = 0; i < numberOfRows; i++){ %>" +
        "<tr>" +
        "<% for(var j = 0; j < 7; j++){ %>" +
        "<% var d = j + i * 7; %>" +
        "<td class='<%= days[d].classes %>'>" +
        "<div class='day_item'>" +
        "<div class='day_name day-contents'><%= days[d].day %></div>" +
        " <%if(days[d].events.length >0){%>\n" +
        "<div class='plan_time_table' plan_id='<%= days[d].events[0].plan_id %>'>计划:<%= days[d].events[0].plan %></div>\n" +
        "<div class='real_time_table' actual_id='<%= days[d].events[0].actual_id %>'>实际:<%= days[d].events[0].actual %></div>" +
        "</div>" +
        " <%}%>" +
        "</td>" +
        "<% } %>" +
        "</tr>" +
        "<% } %>" +
        "</tbody>" +
        "</table>";

    /**
     * 运行图日历
     */
    var time_table_calendar = AbstractAction.extend(ControlPanelMixin, {
        template: 'time_table_calendar_view_template',
        log_widget: undefined,
        $buttons: undefined,
        calendar: undefined,
        year: undefined,
        month: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {
            "click .plan_time_table": "_on_view_plan_time_table",
            "click .real_time_table": "_on_view_real_time_table"
        }),

        /**
         * 引用laydate
         */
        willStart: function() {
            return this._super.apply(this, arguments).then(function() {
                var def = $.Deferred();
                layui.use('laydate', function() {
                    def.resolve()
                });
                return def;
            })
        },

        /**
         * 查看计划时刻表数据
         * @param {*} event 
         */
        _on_view_plan_time_table: function(event) {
            var self = this
            var target = $(event.target)
            var plan_id = parseInt(target.attr('plan_id'))
            this._rpc({
                "model": "metro_park_base.time_table",
                "method": "view_time_table",
                "args": [plan_id]
            }).then(function(rst) {
                if (rst) {
                    self.do_action(rst)
                }
            })
        },

        /**
         * 查看实际时刻表数据
         * @param {*} event 
         */
        _on_view_real_time_table: function(event) {
            var self = this
            var target = $(event.target)
            var actual_id = parseInt(target.attr('actual_id'))
            this._rpc({
                "model": "metro_park_base.time_table",
                "method": "view_time_table",
                "args": [actual_id]
            }).then(function(rst) {
                if (rst) {
                    self.do_action(rst)
                }
            })
        },


        /**
         * 开始
         */
        start: function() {

            this._super.apply(this, arguments)
                // 日期渲染
            layui.laydate.render({
                elem: '.year_month_picker',
                type: 'month',
                value: moment().format('YYYY-MM'),

                done: function(value, date) {
                    var tmp_date = moment(value)
                    var year = tmp_date.year()
                    var month = tmp_date.month()

                    //取得实际的运行图
                    var events = [{
                        date: "YYYY-MM-DD",
                        and: "anything else"
                    }]

                    if (self.year != year) {
                        self.calendar.setYear(year);
                        self.year = year
                    }

                    if (self.month != month) {
                        self.calendar.setMonth(month);
                        self.month = month
                    }

                    if (!isNaN(year) && !isNaN(month)) {
                        self._rpc({
                            model: 'metro_park_base.time_table',
                            method: 'set_clndr_events',
                            args: [self.id, year, month]
                        }).then(function(events) {
                            self.calendar.setEvents(events)
                        })
                    }

                }
            });
            var self = this
            self._rpc({
                model: 'metro_park_base.time_table',
                method: 'get_clndr_events',
                args: [self.id, moment().year(), moment().month()]
            }).then(function(events) {
                self.events = events

                // 日历
                // var events = [
                //     {date: '2019-05-06', title: 'T0001',},
                //     {date: '2019-05-05', title: 'CT0002',},
                //     {date: '2019-05-07', title: 'T00013',},
                //     {date: '2019-05-05', title: 'CT00014',},
                //     {date: '2019-05-04', title: 'T00015',},
                //     {date: '2019-05-08', title: 'T00016',},
                //     {date: '2019-05-09', title: 'T00019',},
                // ]

                self.year = moment().year()
                self.month = moment().month()
                self.calendar = self.$el.find('.calendar').clndr({
                    template: calendar_template,
                    startWithMonth: moment(),
                    showAdjacentMonths: true,
                    daysOfTheWeek: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
                    events: self.events,

                    clickEvents: {
                        click: function(target) {

                        }
                    }
                });
            })

            // control panel
            this._renderButtons();
            this._updateControlPanel();
        },

        do_show: function() {
            this._updateControlPanel();
        },

        _renderButtons: function() {
            this.$buttons = $(qweb.render('time_table_calendar_btns'));
        },

        _updateControlPanel: function() {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                }
            });
        }
    });

    core.action_registry.add('time_table_calendar', time_table_calendar);

    return time_table_calendar;
});