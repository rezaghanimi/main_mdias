/**
 * 计划预演
 */
odoo.define('metro_park_maintance.plan_conflict_check', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var plan_conflict_check = AbstractAction.extend({
        template: "metro_park_maintance.plan_conflict_check",

        willStart: function () {
            var self = this
            return this._super.apply(this, arguments).then(function () {
                // 取得当前的检修计划和收发车计划和调车计划
                // var date = moment().format('YYYY-MM-DD')
                // this._rpc({
                //     "model": "metro_park_maintenance.rule_info",
                //     "method": "get_day_plans",
                //     "args": [],
                //     "kwargs": {
                //         date: date
                //     }
                // }).then(function (rst) {
                //     self.plans = rst
                // })
            })
        },

        start: function () {
            this.canvas = undefined
            this.axis_color = '#888'
            this.hour_sep_height = 15
            this.five_min_sep_height = 10
            return this._super.apply(this, arguments)
        },

        on_attach_callback: function () {
            this._super.apply(this, arguments)
            this.init_canvas()
            this.render()
        },

        /**
         * 计划从早上3点到晚上3点
         */
        render: function () {
            this.render_time_axis();
        },

        get_width: function() {
            return this.canvas.getWidth()
        },

        get_height: function() {
            return this.canvas.getHeight()
        },

        init_canvas: function () {

            this.canvas = new fabric.Canvas(this.$('canvas')[0]);

            var el = fabric.util.createCanvasElement();

            el.width = this.width;
            el.height = this.height;

            // 鼠标点击事件处理
            this.canvas.on('mouse:down', _.bind(this.on_canvas_mouse_down, this))
            this.canvas.on('mouse:up', _.bind(this.on_canvas_mouse_up, this))
            this.canvas.on('mouse:move', _.bind(this.on_canvas_mouse_move, this))

            // 设置宽度
            // this.canvas.setWidth("100%", {
            //     cssOnly: true
            // })

            // // 设置高度
            // this.canvas.setHeight("100%", {
            //     cssOnly: true
            // })
        },

        get_canvas: function () {
            return this.canvas
        },

        /**
         * 当前时间画条线
         */
        add_time_line: function () {
            if (!this.current_time) {

            }
        },

        // 绘制坐标轴
        render_time_axis: function() {
            var x_start = 100
            var y_start = 100

            // 以分钟为单位, 每小时画一个大刻度，每分5分钟画一个中刻度每10分钟画一个中刻度， 每分钟间隔10个像素
            var total_width = 60 * 24 * 10
            var line = new fabric.Line(
                [x_start, y_start, x_start + total_width, y_start], {
                stroke: this.axis_color,
                strokeWidth: 2,
                hasControls: false,
                hasBorders: false,
                lockMovementX: true, // 禁止移动
                lockMovementY: true, // 禁止移动
                hoverCursor: 'default'
            })
            this.canvas.add(line)

            // 以5分钟为单位
            for(var i = 0; i < 24; i++) {
                var hour_width = i * 60 * 10
                var hour_start = x_start + hour_width
                // 画一个大刻度
                var line = new fabric.Line([hour_start, y_start, x_start + hour_width,
                     y_start - this.hour_sep_height], {
                    stroke: this.axis_color,
                    strokeWidth: 1,
                    hasControls: false,
                    hasBorders: false,
                    lockMovementX: true, // 禁止移动
                    lockMovementY: true, // 禁止移动
                    hoverCursor: 'default'
                })
                this.canvas.add(line)

                // 每隔5分钟画一个小的刻度, 一头一尾由于有刻度，所以没画
                for (var j = 1; j < 60 * 10 / 5 - 120; j += 12 * 10) {
                    var five_min_x = hour_start + j * 12 * 10
                    var line = new fabric.Line([five_min_x, y_start, x_start + hour_width,
                        y_start - this.five_min_sep_height], {
                       stroke: this.axis_color,
                       strokeWidth: 1,
                       hasControls: false,
                       hasBorders: false,
                       lockMovementX: true, // 禁止移动
                       lockMovementY: true, // 禁止移动
                       hoverCursor: 'default'
                   })
                }

                // 更新起点坐标
                x_start += hour_width
            }
        },

        on_canvas_mouse_down: function (options) {
            return
            var x = options.e.clientX - this.canvas._offset.left;
            var y = options.e.clientY - this.canvas._offset.top;

            var evt = options.e;
            if (evt.altKey === true) {
                this.isDragging = true;
                this.selection = false;
                this.lastPosX = evt.clientX;
                this.lastPosY = evt.clientY;
            }
        },

        on_canvas_mouse_move: function(option) {
            return
            if (this.isDragging) {
                var e = options.e;
                this.viewportTransform[4] += e.clientX - this.lastPosX;
                this.viewportTransform[5] += e.clientY - this.lastPosY;
                this.requestRenderAll();
                this.lastPosX = e.clientX;
                this.lastPosY = e.clientY;
            }
        },

        on_canvas_mouse_up: function () {
            return
            var x = options.e.clientX - this.canvas._offset.left;
            var y = options.e.clientY - this.canvas._offset.top;

            this.isDragging = false;
            this.selection = true;
        }
    });

    core.action_registry.add('plan_conflict_check', plan_conflict_check);
    return plan_conflict_check;
});