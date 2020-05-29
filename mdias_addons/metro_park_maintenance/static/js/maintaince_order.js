odoo.define('maintaince_order_btn', function (require) {
    'use strict';

    var ListView = require("web.ListView");
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.fnt_table_render");
    var core = require('web.core');
    var ListController = require('funenc.fnt_table_controller');
    var qweb = core.qweb;

    var maintaince_order_render = ListRenderer.extend({});
    var maintaince_order_Controller = ListController.extend({
        buttons_template: 'maintaince_order_btn',
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
            this.id = params.initialState.context.id;
            this.params = params;
            this.model_base = params.modelName;
        },
        renderButtons: function ($node) {
            if (!this.noLeaf && this.hasButtons) {
                this.$buttons = $(qweb.render(this.buttons_template, {
                    widget: this,
                }));
                this.$buttons.on('click', '.send_job', this._send_job.bind(this));
                this.$buttons.on('click', '.start_job', this._start_job.bind(this));
                this.$buttons.on('click', '.finish_job', this._finish_job.bind(this));
                this.$buttons.on('click', '.finish_job_confirm', this._finish_job_confirm.bind(this));
                this.$buttons.on('click', '.force_close', this._force_close.bind(this));
                this.$buttons.on('click', '.order_obsolete', this._order_obsolete.bind(this));
                this.$buttons.appendTo($node);
            }
        },
        _send_job: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'send_job',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },
        _start_job: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'start_job',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

        _finish_job: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'finish_job',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

        _finish_job_confirm: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'finish_job_confirm',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

        _force_close: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'force_close',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })
        },

        _order_obsolete: function () {
            var self = this;
            let fields = {};
            _.forEach(self.renderer.columns, function (item) {
                if (item.tag === 'field') {
                    fields[item.attrs.name] = item.attrs.string ? item.attrs.string : self.renderer.state.fields[item.attrs.name].string
                }
            });
            var records;
            if (!records) {
                records = _.map(this.selectedRecords, function (id) {
                    return self.model.localData[id].res_id;
                });
            }
            self._rpc({
                model: 'metro_park_maintenance.maintaince_order',
                method: 'order_obsolete',
                kwargs: {'ids': records}
            }).then(function (res) {
                self.do_action(res,{
                    on_close: function () {
                        self.reload()
                    }
                })
            })

        },
    });

    var maintaince_order_btn = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: maintaince_order_render,
            Controller: maintaince_order_Controller
        }),
        viewType: "list"
    });

    view_registry.add("maintaince_order_btn", maintaince_order_btn);
});