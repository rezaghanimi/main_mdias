<template>
    <div class='container-fluid'>
        <div class="row" style="margin-top: 2rem">
            <div class="col-md-8" style="margin-bottom: 2rem">
                <div class="el-button-group">
                    <el-button type="primary" @click="openEarlySetting" size="mini">设定预警阀值</el-button>
                    <el-button type="primary" @click="openEarlyNotifySetting" size="mini">预警提醒配置</el-button>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <h3>
                    车辆生产指标预警
                </h3>
            </div>
        </div>
        <div class="row" v-for="ty in line_types">
            <early-waring-info-line :data_type="ty"></early-waring-info-line>
        </div>
    </div>
</template>

<script>
    import WidgetMixin from '../../../mixins/widget_mixin'
    import EarlyWaringInfoLine from './EarlyWaringInfoLine'

    export default {
        name: "EarlyWaringPage",
        mixins: [WidgetMixin],
        components: {EarlyWaringInfoLine},
        data() {
            return {
                line_types: [
                    'train_maintain',
                    'train_run_start',
                    'train_run_finished',
                    'construction'
                ]
            }
        },
        methods: {
            openEarlySetting() {
                this.do_action({
                    type: 'ir.actions.client',
                    name: '预警阀值设置',
                    tag: 'EarlySetting',
                    target: 'new'
                })
            },
            openEarlyNotifySetting() {
                let self = this;
                this._rpc({
                    'model': 'res.config.settings',
                    'method': 'early_waring_notify_action'
                }).then(function (action) {
                    self.do_action(action)
                });
            }

        }

    }
</script>

<style scoped>
    .container-fluid {
        margin-top: 1rem;
    }

</style>