<template>
    <div class="line-content col">
        <div style="width: 280px;">
            <div style="height: 290px;" class="card">
                <div slot="header" class="clearfix text-center">
                    <span>{{train_info[0]}}{{train_info[1]}}</span>
                </div>
                <div style="text-align: center" class="progress-content">
                    <el-progress :stroke-width="14" type="circle"
                                 :color="all_customColor"
                                 :percentage="total_plan_num && (finished_plan_num/total_plan_num).toFixed(2)*100"></el-progress>
                </div>
                <div style="text-align: center;">
                    <div><strong>综合{{train_info[1]}}</strong></div>
                    <div>完成/总任务数</div>
                    <div>{{finished_plan_num}}/{{total_plan_num}}</div>
                </div>
            </div>
        </div>
        <div style="padding-left: 20px; flex-grow: 1;">
            <div style="height: 290px;" class="card">
                <div slot="header" class="clearfix">
                    <div style="display: flex; align-items: center; margin: -3px 0;">
                        <div><strong>选择日期:</strong></div>
                        <el-date-picker size='mini' v-model="date_range" type="daterange" align="right" unlink-panels
                                        range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"
                                        :picker-options="date_pickerOptions">
                        </el-date-picker>
                        <div style="position: absolute; right: 30px; font-size: 14px; color: seagreen;cursor: pointer;">
                            <el-button @click="open_view" type="text">查看更多</el-button>

                        </div>
                    </div>
                </div>
                <div style="text-align: left;">
                    <div v-for='task in tasks'
                         style="display: flex; align-items: center; font-size: 14px; margin-bottom: 10px;margin-top: 5px ">
                        <div style="width: 130px;">{{task.train_name}}{{train_info[0]}}</div>
                        <div style="flex-grow: 1;">
                            <el-progress :stroke-width="10"
                                         :color="task.single_customColor"
                                         :percentage="task.total_num && (task.finished_num/task.total_num * 100).toFixed(2)"></el-progress>
                        </div>

                    </div>
                    <div style="text-align: center;bottom: 1rem;position: absolute;align-self: center;width: 100%">
                        <el-pagination :page-size='limit' :current-page="current_page"
                                       layout="prev, pager, next, jumper"
                                       :pager-count="6"
                                       @current-change="handleCurrentChange"
                                       :total="page_count">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import WidgetMixin from '../../../mixins/widget_mixin'

    export default {
        mixins: [WidgetMixin],
        name: "EarlyWaringInfoLine",
        props: {
            data_type: {
                default: String
            }
        },
        data() {
            return {
                date_pickerOptions: {
                    shortcuts: [{
                        text: '最近一周',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近一个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                            picker.$emit('pick', [start, end]);
                        }
                    }, {
                        text: '最近三个月',
                        onClick(picker) {
                            const end = new Date();
                            const start = new Date();
                            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
                            picker.$emit('pick', [start, end]);
                        }
                    }]
                },
                date_range: [],
                total_plan_num: 100,
                finished_plan_num: 100,
                train_info: ['车辆检修', '完成率'],
                tasks: [
                    {
                        train_name: '10000',
                        total_num: 100,
                        finished_num: 100,
                        single_customColor: "#409eff",
                    }
                ],
                view_id: null,
                add_ratio: 100,
                page_count: 100,
                limit: 5,
                current_page: 1,
                action_domain: null,
                model: null,
                all_customColor: "#409eff",
            }
        },
        mounted() {
            this.date_range = this.get_near_day();
            this.load_overall_info();
            this.load_task_data();
        },
        computed: {
            parameter() {
                const {date_range, current_page} = this;
                return {
                    date_range,
                    current_page
                }
            }
        },
        methods: {
            handleCurrentChange(data) {
                this.current_page = data
                this.load_task_data
            },
            color_change() {

            },
            load_task_data() {
                let self = this;
                let offset = this.limit * (this.current_page - 1);
                this._rpc({
                    'model': 'metro_park_production.early_waring_info',
                    'method': 'request_early_waring_task_info',
                    'args': [self.data_type, self.date_range[0], self.date_range[1]],
                    'kwargs': {'offset': offset, 'limit': self.limit}
                }).then((res) => {
                    console.log(res)
                    if (res) {
                        this.tasks = res
                    }
                })
            },
            load_overall_info() {
                let self = this;
                this._rpc({
                    'model': 'metro_park_production.early_waring_info',
                    'method': 'get_overall_info',
                    'args': [self.data_type, self.date_range[0], self.date_range[1]],
                }).then((res) => {
                    if (res) {
                        self.total_plan_num = res.sum_num;
                        self.finished_plan_num = res.finished_num;
                        self.model = res.model;
                        self.action_domain = res.action_domain;
                        self.view_id = res.view_id;
                        self.train_info = res.train_info;
                        self.all_customColor = res.all_customColor;
                        self.page_count = res.page_count;
                    }
                })
            },
            get_near_day() {
                const end = new Date();
                const start = new Date();
                start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
                return [start, end];
            },
            open_view() {
                this.do_action({
                    'type': 'ir.actions.act_window',
                    'res_model': this.model,
                    'view_id': this.view_id,
                    'domain': this.action_domain,
                    'target': 'new',
                    'views': [[false, 'list'], [false, 'form']],
                })
            }
        },
        watch: {
            parameter() {
                this.load_task_data()
                this.load_overall_info()
                this.color_change()
            },
        }
    }
</script>

<style scoped>
    .line-content {
        display: flex;
        padding-bottom: 10px;
    }

    .progress-content {
        margin: auto;
    }

</style>