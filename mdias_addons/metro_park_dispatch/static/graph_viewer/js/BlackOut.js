
BlackOut = function (editorUI, parkMap) {
    mxEventSource.call(this);

    this.parkMap = parkMap
    this.editorUI = editorUI

    this.initListener();
};

mxUtils.extend(BlackOut, mxEventSource);

/**
 * 初始化事件监听
 */
BlackOut.prototype.initListener = function () {
    var self = this
    console.log('install blockout listener!')
    this.parkMap.addListener('show_block', function (evt) {
        self.ShowBlockout()
    })

    this.parkMap.addListener('hide_block', function (evt) {
        self.HideBlockout()
    })
}

BlackOut.prototype.ShowBlockout = function () {
    this.parkMap.sysBlackout = true
    if (!document.querySelector('#blackout_grays')) {
        $('head').append($(`<style id='blackout_grays'>
            .geDiagramContainer {
                filter: grayscale(100%);
                -webkit-filter: grayscale(100%);
                -moz-filter: grayscale(100%);
                -ms-filter: grayscale(100%);
                -o-filter: grayscale(100%);
                filter: progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);
                -webkit-filter: grayscale(1)}</style>`))
    }
}

BlackOut.prototype.HideBlockout = function () {
    this.parkMap.sysBlackout = false
    $('#blackout_grays').remove()
}