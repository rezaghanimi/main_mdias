<template>
    <div>
        <el-button size="mini" @click="playVideo" type="primary" icon="el-icon-view" round></el-button>
        <el-dialog
                :title='metadata.name'
                :visible.sync="dialogVisible"
                width="60%"
                v-if="dialogVisible"
                modal="false"
                :modal-append-to-body="true"
                :append-to-body="true"
                @close="closeDialog"
                custom-class="video-js-el-dialog"
                top="10"
        >
            <video
                    id="videoElement"
                    controls preload="auto"
                    class="video-js vjs-theme-city"
            >
            </video>
        </el-dialog>
    </div>
</template>

<script>

    import WidgetMixin from '../mixins/widget_mixin';

    export default {
        name: "VideoField",
        mixins: [WidgetMixin],
        data() {
            return {
                metadata: {},
                dialogVisible: false,
                value_data: [],
            }
        },
        mounted() {
            this.metadata = this.$widget.metadata;

        },
        methods: {
            playVideo(event) {
                event.stopPropagation();
                this.dialogVisible = true;
                this._play();
            },
            _play() {
                let self = this;
                setTimeout(function () {
                    self.initVideo([
                        {
                            src: self.metadata.url,
                            type: 'video/mp4',
                        }
                    ]);
                })

            },
            closeDialog() {
                this.videoPlayer.dispose();
            },
            initVideo: function (sources) {
                //初始化视频方法
                this.videoPlayer = this.$video('#videoElement', {
                    controls: true,
                    techOrder: ["html5", "flash"],
                    preload: 'auto',
                    autoplay: true,
                    fluid: true, // 自适应宽高
                    language: 'zh-CN', // 设置语言
                    muted: false, // 是否静音
                    inactivityTimeout: false,
                    controlBar: { // 设置控制条组件
                        'currentTimeDisplay': true,
                        'timeDivider': true,
                        'durationDisplay': true,
                        'remainingTimeDisplay': false,
                        volumePanel: {
                            inline: false,
                        },
                        /* 使用children的形式可以控制每一个控件的位置，以及显示与否 */
                        children: [
                            {name: 'playToggle'}, // 播放按钮
                            {name: 'currentTimeDisplay'}, // 当前已播放时间
                            {name: 'progressControl'}, // 播放进度条
                            {name: 'durationDisplay'}, // 总时间
                            { // 倍数播放
                                name: 'playbackRateMenuButton',
                                'playbackRates': [0.5, 1, 1.5, 2, 2.5]
                            },
                            {
                                name: 'volumePanel', // 音量控制
                                inline: false, // 不使用水平方式
                            },
                            {name: 'FullscreenToggle'} // 全屏
                        ]
                    },
                    sources: sources,
                }, function () {
                    console.log('视频就绪>>>');
                });
            }

        },
        widget: {
            fieldsToFetch: {
                name: {type: 'char'},
                datas_fname: {type: 'char'},
                mimetype: {type: 'char'},
            },

            supportedFieldTypes: ['many2many', 'many2one'],
            init() {

                let res = this._super.apply(this, arguments);
                this.metadata = {};
                return res
            },
            _generatedMetadata: function () {
                var self = this;
                self.metadata = {
                    url: self._getFileUrl(this.value.data.id),
                    name: this.value.data.display_name
                };
            },
            _getFileUrl: function (attachment_id) {
                return '/metro_park_production/video_stream?attachment_video_id=' + attachment_id;
            },
            _render: function () {
                this._generatedMetadata();
            }
        },
    }
</script>

<style >
    .video-js [aria-hidden="true"].vjs-icon-placeholder, [aria-hidden="1"].vjs-icon-placeholder, [aria-hidden="true"].vjs-slider-bar{
        display: block  !important;
    }
    .video-js-el-dialog{
        background: #0a0c0d;
        color: #ffffff;
    }
    .video-js-el-dialog .el-dialog__title{
        color: white;
    }
    .video-js-el-dialog .el-dialog__body{
        padding-top: 5px;
    }
</style>