layui.use(['element', 'jquery', 'api', 'layer', 'table', 'upload', "form"], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const table = layui.table;
    const upload = layui.upload;
    const form = layui.form;

    // 设置事故事件表格
    const scheduleDirectiveTable = table.render({
        title: '计划下达反馈列表',
        id: 'schedule-directive-table',
        elem: '#schedule-directive-table',
        url: api.base_url + api.driver_position.findDriverPositionPage.url,
        method: api.driver_position.findDriverPositionPage.type,
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
            , {title: '序号', templet: '#indexTpl'}
            , {field: 'lineNo', title: '线路'}
            , {field: 'name', title: '位置图名称'}
            , {field: 'type', title: '运行图类型'}
            , {field: 'createdBy', title: '编制时间', sort: false}
            , {field: 'createdBy', title: '编制人'}
            , {fixed: 'right', width: 240, title: '操作', toolbar: '#editBar'}
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
            case 'view':
                localStorage.setItem("preViewId", obj.data.id);
                $("#layui-content-body").load("modules/driver-shift-position-preview.html", function () {
                    setTimeout(() => {
                        $('#loadData').click();
                    }, 100);
                });
                break;
            case "export":
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
                let fileName = "司机位置图-" + obj.data.name + ".xlsx";
                request.open(api.driver_position.exportDriverPositionToExcel.type, api.base_url + api.driver_position.exportDriverPositionToExcel.url + '/' + obj.data.id, true);
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
            case "upload":
                layer.open({
                    type: 1,
                    title: '上传司机位置图',
                    content: $('#uploadDriverPosition').html(),
                    resize: false,
                    area: ['700px', '350px'],
                    btn: ['上传', '取消'],
                    yes: function (index, layero) {//保存按钮
                        layero.find("#submit-uploadTrainSchedule-form").click();
                    },
                    btn2: function (index, layero) {//取消按钮
                    },
                    btnAlign: "r",
                    success: function (layero, index) {
                        layero.find("#schedule-file").addClass("schedule-file");
                        //初始化表格
                        form.render();

                        //上传按钮
                        upload.render({
                            elem: '.schedule-file',
                            url: '/upload/',
                            accept: "file",
                            acceptMime: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                            auto: false,
                            size: 20000, //限制文件大小，单位 KB
                            done: function (res) {
                            }
                        });
                        //监听数据提交
                        form.on('submit(submit-uploadTrainSchedule-form)', function (data) {
                            const loadingIndex = layer.load(2, {zIndex: 19891019}); //换了种风格
                            const formData = new FormData(data.form);
                            $.ajax({
                                type: api.driver_position.uploadDriverPositionExcel.type,
                                url: api.base_url + api.driver_position.uploadDriverPositionExcel.url + "/" + obj.data.id,
                                data: formData,
                                async: true,
                                contentType: false,
                                processData: false,
                                success: function (data) {
                                    layer.close(loadingIndex);
                                    if (data.success) {
                                        layer.close(index);
                                        layer.msg('操作成功', {
                                            icon: 1,
                                            time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                        });
                                        scheduleDirectiveTable.reload();
                                    } else {
                                        layer.msg(data.message, {
                                            icon: 5,
                                            time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                        });
                                    }
                                },
                                error: function (data) {
                                    layer.close(loadingIndex);
                                    layer.msg('操作失败', {
                                        icon: 5,
                                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                    });
                                }
                            });
                            return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
                        });
                    }
                });
                break;
            case "del":
                layer.confirm('确认删除该记录么?', function (index) {
                    const loadingIndex = layer.load(2); //换了种风格
                    $.ajax({
                        type: api.driver_position.deleteDriverPositionById.type,
                        url: api.base_url + api.driver_position.deleteDriverPositionById.url + "/" + obj.data.id,
                        async: true,
                        contentType: 'application/json',
                        success: function (data) {
                            layer.close(loadingIndex);
                            if (data.success) {
                                scheduleDirectiveTable.reload();
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
        }
    });
    $('#directiveSchedule').click(function () {
        $("#layui-content-body").load("modules/driver-shift-position.html");
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
        table.reload("schedule-directive-table", {
            url: api.base_url + api.driver_position.findDriverPositionPage.url,
            method: api.driver_position.findDriverPositionPage.type,
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
