import { vueWidgetRegister } from '../base/__init_';
import AttachmentListField from './AttachmentListField'

import 'froala-editor/js/froala_editor.pkgd.min.js';
import 'froala-editor/css/froala_editor.pkgd.min.css';
import 'froala-editor/css/froala_style.min.css';
import 'froala-editor/js/languages/zh_cn';
import 'froala-editor/js/plugins.pkgd.min.js';
import Video from 'video.js'
import Vue from "vue/dist/vue.esm.js";
import VueFroala from 'vue-froala-wysiwyg'
Vue.use(VueFroala);


import FroalaTableEditor from './FroalaTableEditor';
import ColorPicker from './ColorPicker'
import VideoField from './VideoField'

vueWidgetRegister.fieldRegister('AttachmentListField', AttachmentListField);

vueWidgetRegister.fieldRegister('FroalaTableEditor', FroalaTableEditor);
vueWidgetRegister.fieldRegister('ColorPicker', ColorPicker);
vueWidgetRegister.fieldRegister('VideoField', VideoField);
