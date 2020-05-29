layui.use(['element', 'jquery', 'laytpl', 'api', 'form'], function () {
    const element = layui.element;
    const $ = layui.$; //重点处
    const laytpl = layui.laytpl;
    const api = layui.api;
    const form = layui.form;
    let absentDrivers = [];
    let originData = {};
    let currentData = {};
    let scheduleTable = {};
    loadAllDriverScheduleTable();

    /**
     * 根据选择的派班表加载数据
     */
    function loadScheduleDetail(id) {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '数据加载中...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '100px',
                    'text-align': 'center',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        $.ajax({
            type: api.schedule.findScheduleTableDetailById.type,
            url: api.base_url + api.schedule.findScheduleTableDetailById.url + '/' + id,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    const data = response.data;
                    originData = _.cloneDeep(data);
                    currentData = _.cloneDeep(data);
                    absentDrivers = data.absentDrivers;
                    scheduleTable = data.scheduleTable;
                    showScheduleTableInfo();
                    renderAbsentDriverSchedule(absentDrivers);
                    renderDriverSchedule(data);
                    processDriverData(currentData);
                    $('#operation-container button').removeClass('layui-disabled');
                }
            },
            error: function (response) {

            }
        })
    }

    /**
     * 显示派班表的信息
     */
    function showScheduleTableInfo() {
        if (scheduleTable.circleModel) {
            let result = '';
            let circleModel = scheduleTable.circleModel.replace(/[0-9]/ig, "").split(',');
            for (let i = 0; i < circleModel.length; i++) {
                result += '<button class="layui-btn layui-btn-sm layui-btn-primary">' + circleModel[i] + '</button>'
            }
            $('#circleModel').html(result);
        }
        if (scheduleTable.date) {
            $('#scheduleDate').html(dateFns.format(scheduleTable.date, 'YYYY-MM-DD'));
        }
    }

    /**
     * 根据司机信息渲染界面
     */
    function renderDriverSchedule(data) {
        const getTpl = document.getElementById('scheduleClassTemplate').innerHTML;
        const view = document.getElementById("templateContainer");
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     * 加载司机派班表
     */
    function loadAllDriverScheduleTable() {
        $.ajax({
            type: api.schedule.findLatestSchedules.type,
            url: api.base_url + api.schedule.findLatestSchedules.url,
            data: {lineNo: '2'},
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    renderDriverPositionSelect(response.data.map(item => {
                        return {id: item.id, name: item.name}
                    }))
                }
            },
            error: function (response) {

            }
        })
    }

    /**
     * 渲染界面
     * @param data
     */
    function renderDriverPositionSelect(data) {
        const getTpl = document.getElementById('scheduleTableSelectTemplate').innerHTML;
        const view = document.getElementById('scheduleSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     * 选择派班表
     */
    $('#scheduleTableSelect').click(function () {
        layer.open({
            type: 1,
            title: '派班表选择',
            content: $('#timeScheduleEdit').html().replace('submitTimeSchedule', 'submitTimeSchedule-copy').replace('scheduleTimeInput', 'scheduleTimeInput-copy').replace('aheadTimeInput', 'aheadTimeInput-copy'),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                $('#submitTimeSchedule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: ['400px', '600px'],
            success: function (layero, index) {
                form.render();
                form.on('submit(time-schedule-select)', function (data) {
                    if (data.field.scheduleTableId) {
                        layer.close(index);
                        loadScheduleDetail(data.field.scheduleTableId);
                    }
                    return false;
                });
            }
        });
    });

    /**
     * 处理司机数据 生成右击菜单
     * @param data
     */
    function processDriverData(data) {
        let fleets = data.drivers;
        let menus = fleets.map(item => {
            let firstElement = item.machineClasses.find(element => {
                return element.shift;
            });
            let type = firstElement ? firstElement.shift.typeName : '休班';
            let drivers = item.machineClasses.map(entry => {
                let drivers = entry.drivers.map(element => {
                    return {
                        name: element.name, id: entry.name + ":" + element.id, callback: function (itemKey, opt, e) {
                            console.log(itemKey);
                            let me = $(this);
                            changeDriverOrStudent(me.attr('id'), me.attr('type'), me.closest('tr').attr('type'), me.attr('value'), itemKey);
                        }
                    };
                });
                let students = entry.student.map(element => {
                    return {
                        name: element.name, id: entry.name + ":" + element.id, callback: function (itemKey, opt, e) {
                            let me = $(this);
                            changeDriverOrStudent(me.attr('id'), me.attr('type'), me.closest('tr').attr('type'), me.attr('value'), itemKey);
                        }
                    };
                });
                let position = entry.name;
                let result = {};
                result.name = position;
                let items = [];
                if (drivers.length > 0) {
                    let tempDrivers = {};
                    drivers.forEach(element => {
                        tempDrivers['change:drivers:' + item.name + ':' + element.id] = element;
                    });
                    items.push({name: '司机', items: tempDrivers});
                }
                if (students.length > 0) {
                    let tempStudent = {};
                    students.forEach(element => {
                        tempStudent['change:student:' + item.name + ':' + element.id] = element;
                    });
                    items.push({name: '学员/实习生', items: tempStudent});
                }
                result.items = items;
                return result;
            });
            let result = {};
            result.name = type;
            result.items = drivers;
            if (drivers.length > 40) {
                let arrays = _.chunk(drivers, drivers.length / 2);
                let tempDrivers = [];
                arrays.forEach(element => {
                    tempDrivers.push({name: element[0].name + '-' + element[element.length - 1].name, items: element});
                });
                result.items = tempDrivers;
            } else {
                result.items = drivers;
            }
            return result;
        });
        let supplyMenus = fleets.map(item => {
            let firstElement = item.machineClasses.find(element => {
                return element.shift;
            });
            let type = firstElement ? firstElement.shift.typeName : '休班';
            let drivers = item.machineClasses.map(entry => {
                let position = entry.name;
                let result = {};
                result.name = position;
                result.id = item.name + ':' + position;
                result.callback = function (itemKey, opt, e) {
                    let me = $(this);
                    supplyDriverOrStudent(me.attr('id'), me.attr('type'), me.closest('tr').attr('type'), me.attr('value'), itemKey);
                };
                return result;
            });
            let result = {};
            result.name = type;
            result.items = drivers;
            if (drivers.length > 0) {
                let arrays = _.chunk(drivers, drivers.length / 2);
                let tempDrivers = [];
                arrays.forEach(element => {
                    let tempPositions = {};

                    element.forEach(entry => {
                        tempPositions['supply:' + entry.id] = entry
                    });
                    tempDrivers.push({
                        name: element[0].name + '-' + element[element.length - 1].name,
                        items: tempPositions
                    });
                });
                result.items = tempDrivers;
            }
            return result;
        });
        initDriverContextMenu(menus, supplyMenus);
    }

    /**
     * 右击菜单
     */
    function initDriverContextMenu(menus, supplyMenus) {
        let loadItems = function () {
            return new Promise(function (resolve, reject) {
                resolve(menus);
                reject({'name': '加载失败'})
            });
        };
        let loadCloneItems = function () {
            return new Promise(function (resolve, reject) {
                resolve(supplyMenus);
                reject({'name': '加载失败'})
            });
        };
        $.contextMenu('destroy', '.rightClick');
        $.contextMenu({
            selector: '.rightClick',
            className: "limit-context-size",
            build: function ($trigger, e) {
                return {
                    callback: function (key, options) {
                        console.log(options);
                        const m = "clicked: " + key;
                        console.log(this);
                        console.log($(this).attr("id"));
                        console.log($(this).attr("type"));
                        window.console && console.log(m);
                    },
                    items: {
                        "edit": {
                            name: "调整状态", icon: "edit", items: {
                                'OCC': {
                                    name: 'OCC轮值', callback: function (itemKey, opt, e) {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), 'OCC轮值', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "duty": {
                                    name: '日勤', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '日勤', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "training": {
                                    name: '培训', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '培训', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "year": {
                                    name: '年休', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '年休', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "weak": {
                                    name: '病假', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '病假', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "affairs": {
                                    name: '事假', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '事假', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "wedding": {
                                    name: '婚假', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '婚假', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "nursing": {
                                    name: '护理假', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '护理假', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "changeRest": {
                                    name: '调休', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '调休', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "newLine": {
                                    name: '新线调试', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '新线调试', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "stationary": {
                                    name: '外部驻勤', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '外部驻勤', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                                "other": {
                                    name: '其他', callback: function () {
                                        let me = $(this);
                                        movePersonToAbsent(me.attr('id'), me.attr('type'), '其他', me.closest('tr').attr('type'), me.attr('value'));
                                    }
                                },
                            }
                        },
                        "update":
                            {
                                name: '调班',
                                items: loadCloneItems(),
                            },
                        "change":
                            {
                                name: '换班',
                                items: loadItems(),
                            },
                        "sep1": "---------",
                        "quit": {
                            name: "取消", icon: function () {
                                return 'context-menu-icon context-menu-icon-quit';
                            }
                        }
                    }
                }
            },

        });
    }

    /**
     * 修改司机状态 将司机列入休假名单中
     * @param id
     * @param type
     * @param reason
     * @param fleetName
     * @param machineClassName
     */
    function movePersonToAbsent(id, type, reason, fleetName, machineClassName) {
        let fleet = currentData.drivers.find(item => {
            return item.name == fleetName;
        });
        let targets = fleet.machineClasses[machineClassName - 1][type];
        console.log(targets);
        let target = targets.find(item => {
            return item.id = id;
        });
        targets.splice(targets.indexOf(target), 1);
        target.driverShiftId = '';
        target.status = 0;
        target.reason = reason;
        target.remark = '';
        absentDrivers.push(target);
        absentDrivers.sort((a, b) => {
            return a.reason > b.reason ? 1 : -1;
        });
        renderDriverSchedule(currentData);
        processDriverData(currentData);
        renderAbsentDriverSchedule(absentDrivers);
    }

    /**
     *  互换班组
     * @param id
     * @param type
     * @param fleetName
     * @param machineClassName
     * @param target
     */
    function changeDriverOrStudent(id, type, fleetName, machineClassName, target) {
        let conditions = target.split(":");
        if (type != conditions[1]) {
            layer.msg('互换机班需要相同的职别', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
            return;
        }
        let fleet = currentData.drivers.find(item => {
            return item.name == fleetName;
        });
        let sources = fleet.machineClasses[machineClassName - 1][type];
        let source = sources.find(item => {
            return item.id = id;
        });
        let targetFleet = currentData.drivers.find(item => {
            return item.name == conditions[2];
        });
        let targets = targetFleet.machineClasses[conditions[3] - 1][type];
        if (!target || targets.length == 0) {
            layer.msg('目标位置无出勤人员', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
        } else {
            let target = targets.find(item => {
                return item.id == conditions[4];
            });
            sources.splice(sources.indexOf(source), 1);
            targets.splice(targets.indexOf(target), 1);

            targets.push(source);
            sources.push(target);
            renderDriverSchedule(currentData);
            processDriverData(currentData);

        }
    }

    /**
     * 将目标司机或者学员调整到对应的位置
     * @param id
     * @param type
     * @param fleetName
     * @param machineClassName
     * @param target
     */
    function supplyDriverOrStudent(id, type, fleetName, machineClassName, target) {
        let fleet = currentData.drivers.find(item => {
            return item.name == fleetName;
        });
        let sources = fleet.machineClasses[machineClassName - 1][type];
        let source = sources.find(item => {
            return item.id = id;
        });
        let conditions = target.split(":");
        let targetFleet = currentData.drivers.find(item => {
            return item.name == conditions[1];
        });
        let targets = targetFleet.machineClasses[conditions[2] - 1][type];
        if (targets.length > 0) {
            layer.msg('目标位置已有出勤人员', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
        } else {
            source.fleet = conditions[1];
            source.machineClass = conditions[2];
            targets.push(source);
            sources.splice(sources.indexOf(source), 1);
            renderDriverSchedule(currentData);
            processDriverData(currentData);
        }
    }

    /**
     * 休假或者没有上线的司机的操作
     */
    function createAbsentDriverMenu() {
        if (absentDrivers && absentDrivers.length > 0) {
            $.contextMenu('destroy', '.absent-click');
            $.contextMenu({
                selector: '.absent-click',
                className: "limit-context-size",
                items: {
                    'backOrigin': {
                        name: '返回原机班', callback: function (itemKey, opt, e) {
                            let me = $(this);
                            driverBackOriginPosition(me.attr("id"));
                        }
                    },
                    'updateStatus': {
                        name: '调整司机状态', items: {
                            'OCC': {
                                name: 'OCC轮值', callback: function (itemKey, opt, e) {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), 'OCC轮值');
                                }
                            },
                            "duty": {
                                name: '日勤', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '日勤');
                                }
                            },
                            "training": {
                                name: '培训', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '培训');
                                }
                            },
                            "year": {
                                name: '年休', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '年休');
                                }
                            },
                            "weak": {
                                name: '病假', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '病假');
                                }
                            },
                            "affairs": {
                                name: '事假', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '事假');
                                }
                            },
                            "wedding": {
                                name: '婚假', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '婚假');
                                }
                            },
                            "nursing": {
                                name: '护理假', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '护理假');
                                }
                            },
                            "changeRest": {
                                name: '调休', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '调休');
                                }
                            },
                            "newLine": {
                                name: '新线调试', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '新线调试');
                                }
                            },
                            "stationary": {
                                name: '外部驻勤', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '外部驻勤');
                                }
                            },
                            "other": {
                                name: '其他', callback: function () {
                                    let me = $(this);
                                    updateDriverStatus(me.attr("id"), '其他');
                                }
                            },
                        }
                    }
                }
            });
        }
    }

    /**
     * 休假人员修改状态
     * @param id
     * @param reason
     */
    function updateDriverStatus(id, reason) {
        let target = absentDrivers.find(item => {
            return item.id == id;
        });
        if (target.reason != reason) {
            target.reason = reason;
            absentDrivers.sort((a, b) => {
                return a.reason > b.reason ? 1 : -1;
            });
            renderAbsentDriverSchedule(absentDrivers);

        }
    }

    /**
     * 返回原机班的操作处理数据
     */
    function driverBackOriginPosition(id) {
        let target = absentDrivers.find(item => {
            return item.id == id;
        });
        let fleetName = target.originFleet;
        let machineClassName = target.originMachineClass;

        let fleet = currentData.drivers.find(item => {
            return item.name == fleetName;
        });
        let type = target.job == '电客车司机' ? 'drivers' : 'student';
        let sources = fleet.machineClasses[machineClassName - 1][type];
        if (sources && sources.length > 0) {
            layer.msg('原机班已有出勤人员', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
        } else {
            target.machineClass = target.originMachineClass;
            target.fleet = target.originFleet;
            sources.push(target);
            absentDrivers.splice(absentDrivers.indexOf(target), 1);
            absentDrivers.sort((a, b) => {
                return a.reason > b.reason ? 1 : -1;
            });
            renderDriverSchedule(currentData);
            processDriverData(currentData);
            renderAbsentDriverSchedule(absentDrivers);
        }
    }

    /**
     * 根据司机信息渲染请假人员名单
     */
    function renderAbsentDriverSchedule(data) {
        createAbsentDriverMenu();
        const getTpl = document.getElementById('absentDriverTemplate').innerHTML;
        const view = document.getElementById("absentDriverContainer");
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     *返回按钮点击事件
     */
    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule.html");
    });

    /**
     * 保存新发派班表
     */
    $('#saveNewSchedule').click(function () {
        scheduleTable.id = '';
        currentData.scheduleTable = scheduleTable;
        const loadingIndex = layer.load(2); //换了种风格
        $.ajax({
            type: api.schedule.createSchedule.type,
            url: api.base_url + api.schedule.createSchedule.url,
            data: JSON.stringify(currentData),
            async: true,
            contentType: 'application/json',
            success: function (data) {
                layer.close(loadingIndex);
                if (data.success) {
                    layer.msg('操作成功', {
                        icon: 1,
                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                    }, function () {
                        $("#layui-content-body").load("modules/driver-shift-schedule.html");
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
    });

    /**
     * addDay 增加一天
     */
    $('#addDay').click(function () {
        if (scheduleTable.date) {
            scheduleTable.date = dateFns.addDays(scheduleTable.date, 1);
            showScheduleTableInfo();
            processScheduleCircle(true);
        }
    });
    /**
     * 减一天
     */
    $('#subtractDay').click(function () {
        if (scheduleTable.date) {
            scheduleTable.date = dateFns.subDays(scheduleTable.date, 1);
            showScheduleTableInfo();
        }
    });

    /**
     * 处理派班表的轮转信息
     */
    function processScheduleCircle(reverse) {
        if (scheduleTable.circleModel) {
            let circleModel = scheduleTable.circleModel.replace(/[0-9]/ig, "").split(',');
            let circleModelTemp = arrayRotate(_.cloneDeep(circleModel), reverse);
            if (currentData.drivers) {
                let shiftData = currentData.drivers.map(item => {
                    let machineClasses = item.machineClasses;
                    if (machineClasses && machineClasses.length > 0) {
                        let type = machineClasses[0].status.replace(/[0-9]/ig, "");
                        let shifts = machineClasses.map(element => {
                            return element.shift;
                        });
                        let statuses = machineClasses.map(element => {
                            return element.status;
                        });
                        return {name: item.name, type: type, data: {shifts: shifts, status: statuses}};
                    }
                    return {name: item.name, type: '', data: {shifts: [], status: []}}
                });
                shiftData.forEach(item => {
                    let type = circleModelTemp[circleModel.indexOf(item.type)];
                    console.log(type);
                    let data = shiftData.find(element => {
                        return element.type == type;
                    });
                    if (data) {
                        let fleet = currentData.drivers.find(element => {
                            return element.name == item.name;
                        });
                        if (fleet) {
                            for (let i = 0; i < fleet.machineClasses.length; i++) {
                                fleet.machineClasses[i].shift = data.data.shifts[i];
                                fleet.machineClasses[i].status = data.data.status[i];
                            }
                        }
                    }

                });
                renderDriverSchedule(currentData);
                processDriverData(currentData);
            }
        }
    }

    /**
     * 往上挪动班次信息
     */
    $('#upRoll').click(function () {
        rotateSchedule();
    });
    /**
     * 往下挪动班次信息
     */
    $('#downRoll').click(function () {
        rotateSchedule(true);
    });

    /**
     * 根据参数滚动派班表中的派班班次信息
     * @param reverse
     */
    function rotateSchedule(reverse) {
        if (currentData.drivers) {
            currentData.drivers.forEach(item => {
                let machineClasses = item.machineClasses;
                if (machineClasses && machineClasses.length > 0) {
                    let shifts = machineClasses.map(element => {
                        return element.shift;
                    });
                    let statuses = machineClasses.map(element => {
                        return element.status;
                    });
                    let rotateShifts = arrayRotate(shifts, reverse);
                    let rotateStatuses = arrayRotate(statuses, reverse);
                    for (let i = 0; i < machineClasses.length; i++) {
                        machineClasses[i].shift = rotateShifts[i];
                        machineClasses[i].status = rotateStatuses[i];
                    }
                }
            });
            renderDriverSchedule(currentData);
            processDriverData(currentData);
        }
    }

    /**
     * 数组滚动
     * @param arr
     * @param reverse
     * @returns {*}
     */
    function arrayRotate(arr, reverse) {
        if (reverse) arr.unshift(arr.pop());
        else arr.push(arr.shift());
        return arr;
    }
});