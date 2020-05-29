odoo.define('funenc.dev_list_view', function (require) {
    "use strict";

    var core = require('web.core')
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var qweb = core.qweb

    var dev_list_render = ListRenderer.extend({})

    var dev_list_controller = ListController.extend({
        buttons_template: 'Funenc.ListView_null.buttons',
        //去掉action 菜单
        renderSidebar: function ($node) {
            this.$sidebar = $(qweb.render(this.buttons_template));
            $node.css('display', 'none')
            this.$sidebar.appendTo($node);

        },
        /**
         * 重写，添加渲染按扭
         * @param {} $node 
         */
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
                // this.$buttons.on('click', '.o_list_button_add', this._onCreateRecord.bind(this));
                //
                // this._assignCreateKeyboardBehavior(this.$buttons.find('.o_list_button_add'));
                // this.$buttons.find('.o_list_button_add').tooltip({
                //     delay: { show: 200, hide: 0 },
                //     title: function () {
                //         return qweb.render('CreateButton.tooltip');
                //     },
                //     trigger: 'manual',
                // });
                // this.$buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
                // // 调用server_action
                // this.$buttons.on('click', '.funenc_import_dev', this._onImportDev.bind(this));
                this.$buttons.appendTo($node);
            }
        },

        /**
         * 导入设备
         */
        _onImportDev: function() {
            this.do_action({
                type:'ir.actions.act_window',
                view_type: 'form',
                view_mode: 'form',
                res_model: 'metro_park_maintenance.dev_import_wizard',
                views: [[false, 'form']]
            })
        }
    })

    var dev_list_view = ListView.extend({
        config: _.extend({}, BasicView.prototype.config, {
            Renderer: dev_list_render,
            Controller: dev_list_controller
        }),
        viewType: 'list'
    });

    view_registry.add('dev_list_view', dev_list_view);

    return dev_list_view;
});
