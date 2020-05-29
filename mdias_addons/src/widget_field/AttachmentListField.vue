<template>
    <div>
        <div>
            <el-button size="mini" type="text" @click.stop="openDialog">{{display_name}}</el-button>

            <el-dialog
                    title="附件"
                    :visible.sync="dialogVisible"
                    :modal-append-to-body="true"
                    :append-to-body="true"
                    width="60%"
            >
                <el-table
                        :data="value_data"
                        style="width: 100%"
                        border
                        height="32rem"
                        width="100%"
                >
                    <el-table-column label="文件名" prop="data">
                        <template slot-scope="scope">
                            <span>{{scope.row.data.name || scope.row.data.filename}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="下载" prop="id">
                        <template slot-scope="scope">
                            <a :href="metadata[scope.row.id].url">
                                下载
                            </a>
                        </template>
                    </el-table-column>
                </el-table>
            </el-dialog>
        </div>

    </div>


</template>

<script>
    import WidgetMixin from '../mixins/widget_mixin'

    export default {
        name: "AttachmentListField",
        mixins: [WidgetMixin],
        computed: {
            display_name() {
                return this.$widget.nodeOptions.button_name || '下载'
            }
        },
        data() {
            return {
                metadata: {},
                dialogVisible: false,
                value_data: [],
            }
        },
        mounted() {
            this.metadata = this.$widget.metadata;

        },
        methods: {
            openDialog(event) {
                event.stopPropagation();
                this.value_data = this.$widget.value.data
                this.dialogVisible = true
            }

        },
        widget: {
            fieldsToFetch: {
                name: {type: 'char'},
                datas_fname: {type: 'char'},
                mimetype: {type: 'char'},
            },

            supportedFieldTypes: ['many2many', 'many2one'],
            init() {

                let res = this._super.apply(this, arguments);
                if (this.field.type !== 'many2many' || this.field.relation !== 'ir.attachment') {
                    var msg = "The type of the field '%s' must be a many2many field with a relation to 'ir.attachment' model.";
                    throw _.str.sprintf(msg, this.field.string);
                }
                this.metadata = {};
                return res
            },
            _generatedMetadata: function () {
                var self = this;
                _.each(this.value.data, function (record) {
                    self.metadata[record.id] = {
                        url: self._getFileUrl(record.data),
                        name: record.name
                    };
                });
            },
            _getFileUrl: function (attachment) {
                return '/web/content/' + attachment.id + '?download=true';
            },
            _render: function () {
                this._generatedMetadata();
            }
        },
    }
</script>

<style scoped>

</style>