<template>
    <div class="fr-fullscreen-wrapper" style="top: 0;position:fixed;left:0;right: 0;height:100%">
        <Swiper v-if="pages.length > 0" :interval="10000" :showIndicator="false">
            <Slide v-for="(page,index) in pages" :key="index">
                <div class="fr-box fr-ltr fr-basic fr-top" role="application" style="z-index: 99999;">
                    <div class="fr-wrapper" dir="ltr" style="height: 600rem; overflow: hidden;border: 0">
                        <div :style="{height: '100%',background: backgroud}" class="fr-element fr-view" dir="ltr"
                             contenteditable="true"
                             aria-disabled="false" spellcheck="true" v-html="page.html_value">
                        </div>
                    </div>
                </div>
            </Slide>
        </Swiper>
    </div>
</template>

<script>
    import {Slide, Swiper} from 'vue-swiper-component';
    import widget_mixin from '../mixins/widget_mixin'

    export default {
        components: {
            Swiper,
            Slide
        },
        mixins: [widget_mixin],
        data() {
            return {
                pages: [],
                background: null,
            }
        },
        methods: {
            GetQueryString(name) {
                var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
                var r = window.location.search.substr(1).match(reg);
                if (r !== null) return unescape(r[2]);
                return null;
            },
            request_data() {
                let id = this.GetQueryString('mid');
                let self = this;
                this._rpc({
                    model: 'metro_park_production.screen',
                    method: 'request_data',
                    args: [id]
                }).then(function (value) {
                    console.log(value)
                    self.pages = value.pages;
                    self.backgroud = value.background;
                })
            }

        },
        mounted() {
            this.request_data();
            document.title = '大屏表单'
        },
        name: "ScreenLaunch",
    }
</script>

<style scoped>

</style>