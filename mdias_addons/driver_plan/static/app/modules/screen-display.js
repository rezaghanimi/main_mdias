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
        title: '大屏显示调节',
        id: 'screen-display-table',
        elem: '#screen-display-table',
        url: api.base_url + api.screenDisplay.findScreenDisplayPage.url,
        method: api.screenDisplay.findScreenDisplayPage.type,
        contentType: 'application/json',
        height: 'full-100',
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
            , {
                field: 'date', title: '日期', templet: function (res) {
                    return dateFns.format(res.date, 'YYYY-MM-DD')
                }
            }

            , {field: 'attendanceSendContent', title: '出勤内容传达'}
            , {field: 'companyInfo', title: '公司要闻'}
            , {field: 'partyInfo', title: '公司党政工团信息'}
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
    $('#createScreenDisplay').click(function () {
        layer.open({
            type: 1,
            title: '添加大屏显示',
            content: $('#screenDisplayEdit').html().replace('scheduleDate', "scheduleDate-copy"),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                layero.find("#submit-form").click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: ['900px', '700px'],
            success: function (layero, index) {
                form.render();
                //日期时间选择器
                laydate.render({
                    elem: '#scheduleDate-copy'
                    , type: 'date',
                    btns: ['now', 'confirm']
                });
                form.on('submit(screen-display)', function (data) {
                    console.log(data.field);
                    const loadingIndex = layer.load(2); //换了种风格
                    $.ajax({
                        type: api.screenDisplay.saveScreenDisplay.type,
                        url: api.base_url + api.screenDisplay.saveScreenDisplay.url,
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
            }
        }, function (value, index) {
        });
    });
    //监听行工具事件
    table.on('tool(screen-display-table)', function (object) {
        const data = object.data;
        if (object.event === 'del') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.screenDisplay.deleteScreenDisplay.type,
                    url: api.base_url + api.screenDisplay.deleteScreenDisplay.url + "/" + data.id,
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
                title: '修改大屏调节',
                content: $('#screenDisplayEdit').html().replace('scheduleDate', "scheduleDate-copy"),
                resize: false,
                area: '700px',
                btn: ['提交', '取消'],
                btnAlign: "r",
                yes: function (index, layero) {//保存按钮
                    layero.find("#submit-form").click();
                },
                btn2: function (index, layero) {//取消按钮
                },
                success: function (layero, index) {
                    form.render();
                    //日期时间选择器
                    laydate.render({
                        elem: '#scheduleDate-copy'
                        , type: 'date'
                        , btns: ['now', 'confirm']
                    });
                    form.val('screenDisplayEdit', data);
                    form.on('submit(screen-display)', function (data) {
                        const loadingIndex = layer.load(2); //换了种风格
                        $.ajax({
                            type: api.screenDisplay.updateScreenDisplay.type,
                            url: api.base_url + api.screenDisplay.updateScreenDisplay.url,
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
        table.reload("screen-display-table", {
            url: api.base_url + api.screenDisplay.findScreenDisplayPage.url,
            method: api.screenDisplay.findScreenDisplayPage.type,
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
