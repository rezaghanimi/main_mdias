<template>
    <div class="container-fluid pdf-container-fluid">
        <el-row>
            <el-col :span="24">
                <div class="pdfContent" id="pdfContent">
                    <el-row justify="center" type="flex">
                        <el-col :span="24">
                            <div class="A4 page">
                                <el-row>
                                    <el-col :span="24" class="text-center">
                                        <h2>变电所（站）第二种工作票</h2>
                                    </el-col>
                                </el-row>
                                <el-row>
                                    <el-col :span="6" :offset="2">
                                        <h4>
                                            <p>

                                            </p>
                                        </h4>

                                    </el-col>
                                    <el-col :span="6" :offset="8">
                                        <h4>
                                            <p style="float: right ">
                                                <input v-model="data.s_year" style="width: 5rem"
                                                       class="inline-input years-month-input">年
                                                <input v-model="data.s_month"
                                                       class="inline-input years-month-input">月
                                                <input v-model="data.s_day"
                                                       class="inline-input years-month-input">日
                                            </p>
                                        </h4>
                                    </el-col>
                                </el-row>
                                <el-row justify="center">
                                    <el-col :offset="2" :span="8" class="text-left">
                                        <p style="float: left">
                                            <input class="inline-input" style="width: 15rem"
                                                   v-model="data.station">站（所）
                                        </p>

                                    </el-col>
                                    <el-col :span="6" class="text-left">
                                        <p>
                                            作业代码
                                            <input class="inline-input"
                                                   v-model="data.p_work_code || data.su_work_code">
                                        </p>
                                    </el-col>
                                    <el-col :span="6" class="text-left" :offset="2">
                                        <p style="float: left">
                                            第<input class="inline-input"
                                                    v-model="data.ticket_number">号
                                        </p>
                                    </el-col>
                                </el-row>
                                <el-row justify="center">
                                    <table class="table table-bordered pdfTable">
                                        <thead></thead>
                                        <tbody>
                                        <tr>
                                            <td colspan="2" rowspan="2">作业地点及内容</td>
                                            <td colspan="4" rowspan="2">{{data.address_and_content}}</td>
                                            <td colspan="1">发票人</td>
                                            <td colspan="1">{{data.reporter}}</td>
                                        </tr>
                                        <tr>
                                            <td colspan="1">发票日期</td>
                                            <td colspan="1">{{data.d_rec}}</td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">工作票有效期</td>
                                            <td colspan="6">{{data.ticket_work_time}}</td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">工作领导人</td>
                                            <td colspan="3">姓名：{{data.p_principal}}</td>
                                            <td colspan="3">安全等级：{{safe_key[data.p_principal_safety_code]}}</td>
                                        </tr>

                                        <tr>
                                            <td colspan="3" rowspan="3">作业组成员姓名及安全等级（安全等级填在括号内）</td>
                                            <td colspan="1" style="height: 2.5rem"><p>{{data.group_worker.group_worker1
                                                || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker2 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker3 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker4 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker5 || ''}}</p></td>
                                        </tr>
                                        <tr>
                                            <td colspan="1" style="height: 2.5rem"><p>{{data.group_worker.group_worker6
                                                || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker7 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker8 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker9 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker10 || ''}}</p></td>
                                        </tr>
                                        <tr>
                                            <td colspan="1" style="height: 2.5rem"><p>{{data.group_worker.group_worker11
                                                || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker12 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker13 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker14 || ''}}</p></td>
                                            <td colspan="1"><p>{{data.group_worker.group_worker15 || ''}}</p></td>
                                        </tr>

                                        <tr>
                                            <td colspan="8">
                                                <p>
                                                    工作条件（停电或不停电）：
                                                </p>
                                                <p>
                                                    <input v-model="data.work_conditions"
                                                           class="inline-input" style="width: 50rem">
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="4" style="height: 10rem" class="title-block">
                                                 <h5>必须采取的安全措施</h5>
                                                <div class="auto-text-content">

                                                    <pre><span>{{data.security_measures}}</span><br></pre>
                                                    <textarea v-model="data.security_measures"
                                                              style="position:absolute;top:0;left:0;height:100%;"
                                                              class="text-block"
                                                              disabled="readonly">
                                                    </textarea>
                                                </div>

                                            </td>
                                            <td colspan="4" class="title-block">
                                                <h5>已经完成的安全措施</h5>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="8">
                                                <el-row>
                                                    <el-col :span="24">
                                                        <p>已做好安全措施准予在
                                                            <input
                                                                class="inline-input years-month-input">年
                                                            <input
                                                                class="inline-input years-month-input">月
                                                            <input
                                                                class="inline-input years-month-input">日
                                                            <input
                                                                class="inline-input years-month-input">时
                                                            <input
                                                                class="inline-input years-month-input">分开始工作。
                                                        </p>

                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <p class="sign-block">值班员：
                                                        <input v-model="data.p_day"
                                                               class="inline-input">（签字）
                                                    </p>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="24">
                                                        <p>经检查安全措施已做好于
                                                            <input
                                                                class="inline-input years-month-input">年
                                                            <input
                                                                class="inline-input years-month-input">月
                                                            <input
                                                                class="inline-input years-month-input">日
                                                            <input
                                                                class="inline-input years-month-input">时
                                                            <input
                                                                class="inline-input years-month-input">分开始工作。
                                                        </p>

                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="8" :offset="16">
                                                        <p class="sign-block">工作领导人：
                                                            <input
                                                                class="inline-input">（签字）
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="24">
                                                        <p>变更作业组成员记录：
                                                            <input style="width: 40rem"
                                                                   class="inline-input">
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="8" :offset="16">
                                                        <p class="sign-block">发票人：
                                                            <input
                                                                class="inline-input">（签字）
                                                        </p>

                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="8" :offset="16">
                                                        <p class="sign-block">工作领导人：
                                                            <input
                                                                class="inline-input">（签字）
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="24">


                                                        <p>工作已于
                                                            <input
                                                                class="inline-input years-month-input">年
                                                            <input
                                                                class="inline-input years-month-input">月
                                                            <input
                                                                class="inline-input years-month-input">日
                                                            <input
                                                                class="inline-input years-month-input">时
                                                            <input
                                                                class="inline-input years-month-input">分结束。
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col>
                                                        <p class="sign-block">工作领导人：
                                                            <input
                                                                class="inline-input">（签字）
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col :span="24">
                                                        <p>工作业地点已清理就绪，工作票于
                                                            <input
                                                                class="inline-input years-month-input">年
                                                            <input
                                                                class="inline-input years-month-input">月
                                                            <input
                                                                class="inline-input years-month-input">日
                                                            <input
                                                                class="inline-input years-month-input">时
                                                            <input
                                                                class="inline-input years-month-input">分结束。
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                                <el-row>
                                                    <el-col>
                                                        <p class="sign-block">值班员:
                                                            <input
                                                                class="inline-input">（签字）
                                                        </p>
                                                    </el-col>
                                                </el-row>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </el-row>
                            </div>
                        </el-col>
                    </el-row>
                </div>
            </el-col>
        </el-row>
        <el-row justify="center">
            <el-col :span="6" :offset="12">
                <el-button icon="el-icon-printer" onclick="jQuery('#pdfContent').print()" type="primary">
                    打印
                </el-button>
            </el-col>
        </el-row>


    </div>

</template>

<script>
    /* eslint-disable */
    require('./jQuery.print.js');
    // Print substation_work_ticket
    export default {
        data() {
            return {
                safe_key: {
                    'grade1': '1级',
                    'grade2': '2级',
                    'grade3': '3级',
                    'grade4': '4级',
                    'grade5': '5级',

                },
                data: {
                    s_year: '',
                    s_mon: '',
                    s_day: '',
                    station: '',
                    p_work_code: '',
                    su_work_code: '',
                    id: '',
                    address_and_content: '',
                    reporter: '',
                    d_rec: '',
                    ticket_work_time: '',
                    p_principal: '',
                    p_principal_safety_code: '',
                    group_worker: {},
                    work_conditions: ''
                }
            };
        },

        mounted() {

            this.$nextTick(() => {
                if (this.$root.$widget) {
                    if (this.$root.$widget.options.context.data_str) {
                        this.data = JSON.parse(
                            this.$root.$widget.options.context.data_str
                        )[0];
                        console.log(JSON.stringify(this.data, 0, 2));
                    }
                    this.data.s_year = this.$root.$widget.options.context.s_year;
                    this.data.s_month = this.$root.$widget.options.context.s_month;
                    this.data.s_day = this.$root.$widget.options.context.s_day;
                    this.data.station = this.$root.$widget.options.context.station;
                    this.data.reporter = this.$root.$widget.options.context.reporter;
                    this.data.d_rec = this.$root.$widget.options.context.d_rec;
                    this.data.p_principal = this.$root.$widget.options.context.p_principal;
                    this.data.group_worker = this.$root.$widget.options.context.group_worker;
                    this.data.security_measures = this.$root.$widget.options.context.security_measures;
                }
            });
        },
        methods: {},
        name: 'SubstationSecondWorkTicket'
    };
</script>

<style lang="less" scoped>
    .A4 {
        background: white;
        height: 100rem;
        page-break-before: always;
        width: 73rem;
        padding: 3rem;
        margin: auto;
        font-size: 1rem;
    }

    .pdf-container-fluid {
        padding: 0;
        margin: auto;
    }

    .inline-input {
        border-left-width: 0;
        border-top-width: 0;
        border-right-width: 0;
        border-bottom-color: black;
        text-align: center;
        width: 8rem;
        background-color: transparent

    }

    .pdfTable {
        table-layout: fixed;
        word-break: break-all;
        border-collapse: collapse;
        margin: 0 auto;
        text-align: center;
        font-size: 1.2rem;
    }

    .pdfTable {
        height: 70rem;
        border: 2px solid black;
        width: 60rem;

    }

    .pdfTable td {
        border: 1.5px solid black !important;
    }

    .pdfTable p {
        text-align: left;
        margin: 0;
    }

    .pdfContent {
        width: 100%;
        margin: auto;
    }


    @page {
        size: auto;
        margin: 0mm;
    }

    .sign-block {
        float: right;
    }

    .years-month-input {
        width: 2rem;
    }

    .sign-content .el-row {
        margin-bottom: 1.2rem;
    }

    .pdfContent {
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
        user-input: none;
        user-focus-key: none;

    }

    .pdfContent input {
        pointer-events: none;
    }

    .pdfContent td {
        vertical-align: middle;
        text-align: center;
    }

    .title-block {
        vertical-align: top !important;
        text-align: left !important;

    }

    .text-block {
        height: 25rem;
        border: 0;
        overflow: hidden;
        resize: none;
        background: none;
    }

     .auto-text-content {
        position: relative;
    }

    pre {
        display: block;
        visibility: hidden;
    }

</style>