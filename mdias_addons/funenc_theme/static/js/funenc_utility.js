odoo.define("funenc.utility", function (require) {
    "use strict";

    //全屏
    function fullScreen() {
        var ele = document.documentElement
            , reqFullScreen = ele.requestFullScreen || ele.webkitRequestFullScreen
                || ele.mozRequestFullScreen || ele.msRequestFullscreen;
        if (typeof reqFullScreen !== 'undefined' && reqFullScreen) {
            reqFullScreen.call(ele);
        };
    }

    //退出全屏
    function exitScreen() {
        var ele = document.documentElement
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
    }

    return {
        fullScreen: fullScreen,
        exitScreen: exitScreen
    }
})
