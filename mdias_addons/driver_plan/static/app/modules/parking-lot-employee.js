layui.use(['element', 'jquery', 'layer', 'table', 'api', 'form', 'laydate'], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const table = layui.table;
    const form = layui.form;
    const laydate = layui.laydate;
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
            , {field: 'lineNo', title: '所属车间'}
            , {field: 'organizationName', title: '级别'}
            , {field: 'job', title: '职别', sort: false}
            , {field: 'fleet', title: '所在地点'}
            , {field: 'machineClass', title: '备注', sort: false}
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
});
