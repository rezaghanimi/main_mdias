/**
 * main menu
 */
odoo.define('funenc.AppMenuExtend', function (require) {
    "use strict";

    var AppMenu = require('funenc.AppMenu')
    var core = require('web.core')
    var qweb = core.qweb



    var AppMenuExtend = AppMenu.include({
        events: _.extend({}, AppMenu.prototype.events, {
            "click .nav-item": "_on_click_nav_link",
        }),

        /**
         * 点击nav link
         */
        _on_click_nav_link: function (event) {
            var target = $(event.currentTarget);
            var text = $(target).find(".nav-link-title").text();

            // 如果是司机排班则隐藏左侧
            if (_.str.trim(text) == '司机排班') {
                $('.left-sidebar').hide()
                this.show_margin(false);
                this.jumpToDriverClient(target);
            } else {
                $('.left-sidebar').show()
                this.show_margin(true);
            }
        },

        /**
         * 跳转到司机排班
         */
        jumpToDriverClient: function (target) {
            var nav_link = $(target).find(".nav-link");
            var href = nav_link.attr("href")
            window.location.href = href

        },

        /**
         * 隐藏边界
         * @param {*} show_margin
         */
        show_margin: function (show_margin) {
            if (show_margin) {
                $("html .o_web_client > .o_main").css("padding-left", "250px")
            } else {
                $("html .o_web_client > .o_main").css("padding-left", "0px")
            }
        },

    });

    return AppMenuExtend;
});


