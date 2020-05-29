
const path = require("path");
module.exports = {
    mode: "development",
    entry: [
        // left tee
        "./left_tree_list/funenc_left_tree_list_controller.js",
        "./left_tree_list/funenc_left_tree_list_render.js",
        "./left_tree_list/funenc_left_tree_list.js",
        // log_tree
        "./log_tree/funenc_log_tree_controller.js",
        "./log_tree/funenc_log_tree_render.js",
        "./log_tree/funenc_log_tree.js",
        // table
        "./table/funenc_table_controller.js",
        "./table/funenc_table_edittable_render.js",
        "./table/funenc_table_render.js",
        "./table/funenc_table.js",
        // tree_grid
        "./table/funenc_tree_grid_controller.js",
        "./table/funenc_tree_grid_render.js",
        "./table/funenc_tree_grid.js",
        // all others
        "./fuennc_control_pannel.js",
        "./funenc_abstract_controller.js",
        "./funenc_abstract_view.js",
    ],
    output: {
        path: path.resolve(__dirname, "./"),
        filename: "funenc_framwork.js"
    }
}