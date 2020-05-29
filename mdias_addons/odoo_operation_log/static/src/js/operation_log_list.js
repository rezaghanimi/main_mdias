odoo.define('odoo_operation_log.operation_log_list', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var LogList = AbstractAction.extend({
        on_attach_callback: function () {
            this._render_page();
        },

        _render_page: function () {
            var self = this;
            self.$el.html('<div id="vue-app">');
            self._rpc({
                model: 'vue_template_manager.template_manage',
                method: 'get_template_content',
                kwargs: {
                    module_name: 'odoo_operation_log',
                    template_name: 'log_list_page'
                }
            }).then(function (el) {
                Vue.nextTick(function () {

                    new Vue({
                        template: el,
                        data() {
                            return {
                                OFFSET: 0,
                                last_log_id: 1,
                                current_dataset: [],
                                limit: 200,
                                fields_dataset: [],
                                dialogVisible: false,
                                log_info: {
                                    log_types: {},
                                    sum_count: 0
                                },
                                search_form: {
                                    log_type: null,
                                    log_date_range: [],
                                    user_login: null,
                                },
                                rules: [],
                                loading: true,
                                current_page: 1,
                                tableHeight: 0

                            }
                        },
                        computed: {
                            page_count: function () {
                                return Math.ceil(this.log_info.sum_count / this.limit)
                            },
                            total_data: function () {
                                return this.limit * (this.current_page - 1) + this.current_dataset.length
                            }
                        },
                        methods: {
                            lookLogDetail: function (row) {

                                var $vue = this;
                                return self._rpc({
                                    'model': 'odoo_operation_log.log',
                                    'method': 'get_fields_log',
                                    'kwargs': {log_id: row.id},
                                }).then(function (result) {
                                    $vue.dialogVisible = true;
                                    $vue.fields_dataset = result;
                                });
                            },
                            request_logs: function () {
                                var $vue = this;
                                this.loading = true;
                                return self._rpc({
                                    'model': 'odoo_operation_log.log',
                                    'method': 'get_logs',
                                    'kwargs': {
                                        page_num: $vue.current_page,
                                        limit: $vue.limit,
                                        log_type: $vue.search_form.log_type,
                                        date_range: $vue.search_form.log_date_range,
                                        user_login: $vue.search_form.user_login
                                    },
                                }).then(function (result) {
                                    $vue.current_dataset = result
                                    $vue.loading = false;
                                    $vue.request_logs_info();

                                });
                            },
                            request_logs_info: function () {
                                var $vue = this;
                                return self._rpc({
                                    'model': 'odoo_operation_log.log',
                                    'method': 'get_logs_info',
                                    'kwargs': {
                                        log_type: $vue.search_form.log_type,
                                        date_range: $vue.search_form.log_date_range,
                                        user_login: $vue.search_form.user_login
                                    }
                                }).then(function (result) {
                                    $vue.log_info = result;

                                });


                            },
                            pageCurrentChange: function (val) {
                                this.current_page = val;
                                this.request_logs()
                            },
                            onSearch() {
                                this.request_logs()
                            },
                            onClear() {
                                _.forEach(this.search_form, (v, k) => {
                                    this.search_form[k] = null
                                });
                                this.request_logs();
                            },
                            handleSizeChange(val) {
                                this.limit = val;
                                this.request_logs()
                            }
                        },
                        watch: {},
                        mounted: function () {
                            this.$nextTick(function () {
                                 this.tableHeight = ($('.o_content').outerHeight(true) - 150) + 'px'
                            }.bind(this));
                            this.request_logs_info();
                            this.request_logs();
                            debugger

                        }
                    }).$mount(self.$el.children('div').get(0));
                });
            });
        }
    });
    core.action_registry.add('ActionLogList', LogList)
});

