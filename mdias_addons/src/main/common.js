import Vue from "vue/dist/vue.esm.js";
import moment from "moment";
import ElementUI from "element-ui";
Vue.prototype.$video = Video
require('video.js/dist/video-js.css')
require("element-ui/lib/theme-chalk/index.css");
require('../widget_field/main');
require('../widget_action/main');



import VueFroala from 'vue-froala-wysiwyg'
import Video from "video.js";
Vue.use(ElementUI);
Vue.use(VueFroala);
Vue.config.productionTip = false;
Vue.prototype.$moment = moment;

