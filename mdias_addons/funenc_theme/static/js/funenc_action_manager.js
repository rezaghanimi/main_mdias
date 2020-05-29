odoo.define('funenc.action_manager', function (require) {
    "use strict";

    /**
     * 扩展action manager 增加 tab功能
     */
    var dom = require('web.dom');
    var pyUtils = require('web.py_utils');
    var ActionManager = require('web.ActionManager')
    var Context = require('web.Context');
    var core = require('web.core');
    var data = require('web.data'); // this will be removed at some point
    var SearchView = require('web.SearchView');

    var qweb = core.qweb;

    // 可以选择tab放在上面还是放在下面, 其实还可以做成左右，不过这里算了
    var FILTER_TAB_TBAS = 'layadmin-layout-tabs';
    var TABS_HEADER = '#funenc_tab_headers>li';

    ActionManager.include({
        PADDING_LEFT: 250,
        className: 'o_content',
        tab_template: 'funenc.tab_page',
        current_action: undefined,
        pageTabs: true,
        // 使用字典来缓存action的controller信息, 同一个action有多种视图, 所以要这样设计
        action_stack: {},
        events: _.extend({}, ActionManager.prototype.events, {
            'click dd[layadmin-event=closeThisTabs]': 'closeThisTabs',
            'click dd[layadmin-event=closeAllTabs]': function () {
                this.closeAllTabs()
            },
            'click dd[layadmin-event=closeOtherTabs]': function () {
                this.closeOtherTabs()
            },
            'click div[layadmin-event=leftPage]': function () {
                this.turnPage('left')
            },
            'click div[layadmin-event=rightPage]': function () {
                this.turnPage('right')
            },
        }),

        /**
         * 增加tab page在前面
         * @override
         */
        start: function () {
            var self = this;
            // 使用layui的element
            var element = layui.element;
            return this._super.apply(this).then(function () {
                // 渲染tab
                var tab_box = $(qweb.render(self.tab_template, {
                    widget: this
                }))
                return tab_box.prependTo(self.$el);
            }).then(function () {

                // 切换tab的时候，将tab_body显示出来
                element.on('tab(' + FILTER_TAB_TBAS + ')', function (data) {
                    var index = data.index;
                    var tab_page_body = self.$('.funenc_tab_page_body').eq(index || 0);
                    tab_page_body.addClass('layui-show').siblings().removeClass('layui-show');
                });

                // 删除tab
                element.on('tabDelete(' + FILTER_TAB_TBAS + ')', function (obj) {
                    var tab_bodys = self.$('.funenc_tab_page_body');
                    var tab_body = tab_bodys.eq(obj.index);
                    var actionID = tab_body.attr('actionid')
                    self._removeAction(actionID)

                    if (obj.index != 0) {
                        // 取得当前最后一个action作为当前的action
                        var tmp_body = tab_bodys.eq(obj.index - 1);
                        var tmp_action_id = tmp_body.attr('actionid')
                        var action = self.actions[tmp_action_id];
                        var controller = self.controllers[action.controllerID];
                        self.current_controller = controller;
                    } else {
                        self.current_controller = undefined;
                    }

                    // remove the tab body
                    tab_body.remove()
                });

                // 监听选项卡的更多操作
                element.on('nav(layadmin-pagetabs-nav)', function (elem) {
                    var dd = elem.parent();
                    dd.removeClass('layui-this');
                    dd.parent().removeClass('layui-show');
                });

                // 监听resize
                $(window).on('resize', _.bind(self.on_resize, self));
            });

        },

        willStart: function () {
            var def = $.Deferred()
            // 申明要使用element, layui异步加载机制
            layui.use(['element'], function () {
                def.resolve();
            });
            // core.bus.on('main_max', this, this.showMaxMain.bind(this));
            // core.bus.on('main_window', this, this.hindMaxMain.bind(this));
            return $.when(this._super.apply(this), def);
        },

        /**
         * 更新page高度
         */
        on_resize: function () {
            var height = this.$('.funenc-tabs-body').height();
            $('.funenc_tab_page_body ').height(height)
        },

        on_attach_callback: function () {
            this._super.apply(this, arguments)
            // 渲染ta
            layui.element.render('nav', 'layadmin-pagetabs-nav')
        },

        /**
         * 通知改变菜单选中, 同步菜单信息
         * @param {*} event
         */
        _on_tab_item_click: function (event) {
            var self = this;
            var target = event.target;
            var tab_index = target.data('tab_index')
            self.trigger_up('tab_changed', {tab_index: tab_index})
        },

        // 滚动页面标签
        turnPage: function (direction) {
            var all_li = this.$(TABS_HEADER);
            if (all_li.length > 1) {
                var index = all_li.index(this.$(TABS_HEADER + '.layui-this'));
                if (index !== 0 && direction === 'left') {
                    all_li.eq(index - 1).trigger('click')
                } else if (direction === 'right') {
                    all_li.eq(index + 1).trigger('click')
                }
            }
        },

        //关闭其它标签页或所有标签
        closeOtherTabs: function (type) {
            var close_li = type === 'all' ? this.$(TABS_HEADER) : this.$(TABS_HEADER + ':not(.layui-this)');
            close_li.each(function (index, item) {
                $(item).find('.layui-tab-close').trigger('click')
            });
        },

        /**
         * Returns the action of the last controller in the controllerStack, i.e.
         * the action of the currently displayed controller in the main window (not
         * in a dialog), and null if there is no controller in the stack.
         *
         * @returns {Object|null}
         */
        getCurrentAction: function () {
            var action_id = this.$('.funenc_tab_page_body.layui-show').attr('actionid');
            if (action_id) {
                return this.actions[action_id]
            }
            return this.currentAction
        },

        /**
         * 取得当前的controller, tabheader上保存的只是action的id,
         * 我取得actionId jsID的话要通过tab_page_body去获取
         * @returns {Object|null}
         */
        getCurrentController: function () {
            var action = this.getCurrentAction();
            if (action && action.controller_stack && action.controller_stack.length > 0) {
                return _.last(action.controller_stack)
            }
            return null
        },

        /**
         * Pushes the given state, with additional information about the given
         * controller, like the action's id and the controller's title.
         *
         * @private
         * @param {string} controllerID
         * @param {Object} [state={}]
         */
        _pushState: function (controllerID, state) {
            var controller = this.controllers[controllerID];
            if (controller) {
                var action = this.actions[controller.actionID];
                if (action.target === 'new' || action.pushState === false) {
                    // do not push state for actions in target="new" or for actions
                    // that have been explicitly marked as not pushable
                    return;
                }
                state = _.extend({}, state, this._getControllerState(controller.jsID));
                this.trigger_up('push_state', {state: state});
            }
        },

        _preprocessAction: function (action, options) {
            // ensure that the context and domain are evaluated
            var context = new Context(this.userContext, options.additional_context, action.context);
            action.context = pyUtils.eval('context', context);
            if (action.domain) {
                action.domain = pyUtils.eval('domain', action.domain, action.context);
            }
            action._originalAction = JSON.stringify(action);
            var new_context = _.clone(action.context)
            delete new_context['params']
            var hash = objectHash.MD5({
                id: action.id,
                model: action.model,
                context: new_context,
                domain: action.domain,
                target: action.target,
                view_mode: action.view_mode,
                views: action.views,
                src_model: action.src_model
            });
            action.jsID = hash;
            action.pushState = options.pushState;
        },

        /**
         * delete widgets
         */
        _removeAction: function (jsID) {
            var action = this.actions[jsID];
            var controller = this.controllers[action.controllerID];
            delete this.actions[action.jsID];
            delete this.controllers[action.controllerID];
            controller.widget.destroy();
            delete this.actions[jsID];
        },

        /**
         * 在这个地方绑定的dom
         * @param {*} controller
         * @param {*} options
         */
        _pushController: function (controller, options) {
            options = options || {};

            // append the new controller to the DOM
            this._appendController(controller);
        },

        /**
         * 查找action对应的序号
         * @param {} action
         */
        get_tab_index: function (action) {
            var item_index = -1;
            var tabs = this.$('#funenc_tab_headers>li');
            tabs.each(function (index) {
                var li = $(this)
                var jsID = li.attr('lay-id');
                if (jsID && jsID != '' && jsID === action.jsID) {
                    item_index = index;
                }
            });
            return item_index
        },

        _executeAction: function (action, options) {
            var self = this;
            this.actions[action.jsID] = action;

            // pop up the new window, it is not manageed by the action manager
            if (action.target === 'new') {
                return this._executeActionInDialog(action, options);
            }

            return this.clearUncommittedChanges()
                .then(function () {
                    var controller = self.controllers[action.controllerID];
                    return self.dp.add(self._startController(controller));
                })
                .then(function (controller) {

                    if (self.currentDialogController) {
                        self._closeDialog({silent: true});
                    }

                    // update the internal state and the DOM
                    self._pushController(controller, options);

                    // record current action
                    self.currentAction = action

                    // store the controller
                    if (!action.controller_stack) {
                        action.controller_stack = [controller]
                    } else {
                        action.controller_stack.push(controller)
                    }

                    // store the action into the sessionStorage so that it can be
                    // fully restored on F5
                    self.call('session_storage', 'setItem', 'current_action', action._originalAction);
                    return action;
                })
                .fail(function () {
                    self._removeAction(action.jsID);
                });
        },

        /**
         * 在这里添加tab页
         * Appends the given controller to the DOM and restores its scroll position.
         * Also updates the control panel.
         *
         * @private
         * @param {Object} controller
         */
        _appendController: function (controller) {
            this.controlPanel.do_hide();

            var element = layui.element;

            // add a tab page
            var action = this.actions[controller.actionID]
            this.current_controller = controller;
            var $body_box;

            // 新加, 如果已经有了的话直接选
            if (this.get_tab_index(action) === -1) {

                // 如果未在选项卡中匹配到，则追加选项卡
                var name = action.name || '新标签页';
                layui.element.tabAdd(FILTER_TAB_TBAS, {
                    title: '<span>' + name + '</span>',
                    id: action.jsID
                });
                var height = this.$('.funenc-tabs-body').height();
                $body_box = $(core.qweb.render("funenc_tab_body"))
                $body_box.attr('actionid', action.jsID)
                $body_box.height(height)
                $body_box.appendTo(this.$('.funenc-tabs-body'))
                // 绑定actionID
            } else {
                $body_box = this.$('.funenc-tabs-body').find('[actionid="' + action.jsID + '"]');
                $body_box.empty();
            }
            // 如果是已经存在则只是显示出来就可以啦
            dom.append($body_box, controller.widget.$el, {
                in_DOM: this.isInDOM,
                callbacks: [{widget: controller.widget}]
            });
            // 选中jsId的tab项
            element.tabChange('layadmin-layout-tabs', action.jsID);
        },

        /**
         *
         * @private
         */
        _onHistoryBack: function () {
            if (this.currentDialogController) {
                this._closeDialog();
            }
        },

        // 关闭当前 pageTabs
        closeThisTabs: function () {
            var othis = this.$('#funenc_tab_headers .layui-this');
            if (othis.length > 0) {
                var index = othis.index()
                this.$('#funenc_tab_headers>li').eq(index).find('.layui-tab-close').trigger('click');
            }
        },

        closeAllTabs: function () {
            this.closeOtherTabs('all');
        },

        _onSearch: function (ev) {
            ev.stopPropagation();
            // AAB: the id of the correct controller should be given in data
            var currentController = this.getCurrentController();
            if (currentController) {
                var action = this.actions[currentController.actionID];
                _.extend(action.env, this._processSearchData(action, ev.data));
                if (currentController.widget.reload) {
                    currentController.widget.reload(_.extend({offset: 0}, action.env));
                }
            }
        },

        /**
         * 说明，这里将search_view绑定到了action上面去了
         * @param {*} action
         */
        _createSearchView: function (action) {

            // if requested, keep the searchview of the current action instead of
            // creating a new one
            if (action._keepSearchView) {
                var currentAction = this.getCurrentAction();
                if (currentAction) {
                    action.searchView = currentAction.searchView;
                    action.env = currentAction.env; // make those actions share the same env
                    return $.when(currentAction.searchView);
                } else {
                    // there is not searchview to keep, so reset the flag to false
                    // to ensure that the one that will be created will be correctly
                    // destroyed
                    action._keepSearchView = false;
                }
            }

            // AAB: temporarily create a dataset, until the SearchView is refactored
            // and stops using it
            var dataset = new data.DataSetSearch(this, action.res_model, action.context, action.domain);
            if (action.res_id) {
                dataset.ids.push(action.res_id);
                dataset.index = 0;
            }

            // find 'search_default_*' keys in actions's context
            var searchDefaults = {};
            _.each(action.context, function (value, key) {
                var match = /^search_default_(.*)$/.exec(key);
                if (match) {
                    searchDefaults[match[1]] = value;
                }
            });

            var searchView = new SearchView(this, dataset, action.searchFieldsView, {
                $buttons: $('<div>'),
                action: action,
                disable_custom_filters: action.flags.disableCustomFilters,
                search_defaults: searchDefaults,
            });

            return searchView.appendTo(document.createDocumentFragment()).then(function () {
                action.searchView = searchView;
                return searchView;
            });
        },
        showMaxMain: function () {
            $('.o_main').css({'padding-left': 0, 'z-index': 99});
            core.bus.trigger('show_sidebar')
        },
        hindMaxMain: function () {
            $('.o_main').css({'padding-left': this.PADDING_LEFT, 'z-index': 1})
            core.bus.trigger('hide_sidebar')
        },

        loadState: function (state) {
            var self = this;
            var action;
            if (!state.action) {
                return $.when();
            }
            if (_.isString(state.action) && core.action_registry.contains(state.action)) {
                if (core.home_client_action 
                    && state.action === core.home_client_action.tag) {
                    return $.when().then(function () {
                        self.trigger_up('open_home');
                    })
                }
                action = {
                    params: state,
                    tag: state.action,
                    type: 'ir.actions.client',
                };
            } else {
                action = state.action;
            }
            return this.doAction(action, {
                clear_breadcrumbs: true,
                pushState: false,
            });
        },

    })
});