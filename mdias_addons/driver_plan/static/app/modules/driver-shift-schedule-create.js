layui.use(['element', 'jquery', 'form', 'laytpl', 'api', 'steps', 'laydate'], function () {
    const element = layui.element;
    const form = layui.form;
    const $ = layui.$; //重点处
    const laytpl = layui.laytpl;
    const api = layui.api;
    const laydate = layui.laydate;
    let global$Step = {};
    let globalOptions = {};
    let positionData = {};
    let shiftData = {};
    let driverData = {};
    let globalDriverSchedule = {};
    let absentDrivers = [];
    loadDriverPositions();
    loadAllDriverInfo();
    element.init();
    initSteps();

    /**
     * 初始化日期
     */
    laydate.render({
        elem: '#scheduleDate'
    });

    /**
     * 初始化步骤条
     */
    function initSteps() {
        global$Step = $("#step_demo").step();
        $("#preBtn").click(function (event) {
            global$Step.preStep();//上一步
        });
        $("#nextBtn").click(function (event) {
            if (global$Step.getCurrentPage() == 0 || global$Step.getCurrentPage() == 1) {
                console.log('first');
                selectDriverPositionToMachineClass();
                // $step.nextStep();//下一步
            } else if (global$Step.getCurrentPage() == 2) {
                if (globalDriverSchedule) {
                    if (dataCheck()) {
                        global$Step.nextStep();//下一步
                    } else {
                    }
                }

            } else {

            }
        });
    }

    /**
     * 检测司机和派班数据是否满足需求
     * @returns {boolean}
     */
    function dataCheck() {
        for (let i = 0; i < globalDriverSchedule.length; i++) {
            let temp = globalDriverSchedule[i];
            for (let j = 0; j < temp.machineClasses.length; j++) {
                let entry = temp.machineClasses[j];
                if (entry.shift) {
                    if (entry.drivers.length == 0) {
                        setTimeout(function () {
                            layer.msg(entry.shift.typeName + entry.shift.position + '-未分配司机', {
                                icon: 5,
                                time: 2000 //2秒关闭（如果不配置，默认是3秒）
                            }, function () {
                            });
                        }, 100);
                        return false;
                    }
                }

            }
        }
        return true;
    }


    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule.html");
    });
    $('#getAllDriverPosition').click(function () {
        layer.open({
            type: 1,
            title: '司机位置图选择',
            content: $('#timeScheduleEdit').html().replace('submitTimeSchedule', 'submitTimeSchedule-copy'),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                $('#submitTimeSchedule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: ['400px', '500px'],
            success: function (layero, index) {
                form.render();
                form.on('submit(time-schedule-select)', function (data) {
                    if (data.field.position) {
                        layer.close(index);
                        loadPositionData(data.field.position);
                    }
                    return false;
                });
            }
        });
    });

    /**
     * 加载司机位置图数据
     * @param id
     */
    function loadPositionData(id) {
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
            type: api.driver_position.findDriverPositionById.type,
            url: api.base_url + api.driver_position.findDriverPositionById.url + '/' + id,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    const data = response.data;
                    positionData = data;
                    const shifts = processData(data.driverShifts);
                    const dayShiftList = shifts.filter(item => {
                        return item.type === 'day';
                    });
                    const morningShiftList = shifts.filter(item => {
                        return item.type === 'morning';
                    });
                    const nightShiftList = shifts.filter(item => {
                        return item.type === 'night';
                    });
                    shiftData.dayShiftList = dayShiftList;
                    shiftData.morningShiftList = morningShiftList;
                    shiftData.nightShiftList = nightShiftList;
                    renderMachineClassView(morningShiftList, 'morningShiftContainer');
                    renderMachineClassView(dayShiftList, 'dayShiftContainer');
                    renderMachineClassView(nightShiftList, 'nightShiftContainer');
                }
            },
            error: function (response) {

            }
        })
    }

    /**
     * 处理数据
     * @param data
     * @returns {*}
     */
    function processData(data) {
        return data.map(item => {
            item.dtsList = item.dtsList.map(function (entry, index, array) {
                //处理休息时间计算
                if (index === 0 || array.length === 1) {
                    entry.restTime = '00:00:00';
                } else {
                    entry.restTime = diff(array[index - 1]['arrivalSchedule'].arrivalTime, entry['pickUpSchedule'].arrivalTime);
                }
                return entry;
            });
            //处理出退勤地点
            if (item.dtsList[0].origin) {
                item.firstDepartureStation = item.dtsList[0].pickUpSchedule.departureStation;
            } else {
                item.firstDepartureStation = item.dtsList[0].pickUpSchedule.arrivalStation;
            }
            item.lastArrivalStation = item.dtsList[item.dtsList.length - 1].arrivalStation;
            return item;
        });
    }

    //计算时间两个时间 HH:mm:ss 相差的HH:mm:ss
    function diff(start, end) {
        start = start.split(":");
        end = end.split(":");
        const startDate = new Date(0, 0, 0, start[0], start[1], start[2]);
        const endDate = new Date(0, 0, 0, end[0], end[1], start[2]);
        let diff = endDate.getTime() - startDate.getTime();
        let hours = Math.floor(diff / 1000 / 60 / 60);
        const seconds = Math.floor(diff / 100) % 60;
        diff -= hours * 1000 * 60 * 60;
        const minutes = Math.floor(diff / 1000 / 60);

        // If using time pickers with 24 hours format, add the below line get exact hours
        if (hours < 0)
            hours = hours + 24;

        return (hours <= 9 ? "0" : "") + hours + ":" + (minutes <= 9 ? "0" : "") + minutes + ":00";
    }

    //自定义layui tpl函数
    laytpl.convertSecondsToTime = function (seconds) {
        let hours = Math.floor(seconds / 60 / 60);
        const second = seconds % 60;
        seconds -= hours * 60 * 60;
        const minutes = Math.floor(seconds / 60);

        // If using time pickers with 24 hours format, add the below line get exact hours
        if (hours < 0)
            hours = hours + 24;
        return (hours <= 9 ? "0" : "") + hours + ":" + (minutes <= 9 ? "0" : "") + minutes + ":" + (Math.abs(second) <= 9 ? '0' : '') + Math.abs(second);
    };

    /**
     *
     * @param data
     * @param template
     * @param viewContainer
     */
    function renderMachineClassView(data, viewContainer) {
        const getTpl = document.getElementById('processScheduleTemplate').innerHTML;
        const view = document.getElementById(viewContainer);
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    function loadDriverPositions() {
        $.ajax({
            type: api.driver_position.findAllDriverPosition.type,
            url: api.base_url + api.driver_position.findAllDriverPosition.url,
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

    function renderDriverPositionSelect(data) {
        const getTpl = document.getElementById('schedulePositionSelectTemplate').innerHTML;
        const view = document.getElementById('positionSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    /**
     * 加载司机数据
     */
    function loadAllDriverInfo() {
        $.ajax({
            type: api.driver.findAll.type,
            url: api.base_url + api.driver.findAll.url,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    driverData = processDriverData(response.data);
                    console.log(driverData);
                }
            },
            error: function (response) {

            }
        })
    }

    /**
     * 处理司机数据
     */
    function processDriverData(data) {
        let temp = _.cloneDeep(data);
        temp.forEach(item => {
            /**
             * 机班队长和组长
             */
            let captain = item.machineClasses.find(entry => {
                if (entry.name == undefined || entry.name == null || entry.name == '') {
                    return entry;
                }
            });
            let leaders = captain.drivers.filter(element => {
                return element.job == '电客车组长';
            }).map(element => {
                element.originFleet = element.fleet;
                element.originMachineClass = element.machineClass;
                return element;
            });
            let captains = captain.drivers.filter(element => {
                return element.job == '电客车队长';
            }).map(element => {
                element.originFleet = element.fleet;
                element.originMachineClass = element.machineClass;
                return element;
            });
            item.machineClasses = item.machineClasses.filter(entry => {
                return (entry.name != undefined && entry.name != null && entry.name != '');
            }).sort((a, b) => {
                return a.name - b.name;
            });
            /**
             * 处理客车司机与学员/见习生
             */
            item.machineClasses.forEach(element => {
                let realDrivers = element.drivers.filter(entry => {
                    return entry.job == '电客车司机';
                }).map(element => {
                    element.originFleet = element.fleet;
                    element.originMachineClass = element.machineClass;
                    return element;
                });
                let student = element.drivers.filter(entry => {
                    return entry.job == '电客车学员' || entry.job == '实习生';
                }).map(element => {
                    element.originFleet = element.fleet;
                    element.originMachineClass = element.machineClass;
                    return element;
                });
                element.drivers = realDrivers;
                element.student = student;
                element.status = "休" + element.name;
                element.id = uuid();
            });
            item.captains = captains;
            item.leaders = leaders;
            item.id = uuid();
        });
        console.log(temp);
        return temp;
    }

    /**
     * uuid生成器
     * @returns {string}
     */
    function uuid() {
        let d = Date.now();
        if (typeof performance !== 'undefined' && typeof performance.now === 'function') {
            d += performance.now(); //use high-precision timer if available
        }
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = (d + Math.random() * 16) % 16 | 0;
            d = Math.floor(d / 16);
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
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
     * 选择车队 机班与位置图中位置的对应关系
     */
    function selectDriverPositionToMachineClass() {
        layer.open({
            type: 1,
            title: '补充规则设定',
            content: $('#machineClassTemplate').html().replace('submit-position-to-machine', 'submit-position-to-machine-copy'),
            resize: false,
            btn: ['完成', '取消'],
            btnAlign: "r",
            yes: function (index, layero) {//保存按钮
                $('#submit-position-to-machine-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            area: ['800px', '600px'],
            success: function (layero, index) {
                form.render();
                form.on('submit(submit-position-to-machine)', function (data) {
                    if (data.field) {
                        //不能选择相同车队
                        if (!(data.field.dayFleet != data.field.morningFleet && data.field.dayFleet != data.field.nightFleet && data.field.morningFleet != data.field.nightFleet)) {
                            layer.msg('不能选择相同车队', {
                                icon: 5,
                                time: 2000 //2秒关闭（如果不配置，默认是3秒）
                            }, function () {

                            });
                            return false;
                        }
                        let dayFields = Object.keys(data.field).filter(item => {
                            return item.startsWith("day");
                        });
                        let morningFields = Object.keys(data.field).filter(item => {
                            return item.startsWith("morning");
                        });
                        let nightFields = Object.keys(data.field).filter(item => {
                            return item.startsWith("night");
                        });
                        let dayPosition = {'type': 'day'};
                        dayFields.forEach(item => {
                            dayPosition[item] = data.field[item];
                        });
                        let morningPosition = {'type': 'morning'};
                        morningFields.forEach(item => {
                            morningPosition[item] = data.field[item];
                        });
                        let nightPosition = {'type': 'night'};
                        nightFields.forEach(item => {
                            nightPosition[item] = data.field[item];
                        });
                        globalOptions.dayPosition = dayPosition;
                        globalOptions.nightPosition = nightPosition;
                        globalOptions.morningPosition = morningPosition;
                        processPositionDataToDriverMachineClass();
                        layer.close(index);
                    }
                    return false;
                });
            }
        });
    }

    /**
     *处理司机位置图与机班的对应关系
     */
    function processPositionDataToDriverMachineClass() {
        let tempDriverData = _.cloneDeep(driverData);
        // 查询当前选择的车队分配任务
        let activeFleets = Object.keys(globalOptions).map(item => {
            let temp = globalOptions[item];
            return {
                fleet: temp[temp.type + "Fleet"],
                type: temp.type,
                position: temp[temp.type + 'FleetDriverPosition'],
                machine: temp[temp.type + 'FleetMachinePosition']
            };
        });
        activeFleets.forEach(element => {
            let currentFleet = tempDriverData.find(item => {
                return item.name.includes(element.fleet);
            });
            let position = element.position - 1;
            let machine = element.machine - 1;
            let type = element.type;
            let machineSize = currentFleet.machineClasses.length;
            let shifts = shiftData[type + 'ShiftList'];
            let positionSize = shifts.length;
            for (let i = 0; i < machineSize; i++) {
                let currentMachine = machine + i;
                let currentPosition = position + i;
                if (currentMachine > machineSize - 1) {
                    currentMachine = currentMachine - machineSize;
                }
                if (currentPosition > positionSize - 1) {
                    currentPosition = currentPosition - positionSize;
                }
                let shift = shifts[currentPosition];
                let machineClass = currentFleet.machineClasses[currentMachine];
                machineClass.status = shift.typeName + +shift.position;
                machineClass.shift = shift;
            }
        });
        globalDriverSchedule = tempDriverData;
        renderDriverSchedule(tempDriverData);
        console.log(tempDriverData);
        processMachineDriverData(tempDriverData);
        global$Step.nextStep();
    }

    /**
     * 保存派班表
     */
    form.on('submit(submit-driver-schedule)', function (data) {
        let postData = {};
        postData.scheduleTable = data.field;
        postData.scheduleTable.circleModel = positionData.driverPosition.circleModel;
        postData.drivers = globalDriverSchedule;
        postData.absentDrivers = absentDrivers;
        const loadingIndex = layer.load(2); //换了种风格
        $.ajax({
            type: api.schedule.saveSchedule.type,
            url: api.base_url + api.schedule.saveSchedule.url,
            data: JSON.stringify(postData),
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
        return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
    });

    /**
     * 处理司机数据 生成右击菜单
     * @param data
     */
    function processMachineDriverData(data) {
        let menus = data.map(item => {
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
        let supplyMenus = data.map(item => {
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
     *返回按钮点击事件
     */
    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-schedule.html");
    });

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
        let fleet = globalDriverSchedule.find(item => {
            return item.name == fleetName;
        });
        console.log(fleet);
        console.log(fleet.machineClasses[machineClassName - 1]);
        let targets = fleet.machineClasses[machineClassName - 1][type];
        let target = targets.find(item => {
            return item.id = id;
        });
        console.log(target);
        targets.splice(targets.indexOf(target), 1);
        target.driverShiftId = '';
        target.status = 0;
        target.reason = reason;
        target.remark = '';
        absentDrivers.push(target);
        absentDrivers.sort((a, b) => {
            return a.reason > b.reason ? 1 : -1;
        });
        renderDriverSchedule(globalDriverSchedule);
        processMachineDriverData(globalDriverSchedule);
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
        let fleet = globalDriverSchedule.find(item => {
            return item.name == fleetName;
        });
        let sources = fleet.machineClasses[machineClassName - 1][type];
        let source = sources.find(item => {
            return item.id = id;
        });
        let targetFleet = globalDriverSchedule.find(item => {
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
            swap(source, target, 'fleet');
            swap(source, target, 'machineClass');
            targets.push(source);
            sources.push(target);
            renderDriverSchedule(globalDriverSchedule);
            processMachineDriverData(globalDriverSchedule);

        }
    }

    /**
     * 对象属相的swap
     * @param sourceObj
     * @param sourceKey
     * @param targetObj
     * @param targetKey
     */
    function swap(sourceObj, sourceKey, targetObj, targetKey) {
        const temp = sourceObj[sourceKey];
        sourceObj[sourceKey] = targetObj[targetKey];
        targetObj[targetKey] = temp;
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
        let fleet = globalDriverSchedule.find(item => {
            return item.name == fleetName;
        });
        let sources = fleet.machineClasses[machineClassName - 1][type];
        let source = sources.find(item => {
            return item.id = id;
        });
        let conditions = target.split(":");
        let targetFleet = globalDriverSchedule.find(item => {
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
            renderDriverSchedule(globalDriverSchedule);
            processMachineDriverData(globalDriverSchedule);
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

        let fleet = globalDriverSchedule.find(item => {
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
            renderDriverSchedule(globalDriverSchedule);
            processMachineDriverData(globalDriverSchedule);
            renderAbsentDriverSchedule(absentDrivers);
        }
    }

    /**
     * 根据司机信息渲染界面
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

});
