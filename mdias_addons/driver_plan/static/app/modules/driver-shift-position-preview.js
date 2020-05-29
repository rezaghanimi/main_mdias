layui.use(['element', 'jquery', 'table', 'form', 'laytpl', 'api', 'layer'], function () {
    const element = layui.element;
    const table = layui.table;
    const form = layui.form;
    const laytpl = layui.laytpl;
    const $ = layui.$; //重点处
    const api = layui.api;
    let positionData = {};
    element.init();
    loadNormalRuleSelect();
    $('#backList').click(() => {
        $("#layui-content-body").load("modules/driver-shift-position-view.html");
    });
    $('#loadData').click(function () {
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
            url: api.base_url + api.driver_position.findDriverPositionById.url + '/' + localStorage.getItem("preViewId"),
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
                    renderMachineClassView(morningShiftList, 'morningShiftContainer');
                    renderMachineClassView(dayShiftList, 'dayShiftContainer');
                    renderMachineClassView(nightShiftList, 'nightShiftContainer');
                }
            },
            error: function (response) {

            }
        })
    });

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

    /**
     * 司机位置图预演分析
     */
    $("#previewAnalysis").click(function () {
        layer.open({
            type: 1,
            title: '选择预演分析规则',
            content: $('#ruleSelectTemplate').html().replace('submitTimeSchedule', 'submitTimeSchedule-copy'),
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
                    if (data.field.id) {
                        analysisDriverPosition(data.field.id);
                        layer.close(index);
                    }
                    return false;
                });
            }
        });
    });

    function analysisDriverPosition(ruleId) {
        let count = 0;
        const loadingIndex = layer.load(2, { //icon支持传入0-2
            content: '预演分析中,请耐心等待...',
            success: function (layero) {
                layero.find('.layui-layer-content').css({
                    'padding-top': '39px',
                    'width': '200px',
                    'text-align': 'center',
                    'background-position': 'top center'
                });
            }
        }); //换了种风格
        findPositionAnalyseData();
        $.ajax({
            method: api.rule.findByRuleId.type,
            url: api.base_url + api.rule.findByRuleId.url + '/' + ruleId,
            async: true,
            contentType: 'application/json',
            success: function (response) {
                count += 1;
                if (count == 2) {
                    closeLayer(loadingIndex);
                }
                if (response.success) {
                    // 渲染界面修改数据
                    let rule = JSON.parse(response.data.value);
                    let ruleMaxWorkTime = convertTimeToHour(rule.maxWorkTime);
                    let ruleMinWorkTime = convertTimeToHour(rule.minWorkTime);
                    $('#ruleMaxWorkTime').html(ruleMaxWorkTime);
                    $('#ruleMinWorkTime').html(ruleMinWorkTime);
                    $('#ruleMinRestTime').html(convertTimeToMinute(rule.minRestTime));
                    let result = findPositionAnalyseData();
                    let positionMaxWorkTime = convertTimeToHour(secondsToHms(result.maxJobTime));
                    let positionMinWorkTime = convertTimeToHour(secondsToHms(result.minJobTime));
                    $('#positionMaxWorkTime').html(positionMaxWorkTime);
                    $('#positionMinWorkTime').html(positionMinWorkTime);
                    $('#positionMinRestTime').html(convertTimeToMinute(result.minRestTime));
                    $('#maxShift').html(result.maxJobShift.typeName + result.maxJobShift.position);
                    let maxShiftTime = (positionMaxWorkTime - ruleMaxWorkTime).toFixed(1);
                    console.log(maxShiftTime);
                    $('#maxShiftTime').html(maxShiftTime);
                    $('#minShift').html(result.minJobShift.typeName + result.minJobShift.position);
                    let minShiftTime = (ruleMinWorkTime - positionMinWorkTime).toFixed(1);
                    $('#minShiftTime').html(minShiftTime);

                    $('#minRestShift').html(result.minRestShift.typeName + result.minRestShift.position);
                    let minRestPickUpTime = result.minSchedule.pickUpSchedule.arrivalTime;
                    $('#minRestPickUpTime').html(minRestPickUpTime);
                }
            },
            error: function (response) {

            }
        });
        $.ajax({
            method: api.driver_position.analysisDriverPosition.type,
            url: api.base_url + api.driver_position.analysisDriverPosition.url + '/' + localStorage.getItem("preViewId"),
            async: true,
            contentType: 'application/json',
            success: function (response) {
                count += 1;
                if (count == 2) {
                    closeLayer(loadingIndex);
                }
                if (response.success) {
                    const data = response.data;
                    console.log(data);
                    $('#positionTrains').text(data.positionTrainNos.length);
                    $('#scheduleTrains').text(data.scheduleTrainNos.length);
                    console.log(data.diff);
                    if (data.diff.length > 0) {
                        $('#missTrains').html(createTableTr(data.diff));
                    }
                }
            },
            error: function (response) {

            }
        });
    }

    /**
     * 时刻表与位置图缺失车次显示
     * @param data
     * @returns {string}
     */
    function createTableTr(data) {
        let result = '';
        data.forEach(item => {
            result += '<tr><td>' + item + '</td></tr>';
        });
        return result;
    }

    /**
     * 转换秒数为时间
     * @param d
     * @returns {string}
     */
    function secondsToHms(seconds) {
        let hours = Math.floor(seconds / 60 / 60);
        const second = seconds % 60;
        seconds -= hours * 60 * 60;
        const minutes = Math.floor(seconds / 60);

        if (hours < 0)
            hours = hours + 24;
        return (hours <= 9 ? "0" : "") + hours + ":" + (minutes <= 9 ? "0" : "") + minutes + ":" + (Math.abs(second) <= 9 ? '0' : '') + Math.abs(second);
    }

    /**
     * 转换时间为小时 例如08:30:00为8.5h
     * @param time
     * @returns {number}
     */
    function convertTimeToHour(time) {
        const times = time.split(":");
        return parseInt(times[0]) + Number((times[1] / 60).toFixed(2))
    }

    /**
     * 转换时间为分钟数 例如01:30:00为90分钟
     * @param time
     * @returns {number}
     */
    function convertTimeToMinute(time) {
        const times = time.split(":");
        return parseInt(times[0]) * 60 + parseInt(times[1]);
    }

    /**
     * 分析查找位置图时间
     */
    function findPositionAnalyseData() {
        let result = {};
        let maxJobTime = 0;
        let minJobTime = 9999999;
        let maxJobShift = {};
        let minJobShift = {};
        let minRestTime = "99:99:99";
        let minRestShift = {};
        let minSchedule = {};
        positionData.driverShifts.forEach(item => {
            if (item.jobTime > maxJobTime) {
                maxJobTime = item.jobTime;
                maxJobShift = item;
            }
            if (item.jobTime < minJobTime) {
                minJobTime = item.jobTime;
                minJobShift = item;
            }
            let size = item.dtsList.length;

            if (size > 2) {
                item.dtsList.forEach((entry, index) => {
                    if (index != 0) {
                        if (entry.restTime < minRestTime) {
                            minRestTime = entry.restTime;
                            minRestShift = item;
                            minSchedule = entry;
                        }
                    }
                })
            }
        });
        result.maxJobTime = maxJobTime;
        result.minJobTime = minJobTime;
        result.maxJobShift = maxJobShift;
        result.minJobShift = minJobShift;
        result.minRestTime = minRestTime;
        result.minRestShift = minRestShift;
        result.minSchedule = minSchedule;
        return result;
    }

    /**
     * 关闭加载提示信息 并显示预演分析结果
     * @param index
     */
    function closeLayer(index) {
        $('#analysisResult').removeClass('layui-hide');
        layer.close(index);
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

    /**
     * 渲染普通规则select
     * @param data
     */
    function renderNormalRuleSelect(data) {
        const getTpl = document.getElementById('scheduleRuleSelectTemplate').innerHTML;
        const view = document.getElementById('ruleSelect');
        view.innerHTML = '';
        laytpl(getTpl).render(data, function (html) {
            view.innerHTML = html;
        });
    }
});
