layui.use(['element', 'jquery', 'layer', 'table', 'api', 'form', 'laydate'], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const table = layui.table;
    const form = layui.form;
    const laydate = layui.laydate;
    setTimeout(() => {
        laydate.render({
            elem: '#startDate'
            , type: 'date'
            , btns: ['now', 'confirm']
        });
        laydate.render({
            elem: '#endDate'
            , type: 'date'
            , btns: ['now', 'confirm']
        });
        form.render();
    }, 1);
    // 设置事故事件表格
    const crossingTable = table.render({
        title: '交路列表',
        id: 'crossing-table',
        elem: '#crossing-table',
        url: api.base_url + api.mileage.listAll.url,
        method: api.mileage.listAll.type,
        contentType: 'application/json',
        height: 'full-170',
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
            , {field: 'name', title: '交路名称'}
            , {field: 'code', title: '编号'}
            , {field: 'mileage', title: '里程(km)'}
            , {field: 'line', title: '所属线路'}
            , {field: 'section', title: '区间'}
            , {field: 'createdBy', title: '录入人员'}
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
                "count": res.data['totalElements'], //解析数据长度
                "data": res.data.content //解析数据列表
            };
            return data;
        },
        page: true
    });


    $('#addCrossing').click(function () {
        layer.open({
            type: 1,
            title: '添加交路信息',
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
                        type: api.mileage.save.type,
                        url: api.base_url + api.mileage.save.url,
                        data: JSON.stringify(data.field),
                        async: true,
                        contentType: 'application/json',
                        success: function (data) {
                            layer.close(loadingIndex);
                            if (data.success) {
                                crossingTable.reload();
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
    });
    //监听行工具事件
    table.on('tool(crossing-table)', function (object) {
        const data = object.data;
        if (object.event === 'del') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.mileage.delete.type,
                    url: api.base_url + api.mileage.delete.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            crossingTable.reload();
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
        } else if (object.event === 'edit') {
            layer.open({
                type: 1,
                title: '修改交路信息',
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
                    form.val('driver-edit-form', data);
                    form.on('submit(submit-driver-edit-form)', function (data) {
                        const loadingIndex = layer.load(2); //换了种风格
                        $.ajax({
                            type: api.mileage.update.type,
                            url: api.base_url + api.mileage.update.url,
                            data: JSON.stringify(data.field),
                            async: true,
                            contentType: 'application/json',
                            success: function (data) {
                                layer.close(loadingIndex);
                                if (data.success) {
                                    crossingTable.reload();
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
                        return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
                    });
                }
            }, function (value, index) {
            });
        }
    });
    /**
     * 司机里程
     */
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
            , {
                field: 'emergencyPhone', title: '里程(km)', templet: function (res) {
                    return 129
                }
            }
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
});
