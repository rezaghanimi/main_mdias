odoo.define('funenc.pager', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var funencPager = Widget.extend({
        totalNumber: undefined,
        pageSize: undefined,
        currentPage: undefined,
        data_source: undefined,
        pager: undefined,

        /**
         * init
         * @param {*} totalNumber
         * @param {*} pageSize
         * @param {*} pageNumber
         */
        init: function (parent, totalNumber, currentPage, pageSize) {
            this.totalNumber = totalNumber || 0;
            this.pageSize = pageSize || 10;
            this.currentPage = currentPage || 0;
            this._super.apply(this, arguments);
        },

        get_total_page: function () {
            return this.pager.getPagesCount();
        },

        get_current_page: function () {
            return this.pager.getCurrentPage() - 1;
        },

        /**
         * 取得当前的偏移
         */
        get_cur_offset: function () {
            var current_page = this.get_current_page();
            var offset = current_page * this.pageSize;
            return offset;
        },

        /**
         * get current offset
         */
        get_cur_limit: function () {
            var current_page = this.get_current_page();
            var offset = (current_page + 1) * this.pageSize;
            if (offset > this.totalNumber) {
                return this.totalNumber - current_page * this.pageSize;
            } else {
                return this.pageSize;
            }
        },

        /**
         * start
         */
        start: function () {
            this._super.apply(this, arguments)
            this.$el.addClass("funenc_pager");
            this.renderPager();
        },

        /**
         * render pagenation
         * @param {} option
         */
        renderPager: function () {
            var self = this;
            this.$el.empty();
            this.pager = this.$el.pagination({
                items: this.totalNumber,
                itemsOnPage: this.pageSize,
                currentPage: this.currentPage,
                cssStyle: 'light-theme',
                onPageClick: function (pageNumber, event) {
                    if (event) {
                        event.preventDefault();
                    }
                    var offset = this.currentPage * this.itemsOnPage;
                    var limit = this.currentPage + 1 == this.pages ? this.itemsOnPage : this.items - offset;
                    var limitChanged = limit != this.itemsOnPage ? true : false
                    self.trigger_up('funenc_pager_changed', {
                        offset: offset,
                        limitChanged: limitChanged
                    });
                }
            });
        },

        /**
         * 重新渲染
         */
        updateState: function (option) {
            this.totalNumber = option.totalNumber;
            this.pageSize = option.pageSize;
            this.currentPage = option.currentPage;
            this.renderPager();
        },

        disable: function () {
            //this.$el.disable();
        },

        enable: function () {
            //this.$el.enable();
        }
    });

    return funencPager
});