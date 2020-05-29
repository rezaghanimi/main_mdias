odoo.define("funenc.list_controller", function (require) {
    "use strict";

    var ListController = require("web.ListController");
    var searchExt = require("funenc.search_extend");
    searchExt = searchExt.search_extend
    var AbstractAction = require('web.AbstractAction');
    var core = require("web.core");
    var Dialog = require('web.Dialog');
    var qweb = core.qweb;
    var _t = core._t;

    ListController.include({
        template: 'funenc.controller',
        // 自定义搜索区
        customSearch: undefined,
        search_inited: false,
        select_mode: false,

        set_select_mode: function() {
            this.select_mode = true;
        },

        /**
         * 打开选择对话框
         * @param {*} event 
         */
        _onOpenRecord: function(event) {
            if (this.select_mode) {
                var selectedRecord = this.model.get(event.data.id);
                this.trigger_up('select_record', {
                    id: selectedRecord.res_id,
                    display_name: selectedRecord.data.display_name,
                });
            } else {
                this._super.apply(this, arguments);
            }
        },

        // 自定义templates
        custom_btn_template: undefined,

        init: function () {
            this._super.apply(this, arguments);
            this.renderer_attrs = this.renderer.arch.attrs;
            if (this.renderer_attrs.template) {
                this.template = this.renderer_attrs.template;
            }
            this.tab_domain = {};
            this.current_tab_key = undefined;
        },

        start: function () {
            AbstractAction.prototype.start.apply(this, arguments)

            this.view_options = this.get_current_view_options();

            this.$buttons = this.$('.operation_btn')
            this.$search = this.$('.search')
            this.$search_buttons = this.$('.search_btns')
            this.$sidebar = this.$('.side_bar')
            this.$pager = this.$('.pager')
            this.$custom_search = this.$('.custom_search')
            this.$search = this.$('.search')
            this.$switch_buttons = this.$('.switch_btn');
            var $content = this.$('.content')
            this.renderer.appendTo($content)

            this._renderControlPanelElements();

            return this._update(this.initialState);
        },

        on_attach_callback: function () {
            if (this.customSearch) {
                this.customSearch.pannel.on_attach_callback()
            }
            this._super()
        },

        /**
         * 扩展，添加自定义搜索区域, 如果配置了搜索区域的话则自定义, 如果没有配置的话则直接使用高有搜索
         * @param {*} custom_area
         * @param {*} view
         * @param {*} searchview
         */
        renderCustomSearch: function ($custom_area, fields, attrs, searchview) {
            if (!$custom_area) {
                console.log('there is no render area for the custom search area!');
                return;
            }

            // 自定义的list还有问题
            if (fields) {
                if (attrs.search_ex_template) {
                    if (!this.custom_search) {
                        if (searchview) {
                            searchview.$el.hide();
                        }
                        this.customSearch = new searchExt(
                            this,
                            fields,
                            attrs.search_ex_template,
                            attrs.search_pannel_js_class,
                            searchview
                        );
                        this.customSearch.appendTo($custom_area);
                    }
                }
            }
        },

        /**
         * 如果用户指定了template，则使用自定义的tempate
         * @param {*} $node
         */
        renderButtons: function ($node) {
            // 完全自定义的template
            if (this.renderer_attrs.custom_btn_template) {
                this.$buttons = $(qweb.render(this.renderer_attrs.custom_btn_template, {widget: this}));
                this.$buttons.appendTo($node);
                return
            }

            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, {widget: this}));
                this.$buttons.on('click', '.o_list_button_add', this._onCreateRecord.bind(this));

                this._assignCreateKeyboardBehavior(this.$buttons.find('.o_list_button_add'));
                this.$buttons.find('.o_list_button_add').tooltip({
                    delay: {show: 200, hide: 0},
                    title: function () {
                        return qweb.render('CreateButton.tooltip');
                    },
                    trigger: 'manual',
                });
                this.$buttons.on('click', '.o_list_button_discard', this._onDiscard.bind(this));
                this.$buttons.appendTo($node);
            }

            // 附加其它按扭
            if (this.renderer_attrs.extra_btn_template) {
                this.$extra_buttons = $(qweb.render(this.buttons_template, {widget: this}));
                this.$extra_buttons.appendTo($node);
            }
        },

        get_current_view_options: function () {
            var options = {};
            var self = this;
            _.each(this.actionViews, function (view) {
                if (view.type === self.viewType) {
                    options = view.fieldsView.options;
                }
            });
            return options
        },

        get_tab_domain: function (key) {
            var domain = [];
            _.each(this.view_options.tab_options, function (option) {
                if (option.key === key) {
                    domain = option.domain;
                }
            });
            return domain
        },

        click_tab: function (data) {
            var tab_key = data.elem.context.dataset.tabKey;
            this.current_tab_key = tab_key;
            var domain = this.get_tab_domain(this.current_tab_key);
            this.trigger_up('search', {
                domains: [domain]
            });
        },

        list_tab_template: 'FunencListTab',

        _renderTabContent() {
            var self = this;
            var tab_domain = (this.view_options && this.view_options.tab_options) || undefined;
            if (tab_domain === undefined) {
                return false
            }
            var $tabContent = $(qweb.render(this.list_tab_template, {
                tabs: tab_domain
            }));
            $tabContent.find('li').first().addClass('layui-this');
            this.$('.tab-content').append($tabContent);
            var element = layui.element;
            element.on('tab(list_tab)', function (data) {
                self.click_tab(data)
            })
            element.tabChange('list_tab', 0);
        },

        /**
         * 扩展，添加渲染自定义区域, 这个在start里面被调用
         */
        _renderControlPanelElements: function () {
            // 渲染自定义区域
            var fileds = this.renderer.state.fields;
            var attrs = this.renderer.arch.attrs;

            // 将字段信息传入进去, attrs里边有配置信息, searchview用于搜索
            this.renderCustomSearch(this.$custom_search, fileds, attrs, this.searchView);

            // 渲染按扭
            this.renderButtons(this.$buttons);
            if (this.$buttons) {
            //     this.$buttons.find('button[type="action"]').on('click', _.bind(this._onActionClicked, this));
            }
            // 渲染侧边栏
            this.renderSidebar(this.$sidebar);

            // 渲染分页
            this.renderPager(this.$pager);

            // 渲染视图切换
            this._renderSwitchButtons(this.$switch_buttons);
            this._renderTabContent()
        },

        /**
         * 更新数据
         * @param {*} state
         */
        _update: function (state) {
            if (this.searchView && !this.search_inited) {
                this.searchView.$el.appendTo(this.$search)
                this.$search_buttons.hide();
                this.searchView.$buttons.contents().appendTo(this.$search_buttons)
                this.search_inited = true;
            }
            this._update_search_view(this.searchView, !this.searchable || this.searchviewHidden,
                this.groupable, this.enableTimeRangeMenu);
            // 可能动态被改变
            if (!this.searchable || this.searchviewHidden) {
                this.$search.hide();
            }
            return this._super(state)
        },

        /**
         * 更新搜索视图
         * @param {*} searchview
         * @param {*} isHidden
         * @param {*} groupable
         * @param {*} enableTimeRangeMenu
         */
        _update_search_view: function (searchview, isHidden, groupable, enableTimeRangeMenu) {
            if (searchview) {
                searchview.toggle_visibility(!isHidden);
                if (groupable !== undefined) {
                    searchview.groupby_menu.do_toggle(groupable);
                }
                if (enableTimeRangeMenu !== undefined) {
                    searchview.displayTimeRangeMenu(enableTimeRangeMenu);
                }
            }
            this.$search.toggle(!isHidden);
        },

        /**
         * 暂时进行了屏蔽
         * @param {*} $node
         */
        _renderSwitchButtons: function ($node) {
        },

        /**
         * 添加sort属性
         * @param {*} node
         */
        _renderHeaderCell: function (node) {
            var name = node.attrs.name;
            var order = this.state.orderedBy;
            var isNodeSorted = order[0] && order[0].name === name;
            var field = this.state.fields[name];
            var $th = $('<th>');
            if (!field) {
                return $th;
            }
            var description;
            if (node.attrs.widget) {
                description = this.state.fieldsInfo.list[name].Widget.prototype.description;
            }
            if (description === undefined) {
                description = node.attrs.string || field.string;
            }

            // 是否禁用sort
            var disable_sort = node.attrs.disable_sort || false
            console.log(node.attrs)

            $th.text(description)
                .data('name', name)
                .toggleClass('o-sort-down', isNodeSorted ? !order[0].asc : false)
                .toggleClass('o-sort-up', isNodeSorted ? order[0].asc : false)
                .addClass((field.sortable && !disable_sort) && 'o_column_sortable');

            if (isNodeSorted) {
                $th.attr('aria-sort', order[0].asc ? 'ascending' : 'descending');
            }

            if (field.type === 'float' || field.type === 'integer' || field.type === 'monetary') {
                $th.css({textAlign: 'right'});
            }

            if (config.debug) {
                var fieldDescr = {
                    field: field,
                    name: name,
                    string: description || name,
                    record: this.state,
                    attrs: node.attrs,
                };
                this._addFieldTooltip(fieldDescr, $th);
            }
            return $th;
        },
        _onButtonClicked: function (event) {
            var attrs = event.data.attrs;
            var self = this;
            event.stopPropagation();
            if (attrs.confirm) {
                Dialog.confirm(this, attrs.confirm, {
                    confirm_callback:  function () {
                        self._callButtonAction(event.data.attrs, event.data.record)
                    }.bind(this)
                });
            }else {
                 this._callButtonAction(event.data.attrs, event.data.record);
            }
        },
    });
});
