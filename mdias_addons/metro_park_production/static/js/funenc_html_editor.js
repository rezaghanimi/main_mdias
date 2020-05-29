odoo.define('metro_park_production.funenc_html_editor', function (require) {
    "use strict";

    var registry = require('web.field_registry');
    var basic_fields = require('web.basic_fields');
    // var AbstractField = require('web.AbstractField');
    var DebouncedField = basic_fields.DebouncedField

    var FunencHtmlEditor = DebouncedField.extend({

        template: "metro_park_production.funenc_html_editor",
        events: {},

        start: function () {
            this._super.apply(this, arguments);
            // this.inited = false
            // debugger
            // setTimeout(() => {
            //     tinymce.init({
            //         selector: '.fnt_html_editor',
            //         language: 'zh_CN',//加载中文语言表
            //         height: 800,
            //         plugins: "table", //依赖表格插件
            //         menubar: false,
            //         base_url: "metro_park_production/static/js/tinymce/",
            //         templates: [
            //             {
            //                 "title": "检修大屏",
            //                 "description": "高大路停车场",
            //                 "url": "/metro_park_production/static/js/tinymce/template.html"
            //             }],
            //     });
            // }, 100);
            // debugger
        },


        destroy: function () {
            this._super.apply(this, arguments);
        },

        _formatValue: function (value) {
            return this._super.apply(this, arguments) || '';
        },

        _getValue: function () {
            var content = tinyMCE.activeEditor.getContent();
            console.log('the content is:', content)
            return content
        },

        _renderEdit: function () {
            var self = this
            if (!this.inited) {
                this.inited = true
               var textArea_id = 'big_screen'
                setTimeout(() => {
                    var tinymce_info = tinymce.init({
                        selector: '#big_screen',
                        base_url: "/metro_park_production/static/js/tinymce/",
                        language: 'zh_CN',//加载中文语言表
                        plugins: "table,template", //依赖table插件
                        height: 800,
                        templates: [
                            {
                                "title": "检修大屏",
                                "description": "高大路停车场",
                                "url": "/metro_park_production/static/js/tinymce/gaodalu_overhaul_template.html"
                            },
                            {
                                "title": "检修大屏",
                                "description": "板桥停车场",
                                "url": "/metro_park_production/static/js/tinymce/banqiao_overhaul_template.html"
                            },
                            {
                                "title": "安全检修",
                                "description": "高大路停车场",
                                "url": "/metro_park_production/static/js/tinymce/gaodalu_safe_template.html"
                            },
                            {
                                "title": "安全检修",
                                "description": "板桥停车场",
                                "url": "/metro_park_production/static/js/tinymce/banqiao_safe_template.html"
                            }
                        ],

                        init_instance_callback: function (editor) {
                            editor.setContent(self.value);
                            editor.on('blur', function (e) {
                                self._doAction()
                            });
                        }
                    },
                    );
                    console.log(tinymce)
                 if (tinymce.editors.length > 0) {
                   // tinymce.execCommand('mceFocus', true, textArea_id );
                   tinymce.execCommand('mceRemoveEditor',true, textArea_id);
                   tinymce.execCommand('mceAddEditor',true, textArea_id);
                }
                }, 100);
                // debugger
            }
        }
    });

    registry.add('FunencHtmlEditor', FunencHtmlEditor)

    return FunencHtmlEditor;
});
