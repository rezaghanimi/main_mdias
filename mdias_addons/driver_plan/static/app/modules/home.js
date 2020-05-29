layui.use(['element', 'jquery', 'layer'], function () {
    const element = layui.element;
    const $ = layui.$;
    setInterval(
        timer, 1000
    );

    function timer() {
        $('.time-container').text(dateFns.format(new Date(), 'YYYY年MM月DD日 HH:mm:ss'))
    }

    $('#marquee-container').marquee({
        //speed in milliseconds of the marquee
        duration: 15000,
        //gap in pixels between the tickers
        gap: 10,
        //time in milliseconds before the marquee will start animating
        delayBeforeStart: 500,
        //'left' or 'right'
        direction: 'left',
        pauseOnHover: false,
        //true or false - should the marquee be duplicated to show an effect of continues flow
        duplicated: true
    });
    $('#fullScreen').click(function () {
        if (screenfull.enabled) {
            screenfull.request();
        } else {
            layer.msg('浏览器禁止全屏', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
        }
    });
    $('#home_button').click(function () {
        localStorage.setItem("previewScheduleId", $(this).attr("value"));
        $("#layui-content-body").load("modules/driver-shift-schedule-preview.html", function () {
            setTimeout(() => {
                $('#loadData').click();
            }, 100);
        });
    });
});
