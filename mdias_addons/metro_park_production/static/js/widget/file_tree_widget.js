/**
 * Created by YCQ on 19/08/18/0018.
 */
odoo.define('file_tree_widget', function (require) {
    'use strict';

    var Widget = require('web.Widget');
    var Dialog = require('web.Dialog');
    var widget_registry = require('web.widget_registry');

    var file_tree_widget = Widget.extend({
        template: 'tem_file_tree_widget',

        events: _.extend({}, Widget.prototype.events, {
            'click .look': function () {
                this._look(false)
            },
            'click .down': function () {
                this._look(true)
            },
            'click .del': '_del',
            'click .edit': '_edit',
        }),

        init: function (parent, record, options) {
            this._super(parent, record, options);
            this.record = record
        },

        _look: function (can_down) {
            var href = '/web/content/' + this.record.model +
                '/' + this.record.res_id + '/file_content/' +
                this.record.data.file_name;
            href  = can_down === true ? href + '?download=true' : href;
            window.open(href)
        },

        _del: function () {
            var self = this;
            Dialog.confirm(self, '是否确定删除?', {
                title: '提示',
                confirm_callback: function () {
                    self._rpc({
                        model: self.record.model,
                        method: 'unlink',
                        args: [self.record.res_id],
                    }).then(function () {
                        self.trigger_up('reload')
                    })
                }
            });
        },

        _edit: function () {
            var self = this;
            self.do_action({
                type: 'ir.actions.act_window',
                res_model: self.record.model,
                res_id: self.record.res_id,
                target: 'new',
                views: [[false, 'form']],
            },{
                on_close: function () {
                    self.trigger_up('reload');
                }
            });
        }
    });

    widget_registry.add('file_tree_widget', file_tree_widget);

    return file_tree_widget
});
