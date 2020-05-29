<template>

        <el-main style="padding: 0;margin: 0;border: 0;height: 100%;width: 100%">
            <el-row>
                <el-col span="8">
                    <e-chat id="chat-dispatch-train" style="width: 100rem;height: 60rem" :options="dispatchTrainNumOptions"/>
                </el-col>
                <!--            <el-col span="8">-->
                <!--                <e-chat id="chat-train-production"/>-->
                <!--            </el-col>-->
                <!--            <el-col span="8">-->
                <!--                <e-chat id="chat-construction-findished"/>-->
                <!--            </el-col>-->
            </el-row>
            <!--        <el-row>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-distribution"/>-->
            <!--            </el-col>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-department"/>-->
            <!--            </el-col>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-department1"/>-->
            <!--            </el-col>-->
            <!--        </el-row>-->
            <!--        <el-row>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-department2"/>-->
            <!--            </el-col>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-department3"/>-->
            <!--            </el-col>-->
            <!--            <el-col span="8">-->
            <!--                <e-chat id="chat-construction-department4"/>-->
            <!--            </el-col>-->
            <!--        </el-row>-->
        </el-main>
</template>

<script>
    import ECharts from "vue-echarts/components/ECharts";
    import "echarts/theme/macarons.js";
    import "echarts/lib/chart/bar";
    import chatConfig from './bi_echat_config'

    console.log(chatConfig)
    export default {
        name: "BI",
        components: {
            'e-chat': ECharts
        },
        data() {
            return {
                dispatchTrainNumOptions: chatConfig.dispatchTrainNum
            }
        }
    }
</script>

<style scoped>

</style>