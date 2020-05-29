import Vue from "vue/dist/vue.esm.js";
const EL_INDEX = 0;

export var VueMixin = {
    vue_component: null,
    root_path: '../components/',
    vue: null,
    _bind_vue: function ($el, widget, require) {
        if (this.vue_component === null) {
            error('Vue component nos is null')
        }
        $el.append("<div/>")
        let self = this;
        let def = Vue.nextTick(function () {
            let vue_component = self.vue_component;
            vue_component.$widget = widget;
            let instance = new Vue({
                render: h => h(vue_component),
                beforeCreate: function () {
                    this.$widget = widget;
                    this.$required = require;
                }
            }).$mount($el.children('div').get(EL_INDEX));
            self.vue = instance;
            return instance;
        });
        Vue.config.productionTip = false;
        return def

    },

    destroy() {
        if (this.vue) {
            try {
                this.vue.$destroy();
            } catch (e) {
            }
        }
    }

};
