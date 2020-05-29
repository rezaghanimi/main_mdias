<template>
    <div class="container-fluid vue-field-content">
        <span class="spanlh36" v-if="mode!=='edit'">
            {{value_description ? value_description: '无'}}</span>
        <div class="container-fluid vue-field-content" v-else>
            <div class="row">
                <div class="col-md-12">
                  <textarea
                      @focus="onTextFocus"
                      class="o_field_text o_field_widget o_input"
                      cols="30"
                      readonly="readonly"
                      rows="10"
                      style="height:80px"
                      v-model="value_description"></textarea>
                </div>
            </div>
            <div class="row" v-if="show_group_button">
                <div class="col-md-12">
                    <el-button-group>

                        <el-button @click="onOk" icon="el-icon-success" size="small" type="primary">
                            确认
                        </el-button>
                        <el-button @click="onClear" icon="el-icon-delete" size="small" type="primary">
                            清空
                        </el-button>
                    </el-button-group>
                </div>
            </div>

            <div class="row" v-for="v, k in line_names" v-if="show_group_button && group_box_station">

                <div class="col-md-12">
                    <el-divider></el-divider>
                    <div style="margin-left:.5rem;margin-top: .5rem">
                        <el-tag size="medium" type="info" effect="plain">{{v}}</el-tag>
                        <el-button style="margin-left: .5rem" icon="el-icon-plus" type="primary" @click="onAddSelect(k)"
                                   size="mini" circle></el-button>
                    </div>
                    <select-range-group v-model="range_checked[k]" @change="onRangeChange(arguments, k)">
                        <select-range v-for="key in add_selection[k]"
                                      ref="select_range"
                                      :key="key"
                                      :range_data="group_box_station[k]"
                                      :label="key"
                                      @delete_self="deleteRangeSelect(k, key)"
                        />
                    </select-range-group>
                    <el-checkbox-group v-model="check_data[k]">
                        <el-checkbox :key="value.id" :label="value.id" v-for="value in group_box_station[k]">
                            {{value.name}}
                        </el-checkbox>
                    </el-checkbox-group>
                </div>
            </div>
        </div>

    </div>
</template>
<script>
    import SelectMixin from '../components/mixins/SelectMixin'
    import SelectRangeGroup from '../components/SelectRangeGroup'
    import SelectRange from '../components/SelectRange'

    export default {
        components: {
            SelectRangeGroup, SelectRange
        },
        mixins: [SelectMixin],
        data() {
            return {
                lines: [],
                group_box_station: {},
                check_data: {},
                show_group_button: false,
                line_names: {},
                add_selection: {},
                range_checked: {},
                range_state_map: {}
            };
        },
        computed: {
            line_ids: function () {
                if (this.lines.length === 0)
                    return [];
                else {
                    let ids = [];
                    _.each(this.lines, (line) => {
                        ids.push(line.id)
                    });
                    return ids;
                }
            },
        },
        methods: {

            line_box_date() {
                let self = this;
                this.$widget._rpc({
                    model: 'train_station.train_station',
                    method: 'get_line_area',
                    kwargs: {
                        'line_ids': this.line_ids
                    }
                }).then(function (res) {
                    self.group_box_station = res;
                });

            },
            _load_line_data() {
                let self = this;
                this.$widget._rpc({
                    model: 'train_line.train_line',
                    method: 'search_read',
                    domain: [['id', 'in', this.line_ids]],
                    fields: ['id', 'name']
                }, {
                    shadow: true
                }).then((res) => {
                    let names = {}
                    _.each(res, (re) => {
                        names[re.id] = re.name
                    });
                    let set_key = (value, k, data) => {
                        if (value[k] === undefined) {
                            self.$set(value, k, data);
                        }

                    };
                    _.each(names, (v, k) => {
                        set_key(this.check_data, k, []);
                        set_key(this.range_checked, k, []);
                        set_key(this.add_selection, k, []);
                        set_key(this.range_state_map, k, {})
                    });
                    self.line_names = names;
                })
            },

            onTextFocus() {
                this.load_widget_lines();
                if (this.lines.length === 0) {
                    return
                }
                if (this.show_group_button === false) {
                    this.show_group_button = true;
                    this._load_line_data();
                    this.line_box_date();
                }

            },
            load_widget_lines() {
                this.lines = this.get_ref_field_id_name(this.$widget.attrs.options.line_ids)

            },
            compress_description(data) {
                if (data.length === 0) {
                    return
                }
                data = _.sortBy(data, 'index', 'asc');
                let description = '';
                for (let i = 0; i < data.length; i++) {
                    let d = data[i];
                    let start_name = d.name;
                    let index = d.index;
                    let end_name = null;
                    for (let j = i + 1; j < data.length; j++) {
                        let v = data[j];
                        if (index + 1 !== v.index || j=== data.length -1) {
                            if(j=== data.length -1){
                                end_name = data[j].name;
                                i = j;
                            }else {
                                end_name = data[j - 1].name;
                                i = j - 1
                            }
                            break
                        }
                        index++
                    }
                    if (!!end_name) {
                        if (start_name === end_name) {
                            description += start_name + ';'
                        } else {
                            description += start_name + '<----->' + end_name
                        }
                    } else {
                        description += start_name + ';'
                    }
                    description += ';'
                }
                return description
            },
            onOk() {
                this.show_group_button = false;
                this.value_data = this.check_data;
                let description = '';

                _.each(this.check_data, (v, k) => {
                    if (this.check_data[k].length === 0) return;
                    let data = [];
                    description += this.line_names[k] + ':';
                    _.each(this.check_data[k], (id) => {
                        let d = this.group_box_station[k].find((value) => {
                            return value.id === id
                        });
                        if (d === undefined) return;
                        data.push(d)
                    });
                    description += this.compress_description(data);
                    description += '\n'
                });
                this.value_description = description;
                this._clearRangeData();
                this._clearRangeSelect();
                this.commit()
            },

            onClear() {
                this.show_group_button = false;
                this.value_description = null;
                this.value_data = []
                _.each(this.check_data, (v, k) => {
                    this.check_data[k] = []
                });
                this._clearRangeData();
                this._clearRangeSelect();
            },
            onAddSelect(line_id) {

                let keys = _.sortBy(this.add_selection[line_id]);
                if (keys.length === 0) {
                    keys.push(1)
                } else {
                    let key = keys[keys.length - 1] + 1;
                    keys.push(key);

                    this.$set(this.range_state_map[line_id], keys.length, [])
                }
                this.add_selection = {};
                this.$set(this.add_selection, line_id, keys)
            },
            onRangeChange([value, label], line_id) {

                this.range_state_map[line_id][label] = value;
                this.update_checked();
            },
            deleteRangeSelect(line_id, key) {
                this.add_selection[line_id] = this.add_selection[line_id].filter((k) => {
                    return key !== k;
                });

                if (line_id in this.range_state_map) {
                    delete this.range_state_map[line_id][key]
                    this.update_checked();
                }

            },
            _clearRangeSelect() {
                _.each(this.add_selection, (v, k) => {
                    this.add_selection[k] = [];
                })
            },
            _clearRangeData() {
                _.each(this.range_checked, (v, k) => {
                    this.range_checked[k] = [];
                })

            },
            update_checked() {
                _.each(this.range_state_map, (line_check, k) => {
                    this.check_data[k] = [];
                    _.each(line_check, (v, key) => {
                        _.each(v, (id) => {
                            if (!this.check_data[k].includes(id)) {
                                this.check_data[k].push(id)
                            }
                        });

                    });

                });
            }
        },
        widget: {

            init: function (parent, options) {
                //this.vue 这里可以使用vue的实例

                return this._super.apply(this, arguments);
            },
            start: function () {
                return this._super.apply(this, arguments)
            },
        },

    };
</script>

<style>
    .vue-field-content {
        margin: 0;
        padding: 0;
    }
</style>


