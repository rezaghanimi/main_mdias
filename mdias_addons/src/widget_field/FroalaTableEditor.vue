<template>
    <div class="froala-field">
        <froala v-model="value" :tag="'textarea'" :config="config">
        </froala>
    </div>
</template>

<script>

    import widget_mixin from '../mixins/widget_mixin'

    export default {
        name: 'FroalaEditorField',
        mixins: [widget_mixin],
        data() {
            let self = this;
            let mode = self.$root.$widget.mode;
            let config = {
                language: "zh_cn",
                zIndex: 99999,
                events: {
                    'initialized': function () {
                        if (mode !== 'edit') {
                            this.edit.off()
                        }
                        this.html.set(self.$widget.value);
                    }
                }
            };

            if (mode === 'edit') {
                _.extend(config, {
                    heightMin: 600,
                    height: 720,
                    toolbarSticky: true
                })
            }
            if (mode === 'readonly') {
                _.extend(config, {
                    toolbarButtons: [],
                    toolbarSticky: false,
                    toolbarBottom: false
                })
            }
            return {
                config: config,
                value: null,
            }
        },
        watch: {
            value(value) {
                this.$widget._setValue(value)
            }
        },
        widget: {
            supportedFieldTypes: ['html'],
        }
    }
</script>

<style>
    .froala-field {
        margin-top: 2rem;
    }

    .fr-dropdown-wrapper {
        min-height: 10rem;
    }

    .modal-dialog.modal-lg.fr-fullscreen-wrapper {
        max-width: 100%;
    }

    .fr-wrapper > div[style*='z-index:9999;width:100%;position:relative'] {
        position: absolute;
        top: -10000px;
        opacity: 0;
    }

    .fr-box.fr-basic .fr-element {
        margin-top: -1rem;
    }

    .second-toolbar #logo {
        display: none;
    }
</style>
