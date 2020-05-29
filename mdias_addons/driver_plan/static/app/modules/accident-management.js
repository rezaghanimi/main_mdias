layui.use(['element', 'layer', 'table', 'laydate', 'form', 'api'], function () {
    const element = layui.element;
    element.init();
    const table = layui.table;
    const form = layui.form;
    const $ = layui.$; //重点处
    const api = layui.api;
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
    const accidentTable = table.render({
        title: '事故事件单管理',
        id: 'accident-info-table',
        elem: '#accident-info-table',
        method: api.accident_card.listAll.type,
        url: api.base_url + api.accident_card.listAll.url,
        contentType: 'application/json',
        toolbar: '#accident-info-tool-bar',
        height: 'full-140',
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
            , {field: 'category', title: '类别'}
            , {
                field: 'date', title: '日期', templet: function (res) {
                    return dateFns.format(res.date, 'YYYY-MM-DD')
                }
            }
            , {field: 'fullTrainNo', title: '车次'}
            , {field: 'trainNo', title: '车号'}
            , {field: 'driverName', title: '司机', sort: false}
            , {field: 'happenDate', title: '时间'}
            , {field: 'address', title: '地点', sort: false}
            , {field: 'scheduleName', title: '调度人'}
            , {field: 'description', title: '概况'}
            , {field: 'solution', title: '处理情况'}
            , {field: 'comment', title: '备注'}
            , {field: 'operateName', title: '录入人员'}
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
    table.on('toolbar(accident-info-table)', function (obj) {
        switch (obj.event) {
            case 'export':
                table.exportFile(obj.config.id, obj.config.data, 'xls'); //data 为该实例中的任意数量的数据
                break;
            case 'add':
                layer.open({
                    type: 1,
                    title: '新增事故事件',
                    content: $('#editAccidentInfo').html().replace('happenDateInput', "happenDateInput-copy"),
                    resize: false,
                    btn: ['提交', '取消', '保存并继续添加'],
                    btnAlign: "r",
                    yes: function (index, layero) {//保存按钮
                        layero.find("#submit-accident-edit-form").click();
                    },
                    btn2: function (index, layero) {//取消按钮
                    },
                    btn3: function (index, layero) {//取消按钮
                        layero.find("#submit-accident-edit").click();
                        return false;
                    },
                    area: '700px',
                    success: function (layero, index) {
                        form.render();
                        //日期时间选择器
                        laydate.render({
                            elem: '#happenDateInput-copy'
                            , type: 'datetime',
                            btns: ['now', 'confirm']
                        });
                        form.on('submit(submit-accident-edit-form)', function (data) {
                            console.log(data.field);
                            const loadingIndex = layer.load(2); //换了种风格
                            $.ajax({
                                type: api.accident_card.save.type,
                                url: api.base_url + api.accident_card.save.url,
                                data: JSON.stringify(data.field),
                                async: true,
                                contentType: 'application/json',
                                success: function (data) {
                                    layer.close(loadingIndex);
                                    if (data.success) {
                                        accidentTable.reload();
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
                        form.on('submit(submit-accident-edit)', function (data) {
                            const loadingIndex = layer.load(2); //换了种风格
                            console.log(data);
                            $.ajax({
                                type: api.accident_card.save.type,
                                url: api.base_url + api.accident_card.save.url,
                                data: JSON.stringify(data.field),
                                async: true,
                                contentType: 'application/json',
                                success: function (data) {
                                    layer.close(loadingIndex);
                                    if (data.success) {
                                        layero.find("#submit-accident-edit-reset").click();
                                        accidentTable.reload();
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
                accidentTable.reload({
                    where: { //设定异步数据接口的额外参数，任意设
                        param: $('#input-param').val()
                    }
                    , page: {
                        curr: 1 //重新从第 1 页开始
                    }
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
        table.reload("accident-info-table", {
            method: api.accident_card.listAll.type,
            url: api.base_url + api.accident_card.listAll.url,
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
    table.on('tool(accident-info-table)', function (object) {
        const data = object.data;
        if (object.event === 'del') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.accident_card.delete.type,
                    url: api.base_url + api.accident_card.delete.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            accidentTable.reload();
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
                title: '修改事故事件',
                content: $('#editAccidentInfo').html().replace('happenDateInput', "happenDateInput-copy"),
                resize: false,
                area: '700px',
                btn: ['提交', '取消'],
                btnAlign: "r",
                yes: function (index, layero) {//保存按钮
                    layero.find("#submit-accident-edit-form").click();
                },
                btn2: function (index, layero) {//取消按钮
                },
                success: function (layero, index) {
                    form.render();
                    //日期时间选择器
                    laydate.render({
                        elem: '#happenDateInput-copy'
                        , type: 'datetime'
                        , btns: ['now', 'confirm']
                    });
                    form.val('driver-edit-form', data);
                    form.on('submit(submit-accident-edit-form)', function (data) {
                        const loadingIndex = layer.load(2); //换了种风格
                        $.ajax({
                            type: api.accident_card.update.type,
                            url: api.base_url + api.accident_card.update.url,
                            data: JSON.stringify(data.field),
                            async: true,
                            contentType: 'application/json',
                            success: function (data) {
                                layer.close(loadingIndex);
                                if (data.success) {
                                    accidentTable.reload();
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
});
