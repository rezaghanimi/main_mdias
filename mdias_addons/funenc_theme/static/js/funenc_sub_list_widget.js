odoo.define('funenc.sub_list_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var data = require('web.data');
    var dom = require('web.dom');
    var ListController = require('web.ListController');
    var fnt_table = require('funenc.fnt_table');
    var pyUtils = require('web.py_utils');
    var SearchView = require('web.SearchView');
    var widgetRegistry = require('web.widget_registry');
    var ControlPanel = require('web.ControlPanel');
    var qweb = core.qweb
    var view_registry = require('web.view_registry');

    /**
     * 封装list, 让list等作为组件进行调用, 说明，一些参数是通过view的option给传入进来的
     */
    var SubListWidget = Widget.extend({
        app: undefined,
        dataset: undefined,
        domain: [],
        context: {},
        options: {},
        initial_ids: undefined,
        list_view_id: undefined,
        search_view_id: undefined,
        res_model: undefined,
        list_controller: undefined,
        control_pannel: undefined,
        view_class: undefined,
        custom_events: {
            // 处理搜索
            search: function (event) {
                // prevent this event from bubbling up to the action manager
                event.stopPropagation(); 
                var d = event.data;
                var searchData = this._process_search_data(d.domains, d.contexts, d.groupbys);
                this.list_controller.reload(_.extend({ offset: 0 }, searchData));
            },
            get_controller_context: '_onGetControllerContext',
            env_updated: function (event) {
                event.stopPropagation();
            },
            push_state: '_onPushState',
        },

        _onPushState: function (event) {
            event.stopPropagation();
        },

        /**
         * 取得控制器，方便外部进行加载
         */
        get_controller: function() {
            return this.list_controller;
        },

        /**
         * 说明，传进来的第二个参数为action
         * @param {} parent
         * @param {*} action
         */
        init: function (parent, options) {
            this._super.apply(this, arguments)

            // 有些子视图也需要control pannel, 添加一个control pannel在这里
            if (true || options.need_control_pannel) {
                this.controlPanel = new ControlPanel(this);
                this.controlPanel.insertBefore(this.$el);
            }

            this.options = options
            this.initial_ids = options.initial_ids;
            this.domain = options.domain || []
            this.context = options.context || {};
            this.hide_toolbar = options.hide_toolbar

            _.defaults(this.options, { initial_view: 'search' });

            this.controller_class = options.controller_class || ListController
            this.res_model = options.res_model || "";

            // 指定示图
            this.list_view_id = options.list_view_id || false
            this.view_class = options.view_class || false
           
            // FIXME: remove this once a dataset won't be necessary anymore to interact
            // with data_manager and instantiate views
            this.dataset = new data.DataSet(this, this.res_model, this.context);
        },

        start: function () {
            if (this.options.class) {
                this.$el.addClass(this.options.class)
            }
            var self = this;
            var user_context = this.getSession().user_context;

            var _super = this._super.bind(this);

            var context = pyUtils.eval_domains_and_contexts({
                domains: [],
                contexts: [user_context, this.context]
            }).context;

            var search_defaults = {};
            _.each(context, function (value_, key) {
                var match = /^search_default_(.*)$/.exec(key);
                if (match) {
                    search_defaults[match[1]] = value_;
                }
            });
            
            this.loadViews(this.dataset.model, this.dataset.get_context().eval(),
                [[this.options.list_view_id || false, 'list'], [this.options.sarch_view_id || false, 'search']], {})
                .then(this.setup.bind(this, search_defaults))
                .then(function (fragment) {
                    dom.append(self.$el, fragment, {
                        callbacks: [{ widget: self.list_controller }],
                        in_DOM: true,
                    });
                    _super();
                });
        },

        /**
         * 调用树视图, 并且带搜索
         */
        setup: function (search_defaults, fields_views) {
            var self = this;
            var fragment = document.createDocumentFragment();
            var searchDef = $.Deferred();

            // Set the dialog's header and its search view
            var $header = $('<div/>').addClass('sub_list_header').appendTo(fragment);
            if (this.options.custom_area_template) {
                var custom = $(qweb.render(this.options.custom_area_template));
                custom.appendTo($header);
            }
            var $pager = $('<div/>').addClass('o_pager').appendTo($header);

            // search view 是将扩展搜索放在了$buttons里面，所以可以将$buttons放到别的地方
            var $buttons = $('<div/>').addClass('o_search_options').appendTo($header)
            var options = {
                //$buttons: $buttons,
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

                // 隐藏，要通过它来默认搜索
                if (options.has_search) {
                    $buttons.show()
                    searchview.$el.show();
                } else {
                    $buttons.hide();
                    searchview.$el.hide();
                }

                // 初始的时候就进行了搜索，直接第一次加载的时候搜索
                var VIEW_CLASS   = undefined
                var fieldsView = fields_views['list'];
                var parsedXML = new DOMParser().parseFromString(fieldsView.arch, "text/xml");
                var key = parsedXML.documentElement.getAttribute('js_class');
                if (key) {
                    VIEW_CLASS  = view_registry.get(key);
                }
                if (!VIEW_CLASS) {
                    VIEW_CLASS  = fnt_table
                }
                
                var listView = new VIEW_CLASS(fields_views.list, _.extend({
                    context: searchResult.context,
                    domain: searchResult.domain,
                    groupBy: searchResult.groupBy,
                    modelName: self.dataset.model,
                    hasSelectors: !self.options.disable_multiple_selection,
                    readonly: true,
                }, self.options.list_view_options));

                listView.setController(self.controller_class);
                return listView.getController(self);
            }).then(function (controller) {
                self.list_controller = controller;
                if (self.controlPanel) {
                    self.list_controller.set_cp_bus(self.controlPanel);
                }
                return self.list_controller.appendTo(fragment);
            }).then(function () {
                searchview.toggle_visibility(true);
                self.list_controller.do_show();
                self.list_controller.renderPager($pager);
                return fragment;
            });
        },

        reload: function (options) {
            this.list_controller.trigger_up("reload", options);
        },

        /**
         * 处理搜索
         * @param {*} domains
         * @param {*} contexts
         * @param {*} groupbys
         */
        _process_search_data: function (domains, contexts, groupbys) {
            var results = pyUtils.eval_domains_and_contexts({
                domains: [this.domain].concat(domains),
                contexts: [this.context].concat(context),
                group_by_seq: groupbys || [],
                eval_context: this.getSession().user_context,
            });
            var context = _.omit(results.context, function (value, key) { return key.indexOf('search_default_') === 0; });
            return {
                context: context,
                domain: results.domain,
                groupBy: results.group_by,
            };
        },
    });

    widgetRegistry.add('SubListWidget', SubListWidget);

    return SubListWidget;
});