export default {
    data() {
        return {
            mode: this.$root.$widget.mode,
        }
    },
    computed: {
        $widget() {
            return this.$root.$widget;
        },
        $required(){
            return this.$root.$required
        },
        $filed_string(){
            return this.$widget.field.string
        },
        $widget_value(){
            return this.$widget.value.data;
        }

    },
    methods:{
        do_action(){
            return this.$widget.do_action.apply(this.$widget, arguments)
        },
        _rpc(){
             return this.$widget._rpc.apply(this.$widget, arguments)
        }
    }


}