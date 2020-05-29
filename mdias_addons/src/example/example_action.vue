<template>

</template>

<script>
    export default {
        name: "example_action",
        data() {
            return {
                value: null,
            }
        },
        computed: {
        $widget() {
            return this.$root.$widget;

            },
        $require(){
            return this.$root.$required;
            }
        },
        methods:{
          test_require(){
              let web = this.$require('web.client')
          }
        },

        widget: {

            init: function (parent, options) {
                //this.vue 这里可以使用vue的实例

                return this._super.apply(this, arguments);
            },
            start: function () {
                return this._super.apply(this, arguments)
            }
        },
    }
</script>

<style scoped>

</style>