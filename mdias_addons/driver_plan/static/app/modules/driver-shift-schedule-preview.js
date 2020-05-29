layui.use(['element', 'jquery', 'laytpl', 'api'], function () {
    const element = layui.element;
    const $ = layui.$; //重点处
    const laytpl = layui.laytpl;
    const api = layui.api;
    $('#loadData').click(function () {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '数据加载中...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '100px',
                    'text-align': 'center',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        $.ajax({
            type: api.schedule.findScheduleTableDetailById.type,
            url: api.base_url + api.schedule.findScheduleTableDetailById.url + '/' + localStorage.getItem("previewScheduleId"),
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    const data = response.data;
                    renderDriverSchedule(data);
                    renderAbsentDriverSchedule(data.absentDrivers);
                }
            },
            error: function (response) {

            }
        })
    });

    /**
     * 根据司机信息渲染界面
     */
    function renderDriverSchedule(data) {
        const getTpl = document.getElementById('scheduleClassTemplate').innerHTML;
        const view = document.getElementById("templateContainer");
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     * 根据司机信息渲染请假人员名单
     */
    function renderAbsentDriverSchedule(data) {
        const getTpl = document.getElementById('absentDriverTemplate').innerHTML;
        const view = document.getElementById("absentDriverContainer");
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     *返回按钮点击事件
     */
    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule.html");
    });
});
