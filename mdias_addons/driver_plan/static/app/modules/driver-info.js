layui.use(['element', 'layer', 'table', 'upload', 'form', 'api'], function () {
    const element = layui.element;
    element.init();
    const table = layui.table;
    const form = layui.form;
    const $ = layui.$; //重点处
    // 上传并覆盖
    const upload = layui.upload;
    const api = layui.api;
    // 设置司机信息表格
    const driverTable = table.render({
        title: '司机信息表',
        id: 'driver-info-table',
        elem: '#driver-info-table',
        url: api.base_url + api.driver.listAll.url,
        method: api.driver.listAll.type,
        contentType: 'application/json',
        toolbar: '#DriverInfoTableToolBar',
        defaultToolbar: [],
        text: {
            none: '暂无相关数据'
        },
        done: function (res, curr, count) {
            //table reload会使upload失效 每次加载完毕后重新处理
            //执行实例
        }
        ,
        cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {title: '序号', templet: '#indexTpl'}
            , {field: 'name', title: '姓名'}
            , {field: 'employeeNumber', title: '工号'}
            , {field: 'sex', title: '性别'}
            , {field: 'lineNo', title: '所属线路'}
            , {field: 'organizationName', title: '所属单位'}
            , {field: 'job', title: '职别', sort: false}
            , {field: 'fleet', title: '车队'}
            , {field: 'machineClass', title: '机班', sort: false}
            , {field: 'mobilePhone', title: '电话'}
            , {field: 'emergencyPhone', title: '紧急联系电话'}
            , {
                field: 'lastModifiedDate', title: '修改时间', templet: function (res) {
                    return dateFns.format(res.lastModifiedDate, 'YYYY-MM-DD')
                }
            }
            , {fixed: 'right', title: '操作', width: 120, toolbar: '#barDemo'}
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
                "count": res.data.totalElements, //解析数据长度
                "data": res.data.content //解析数据列表
            };
            return data;
        },
        page: true
    });
    //监听单元格编辑
    table.on('toolbar(driver-info-table)', function (obj) {
        switch (obj.event) {
            case 'export':
                table.exportFile(obj.config.id, obj.config.data, 'xls'); //data 为该实例中的任意数量的数据
                break;
            case 'downloadTemplate':
                const loadingIndex = layer.load(2, { //icon支持传入0-2
                    content: '模板下载中...',
                    success: function (layero) {
                        layero.find('.layui-layer-content').css({
                            'padding-top': '39px',
                            'width': '100px',
                            'background-position': 'top center'
                        });
                    }
                }); //换了种风格
                const request = new XMLHttpRequest();
                let fileName = "司机信息模板.xlsx";
                request.open(api.driver.downloadDriverTemplate.type, api.base_url + api.driver.downloadDriverTemplate.url, true);
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
            case 'add':
                layer.open({
                    type: 1,
                    title: '添加司机信息',
                    content: $('#editDriverInfo').html(),
                    resize: false,
                    area: '700px',
                    btn: ['提交', '取消'],
                    btnAlign: "r",
                    yes: function (index, layero) {//保存按钮
                        layero.find("#submit-driver-edit-form").click();
                    },
                    btn2: function (index, layero) {//取消按钮
                    },
                    success: function (layero, index) {
                        form.render();
                        form.on('submit(submit-driver-edit-form)', function (data) {
                            console.log(data.field);
                            const loadingIndex = layer.load(2); //换了种风格
                            $.ajax({
                                type: api.driver.save.type,
                                url: api.base_url + api.driver.save.url,
                                data: JSON.stringify(data.field),
                                async: true,
                                contentType: 'application/json',
                                success: function (data) {
                                    layer.close(loadingIndex);
                                    if (data.success) {
                                        driverTable.reload();
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
                                    layer.close(loadingIndex);
                                    layer.msg('操作失败', {
                                        icon: 5,
                                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                    }, function () {
                                    });
                                }
                            });
                            return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
                        });
                    }
                }, function (value, index) {
                });
                break;
            case 'search':
                driverTable.reload({
                    where: { //设定异步数据接口的额外参数，任意设
                        param: $('#input-param').val()
                    }
                    , page: {
                        curr: 1 //重新从第 1 页开始
                    }
                });
                break;
            case  'upload':
                layer.open({
                    type: 1,
                    title: '上传司机信息',
                    content: $('#uploadTrainSchedule').html().replace('schedule-form', 'schedule-form-copy').replace('cancel-uploadTrainSchedule-form', 'cancel-uploadTrainSchedule-form-copy'),
                    resize: false,
                    area: ['700px', '300px'],
                    success: function (layero, index) {
                        //选完文件后不自动上传
                        form.render();
                        form.on('submit(submit-uploadTrainSchedule-form)', function (data) {
                            const loadingIndex = layer.load(2, { //icon支持传入0-2
                                content: '上传中...',
                                success: function (layero) {
                                    layero.find('.layui-layer-content').css({
                                        'padding-top': '39px',
                                        'width': '100px',
                                        'background-position': 'top center'
                                    });
                                }
                            }); //换了种风格
                            const formData = new FormData(data.form);
                            $.ajax({
                                type: api.driver.uploadDriverTemplate.type,
                                url: api.base_url + api.driver.uploadDriverTemplate.url,
                                data: formData,
                                async: true,
                                contentType: false,
                                processData: false,
                                success: function (data) {
                                    layer.close(loadingIndex);
                                    if (data.success) {
                                        driverTable.reload();
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
                                    layer.close(loadingIndex);
                                    console.log(data);
                                    layer.msg('操作失败', {
                                        icon: 5,
                                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                    }, function () {
                                    });
                                }
                            });
                            return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
                        });
                        upload.render({
                            elem: '#schedule-form-copy',
                            url: '/upload/',
                            accept: "file",
                            acceptMime: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel',
                            auto: false,
                            size: 60, //限制文件大小，单位 KB
                            done: function (res) {
                                console.log(res)
                            }
                        });
                        $('#cancel-uploadTrainSchedule-form-copy').click(function () {
                            //关闭弹窗
                            layer.close(index);
                            return false;
                        });

                    }
                }, function (value, index) {
                });
                break;

        }
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
        table.reload("driver-info-table", {
            method: api.driver.listAll.type,
            url: api.base_url + api.driver.listAll.url,
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
    //监听行工具事件
    table.on('tool(driver-info-table)', function (object) {
        const data = object.data;
        if (object.event === 'del') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.driver.delete.type,
                    url: api.base_url + api.driver.delete.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            driverTable.reload();
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
                        layer.close(loadingIndex);
                        console.log(data);
                        layer.msg('操作失败', {
                            icon: 5,
                            time: 2000 //2秒关闭（如果不配置，默认是3秒）
                        }, function () {
                        });
                    }
                });
            });
        } else if (object.event === 'edit') {
            layer.open({
                type: 1,
                title: '修改司机信息',
                content: $('#editDriverInfo').html(),
                resize: false,
                area: ['700px', '520px'],
                btn: ['提交', '取消'],
                btnAlign: "r",
                yes: function (index, layero) {//保存按钮
                    layero.find("#submit-driver-edit-form").click();
                },
                btn2: function (index, layero) {//取消按钮
                },
                success: function (layero, index) {
                    form.val('driver-edit-form', data);
                    form.render();
                    form.on('submit(submit-driver-edit-form)', function (data) {
                        const loadingIndex = layer.load(2); //换了种风格
                        $.ajax({
                            type: api.driver.update.type,
                            url: api.base_url + api.driver.update.url,
                            data: JSON.stringify(data.field),
                            async: true,
                            contentType: 'application/json',
                            success: function (data) {
                                layer.close(loadingIndex);
                                if (data.success) {
                                    driverTable.reload();
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
                                layer.close(loadingIndex);
                                console.log(data);
                                layer.msg('操作失败', {
                                    icon: 5,
                                    time: 2000 //2秒关闭（如果不配置，默认是3秒）
                                }, function () {
                                });
                            }
                        });
                        return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
                    });
                }
            }, function (value, index) {
            });
        }
    });
})
