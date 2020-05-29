odoo.define('metro_park_production.big_screen_list', function (require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var list_render = ListRenderer.extend({})

    var list_controller = ListController.extend({
        buttons_template: 'metro_park_production.big_screen_list.buttons',

        /**
         * 重写，添加渲染按扭
         * @param {} node 
         */
        renderButtons: function (node) {
            if (!this.noLeaf && this.hasButtons) {
                this.buttons = $(qweb.render(this.buttons_template, { widget: this }));
                this.buttons.on('click', '.o_list_button_add', this._onCreateRecord.bind(this));
                this._assignCreateKeyboardBehavior(this.buttons.find('.o_list_button_add'));
                this.buttons.find('.o_list_button_add').tooltip({
                    delay: { show: 200, hide: 0 },
                    title: function () {
                        return qweb.render('CreateButton.tooltip');
                    },
                    trigger: 'manual',
                });
                this.buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
                // 调用server_action
                this.buttons.on('click', '.publish_screen', this._onPublishSecreen.bind(this));
                this.buttons.appendTo(node);
            }
        },

        /**
         * 发布大屏信息
         */
        _onPublishSecreen: function() {
            var self = this
            this._rpc({
                "model": "metro_park_production.screen.page",
                "method": "publish_big_screen",
                "args": []
            }).then(function (rst) {
                if (rst) {
                    self.do_action(rst)
                }
            })
        }
    })

    var big_screen_list = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: list_render,
            Controller: list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('big_screen_list', big_screen_list);

    return big_screen_list;
});
