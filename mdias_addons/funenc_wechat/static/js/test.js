
/**
 * Created by artorias on 2019/3/5.
 */
odoo.define('user_tree_js', function (require) {
    'use strict';

    var ListView = require("web.ListView");
    var view_registry = require("web.view_registry");
    var ListRenderer = require("funenc.left_tree_render");
    var ListController = require("funenc.left_tree_controller");

    var user_tree_controller = ListController.extend({
        on_attach_callback: function () {
            var self = this;
            this.app = new Vue({
                el: "#" + this.tree_id,
                data() {
                    return {
                        defaultProps: {
                            children: "sub",
                            label: "name",
                            id: "id",
                            isLeaf: 'leaf'
                        }
                    };
                },

                methods: {
                    handleNodeClick(data) {
                        self._rpc({
                            model: 'funenc.wechat.department',
                            method: 'get_children_dep_ids',
                            args: [data.id]
                        }).then(function (ids) {
                            self.trigger_up("search", {
                                domains: [[["department_ids", "in", ids]]],
                            });
                        })
                    },

                    loadNode(node, resolve) {
                        var id = (node.data && node.data.id) || null;
                        self._rpc({
                            model: 'funenc.wechat.department',
                            method: 'get_sub_departments_info',
                            kwargs: { department_id: id }
                        }).then(function (data) {
                            return resolve(data);
                        });
                    }
                }
            });
        },
    });

    var left_department_user_tree = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Renderer: ListRenderer,
            Controller: user_tree_controller
        }),
        viewType: "list"
    });

    view_registry.add("left_department_user_tree", left_department_user_tree);
});