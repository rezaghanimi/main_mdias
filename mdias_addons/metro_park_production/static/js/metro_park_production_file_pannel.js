/**
 * Created by YCQ on 19/08/18/0018.
 */
odoo.define("metro_park_production_file_pannel", function (require) {
    "use strict";

    var Dialog = require('web.Dialog');
    var core = require('web.core');
    var QWeb = core.qweb;
    var widgetRegistry = require('web.widget_registry');
    var search_pannel_default = require('funenc.custom_search_pannel');

    var metro_park_production_file_pannel = search_pannel_default.extend({
        events: _.extend({}, search_pannel_default.prototype.events, {
            'click .upload_production_files': 'upload_production_files',
        }),

        upload_production_files: function () {
            var self = this;
            var get_type_option = function () {
                return self._rpc({
                    model: 'metro_park_production.file_type',
                    method: 'search_read',
                    domain: [],
                    fields: ['name']
                })
            }
            var get_html = function () {
                return self._rpc({
                    model: 'vue_template_manager.template_manage',
                    method: 'get_template_content',
                    kwargs: {module_name: 'metro_park_production', template_name: 'upload_file'}
                })
            }

            $.when(get_type_option(), get_html()).then(function (rst, $el) {
                var dialog = new Dialog(this, {
                    title: '上传文件',
                    size: 'medium',
                    $content: $el,
                    buttons: []
                });
                dialog.open().opened(function () {
                    self._render_upload(rst)
                });
                dialog.on("closed", self, function () {
                    self.trigger_up('reload')
                });
            })
        },

        _render_upload: function (type_options) {
            new Vue({
                el: '#production_file_app',
                data(){
                    return {
                        options: type_options,
                        file_type: '',
                        upload_data: {
                            file_type: ''
                        },
                        fileList: []
                    }
                },
                methods: {
                    submitUpload() {
                        var file_type = this.file_type;
                        if (!this.file_type) {
                            this.$notify({
                                title: '警告',
                                message: '未指定上传文件类型',
                                type: 'warning'
                            });
                            return
                        }
                        this.upload_data.file_type = file_type;
                        this.$refs.upload.submit();
                    },
                }
            })
        }
    });

    widgetRegistry.add("metro_park_production_file_pannel", metro_park_production_file_pannel);

    return metro_park_production_file_pannel
});
