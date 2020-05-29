odoo.define('funenc.basic_controller', function (require) {
    "use strict";

    var BasicController = require('web.BasicController');
    var FunencPager = require('funenc.pager');

    BasicController.include({
        /**
         * 重写, 使用自定义的分页
         */
        renderPager: function ($node) {
            var self = this;
            var data = this.model.get(this.handle, { raw: true });
            var start_index = data.offset;
            var pageSize = data.limit;
            var currentPage = start_index / pageSize + 1;
            this.funenc_pager = new FunencPager(this, data.count, currentPage, pageSize);;

            this.funenc_pager.on('funenc_pager_changed', this, function (info) {
                this.funenc_pager.disable();

                var offset = info.data.offset;
                var limitChanged = info.data.limitChanged;

                var data = this.model.get(this.handle, { raw: true });
                this.reload({ limit: data.limit, offset: offset })
                    .then(function () {
                        // Reset the scroll position to the top on page changed only
                        if (!limitChanged) {
                            self.trigger_up('scrollTo', { top: 0 });
                        }
                    })
                    .then(this.funenc_pager.enable.bind(this.funenc_pager));
            })
            this.funenc_pager.appendTo($node);
            this._updatePager();
        },

        /**
         * 更新分页, 扩展在底部增加分页
         */
        _updatePager: function () {
            this._super.apply(this, arguments);
            if (this.funenc_pager) {
                var data = this.model.get(this.handle, { raw: true });

                var start_index = data.offset;
                var currentPage = start_index / data.limit + 1;

                this.funenc_pager.updateState({
                    totalNumber: data.count,
                    currentPage: currentPage,
                    pageSize: data.limit
                });

                var isRecord = data.type === 'record';
                var hasData = !!data.count;
                var isGrouped = data.groupedBy ? !!data.groupedBy.length : false;
                var isNew = this.model.isNew(this.handle);
                var isPagerVisible = isRecord ? !isNew : (hasData && !isGrouped);
                if (data.count <= data.limit) {
                    isPagerVisible = false;
                }
                this.funenc_pager.do_toggle(isPagerVisible);
            }
        },
    })
})