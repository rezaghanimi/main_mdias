odoo.define('metro_park_dispatch.cur_train_manage_with_wizard', function (require) {
  "use strict";

  var BasicView = require('web.BasicView');
  var ListRenderer = require('web.ListRenderer');
  var ListController = require('web.ListController');
  var ListView = require('web.ListView')
  var view_registry = require("web.view_registry");
  var ListRenderer = require("web.ListRenderer")
  var BasicModel = require('web.BasicModel');

  // 控制器
  var cur_train_manage_with_wizardController = ListController.extend({
    buttons_template: 'ListView.buttons',

    renderButtons: function ($node) {
      if (!this.noLeaf && this.hasButtons) {
        this.$buttons = $(qweb.render(this.buttons_template, { widget: this }));
        this.$buttons.on('click', '.o_list_button_add', this._onCreateRecord.bind(this));

        this._assignCreateKeyboardBehavior(this.$buttons.find('.o_list_button_add'));
        this.$buttons.find('.o_list_button_add').tooltip({
          delay: { show: 200, hide: 0 },
          title: function () {
            return qweb.render('CreateButton.tooltip');
          },
          trigger: 'manual',
        });
        this.$buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
        this.$buttons.appendTo($node);
      }
    },
  })

  // 重写，自定义搜索
  var cur_train_manage_with_wizardModel = BasicModel.extend({

  })

  // 重写，渲染列表视图
  var cur_train_manage_with_wizardRender = ListRenderer.extend({

  })

  // 扩展、重新配置list
  var cur_train_manage_with_wizard = ListView.extend({
    config: _.extend({}, BasicView.prototype.config, {
      Model: cur_train_manage_with_wizardModel,
      Renderer: cur_train_manage_with_wizardRender,
      Controller: cur_train_manage_with_wizardController,
    })
  });

  view_registry.add("cur_train_manage_with_wizard", cur_train_manage_with_wizard);

  return cur_train_manage_with_wizard;
});
