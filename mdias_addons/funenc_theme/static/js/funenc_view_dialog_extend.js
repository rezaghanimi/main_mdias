odoo.define('funenc.view_dialogs_extend', function (require) {
    "use strict";

    var view_dialogs = require('web.view_dialogs');
    var fnt_table = require('funenc.fnt_table');
    var fnt_table_controller = require('funenc.fnt_table_controller');
    var SearchView = require('web.SearchView');
    var view_registry = require('web.view_registry');

    var core = require('web.core');
    var _t = core._t;

    // var SelectCreateListController = fnt_table_controller.extend({
    //     // Override the ListView to handle the custom events 'open_record' (triggered when clicking on a
    //     // row of the list) such that it triggers up 'select_record' with its res_id.
    //     custom_events: _.extend({}, fnt_table_controller.prototype.custom_events, {
    //         open_record: function (event) {
    //             var selectedRecord = this.model.get(event.data.id);
    //             this.trigger_up('select_record', {
    //                 id: selectedRecord.res_id,
    //                 display_name: selectedRecord.data.display_name,
    //             });
    //         },
    //     }),
    // });

    view_dialogs.SelectCreateDialog.include({
        setup: function (search_defaults, fields_views) {
            var self = this;
            var fragment = document.createDocumentFragment();
    
            var searchDef = $.Deferred();
    
            // Set the dialog's header and its search view
            var $header = $('<div/>').addClass('o_modal_header').appendTo(fragment);
            // 这里分页可以渲染到底部上面去更合理
            var $pager = $('<div/>').addClass('o_pager').appendTo($header);
            var options = {
                $buttons: $('<div/>').addClass('btn-group o_search_options').appendTo($header),
                search_defaults: search_defaults,
            };
            var searchview = new SearchView(this, this.dataset, fields_views.search, options);
            searchview.prependTo($header).done(function () {
                var d = searchview.build_search_data();
                if (self.initial_ids) {
                    d.domains.push([["id", "in", self.initial_ids]]);
                    self.initial_ids = undefined;
                }
                var searchData = self._process_search_data(d.domains, d.contexts, d.groupbys);
                searchDef.resolve(searchData);
            });
    
            return $.when(searchDef).then(function (searchResult) {
                var listView = undefined
                var view_class = fnt_table
                if (self.options.js_class) {
                    view_class = view_registry.get(self.options.js_class);
                }
                // Set the list view, 在这里使用fnt_table
                var listView = new view_class(fields_views.list, _.extend({
                    context: searchResult.context,
                    domain: searchResult.domain,
                    groupBy: searchResult.groupBy,
                    modelName: self.dataset.model,
                    hasSelectors: !self.options.disable_multiple_selection,
                    readonly: true,
                }, self.options.list_view_options));
                var controller = listView.config.Controller
                listView.setController(controller);
                return listView.getController(self);
            }).then(function (controller) {
                // 设置为选择模式
                controller.set_select_mode();
                self.list_controller = controller;
                // Set the dialog's buttons
                self.__buttons = [{
                    text: _t("Cancel"),
                    classes: "btn-secondary o_form_button_cancel",
                    close: true,
                }];
                if (!self.options.no_create) {
                    self.__buttons.unshift({
                        text: _t("Create"),
                        classes: "btn-primary",
                        click: self.create_edit_record.bind(self)
                    });
                }
                if (!self.options.disable_multiple_selection) {
                    self.__buttons.unshift({
                        text: _t("Select"),
                        classes: "btn-primary o_select_button",
                        disabled: true,
                        close: true,
                        click: function () {
                            var records = self.list_controller.getSelectedRecords();
                            var values = _.map(records, function (record) {
                                return {
                                    id: record.res_id,
                                    display_name: record.data.display_name,
                                };
                            });
                            self.on_selected(values);
                        },
                    });
                }
                return self.list_controller.appendTo(fragment);
            }).then(function () {
                searchview.toggle_visibility(true);
                self.list_controller.do_show();
                // 渲染分页
                //self.list_controller.renderPager($pager);
                return fragment;
            });
        }
    });
});