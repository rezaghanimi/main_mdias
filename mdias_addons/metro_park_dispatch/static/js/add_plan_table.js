odoo.define('metro_park_dispatch.add_new_plan_list', function (require) {
  "use strict";

  /**
   * 添加新的计划
   */
  var BasicView = require('web.BasicView');
  var ListRenderer = require('funenc.fnt_table_render');
  var ListController = require('funenc.fnt_table_controller');
  var ListView = require('web.ListView')
  var view_registry = require("web.view_registry");
  var BasicModel = require('web.BasicModel');

  // 控制器
  var AddPlanController = ListController.extend({})

  // 重写，自定义搜索
  var AddPlanListModel = BasicModel.extend({})

  // 重写，渲染列表视图
  var AddPlanListRender = ListRenderer.extend({

    _moveToNextLine: function () {
      var self = this;
      var record = this.state.data[this.currentRow];
      this.commitChanges(record.id).then(function () {
        var fieldNames = self.canBeSaved(record.id);
        if (fieldNames.length) {
          return;
        }

        if (self.currentRow < self.state.data.length - 1) {
          self._selectCell(self.currentRow + 1, 0);
        } else {
          self.unselectRow()
          // add record 报错
          // self.unselectRow().then(function () {
          //   self.trigger_up('add_record', {
          //     onFail: self._selectCell.bind(self, 0, 0, {}),
          //   });
          // });
        }
      });
    },

  })

  // 扩展、重新配置list
  var addNewPlanList = ListView.extend({
    config: _.extend({}, BasicView.prototype.config, {
      Model: AddPlanListModel,
      Renderer: AddPlanListRender,
      Controller: AddPlanController,
    })
  });

  view_registry.add("addNewPlanList", addNewPlanList);

  return addNewPlanList;
});
