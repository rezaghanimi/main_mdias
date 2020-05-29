/**
* apartment client
*/
odoo.define('funenc.metro_park.map_widget', function (require) {
    "use strict";

    var Widget = require('web.Widget');

    /**
     * apartment_client
     */
    var MapWidget = Widget.extend({

        xml_file_data: undefined,
        editorUI: undefined,
        themes: undefined,
        graph: undefined,

        /**
         * 
         * @param {*} parent 
         * @param {*} xml_file 
         */
        init: function (parent, xml_file_data) {
            this._super.apply(this, arguments)
            this.xml_file_data = xml_file_data
            this.graph = window.graph
        },

        /**
         * 初始化数据
         */
        willStart: function () {
            var self = this
            var def = $.Deferred();

            // Adds required resources (disables loading of fallback properties, this can only
            // be used if we know that all keys are defined in the language specific file)

            mxResources.loadDefaultBundle = false;
            var bundle = mxResources.getDefaultBundle(RESOURCE_BASE, mxLanguage)
             || mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);

            //  动态加载资源
            mxUtils.getAll([bundle, STYLE_PATH + '/default.xml'], function (xhr) {

                var bundle_cache = {
                    valid: false,
                    part0: undefined,
                    part1: undefined
                }

                // Adds bundle text to resources
                bundle_cache.part0 = xhr[0].getText()
                bundle_cache.part1 = xhr[1].getDocumentElement();
                bundle_cache.valid = true

                mxResources.parse(bundle_cache.part0);

                // Configures the default graph theme
                self.themes = new Object();
                self.themes[Graph.prototype.defaultThemeName] = bundle_cache.part1;

                def.resolve()
            }, function () {
                def.reject()
            })

            return def;
        },

        /**
         * start
         */
        start: function () {
            this._super.apply(this)
            // 导入数据
            this.reload_map(this.xml_file_data);
        },

        /**
         * 重新加载资源
         */
        reload_map: function(map_data) {
            this.editorUI = new EditorUi(new Editor(false, this.themes), this.$el[0]);
            this.graph = this.editorUI.editor.graph
            if (map_data) {
                var doc = $.parseXML(map_data);

                // 保存data
                this.xml_file_data = map_data;
                
                graph.importGraphModel(doc.documentElement)
                // 禁止选中
                graph.setCellsSelectable(false)
                // 禁止移动
                graph.setCellsMovable(false)
                // 禁止编辑
                graph.setCellsEditable(false) 
                // 移动到中心
                graph.center();
            }
        },

        get_graph: function() {
            return this.editorUI? this.editorUI.editor.graph : undefined
        },

        destroy: function() {
            this._super.apply(this, arguments)
            if(this.editorUI) {
                this.editorUI.destroy();
            }
        }
    });

    return MapWidget
});
