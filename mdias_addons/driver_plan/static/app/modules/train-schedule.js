layui.use(['element', 'jquery', 'table', 'form', 'upload', 'api'], function () {
    const element = layui.element;
    const table = layui.table;
    const form = layui.form;
    const upload = layui.upload;
    const $ = layui.$; //重点处
    const api = layui.api;
    element.init();
    var runDiagramId = 1;


    $(document).on("click", ".layui-table-body table.layui-table tbody tr", function () {
        var index = $(this).attr('data-index');
        var tableBox = $(this).parents('.layui-table-box');
        //存在固定列
        if (tableBox.find(".layui-table-fixed.layui-table-fixed-l").length > 0) {
            tableDiv = tableBox.find(".layui-table-fixed.layui-table-fixed-l");
        } else {
            tableDiv = tableBox.find(".layui-table-body.layui-table-main");
        }
        //获取已选中列并取消选中
        var trs = tableDiv.find(".layui-unselect.layui-form-checkbox.layui-form-checked").parent().parent().parent();
        for (var i = 0; i < trs.length; i++) {
            var ind = $(trs[i]).attr("data-index");
            if (ind != index) {
                var checkCell = tableDiv.find("tr[data-index=" + ind + "]").find("td div.laytable-cell-checkbox div.layui-form-checkbox I");
                if (checkCell.length > 0) {
                    checkCell.click();
                }
            }
        }
        //选中单击行
        var checkCell = tableDiv.find("tr[data-index=" + index + "]").find("td div.laytable-cell-checkbox div.layui-form-checkbox.layui-form-checked I");
        if (!checkCell.length) {
            var checkCell = tableDiv.find("tr[data-index=" + index + "]").find("td div.laytable-cell-checkbox div.layui-form-checkbox I");
            checkCell.click();
        }

        //实现表格联动
        var wapper = $(this).closest('.schedule-list-table-wrapper');
        if (wapper.length) {
            var checkStatus = table.checkStatus('schedule-list-table');
            var id = checkStatus.data[0].id;
            if (runDiagramId != id) {
                runDiagramId = id;
                resetMxForm();
            }
        }
    });

    $(document).on("click", "td div.laytable-cell-checkbox div.layui-form-checkbox", function (e) {
        e.stopPropagation();
    });

    /**
     * 打开时刻表上传页面
     */
    const openImportDialog = function (data) {
        layer.open({
            type: 1,
            title: '上传时刻表',
            content: $('#uploadTrainSchedule').html(),
            resize: false,
            area: '700px',
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

                //设置form的值
                if (data) {
                    form.val("uploadTrainSchedule-form", data)
                }

                //监听数据提交
                form.on('submit(submit-uploadTrainSchedule-form)', function (data) {
                    const loadingIndex = layer.load(2, {zIndex: 19891019}); //换了种风格
                    const formData = new FormData(data.form);
                    $.ajax({
                        type: api.train_schedule.upload.type,
                        url: api.base_url + api.train_schedule.upload.url,
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
                                reloadMainData();
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
    };


    /**
     * 重新加载数据
     */
    const reloadMainData = function () {
        var searchkey = $("#search").val();
        table.reload("schedule-list-table", {
            where: {
                param: searchkey,
            }
        })
    };

    /**
     * 搜索明细数据
     */
    const searchMxData = function (data) {
        if (!runDiagramId) {
            table.reload("schedule-mx-list-table", {
                data: [],
                page: false
            })
        } else {
            data.tableId = runDiagramId;
            table.reload("schedule-mx-list-table", {
                method: api.train_schedule.list_schedule.type,
                url: api.base_url + api.train_schedule.list_schedule.url + "/" + runDiagramId,
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
                    var data = {
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
        }
    };

    /**
     * 重置明细搜索表单
     */
    const resetMxForm = function () {
        $("#mx-table-search-form")[0].reset();
        $("#mx-search-btn")[0].click();
    }

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

    /**
     * 时刻表总览
     */
    table.render({
        title: '时刻表总览',
        elem: '#schedule-list-table',
        method: api.train_schedule.list_table.type,
        url: api.base_url + api.train_schedule.list_table.url,
        page: true, //开启分页
        request: {//分页参数
            pageName: 'pageNo',//页码的参数名称，默认：page
            limitName: 'pageSize' //每页数据量的参数名，默认：limit
        },
        response: {
            statusCode: 200 //重新规定成功的状态码为 200，table 组件默认为 0
        },
        parseData: function (res) { //res 即为原始返回的数据
            runDiagramId = null;
            var data = {
                "code": res.code, //解析接口状态
                "msg": res.message, //解析提示文本
                "count": res.data.totalElements, //解析数据长度
                "data": res.data.content //解析数据列表
            };
            //设置第一条被选中
            var content = data.data;
            if (content && content.length) {
                content[0].LAY_CHECKED = true;
                runDiagramId = content[0].id;
            }
            return data;
        },
        text: {
            none: '暂无相关数据'
        },
        toolbar: '#list-toolbar',
        defaultToolbar: [],
        cols: [[ //表头
            {type: 'checkbox', fixed: 'left'},
            {field: 'trainDiagramNo', title: '运行图编号'},
            {field: 'scheduleNo', title: '时刻表编号'},
            {
                field: 'uploadDate', title: '上传时间', templet: function (res) {
                    return dateFns.format(res.uploadDate, 'YYYY-MM-DD')
                }
            },
            {field: 'operateName', title: '上传人'},
            {fixed: 'right', title: '操作', toolbar: '#list-bar', width: 120}
        ]],
        done: function (res, curr, count) {
            resetMxForm();
        }
    });

    /**
     *  监听时刻表总览头部工具栏事件
     */
    table.on('toolbar(schedule-list-table)', function (obj) {
        switch (obj.event) {
            case 'import':
                openImportDialog();//弹出上传框
                break;
            case 'search':
                reloadMainData();//重新加载数据
                break;
        }
    });

    /**
     * 监听时刻表总览行级工具栏
     */
    table.on('tool(schedule-list-table)', function (obj) {
        var data = obj.data;
        var id = data.id;
        if (obj.event === 'del') {
            layer.confirm('确认要删除该条数据吗？', function () {
                const loadingIndex = layer.load(2, {zIndex: 19891019}); //换了种风格
                $.ajax({
                    type: api.train_schedule.delete.type,
                    url: api.base_url + api.train_schedule.delete.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            reloadMainData();//重新加载数据
                            layer.closeAll();
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
        } else if (obj.event === 'edit') {
            openImportDialog(id);//弹出上传框
        }
    });

    /**
     *  监听时刻表总览行单击事件
     */
    table.on('row(schedule-list-table)', function (obj) {
    });

    /**
     * 时刻表明细
     */
    table.render({
        title: '时刻表明细',
        elem: '#schedule-mx-list-table',
        page: true,
        data: [],
        text: {
            none: '暂无相关数据'
        },
        defaultToolbar: [],
        cols: [[ //表头
            {type: 'checkbox', fixed: 'left'},
            {field: 'stationName', title: '车站名称'},
            {
                field: 'direction', title: '方向',
                templet: function (row) {
                    var direction = row.direction;
                    return direction == 1 ? "上行" : "下行";
                }
            },
            {field: 'fullTrainNo', title: '车次'},
            {field: 'departureStation', title: '始发站名'},
            {field: 'arrivalStation', title: '终到站名'},
            {field: 'arrivalTime', title: '到点'},
            {field: 'departureTime', title: '发点'},
            {field: 'stopTime', title: '停站时间'},
            {field: 'track', title: '停站股道'},
        ]],
    });

    /**
     * 打开时刻表上传页面
     */
    const openMxEditDialog = function (data) {
        layer.open({
            type: 1,
            title: '修改时刻表明细',
            content: $('#uploadTrainSchedule').html(),
            resize: false,
            area: '700px',
            btn: ['保存', '取消'],
            yes: function (index, layero) {//保存按钮
                layero.find("#mx-submit").click();
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

                //设置form的值
                if (data) {
                    form.val("uploadTrainSchedule-form", data)
                }

                //监听数据提交
                form.on('submit(submit-uploadTrainSchedule-form)', function (data) {
                    const loadingIndex = layer.load(2, {zIndex: 19891019}); //换了种风格
                    const formData = new FormData(data.form);
                    $.ajax({
                        type: "POST",
                        url: "http://localhost:8080/train-schedule/upload",
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
                                reloadMainData();
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
    };

    /**
     * 监听时刻表总览行级工具栏
     */
    table.on('tool(schedule-mx-list-table)', function (obj) {
        var data = obj.data;
        var id = data.id;
        if (obj.event === 'del') {
            layer.confirm('确认要删除该条数据吗？', function () {
                //TODO
            });
        } else if (obj.event === 'edit') {
            openMxEditDialog(id);//弹出上传框
        }
    });
})
