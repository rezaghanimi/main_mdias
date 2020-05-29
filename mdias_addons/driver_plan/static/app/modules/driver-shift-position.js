layui.use(['element', 'jquery', 'api', 'layer', 'steps', 'laytpl', 'form', 'layedit'], function () {
    const $ = layui.$;
    const element = layui.element;
    const api = layui.api;
    const laytpl = layui.laytpl;
    const form = layui.form;
    let resultGlobal;
    let drake = window.dragula();
    let normalRule;
    let scheduleTableId;
    let morningShiftList = [];
    let dayShiftList = [];
    let nightShiftList = [];
    let shiftData = {day: dayShiftList, morning: morningShiftList, night: nightShiftList};
    let classTypeName = {day: '白', morning: '早', night: '夜'};
    let classTypeContainer = {day: 'dayShiftContainer', morning: 'morningShiftContainer', night: 'nightShiftContainer'};
    initSteps();
    loadScheduleTable();
    loadNormalRuleSelect();
    loadExtraRuleSelect();

    /**
     * 初始化步骤条
     */
    function initSteps() {
        const $step = $("#step_demo").step();

        $("#preBtn").click(function (event) {
            $step.preStep();//上一步
        });
        $("#nextBtn").click(function (event) {
            if ($step.getCurrentPage() == 0 || $step.getCurrentPage() == 1) {
                if (!resultGlobal) {
                    layer.open({
                        type: 1
                        , id: 'layerMessage' + new Date().getTime() //防止重复弹出
                        , content: '<div style="padding: 20px 100px;">' + '请先生成司机位置图!' + '</div>'
                        , btn: '关闭'
                        , resize: false
                        , btnAlign: 'c' //按钮居中
                        , shade: 0 //不显示遮罩
                        , yes: function () {
                            layer.closeAll();
                        }
                    });
                    return;
                }
                // if (resultGlobal && resultGlobal.unAssignDtsList.length > 0) {
                //     layer.open({
                //         type: 1
                //         , id: 'layerMessage' //防止重复弹出
                //         , content: '<div style="padding: 20px 100px;">' + '存在未分配的任务!' + '</div>'
                //         , btn: '关闭'
                //         , resize: false
                //         , btnAlign: 'c' //按钮居中
                //         , shade: 0 //不显示遮罩
                //         , yes: function () {
                //             layer.closeAll();
                //         }
                //     });
                //     return;
                // }
                $step.nextStep();//下一步
            } else if ($step.getCurrentPage() == 2) {
                if (morningShiftList.length == 0 || dayShiftList.length == 0 || nightShiftList.length == 0) {
                    layer.open({
                        type: 1
                        , id: 'layerMessage' + new Date().getTime() //防止重复弹出
                        , content: '<div style="padding: 20px 100px;">' + '请处理机班分组!' + '</div>'
                        , btn: '关闭'
                        , resize: false
                        , btnAlign: 'c' //按钮居中
                        , shade: 0 //不显示遮罩
                        , yes: function () {
                            layer.closeAll();
                        }
                    });
                    return;
                }
                $step.nextStep();//下一步

            } else {

            }
        });
    }

    $('#ga').click(() => {
        layer.open({
            type: 1,
            title: '参数选择',
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
                    if (data.field.no) {
                        layer.close(index);
                        schedule(data.field);
                    }
                    return false;
                });
            }
        });
    });

    //请求生成派班数据
    function schedule(param) {
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '该步骤时间较长,请耐心等待...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '200px',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        loadNormalRuleByRuleId(param.rule);
        scheduleTableId = param.no;
        $.ajax({
            type: api.driver_position.ga.type,
            url: api.base_url + api.driver_position.ga.url + '/' + param.no,
            data: {'ruleId': param['rule']},
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    //重置所有车辆信息
                    const result = response.data;
                    const unAssignList = result.unAssignDtsList.map(function (item) {
                        let temp = [];
                        // 合并过得区间展示原有数据
                        if (item.mergedDts.length > 0) {
                            temp = temp.concat(item.mergedDts);
                            const itemTemp = _.cloneDeep(item);
                            itemTemp.mergedDts = [];
                        } else {
                            temp.push(item);
                        }
                        return temp;
                    });
                    const assignList = result.assignShiftList.map(function (item) {
                        return processAssignList(item);
                    });
                    const mixData = {};
                    mixData.unAssignDtsList = unAssignList.flat().map(function (item) {
                        item.id = uuid();
                        return item;
                    });
                    mixData.assignShiftList = assignList;
                    console.log(mixData.unAssignDtsList.length);
                    resultGlobal = mixData;
                    renderUnAssignShift();
                    renderAssignShift();
                    initDragTimeout();
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


    function processAssignList(item) {
        const tempDtsList = item.dtsList.map(function (entry) {
            let temp = [];
            // 合并过得区间展示原有数据
            if (entry.mergedDts.length > 0) {
                temp = temp.concat(entry.mergedDts);
                const entryTemp = _.cloneDeep(entry);
                entryTemp.mergedDts = [];
            } else {
                temp.push(entry);
            }
            return temp;
        });
        const itemTemp = _.cloneDeep(item);
        //数组降维
        let resultList = tempDtsList.flat();
        //根据发车时间排序
        resultList = resultList.sort(function (a, b) {
            return a.departureTime > b.departureTime ? 1 : -1;
        }).map(function (entry, index, array) {
            //处理休息时间计算
            if (index === 0 || array.length === 1) {
                entry.restTime = '00:00:00';
            } else {
                entry.restTime = diff(array[index - 1]['arrivalSchedule'].arrivalTime, entry['pickUpSchedule'].arrivalTime);
            }
            entry.id = uuid();
            return entry;
        });
        //计算工作时间
        if (resultList.length > 0) {
            itemTemp.jobTime = countJobTime(resultList[0].pickUpSchedule.arrivalTime, resultList[resultList.length - 1].arrivalSchedule.arrivalTime);
        }
        itemTemp.id = uuid();
        itemTemp.dtsList = resultList;
        //处理出勤地点和退勤地点
        if (resultList.length > 0) {
            if (resultList[0].origin) {
                itemTemp.firstDepartureStation = resultList[0].pickUpSchedule.departureStation;
            } else {
                itemTemp.firstDepartureStation = resultList[0].pickUpSchedule.arrivalStation;
            }
            itemTemp.lastArrivalStation = resultList[resultList.length - 1].arrivalStation;
        }

        return itemTemp;
    }

    function countJobTime(start, end) {
        return timeToNumber(end) - timeToNumber(start);
    }

    function timeToNumber(time) {
        const timeArray = time.split(':');
        return timeArray[0] <= 0 ? (timeArray[0] + 24) * 60 * 60 : timeArray[0] * 60 * 60 + timeArray[1] * 60 + parseInt(timeArray[2]);
    }

    /**
     * 初始化拖动插件
     */
    function initDrag() {
        if (drake) {
            drake.destroy();
        }
        const containers = document.querySelectorAll('.accept-container');
        const result = [];
        containers.forEach(item => {
            result.push(item);
        });
        result.push(document.querySelector('#left'));
        drake = dragula(result, {
            isContainer: function (el) {
                // return el.classList.contains('dragula-container');
                return false; // only elements in drake.containers will be taken into account
            },
            moves: function (el, source, handle, sibling) {
                //从左往右拖动需要处理查询
                return true
            },
            invalid: function (el, handle) {
                return false; // don't prevent any drags from initiating by default
            },
            accepts: function (el, target) {
                return valid(el, target);
            },
            direction: 'vertical',             // Y axis is considered when determining where an element would be dropped
            copy: false,                       // elements are moved by default, not copied
            copySortSource: false,             // elements in copy-source containers can be reordered
            revertOnSpill: false,              // spilling will put the element back where it was dragged from, if this is true
            removeOnSpill: false,              // spilling will `.remove` the element, if this is true
            mirrorContainer: document.body,    // set the element that gets mirror elements appended
            ignoreInputTextSelection: true
        }).on('dragend', function (el) {
            /**
             * 拖动结束处理class
             */
            const elements = $('.accept-status');
            elements.removeClass('accept-status');
            elements.removeClass('reject-status');
            const els = $('.reject-status');
            els.removeClass('accept-status');
            els.removeClass('reject-status');
            renderUnAssignShift();
            renderAssignShift();
            initDragTimeout();
        }).on('drag', function (el, source) {
            //开始拖动时查询可以接收的容器 从左边往右边
            if (document.querySelector("#left") === source) {
                findAcceptContainers(el);
            }
        }).on('drop', function (el, target, source, sibling) {
            //拖动完毕后处理数据 并重新渲染界面
            // TODO 此处由于需要渲染整个界面效率还有待优化
            //从右往左拖动处理数据方式
            if (target === document.querySelector("#left")) {
                const container = _.get(resultGlobal, $(source).attr('id'), undefined);
                if (container) {
                    const dragEl = container.dtsList.find(item => {
                        return item.id === $(el).attr('id');
                    });
                    if (dragEl) {
                        resultGlobal.unAssignDtsList.push(dragEl);
                        container.dtsList.splice(container.dtsList.indexOf(dragEl), 1);
                        let tempItem = processAssignList(container);
                        _.set(resultGlobal, $(source).attr('id'), tempItem);
                    }
                }
            } else if (source == document.querySelector("#left") && $(target).hasClass('accept-container')) {
                //从左边往右边
                //拖动完毕后处理数据
                const item = _.get(resultGlobal, $(el).attr('id'), undefined);
                const container = _.get(resultGlobal, $(target).attr('id'), undefined);
                if (item && container) {
                    container.dtsList.push(item);
                    resultGlobal.unAssignDtsList.splice(resultGlobal.unAssignDtsList.indexOf(item), 1);
                    let tempItem = processAssignList(container);
                    _.set(resultGlobal, $(target).attr('id'), tempItem);
                }
            } else {
                //左边上下拖动情况
                const item = _.get(resultGlobal, $(el).attr('id'), undefined);
                const container = _.get(resultGlobal, $(target).attr('id'), undefined);
                const fromContainer = _.get(resultGlobal, $(source).attr('id'), undefined);
                if (item && container && fromContainer) {
                    container.dtsList.push(item);
                    fromContainer.dtsList.splice(container.dtsList.indexOf(item), 1)
                    let tempItem = processAssignList(container);
                    let fromItem = processAssignList(fromContainer);
                    _.set(resultGlobal, $(target).attr('id'), tempItem);
                    _.set(resultGlobal, $(source).attr('id'), fromItem);

                }

            }
            //拖动完毕后保存数据到localStorage

        });
    }

    //
    function valid(el, target) {
        //从右边往左拖动不进行校验
        //如果目标元素是初始化容器则直接返回true
        if (document.querySelector("#left") === target) {
            $(el).addClass('accept-status');
            return true;
        }
        // 从左边往右边拖动 或者 已经分配列表中上下拖动
        const item = _.get(resultGlobal, $(el).attr('id'), undefined);
        const container = _.get(resultGlobal, $(target).attr('id'), undefined);
        //从左边往右边拖动
        if (item && container) {
            const result = container.dtsList.length == 0 ? true : container.dtsList.some((entry, index, array) => {
                if (index === array.length - 1) {
                    if ((item.pickUpSchedule.arrivalTime >= entry.arrivalSchedule.arrivalTime) &&
                        (item.arrivalSchedule.direction === -entry.arrivalSchedule.direction)) {
                        return true;
                    }
                } else if (index === 0) {
                    if ((item.arrivalSchedule.arrivalTime <= entry.pickUpSchedule.arrivalTime) &&
                        (item.arrivalSchedule.direction === -entry.arrivalSchedule.direction)) {
                        return true;
                    }
                } else {
                    if ((item.arrivalSchedule.arrivalTime < entry.pickUpSchedule.arrivalTime) &&
                        (item.arrivalSchedule.direction === -entry.arrivalSchedule.direction) && item.pickUpSchedule.arrivalTime > array[index + 1].arrivalSchedule.arrivalTime) {
                        return true;
                    }
                }
                return false;
            });
            if (result) {
                $(el).addClass('accept-status');
            } else {
                $(el).addClass('reject-status');
            }
            return result;
        }
        return false;
    }

    function findAcceptContainers(el) {
        console.log(el);
        const data = _.get(resultGlobal, $(el).attr('id'), undefined);
        if (data) {
            const acceptContainers = resultGlobal.assignShiftList.filter(item => {
                return item.dtsList.some((entry, index, array) => {
                    if (index === array.length - 1) {
                        if ((data.pickUpSchedule.arrivalTime > entry.arrivalSchedule.arrivalTime) &&
                            (data.arrivalSchedule.direction === -entry.arrivalSchedule.direction)) {
                            return true;
                        }
                    } else if (index === 0) {
                        if ((data.arrivalSchedule.arrivalTime < entry.pickUpSchedule.arrivalTime) &&
                            (data.arrivalSchedule.direction === -entry.arrivalSchedule.direction)) {
                            return true;
                        }
                    } else {
                        if ((data.arrivalSchedule.arrivalTime < entry.pickUpSchedule.arrivalTime) &&
                            (data.arrivalSchedule.direction === -entry.arrivalSchedule.direction) && data.pickUpSchedule.arrivalTime > array[index + 1].arrivalSchedule.arrivalTime) {
                            return true;
                        }
                    }
                    return false;
                })
            });
            acceptContainers.forEach(item => {
                $('#' + item.id).addClass("accept-status");
            })
        }
    }

    //渲染未分配任务
    function renderUnAssignShift() {
        const getTpl = document.getElementById('scheduleTemplate').innerHTML;
        const view = document.getElementById('left');
        view.innerHTML = '';
        laytpl(getTpl).render(resultGlobal, function (html) {
            view.innerHTML = html;
        });
    }

    //渲染已分配任务
    function renderAssignShift() {
        const getTpl = document.getElementById('assignScheduleTemplate').innerHTML;
        const view = document.getElementById('assignScheduleContainer');
        view.innerHTML = '';
        laytpl(getTpl).render(resultGlobal, function (html) {
            view.innerHTML = html;
        });
    }

    // 延时初始化拖动插件
    function initDragTimeout() {
        setTimeout(() => {
            initDrag();
        }, 1);
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

    /**
     * 生成uuid
     * @returns {string}
     */
    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
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

    //处理新增机班数据
    $('#addContainers').click(() => {
        addAssignShift();
    });

    function addAssignShift() {
        if (resultGlobal) {
            const loadingIndex = layer.load(2); //换了种风格
            const tempShift = {
                driverTime: null,
                dtsList: [],
                firstDepartureStation: "",
                firstDepartureTime: 0,
                jobTime: 0,
                lastArrivalStation: "",
                lastArrivalTime: 0,
                position: 0,
                id: uuid()
            };
            resultGlobal.assignShiftList.push(tempShift);
            renderAssignShift();
            initDragTimeout();
            layer.close(loadingIndex);
        }
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
     *表单代码
     */
    //监听提交
    form.on('submit(position-schedule)', function (data) {
        console.log(data.field);
        let shifts = [];
        Object.keys(shiftData).forEach(item => {
            shifts = shifts.concat(shiftData[item]);
        });
        console.log(shifts);
        const post = {};
        post.driverPosition = data.field;
        post.driverPosition.circleModel = normalRule.circleModel;
        post.driverPosition.scheduleTableNo = scheduleTableId;
        post.driverShifts = shifts;
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '该步骤时间较长,请耐心等待...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '200px',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        $.ajax({
            method: api.driver_position.save.type,
            url: api.base_url + api.driver_position.save.url,
            data: JSON.stringify(post),
            async: true,
            contentType: 'application/json',
            success: function (response) {
                layer.close(loadingIndex);
                if (response.success) {
                    layer.msg('操作成功', {
                        icon: 1,
                        time: 2000 //2秒关闭（如果不配置，默认是3秒）
                    }, function () {
                        $("#layui-content-body").load("modules/driver-shift-position-view.html");
                    });
                }
            },
            error: function (response) {

            }
        });
        return false;
    });

    // 处理时刻表选择
    function loadScheduleTable() {
        $.ajax({
            method: api.train_schedule.list_all_table.type,
            url: api.base_url + api.train_schedule.list_all_table.url,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    const scheduleNos = response.data.map(item => {
                        return {id: item.id, no: item.scheduleNo};
                    });
                    renderScheduleNoSelect(scheduleNos);
                }
            },
            error: function (response) {

            }
        });
    }

    //处理普通规则选择
    function loadNormalRuleSelect() {
        $.ajax({
            method: api.rule.findAllNormalRules.type,
            url: api.base_url + api.rule.findAllNormalRules.url,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    const rules = response.data.map(item => {
                        return {id: item.id, name: item.name};
                    });
                    renderNormalRuleSelect(rules);
                }
            },
            error: function (response) {

            }
        });
    }

    //处理补充规则选择
    function loadExtraRuleSelect() {
        $.ajax({
            method: api.rule.findAllExtraRules.type,
            url: api.base_url + api.rule.findAllExtraRules.url,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    const rules = response.data.map(item => {
                        return {id: item.id, name: item.name};
                    });
                    renderExtraRuleSelect(rules);
                }
            },
            error: function (response) {

            }
        });
    }

    function renderScheduleNoSelect(data) {
        const getTpl = document.getElementById('scheduleNoSelectTemplate').innerHTML;
        const view = document.getElementById('scheduleNoSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    function renderNormalRuleSelect(data) {
        const getTpl = document.getElementById('scheduleRuleSelectTemplate').innerHTML;
        const view = document.getElementById('ruleSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    function renderExtraRuleSelect(data) {
        const getTpl = document.getElementById('scheduleExtraRuleSelectTemplate').innerHTML;
        const view = document.getElementById('extraSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }

    // step2 处理白班夜班早班分组
    $('#processShift').click(() => {
        layer.open({
            type: 1,
            title: '补充规则选择',
            content: $('#scheduleClassEdit').html().replace('submitExtraRule', 'submitExtraRule-copy'),
            resize: false,
            btn: ['提交', '取消'],
            btnAlign: "r",
            area: ['530px', '500px'],
            yes: function (index, layero) {//保存按钮
                $('#submitExtraRule-copy').click();
            },
            btn2: function (index, layero) {//取消按钮
            },
            success: function (layero, index) {
                form.render();
                form.on('submit(extra-rule-select)', function (data) {
                    if (data.field) {
                        console.log(data.field);
                        layer.close(index);
                        const extraRule = data.field.extraRule;
                        console.log(normalRule);
                        if (extraRule != undefined && extraRule != null && extraRule != '') {
                        }
                        if (normalRule) {
                            const loadingIndex = layer.load(2, { //icon支持传入0-2
                                content: '机班分组处理中...',
                                success: function (layero) {
                                    layero.find('.layui-layer-content').css({
                                        'padding-top': '39px',
                                        'width': '150px',
                                        'background-position': 'top center'
                                    });
                                }
                            }); //换了种风格
                            processMachineClassType();
                            layer.close(loadingIndex);
                        }
                    }
                    return false;
                });
            }
        });
    });

    /**
     * 根据规则划分白夜早班数据
     */
    function processMachineClassType() {
        if (normalRule && resultGlobal) {
            //白班时间段
            const dayShiftEndTime = normalRule.dayShiftEndTime;
            const dayShiftStartTime = normalRule.dayShiftStartTime;
            //早班时间段
            const morningShiftEndTime = normalRule.morningShiftEndTime;
            const morningShiftStartTime = normalRule.morningShiftStartTime;
            //夜班时间段
            const nightShiftEndTime = normalRule.nightShiftEndTime;
            const nightShiftStartTime = normalRule.nightShiftStartTime;
            //处理新增空白机班
            resultGlobal.assignShiftList = resultGlobal.assignShiftList.filter(item => {
                return item.dtsList.length > 0;
            });
            morningShiftList = [];
            dayShiftList = [];
            nightShiftList = [];
            resultGlobal.assignShiftList.forEach(item => {
                if (item.dtsList[0].pickUpSchedule.departureTime < morningShiftEndTime) {
                    item.type = 'morning';
                    item.typeName = '早';
                    morningShiftList.push(item);
                    return;
                }
                if (item.dtsList[0].pickUpSchedule.departureTime < dayShiftEndTime) {
                    item.type = 'day';
                    item.typeName = '白';
                    dayShiftList.push(item);
                    return;
                }
                item.type = 'night';
                item.typeName = '夜';
                nightShiftList.push(item);
            });
            /**
             * 处理机班位置
             */
            dayShiftList.forEach((item, index) => {
                item.position = index + 1;
            });
            morningShiftList.forEach((item, index) => {
                item.position = index + 1;
            });
            nightShiftList.forEach((item, index) => {
                item.position = index + 1;
            });
            shiftData = {day: dayShiftList, morning: morningShiftList, night: nightShiftList};
            renderMachineClassView(morningShiftList, 'morningShiftContainer');
            renderMachineClassView(dayShiftList, 'dayShiftContainer');
            renderMachineClassView(nightShiftList, 'nightShiftContainer');
            form.render();
            /**
             * 监听班组类型切换
             */
            form.on('select(classType)', function (data) {
                const loadingIndex = layer.load(2, { //icon支持传入0-2
                    content: '数据处理中...',
                    success: function (layero) {
                        layero.find('.layui-layer-content').css({
                            'padding-top': '39px',
                            'width': '100px',
                            'text-align': 'center',
                            'background-position': 'top center'
                        });
                    }
                }); //换了种风格
                classTypeSelectChange(data);
                layer.close(loadingIndex);
            });
        } else {
            layer.msg('处理机班分组失败,规则信息不存在', {
                icon: 5,
                time: 2000 //2秒关闭（如果不配置，默认是3秒）
            }, function () {
            });
        }
    }

    function classTypeSelectChange(data) {
        const id = $(data.elem).parents('table').attr('id');
        const type = $(data.elem).parents('table').attr('data-type');
        if (data.value != undefined && data.value != null && data.value != type) {
            const resource = shiftData[type].find(item => {
                return item.id == id;
            });
            if (resource) {
                shiftData[type].splice(shiftData[type].indexOf(resource), 1);
                shiftData[type].sort(function (a, b) {
                    return a.departureTime > b.departureTime ? 1 : -1;
                }).forEach((item, index) => {
                    item.position = index + 1;
                });
                resource.type = data.value;
                resource.typeName = classTypeName[data.value];
                shiftData[data.value].push(resource);
                shiftData[data.value].sort(function (a, b) {
                    return a.departureTime > b.departureTime ? 1 : -1;
                }).forEach((item, index) => {
                    item.position = index + 1;
                });
                renderMachineClassView(shiftData[type], classTypeContainer[type]);
                renderMachineClassView(shiftData[data.value], classTypeContainer[data.value]);
                //渲染后初始化
                form.render();
                /**
                 * 监听班组类型切换
                 */
                form.on('select(classType)', function (data) {
                    const loadingIndex = layer.load(2, { //icon支持传入0-2
                        content: '数据处理中...',
                        success: function (layero) {
                            layero.find('.layui-layer-content').css({
                                'padding-top': '39px',
                                'width': '100px',
                                'text-align': 'center',
                                'background-position': 'top center'
                            });
                        }
                    }); //换了种风格
                    classTypeSelectChange(data);
                    layer.close(loadingIndex);
                });
            }
        }
    }

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


    /**
     * 选择完毕普通规则后加载规则属性 方便在第二步的时候处理数据
     * @param ruleId
     */
    function loadNormalRuleByRuleId(ruleId) {
        $.ajax({
            method: api.rule.findByRuleId.type,
            url: api.base_url + api.rule.findByRuleId.url + '/' + ruleId,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                if (response.success) {
                    normalRule = JSON.parse(response.data.value);
                }
            },
            error: function (response) {

            }
        });
    }

    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-position-view.html");
    });
});
