layui.use(['element', 'layer', 'table', 'laydate', 'form', 'api'], function () {
    const element = layui.element;
    element.init();
    const table = layui.table;
    const form = layui.form;
    const $ = layui.$; //重点处
    const api = layui.api;
    const laydate = layui.laydate;
    setTimeout(() => {
        form.render();
    }, 1);
    // 设置事故事件表格
    const driverPunchCardRecordTable = table.render({
        title: '一体机数据查询',
        id: 'punch-record-table',
        elem: '#punch-record-table',
        method: api.driverPunchCard.findPunchRecordPage.type,
        url: api.base_url + api.driverPunchCard.findPunchRecordPage.url,
        contentType: 'application/json',
        height: 'full-170',
        toolbar: '#accident-info-tool-bar',
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
                field: 'recordDate', title: '日期', templet: function (res) {
                    return dateFns.format(res.recordDate, 'YYYY-MM-DD')
                }
            }
            , {field: 'scheduleTableName', title: '执行班表名称'}
            , {field: 'name', title: '员工姓名'}
            , {field: 'employeeNumber', title: '员工号', sort: false}
            , {field: 'job', title: '岗位'}
            , {field: 'status', title: '班次', sort: false}
            , {field: 'taskText', title: '类型', sort: false}
            , {
                field: 'punchBySelf', title: '代出退勤', templet: function (res) {
                    return res.punchBySelf ? "否" : "是"
                }
            }
            , {field: 'recordTime', title: '记录时间'}
            , {
                field: 'lateOrEarly', title: '早退迟到', templet: function (res) {
                    return res.lateOrEarly ? "是" : "否"
                }
            }
            , {field: 'alcoholValue', title: '酒测值'}
            , {field: 'alcoholText', title: '酒测结果',}
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
            console.log(data);
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
    /**
     * 搜索明细数据
     */
    const searchMxData = function (data) {

        table.reload("punch-record-table", {
            method: api.driverPunchCard.findPunchRecordPage.type,
            url: api.base_url + api.driverPunchCard.findPunchRecordPage.url,
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

    function check(values) {
        for (let i = 0; i < values.length; i++) {
            if (values[i] != '') {
                return false;
            }
        }
        return true;
    }

    $('#replacePunchCard').click(function () {
        layer.open({
            type: 1,
            title: '带人出退勤',
            content: $('#replacePunchCardTemplate').html(),
            resize: false,
            btn: ['提交', '取消'],
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
                form.on('submit(submit-accident-edit-form)', function (data) {
                    const loadingIndex = layer.load(2); //换了种风格
                    $.ajax({
                        type: api.driverPunchCard.replacePunchCard.type,
                        url: api.base_url + api.driverPunchCard.replacePunchCard.url,
                        data: JSON.stringify(data.field),
                        async: true,
                        contentType: 'application/json',
                        success: function (data) {
                            layer.close(loadingIndex);
                            if (data.success) {
                                driverPunchCardRecordTable.reload();
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
                    return false;
                });
            }
        });
    });
});
