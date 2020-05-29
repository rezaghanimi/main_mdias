odoo.define('funenc.many2one', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var core = require('web.core');
    var data = require('web.data');
    var dialogs = require('web.view_dialogs');
    

    var _t = core._t;

    /**
     * 重写，目的是为了添加旋转箭头, direct_search 直接弹出搜索对话框, 用于像企业微信这些
     */
    relational_fields.FieldMany2One.include({
        
        /**
         * 搜索的时候转动箭头
         */
        _onInputClick: function () {
            if (this.attrs.options.direct_search) {
                this.direct_search()
            } else {
                if (this.$input.parents(".modal-body").length > 0) {
                    this.$input.autocomplete("option", "appendTo", "");
                } else {
                    this.$input.autocomplete("option", "appendTo", ".o_web_client");
                }
    
                if (this.$input.autocomplete("widget").is(":visible")) {
                    this.$input.autocomplete("close");
                    this.$(".o_dropdown_arrow").addClass("is-reverse")
                } else if (this.floating) {
                    this.$(".o_dropdown_arrow").removeClass("is-reverse")
                    this.$input.autocomplete("search"); // search with the input's content
                } else {
                    this.$(".o_dropdown_arrow").removeClass("is-reverse")
                    this.$input.autocomplete("search", ''); // search with the empty string
                }
            }
        },

        direct_search: function () {
            var self = this;
            var def = $.Deferred();
            this.orderer.add(def);

            var context = this.record.getContext(this.recordParams);
            var domain = this.record.getDomain(this.recordParams);

            // Add the additionalContext
            _.extend(context, this.additionalContext);

            var blacklisted_ids = this._getSearchBlacklist();
            if (blacklisted_ids.length > 0) {
                domain.push(['id', 'not in', blacklisted_ids]);
            }

            // Clear the value in case the user clicks on discard
            self.$('input').val('');
            return self._searchCreatePopup("search");
        },

        /**
         * 添加class
         * @param {*} value 
         */
        reinitialize: function (value) {
            this._super(value);
            this.$(".o_dropdown_arrow").addClass("is-reverse")
        },

        /**
         * 增加limit参数
         */
        init: function () {
            this._super.apply(this, arguments);
            if (this.attrs.options.limit) {
                this.limit = this.attrs.options.limit
            }
        },

        /**
         * 扩展搜索，增加自定义domain
         * @param {*} search_val 
         */
        _search: function (search_val) {
            var self = this;
            var def = $.Deferred();
            this.orderer.add(def);

            var domain_def = $.Deferred()
            var context = this.record.getContext(this.recordParams);
            if (this.attrs.options.dynamic_domain_model &&
                this.attrs.options.dynamic_domain_method) {
                this._rpc({
                    "model": this.attrs.options.dynamic_domain_model,
                    "method": this.attrs.options.dynamic_domain_method,
                    "args": [this.record]
                }).then(function (rst) {
                    domain_def.resolve(rst)
                })
            } else {
                domain_def.resolve(this.record.getDomain(this.recordParams))
            }

            var self = this
            domain_def.then(function (domain) {
                // Add the additionalContext
                _.extend(context, self.additionalContext);

                var blacklisted_ids = self._getSearchBlacklist();
                if (blacklisted_ids.length > 0) {
                    domain.push(['id', 'not in', blacklisted_ids]);
                }

                self._rpc({
                    model: self.field.relation,
                    method: "name_search",
                    kwargs: {
                        name: search_val,
                        args: domain,
                        operator: "ilike",
                        limit: self.limit + 1,
                        context: context,
                    }
                })
                    .then(function (result) {
                        // possible selections for the m2o
                        var values = _.map(result, function (x) {
                            x[1] = self._getDisplayName(x[1]);
                            return {
                                label: _.str.escapeHTML(x[1].trim()) || data.noDisplayContent,
                                value: x[1],
                                name: x[1],
                                id: x[0],
                            };
                        });

                        // search more... if more results than limit
                        if (values.length > self.limit) {
                            values = values.slice(0, self.limit);
                            values.push({
                                label: _t("Search More..."),
                                action: function () {
                                    self._rpc({
                                        model: self.field.relation,
                                        method: 'name_search',
                                        kwargs: {
                                            name: search_val,
                                            args: domain,
                                            operator: "ilike",
                                            limit: 160,
                                            context: context,
                                        },
                                    })
                                        .then(self._searchCreatePopup.bind(self, "search"));
                                },
                                classname: 'o_m2o_dropdown_option',
                            });
                        }
                        var create_enabled = self.can_create && !self.nodeOptions.no_create;
                        // quick create
                        var raw_result = _.map(result, function (x) { return x[1]; });
                        if (create_enabled && !self.nodeOptions.no_quick_create &&
                            search_val.length > 0 && !_.contains(raw_result, search_val)) {
                            values.push({
                                label: _.str.sprintf(_t('Create "<strong>%s</strong>"'),
                                    $('<span />').text(search_val).html()),
                                action: self._quickCreate.bind(self, search_val),
                                classname: 'o_m2o_dropdown_option'
                            });
                        }
                        // create and edit ...
                        if (create_enabled && !self.nodeOptions.no_create_edit) {
                            var createAndEditAction = function () {
                                // Clear the value in case the user clicks on discard
                                self.$('input').val('');
                                return self._searchCreatePopup("form", false, self._createContext(search_val));
                            };
                            values.push({
                                label: _t("Create and Edit..."),
                                action: createAndEditAction,
                                classname: 'o_m2o_dropdown_option',
                            });
                        } else if (values.length === 0) {
                            values.push({
                                label: _t("No results to show..."),
                            });
                        }

                        def.resolve(values);
                    });
            })

            return def;
        },

        /**
         * 重写，增加自定义的view
         * @param {*} view 
         * @param {*} ids 
         * @param {*} context 
         */
        _searchCreatePopup: function (view, ids, context) {
            var self = this;
            return new dialogs.SelectCreateDialog(this, _.extend({}, this.nodeOptions, {
                res_model: this.field.relation,
                domain: this.record.getDomain({fieldName: this.name}),
                context: _.extend({}, this.record.getContext(this.recordParams), context || {}),
                title: (view === 'search' ? _t("Search: ") : _t("Create: ")) + this.string,
                initial_ids: ids ? _.map(ids, function (x) { return x[0]; }) : undefined,
                initial_view: view,
                js_class: this.attrs.options.js_class || undefined,
                disable_multiple_selection: true,
                no_create: !self.can_create,
                on_selected: function (records) {
                    self.reinitialize(records[0]);
                    self.activate();
                }
            })).open();
        },

        /**
         * @private
         */
        _bindAutoComplete: function () {
            var self = this;

            // avoid ignoring autocomplete="off" by obfuscating placeholder, see #30439
            if (this.$input.attr('placeholder')) {
                this.$input.attr('placeholder', function (index, val) {
                    return val.split('').join('\ufeff');
                });
            }

            this.$input.autocomplete({
                source: function (req, resp) {
                    _.each(self._autocompleteSources, function (source) {
                        // Resets the results for this source
                        source.results = [];

                        // Check if this source should be used for the searched term
                        if (!source.validation || source.validation.call(self, req.term)) {
                            source.loading = true;

                            // Wrap the returned value of the source.method with $.when.
                            // So event if the returned value is not async, it will work
                            $.when(source.method.call(self, req.term)).then(function (results) {
                                source.results = results;
                                source.loading = false;
                                resp(self._concatenateAutocompleteResults());
                            });
                        }
                    });
                },

                select: function (event, ui) {
                    // we do not want the select event to trigger any additional
                    // effect, such as navigating to another field.
                    event.stopImmediatePropagation();
                    event.preventDefault();

                    var item = ui.item;
                    self.floating = false;
                    if (item.id) {
                        self.reinitialize({ id: item.id, display_name: item.name });
                    } else if (item.action) {
                        item.action();
                    }
                    return false;
                },

                focus: function (event) {
                    event.preventDefault(); // don't automatically select values on focus
                },

                close: function (event) {
                    self.$(".o_dropdown_arrow").addClass("is-reverse")
                    // it is necessary to prevent ESC key from propagating to field
                    // root, to prevent unwanted discard operations.
                    if (event.which === $.ui.keyCode.ESCAPE) {
                        event.stopPropagation();
                    }
                },
                autoFocus: true,
                html: true,
                minLength: 0,
                delay: this.AUTOCOMPLETE_DELAY,
            });

            this.$input.autocomplete("option", "position", { my: "left top-110", at: "left bottom+110" });
            this.autocomplete_bound = true;
        }
    });
});