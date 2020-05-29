layui.use(['element', 'jquery', 'api', 'layer', 'table', 'form', 'laydate'], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const form = layui.form;
    const table = layui.table;
    const laydate = layui.laydate;
    setTimeout(() => {
        laydate.render({
            elem: '#date'
            , type: 'date'
            , btns: ['now', 'confirm']
        });
        form.render();
    }, 1);
    // 设置事故事件表格
    const scheduleTable = table.render({
        title: '派班计划表管理',
        id: 'schedule-info-table',
        elem: '#schedule-info-table',
        url: api.base_url + api.schedule.findScheduleTablePageable.url,
        method: api.schedule.findScheduleTablePageable.type,
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
                field: 'lineNo', title: '线路'
            }
            , {field: 'name', title: '派班计划名称'}
            , {
                field: 'trainNo', title: '所属线路图类型', templet: function (res) {
                    return "W";
                }
            }, {
                field: 'date', title: '使用日期', templet: function (res) {
                    return dateFns.format(res.date, 'YYYY-MM-DD')
                }
            }
            , {field: 'operateName', title: '编制人'}
            , {
                field: 'lastModifiedDate', title: '编制时间', templet: function (res) {
                    return dateFns.format(res.lastModifiedDate, 'YYYY-MM-DD HH:mm:ss')
                }
            }
            , {fixed: 'right', title: '操作', width: 240, toolbar: '#barDemo'}
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
    table.on('tool(schedule-info-table)', function (obj) {
        switch (obj.event) {
            case 'delExtra':
                layer.confirm('确认删除该记录么?', function (index) {
                    const loadingIndex = layer.load(2); //换了种风格
                    $.ajax({
                        type: api.schedule.deleteById.type,
                        url: api.base_url + api.schedule.deleteById.url + "/" + obj.data.id,
                        async: true,
                        contentType: 'application/json',
                        success: function (data) {
                            layer.close(loadingIndex);
                            if (data.success) {
                                scheduleTable.reload();
                                layer.close(index);
                                layer.msg('操作成功', {
                                    icon: 1,
                                    time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                }, function () {

                                });
                            } else {
                                layer.msg(data.message, {
                                    icon: 5,
                                    time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                }, function () {
                                });
                            }
                        },
                        error: function (data) {
                            console.log(data);
                            layer.close(loadingIndex);
                            layer.msg('操作失败', {
                                icon: 5,
                                time: 2000 //2秒关闭（如果不配置，默认是3秒）
                            }, function () {
                            });
                        }
                    });
                });
                break;
            case "update":
                localStorage.setItem("updateScheduleId", obj.data.id);
                $("#layui-content-body").load("modules/driver-shift-schedule-edit.html", function () {
                    setTimeout(() => {
                        $('#loadData').click();
                    }, 100);
                });
                break;
            case'view':
                console.log(obj);
                localStorage.setItem("previewScheduleId", obj.data.id);
                $("#layui-content-body").load("modules/driver-shift-schedule-preview.html", function () {
                    setTimeout(() => {
                        $('#loadData').click();
                    }, 100);
                });
                break;
            case 'export':
                //导出
                const loadingIndex = layer.load(2, { //icon支持传入0-2
                    content: '导出数据中,请耐心等待...',
                    success: function (layero) {
                        layero.find('.layui-layer-content').css({
                            'padding-top': '39px',
                            'width': '200px',
                            'background-position': 'top center'
                        });
                    }
                }); //换了种风格
                const request = new XMLHttpRequest();
                let scheduleDate = dateFns.format(obj.data.date, 'YYYY-MM-DD');
                let fileName = "司机派班表-" + scheduleDate + ".xlsx";
                request.open(api.schedule.exportScheduleTable.type, api.base_url + api.schedule.exportScheduleTable.url + '/' + obj.data.id, true);
                request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
                request.responseType = 'blob';
                request.onload = function (e) {
                    layer.close(loadingIndex);
                    if (this.status === 200) {
                        console.log(this);
                        const blob = this.response;
                        if (window.navigator.msSaveOrOpenBlob) {
                            window.navigator.msSaveBlob(blob, fileName);
                        } else {
                            const downloadLink = window.document.createElement('a');
                            const contentTypeHeader = request.getResponseHeader("Content-Type");
                            downloadLink.href = window.URL.createObjectURL(new Blob([blob], {type: contentTypeHeader}));
                            downloadLink.download = fileName;
                            document.body.appendChild(downloadLink);
                            downloadLink.click();
                            document.body.removeChild(downloadLink);
                        }
                    }
                };
                request.send();
                break;
        }
    });
    //新增派班表计划
    $('#createSchedule').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule-create.html");
    });

    //新发派班表
    $('#copySchedule').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule-new.html");
    });

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
        table.reload("schedule-info-table", {
            url: api.base_url + api.schedule.findScheduleTablePageable.url,
            method: api.schedule.findScheduleTablePageable.type,
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
