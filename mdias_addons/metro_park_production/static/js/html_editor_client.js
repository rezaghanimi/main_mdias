odoo.define('metro_park_production.funenc_html_editor_client', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');

    /**
     * 看计划时间轴
     */
    var funenc_html_editor_client = AbstractAction.extend(ControlPanelMixin, {

        template: 'metro_park_production.funenc_html_editor',

        init: function (parent, action) {
            this._super.apply(this, arguments)
            this.screen_page_id = action.context.active_id || action.params.active_id || action.page_id
        },

        start: function () {
            this._super.apply(this, arguments)
        },

        willStart: function () {
            return this._super.apply(this, arguments)
        },

        on_attach_callback: function () {
            this._super.apply(this)
            var self = this
            if (!this.editor) {
                var editor = new Jodit(this.$('.funenc_editor_box')[0], {
                    textIcons: false,
                    iframe: false,
                    iframeStyle: '*,.jodit_wysiwyg {color:red;}',
                    height: 300,
                    defaultMode: Jodit.MODE_WYSIWYG,
                    observer: {
                        timeout: 100
                    },
                    uploader: {
                        url: 'https://xdsoft.net/jodit/connector/index.php?action=fileUpload'
                    },
                    filebrowser: {
                        // buttons: ['list', 'tiles', 'sort'],
                        ajax: {
                            url: 'https://xdsoft.net/jodit/connector/index.php'
                        }
                    },
                    commandToHotkeys: {
                        'openreplacedialog': 'ctrl+p'
                    }
                });
            }
        }
    });

    core.action_registry.add('funenc_html_editor_client', funenc_html_editor_client);

    return funenc_html_editor_client;
});