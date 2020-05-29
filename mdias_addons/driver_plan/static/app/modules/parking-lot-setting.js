layui.use(['element', 'jquery', 'api', 'layer', 'table', 'form', 'layedit', 'formSelects', 'laydate', 'laytpl'], function () {
    const element = layui.element;
    const $ = layui.$;
    const api = layui.api;
    const table = layui.table;
    const form = layui.form;
    const formSelects = layui.formSelects;
    const laydate = layui.laydate;
    const laytpl = layui.laytpl;
    //普通规则
    const replaceDateInputIds = ['maxWorkTimeInput', 'minRestTimeInput', 'morningShiftStartTimeInput', 'morningShiftEndTimeInput', 'dayShiftStartTimeInput', 'dayShiftEndTimeInput', 'nightShiftStartTimeInput', 'nightShiftEndTimeInput',
        'launchStartTimeInput', 'launchEndTimeInput', 'dinnerStartTimeInput', 'dinnerEndTimeInput', 'submitTimeSchedule', 'maxRestTimeInput', 'minWorkTimeInput', 'minDinnerTimeInput', 'maxDinnerTimeInput'];
    const excludesIds = ['submitTimeSchedule'];
    //补充规则
    const replaceExtraDateInputIds = ['submitExtraRule', 'aheadTimeInput'];
    initSelectStationData();
    initSelectRouteData();
    initSelectCircleModelData();
    // 设置事故事件表格
    const ruleTable = table.render({
        title: '普通规则列表',
        id: 'schedule-rule-table',
        elem: '#schedule-rule-table',
        url: api.base_url + api.rule.findNormalRulePage.url,
        method: api.rule.findNormalRulePage.type,
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
            , {field: 'name', title: '规则名称'}
            , {field: 'type', title: '运行图类型'}
            , {field: 'lineNo', title: '所属线路'}
            , {
                field: 'makeDate', title: '编制时间', sort: false, templet: function (res) {
                    return dateFns.format(res.makeDate, 'YYYY-MM-DD HH:mm:ss')
                }
            }
            , {field: 'createdBy', title: '录入人员'}
            , {fixed: 'right', title: '操作', width: 120, toolbar: '#normalBar'}
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
    //监听普通规则table 行点击事件
    table.on('tool(schedule-rule-table)', function (object) {
        const data = object.data;
        if (object.event === 'editNormal') {
            updateNormalRuleView(data);
        } else if (object.event === 'delNormal') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.rule.deleteByRuleId.type,
                    url: api.base_url + api.rule.deleteByRuleId.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            ruleTable.reload();
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
        }

    });
    //点击刷新普通规则table
    $('#refreshTable').click(() => {
        if (ruleTable) {
            ruleTable.reload();
        }
    });
    const extraRuleTable = table.render({
        title: '派班计划表管理',
        id: 'extra-schedule-rule-table',
        elem: '#extra-schedule-rule-table',
        url: api.base_url + api.rule.findExtraRulePage.url,
        method: api.rule.findExtraRulePage.type,
        contentType: 'application/json',
        height: 'full-320',
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
            , {field: 'name', title: '规则名称'}
            , {field: 'type', title: '运行图类型'}
            , {field: 'lineNo', title: '所属线路'}
            , {
                field: 'makeDate', title: '编制时间', sort: false, templet: function (res) {
                    return dateFns.format(res.makeDate, 'YYYY-MM-DD HH:mm:ss')
                }
            }
            , {field: 'createdBy', title: '录入人员'}
            , {fixed: 'right', title: '操作', width: 120, toolbar: '#extraBar'}
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

    $('#refreshExtraTable').click(() => {
        if (extraRuleTable) {
            extraRuleTable.reload();
        }
    });

    //监听补充规则table 行点击事件
    table.on('tool(extra-schedule-rule-table)', function (object) {

        const data = object.data;
        if (object.event === 'editExtra') {

        } else if (object.event === 'delExtra') {
            layer.confirm('确认删除该记录么?', function (index) {
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.rule.deleteByRuleId.type,
                    url: api.base_url + api.rule.deleteByRuleId.url + "/" + data.id,
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            extraRuleTable.reload();
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
        }
    });

    $('#createSchedule').click(() => {
        layer.open({
            type: 1,
            title: '添加规则',
            content: replaceArray($('#rule-setting-form').html(), replaceDateInputIds, '-copy'),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            area: '1000px',
            yes: function (index, layero) {//保存按钮
                $('#submitTimeSchedule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            success: function (layero, index) {
                form.render();
                resetSelects();
                replaceDateInputIds.filter(item => {
                    return !excludesIds.includes(item);
                }).forEach(item => {
                    //日期时间选择器
                    laydate.render({
                        elem: '#' + item + '-copy'
                        , type: 'time',
                        btns: ['now', 'confirm']
                    });
                });
                form.on('submit(time-schedule-select)', function (data) {
                    saveNormalRule(data.field, index);
                    return false;
                });
            }
        });
    });

    function saveNormalRule(data, index) {
        const rule = {};
        rule.name = data.name;
        rule.type = data.type;
        rule.value = JSON.stringify(data);
        const loadingIndex = layer.load(2); //换了种风格
        $.ajax({
            type: api.rule.saveNormalRule.type,
            url: api.base_url + api.rule.saveNormalRule.url,
            data: JSON.stringify(rule),
            async: true,
            contentType: 'application/json',
            success: function (data) {
                layer.close(loadingIndex);
                if (data.success) {
                    layer.close(index);
                    ruleTable.reload();
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
    }

    function replaceArray(source, find, replace) {
        let replaceString = source;
        for (let i = 0; i < find.length; i++) {
            replaceString = replaceString.replace(find[i], find[i] + replace);
        }
        return replaceString;
    };

    function replaceArrays(source, find, replace) {
        let replaceString = source;
        for (let i = 0; i < find.length; i++) {
            replaceString = replaceString.replace(find[i], replace[i]);
        }
        return replaceString;
    };
    $('#addExtraRule').click(() => {
        layer.open({
            type: 1,
            title: '添加补充规则',
            content: replaceArray($('#extra-rule-setting-form').html(), replaceExtraDateInputIds, '-copy'),
            resize: true,
            btn: ['完成', '取消'],
            btnAlign: "r",
            maxHeight: 1000,
            yes: function (index, layero) {//保存按钮
                //触发form验证
                layero.find('form').each(function () {
                    $(this).find('.form-submit').click();
                });
                /**
                 * 在form表单中提交时多次触发
                 * @type {Array}
                 */
                    // TODO 待优化点击提交 form多次触发submit 多个form不好控制 暂时有点击触发数据校验
                const dutyForms = [];
                layero.find('.duty-form').each(function () {
                    dutyForms.push(translateFromData($(this).serializeArray()));
                });

                const leavingForms = [];
                layero.find('.leaving-form').each(function () {
                    leavingForms.push(translateLeavingFromData($(this).serializeArray()));
                });
                const formData = translateFromDataToObject(layero.find('.extra-form').serializeArray());
                saveExtraRule(dutyForms, leavingForms, formData, index);
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: '1000px',
            success: function (layero, index) {
                form.render();
                initTimeSelectTimeout();
                initPickupFromAddAndDelete(layero);
                initLeavingWorkFormAddAndDelete(layero);
                //添加出勤地点
                layero.find('#addDutyForm').click(() => {
                    layero.find('.pickUpFormContainer').append(replaceArrays($('#pickup-template').html(), ['aheadTimeInputTemplate'], ['aheadTimeInput-copy' + new Date().getTime()]));
                    initPickupFromAddAndDelete(layero);
                    initTimeSelectTimeout();
                    form.render();
                });
                //添加退勤地点
                layero.find('#addLeadingWorkForm').click(() => {
                    layero.find('.leavingWorkFormContainer').append($('#leavingWork-template').html());
                    initLeavingWorkFormAddAndDelete(layero);
                    form.render();
                });
                form.on('submit(*)', function (data) {
                    return false;
                });
            }
        });
    });

    /**
     * 初始化form退勤地点form里面的button事件
     */
    function initLeavingWorkFormAddAndDelete(layero) {
        layero.find('.deleteLeavingWorkRow').unbind('click');
        layero.find('.deleteLeavingWorkRow').click(function () {
            $(this).closest('form').remove();
        });
        layero.find('.addLeavingWork').unbind('click');
        layero.find('.addLeavingWork').click(function () {
            let items = $(this).attr('data-value');
            items = parseInt(items);
            items += 1;
            $(this).attr('data-value', items);
            $(this).parent().after('<div class="layui-row margin-top-20">' + replaceArrays(layero.find('.leavingRow').html(), ['添加', 'addLeavingWork', 'pickUpStation'],
                ['删除', 'deleteLeavingWork', 'pickUpStation' + items])
                + '</div>');
            form.render();
            layero.find('.deleteLeavingWork').unbind('click');
            layero.find('.deleteLeavingWork').click(function () {
                $(this).parent().remove();
                form.render();
            });
        });
    }

    /**
     * 初始化form出勤表单里面的button事件
     * @param layero
     */
    function initPickupFromAddAndDelete(layero) {
        layero.find('.deleteRow').unbind('click');
        layero.find('.deleteRow').click(function () {
            $(this).closest('form').remove();
        });
        layero.find('.addPickUp').unbind('click');
        layero.find('.addPickUp').click(function () {
            let items = $(this).attr('data-value');
            items = parseInt(items);
            items += 1;
            $(this).attr('data-value', items);
            $(this).parent().after('<div class="layui-row margin-top-20">' + replaceArrays(layero.find('.pickUpRow').html(), ['添加', 'addPickUp', 'aheadTimeInput-copy', 'pickUpStation', 'aheadTime'],
                ['删除', 'deletePickUp', 'aheadTimeInput-copy' + new Date().getTime(), 'pickUpStation' + items, 'aheadTime' + items])
                + '</div>');
            form.render();
            initTimeSelectTimeout();
            layero.find('.deletePickUp').unbind('click');
            layero.find('.deletePickUp').click(function () {
                    $(this).parent().remove();
                    form.render();
                    initTimeSelectTimeout();
                }
            )
        });
    }

    function initTimeSelectTimeout() {
        setTimeout(initTimeSelect, 1)
    }

    /**
     * 初始化时间选择框
     */
    function initTimeSelect() {
        lay('.aheadTime').each(function () {
            //防止lay-key重复导致laydate一闪而过
            $(this).removeAttr('lay-key');
            laydate.render({
                elem: '#' + $(this).attr('id')
                , type: 'time',
                btns: ['now', 'confirm']
            });
        });
        element.init();
    }

    function translateFromDataToObject(array) {
        let result = {};
        array.forEach(item => {
            result[item.name] = item.value;
        });
        return result;
    }

    /**
     * 转换出勤地点数据
     * 将表单数据转为对象数据
     {name: "dutyStation", value: "电客车组长"}
     1: {name: "pickUpStation", value: "电客车司机"}
     2: {name: "aheadTime", value: "18:07:56"}
     3: {name: "pickUpStation1", value: "电客车组长"}
     4: {name: "aheadTime1", value: "18:07:58"}
     5: {name: "pickUpStation2", value: "电客车司机"}
     6: {name: "aheadTime2", value: "18:07:49"}
     7: {name: "pickUpStation3", value: "实习生"}
     8: {name: "aheadTime3", value: "18:07:51"}
     9: {name: "pickUpStation4", value: "电客车司机"}
     10: {name: "aheadTime4", value: "18:07:52"}
     转换为
     {dutyStation:'',pickUpList:[
            {pickUpStation:'',aheadTime:'00:34:00'}....
     ]}
     */
    function translateFromData(array) {
        let result = {};
        const nullTarget = array.find(item => {
            return item.value == undefined || item.value == null || item.value == '';
        });
        if (nullTarget) {
            return {};
        }
        const target = array.find(item => {
            return item.name === 'dutyStation';
        });
        if (target) {
            result.dutyStation = target.value;
            result.pickUpList = [];
            array.splice(array.indexOf(target), 1);//删除dutyStation
            for (let i = 0; i < array.length / 2; i++) {
                const targetPick = array.find(item => {
                    return item.name == 'pickUpStation' + (i == 0 ? '' : i);
                });
                const targetAhead = array.find(item => {
                    return item.name === 'aheadTime' + (i == 0 ? '' : i);
                });
                if (targetPick && targetAhead) {
                    result.pickUpList.push({pickUpStation: targetPick.value, aheadTime: targetAhead.value});
                }
            }
        }
        return result;
    }

    /**
     * 转换退勤地点数据
     * @param array
     * @returns {{}}
     */
    function translateLeavingFromData(array) {
        let result = {};
        const nullTarget = array.find(item => {
            return item.value == undefined || item.value == null || item.value == '';
        });
        if (nullTarget) {
            return {};
        }
        const target = array.find(item => {
            return item.name === 'leavingStation';
        });
        if (target) {
            result.leavingStation = target.value;
            result.pickUpList = [];
            array.splice(array.indexOf(target), 1);//删除dutyStation
            for (let i = 0; i < array.length / 2; i++) {
                const targetPick = array.find(item => {
                    return item.name == 'pickUpStation' + (i == 0 ? '' : i);
                });
                if (targetPick) {
                    result.pickUpList.push({pickUpStation: targetPick.value});
                }
            }
        }
        return result;
    }

    /***
     *保存补充规则
     */
    function saveExtraRule(dutyForms, leavingForms, formData, index) {
        /**
         * 数据校验以及数据保存
         */
        if (dutyForms && leavingForms && formData && dutyForms.length > 0 && leavingForms.length > 0 && formData.name != '') {
            const emptyTarget = dutyForms.find(item => {
                return Object.keys(item).length === 0;
            });
            const emptyLeavingTarget = leavingForms.find(item => {
                return Object.keys(item).length === 0;

            });
            if (!emptyTarget && !emptyLeavingTarget) {
                const value = {dutyData: dutyForms, leavingData: leavingForms};
                formData.value = JSON.stringify(value);
                const loadingIndex = layer.load(2); //换了种风格
                $.ajax({
                    type: api.rule.saveExtraRule.type,
                    url: api.base_url + api.rule.saveExtraRule.url,
                    data: JSON.stringify(formData),
                    async: true,
                    contentType: 'application/json',
                    success: function (data) {
                        layer.close(loadingIndex);
                        if (data.success) {
                            extraRuleTable.reload();
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
            }

        }
    }

    function updateNormalRuleView(data) {
        layer.open({
            type: 1,
            title: '修改规则',
            content: replaceArray($('#rule-setting-form').html(), replaceDateInputIds, '-copy'),
            resize: true,
            btn: ['提交', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                $('#submitTimeSchedule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: '1000px',
            success: function (layero, index) {
                form.render();
                const temp = JSON.parse(data.value);
                if (temp.changePoint) {
                    setSelectsValue('changePoint', temp.changePoint.split(','));
                }
                if (temp.routes) {
                    setSelectsValue('changeRoute', temp.routes.split(','));
                }
                if (temp.circleModel) {
                    setSelectsValue('circleModel', temp.circleModel.split(','));
                }
                temp.id = data.id;
                form.val('normal-rule-edit-form', temp);
                replaceDateInputIds.filter(item => {
                    return !excludesIds.includes(item);
                }).forEach(item => {
                    //日期时间选择器
                    laydate.render({
                        elem: '#' + item + '-copy'
                        , type: 'time',
                        btns: ['now', 'confirm']
                    });
                });
                form.on('submit(time-schedule-select)', function (data) {
                    updateNormalRule(data.field, index);
                    return false;
                });
            }
        });
    }

    function updateNormalRule(data, index) {
        const rule = {};
        rule.name = data.name;
        rule.type = data.type;
        rule.id = data.id;
        rule.value = JSON.stringify(data);
        const loadingIndex = layer.load(2); //换了种风格
        $.ajax({
            type: api.rule.updateNormalRule.type,
            url: api.base_url + api.rule.updateNormalRule.url,
            data: JSON.stringify(rule),
            async: true,
            contentType: 'application/json',
            success: function (data) {
                layer.close(loadingIndex);
                if (data.success) {
                    layer.close(index);
                    ruleTable.reload();
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
    }

    function resetSelects() {
        formSelects.value('changePoint', []);
        formSelects.value('changeRoute', []);
        formSelects.value('circleModel', []);
    }

    function setSelectsValue(target, value) {
        formSelects.value(target, value);
    }

    /**
     * 初始化当前页面所有select 选择站点数据
     */
    function initSelectStationData() {
        $.ajax({
            type: api.train_schedule.list_all_station.type,
            url: api.base_url + api.train_schedule.list_all_station.url + "/1",
            async: true,
            contentType: 'application/json',
            success: function (data) {
                //请求数据成功渲染界面
                if (data.success) {
                    const getTpl = document.getElementById('stationOptionTemplate').innerHTML;
                    laytpl(getTpl).render(data.data, function (html) {
                        document.querySelectorAll('.stationSelect').forEach(item => {
                            item.innerHTML = html;
                        });
                    });
                    const tpl = document.getElementById('stationMultipleOptionTemplate').innerHTML;
                    laytpl(tpl).render(data.data, function (html) {
                        document.querySelectorAll('.stationMultipleSelect').forEach(item => {
                            item.innerHTML = html;
                        });
                        formSelects.render();
                        formSelects.btns('changePoint', []);
                    });
                }
            },
            error: function (data) {

            }
        });
    }

    /**
     * 初始化当前页面所有select 选择交路数据
     */
    function initSelectRouteData() {
        $.ajax({
            type: api.train_schedule.list_all_route.type,
            url: api.base_url + api.train_schedule.list_all_route.url + "/1",
            async: true,
            contentType: 'application/json',
            success: function (data) {
                //请求数据成功渲染界面
                if (data.success) {
                    const tpl = document.getElementById('routeOptionTemplate').innerHTML;
                    laytpl(tpl).render(data.data, function (html) {
                        document.querySelectorAll('.routeMultipleSelect').forEach(item => {
                            item.innerHTML = html;
                        });
                        formSelects.render();
                        formSelects.btns('changeRoute', []);
                    });
                }
            },
            error: function (data) {

            }
        });
    }

    /**
     * 初始化当前页面所有select 选择交路数据
     */
    function initSelectCircleModelData() {
        formSelects.render();
        formSelects.btns('circleModel', []);
    }
});
