layui.use(['element', 'jquery', 'api', 'layer', 'table', 'laytpl', 'form', 'laydate'], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const table = layui.table;
    const laytpl = layui.laytpl;
    const form = layui.form;
    const laydate = layui.laydate;
    loadAllDriverScheduleTable();
    let originData = {};
    let lastFocused;
    setTimeout(() => {
        laydate.render({
            elem: '#date'
            , type: 'date'
            , btns: ['now', 'confirm']
        });
        form.render();
    }, 1);
    // 设置事故事件表格
    const scheduleDirectiveTable = table.render({
        title: '计划下达反馈列表',
        id: 'schedule-directive-table',
        elem: '#schedule-directive-table',
        url: api.base_url + api.schedule_distribute.findPage.url,
        method: api.schedule_distribute.findPage.type,
        contentType: 'application/json',
        height: 'full-120',
        defaultToolbar: [],
        text: {
            none: '暂无相关数据'
        },
        done: function (res, curr, count) {
        }
        ,
        cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {title: '序号', width: 80, templet: '#indexTpl'}
            , {
                field: 'scheduleTableName', title: '执行班表名称'
            }, {
                field: 'aheadTime', title: '提前时间量'
            }
            , {field: 'pushDate', title: '通知下发时间'}
            , {field: 'operateName', title: '操作人'}
            , {
                field: 'notificationNumber', title: '通知成功数/通知人数', sort: false, templet: function (res) {
                    return res.successNumber + '/' + res.notificationNumber;
                }
            }
            , {
                field: 'feedBackNumber', title: '已反馈人数'
            }
            , {
                field: 'noFeedBackNumber', title: '未反馈人数', sort: false
            }
            , {
                field: 'feedBackRate', title: '3小时反馈率', templet: function (res) {
                    return (res.feedBackRate * 100).toFixed(2) + '%';
                }
            }
            , {fixed: 'right', title: '操作', width: 200, toolbar: '#barDemo'}
        ]],
        request: {//分页参数
            pageName: 'pageNo',//页码的参数名称，默认：page
            limitName: 'pageSize' //每页数据量的参数名，默认：limit
        },
        response: {
            statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
        },
        parseData: function (res) { //res 即为原始返回的数据
            const data = {
                "code": res.code, //解析接口状态
                "msg": res.message, //解析提示文本
                "count": res.data['totalElements'], //解析数据长度
                "data": res.data.content //解析数据列表
            };
            return data;
        },
        page: true
    });
    //监听单元格编辑
    table.on('tool(schedule-directive-table)', function (obj) {
        switch (obj.event) {
            case 'delExtra':
                deleteDistribute(obj.data.id);
                break;
            case'detail':
                showFeedback(obj.data.id);
                break;

            case 'urgent':
                // 催办
                urgentScheduleTableDistribute(obj.data.id);
                break;
        }
    });

    /**
     * 催办司机派班表中未反馈的人员
     */
    function urgentScheduleTableDistribute(id) {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '催办中...',
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
            type: api.schedule_distribute.urgentDistribute.type,
            url: api.base_url + api.schedule_distribute.urgentDistribute.url + '/' + id,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    layer.msg('催办成功', {
                        icon: 1,
                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                    }, function () {

                    });
                } else {
                    layer.msg('催办失败', {
                        icon: 1,
                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                    }, function () {

                    });
                }
            },
            error: function (response) {
                layer.close(loadingIndex);
            }
        })
    }

    /**
     * 删除下发信息
     * @param id
     */
    function deleteDistribute(id) {
        layer.confirm('确认删除该记录么?', function (index) {
            layer.close(index);
            const loadingIndex = layer.load(2, { //icon支持传入0-2
                content: '数据删除中...',
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
                type: api.schedule_distribute.deleteDistribute.type,
                url: api.base_url + api.schedule_distribute.deleteDistribute.url + '/' + id,
                async: true,
                contentType: 'application/json',
                success: function (response) {
                    layer.close(loadingIndex);
                    if (response.success) {
                        loadAllDriverScheduleTable();
                        scheduleDirectiveTable.reload();
                    }
                },
                error: function (response) {
                    layer.close(loadingIndex);
                }
            })
        });
    }

    /**
     * 加载司机派班表
     */
    function loadAllDriverScheduleTable() {
        $.ajax({
            type: api.schedule.getAllNoDistributeTables.type,
            url: api.base_url + api.schedule.getAllNoDistributeTables.url,
            data: {lineNo: '2'},
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    renderDriverPositionSelect(response.data.map(item => {
                        return {id: item.id, name: item.name}
                    }))
                }
            },
            error: function (response) {

            }
        })
    }

    /**
     * 渲染界面
     * @param data
     */
    function renderDriverPositionSelect(data) {
        const getTpl = document.getElementById('scheduleTableSelectTemplate').innerHTML;
        const view = document.getElementById('scheduleSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     * 下发派班表
     */
    $('#directiveSchedule').click(function () {
        layer.open({
            type: 1,
            title: '派班表选择',
            content: $('#timeScheduleEdit').html().replace('submitTimeSchedule', 'submitTimeSchedule-copy').replace('scheduleTimeInput', 'scheduleTimeInput-copy').replace('aheadTimeInput', 'aheadTimeInput-copy'),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                $('#submitTimeSchedule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: ['800px'],
            success: function (layero, index) {
                laydate.render({
                    elem: '#scheduleTimeInput-copy'
                    , type: 'time',
                    btns: ['now', 'confirm']
                });
                laydate.render({
                    elem: '#aheadTimeInput-copy'
                    , type: 'time',
                    btns: ['now', 'confirm']
                });
                form.render();
                addTextAreaFocusEvent();
                addClickEventToTemapletClass();
                form.on('submit(time-schedule-select)', function (data) {
                    if (data.field.scheduleTime == undefined || data.field.scheduleTime == null || data.field.scheduleTime != '') {
                        let nowTme = dateFns.format(new Date(), "HH:mm:ss");
                        if (nowTme > data.field.scheduleTime) {
                            layer.msg('定时发送时间不能小于当前时间', {
                                icon: 5,
                                time: 2000 //2秒关闭（如果不配置，默认是3秒）
                            }, function () {
                            });
                            return false;
                        }
                    }
                    if (data.field.scheduleTableId) {
                        layer.close(index);
                        distributeScheduleTable(data.field)
                    }
                    return false;
                });
            }
        });
    });

    /**
     *下发派班表
     */
    function distributeScheduleTable(data) {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '派班下发中,请耐心等待',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '200px',
                    'text-align': 'center',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        $.ajax({
            type: api.schedule_distribute.distribute.type,
            url: api.base_url + api.schedule_distribute.distribute.url,
            data: JSON.stringify(data),
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    loadAllDriverScheduleTable();
                    scheduleDirectiveTable.reload();
                }
            },
            error: function (response) {
                layer.close(loadingIndex);

            }
        })
    }

    /**
     * 加载已读和未读列表
     */
    function loadDriverFeedbackDetail(id) {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '数据加载中',
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
            type: api.schedule_distribute.feedback.type,
            url: api.base_url + api.schedule_distribute.feedback.url + "/" + id,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    let html = $('#directive-detail-info').html().replace('no-feedback-table', 'no-feedback-table-copy').replace('feedback-table', 'feedback-table-copy')
                        .replace('searchFeedback', 'searchFeedback-copy').replace('searchFeedbackButton', "searchFeedbackButton-copy")
                        .replace('searchNoFeedback', 'searchNoFeedback-copy').replace('searchNoFeedbackButton', 'searchNoFeedbackButton-copy');
                    layer.open({
                        type: 1,
                        title: '下达反馈详情',
                        content: html,
                        resize: true,
                        area: ['1250px', '740px'],
                        btn: ['催办', '取消'],
                        btnAlign: "r",
                        yes: function (index, layero) {//催办按钮
                            let data = table.checkStatus('no-feedback-table');
                            if (data.data.length <= 0) {
                                layer.msg('请选择催办人员', {
                                    icon: 5,
                                    time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                }, function () {
                                });
                            } else {

                            }
                        },
                        btn2: function (index, layero) {//取消按钮
                            layer.close(index);
                        },
                        success: function (layero, index) {
                            originData = response.data;
                            renderFeedback(response.data);
                        }
                    });
                }
            },
            error: function (response) {
                layer.close(loadingIndex);

            }
        })
    }

    /**
     *渲染已反馈和未反馈界面
     */
    function renderFeedback(data) {
        console.log(data);
        // if (data.feedback.length > 0) {
        //     const getTpl = document.getElementById('driverTemplate').innerHTML;
        //     const view = document.getElementById('feedbackList');
        //     view.innerHTML = '';
        //     laytpl(getTpl).render(data.feedback, function (html) {
        //         view.innerHTML = html;
        //     });
        // }

        const feedbackTable = table.render({
            title: '反馈列表',
            id: 'feedback-table',
            elem: '#feedback-table-copy',
            data: data.feedback,
            defaultToolbar: [],
            height: '520',
            text: {
                none: '暂无相关数据'
            },
            done: function (res, curr, count) {
            }
            ,
            cols: [[
                {field: 'name', title: '姓名'}
                , {field: 'mobilePhone', title: '电话'}
            ]],
            request: {//分页参数
                pageName: 'pageNo',//页码的参数名称，默认：page
                limitName: 'pageSize' //每页数据量的参数名，默认：limit
            },
            response: {
                statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
            },
            page: true
        });


        const noFeedbackTable = table.render({
            title: '未反馈列表',
            id: 'no-feedback-table',
            elem: '#no-feedback-table-copy',
            data: data.noFeedback,
            defaultToolbar: [],
            height: '520',
            text: {
                none: '暂无相关数据'
            },
            done: function (res, curr, count) {
            }
            ,
            cols: [[
                {type: 'checkbox', fixed: 'left'}
                , {field: 'name', title: '姓名'}
                , {field: 'mobilePhone', title: '电话'}
            ]],
            request: {//分页参数
                pageName: 'pageNo',//页码的参数名称，默认：page
                limitName: 'pageSize' //每页数据量的参数名，默认：limit
            },
            response: {
                statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
            },
            page: true
        });
        $('#searchFeedbackButton-copy').click(function () {
            let value = $('#searchFeedback-copy').val();
            if (value != null && value != '') {
                let filterData = originData.feedback.filter(item => {
                    return item.name.includes(value) || item.mobilePhone.includes(value);
                });
                noFeedbackTable.reload({
                    data: filterData
                })
            } else {
                noFeedbackTable.reload({
                    data: originData.feedback
                })
            }

        });
        $('#searchNoFeedbackButton-copy').click(function () {
            let value = $('#searchNoFeedback-copy').val();
            if (value != null && value != '') {
                let filterData = originData.noFeedback.filter(item => {
                    return item.name.includes(value) || item.mobilePhone.includes(value);
                });
                noFeedbackTable.reload({
                    data: filterData
                })
            } else {
                noFeedbackTable.reload({
                    data: originData.noFeedback
                })
            }
        });
    }

    function showFeedback(id) {
        loadDriverFeedbackDetail(id);
    }

    /**
     * 监控所有的textarea focus事件
     */

    function addTextAreaFocusEvent() {
        $('textarea').on('focus', function () {
            lastFocused = document.activeElement;
        })
    }

    /**
     * 给所有的template class加上点击事件
     */

    function addClickEventToTemapletClass() {
        $('.template').click(function () {
            var text = $(this).html();
            var input = lastFocused;
            if (input == undefined) {
                return;
            }
            var scrollPos = input.scrollTop;
            var pos = 0;
            var browser = ((input.selectionStart || input.selectionStart == "0") ?
                "ff" : (document.selection ? "ie" : false));
            if (browser == "ie") {
                input.focus();
                var range = document.selection.createRange();
                range.moveStart("character", -input.value.length);
                pos = range.text.length;
            } else if (browser == "ff") {
                pos = input.selectionStart
            }
            var front = (input.value).substring(0, pos);
            var back = (input.value).substring(pos, input.value.length);
            input.value = front + text + back;
            pos = pos + text.length;
            if (browser == "ie") {
                input.focus();
                var range = document.selection.createRange();
                range.moveStart("character", -input.value.length);
                range.moveStart("character", pos);
                range.moveEnd("character", 0);
                range.select();
            } else if (browser == "ff") {
                input.selectionStart = pos;
                input.selectionEnd = pos;
                input.focus();
            }
            input.scrollTop = scrollPos;
            $(input).trigger('input');
        });
    }

    /**
     * 重置明细搜索表单
     */
    const resetMxForm = function () {
        $("#mx-table-search-form")[0].reset();
        $("#mx-search-btn")[0].click();
    };
    /**
     * 监听点击重置按钮
     */
    form.on('submit(mx-reset-btn)', function (data) {
        resetMxForm();
        return false;
    });
    /**
     * 监听点击搜索按钮
     */
    form.on('submit(mx-search-btn)', function (data) {
        searchMxData(data.field);
        return false;
    });
    form.on('submit(export-btn)', function (data) {
        return false;
    });
    /**
     * 搜索明细数据
     */
    const searchMxData = function (data) {
        table.reload("schedule-directive-table", {
            url: api.base_url + api.schedule_distribute.findPage.url,
            method: api.schedule_distribute.findPage.type,
            contentType: 'application/json',
            request: {//分页参数
                pageName: 'pageNo',//页码的参数名称，默认：page
                limitName: 'pageSize' //每页数据量的参数名，默认：limit
            },
            page: true,
            response: {
                statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
            },
            parseData: function (res) { //res 即为原始返回的数据
                const data = {
                    "code": res.code, //解析接口状态
                    "msg": res.message, //解析提示文本
                    "count": res.data.totalElements, //解析数据长度
                    "data": res.data.content //解析数据列表
                };
                return data;
            },
            text: {
                none: '暂无相关数据'
            },
            where: data
        })
    };
});
