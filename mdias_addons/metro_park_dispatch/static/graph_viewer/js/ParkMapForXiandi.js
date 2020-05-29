/**
 * 通过option传入相关数据
 */
ParkMapForXiandi = function (editorUi, netWork, options) {
    mxEventSource.call(this);

    this.editorUi = editorUi;

    this.editor = this.editorUi.editor;
    this.graph = this.editor.graph;
    this.model = this.graph.model
    this.netWork = netWork

    this.frontState = 1;
    this.interLockState = 1

    this.sysBlackout = false
    this.breakStatistics = []
    this.mdiasControl = false
    this.selfControlPlan = false
    this.planFrameReady = false
    this.popId = 0

    this.gloabalUpdate = false;
    this.location = options.location || undefined
    this.disableOperation = options.disableOperation || false

    // 按扭表
    this.buttonTableData = options.buttonTable || []
    this.buttonTable = this.parseButtonTable()

    // 道岔区段对应表
    this.switchBelongSec = options.switchBelongSec || []
    // 底部按扭
    this.bottomButton = options.bottomButton || []

    this.oldColorCache = {};
    this.parkElementCache = {};
    this.alarmStatusCache = {};
    this.oldFillColorCache = {};
    this.specialColorCache = {};
    this.switchCrowCache = {};
    this.signalAlarmCache = {};
    this.flashCells = new Set();
    this.delayCountingInfo = {}
    this.busyInfos = {}

    // 命令相关
    this.clickPath = []; // 历史点击
    this.startTime = null
    this.status = 0
    this.actionMark = null

    // 是否位上电解锁状态,用以处理光带的颜色显示
    this.sdjs = 0

    // 列车相关
    this.trainCache = {}; // 记录uid和train的对应
    this.trainInfoCache = {};
    this.trainOnTop = true
    this.uidTrainCache = {} // 记录uid对应的train

    // busy icons 
    this.busyIconsCache = {}

    this.buton_type_status_map = {
        'la': 1, // 列车进路
        'da': 2, // 调车进路
        'ya': 3 // 引导进路
    };

    this.statusMap = {
        'all_cancel': 4, // 进路取消
        'all_relieve': 5, // 总人解
        'switch_direct': 6, // 道岔总定
        'switch_reverse': 7, // 道岔总反
        'switch_lock': 8, // 道岔单锁
        'switch_unlock': 9, // 道岔单解
        'switch_block': 10, // 道岔封锁
        'switch_unblock': 11, // 道岔解封
        // 'allcancel': 12,// 进路人解
        'sector_fault_unlock': 13, // 区段故障解锁
        'all_lock': 14, // 引导总锁
        'signal_block': 15, // 按钮封闭
        'signal_unblock': 16, // 按钮解封
        'guide_road': 18, // 引导进路办理
        'guide_open': 19, // 开放引导,
        'another_road_way': 20 // 变通进路
    };

    this.operationName = [
        "",
        "列车进路",
        "调车进路",
        "引导进路",
        "进路取消",
        "总人解",
        "道岔总定",
        "道岔总反",
        "道岔单锁",
        "道岔单解",
        "道岔封锁",
        "道岔解封",
        "进路人解",
        "区故解",
        "引导总锁",
        "按钮封锁",
        "按钮解封",
        "",
        "引导进路办理",
        "开放引导",
        "变通进路"
    ];
    this.pre_button = {}

    // 隐藏道岔名称
    this.hideSwitchName = false
    // 隐藏道岔区段名称
    this.hideSwitchSectionName = false
    // 隐藏信号机名称
    this.hideSignalName = false
    // 隐藏区段名称
    this.hideSectionName = false
    // 隐藏道岔位置
    this.hideSwitchPosition = false
    // 显示光带
    this.showLightBelt = false
    // 手动确认路由，调车计划的信息窗口
    this.manualConfirmPlan = true

    // 颜色配置, 区段
    this.railColors = {
        blue: '#5578b6',
        white: '#FFFFFF',
        red: '#FF0000',
        pink: '#ff939'
    }

    // 道岔颜色
    this.switchColors = {
        blue: '#5578b6',
        yellow: '#FFFF00',
        white: '#fff',
        red: '#f00'
    }

    // 列车选项
    this.train_carriage_width = 37
    this.train_carriage_height = 24

    this.train_head_width = 17
    this.train_head_height = 24

    this.train_tail_width = 17
    this.train_tail_height = 24

    this.busy_icon_width = 32
    this.busy_icon_height = 32

    this.editor.graph.getRubberband().setEnabled(false)
    this.editor.graph.setCellsSelectable(false);
    this.editor.graph.setCellsLocked(true);
    this.editor.graph.setCellsMovable(false)
    this.editor.graph.setCellsEditable(false)
    this.editor.graph.setConnectable(false);
    this.editor.graph.setTooltips(false);
    this.editor.graph.setPanning(false);

    this.graph.gridEnabled = false;
    this.graph.setTooltips(false);

    this.init();

    // 网络连接成功时加载现车信息
    var self = this;
    netWork.addListener('socketio_connected', function () {
        self.initBusyIcons();
    })

    // cef 操作
    this.operation = new CefOperation()

    // 键盘
    this.keybaord = new Keyboard(this, this.editorUi)

    // 初始化操作
    if (!this.disableOperation) {
        this.initParkElementClick()
    }

    // 初始化菜单动作
    this.initMenuActions()

    // 处理鼠标
    this.hookGetCursorForCell();

    // 延迟闪烁
    setInterval(() => {
        this.DoFlashCells()
    }, 1000);
};

mxUtils.extend(ParkMapForXiandi, mxEventSource);

ParkMapForXiandi.prototype.initMenuActions = function () {
    var self = this
    // 占线板删除
    this.editor.graph.addListener('delete_busy_icon', function (sender, event) {
        var cell = event.getProperty('cell')
        var busyType = cell.getAttribute("busy_type")
        var uid = cell.getAttribute('position');
        self.netWork.call_server_method(
            'metro_park_base.busy_board',
            'set_busy_icon_status', {
                location_alias: self.location,
                uid: uid,
                busy_types: [busyType],
                operation: 'del'
            }).then(function () {
            self.graph.removeCells([cell])
        })
    })

    // 删除列车
    this.editor.graph.addListener('delete_train_carriage', function (sender, event) {
        var cell = event.getProperty('cell')
        var train_no = cell.getAttribute('train_no')
        self.netWork.call_server_method(
            'metro_park_dispatch.cur_train_manage',
            'remove_train_position', {
                "train_no": train_no
            }).then(function (res) {
            if (res == 'success') {
                self.removeCarriage(train_no)
            }
        })
    })
}

ParkMapForXiandi.prototype.parseButtonTable = function () {
    return this.buttonTableData.map((data) => {
        var ar = data.split('=')
        return {
            "name": _.trim(ar[1]),
            "index": _.trim(ar[0]),
            "type": _.trim(ar[2])
        }
    })
}

ParkMapForXiandi.prototype.hookGetCursorForCell = function () {
    var getCursorForCell = this.graph.getCursorForCell;
    this.graph.getCursorForCell = function (cell) {
        var name = cell.getAttribute('name')
        if (name == 'button' ||
            name == 'light' ||
            name == 'road' ||
            name == 'boundary' ||
            name == 'direct' ||
            name == 'reverse') {
            return 'pointer'
        }

        // 区故解道岔区段也可点击
        if (cell.getAttribute('belongsector')) {
            return 'pointer'
        }

        return getCursorForCell.apply(this, arguments);
    };
}

/**
 * 元素点击事件
 */
ParkMapForXiandi.prototype.initParkElementClick = function () {

    var self = this
    // 监听点击事件
    this.editor.graph.addListener(mxEvent.CLICK, function (sender, evt) {

        if (!self.mdiasControl) {
            return
        }

        var event = evt.getProperty('event')
        var cell = evt.getProperty('cell');
        if (!cell) {
            return
        }

        var parkElement = cell.getParkElement()
        if (parkElement) {
            // 获取点击按钮的联锁index
            var uindex =
                cell.getAttribute('button_index') ?
                cell.getAttribute('button_index') :
                parkElement.getAttribute('button_index')
            var uindex2 =
                cell.getAttribute('button_index2') ?
                cell.getAttribute('button_index2') :
                parkElement.getAttribute('button_index2')

            // 特殊控制模式按钮
            if (parkElement.getAttribute('type') == 'selfcontrolplan') {
                var func = _.bind(self.onSelfControlClick, self)
                if (parkElement.getAttribute('uid') == '自控模式') {
                    func(true);
                } else {
                    func(false);
                }
                return
            }

            // 特殊按钮处理
            if (parkElement.value.getAttribute('type') == 'BTN') {
                // 获取btntype
                if (parkElement.getAttribute('btntype') == 'confirm') { // 非进路
                    self.onConfirmClick(parkElement, uindex, event.target)
                } else if (parkElement.getAttribute('btntype') == 'password') { // 非进路故障解锁1
                    self.keybaord.setPosition(event.target)
                    self.status = 110
                    self.keybaord.reveal(function () {
                        self.status = 0
                        self.buttonClick({
                            cell: parkElement,
                        }, {
                            type: 'BTN',
                            uindex: uindex,
                            name: parkElement.elementStatus.name
                        }, event.target)
                    })
                }
                return
            }

            // 点击到按钮展示覆盖物时, 注意这里是原始点击的cell, 而不是parkElement
            if (cell.getAttribute('name') == 'fork') {
                parkElement.getSubCell('button').map(tmpCell => {
                    if (tmpCell.getAttribute('type') &&
                        tmpCell.getAttribute('type').toUpperCase() ==
                        cell.getAttribute('type').toUpperCase()) {
                        uindex = tmpCell.getAttribute('button_index')
                    }
                })
            }

            // 点击到boundary的情况
            if (cell.getAttribute('name') == 'boundary') {
                parkElement.getSubCell('light').map(tmpCell => {
                    if (tmpCell.getAttribute('type') &&
                        tmpCell.getAttribute('type').toUpperCase() ==
                        cell.getAttribute('type').toUpperCase()) {
                        uindex = tmpCell.getAttribute('button_index')
                    }
                })
            }

            // 如果是道岔区段和道岔
            var belongSectors = false
            var cqid = 0
            for (var item in self.switchBelongSec) {
                if (self.switchBelongSec[item].includes(
                        Number(self.getCellUid(cell)))) {
                    belongSectors = true
                    cqid = item
                    break
                }
            }

            if (belongSectors) {
                //如果是道岔
                let item = _.find(self.buttonTable, (item) => {
                    return item.name == cqid;
                })

                self.buttonClick({
                    cell: parkElement,
                    type: parkElement.getAttribute('type')
                }, {
                    name: cell.getAttribute('name'),
                    uindex: uindex,
                    type: cell.getAttribute('type')
                }, event.target)

                self.buttonClick({
                    cell: null,
                    type: 'cq',
                    name: cqid
                }, {
                    name: cell.getAttribute('name'),
                    uindex: item ? item.index : -1,
                    type: cell.getAttribute('type')
                }, event.target)

                return
            }

            self.buttonClick({
                cell: parkElement,
                type: parkElement.getAttribute('type')
            }, {
                name: cell.getAttribute('name'),
                uindex: uindex,
                type: cell.getAttribute('type'),
                uindex2: uindex2
            }, event.target)
        }

        // 点击道岔区段label
        if (cell.getAttribute('belongsector')) {
            var parkElement = cell.getParkElement()
            var cqindex = -1
            var tmp_name = cell.getAttribute('belongsector').toLowerCase()
            var item = _.find(self.buttonTable, (item) => {
                return item.name.toLowerCase() == tmp_name
            })

            if (item) {
                cqindex = item.index
            }

            self.buttonClick({
                cell: parkElement,
                type: 'cq',
                name: cell.getAttribute('belongsector')
            }, {
                name: cell.getAttribute('name'),
                uindex: cqindex,
                type: cell.getAttribute('type')
            }, event.target)
        }
    });
}

// 获取cell
ParkMapForXiandi.prototype.getCellUid = function (cell) {
    if (cell.getAttribute('uid')) {
        return cell.getAttribute('uid')
    } else {
        if (cell.parent != null) {
            return this.getCellUid(cell.parent)
        } else {
            return null
        }
    }
}

/**
 * 确定按扭点击
 */
ParkMapForXiandi.prototype.onConfirmClick = function (parkElement, uindex, eventTarget) {
    var self = this
    pop.confirm({
        title: "提示",
        sizeAdapt: false,
        content: parkElement.elementStatus.light == 0 ? "请确定是否按下按钮！" : "请确定是否抬起按钮！",
        button: [
            ["success", "确定",
                function (e) {
                    pop.close(e)
                    self.buttonClick({
                        cell: parkElement,
                    }, {
                        type: 'BTN',
                        uindex: uindex,
                        name: parkElement.elementStatus.name
                    }, eventTarget)
                }
            ],
            ["default", "取消",
                function (e) {
                    pop.close(e)
                }
            ]
        ],
        buttonSpcl: "",
        anim: "fadeIn-zoom",
        width: 450,
        height: 180,
        id: 'mdias_pop_' + this.pop++,
        place: 5,
        drag: true,
        index: true,
        toClose: true,
        mask: true,
        class: false
    });
}

/**
 * 自控模式点击
 */
ParkMapForXiandi.prototype.onSelfControlClick = function (bSelfControl) {
    if (this.disableOperation) {
        return
    }
    var self = this
    if (bSelfControl) {
        pop.confirm({
            title: "提示",
            sizeAdapt: false,
            content: "请确定是否切换到自控模式",
            button: [
                ["success", "确定",
                    function (event) {
                        pop.close(event)
                        self.selfControlPlan = true

                        // 发送信息给联锁
                        self.operation.cef_send_sub({
                            type: "setPlanControl",
                            selfcontrolplan: true,
                            mdiasControl: self.mdiasControl
                        })

                        var cell = self.parkElementCache['集控模式']
                        var button = cell.getSubCell('button')[0]
                        self.setFillColor(button, '#ffd966')
                        var light = cell.getSubCell('light')[0]
                        self.setFillColor(light, '#000')

                        // 设置集控模式按扭
                        var cell2 = self.parkElementCache['自控模式']
                        var button2 = cell2.getSubCell('button')[0]
                        self.setFillColor(button2, '#ffd966')
                        var light2 = cell2.getSubCell('light')[0]
                        if (light2.getAttribute('name') != 'light') {
                            console.log('find sub control error', light2.getAttribute('name'))
                        }
                        self.setFillColor(light2, '#0f0')
                    }
                ],
                ["default", "取消",
                    function (e) {
                        pop.close(e)
                    }
                ]
            ],
            buttonSpcl: "",
            anim: "fadeIn-zoom",
            width: 450,
            height: 180,
            id: "random-72160",
            place: 5,
            drag: true,
            index: true,
            toClose: true,
            mask: true,
            class: false
        });
    } else {
        pop.confirm({
            title: "提示",
            sizeAdapt: false,
            content: "请确定是否切换到集控模式",
            button: [
                ["success", "确定",
                    function (event) {
                        pop.close(event)
                        self.selfControlPlan = false
                        self.operation.cef_send_sub({
                            type: "setPlanControl",
                            selfcontrolplan: false,
                            mdiasControl: self.mdiasControl
                        })
                        var cell = self.parkElementCache['集控模式']
                        var light = cell.getSubCell('button')[0]
                        self.setFillColor(light, '#ffd966')
                        // 设置灯为绿色
                        light = cell.getSubCell('light')[0]
                        self.setFillColor(light, '#0f0')

                        var cell2 = self.parkElementCache['自控模式']
                        var button2 = cell2.getSubCell('button')[0]
                        self.setFillColor(button2, '#ffd966')
                        // 设置灯为黑色
                        var light2 = cell2.getSubCell('light')[0]
                        self.setFillColor(light2, '#000')
                    }
                ],
                ["default", "取消",
                    function (e) {
                        pop.close(e)
                    }
                ]
            ],
            buttonSpcl: "",
            anim: "fadeIn-zoom",
            width: 450,
            height: 180,
            id: "random-72160",
            place: 5,
            drag: true,
            index: true,
            toClose: true,
            mask: true,
            class: false
        });
    }
};

ParkMapForXiandi.prototype.init = function () {
    var self = this;

    // 移除cell
    this.graph.addListener(mxEvent.CELLS_REMOVED, function (sender, evt) {
        var cells = evt.getProperty('cells');
        for (var index = 0; index < cells.length; index++) {
            var cell = cells[index]
            var id = cell.getId()
            var type = cell.getAttribute('type')
            if (type == 'train_body') {
                var position = cell.getAttribute('position')
                if (position in self.uidTrainCache) {
                    var train_uids = self.uidTrainCache[position]
                    train_uids = _.without(train_uids, id)
                    self.uidTrainCache[position] = train_uids
                }
                delete self.trainCache[id]
            } else if (type == 'busy_icon') {
                var busyType = cell.getAttribute('busy_type')
                var uid = cell.getAttribute('position')
                var oldInfos = self.busyInfos[uid] || []
                delete oldInfos[busyType]
                self.busyInfos[uid] = oldInfos
                delete self.busyIconsCache[id]
            } else if (type == 'train_carriage') {
                var train_no = cell.getAttribute('train_no')
                delete self.trainInfoCache[train_no]
            }
        }
    })

    // 监听添加组件
    this.graph.addListener(mxEvent.CELLS_ADDED, function (sender, evt) {
        var cells = evt.getProperty('cells');

        for (var index = 0; index < cells.length; index++) {
            var cell = cells[index]
            var uid = cell.getAttribute('uid')
            if (uid) {

                // 如果发现uid属性则加入全局存放
                self.parkElementCache[uid] = cell
                uid = uid.toUpperCase()

                if (uid.indexOf('BTN') > -1) {
                    uid = uid.split('BTN')[0]
                }

                // 给所有的站场元素添加button_index
                _.find(self.buttonTable, (tableItem) => {

                    var index = tableItem.index
                    var name = tableItem.name
                    var itemType = tableItem.type

                    if (name == uid) {

                        if (cell.getAttribute('type') == 'BTN') {
                            cell.setAttribute('button_index', index)
                            return true
                        }

                        if (cell.getSubCell('light').length == 0 &&
                            cell.getSubCell('button').length == 0) {
                            cell.setAttribute('button_index', index)
                            return true
                        }

                        cell.getSubCell('light').map(light => {
                            var tmpType = light.getAttribute('type')
                            if (tmpType && tmpType.toUpperCase() == itemType) {
                                light.setAttribute('button_index', index)
                                return true
                            }
                        })

                        cell.getSubCell('button').map(button => {
                            var tmpType = button.getAttribute('type')
                            if (tmpType && tmpType.toUpperCase() == itemType) {
                                button.setAttribute('button_index', index)
                                return true
                            }
                        })
                    }

                    return false
                })
            }

            // 保存道岔区段label
            var attr = cell.getAttribute('belongsector')
            if (attr && !cell.children) {
                self.parkElementCache[attr.toLowerCase()] = cell
            }
        }
    });

    // 设置车辆cell样式
    this.initTrainStyle();

    // 初始化占线板设置
    this.initBusyIconStyle();
}

// 计时函数
ParkMapForXiandi.prototype.startCounting = function () {
    var self = this

    this.startTime = Date.now()
    var actionMark = Math.random()
    this.actionMark = actionMark

    // 操作倒计时
    var tmpId, countingFunc = () => {
        if (this.actionMark != actionMark) {
            clearInterval(tmpId)
            this.fireEvent(new mxEventObject('countingDown', 'html', '空闲'));
            return
        }
        var htmlText = '操作剩余时间：<span style="color:red">' +
            Math.ceil((15000 - (Date.now() - this.startTime)) / 1000) + 's</span>'
        this.fireEvent(new mxEventObject('countingDown', 'html', htmlText));
    }
    countingFunc()
    tmpId = setInterval(countingFunc, 800);

    // 15s未操作，重置为空闲状态
    setTimeout(function () {
        if (self.actionMark != actionMark) return
        if (Object.keys(self.pre_button).length) {
            self.pre_button = {}
        }
        self.resetStatus()
    }, 15000)
}

/**
 * 设置全局状态
 */
ParkMapForXiandi.prototype.setGlobalState = function (state) {

    if (!state) {
        return
    }

    // if (state.data.length) {
    //     console.log('收到数据:', state.data)
    // }

    if (['DATA_SDI', 'DATA_SDCI'].includes(state['data_type'])) {
        let sdjs_item = _.find(state.data, (item) => {
            return item.type == 6 && item.name == "SDJS"
        })
        if (sdjs_item) {
            this.sdjs = sdjs_item.light
        }

        this.gloabalUpdate = true
        this.graph.model.beginUpdate();

        try {
            var elementStatuses = state.data
            elementStatuses.map((status) => {
                status.name = status.name.toUpperCase()
                var uid = status.name

                // 不在graph上的dom控制，位于下方的按钮, 那应当给toolbar去处理下吧
                if (uid == this.bottomButton.name ||
                    uid == this.bottomButton.name + 'BTN') {
                    if (status.light) {
                        this.fireEvent(
                            new mxEventObject('update_bottom_btn_style', 'css', {
                                background: "#E7BA28",
                                color: "red"
                            }, 'status', status));
                    } else {
                        this.fireEvent(
                            new mxEventObject('update_bottom_btn_style', 'css', 'color:red', 'status', status));
                        $('body').trigger('click')
                    }
                    return
                }

                if (!this.parkElementCache[uid]) {
                    // console.error('不合法名称：', status.name)
                    return
                }

                switch (status.type) {

                    case 1: // 道岔
                        this.setSwitchStatus(status.name, status)
                        break

                    case 2: // 区段
                        this.setRailSecStatus(status.name, status)
                        break

                    case 3: // 出站信号
                    case 4: // 进站信号
                    case 5: // 调车信号
                        this.setSignalStatus(status.name, status)
                        break

                    case 6: // 信号灯
                        this.setLightStatus(status.name, status)
                        break

                    case 8: // 报警
                        if (!uid in this.alarmStatusCache) {
                            this.alarmStatusCache[uid] = 0
                        }
                        if (status.value) {
                            if (!this.alarmStatusCache[uid]) {
                                this.alarmStatusCache[uid] = true
                                this.fireEvent(new mxEventObject(
                                    'add_interlock_alarm', 'msg', uid + '报警!'));
                            }
                        } else {
                            // 取消报警
                            if (this.alarmStatusCache[uid]) {
                                this.alarmStatusCache[uid] = false
                                this.fireEvent(
                                    new mxEventObject('add_interlock_alarm', 'msg', uid + '恢复!'));
                            }
                        }
                        break;
                }
            })
        } finally {
            this.graph.model.endUpdate();
            this.gloabalUpdate = false
        }
    }

    // 处理故障
    else if (['DATA_FIR'].includes(state['data_type'])) {

        /*
         *  故障信息报告帧
         */
        // struct FIR_NODE {
        //     BYTE op_code;           // 操作号
        //     BYTE notice_code;       // 提示信息代码
        //     WORD equip_code;        // 设备号
        //     BYTE equip_property;    // 设备性质
        //     BYTE revered;           // 预留
        // };
        // state.data.equip_code
        // $('#signalname').html('')

        return

        var element = null
        for (var element in this.parkElementCache) {
            if (this.parkElementCache[element].elementStatus &&
                this.parkElementCache[element].elementStatus.index == state.data.equip_code) {
                element = this.parkElementCache[element]
            }
        }

        var elementTypes = [{
            type: 0x55,
            name: '列车信号'
        }, {
            type: 0xaa,
            name: '调车信号'
        }, {
            type: 0x1F,
            name: '道岔'
        }, {
            type: 0x1E,
            name: '区段'
        }, {
            type: 0x21,
            name: '非进路调车'
        }, {
            type: 0xA5,
            name: '按钮'
        }]

        var elementType = elementTypes.find(p => {
            return p.type == state.data.equip_property
        })

        var infos = [
            '',
            '进路选不出',
            '信号不能保持',
            '命令不能执行',
            '信号不能开放',
            '灯丝断丝',
            '2灯丝断丝',
            '操作错误',
            '操作无效',
            '不能自动解锁',
            '进路不能闭锁'
        ]
        var msg = elementType.name + element.elementStatus.name + infos[state.data.notice_code]
        this.fireEvent(new mxEventObject('add_warning', 'msg', msg));
    }

    // 处理状态
    else if (['DATA_RSR'].includes(state['data_type'])) {

        // 运行状态报告帧
        // struct RSR_NODE {
        //     BYTE server_status //主备机;
        //     BYTE control_status 站控非站控;
        // };

        if (state.data.server_status == 0x55) {} else if (state.data.server_status == 0xaa) {}

        if (state.data.control_status == 0x55) {

            // 自律控制绿色
            var cell = this.parkElementCache['自律控制']
            var light = cell.getSubCell('light')[0]

            this.setFillColor(light, '#0f0')
            this.mdiasControl = true

            cell = this.parkElementCache['集控模式']
            var light = cell.getSubCell('button')[0]

            this.setFillColor(light, '#ffd966')
            light = cell.getSubCell('light')[0]

            cell = this.parkElementCache['自控模式']
            light1 = cell.getSubCell('button')[0]

            this.setFillColor(light, '#ffd966')
            light2 = cell.getSubCell('light')[0]

            if (this.selfControlPlan) {
                this.setFillColor(light1, '#000')
                this.setFillColor(light2, '#0f0')
            } else {
                this.setFillColor(light1, '#0f0')
                this.setFillColor(light2, '#000')
            }
        } else if (state.data.control_status == 0xaa) {

            // 自律控制灭灯
            var cell = this.parkElementCache['自律控制']
            var light = cell.getSubCell('light')[0]

            this.setFillColor(light, '#000')
            this.mdiasControl = false

            cell = this.parkElementCache['集控模式']
            var light = cell.getSubCell('button')[0]
            this.setFillColor(light, '#b3b3b3')

            light = cell.getSubCell('light')[0]
            this.setFillColor(light, '#000')

            var cell2 = this.parkElementCache['自控模式']
            var light2 = cell2.getSubCell('button')[0]

            this.setFillColor(light2, '#b3b3b3')

            light2 = cell2.getSubCell('light')[0]
            this.setFillColor(light2, '#000')
        }

        // 设置控制状态
        if (!this.disableOperation) {
            this.operation.cef_send_sub({
                type: "setPlanControl",
                selfcontrolplan: this.selfControlPlan,
                mdiasControl: this.mdiasControl
            })
        }
    }

    // 通信状态
    else if (['DATA_NETINFO'].includes(state['data_type'])) {
        if (state.data.type) { // 联锁
            this.interLockState = state.data.status;
            if (state.data.status == 1) {
                var cell = this.parkElementCache['允许MDIAS控']
                var light = cell.getSubCell('light')[0]
                this.setFillColor(light, '#000')
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', 'MDIAS与现地通信中断!'))
            } else if (state.data.status == 0) {
                var cell = this.parkElementCache['允许MDIAS控']
                var light = cell.getSubCell('light')[0]
                this.setFillColor(light, '#0f0')
                if (this.frontState == 0) {
                    this.fireEvent(new mxEventObject('hide_block', 'msg', 'block out'))
                    this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', 'MDIAS与现地通信恢复!'))
                }
            } else if (state.data.status == 2) {
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '现地通信故障!'))
            } else if (state.data.status == 3) {
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '联锁通信数据错误!'))
            } else if (state.data.status == 4) {
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '联锁协议版本不一致!'))
            }
        } else { // 前置机
            this.frontState = state.data.status;
            if (state.data.status == 1) {
                var cell = this.parkElementCache['允许MDIAS控']
                var light = cell.getSubCell('light')[0]
                this.setFillColor(light, '#000')
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '前置机通信中断'))
            } else if (state.data.status == 0) {
                var cell = this.parkElementCache['允许MDIAS控']
                var light = cell.getSubCell('light')[0]
                this.setFillColor(light, '#0f0')

                if (this.interLockState == 0) {
                    this.fireEvent(new mxEventObject('hide_block'))
                    this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '前置机通信恢复'))
                }
            } else if (state.data.status == 2) {
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '前置机通信故障'))
            } else if (state.data.status == 3) {
                this.fireEvent(new mxEventObject('show_block'))
                this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', '前置机通信数据错误'))
            }
        }
    }
}

ParkMapForXiandi.prototype.normalizeUID = function (uid) {
    return uid.replace('/', '_').toUpperCase()
}

// 设置区段状态
ParkMapForXiandi.prototype.setRailSecStatus = function (uid, status) {

    var cell = this.parkElementCache[uid]
    if (!cell) {
        return
    }

    // 设置cell的站场状态
    cell.setParkStatus(status);

    // 获取子组件
    var roads = cell.getSubCell('road')
    var nameLabels = cell.getSubCell('label')

    uid = this.normalizeUID(uid)

    // 重置显示颜色, 先恢复，然后根据状态再进行处理
    var allParts = [roads]
    allParts.map(parts => {
        parts.map((part) => {
            this.flashCells.delete(part)
            this.graph.model.setVisible(part, true);
            let style = mxUtils.setStyle(part.style, "strokeWidth", 1)
            style = mxUtils.setStyle(style, "opacity", 100)
            style = mxUtils.setStyle(style, "strokeColor", 'None')
            this.graph.model.setStyle(part, style)
            // this.setFillColor(part, '#5578b6')
            this.setFillColor(part, this.railColors.blue)
        })
    })

    // 如果隐藏区段标签则隐藏
    if (!this.hideSectionName) {
        nameLabels.map(label => this.setLabelText(
            label, `<div style="background:none;color:#fff;">${uid}</div>`))
    } else {
        nameLabels.map(label => this.setLabelText(
            label, `<div style="visibility:hidden">${uid}</div>`))
    }

    // 绿色光带：道岔所在的轨道区段处于空闲锁闭状态
    if (!status.hold && status.lock) {
        roads.map(road => {
            this.setFillColor(road, '#0f0')
        })
    }

    // 红色光带：表示区段为占用状态或区段轨道电路故障；
    if (status.hold) {
        roads.map(road => {
            this.setFillColor(road, this.railColors.red)
        })
    }

    if (status.block == 1) {
        roads.map(road => {
            this.flashCells.add(road)
        })
    }

    // 在原有区段状态上下增加粉红色线框的光带：表示区段被人工设置为轨道分路不良标记。
    if (status.badness) {
        roads.map(road => {
            this.setStrokeColor(road, this.railColors.pink)
        })
    }

    if (status.notice != 0) {
        switch (status.notice) {
            case 22:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 照查不满足`))
                break
            case 23:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 机务段不同意`))
                break
            case 24:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 事故无驱吸起`))
                break
            case 25:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 照查错误`))
                break
            case 26:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 开通条件不满足`))
                break
            case 27:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 在进路中`))
                break
            case 28:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 不能正常解锁`))
                break
            case 29:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 占用`))
                break
            case 30:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 照查敌对`))
                break
            case 31:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 较核错`))
                break
        }
    }
}


//设置状态灯状态
ParkMapForXiandi.prototype.setLightStatus = function (uid, status) {

    // BYTE light : 1;               // 亮灯
    // BYTE flash : 1;               // 闪灯
    // BYTE red : 1;                 // 红灯
    // BYTE yellow : 1;              // 黄灯
    // BYTE green : 1;               // 绿灯
    // BYTE blue : 1;                // 蓝灯
    // BYTE white : 1;               // 白灯
    // BYTE yellow2 : 1;             // 黄灯

    var cell = this.parkElementCache[uid]
    if (!cell) return

    cell.setParkStatus(status)

    // 根据不同种类信号机初始化, 特殊信号灯比如电源灯
    if (cell.getAttribute('type')) {

        var lights = cell.getSubCell('light')
        var lighto = undefined;

        // 如果子项没有light的话说明是单独的灯
        if (lights && lights.length > 0) {
            lighto = lights[0]
        } else {
            lighto = cell
        }

        // 重置数据
        this.flashCells.delete(lighto)
        this.showcell(lighto)

        if (cell.getAttribute('type') == 'lightflash') {
            this.setFillColor(lighto, '#000')
            if (status.light) {
                this.setFillColor(lighto, '#f00')
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'lightyellow') {
            this.setFillColor(lighto, '#000')
            if (status.light) {
                this.setFillColor(lighto, '#ff0')
            }
            if (status.flash) {
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'BTN') {
            this.setFillColor(lighto, '#B3B3B3')
            if (status.light) {
                this.setFillColor(lighto, '#ff0')
            }
            if (status.flash) {
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'lightgreen') {
            this.setFillColor(lighto, '#000')
            if (status.light) {
                this.setFillColor(lighto, '#0f0')
            }
            if (status.flash && !uid.endsWith("ZC")) {
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'lightwhite') {
            this.setFillColor(lighto, '#000')
            if (status.light) {
                this.setFillColor(lighto, '#fff')
            }
            if (status.flash) {
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'lightgray') {
            this.setFillColor(lighto, '#676767')
            if (status.light) {
                this.setFillColor(lighto, '#fff')
            }
            if (status.flash) {
                this.flashCells.add(lighto)
            }
            return
        }

        if (cell.getAttribute('type') == 'lightred') {
            this.setFillColor(lighto, '#f00')
            if (status.light) {
                this.setFillColor(lighto, '#fff')
            }
            if (status.flash) {
                this.flashCells.add(lighto)
            }
            return
        }
        return
    }

    // 获取零件
    lights = cell.getSubCell('light')
    var light1, light2

    if (lights && lights.length && lights.length > 1) {
        // 第一个灯为调车灯，第二个灯为
        light1 = lights.find(light => light.getAttribute('type') == 'da')
        light2 = lights.find(light => light.getAttribute('type') != 'da')
    }

    // 初始化
    if (light1 && light2) {
        this.setFillColor(light1, '#000')
        this.setFillColor(light2, '#000')
    }

    if (lights && lights.length > 0) {
        lighto = lights[0]
    } else {
        lighto = cell
    }

    this.flashCells.delete(lighto)
    this.showcell(lighto, true)
    this.setFillColor(lighto, '#000')

    if (status.light == 0 &&
        status.flash == 0 &&
        status.red == 0 &&
        status.yellow == 0 &&
        status.green == 0 &&
        status.blue == 0 &&
        status.white == 0 &&
        status.yellow2 == 0) {
        if (light1 && light2) {
            this.setFillColor(light1, '#f00')
            this.setFillColor(light2, '#000')
        }
    }

    // 亮红
    if (status.light) {
        this.setFillColor(lighto, '#f00')
    }

    if (status.yellow2) {
        this.setFillColor(lighto, '#ff0')
    }

    if (status.white) {
        this.setFillColor(lighto, '#fff')
    }

    if (status.blue) {
        this.setFillColor(lighto, '#00f')
    }

    if (status.green) {
        this.setFillColor(lighto, '#0f0')
    }

    if (status.yellow) {
        this.setFillColor(lighto, '#ff0')
    }

    if (status.red) {
        this.setFillColor(lighto, '#f00')
        if (light1 && light2) {
            this.setFillColor(light1, '#f00')
            this.setFillColor(light2, '#ff0')
        }
    }

    if (status.flash) {
        this.flashCells.add(lighto)
    }
}

ParkMapForXiandi.prototype.showcell = function (cell) {
    if (cell && cell.setVisible) {
        this.graph.model.setVisible(cell, true)
    }
}

ParkMapForXiandi.prototype.setLabelText = function (cell, code) {
    var oldvalue = cell.cloneValue()
    oldvalue.setAttribute('label', code)
    this.graph.model.setValue(cell, oldvalue)
}

/**
 * 设置cell的填充颜色
 */
ParkMapForXiandi.prototype.setFillColor = function (cell, color, isFlash) {
    if (!cell) {
        return
    }

    if (!isFlash) {
        this.oldColorCache[cell.getId()] = color;
    }

    this.setCellStyle(cell, 'fillColor', color)
};

/**
 * 设置样式上的内容
 */
ParkMapForXiandi.prototype.setCellStyle = function (cell, key, value) {
    var model = this.graph.model;
    var style = mxUtils.setStyle(model.getStyle(cell), key, value);
    model.setStyle(cell, style);
}

// 换cell的边框颜色
ParkMapForXiandi.prototype.setStrokeColor = function (cell, color) {
    if (!cell) {
        return
    }
    this.setCellStyle(cell, 'strokeColor', color)
}

// 全局闪烁
ParkMapForXiandi.prototype.DoFlashCells = function () {

    if (this.gloabalUpdate || !this.flashCells.size) {
        return
    }

    try {
        this.graph.getModel().beginUpdate()
        for (var cell of this.flashCells) {
            // 使用mxgraphmodel来对cell进行更新会直接刷新界面，效率更高
            if (cell.getAttribute('name') == "road") {
                let style = cell.style
                if (this.isFlashing) {
                    style = mxUtils.setStyle(style, "strokeWidth", 2)
                    style = mxUtils.setStyle(style, "opacity", 50)
                    style = mxUtils.setStyle(style, "strokeColor", '#99CCFF')
                } else {
                    style = mxUtils.setStyle(style, "strokeWidth", 1)
                    style = mxUtils.setStyle(style, "opacity", 100)
                    style = mxUtils.setStyle(style, "strokeColor", 'None')
                }
                this.graph.model.setStyle(cell, style)
            } else {
                var id = cell.getId()
                if (id in this.oldFillColorCache) {
                    if (this.isFlashing) {
                        // 设置为黑色
                        this.setFillColor(cell, '#000', true)
                    } else {
                        this.setFillColor(cell, this.oldColorCache[id])
                    }
                } else {
                    this.graph.model.setVisible(cell, this.isFlashing)
                }
            }
        }
        this.isFlashing = !this.isFlashing
    } finally {
        this.graph.getModel().endUpdate()
    }
}

/**
 * 取得分组index
 */
ParkMapForXiandi.prototype.getGroupIndex = function (uid, x, y) {
    var self = this
    if (uid in this.uidTrainCache) {
        var train_ids = this.uidTrainCache[uid]
        var tmpCell = undefined
        for (var i = 0; i < train_ids.length; i++) {
            var tmp_train_id = train_ids[i]
            var train = self.graph.model.getCell(tmp_train_id)
            var tmpPosition = self.getCellPostion(train)
            if (tmpPosition.x < x) {
                if (!tmpCell) {
                    tmpCell = train
                    tmpCell.tmpPosition = tmpPosition
                } else if (tmpPosition.x > tmpCell.tmpPosition.x) {
                    tmpCell = train
                }
            }
        }

        if (tmpCell) {
            return parseInt(tmpCell.getAttribute('group_index'))
        }
    }

    return 0
}

ParkMapForXiandi.prototype.getCellPostion = function (cell) {
    var geo = this.graph.model.getGeometry(cell)
    var x1 = geo.x
    var y1 = geo.y
    var tmpParent = cell.getParent()
    while (tmpParent) {
        var tmpGeo = this.model.getGeometry(tmpParent);
        if (!tmpGeo) {
            break
        }
        x1 += tmpGeo.x
        y1 += tmpGeo.y
        tmpParent = tmpParent.getParent()
    }
    return {
        x: x1,
        y: y1
    }
}

ParkMapForXiandi.prototype.getGroupOffset = function (uid, group_index) {
    var x = 0
    if (uid in this.uidTrainCache) {
        var train_ids = this.uidTrainCache[uid]
        for (var index = 0; index < train_ids.length; index++) {
            var train_id = train_ids[index]
            if (index < group_index) {
                var cell = this.graph.model.getCell(train_id)
                var geo = this.getCellPostion(cell)
                x += geo.x
            }
        }
    }
    return x
}

// 添加容器
ParkMapForXiandi.prototype.addTrain = function (status) {

    // 排除非本站场非法部件
    var uid = this.normalizeUID(status.park_uid)

    if (!this.parkElementCache[uid]) {
        console.log('can not find the uid when add train: ', uid)
        return
    }

    var parentCell = this.parkElementCache[uid];
    var x = 0;
    var y = 0;
    var type = parentCell.getAttribute('type')
    if (type == 'wc') {
        parentCell = parentCell.getSubCell("road")[0]
    } else {
        parentCell = parentCell.getSubCell("boundary")[0]
    }

    // 取得坐标, getGeometry取得的是相对于父容器的坐标
    var tmpPosition = this.getCellPostion(parentCell)
    var x1 = tmpPosition.x
    var y1 = tmpPosition.y
    var geo = this.graph.model.getGeometry(parentCell)

    var defaultParent = this.graph.getDefaultParent()
    var scale = this.graph.view.scale;

    var x = x1 + geo.width / (2.0 * scale)
    var y = y1

    if (type == 'wc') {
        y -= this.train_carriage_height - 2
    } else {
        y -= this.train_carriage_height / 2.0 + 10;
    }

    if (status.group_index && status.group_index > 0) {
        var offset = this.getGroupOffset(uid, status.group_index)
        x += offset
    }

    var doc = mxUtils.createXmlDocument();
    var node = doc.createElement('trainNode')
    var cell = this.graph.insertVertex(
        defaultParent, '', node, x, y, 0, 0, "opacity=0");
    node.setAttribute('type', 'train_body');
    node.setAttribute('position', uid)
    node.setAttribute('group_index', status.group_index)
    node.setAttribute('is_train', true)

    // add the train head
    var headNode = node.cloneNode();
    var head = this.graph.insertVertex(
        cell, '', headNode, 0, 0, this.train_head_width, this.train_head_height,
        "shape=image;image=images/train_head.png;");
    headNode.setAttribute('type', 'train_head')
    headNode.setAttribute('carriage_index', 0)

    // add the train tail
    var tailNode = node.cloneNode();
    var tail = this.graph.insertVertex(
        cell, '', tailNode, 0, 0, this.train_tail_width, this.train_tail_height,
        "shape=image;image=images/train_tail.png;");
    tailNode.setAttribute('type', 'train_tail')
    tailNode.setAttribute('carriage_index', 1)

    // put the train foregroud
    this.graph.orderCells(false, [cell, head, tail]);

    //  缓存，便于操作
    this.trainCache[cell.getId()] = cell

    return cell
}

/**
 * 删除
 */
ParkMapForXiandi.prototype.removeCarriage = function (train_no) {
    if (train_no && train_no in this.trainInfoCache) {
        var cellId = this.trainInfoCache[train_no]
        // 清除
        // delete this.trainInfoCache[cellId]
        var carriage = this.graph.model.getCell(cellId)
        var carriage_index = parseInt(carriage.getAttribute('carriage_index'))
        var train = carriage.getParent()
        this.graph.removeCells([carriage])
        if (!train.children || train.children.length <= 2) {
            // 删除缓缓存
            // delete this.trainCache[uid]
            this.graph.removeCells([train])
        } else {
            // update cell position
            var startPosition = 0;
            var childCells = train.children
            var cellInfos = []
            for (var i = 0; i < childCells.length; i++) {
                var carriage = childCells[i]
                var tmp_index = parseInt(carriage.getAttribute('carriage_index'))
                if (tmp_index > carriage_index) {
                    tmp_index = tmp_index - 1
                    carriage.setAttribute('carriage_index', tmp_index)
                }
                cellInfos.push({
                    'id': childCells[i].getId(),
                    "carriage_index": tmp_index
                })
            }

            cellInfos.sort(function (infoA, infoB) {
                var carriage_index1 = parseInt(infoA['carriage_index']);
                var carriage_index2 = parseInt(infoB['carriage_index']);
                return carriage_index1 - carriage_index2;
            })

            for (var i = 0; i < cellInfos.length; i++) {
                var tmpCell = this.model.getCell(cellInfos[i]["id"]);
                var geo = this.model.getGeometry(tmpCell);
                geo = geo.clone();
                geo.x = startPosition;
                var tmpType = tmpCell.getAttribute('type')
                if (tmpType == 'train_carriage') {
                    startPosition += this.train_carriage_width;
                } else {
                    startPosition += this.train_head_width;
                }
                this.graph.model.setGeometry(tmpCell, geo);
            }
        }
    }
}

// 添加容器
ParkMapForXiandi.prototype.addCarriage = function (status) {

    // 排除非本站场非法部件
    var uid = status.position
    var train_no = status.train_no

    // 从现在车的位置移除
    this.removeCarriage(train_no)

    var tmpCell = this.graph.getModel().getCell(uid);
    var cellType = tmpCell.getAttribute('type')
    var parentCell = undefined;
    var old_cells = []
    if (cellType == 'train_body') {
        parentCell = tmpCell
    } else {
        parentCell = tmpCell.getParent(tmpCell);
    }
    var old_cells = parentCell.children;

    // 取得容器的坐标
    var headWidth = this.train_head_width;
    var carrigeWidth = this.train_carriage_width;
    var height = this.train_carriage_height;

    var insertIndex = -1
    switch (cellType) {
        case 'train_body':
        case 'train_carriage':
        case 'train_head':

            // 统一放在后面，如果要放在前面则拖到前一个上面
            var index = undefined;
            if (cellType == 'train_body') {
                insertIndex = old_cells.length - 1
            } else {
                index = parseInt(tmpCell.getAttribute('carriage_index'));
                insertIndex = index + 1
            }

            // 更新index
            for (var i = 0; i < old_cells.length; i++) {
                var oldCell = old_cells[i];
                var oldIndex = parseInt(oldCell.getAttribute('carriage_index'));
                if (oldIndex >= insertIndex) {
                    oldCell.setAttribute("carriage_index", oldIndex + 1)
                }
            }
            break;

        case 'train_tail':
            var index = parseInt(tmpCell.getAttribute('carriage_index'))
            insertIndex = index;
            tmpCell.setAttribute("carriage_index", index + 1)
            break;
    }

    // create cell
    var doc = mxUtils.createXmlDocument();
    var node = doc.createElement('trainNode')
    var tmp_train_no = train_no
    if (train_no && _.startsWith(train_no, '110')) {
        tmp_train_no = 'K' + train_no.substr(3, train_no.length)
    }
    node.setAttribute('label', tmp_train_no);
    var newCell = this.graph.insertVertex(
        parentCell, '', node, 0, 0, carrigeWidth, height, "train_carriage");

    newCell.setAttribute('carriage_index', insertIndex);
    newCell.setAttribute('type', 'train_carriage')
    newCell.setAttribute('train_no', train_no)
    newCell.setAttribute('is_carriage', true)

    // update cell position
    var startPosition = 0;
    var childCells = parentCell.children
    var cellInfos = []
    for (var i = 0; i < childCells.length; i++) {
        cellInfos.push({
            'id': childCells[i].getId(),
            "carriage_index": childCells[i].getAttribute('carriage_index')
        })
    }

    cellInfos.sort(function (infoA, infoB) {
        var carriage_index1 = parseInt(infoA['carriage_index']);
        var carriage_index2 = parseInt(infoB['carriage_index']);
        return carriage_index1 - carriage_index2;
    })

    for (var i = 0; i < cellInfos.length; i++) {
        var tmpCell = this.model.getCell(cellInfos[i]["id"]);
        var geo = this.model.getGeometry(tmpCell);
        geo = geo.clone();
        geo.x = startPosition;
        var tmpType = tmpCell.getAttribute('type')
        if (tmpType == 'train_carriage') {
            startPosition += carrigeWidth;
        } else {
            startPosition += headWidth;
        }
        this.graph.model.setGeometry(tmpCell, geo);
        if (tmpType == 'train_carriage') {
            this.trainInfoCache[train_no] = tmpCell.getId()
        }
    }

    // set the cell forground
    this.graph.orderCells(false, childCells);

    return newCell
}

/*
 * 取得区段的中间位置
 */
ParkMapForXiandi.prototype.getSecCenterPosition = function (uid) {
    uid = uid.toUpperCase();

    var curCell = undefined;
    var cell = this.parkElementCache[uid];
    if (cell.getAttribute('type') == 'ca') {

        var direct_cell = cell.getSubCell('direct')[0];
        var reverse_cell = cell.getSubCell('reverse')[0];

        // 主里要看当
        var directVisible = direct_sub_cell.isVisible();
        if (directVisible) {
            curCell = direct_cell;
        } else {
            curCell = reverse_cell;
        }
    } else {
        curCell = cell;
    }
    var state = this.graph.view.getState(curCell);
    var cellBounds = state.cellBounds;
    return {
        'x': cellBounds.getCenterX(),
        'y': cellBounds.getCenterY()
    }
}

ParkMapForXiandi.prototype.initTrainStyle = function () {

    var style = new Object();

    // electric train
    style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_IMAGE;
    style[mxConstants.STYLE_ALIGN] = mxConstants.ALIGN_CENTER;
    style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_CENTER;
    style[mxConstants.STYLE_IMAGE_ALIGN] = mxConstants.ALIGN_CENTER;
    style[mxConstants.STYLE_IMAGE_VERTICAL_ALIGN] = mxConstants.ALIGN_CENTER;
    style[mxConstants.STYLE_FILLCOLOR] = '';
    style[mxConstants.STYLE_IMAGE] = 'images/electric_train.png';
    style[mxConstants.STYLE_SPACING] = '0';
    style[mxConstants.STYLE_FONTCOLOR] = '#FF0000';

    this.graph.getStylesheet().putCellStyle('electric_train', style);

    // train left head
    style = mxUtils.clone(style);
    style[mxConstants.STYLE_IMAGE] = 'images/train_head.png';
    this.graph.getStylesheet().putCellStyle('train_head', style);

    // train right head
    style = mxUtils.clone(style);
    style[mxConstants.STYLE_IMAGE] = 'images/train_tail.png';
    this.graph.getStylesheet().putCellStyle('train_tail', style);

    // train carriage
    style = mxUtils.clone(style);
    style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RECTANGLE;
    style[mxConstants.STYLE_LABEL_POSITION] = mxConstants.ALIGN_CENTER;
    style[mxConstants.STYLE_VERTICAL_LABEL_POSITION] = mxConstants.ALIGN_MIDDLE;
    style[mxConstants.STYLE_VERTICAL_ALIGN] = mxConstants.ALIGN_MIDDLE;
    style[mxConstants.STYLE_FONTCOLOR] = 'white';
    style[mxConstants.STYLE_STROKEWIDTH] = '2';
    style[mxConstants.STYLE_STROKECOLOR] = 'red';
    this.graph.getStylesheet().putCellStyle('train_carriage', style);

    // train body
    var bodyStyle = new Object();
    bodyStyle[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_RECTANGLE;
    bodyStyle[mxConstants.STYLE_OPACITY] = 0;
    this.graph.getStylesheet().putCellStyle('train_body', bodyStyle);
}

ParkMapForXiandi.prototype.initBusyIconStyle = function () {

    var style = new Object();

    // construction
    style[mxConstants.STYLE_SHAPE] = mxConstants.SHAPE_IMAGE;
    style[mxConstants.STYLE_FILLCOLOR] = '';
    style[mxConstants.STYLE_IMAGE] = 'images/construction.png';
    style[mxConstants.STYLE_IMAGE_WIDTH] = '24';
    style[mxConstants.STYLE_IMAGE_HEIGHT] = '24';

    this.graph.getStylesheet().putCellStyle('construction', style);

    // electric stoped
    style = mxUtils.clone(style);
    style[mxConstants.STYLE_IMAGE] = 'images/electric.png';
    this.graph.getStylesheet().putCellStyle('electric_stoped', style);

    // blocked
    style = mxUtils.clone(style);
    style[mxConstants.STYLE_IMAGE] = 'images/block.png';
    this.graph.getStylesheet().putCellStyle('area_block', style);
}

ParkMapForXiandi.prototype.dualMap = function (parts, func) {
    parts.map(part => {
        part.map(func)
    })
}

// 设置道岔状态
ParkMapForXiandi.prototype.setSwitchStatus = function (uid, status) {

    var cell = this.parkElementCache[uid]
    if (!cell) {
        console.log('没有找到站场元素', uid);
        return
    }

    cell.setParkStatus(status)

    // 获取零件, 由于有些元件有多个, 所以通过数组的形式来处理
    var roadEntrances = cell.getSubCell('road-entrance');
    var roadDirects = cell.getSubCell('road-direct');
    var roadReverses = cell.getSubCell('road-reverse');
    var reverses = cell.getSubCell('reverse');
    var directs = cell.getSubCell('direct');
    var nameLabels = cell.getSubCell('label');
    var boundarys = cell.getSubCell('boundary');
    var locks = cell.getSubCell('lock');

    // 重置显示颜色为蓝色
    var allParts = [reverses, directs, roadReverses, roadDirects, roadEntrances]
    allParts.map(parts => {
        parts.map((cell) => {
            this.graph.model.setVisible(cell, true)
            this.setFillColor(cell, this.switchColors.blue)
        })
    })

    // 重置lable颜色
    nameLabels.map(label => this.setLabelText(label,
        `<div style="background:none;color:#fff;">${uid}</div>`))

    // 隐藏边框
    if (boundarys.length) {
        boundarys.map(boundary => {
            this.graph.model.setVisible(boundary, false)
        })
    }

    // 隐藏封锁
    if (locks.length) {
        locks.map(lock => {
            this.graph.model.setVisible(lock, 0)
        })
    }

    // 道岔的正反位部份
    var parts = [reverses, directs]
    parts.map(part => {
        part.map((cell) => {
            this.flashCells.delete(cell)
            this.showcell(cell)
        })
    })

    // 设置挤岔状态
    if (status.switch_crowded) {
        // 先判断缓存里是否存在，防止得复提醒
        if (!this.switchCrowCache[uid]) {
            this.fireEvent(new mxEventObject('add_interlock_alarm', 'msg', `道岔${uid}#挤岔`));
            this.switchCrowCache[uid] = true
        }

        // 正反位部份设置成为红色, 同时进行闪烁
        var parts = [reverses, directs]
        parts.map(part => {
            part.map((cell) => {
                this.setFillColor(cell, '#f00')
                this.graph.model.setVisible(cell, true)
                this.flashCells.add(cell)
            })
        })

        nameLabels.map(nameLabel => this.setLabelText(
            nameLabel, `<div style="color:#f00;">${uid}</div>`))
    } else {
        if (uid in this.switchCrowCache) {
            this.fireEvent(
                new mxEventObject('add_interlock_alarm', 'msg', `道岔${uid}#挤岔恢复.`));
            this.switchCrowCache[uid] = false
        }
    }

    if (!status.switch_crowded) {
        // 绿色稳定显示：表示道岔此时处于定位位置；
        if (status.pos) {
            directs.map(direct => {
                if (!this.hideSwitchPosition) {
                    this.setFillColor(direct, '#0f0')
                }
            })
            nameLabels.map(nameLabel => this.setLabelText(
                nameLabel, `<div style="color:#0f0;">${uid}</div>`))
        } else if (!status.switch_crowded) {
            // 隐藏正位
            directs.map(direct => {
                this.graph.model.setVisible(direct, false)
            })
        }

        // 黄色稳定显示：表示道岔此时处于反位位置；
        if (status.pos_reverse) {
            reverses.map(reverse => {
                if (!this.hideSwitchPosition) {
                    this.setFillColor(reverse, '#ff0')
                }
            })
            nameLabels.map(nameLabel => this.setLabelText(
                nameLabel, `<div style="color:#ff0;">${uid}</div>`))
        } else {
            reverses.map(reverse => {
                this.graph.model.setVisible(reverse, false)
            })
        }
    }

    // 黑色稳定显示：表示道岔刚失去表示
    if (status.pos == 0 && status.pos_reverse == 0 && !status.switch_crowded) {
        var parts = [reverses, directs]
        parts.map(part => {
            part.map((cell) => {
                this.graph.model.setVisible(cell, false)
            })
        })

        nameLabels.map(nameLabel => this.setLabelText(
            nameLabel, `<div style="color:#f00;">${uid}</div>`))
    }

    // 黄色稳定显示
    if (this.showLightBelt) {
        var parts = [roadEntrances]
        if (status.pos == 1) {
            parts.push(roadDirects, directs)
        }

        if (status.pos_reverse == 1) {
            parts.push(roadReverses, reverses)
        }

        parts.map(part => {
            part.map((cell) => {
                this.setFillColor(cell, this.switchColors.yellow)
            })
        })
    }

    // 隐藏道岔名称
    if (this.hideSwitchName) {
        nameLabels.map(nameLabel => this.setLabelText(
            nameLabel, `<div style="visibility:hidden">${uid}</div>`))
    }

    // 白色光带：道岔所在的轨道区段处于空闲锁闭状态
    if (status.hold == 0 && status.lock == 1) {
        var parts = [roadEntrances]

        if (status.pos == 1) {
            parts.push(roadDirects, directs)
        }

        if (status.pos_reverse == 1) {
            parts.push(roadReverses, reverses)
        }

        parts.map(part => {
            part.map((cell) => {
                this.setFillColor(cell, this.sdjs ? this.switchColors.white : '#0f0')
            })
        })
    }

    // 红色光带：道岔所在的轨道区段处于占用或轨道电路故障；
    if (status.hold == 1) {
        var parts = [roadEntrances]
        // 正位
        if (status.pos == 1) {
            parts.push(roadDirects, directs)
        }
        // 反位
        if (status.pos_reverse == 1) {
            parts.push(roadReverses, reverses)
        }

        if (status.pos == 0 && status.pos_reverse == 0) {
            a.push(roadDirects, directs)
            a.push(roadReverses, reverses)
        }

        // 设置颜色
        parts.map(part => {
            part.map((cell) => {
                this.setFillColor(cell, this.switchColors.red)
            })
        })
    }

    // 闭锁状态
    if (status.closed) {
        nameLabels.map(i => this.setLabelText(i, `<div style="color:#00f;">${uid}</div>`))
        locks.map(lock => {
            this.graph.model.setVisible(lock, 1)
        })
    }

    // 封锁
    if (status.lock_s || status.lock_protect || status.lock_gt) {
        boundarys.map(boundary => {
            this.graph.model.setVisible(boundary, true)
            if (status.pos) {
                this.setStrokeColor(boundary, "#0f0")
            } else if (status.pos_reverse) {
                this.setStrokeColor(boundary, "#ff0")
            }
        })
    }

    // 预排兰光带
    if (status.pos_blue || status.reverse_blue) {
        var parts = [roadEntrances]

        if (status.pos_blue == 1) {
            parts.push(roadDirects, directs)
        }

        if (status.reverse_blue == 1) {
            parts.push(roadReverses, reverses)
        }

        parts.map(part => {
            part.map((cell) => {
                this.setFillColor(cell, '#00f')
            })
        })
    }

    if (status.notice != 0) {
        switch (status.notice) {
            case 1:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 单锁不能动`));
                break
            case 2:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 锁闭不能动`));
                break
            case 15:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 区段道岔有封闭`));
                break
            case 16:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 注意超限不满足`));
                break
            case 17:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 校核错`));
                break
            case 18:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 有车移动`));
                break
            case 19:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 不能正常解锁`));
                break
            case 20:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 紧急关闭`));
                break
            case 21:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 没锁闭`));
                break
            case 22:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 要求防护道岔不到位`));
                break
            case 23:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 不在要求位置`));
                break
            case 24:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 要求防护道岔不能动`));
                break
            case 25:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 超限不满足`));
                break
            case 26:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 不能动`));
                break
            case 27:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 封闭`));
                break
            case 28:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 锁闭`));
                break
            case 29:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 在进路中`));
                break
            case 30:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} 有车占用`));
                break
            case 31:
                this.fireEvent(new mxEventObject('add_warning', 'msg', `${uid} SFJ失效`));
                break
        }
    }
}

// 设置信号机状态
ParkMapForXiandi.prototype.setSignalStatus = function (uid, status) {
    var cell = this.parkElementCache[uid]
    if (!cell)
        return

    cell.setParkStatus(status)

    // 获取零件
    let lights = cell.getSubCell('light')
    var buttons = cell.getSubCell('button')
    var nameLabels = cell.getSubCell('label')
    var boundarys = cell.getSubCell('boundary')

    // fork 归到boundarys下面去
    boundarys = boundarys.concat(cell.getSubCell('fork'))

    /**
     * 初始化所有零件, 重置显示
     */
    lights.map(light => {
        if (!!light.getAttribute('defaultcolor') &&
            !this.specialColorCache[light.id]) {
            this.specialColorCache[light.id] = light.getAttribute('defaultcolor')
        }
        if (this.specialColorCache[light.id]) {
            this.setFillColor(light, this.specialColorCache[light.id])
        } else {
            this.setFillColor(light, '#000')
        }

        this.setStrokeColor(light, '#5578b6')
    })

    // 重置lable颜色, 白色闪烁
    if (!this.delayCountdown || !this.delayCountdown[uid]) {
        if (!this.hideSignalName) {
            nameLabels.map(nameLabel => this.setLabelText(
                nameLabel, `<div style="background:none;color:#fff;">${uid}</div>`))
        } else if (this.hideSignalName &&
            status.delay_30s == 0 && status.delay_180s == 0) {
            nameLabels.map(nameLabel => this.setLabelText(
                nameLabel, `<div style="visibility:hidden">${uid}</div>`))
        }
    }

    // 列车按扭
    var buttonLa = buttons.find(button => button.getAttribute('type') == 'la')
    // 引导按扭
    var buttonYa = buttons.find(button => button.getAttribute('type') == 'ya')
    // 调车灯
    var lightDa = lights.find(light => light.getAttribute('type') == 'da')
    // 列车灯, 最多也就两个灯
    var lightLa = lights.find(light => light.getAttribute('type') != 'da')

    // 删除闪烁
    this.flashCells.delete(buttonLa)
    this.flashCells.delete(buttonYa)
    this.flashCells.delete(lightDa)
    this.flashCells.delete(lightLa)
    this.flashCells.delete(nameLabels[0])

    this.showcell(nameLabels[0])
    this.showcell(buttonLa)
    this.showcell(buttonYa)
    this.showcell(lightDa)
    this.showcell(lightLa)

    // 加边框显示
    var singleDa = false
    // 两个按扭，且为调车按扭
    if (buttons.length == 1 && buttons[0].getAttribute('type') == 'da') {
        singleDa = true
    }

    if (!boundarys.length) {
        // 获取调车灯坐标作为参考, 创建一个叉
        // var lightDa = lights.find(light => light.getAttribute('type') == 'da')
        if (lightDa) {
            var refPosition = lightDa.geometry
            // 复制一份
            var boundaryValue = lightDa.value.cloneNode(true)
            boundaryValue.setAttribute('name', 'fork')
            var style = "shape=umlDestroy;whiteSpace=wrap;strokeWidth=2;html=1;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;"
            var newBoundary = this.graph.insertVertex(
                lightDa.parent, null, '', refPosition.x + 3, refPosition.y + 3, 14, 14, style);
            newBoundary.value = boundaryValue
            boundarys.push(newBoundary)
        }

        // 创建方框
        if (lightDa) {
            var refPosition = lightDa.geometry
            var boundaryValue = lightDa.value.cloneNode(true)
            boundaryValue.setAttribute('name', 'boundary')

            // 是否有两个灯
            var newBoundary = undefined
            var style = "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;"
            if (lights.length == 2) {
                // 是否在左边, 两个灯一个做了标记，一个未做标记
                var lightNone = lights.find(light => light.getAttribute('type') != 'da')
                if (lightDa.geometry.x > lightNone.geometry.x) {
                    newBoundary = this.graph.insertVertex(
                        lightDa.parent, null, 'rect', refPosition.x - 21, refPosition.y, 42, 19, style);
                } else {
                    newBoundary = this.graph.insertVertex(
                        lightDa.parent, null, 'rect', refPosition.x, refPosition.y, 42, 19, style);
                }
            } else {
                newBoundary = this.graph.insertVertex(
                    lightDa.parent, null, '', refPosition.x, refPosition.y, 19, 19, style);
            }

            newBoundary.value = boundaryValue
            newBoundary.specialName = 'rect'
            boundarys.push(newBoundary)
        }

        // 获取列车信号坐标作为参考, 创建一个叉
        // var lightLa = lights.find(light => light.getAttribute('type') != 'da')
        if (lightLa) {
            var refPosition = lightLa.geometry
            var boundaryValue = lightLa.value.cloneNode(true)

            boundaryValue.setAttribute('name', 'fork')
            var style = "shape=umlDestroy;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;"
            var newBoundary = this.graph.insertVertex(
                lightLa.parent, null, '',
                refPosition.x + 3, refPosition.y + 3, 14, 14, style);

            newBoundary.value = boundaryValue
            boundarys.push(newBoundary)
        }

        // 获取列车信号按钮坐标作为参考, 创建一个叉
        //var tmpButtonLa = buttons.find(button => button.getAttribute('type') == 'la')
        if (buttonLa) {
            var refPosition = buttonLa.geometry
            var boundaryValue = buttonLa.value.cloneNode(true)

            boundaryValue.setAttribute('name', 'fork')
            var style = "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;"
            var newBoundary = this.graph.insertVertex(
                buttonLa.parent, null, '', refPosition.x, refPosition.y, 14, 14, style);

            newBoundary.value = boundaryValue
            boundarys.push(newBoundary)
        }

        // 获取引导按钮坐标作为参考,创建一个叉
        buttonYa = buttons.find(button => button.getAttribute('type') == 'ya' || singleDa)
        if (buttonYa) {
            var refPosition = buttonYa.geometry
            var boundaryValue = buttonYa.value.cloneNode(true)

            boundaryValue.setAttribute('name', 'fork')
            var style = "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;"
            var newBoundary = this.graph.insertVertex(
                buttonYa.parent, null, '', refPosition.x, refPosition.y, 14, 14, style);

            newBoundary.value = boundaryValue
            boundarys.push(newBoundary)
        }
    }

    // 重置，隐藏边框
    if (boundarys.length) {
        boundarys.map(boundary => {
            this.setStrokeColor(boundary, '#f00')
            this.graph.model.setVisible(boundary, false)
        })
    }

    /**
     * 开始设置零件样式
     * / 信号状态
    struct SignalStatus {
        BYTE red_blue: 1;             // 红/兰
        BYTE white : 1;               // 白灯
        BYTE yellow : 1;              // 黄灯
        BYTE yellow_twice : 1;        // 双黄
        BYTE green_yellow : 1;        // 绿黄
        BYTE green : 1;               // 绿灯
        BYTE red_white : 1;           // 红白
        BYTE green_twice : 1;         // 双绿
        BYTE train_btn_flash : 1;     // 列车按钮闪亮
        BYTE ligth_broken_wire : 1;   // 灯丝断丝
        BYTE shunt_btn_light : 1;     // 调车按钮闪亮
        BYTE close_lock : 1;          // 接近锁闭
        BYTE da_start : 1;            // 调车始端
        BYTE signal_end : 1;          // 信号终端
        BYTE delay_180s : 1;          // 延时3分钟
        BYTE delay_30s : 1;           // 延时30秒
                                    
        BYTE guaid_10s : 1;           // 引导10s
        BYTE guaid_flash : 1;         // 坡道延时解锁
        BYTE closed : 1;              // 封闭
        BYTE notice : 5;              // 提示信息
    };
     */
    if (status.closed) {
        if (singleDa) {
            boundarys.map(boundary => {
                this.graph.model.setVisible(boundary, true)
            })
        } else if (buttonLa) {
            // 有列车按钮就全部按钮红叉
            boundarys.map(boundary => {
                if (boundary.value.getAttribute('name') == 'fork' &&
                    (boundary.value.getAttribute('type') == 'la' ||
                        boundary.value.getAttribute('type') == 'ya')) {
                    this.graph.model.setVisible(boundary, true)
                }
            })
        } else {
            // 没有列车就就把车灯红框
            boundarys.map(boundary => {
                if (boundary.value.getAttribute('name') == 'boundary' &&
                    (boundary.value.getAttribute('type') == 'da' || !boundary.value.getAttribute('type'))) {
                    this.graph.model.setVisible(boundary, true)
                }
            })
        }
    }

    // // 信号机方框显示 调车始端
    // if (status.da_start == 1 && status.signal_end == 0) {
    //     boundarys.map(boundary => {
    //         if (boundary.value.getAttribute('name') == 'boundary' &&
    //             (boundary.value.getAttribute('type') == 'da' || !boundary.value.getAttribute('type'))) {
    //             this.graph.model.setVisible(boundary, true)
    //             this.setStrokeColor(boundary, 'white')
    //         }
    //     })
    // }

    // // 信号终端
    // if (status.da_start == 0 && status.signal_end == 1) {
    //     boundarys.map(boundary => {
    //         if (boundary.value.getAttribute('name') == 'boundary' &&
    //             (boundary.value.getAttribute('type') == 'da' || !boundary.value.getAttribute('type'))) {
    //             this.graph.model.setVisible(boundary, true)
    //             this.setStrokeColor(boundary, '#ffff00') // 黄色
    //         }
    //     })
    // }

    // // 调车信号始端，信号终端
    // if (status.da_start == 1 && status.signal_end == 1) {
    //     boundarys.map(boundary => {
    //         if (boundary.value.getAttribute('name') == 'boundary' &&
    //             (boundary.value.getAttribute('type') == 'da' ||
    //                 !boundary.value.getAttribute('type'))) {
    //             this.graph.model.setVisible(boundary, true)
    //             this.setStrokeColor(boundary, '#00ff00') // 绿色
    //         }
    //     })
    // }

    // 接近锁闭
    if (status.close_lock) {
        boundarys.map(boundary => {
            if (boundary.value.getAttribute('name') == 'boundary' &&
                (boundary.value.getAttribute('type') == 'da' || !boundary.value.getAttribute('type'))) {
                this.graph.model.setVisible(boundary, true)
                this.setStrokeColor(boundary, '#8B36B0') // 紫色
            }
        })
    }

    if (status.red_blue) {
        lights.map(light => {
            if (light.id in this.specialColorCache) {
                this.setFillColor(light, this.specialColorCache[light.id])
                this.setStrokeColor(light, this.specialColorCache[light.id])
            }
        })
    }

    if (status.white) {
        if (lightDa) this.setFillColor(lightDa, '#fff')
        if (lightDa) this.setStrokeColor(lightDa, '#fff')
    }

    if (status.guaid_flash && !status.red_white) {
        if (buttonYa) this.flashCells.add(lightDa)
    }

    if (status.yellow) {
        if (lightLa) this.setFillColor(lightLa, '#ff0')
        if (lightLa) this.setStrokeColor(lightLa, '#ff0')
        if (lightDa) this.setFillColor(lightDa, '#000')
        if (lightDa) this.setStrokeColor(lightDa, 'none')
    }

    if (status.yellow_twice) {}
    if (status.green_yellow) {}

    if (status.green) {
        if (lightLa) this.setFillColor(lightLa, '#0f0')
        if (lightLa) this.setStrokeColor(lightLa, '#0f0')
    }

    if (status.red_white || status.red_yellow) {
        if (lightDa) this.setFillColor(lightDa, '#f00')
        if (lightLa) this.setFillColor(lightLa, '#ff0')
        if (lightDa) this.setStrokeColor(lightDa, '#f00')
        if (lightLa) this.setStrokeColor(lightLa, '#ff0')
    }

    if (status.green_twice) {}
    if (status.train_btn_flash) {
        if (buttonLa) this.flashCells.add(buttonLa)
    }

    // 灯丝断丝, 如果原来是正常的则报警，如果原来是非正常也通知变化
    if (status.ligth_broken_wire) {
        // 防止得复报警
        if (!this.signalAlarmCache[uid]) {
            // this.fireEvent(
            //     new mxEventObject('add_interlock_alarm', "msg", `信号机${uid}灯丝断丝!`));
            this.signalAlarmCache[uid] = true
        }
        if (lightDa) {
            this.flashCells.add(lightDa)
        }
    } else {
        if (this.signalAlarmCache[uid]) {
            // this.fireEvent(
            //     new mxEventObject('add_interlock_alarm', "msg", `信号机${uid}灯丝恢复!`));
            this.signalAlarmCache[uid] = false
        }
    }

    if (status.shunt_btn_light) {
        this.flashCells.add(nameLabels[0])
    }

    if (status.delay) {
        // 已经在倒计时中, 过滤掉重复的情况
        if (this.delayCountingInfo[uid]) {
            return
        }
        this.delayCountingInfo[uid] = true
        var remain = status.delay
        var interval = setInterval(() => {
            //满足条件删除定时
            var cell = this.parkElementCache[uid]
            var condition = false
            if (remain < 0) {
                condition = true
            }
            if (!cell.elementStatus.delay) {
                condition = true
            }
            if (condition) {
                clearInterval(interval)
                this.delayCountingInfo[uid] = false
                this.setSignalStatus(uid, cell.elementStatus)
            } else {
                this.delayCountingInfo[uid] = true
                var style = `<div style="white-space:nowrap;background:none;color:#fff;"><span style="white-space:nowrap;background:none;color:#f00;">${remain--}s</span></div>`
                nameLabels.map(nameLabel => {
                    this.setLabelText(nameLabel, style)
                })
            }
        }, 1000)
    }

    if (status.notice) {
        switch (status.notice) {

            // case 1:
            // case 3:
            //     this.history_info.push(uid)
            //     break

            // case 2:
            //     this.history_info.push(uid)
            //     this.alarmwarninglistadd("调车 " + this.history_info.join(" -> "))
            //     this.history_info.splice(0, this.history_info.length);
            //     break

            // case 4:
            //     this.history_info.push(uid)
            //     this.alarmwarninglistadd("列车 " + this.history_info.join("->"))
            //     this.history_info.splice(0, this.history_info.length);

            case 5:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `变更 ${uid}!`));
                break;

            case 6:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `重开 ${uid}!`));
                break;

                // case 7:
                //     this.alarmwarninglistadd(`引导 ${uid}`)
                //     break

            case 8:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `通过 ${uid}!`));
                break;

            case 9:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `调车取消 ${uid}!`));
                break;

            case 10:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `列车取消 ${uid}!`));
                break;

            case 11:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `调车人解 ${uid}!`));
                break;

            case 12:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `列车人解 ${uid}!`));
                break;

            case 17:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `红灯断丝 ${uid}!`));
                break;

            case 18:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `灯丝断丝 ${uid}!`));
                break;

            case 19:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `有车移动 ${uid}!`));
                break;

            case 20:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `有迎面解锁可能 ${uid}!`));
                break;

            case 21:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `非正常关闭 ${uid}!`));
                break;

            case 22:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `不能取消 ${uid}!`));
                break;

            case 23:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `不能通过 ${uid}!`));
                break;

            case 24:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `不能引导 ${uid}!`));
                break;

            case 25:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不是列终!`));
                this.pre_button = {}
                break;

            case 26:
                this.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不是列始!`));
                this.pre_button = {}
                break;

            case 27:
                this.editorUi.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不是调终!`));
                this.pre_button = {}
                break;

            case 28:
                this.editorUi.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不是调始!`));
                this.pre_button = {}
                break;

            case 29:
                this.editorUi.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不构成进路!`));
                this.pre_button = {}
                break;

            case 30:
                this.editorUi.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 不能开放!`));
                break;

            case 31:
                this.editorUi.fireEvent(
                    new mxEventObject('add_warning', "msg", `${uid} 无驱开放!`));
                break;
        }
    }
}

// 重置状态
ParkMapForXiandi.prototype.resetStatus = function () {
    this.startTime = null
    this.status = 0
    this.actionMark = Math.random()
    this.clickPath = []
}

// 按钮点击处理
ParkMapForXiandi.prototype.buttonClick = function (btnInfo, button, e) {
    var self = this

    console.log('点击按钮', btnInfo, button, this.status)

    // 通信中断后不可操作
    if (this.sysBlackout) {
        return
    }

    // 清除
    if (btnInfo == 'clear_action') {
        if (Object.keys(this.pre_button).length) {
            self.operation.send_interlock_cmd({
                status: 0x1A,
                clickPath: [this.pre_button]
            })
        }
        this.resetStatus()
        this.fireEvent(
            new mxEventObject('set_signal_html', ""));
        return
    }

    switch (this.status) {
        // 空闲时
        case 0: {
            // closed状态时按钮不能点
            if (btnInfo &&
                !btnInfo.type &&
                btnInfo.cell &&
                btnInfo.cell.elementStatus &&
                btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(
                    new mxEventObject(
                        'add_warning', 'msg', `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            // BTN按钮
            if (button && button.type && button.type == 'BTN') {

                if (this.location == 'banqiao') {
                    // 板桥有,高大路无,后续需修改为场段关联
                    var index = Number(button.uindex)
                    self.fireEvent(
                        new mxEventObject('add_warning', 'msg', `下发${button.name}`));

                    if (index == 277) {
                        self.fireEvent(
                            new mxEventObject(
                                'add_warning', 'msg', `下发非进路1`));
                    } else if (index == 278) {
                        self.fireEvent(
                            new mxEventObject(
                                'add_warning', 'msg', `下发非进路故障解锁1`));
                    }

                    console.log('the name is:', btnInfo.cell.elementStatus.name)

                    var send_data = {
                        clickPath: [{
                            index: index,
                            name: btnInfo.cell.elementStatus.name
                        }],
                        status: 0xAA
                    }

                    self.operation.send_interlock_cmd(send_data)
                }
                return
            }

            // 始端列车按钮（LA） 始端调车按钮（DA） 信号机引导按钮(YA)
            if (button &&
                button.type && ['la', 'da', 'ya'].includes(button.type)) {
                if (!button.uindex) {
                    return
                }

                // 重开信号
                if (button.type != 'ya' &&
                    btnInfo.cell.elementStatus &&
                    btnInfo.cell.elementStatus.da_start == 1 && [0, 1].indexOf(btnInfo.cell.elementStatus.signal_end) != -1) {
                    var html_text = `重开${btnInfo.cell.elementStatus.name}`
                    self.fireEvent(
                        new mxEventObject('set_signal_html', 'html', html_text));
                    self.fireEvent(
                        new mxEventObject('add_warning', 'msg', html_text));

                    var send_data = {
                        clickPath: [{
                            index: Number(button.uindex),
                            name: btnInfo.cell.elementStatus.name
                        }],
                        status: 0x3A
                    }

                    self.operation.send_interlock_cmd(send_data)
                    return
                }

                var now_button = {
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                }

                self.clickPath.push(now_button)
                self.status = self.buton_type_status_map[button.type]
                self.startCounting()

                // 引导进路
                if (button.type == 'ya') {
                    // 引导状态发送指令
                    if (btnInfo.cell.elementStatus.guaid_10s) {
                        self.commitAction()
                        return
                    }

                    if (btnInfo.cell.elementStatus.red_white) {
                        return
                    }

                    // 调出键盘
                    self.keybaord.setPosition(e)
                    // 这里没有回调对不对哦?
                    self.keybaord.reveal()
                    return
                } else {
                    // 列始 调始
                    self.fireEvent(new mxEventObject('get_signal_name_html', 'call_back', function (
                        html) {
                        var now_html_text = html
                        var new_html_text = ""
                        if (now_html_text.startsWith("列始") &&
                            now_html_text.indexOf("列终") == -1) {
                            if (button.type == "la" &&
                                JSON.stringify(now_button) != JSON.stringify(this.pre_button)) {
                                new_html_text = now_html_text + '—列终' + btnInfo.cell.elementStatus.name
                            }
                        } else if (now_html_text.startsWith("调始") && now_html_text.indexOf("调终") == -1) {
                            if (button.type == "da" && JSON.stringify(now_button) != JSON.stringify(this.pre_button)) {
                                new_html_text = now_html_text + '—调终' + btnInfo.cell.elementStatus.name
                            }
                        } else {
                            new_html_text = button.type == 'la' ? '列始' + btnInfo.cell.elementStatus.name : '调始' + btnInfo.cell.elementStatus.name
                        }
                        if (new_html_text.length) {
                            self.fireEvent(
                                new mxEventObject('set_signal_html', 'html', new_html_text));
                            self.fireEvent(
                                new mxEventObject('add_warning', 'msg', new_html_text));
                        }
                        // 记录前次点击按扭
                        self.pre_button = Object.assign({}, now_button)
                    }));
                }

                // self.commitAction()
                return
            }

            // 空闲时点下其他按钮的处理
            else if (Object.keys(self.statusMap).includes(btnInfo)) {
                // 点击按扭的时候设置了当前状态
                self.status = self.statusMap[btnInfo]
                // 取消引导进路
                if (btnInfo == 'all_relieve') {
                    //调出键盘
                    self.fireEvent(
                        new mxEventObject('get_all_relieve_btn', 'call_back', function (all_relieve_btn) {
                            self.keybaord.setPosition(all_relieve_btn)
                            self.keybaord.reveal(function () {
                                self.startCounting()
                            })
                        }));
                }
                // 区段故障解锁
                else if (btnInfo == 'sector_fault_unlock') {
                    // 调出键盘
                    self.fireEvent(
                        new mxEventObject('get_sector_fault_unlock_btn', 'call_back', function (
                            sector_fault_unlock_btn) {
                            self.keybaord.setPosition(sector_fault_unlock_btn)
                            self.keybaord.reveal(function () {
                                // 在区故解时显示全部区段
                                Object.keys(self.switchBelongSec).map(k => {
                                    var element = self.parkElementCache[k.toLowerCase()]
                                    if (element) {
                                        self.graph.model.setVisible(element, true)
                                    }
                                })
                                self.startCounting()
                            })
                        }));
                }
                // 引导总锁
                else if (btnInfo == 'all_lock') {
                    // 调出键盘
                    self.fireEvent(
                        new mxEventObject('get_all_lock_btn', 'call_back', function (
                            all_lock_btn) {
                            self.keybaord.setPosition(all_lock_btn)
                            self.keybaord.reveal(function () {
                                console.log('引导总锁index:', self.bottomButton.index)
                                self.clickPath.push(Number(self.bottomButton.index))
                                self.commitAction()
                            })
                        }));
                }
                // 引导进路
                else if (btnInfo == 'guide_road') {
                    self.fireEvent(
                        new mxEventObject('get_guide_road_btn', 'call_back', function (
                            guide_road_btn) {
                            self.keybaord.setPosition(guide_road_btn)
                            self.keybaord.reveal(function () {
                                self.startCounting()
                            })
                        }));
                }
                // 开放引导
                else if (btnInfo == 'guide_open') {
                    self.fireEvent(
                        new mxEventObject('get_guide_open_btn', 'call_back', function (
                            guide_open_btn) {
                            self.keybaord.setPosition(guide_open_btn)
                            self.keybaord.reveal(function () {
                                self.startCounting()
                            })
                        }));
                }
                // 其他
                else {
                    self.startCounting()
                }
                return
            }
            break
        }
        // 处理列车进路
        case 1: {
            if (!(btnInfo &&
                    btnInfo.cell &&
                    btnInfo.cell.elementStatus)) {
                return
            }

            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(
                    new mxEventObject(
                        'add_warning', 'msg', `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`))
            }

            if (button &&
                button.type &&
                button.type == 'la' &&
                btnInfo.uid != this.clickPath[0]) {
                if (!button.uindex) {
                    return
                }
                self.fireEvent(new mxEventObject('get_signal_name_html', 'call_back', function (html) {
                    var newHtml = html + '——调终' + btnInfo.cell.elementStatus.name;
                    self.fireEvent(
                        new mxEventObject(
                            'set_signal_html', 'html', newHtml));
                }))
                self.fireEvent(
                    new mxEventObject(
                        'add_warning',
                        'msg',
                        `${self.operationName[self.status]} ${self.clickPath[0].name}->${btnInfo.cell.elementStatus.name}`));
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                self.commitAction()
                return
            }
            break
        }
        // 处理调车进路
        case 2: {
            if (!(btnInfo && btnInfo.cell && btnInfo.cell.elementStatus)) {
                return
            }
            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(
                    new mxEventObject(
                        'add_warning', 'msg', `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            if (button && button.type && button.type == 'da' && btnInfo.uid != self.clickPath[0]) {
                if (!button.uindex) {
                    return
                }
                // 更新singal name
                self.fireEvent(new mxEventObject('get_signal_name_html', 'call_back', function (html) {
                    var newHtml = html + '——调终' + btnInfo.cell.elementStatus.name;
                    self.fireEvent(new mxEventObject('set_signal_html', 'html', newHtml));
                    var msg = `${self.operationName[self.status]} ${self.clickPath[0].name}->${btnInfo.cell.elementStatus.name}`
                    self.fireEvent(new mxEventObject('add_warning', 'msg', msg));
                }))
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                self.commitAction()
                return
            }
            break
        }

        // 引导进路
        case 3: {
            if (btnInfo == 'confirmya') {
                let newHtml = `引导进路${self.clickPath[0].name}`
                self.fireEvent(new mxEventObject('set_signal_html', 'html', newHtml));
                // self.alarmwarninglistadd(`引导进路${self.clickPath[0].name}`)
                self.commitAction()
                return
            }
            break
        }

        // 进路取消
        case 4: {
            if (!(btnInfo && btnInfo.cell && btnInfo.cell.elementStatus)) {
                return
            }
            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(new mxEventObject(
                    'add_warning', 'msg', `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后进行!`));
                return
            }

            if (button && button.type && (button.type == 'da' || button.type == 'la')) {
                if (!button.uindex) {
                    return
                }
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${self.operationName[self.status]} ${btnInfo.cell.elementStatus.name}`));
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                self.commitAction()
                return
            }
            break
        }

        // 总人解
        case 5: {
            if (!(btnInfo && btnInfo.cell && btnInfo.cell.elementStatus)) {
                return
            }
            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            if (btnInfo.cell.elementStatus.red_white ||
                btnInfo.cell.elementStatus.guaid_flash) {
                // 取消引导进路
                self.status = 5
                if (button && button.type && (button.type == 'la' || button.type == 'ya')) {
                    if (!button.uindex) {
                        return
                    }
                    var buttonla = btnInfo.cell.getSubCell('button').find(i => i.getAttribute('type') == 'la')
                    self.clickPath.push({
                        index: Number(buttonla.getAttribute('button_index')),
                        name: btnInfo.cell.elementStatus.name
                    })
                    self.fireEvent(new mxEventObject(
                        'add_warning',
                        'msg',
                        `${self.operationName[self.status]} ${btnInfo.cell.elementStatus.name}`));
                    self.commitAction()
                    return
                }
            } else if (btnInfo.cell) {
                self.status = 12
                if (button && button.type && (button.type == 'la' || button.type == 'da')) {
                    if (!button.uindex) {
                        return
                    }
                    self.clickPath.push({
                        index: Number(button.uindex),
                        name: btnInfo.cell.elementStatus.name
                    })
                    // this.fireEvent(new mxEventObject(
                    //     'add_warning',
                    //     'msg',
                    //     `${self.operationName[self.status]} ${equip.cell.elementStatus.name}`));
                    self.commitAction()
                    return
                }
            }
            break
        }
        // 道岔总定
        case 6:
            // 道岔总反
        case 7:
            // 道岔单锁
        case 8:
            // 道岔单解
        case 9:
            // 道岔封锁
        case 10:
            // 道岔解封
        case 11: {
            if (!(btnInfo && btnInfo.cell && btnInfo.cell.elementStatus)) {
                return
            }
            if (btnInfo.type == 'ca') {
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                this.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name} ${self.operationName[self.status]}`));
                self.commitAction()
                return
            }
            break
        }
        // 区段故障解锁
        case 13: {
            if (btnInfo.type == 'wc' || btnInfo.type == 'cq') {
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.type == 'wc' ? btnInfo.cell.elementStatus.name : btnInfo.name
                })
                var section_name = btnInfo.name ? btnInfo.name : btnInfo.cell.elementStatus.name
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${self.operationName[self.status]} ${section_name}`));
                self.commitAction()
                return
            }
            break
        }
        // 按钮封闭
        case 15:
            // 按钮解封
        case 16: {
            if (!(btnInfo && btnInfo.cell && btnInfo.cell.elementStatus)) {
                return
            }
            if (button && (button.type || btnInfo.type) && (button.type == 'da' || button.type == 'la' || btnInfo.type == 'wc')) {
                if (!button.uindex) {
                    return
                }
                // 不能区分是调车信号还是列车信号, 统一处理位列车信号
                let la_item = _.find(self.buttonTable, (item) => {
                    return item['name'] == btnInfo.cell.elementStatus.name && item['type'] == 'LA'
                })
                self.clickPath.push({
                    index: Number(la_item ? la_item['index'] : button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name} ${self.operationName[self.status]}`));
                self.commitAction()
                return
            }

            if (btnInfo.type == 'ca') {
                self.status = self.status == 15 ? 10 : 11
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                this.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name} ${self.operationName[self.status]}`));
                self.commitAction()
                return
            }
            break
        }
        // 引导进路办理
        case 18: {
            if (!(btnInfo &&
                    btnInfo.cell &&
                    btnInfo.cell.elementStatus)) {
                return
            }

            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            if (self.clickPath.length && button && button.type && button.type == 'la') {
                if (!button.uindex) {
                    return
                }
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name} ${self.operationName[self.status]}`));
                self.commitAction()
                return
            } else if (button && button.uindex2) {
                self.clickPath.push({
                    index: Number(button.uindex2),
                    name: btnInfo.cell.elementStatus.name
                })
                return
            }
            break
        }
        // 开放引导
        case 19: {
            if (!(btnInfo &&
                    btnInfo.cell &&
                    btnInfo.cell.elementStatus)) {
                return
            }

            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            if (button && button.uindex2) {
                self.clickPath.push({
                    index: Number(button.uindex2),
                    name: btnInfo.cell.elementStatus.name
                })
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name} ${self.operationName[self.status]}`));
                self.commitAction()
                return
            }
            break
        }
        // 变通进路
        case 20: {
            if (!(btnInfo &&
                    btnInfo.cell &&
                    btnInfo.cell.elementStatus)) {
                return
            }

            if (btnInfo.cell.elementStatus.closed == 1) {
                self.fireEvent(new mxEventObject(
                    'add_warning',
                    'msg',
                    `${btnInfo.cell.elementStatus.name}信号封锁, 请解封后在使用!`));
                return
            }

            if (button && button.type && button.type == 'la') {
                if (!button.uindex) {
                    return
                }
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
                if (self.clickPath.length == 3) {
                    self.commitAction()
                }
                return
            } else if (self.clickPath.length == 1 && button && button.type && button.type == 'da') {
                if (!button.uindex) {
                    return
                }
                self.clickPath.push({
                    index: Number(button.uindex),
                    name: btnInfo.cell.elementStatus.name
                })
            }
            break
        }
    }
}

// 发送命令并重置状态
ParkMapForXiandi.prototype.commitAction = function () {
    switch (this.status) {
        case 1:
            this.status = 0x05
            if (!this.breakStatistics[0]) {
                this.breakStatistics[0] = {
                    key: '列车进路',
                    value: 0
                }
            }
            this.breakStatistics[0].value++;
            break
        case 2:
            this.status = 0x05
            if (!this.breakStatistics[1]) {
                this.breakStatistics[1] = {
                    key: '调车进路',
                    value: 0
                }
            }
            this.breakStatistics[1].value++;
            break
        case 3:
            this.status = 0xCA
            if (!this.breakStatistics[2]) {
                this.breakStatistics[2] = {
                    key: '引导进路',
                    value: 0
                }
            }
            this.breakStatistics[2].value++;
            break
        case 4:
            this.status = 0x1A
            if (!this.breakStatistics[3]) {
                this.breakStatistics[3] = {
                    key: '进路取消',
                    value: 0
                }
            }
            this.breakStatistics[3].value++;
            break
        case 5:
            this.status = 0x45
            if (!this.breakStatistics[4]) {
                this.breakStatistics[4] = {
                    key: '进路人解',
                    value: 0
                }
            }
            this.breakStatistics[4].value++;
            break
        case 6:
            this.status = 0x25
            this.clickPath.push(0x01)
            if (!this.breakStatistics[5]) {
                this.breakStatistics[5] = {
                    key: '道岔总定',
                    value: 0
                }
            }
            this.breakStatistics[5].value++;
            break
        case 7:
            this.status = 0x25
            this.clickPath.push(0x02)
            if (!this.breakStatistics[6]) {
                this.breakStatistics[6] = {
                    key: '道岔总反',
                    value: 0
                }
            }
            this.breakStatistics[6].value++;
            break
        case 8:
            this.status = 0x25
            this.clickPath.push(0x03)
            if (!this.breakStatistics[7]) {
                this.breakStatistics[7] = {
                    key: '道岔单锁',
                    value: 0
                }
            }
            this.breakStatistics[7].value++;
            break
        case 9:
            this.status = 0x25
            this.clickPath.push(0x04)
            if (!this.breakStatistics[8]) {
                this.breakStatistics[8] = {
                    key: '道岔解锁',
                    value: 0
                }
            }
            this.breakStatistics[8].value++;
            break
        case 10:
            this.status = 0x25
            this.clickPath.push(0x05)
            if (!this.breakStatistics[9]) {
                this.breakStatistics[9] = {
                    key: '道岔单封',
                    value: 0
                }
            }
            this.breakStatistics[9].value++;
            break

        case 11:
            this.status = 0x25
            this.clickPath.push(0x06)
            if (!this.breakStatistics[10]) {
                this.breakStatistics[10] = {
                    key: '道岔解封',
                    value: 0
                }
            }
            this.breakStatistics[10].value++;
            break

        case 12:
            this.status = 0x45
            if (!this.breakStatistics[4]) {
                this.breakStatistics[4] = {
                    key: '进路人解',
                    value: 0
                }
            }
            this.breakStatistics[4].value++;
            break

        case 13:
            this.status = 0x5A
            if (!this.breakStatistics[11]) {
                this.breakStatistics[11] = {
                    key: '区段故障解锁',
                    value: 0
                }
            }
            this.breakStatistics[11].value++;
            break

        case 14:
            this.status = 0x7A
            if (!this.breakStatistics[12]) {
                this.breakStatistics[12] = {
                    key: '引导总锁',
                    value: 0
                }
            }
            this.breakStatistics[12].value++;
            break

        case 15:
            this.status = 0XB5
            this.clickPath.push(0x01)
            if (!this.breakStatistics[13]) {
                this.breakStatistics[13] = {
                    key: '按钮封闭',
                    value: 0
                }
            }
            this.breakStatistics[13].value++;
            break

        case 16:
            this.status = 0XB5
            this.clickPath.push(0x02)
            if (!this.breakStatistics[14]) {
                this.breakStatistics[14] = {
                    key: '按钮解封',
                    value: 0
                }
            }
            this.breakStatistics[14].value++;
            break
        case 18: {
            this.status = 0XCA
            if (!this.breakStatistics[18]) {
                this.breakStatistics[18] = {
                    key: '引导进路办理',
                    value: 0
                }
            }
            this.breakStatistics[18].value++
            break
        }
        case 19: {
            this.status = 0X7B
            if (!this.breakStatistics[19]) {
                this.breakStatistics[19] = {
                    key: '开放引导',
                    value: 0
                }
            }
            this.breakStatistics[19].value++
            break
        }
        case 20: {
            this.status = 0X05
            if (!this.breakStatistics[20]) {
                this.breakStatistics[20] = {
                    key: '变通进路',
                    value: 0
                }
            }
            this.breakStatistics[20].value++
            break
        }
    }

    // 列车进路和调车进路才有前置按扭
    if (0x05 != this.status) {
        this.pre_button = {}
    }

    var copy = JSON.parse(JSON.stringify({
        status: this.status,
        clickPath: this.clickPath
    }))

    this.resetStatus()

    // 重复
    if (copy.clickPath[0] == copy.clickPath[1]) {
        return
    }

    this.operation.send_interlock_cmd(copy)
}

ParkMapForXiandi.prototype.resetStatus = function () {
    this.startTime = null
    this.status = 0
    this.actionMark = Math.random()
    this.clickPath = []
}

ParkMapForXiandi.prototype.clearOldTrain = function (uid) {
    if (!this.parkElementCache[uid]) {
        return
    }
    var parentCell = this.parkElementCache[uid];
    var children = parentCell.children
    var train = undefined
    _.find(children, function (child) {
        if (child.getAttribute('type') == 'train') {
            train = child
        }
    })
    if (train) {
        self.graph.removeCells([cell])
    }
}

ParkMapForXiandi.prototype.AddTrainGroups = function (trainInfos) {
    var self = this
    self.graph.model.beginUpdate();
    var cells = []
    try {
        // 先添加train, 再添加车厢
        for (var uid in trainInfos) {
            var groups = trainInfos[uid]
            for (var key in groups) {
                trains = groups[key]

                // 看看有没有这个车
                var trainCell = self.addTrain({
                    "position": uid,
                    "park_uid": trains[0].park_uid,
                    "group_index": trains[0].group_index
                })

                if (!trainCell) {
                    console.log('add train group error!')
                    break
                }

                cells.push(trainCell)

                if (uid in this.uidTrainCache) {
                    this.uidTrainCache[uid].push(trainCell.getId())
                } else {
                    this.uidTrainCache[uid] = [trainCell.getId()]
                }

                // 添加车厢
                _.each(trains, function (train) {
                    self.addCarriage({
                        "position": trainCell.getId(),
                        "train_no": train.train_no,
                        "group_index": train.group_index
                    })
                })
                cells = cells.concat(trainCell.children)
            }
        }
    } finally {
        self.graph.model.endUpdate();
    }
    return cells
}

/**
 * 更新现车位置
 */
ParkMapForXiandi.prototype.changeTrainPosition = function (trainInfo) {
    var self = this
    var train_no = trainInfo.train_no
    // 为了兼容以前的版本，这里使用park_uid
    var uid = trainInfo.park_uid
    if (!uid) {
        // 移除车辆, 移除一个组
        this.removeCarriage(train_no)
        return
    }
    // 如果是原有的车则可能是整个车移动
    if (train_no in this.trainInfoCache) {
        var id = this.trainInfoCache[train_no]
        var cell = this.model.getCell(id)
        var train = cell.getParent()
        var carriages = train.children
        var dragCarriage = _.find(carriages, (carriage) => {
            var carriage_index = parseInt(carriage.getAttribute('carriage_index'))
            return carriage_index == 1
        })
        // 拖动整个组
        if (dragCarriage) {
            // 统一处理
            var infos = []
            var dragTrainNo = dragCarriage.getAttribute('train_no')
            var groupIndex = parseInt(train.getAttribute('group_index'))
            _.each(carriages, (carriage) => {
                var type = carriage.getAttribute('type')
                var train_no = carriage.getAttribute('train_no')
                if (type == 'train_body' || type == 'train_head' || type == 'train_tail') {
                    return
                }
                infos.push({
                    "uid": uid,
                    "train_no": train_no,
                    "carriage_index": parseInt(carriage.getAttribute('carriage_index')),
                    "drag_train_no": dragTrainNo,
                    "group_index": groupIndex
                })
            })

            // 先通知后端处理
            self.netWork.call_server_method(
                'metro_park_dispatch.cur_train_manage',
                'update_train_info', {
                    "infos": infos,
                    "location_alias": this.location
                })
        } else {
            console.log('can not find the drag carriage')
        }
    } else {
        // 如果没有则添加一个group并添加车
        var infos = {}
        infos[uid] = {
            0: [{
                'train_no': train_no,
                'group_index': 0,
                'park_uid': uid
            }]
        }
        this.initTrainPosition(infos)
    }
}
/**
 * 初始化车辆位置, 如果没有提供cur_trains则从线上去获取所有的现车信息
 */
ParkMapForXiandi.prototype.initTrainPosition = function (groupInfos) {
    var def = $.Deferred();
    var self = this;
    var location = this.location
    // 转换地址
    location = location.replace("_", "")
    if (!groupInfos) {
        this.netWork.call_server_method(
            'metro_park_dispatch.cur_train_manage',
            'get_cur_train_info_v2', {
                location_alias: location
            }).then(function (groupInfos) {
            console.log(groupInfos)
            var cells = self.AddTrainGroups(groupInfos)
            def.resolve(cells)
        }).fail(function () {
            def.reject()
        })
    } else {
        var cells = self.AddTrainGroups(groupInfos)
        def.resolve(cells)
    }
    return def
}

ParkMapForXiandi.prototype.initBusyIcons = function () {
    var self = this;
    var location = this.location
    location = location.replace("_", "")
    this.netWork.call_server_method(
        'metro_park_base.busy_board',
        'get_busy_board_info', {
            location_alias: location
        }).then(
        function (busyInfos) {
            self.graph.model.beginUpdate();
            try {
                _.each(busyInfos, function (busyInfo) {
                    var icons = busyInfo.icons
                    var uid = self.normalizeUID(busyInfo.uid)
                    _.each(icons, function (icon) {
                        self.SetBusyIconStatus({
                            "position": uid,
                            "busy_type": icon
                        })
                    })
                })
            } finally {
                self.graph.model.endUpdate();
            }
        })
}

ParkMapForXiandi.prototype.SetBusyIconStatus = function (status) {

    // 排除非本站场非法部件
    var uid = status.position
    if (!this.parkElementCache[uid]) {
        console.log('没有找一站场元素:', uid)
        return
    }

    var parentCell = this.parkElementCache[uid];
    var busyType = status.busy_type || 'construction'
    var width = this.busy_icon_width
    var height = this.busy_icon_height
    var offset = 0
    if (uid in this.busyInfos) {
        // 已经存在
        var info = this.busyInfos[uid]
        if (busyType in info) {
            return
        } else {
            // 取得位置偏移
            for (var key in info) {
                if (info[key]) {
                    offset += width + 1
                }
            }
            // 标记信息
            info[busyType] = true;
        }
    } else {
        var info = {};
        info[busyType] = true;
        this.busyInfos[uid] = info;
    }

    var x = 0
    var y = 0

    var type = parentCell.getAttribute('type')
    if (type == 'wc') {
        parentCell = parentCell.getSubCell("road")[0]
    } else {
        parentCell = parentCell.getSubCell("boundary")[0]
    }

    var tmpPosition = this.getCellPostion(parentCell)
    var defaultParent = this.graph.getDefaultParent()
    var scale = this.graph.view.scale;

    var x = tmpPosition.x
    var y = tmpPosition.y;

    // 添加busyIcon, 最后一个busyType标识了样式
    var doc = mxUtils.createXmlDocument();
    var node = doc.createElement('busyIconNode')
    var cell = this.graph.insertVertex(
        defaultParent, null, node, x + offset * scale, y - height / 2.0, width, height, busyType);

    node.setAttribute('is_busy_icon', true)
    node.setAttribute('type', 'busy_icon')
    node.setAttribute('busy_type', busyType)
    node.setAttribute('position', uid)

    // 缓存，方便操作, 显示隐藏等
    this.busyIconsCache[cell.id] = cell

    return cell
}

ParkMapForXiandi.prototype.ShowBusyIcons = function (show) {
    for (var key in self.busyIconsCache) {
        var cell = self.busyIconsCache[key]
        this.graph.model.setVisible(cell, show);
    }
}

ParkMapForXiandi.prototype.updateSwitches = function () {
    this.gloabalUpdate = true
    this.model.beginUpdate()
    try {
        // 为1的话为道岔
        for (var key in this.parkElementCache) {
            var parkElement = this.parkElementCache[key]
            var elementStatus = parkElement.elementStatus
            if (elementStatus &&
                elementStatus.type == 1) {
                this.setSwitchStatus(elementStatus.name, elementStatus)
            }
        }
    } finally {
        this.model.endUpdate()
        this.gloabalUpdate = false
    }
}

/**
 * 显示隐藏道岔区段名称
 */
ParkMapForXiandi.prototype.UpdateSwitchSectionName = function () {
    this.gloabalUpdate = true
    this.model.beginUpdate()
    try {
        // 在区故解时显示全部区段
        Object.keys(this.switchBelongSec).map(uid => {
            var parkElement = this.parkElementCache[uid.toLowerCase()]
            if (parkElement) {
                this.model.setVisible(parkElement, !this.hideSwitchSectionName)
            }
        })
    } finally {
        this.model.endUpdate()
        this.gloabalUpdate = false
    }
}

/**
 * 刷新信号机
 */
ParkMapForXiandi.prototype.UpdateSignal = function () {
    this.gloabalUpdate = true
    this.model.beginUpdate()
    try {
        for (var key in this.parkElementCache) {
            var parkElement = this.parkElementCache[key]
            var elementStatus = parkElement.elementStatus
            if (elementStatus &&
                (elementStatus.type == 3 ||
                    elementStatus.type == 4 ||
                    elementStatus.type == 5)) {
                this.setSignalStatus(elementStatus.name, elementStatus)
            }
        }
    } finally {
        this.model.endUpdate()
        this.gloabalUpdate = false
    }
}

/**
 * 刷新无道岔区段
 */
ParkMapForXiandi.prototype.udpateRailSec = function () {
    this.gloabalUpdate = true
    this.graph.model.beginUpdate()
    try {
        for (var key in this.parkElementCache) {
            var parkElement = this.parkElementCache[key]
            var elementStatus = parkElement.elementStatus
            if (elementStatus &&
                elementStatus.type == 2) {
                this.setRailSecStatus(elementStatus.name, elementStatus)
            }
        }
    } finally {
        this.graph.model.endUpdate()
        this.gloabalUpdate = false
    }
}

ParkMapForXiandi.prototype.executeInstruct = function (state) {
    var command = state.command

    // 找出按钮的index
    var uid0 = command[0].equip
    var type0 = command[0].type
    var parkElement0 = this.parkElementCache[uid0]
    var btnIndex0 = parkElement0.getSubCell('button').concat(
        parkElement0.getSubCell('light')).find(
        cell => String(cell.getAttribute('type')).toUpperCase() == type0).getAttribute(
        'button_index')

    // 取得另一个灯的index
    var uid1 = command[1].equip
    var parkElement1 = this.parkElementCache[uid1]
    var type1 = type0 // 这里之前写的时候是写错了？ 应当是command[2].type???
    var btnindex1 = parkElement1.getSubCell('button').concat(parkElement1.getSubCell('light')).find(
        cell => String(cell.getAttribute('type')).toUpperCase() == type1).getAttribute(
        'button_index')

    var clickPath = [{
        index: Number(btnIndex0),
        name: command[0].equip
    }, {
        index: Number(btnindex1),
        name: command[1].equip
    }]

    this.fireEvent(
        new mxEventObject('add_warning', 'msg', `${state.operation} ${state.start_rail}->${state.end_rail}`));

    var send_data = {
        status: 0x05,
        clickPath
    }
    console.info('%c联锁执行计划指令', 'font-size:25px;color:red;', send_data)
    this.operation.send_interlock_cmd(send_data)
}

ParkMapForXiandi.prototype.shadingSignal = function (state) {
    var uid = state.command.equip
    var parkElement = this.parkElementCache[uid]
    var type = state.command.type
    var btnIndex = parkElement.getSubCell('button').concat(parkElement.getSubCell('light')).find(
        cell => String(cell.getAttribute('type')).toUpperCase() == type).getAttribute('button_index')

    this.fireEvent(
        new mxEventObject('add_warning', 'msg', `重开${state.operation}`));

    var send_data = {
        clickPath: [{
            index: Number(btnIndex),
            name: state.command.equip
        }],
        status: 0x3A
    }
    console.info('%c联锁执行计划指令', 'font-size:25px;color:red;', send_data)
    this.operation.send_interlock_cmd(send_data)
}

ParkMapForXiandi.prototype.sendControlPlan = function () {
    if (this.disableOperation) {
        return
    }
    this.planFrameReady = true
    this.operation.cef_send_sub({
        type: "setPlanControl",
        selfcontrolplan: this.selfControlPlan,
        mdiasControl: this.mdiasControl
    })
}

ParkMapForXiandi.prototype.showTrains = function (bShow) {
    for (var uid in this.trainCache) {
        var train = this.trainCache[uid]
        this.graph.model.setVisible(train, bShow)
    }
}

ParkMapForXiandi.prototype.toggle_train_orders = function (bShow) {
    var cells = []
    for (var uid in this.trainCache) {
        var train = this.trainCache[uid]
        cells.push(train)
    }
    this.trainOnTop = !this.trainOnTop
    this.graph.orderCells(!this.trainOnTop, cells);
}