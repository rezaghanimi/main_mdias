/**
 * 计划演练
 */
odoo.define('metro_park.plan_preview_action', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var plan_preview = AbstractAction.extend({
        template: "plan_preview",
        plan_canvas: undefined,

        events: _.extend({}, AbstractAction.prototype.events, {

        }),

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.day_plan_id = action.context.active_id || action.params.active_id
        },

        on_attach_callback: function () {
            this.render_plan()
        },

        render_plan: function () {
            this.plan_canvas = new fabric.Canvas(this.$('canvas')[0]);
            var canvas = this.plan_canvas

            var self = this
            fabric.loadSVGFromURL('/metro_park_maintenance/static/station.svg', function (objects, options) {

                var width = self.$el.width()
                var height = self.$el.height()
    
                canvas.setWidth(width)
                canvas.setHeight(height)

                canvas.renderOnAddRemove = false;
                canvas.add.apply( canvas, objects);
                canvas.renderOnAddRemove = true;
                canvas.renderAll();
            });

            canvas.on('mouse:down', function(opt) {
                var evt = opt.e;
                if (evt.altKey === true) {
                  this.isDragging = true;
                  this.selection = false;
                  this.lastPosX = evt.clientX;
                  this.lastPosY = evt.clientY;
                }
              });
              canvas.on('mouse:move', function(opt) {
                if (this.isDragging) {
                  var e = opt.e;
                  this.viewportTransform[4] += e.clientX - this.lastPosX;
                  this.viewportTransform[5] += e.clientY - this.lastPosY;
                  this.requestRenderAll();
                  this.lastPosX = e.clientX;
                  this.lastPosY = e.clientY;
                }
              });
              canvas.on('mouse:up', function(opt) {
                this.isDragging = false;
                this.selection = true;
              });
        }
    });

    core.action_registry.add('plan_preview', plan_preview);
    return plan_preview;
});