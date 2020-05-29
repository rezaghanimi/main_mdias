odoo.define("funenc.kanban_controller", function (require) {
    "use strict";

    var KanbanController = require("web.KanbanController");
    var searchExt = require("funenc.search_extend");
    var AbstractAction = require('web.AbstractAction');
    var core = require("web.core");
    var qweb = core.qweb
    var _t = core._t;

    KanbanController.include({
        template: 'funenc.controller',
        
        // 自定义搜索区
        customSearch: undefined,
        search_inited: false,
        
        // 自定义templates
        custom_btn_template: undefined,

        init: function () {
            this._super.apply(this, arguments)
            this.renderer_attrs = this.renderer.arch.attrs
        },

        start: function () {
            AbstractAction.prototype.start.apply(this, arguments)

            this.$buttons = this.$('.operation_btn')
            this.$search = this.$('.search')
            this.$search_buttons = this.$('.search_btns')
            this.$sidebar = this.$('.side_bar')
            this.$pager = this.$('.pager')
            this.$custom_search = this.$('.custom_search')
            this.$search = this.$('.search')
            this.$switch_buttons = this.$('.switch_btn')

            var $content = this.$('.content')
            this.renderer.appendTo($content)

            this._renderControlPanelElements();

            return this._update(this.initialState);
        },

        /**
         * 扩展，添加自定义搜索区域, 如果配置了搜索区域的话则自定义, 如果没有配置的话则直接使用高有搜索
         * @param {*} custom_area
         * @param {*} view
         * @param {*} searchview
         */
        renderCustomSerach: function (custom_area, fields_view, attrs, searchview) {
            if (!custom_area) {
                console.log('there is no render area for the custom search area!');
                return;
            }

            // 自定义的list还有问题
            if (fields_view) {
                if (attrs.search_ex_template) {
                    if (!this.customSearch) {
                        if (searchview) {
                            searchview.$el.hide();
                        }
                        this.customSearch = new searchExt(
                            this,
                            fields_view,
                            attrs.search_ex_template,
                            attrs.search_pannel_js_class,
                            searchview
                        );
                        this.customSearch.appendTo(custom_area);
                    }
                }
            }
        },

        /**
         * 扩展，添加渲染自定义区域, 这个在start里面被调用
         */
        _renderControlPanelElements: function () {
            // 渲染自定义区域
            var fields_view = this.renderer.state.fields;
            var attrs = this.renderer.arch.attrs;

            // 将字段信息传入进去, attrs里边有配置信息, searchview用于搜索
            this.renderCustomSerach(this.$custom_area, fields_view, attrs, this.searchView);

            // 渲染按扭
            this.renderButtons(this.$buttons);
            if (this.$buttons) {
                this.$buttons.find('button[type="action"]').on('click', _.bind(this._onActionClicked, this));
            }

            // 渲染侧边栏
            this.renderSidebar(this.$sidebar);

            // 渲染分页
            this.renderPager(this.$pager);

            // 渲染视图切换
            this._renderSwitchButtons(this.$switch_buttons);
        },

        /**
         * 更新数据
         * @param {*} state 
         */
        _update: function (state) {
            this._updateButtons();

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

            this._pushState();
            return this._renderBanner();
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
            return

            var self = this;
            var views = _.filter(this.actionViews, {multiRecord: this.isMultiRecord});
    
            if (views.length <= 1) {
                return $();
            }
    
            var template = config.device.isMobile ? 'ControlPanel.SwitchButtons.Mobile' : 'ControlPanel.SwitchButtons';
            var $switchButtons = $(qweb.render(template, {
                views: views,
            }));

            // create bootstrap tooltips
            _.each(views, function (view) {
                $switchButtons.filter('.o_cp_switch_' + view.type).tooltip();
            });

            // add onclick event listener
            var $switchButtonsFiltered = config.device.isMobile ? $switchButtons.find('button') : $switchButtons.filter('button');
            $switchButtonsFiltered.click(_.debounce(function (event) {
                var viewType = $(event.target).data('view-type');
                self.trigger_up('switch_view', {view_type: viewType});
            }, 200, true));
    
            if (config.device.isMobile) {
                // set active view's icon as view switcher button's icon
                var activeView = _.findWhere(views, {type: this.viewType});
                $switchButtons.find('.o_switch_view_button_icon').addClass('fa fa-lg ' + activeView.icon);
            }

            $switchButtons.appendTo($node)
        },
    });
})
