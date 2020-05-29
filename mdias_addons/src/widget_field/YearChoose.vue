<script>

    import WidgetMixin from '../mixins/widget_mixin'

    export default {
        mixins: [WidgetMixin],
        data() {
            return {
                value1: '',
                dis: 'false',
            };
        },

        mounted(){
            if (this.$widget.value) {
                this.value1 = 'Sun Jan 01 ' + this.$widget.value.split('年')[0] + ' 00:00:00 GMT+0800';
            }
        },
        methods: {
            handleChange(value) {
                let rec = String(value).split('01 ')[1].split(' 00')[0] + '年'
                this.$widget._setValue(rec)
            }
        },

        widget: {
            init: function (parent, options) {
                return this._super.apply(this, arguments);
            },
            start: function () {
                return this._super.apply(this, arguments);
            }
        }
    };
</script>

<template>
    <div class="block" id="date_time">
        <el-date-picker
                v-model="value1"
                type="year"
                placeholder="选择年"
                @change="handleChange"
                :disabled="dis === 'true'"
        >
        </el-date-picker>
    </div>
</template>