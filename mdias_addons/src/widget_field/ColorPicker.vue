<template>
    <div class="block">
        <el-color-picker v-model="color" :disabled="$widget.mode === 'readonly'"></el-color-picker>
    </div>
</template>

<script>
    import widget_mixin from '../mixins/widget_mixin'

    export default {
        name: "ColorPicker",
        mixins: [widget_mixin],
        data() {
            return {
                color: null,
            }
        },
        watch: {
            color(value) {
                this.$widget._setValue(value)
            }
        },
        mounted() {
            this.color = this.$widget.value;
        }
    }
</script>

<style scoped>

</style>