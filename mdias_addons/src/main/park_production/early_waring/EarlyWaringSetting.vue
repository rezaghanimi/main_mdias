<template>
    <div class="container early-waring-content">
        <div class="panel panel-default" v-for="d in early_waring" :key="d.apply_tag">

            <div class="panel-body">
                <div class="panel-heading">
                    <span>{{d.name}}预警值设定</span>
                </div>

                <div v-for="setting in d.settings" :key="setting.id">
                    <early-waring-setting-line
                            :waring_name="d.name"
                            :setting="setting"
                    />
                </div>
            </div>
        </div>
    </div>

</template>

<script>
    import WidgetMixin from '../../../mixins/widget_mixin'
    import EarlyWaringSettingLine from './EarlyWaringSettingLine'

    export default {
        name: "EarlyWaringSetting",
        components: {EarlyWaringSettingLine},
        mixins: [WidgetMixin],
        computed: {},
        data() {
            return {
                early_waring: [
                    {
                        name: null,
                        apply_tag: null,
                        settings: []
                    }
                ],
                checked: {}
            }
        },
        mounted() {
            let self = this;
            this.$nextTick(() => {
                self.make_early_waring_data()
            });
        },
        methods: {
            make_early_waring_data() {
                let self = this;
                self.$widget._rpc({
                    model: 'metro_park_production.early_waring',
                    method: 'get_early_data'
                }).then(function (result) {
                    self.set_data(result)
                })
            },
            set_data(data) {
                this.early_waring = data;
            },
        },

        widget: {
            init() {
                this._super.apply(this, arguments);
            },
        },
    }
</script>

<style scoped>
    .early-waring-content {
        margin: 2rem;
        padding: 1rem;
        background: white;
        border-radius: .5rem;
    }

    .panel-body {
        margin-top: 2rem;
        background: #f0f0f0;
    }
    .panel-heading{
        font-family: "Helvetica Neue", Helvetica, "PingFang SC", 微软雅黑, Tahoma, Arial, sans-serif;
        padding: .5rem;
        font-weight: bold;
    }
    .panel-heading > span{
        color: #3b64ff;
    }
</style>