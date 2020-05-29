odoo.define('metro_park_dispatch.run_plan_monitor_list', function (require) {
    "use strict";
  
    var BasicView = require('web.BasicView');
    var ListRenderer = require('funenc.fnt_table_render');
    var ListController = require('funenc.fnt_table_controller');
    var ListView = require('web.ListView')
    var view_registry = require("web.view_registry");
    var BasicModel = require('web.BasicModel');
  
    // 控制器
    var RunPlanMonitorListController = ListController.extend({

    })
  
    // 重写，自定义搜索
    var RunPlanMonitorListModel = BasicModel.extend({
  
    })
  
    // 重写，渲染列表视图
    var RunPlanMonitorListRender = ListRenderer.extend({

        start: function() {
          this._super.apply(this, arguments)
          this.hasSelectors = false  
        },

        _renderView: function () {
          // 强行禁用hasSelector
          this.hasSelectors = false  
          return this._super.apply(this, arguments)
        },

                /**
         * 遍历表头，取得表头信息，对要显示的字段添加index和key的信息, 如果是有选择框的话则在前边添加一列
         * @param {*} columnInvisibleFields
         */
        _processColumns: function (columnInvisibleFields) {
          var self = this;
          self.handleField = null;

          // 取得所有要显示的列
          this.columns = _.reject(this.arch.children, function (c) {
              if (c.tag === 'control') {
                  return true;
              }
              var reject = c.attrs.modifiers.column_invisible;

              // width
              if (c.attrs.width) {
                  c.width = c.attrs.width
              } else {
                  c.width = 100;
              }

              if (c.attrs.name in columnInvisibleFields) {
                  reject = columnInvisibleFields[c.attrs.name];
              }

              if (!reject && c.attrs.widget === 'handle') {
                  self.handleField = c.attrs.name;
              }

              return reject;
          });

          var index = 0;
          // if (this.hasSelectors) {
          //     index += 1
          // }

          // 设置index和key
          _.each(this.columns, function (column) {
              column.index = index
              column.key = self.cur_table_id + '-' + index
              index++
          })
      },

      _onCellClick: function (event) {
          // The special_click property explicitely allow events to bubble all
          // the way up to bootstrap's level rather than being stopped earlier.
          if (!this._isEditable() 
          || $(event.target).prop('special_click') 
          || $(event.target).attr('type') == 'action') {
              return;
          }
          var $td = $(event.currentTarget);
          var $tr = $td.parent().parent();
          var $table = $tr.parents("table").first()
          var rowIndex = $table.find('.o_data_row').index($tr);
          var data = this.state.data[rowIndex]
          var data = data.data
          // 特殊状态禁目点击
          if (data.state == 'finished' || data.state == 'canceled') {
            return
          }
          var fieldIndex = Math.max($tr.find('.o_data_cell').not('.o_list_button').index($td), 0);
          this._selectCell(rowIndex, fieldIndex, { event: event });
      },
    })
  
    // 扩展、重新配置list
    var RunPlanMonitorList = ListView.extend({
      config: _.extend({}, BasicView.prototype.config, {
        Model: RunPlanMonitorListModel,
        Renderer: RunPlanMonitorListRender,
        Controller: RunPlanMonitorListController,
      })
    });
  
    view_registry.add("RunPlanMonitorList", RunPlanMonitorList);
  
    return RunPlanMonitorList;
  });
  