<template>

    <div class="early-waring-content">
        <div class="all-content">
            <div class="color-picker-select">
                <el-color-picker v-model="setting.all_color" size="mini" class="color-picker"></el-color-picker>
            </div>

            <div class="waring-text">
                {{waring_name}}总体完成率低于
            </div>

            <div class="percentage-input-content">
                <el-input v-model="setting.all_threshold_value_percentage" size="mini" type="number"
                          class="input-width"></el-input>
                <strong>%</strong>
            </div>
            <div class="waring-text">
                为{{setting.waring_line_name}}
            </div>
            <div class="switch">
                <el-switch
                        v-model="setting.all_open"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                </el-switch>
            </div>
        </div>
        <div class="single-content">
            <div class="color-picker-select">
                <el-color-picker v-model="setting.single_color" size="mini" class="color-picker"></el-color-picker>
            </div>
            <div class="waring-text">
                {{waring_name}}单个完成率低于
            </div>
            <div class="percentage-input-content">
                <el-input v-model="setting.single_threshold_value_percentage" type="number"
                          class="input-width" size="mini"></el-input>
                <strong>%</strong>
            </div>

            <div class="waring-text">
                为{{setting.waring_line_name}}
            </div>
            <div class="switch">
                <el-switch
                        v-model="setting.single_open"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                </el-switch>
            </div>
        </div>
    </div>
</template>

<script>
   import WidgetMixin from '../../../mixins/widget_mixin'

    export default {
        name: "EarlyWaringSettingLine",
        mixins: [WidgetMixin],
        props: {
            setting: {
                type: Object,
                default() {
                    return {
                        id: -1,
                        waring_line_name: false,
                        single_open: false,
                        all_open: false,
                        single_threshold_value_percentage: 0,
                        all_threshold_value_percentage: false,
                        single_color: null,
                        all_color: null
                    }
                }
            },
            waring_name: {}
        },
        computed: {},
        data() {
            return {
                setting_data: {
                    id: -1,
                    waring_line_name: false,
                    single_open: false,
                    all_open: false,
                    single_threshold_value_percentage: false,
                    all_threshold_value_percentage: false,
                    single_color: null,
                    all_color: null
                }

            }
        },
        methods: {
            write_line(values){
                this.$widget._rpc({
                    'model': 'metro_park_production.early_waring.line',
                    'method': 'write',
                    'args': [values.id, {
                        'all_color': values.all_color,
                        'single_open': values.single_open,
                        'all_open': values.all_open,
                        'single_threshold_value_percentage': values.single_threshold_value_percentage,
                        'all_threshold_value_percentage': values.all_threshold_value_percentage,
                        'single_color': values.single_color,
                    }]
                })
            }

        },
        watch: {
            setting: {
                immediate: true,
                deep: true,
                handler(val) {
                    this.write_line(val)
                }
            }
        },
    }
</script>

<style scoped>
    .input-width {
        width: 6rem;
        height: 3rem;
        font-family: "Helvetica Neue", Helvetica, "PingFang SC", 微软雅黑, Tahoma, Arial, sans-serif;
    }

    .single-content {
        margin-left: 4rem;
    }

    .all-content div, .single-content div {
        margin: 0;
        display: flex;
        justify-content: end;

    }

    .early-waring-content {
        margin: 0;
        height: 5rem;
    }

    .early-waring-content div {
        display: flex;
        align-items: center;
        vertical-align: center;
        padding: auto;
        background: none;
        margin-left: .5rem;
    }

    .single-content {
        margin-left: 6rem !important;
    }

    .color-picker {
        border-radius: .5rem;
        margin: 50%;
    }

</style>