odoo.define('funenc.left_tree_controller', function (require) {
    "use strict";

    /**
     * controller for fnt table
     */
    var ListController = require('funenc.fnt_table_controller');
    var AbstractAction = require('web.AbstractAction');
    var left_tree_id = 1024

    var left_tree_controller = ListController.extend({
        template: 'FunencLeftTreeList',

        /**
         * 重写开始函数，扩展树形, 这个类作类基类存在，使用的话继承这个基类进行
         */
        start: function () {
            AbstractAction.prototype.start.apply(this, arguments)

            this.tree_id = "user_tree" + left_tree_id++

            this.$el.css('height', 'calc(100% - 20px)')
            this.$el.addClass('left_tree_controller')

            this.$buttons = this.$('.operation_btn')
            this.$search = this.$('.search')
            this.$search_buttons = this.$('.search_btns')
            this.$sidebar = this.$('.side_bar')
            this.$pager = this.$('.pager')
            this.$custom_search = this.$('.custom_search')
            this.$search = this.$('.search')
            this.$switch_buttons = this.$('.switch_btn')

            this._init_spliter();

            this._render_tree_tempate();

            var $content = this.$('.right_table')
            this.renderer.appendTo($content);

            this._renderControlPanelElements();

            return this._update(this.initialState);
        },

        _init_spliter: function () {
            var left_tree = this.$('.left_tree')
            var right_table = this.$('.right_table')
            Split([left_tree[0], right_table[0]], {
                sizes: [20, 80],
            })
        },

        /**
         * 以下代码公作参考
         */
        on_attach_callback: function () {
            // var self = this;
            // this.app = new Vue({
            //     el: "#" + this.tree_id,
            //     data() {
            //         return {
            //             defaultProps: {
            //                 children: "sub",
            //                 label: "name",
            //                 id: "id",
            //                 isLeaf: 'leaf'
            //             }
            //         };
            //     },

            //     methods: {
            //         handleNodeClick(data) {
            //             self._rpc({
            //                 model: 'funenc.wechat.department',
            //                 method: 'get_children_dep_ids',
            //                 args: [data.id]
            //             }).then(function (ids) {
            //                 self.trigger_up("search", {
            //                     domains: [[["department_ids", "in", ids]]],
            //                 });
            //             })
            //         },

            //         loadNode(node, resolve) {
            //             var id = (node.data && node.data.id) || null;
            //             self._rpc({
            //                 model: 'funenc.wechat.user',
            //                 method: 'get_user_tree',
            //                 kwargs: { department_id: id }
            //             }).then(function (data) {
            //                 return resolve(data);
            //             });
            //         }
            //     }
            // });
        },

        /**
         * 由于vue的template在xml中会报错，所以这里写在硬编码放这里
         */
        _render_tree_tempate: function () {
            var tree_box = this.$("#tree_box")
            $('<div id="' + this.tree_id + '">' +
                '    <el-tree :load="loadNode" lazy :props="defaultProps" @node-click="handleNodeClick" :expand-on-click-node="false">\n' +
                '    </el-tree>' +
                '</div>').appendTo(tree_box);
        }
    });

    return left_tree_controller;
});
