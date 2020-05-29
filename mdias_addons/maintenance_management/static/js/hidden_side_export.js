odoo.define('hidden_side_export', function (require) {
    "use strict";

    var ListController = require('web.ListController')
    var core = require('web.core');;
    var _t = core._t;
    var Sidebar = require('web.Sidebar');
    // 重写 renderSidebar 方法
    ListController.include({
        buttons_template: 'ListView.buttons_new',
        renderSidebar: function ($node) {
        var self = this;
        if (this.hasSidebar) {
            var other = [];
            if (this.archiveEnabled) {
                other.push({
                    label: _t("Archive"),
                    callback: function () {
                        Dialog.confirm(self, _t("Are you sure that you want to archive all the selected records?"), {
                            confirm_callback: self._onToggleArchiveState.bind(self, true),
                        });
                    }
                });
                other.push({
                    label: _t("Unarchive"),
                    callback: this._onToggleArchiveState.bind(this, false)
                });
            }
            if (this.is_action_enabled('delete')) {
                other.push({
                    label: _t('Delete'),
                    callback: this._onDeleteSelectedRecords.bind(this)
                });
            }
            this.sidebar = new Sidebar(this, {
                editable: this.is_action_enabled('edit'),
                env: {
                    context: this.model.get(this.handle, {raw: true}).getContext(),
                    activeIds: this.getSelectedIds(),
                    model: this.modelName,
                },
                actions: _.extend(this.toolbarActions, {other: other}),
            });
            this.sidebar.appendTo($node);

            this._toggleSidebar();
        }
    },
    })
});
