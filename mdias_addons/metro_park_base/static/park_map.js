/**
 * 给mxCell添加函数
 */
let sub_cell_cache = Object()
mxCell.prototype.getSubCell = function(name) {
    if (sub_cell_cache[name]) {
        return sub_cell_cache[name]
    }
    if (this.children) {
        let loop = cells => {
            let cell_array = []
            for (let i = 0; i < cells.length; i++) {
                if (cells[i].children) {
                    cell_array = cell_array.concat(loop(cells[i].children))
                } else if (cells[i].getAttribute('name') == name) {
                    cell_array.push(cells[i])
                }
            }
            sub_cell_cache[name] = cell_array
            return cell_array
        }
        return loop(this.children)
    } else {
        return null
    }
}

/**
 * ParkMap
 */
class ParkMap {

    /**
     * 构造函数, 通过option传入选项
     * @param {*} options 
     */
    constructor(options) {

        this.graph = {}

        // 站场图名称
        this.location = options.location

        this.interactive = options.isinteractive || false
        this.disable_pan = options.dispable_pan || false

        // 绑定的容器
        this.$el = options.$el

        // 现车管理调车计划的车辆数据
        this.current_train_state = []

        // ATS现车的车辆数据
        this.all_train_state = []

        // 手动添加的车辆信息
        this.manual_add_trains = {}

        /*** 计划进路下发相关模式控制begin */
        // 默认集控模式
        this.self_control_plan = false

        // 默认非自律控制，mdias控制false
        this.mdias_control = false
            /** 计划进路下发相关模式控制end */

        // 更新全局状态时停止渲染闪烁
        this.global_updating = false

        // 破封统计
        this.break_statistical = []

        // 按钮表
        this.bnt_table = []

        // 存放全部部件细粒度到包含道岔 区段 和信号机 按钮
        this.map_elements = {}

        //有叉区段对应道岔关系
        this.switch_blong_sector = {}

        // 列车容器cell数据
        this.train_container = {}

        // 手动添加的列车容器cell数据
        this.manual_add_train_container = {}

        // 占线版状态
        this.busy_types = []

        // 初始化联锁的连接状态
        this.interlock_state = 1

        // 初始化前置机连接状态
        this.front_machine_state = 1

        // 加载mapXML
        this.defualtxmldoc = null

        this.popid = 1

        // ats特殊规则处理 出入段线的算作场内
        this.special_dev_name_map = {};

        // 场段号
        this.rtu_id = ""

        // 全局闪烁的时间
        this.flash_million_seconds = 700

        // 缓存
        this.cache = Object()
        this.alarm_cache = Object()
        this.switch_crowded_cache = Object()
        this.train_position_cache = Object()

        // 信号灯是否闪烁
        this.gloabal_flash_key = false
            // 全局闪乐的cell
        this.flash_cells = new Set()

        this.show_train = true

        // 初始化constants
        this.init_mx_constants()

        // 加载对应站场图 xml
        this.defualtxmldoc = `/data/${location}/station.xml`

        // 初始化闪烁定时器
        this.init_flash_timer()

        $.when(
            this.load_bottom_btns(),
            this.load_btn_table(),
            this.load_switch_section_map(),
            this.load_rtu_id(),
            this.load_ats_rule()).then(() => {

        })

        // 加载xml后初始化图像
        this.initcb = () => {

            //初始化graph性状
            this.graph.setCellsSelectable(false)
            this.graph.setCellsEditable(false)

            if (dispanning) {
                this.graph.panningHandler.destroy()
            }

            //火车可移动
            this.graph.is_train_movable = true

            setTimeout(() => {
                //初始化graph完成，相关事件绑定可以进行
                graphcallback()
                    //删除loadingpic
                this.$('#loadingpic').remove()
                    //xml加载完成
                document_load_ready()
                this.blockout()
                    //矫正位置
                this.graph.scrollCellToVisible(graphentity.map_elements['centerpoint'], true)
            }, 10);

            this.graph.center()

            // 注册graph的鼠标事件处理
            this.graph.addMouseListener({
                mouseDown: function(sender, evt) {
                    if (!isinteractive) {
                        return
                    }

                    // console.log("鼠标事件", evt)

                    // 过滤鼠标右键
                    if (evt.evt.button == 2) {
                        if (evt.evt.target &&
                            evt.evt.target.className &&
                            evt.evt.target.className.indexOf &&
                            evt.evt.target.className.indexOf('placedbusyicon') > -1) {
                            // 占线板图标右键
                            if (evt.sourceState.cell && graphentity.get_cell_uid(evt.sourceState.cell)) {
                                graphentity.busytypedata = graphentity.get_cell_uid(evt.sourceState.cell)
                            }
                        }
                        return
                    }

                    // 过滤非点击区域
                    if (evt.sourceState) {
                        if (graphentity.get_cell_uid(evt.sourceState.cell)) {

                            if (!graphentity.mdias_control) {
                                return
                            }

                            let equipcell = graphentity.get_park_element_cell(evt.sourceState.cell)

                            // console.log('元件状态：', equipcell.pk_status)

                            // 获取点击按钮的联锁index
                            let uindex = evt.sourceState.cell.getAttribute('buttonindex') ? evt.sourceState.cell.getAttribute('buttonindex') : equipcell.getAttribute('buttonindex')

                            //特殊控制模式按钮
                            if (equipcell.getAttribute('type') == 'selfcontrolplan' &&
                                graphentity.mdias_control) {
                                let nc = graphentity
                                if (equipcell.getAttribute('uid') == '自控模式') {
                                    pop.confirm({
                                        title: "提示",
                                        sizeAdapt: false,
                                        content: "请确定是否切换到自控模式",
                                        button: [
                                            ["success", "确定",
                                                function(e) {
                                                    pop.close(e)
                                                    graphentity.self_control_plan = true
                                                    cef_sendSub({
                                                        type: "setPlanControl",
                                                        selfcontrolplan: true,
                                                        mdiasControl: graphentity.mdias_control
                                                    })
                                                    let cell = graphentity.map_elements['集控模式']
                                                    let light = cell.getSubCell('button')[0]
                                                    nc.set_fill_color(light, '#ffd966')
                                                    light = cell.getSubCell('light')[0]
                                                    nc.set_fill_color(light, '#000')
                                                    let cell2 = graphentity.map_elements['自控模式']
                                                    let light2 = cell2.getSubCell('button')[0]
                                                    nc.set_fill_color(light2, '#ffd966')
                                                    light2 = cell2.getSubCell('light')[0]
                                                    nc.set_fill_color(light2, '#0f0')
                                                }
                                            ],
                                            ["default", "取消",
                                                function(e) {
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
                                                function(e) {
                                                    pop.close(e)
                                                    graphentity.self_control_plan = false
                                                    cef_sendSub({
                                                        type: "setPlanControl",
                                                        selfcontrolplan: false,
                                                        mdiasControl: graphentity.mdias_control
                                                    })
                                                    let cell = graphentity.map_elements['集控模式']
                                                    let light = cell.getSubCell('button')[0]
                                                    nc.set_fill_color(light, '#ffd966')
                                                    light = cell.getSubCell('light')[0]
                                                    nc.set_fill_color(light, '#0f0')
                                                    let cell2 = graphentity.map_elements['自控模式']
                                                    let light2 = cell2.getSubCell('button')[0]
                                                    nc.set_fill_color(light2, '#ffd966')
                                                    light2 = cell2.getSubCell('light')[0]
                                                    nc.set_fill_color(light2, '#000')
                                                }
                                            ],
                                            ["default", "取消",
                                                function(e) {
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
                                return
                            }

                            //特殊按钮处理
                            if (equipcell.value.getAttribute('type') == 'BTN') {
                                //获取btntype
                                if (equipcell.getAttribute('btntype') == 'confirm') { // 非进路
                                    pop.confirm({
                                        title: "提示",
                                        sizeAdapt: false,
                                        content: equipcell.pk_status.light == 0 ? "请确定是否按下按钮！" : "请确定是否抬起按钮！",
                                        button: [
                                            ["success", "确定",
                                                function(e) {
                                                    pop.close(e)
                                                    graphentity.graphAction.buttonClick({
                                                        cell: equipcell,
                                                    }, {
                                                        type: 'BTN',
                                                        uindex,
                                                        name: equipcell.pk_status.name
                                                    }, evt.evt)
                                                }
                                            ],
                                            ["default", "取消",
                                                function(e) {
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
                                if (equipcell.getAttribute('btntype') == 'password') { // 非进路故障解锁1
                                    //调出键盘
                                    graphentity.ikeyboard.options.position.of = evt.evt
                                    graphentity.ikeyboard.reveal().insertText('')
                                    graphentity.graphAction.status = 110
                                    graphentity.graphAction.graphActionCallback = i => {
                                        graphentity.graphAction.status = 0
                                        graphentity.graphAction.buttonClick({
                                            cell: equipcell,
                                        }, {
                                            type: 'BTN',
                                            uindex,
                                            name: equipcell.pk_status.name
                                        }, evt.evt)
                                        graphentity.graphAction.graphActionCallback = null
                                    }
                                    return
                                }
                                return
                            }

                            // 点击到按钮展示覆盖物时
                            if (evt.sourceState.cell.value.getAttribute) {
                                if (evt.sourceState.cell.value.getAttribute('name') == 'fork') {
                                    equipcell.getSubCell('button').map(button => {
                                        if (button.value && button.value.getAttribute('type') &&
                                            button.value.getAttribute('type').toUpperCase() ==
                                            evt.sourceState.cell.value.getAttribute('type').toUpperCase()) {
                                            uindex = button.getAttribute('buttonindex')
                                        }
                                    })
                                }
                                if (evt.sourceState.cell.value.getAttribute('name') == 'boundary') {
                                    equipcell.getSubCell('light').map(light => {
                                        if (light.value &&
                                            light.value.getAttribute('type') &&
                                            light.value &&
                                            light.value.getAttribute('type').toUpperCase() == evt.sourceState.cell.value.getAttribute('type').toUpperCase()) {
                                            uindex = light.getAttribute('buttonindex')
                                        }
                                    })
                                }
                            }

                            // 如果是道岔区段和道岔
                            let belong_sectors = false
                            let cqid = 0
                            for (let i in graphentity.switch_blong_sector) {
                                if (graphentity.switch_blong_sector[i].includes(
                                        Number(graphentity.get_cell_uid(evt.sourceState.cell)))) {
                                    belong_sectors = true
                                    cqid = i
                                    break
                                }
                            }

                            if (belong_sectors) {
                                //如果是道岔
                                let cqindex
                                graphentity.bnt_table.map(s => {
                                    let index = s.split(' = ')[0]
                                    let name = s.split(' = ')[1]
                                    let ty = s.split(' = ')[2]
                                    if (name == cqid) {
                                        cqindex = index
                                    }
                                })

                                graphentity.graphAction.buttonClick({
                                    cell: equipcell,
                                    type: equipcell.getAttribute('type')
                                }, {
                                    name: evt.sourceState.cell.getAttribute('name'),
                                    uindex,
                                    type: evt.sourceState.cell.getAttribute('type')
                                }, evt.evt)


                                graphentity.graphAction.buttonClick({
                                    cell: equipcell,
                                    type: 'cq',
                                    name: cqid
                                }, {
                                    name: evt.sourceState.cell.getAttribute('name'),
                                    uindex: cqindex,
                                    type: evt.sourceState.cell.getAttribute('type')
                                }, evt.evt)

                                return
                            }

                            graphentity.graphAction.buttonClick({
                                cell: equipcell,
                                type: equipcell.getAttribute('type')
                            }, {
                                name: evt.sourceState.cell.getAttribute('name'),
                                uindex,
                                type: evt.sourceState.cell.getAttribute('type')
                            }, evt.evt)
                        }

                        //点击道岔区段label
                        if (evt.sourceState.cell.getAttribute('belongsector')) {
                            // console.log(evt.sourceState.cell.getAttribute('belongsector'))
                            let element_cell = graphentity.get_park_element_cell(evt.sourceState.cell)
                            let cqindex
                            graphentity.bnt_table.map(item => {
                                let ar = item.split(' = ')
                                let index = ar[0]
                                let name = ar[1]
                                let ty = ar[2]
                                if (name.toLowerCase() ==
                                    evt.sourceState.cell.getAttribute('belongsector').toLowerCase()) {
                                    cqindex = index
                                }
                            })

                            graphentity.graphAction.buttonClick({
                                cell: element_cell,
                                type: 'cq',
                                name: evt.sourceState.cell.getAttribute('belongsector')
                            }, {
                                name: evt.sourceState.cell.getAttribute('name'),
                                uindex: cqindex,
                                type: evt.sourceState.cell.getAttribute('type')
                            }, evt.evt)

                            return
                        }
                    }
                    mxLog.debug('mouseDown');
                },

                mouseMove: function(sender, evt) {
                    mxLog.debug('mouseMove');
                },

                mouseUp: function(sender, evt) {
                    mxLog.debug('mouseUp');
                }
            })

            if (this.interactive) {
                // 添加拖拽图标的放下逻辑
                let dragcallback = function(graph, evt, cell, x, y) {
                    if (!this.findtargetcell) {
                        return
                    }
                    let equipcell = graphentity.get_park_element_cell(this.findtargetcell)
                    let busy_type = Number(this.element.dataset.type)

                    graphentity.addBusyicon(equipcell, busy_type)
                }

                Array.prototype.map.call(this.$("#dragicons img"), (node_img, index) => {
                    mxUtils.makeDraggable(node_img, graphentity.graph, dragcallback, node_img.cloneNode(), -15, -15, false, false, true);
                })
            }
        }
    };

    init_graph_action() {
        let self = this
        this.graphAction = {
            // 按据类型
            buton_type_status_map: {
                'la': 1, // 列车进路 l 列车 a 按扭
                'da': 2, // 调车进路 d 调车 a 按扭
                'ya': 3 // 引导进路 y 引导 a 按扭
            },

            // 命令类型
            element_status_map: {
                'all_cancel': 4, // 进路取消
                'all_relieve': 5, // 总人解
                'switch_direct': 6, // 道岔总定
                'switch_reverse': 7, // 道岔总反
                'switch_lock': 8, // 道岔单锁
                'switch_unlock': 9, // 道岔单解
                'switch_block': 10, // 道岔封锁
                'switch_unblock': 11, // 道岔解封
                'sector_faultun_lock': 13, // 区段故障解锁
                'all_lock': 14, // 引导总锁
                'signal_block': 15, // 按钮封闭
                'signal_unblock': 16 // 按钮解封
            },

            // 对应上面的两个操作, 添加股道车辆信息添加为17
            element_op_name: [
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
                "按钮解封"
            ],

            // 操作回调
            graphActionCallback: null,

            // 操作类型
            status: 0,

            // 当前命令stamp
            action_mark: null,

            // 当前触发命令按钮路径
            clickPath: [],

            // 操作开始时间，超过失效
            startTime: null,

            // 上一次点击的进路按钮
            pre_button: {},

            // 计时函数
            start_counting() {
                this.startTime = Date.now()
                let action_mark = Math.random()
                this.action_mark = action_mark

                // 操作倒计时
                let interval_timer_id
                let interval_func = () => {
                    if (this.action_mark != action_mark) {
                        clearInterval(interval_timer_id)
                        self.$('#countingdown').html('空闲')
                        return
                    }
                    let left_time = Math.ceil((15000 - (Date.now() - this.startTime)) / 1000)
                    self.$('#countingdown').html('操作剩余时间：<span style="color:red">' + left_time + 's</span>')
                }
                interval_func()
                interval_timer_id = setInterval(interval_func, 800);

                // 15s未操作，重置为空闲状态
                setTimeout(() => {
                    if (this.action_mark != action_mark) return
                    if (Object.keys(this.pre_button).length) {
                        this.pre_button = {}
                    }
                    this.reset_status()
                }, 15000)
            },

            // 重置状态
            reset_status() {
                this.startTime = null
                this.status = 0
                this.action_mark = Math.random()
                this.clickPath = []
            },

            // 发送命令重置状态
            commit_action() {
                switch (this.status) {
                    case 1:
                        this.status = 0x05
                        if (!self.break_statistical[0]) {
                            self.break_statistical[0] = {
                                key: '列车进路',
                                value: 0
                            }
                        }
                        self.break_statistical[0].value++
                            break
                    case 2:
                        this.status = 0x05
                        if (!self.break_statistical[1]) {
                            self.break_statistical[1] = {
                                key: '调车进路',
                                value: 0
                            }
                        }
                        self.break_statistical[1].value++
                            break
                    case 3:
                        this.status = 0xCA
                        if (!self.break_statistical[2]) {
                            self.break_statistical[2] = {
                                key: '引导进路',
                                value: 0
                            }
                        }
                        self.break_statistical[2].value++
                            break
                    case 4:
                        this.status = 0x1A
                        if (!self.break_statistical[3]) {
                            self.break_statistical[3] = {
                                key: '进路取消',
                                value: 0
                            }
                        }
                        self.break_statistical[3].value++
                            break
                    case 5:
                        this.status = 0x45
                        if (!self.break_statistical[4]) {
                            self.break_statistical[4] = {
                                key: '进路人解',
                                value: 0
                            }
                        }
                        self.break_statistical[4].value++
                            break
                    case 6:
                        this.status = 0x25
                        this.clickPath.push(0x01)
                        if (!self.break_statistical[5]) {
                            self.break_statistical[5] = {
                                key: '道岔总定',
                                value: 0
                            }
                        }
                        self.break_statistical[5].value++
                            break
                    case 7:
                        this.status = 0x25
                        this.clickPath.push(0x02)
                        if (!self.break_statistical[6]) {
                            self.break_statistical[6] = {
                                key: '道岔总反',
                                value: 0
                            }
                        }
                        self.break_statistical[6].value++
                            break
                    case 8:
                        this.status = 0x25
                        this.clickPath.push(0x03)
                        if (!self.break_statistical[7]) {
                            self.break_statistical[7] = {
                                key: '道岔单锁',
                                value: 0
                            }
                        }
                        self.break_statistical[7].value++
                            break
                    case 9:
                        this.status = 0x25
                        this.clickPath.push(0x04)
                        if (!self.break_statistical[8]) {
                            self.break_statistical[8] = {
                                key: '道岔解锁',
                                value: 0
                            }
                        }
                        self.break_statistical[8].value++
                            break
                    case 10:
                        this.status = 0x25
                        this.clickPath.push(0x05)
                        if (!self.break_statistical[9]) {
                            self.break_statistical[9] = {
                                key: '道岔单封',
                                value: 0
                            }
                        }
                        self.break_statistical[9].value++
                            break
                    case 11:
                        this.status = 0x25
                        this.clickPath.push(0x06)
                        if (!self.break_statistical[10]) {
                            self.break_statistical[10] = {
                                key: '道岔解封',
                                value: 0
                            }
                        }
                        self.break_statistical[10].value++
                            break
                    case 12:
                        this.status = 0x45
                        if (!self.break_statistical[4]) {
                            self.break_statistical[4] = {
                                key: '进路人解',
                                value: 0
                            }
                        }
                        self.break_statistical[4].value++
                            break
                    case 13:
                        this.status = 0x5A
                        if (!self.break_statistical[11]) {
                            self.break_statistical[11] = {
                                key: '区段故障解锁',
                                value: 0
                            }
                        }
                        self.break_statistical[11].value++
                            break
                    case 14:
                        this.status = 0x7A
                        if (!self.break_statistical[12]) {
                            self.break_statistical[12] = {
                                key: '引导总锁',
                                value: 0
                            }
                        }
                        self.break_statistical[12].value++
                            break
                    case 15:
                        this.status = 0XB5
                        this.clickPath.push(0x01)
                        if (!self.break_statistical[13]) {
                            self.break_statistical[13] = {
                                key: '按钮封闭',
                                value: 0
                            }
                        }
                        self.break_statistical[13].value++
                            break
                    case 16:
                        this.status = 0XB5
                        this.clickPath.push(0x02)
                        if (!self.break_statistical[14]) {
                            self.break_statistical[14] = {
                                key: '按钮解封',
                                value: 0
                            }
                        }
                        self.break_statistical[14].value++
                            break
                }

                // 调车和进路才是两个按扭
                if (0x05 != this.status) {
                    this.pre_button = {}
                }

                let copy = JSON.parse(JSON.stringify({
                    status: this.status,
                    clickPath: this.clickPath
                }))

                // 重置状态
                this.reset_status()

                if (copy.clickPath[0] == copy.clickPath[1]) {
                    return
                }

                console.log('前端发出命令', copy)

                // 发送命令到联锁
                cef_send(copy)
            },

            /**
             * 处理按据点击事件
             * @param {*} park_element 
             * @param {*} button 
             * @param {*} event 
             */
            buttonClick(park_element, button, event) {
                console.log('点击按钮', park_element, button, this.status)

                // 通信中断后不可操作
                if (this.sys_black_out) {
                    return
                }

                // 清除
                if (park_element == 'clear_action') {
                    if (Object.keys(this.pre_button).length) {
                        cef_send(JSON.parse(JSON.stringify({
                            status: 0x1A,
                            clickPath: [this.pre_button]
                        })))
                    }
                    this.reset_status()
                        // 这里如果放在外层就清空
                    this.$('#signalname').html("")
                    return
                }

                switch (this.status) {

                    // 空闲时
                    case 0:
                        {
                            // closed按钮不能点
                            if (park_element &&
                                !park_element.type &&
                                park_element.cell &&
                                park_element.cell.pk_status &&
                                park_element.cell.pk_status.closed == 1) {
                                self.add_alarm(`${park_element.cell.pk_status.name}信号封锁, 请解封后在使用!`)
                                return
                            }

                            // BTN按钮
                            if (button &&
                                button.type &&
                                button.type == 'BTN') {
                                // 板桥有, 高大路无, 后续需修改为场段关联
                                let index = Number(button.uindex)
                                graphentity.add_alarm(`下发${button.name}`)

                                // if (index == 277) {
                                //     graphentity.add_alarm(`下发非进路1`)
                                // } else if (index == 278) {
                                //     graphentity.add_alarm(`下发非进路故障解锁1`)
                                // }

                                let send_data = {
                                    clickPath: [{
                                        index: index,
                                        name: park_element.cell.pk_status.name
                                    }],
                                    status: 0xAA
                                }

                                console.log('前端发出命令', send_data)
                                cef_send(send_data)
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
                                    park_element.cell.pk_status &&
                                    park_element.cell.pk_status.da_start == 1 && [0, 1].indexOf(park_element.cell.pk_status.signal_end) != -1) {
                                    let html_text = `重开${park_element.cell.pk_status.name}`
                                    self.$('#signalname').html(html_text)
                                    self.add_alarm(html_text)

                                    let send_data = {
                                        clickPath: [{
                                            index: Number(button.uindex),
                                            name: park_element.cell.pk_status.name
                                        }],
                                        status: 0x3A
                                    }

                                    console.log('前端发出命令', send_data)
                                    cef_send(send_data)
                                    return
                                }

                                let now_button = {
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                }

                                this.clickPath.push(now_button)
                                this.status = this.buton_type_status_map[button.type]
                                this.start_counting()

                                // 引导进路
                                if (button.type == 'ya') {
                                    // 引导状态发送指令
                                    if (park_element.cell.pk_status.guaid_10s) {
                                        this.commit_action()
                                        return
                                    }

                                    if (park_element.cell.pk_status.red_white) {
                                        return
                                    }

                                    // 调出键盘
                                    self.ikeyboard.options.position.of = event
                                    self.ikeyboard.reveal().insertText('')
                                    return

                                } else {
                                    // 列始 调始
                                    let new_html_txt = self.$('#signal_name').html()
                                    let new_html_text = ""
                                    if (new_html_txt.startsWith("列始") &&
                                        new_html_txt.indexOf("列终") == -1) {
                                        if (button.type == "la" && JSON.stringify(now_button) !=
                                            JSON.stringify(this.pre_button)) {
                                            new_html_text = self.$('#signal_name').html() + '—列终' + park_element.cell.pk_status.name
                                        }
                                    } else if (new_html_txt.startsWith("调始") &&
                                        new_html_txt.indexOf("调终") == -1) {
                                        if (button.type == "da" && JSON.stringify(now_button) != JSON.stringify(this.pre_button)) {
                                            new_html_text = self.$('#signal_name').html() + '—调终' + park_element.cell.pk_status.name
                                        }
                                    } else {
                                        new_html_text = button.type == 'la' ? '列始' + park_element.cell.pk_status.name : '调始' + park_element.cell.pk_status.name
                                    }
                                    if (new_html_text.length) {
                                        self.$('#signal_name').html(new_html_text)
                                        self.add_alarm(new_html_text)
                                    }
                                    this.pre_button = Object.assign({}, now_button)
                                }

                                this.commit_action()
                                return
                            }
                            // 空闲时点下其他按钮的处理
                            else if (Object.keys(this.element_status_map).includes(park_element)) {

                                this.status = this.element_status_map[park_element]

                                // 取消引导进路
                                if (park_element == 'all_relieve') {
                                    //调出键盘
                                    self.ikeyboard.options.position.of = self.$('#graphactionbtn button:nth-child(4)')
                                    self.ikeyboard.reveal().insertText('')
                                    this.graphActionCallback = i => {
                                        this.start_counting()
                                        this.graphActionCallback = null
                                    }
                                }
                                // 区段故障解锁
                                else if (park_element == 'sectorfaultunlock') {
                                    // 调出键盘
                                    graphentity.ikeyboard.options.position.of = $('#graphactionbtn button:nth-child(5)')
                                    graphentity.ikeyboard.reveal().insertText('')
                                    this.graphActionCallback = i => {
                                        // 在区故解时显示全部区段
                                        Object.keys(graphentity.switch_blong_sector).map(k => {
                                            let c = graphentity.map_elements[k.toLowerCase()]
                                            if (c) {
                                                graphentity.graph.model.setVisible(c, 1)
                                            }
                                        })
                                        this.start_counting()
                                        this.graphActionCallback = null
                                    }
                                }
                                // 引导总锁
                                else if (park_element == 'all_lock') {
                                    // 调出键盘
                                    graphentity.ikeyboard.options.position.of = $('#graphactionbtn button:nth-child(2)')
                                    graphentity.ikeyboard.reveal().insertText('')
                                    this.graphActionCallback = i => {
                                        this.clickPath.push(Number(graphentity.bottombutton.index))
                                        this.commit_action()
                                        this.graphActionCallback = null
                                    }
                                }
                                // 其他
                                else {
                                    this.start_counting()
                                }

                                return
                            }

                            // 区段占压车辆添加
                            else if (button &&
                                button.name == "road" &&
                                park_element.type == "wc" &&
                                park_element.cell.pk_status) {

                                this.status = 17 // 依次往后延
                                let section_name = park_element.cell.pk_status.name.toUpperCase()
                                let prev_train_name = ""
                                if (self.manual_add_trains.hasOwnProperty(section_name)) {
                                    prev_train_name = self.manual_add_trains[section_name]['name']
                                }

                                self.ikeyboard.options.position.of = event
                                self.ikeyboard.reveal().insertText(prev_train_name)
                                this.graphActionCallback = i => {
                                    let nowTrainName = self.ikeyboard.getValue().trim()
                                        // console.log("车辆信息:", section_name, preTrainName, nowTrainName)
                                    this.manualAddTrains(section_name, nowTrainName)
                                    self.graphActionCallback = null
                                    this.reset_status()
                                }
                            }
                            break
                        }

                        // 处理列车进路
                    case 1:
                        {
                            if (!(park_element && park_element.cell && park_element.cell.pk_status)) {
                                return
                            }
                            if (park_element.cell.pk_status.closed == 1) {
                                graphentity.add_alarm(`${park_element.cell.pk_status.name}信号封锁, 请解封后在使用!`)
                                return
                            }

                            if (button && button.type && button.type == 'la' && park_element.uid != this.clickPath[0]) {
                                if (!button.uindex) {
                                    return
                                }
                                let html_content = $('#signalname').html() + '——列终' + park_element.cell.pk_status.name
                                self.$('#signalname').html(html_content)
                                self.add_alarm(
                                    `${this.element_op_name[this.status]} ${this.clickPath[0].name}->${park_element.cell.pk_status.name}`)
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })
                                this.commit_action()
                                return
                            }
                            break
                        }

                        // 处理调车进路
                    case 2:
                        {
                            if (!(park_element &&
                                    park_element.cell &&
                                    park_element.cell.pk_status)) {
                                return
                            }
                            if (park_element.cell.pk_status.closed == 1) {
                                self.add_alarm(`${park_element.cell.pk_status.name}信号封锁, 请解封后在使用!`)
                                return
                            }
                            if (button &&
                                button.type &&
                                button.type == 'da' &&
                                park_element.uid != this.clickPath[0]) {
                                if (!button.uindex) {
                                    return
                                }
                                self.$('#signalname').html($('#signalname').html() + '——调终' + park_element.cell.pk_status.name)
                                self.add_alarm(`${this.element_op_name[this.status]} ${this.clickPath[0].name}->${park_element.cell.pk_status.name}`)
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })
                                this.commit_action()
                                return
                            }
                            break
                        }
                        // 引导进路
                    case 3:
                        {
                            if (park_element == 'confirm_ya') {
                                graphentity.add_alarm(`引导进路${this.clickPath[0].name}`)
                                this.commit_action()
                                return
                            }
                            break
                        }

                        // 进路取消
                    case 4:
                        {
                            if (!(park_element && park_element.cell && park_element.cell.pk_status)) {
                                return
                            }

                            if (park_element.cell.pk_status.closed == 1) {
                                self.add_alarm(`${park_element.cell.pk_status.name}信号封锁, 请解封后在使用!`)
                                return
                            }

                            if (button &&
                                button.type &&
                                (button.type == 'da' || button.type == 'la')) {
                                if (!button.uindex) {
                                    return
                                }
                                // graphentity.add_alarm(`${this.equip_op_name[this.status]} ${equip.cell.pk_status.name}`)
                                this.clickPath.push({
                                    // 按扭表中的位置
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })
                                this.commit_action()
                                return
                            }
                            break
                        }

                        // 总人解
                    case 5:
                        {
                            if (!(park_element &&
                                    park_element.cell &&
                                    park_element.cell.pk_status)) {
                                return
                            }

                            if (park_element.cell.pk_status.closed == 1) {
                                graphentity.add_alarm(`${park_element.cell.pk_status.name}信号封锁, 请解封后在使用!`)
                                return
                            }

                            if (park_element.cell.pk_status.red_white ||
                                park_element.cell.pk_status.guaid_flash) {
                                // 取消引导进路
                                this.status = 5
                                if (button && button.type && (button.type == 'la' || button.type == 'ya')) {
                                    if (!button.uindex) {
                                        return
                                    }
                                    let buttonla = park_element.cell.getSubCell('button').find(i => i.getAttribute('type') == 'la')
                                    this.clickPath.push({
                                            index: Number(buttonla.getAttribute('buttonindex')),
                                            name: park_element.cell.pk_status.name
                                        })
                                        // graphentity.add_alarm(`${this.equip_op_name[this.status]} ${equip.cell.pk_status.name}`)
                                    this.commit_action()
                                    return
                                }
                            } else if (park_element.cell) {
                                this.status = 12
                                if (button && button.type && (button.type == 'la' || button.type == 'da')) {
                                    if (!button.uindex) {
                                        return
                                    }
                                    this.clickPath.push({
                                            index: Number(button.uindex),
                                            name: park_element.cell.pk_status.name
                                        })
                                        // graphentity.add_alarm(`${this.equip_op_name[this.status]} ${equip.cell.pk_status.name}`)
                                    this.commit_action()
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
                    case 11:
                        {
                            if (!(park_element &&
                                    park_element.cell &&
                                    park_element.cell.pk_status)) {
                                return
                            }

                            if (park_element.type == 'ca') {
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })

                                self.add_alarm(
                                    `${park_element.cell.pk_status.name} ${this.element_op_name[this.status]}`)

                                this.commit_action()
                                return
                            }
                            break
                        }

                        // 区段故障解锁
                    case 13:
                        {
                            if (park_element.type == 'wc' || park_element.type == 'cq') {
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.type == 'wc' ? park_element.cell.pk_status.name : park_element.name
                                })
                                let section_name = park_element.cell.pk_status.name
                                graphentity.add_alarm(`${this.element_op_name[this.status]} ${section_name}`)
                                this.commit_action()
                                return
                            }
                            break
                        }
                        // 按钮封闭
                    case 15:
                        {
                            if (!(park_element && park_element.cell && park_element.cell.pk_status)) {
                                return
                            }
                            if (button && button.type && (button.type == 'da' || button.type == 'la')) {
                                if (!button.uindex) {
                                    return
                                }
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })
                                self.add_alarm(`${park_element.cell.pk_status.name} ${this.element_op_name[this.status]}`)
                                this.commit_action()
                                return
                            }
                            break
                        }
                        // 按钮解封
                    case 16:
                        {
                            if (!(park_element && park_element.cell && park_element.cell.pk_status)) {
                                return
                            }
                            if (button && button.type && (button.type == 'da' || button.type == 'la')) {
                                if (!button.uindex) {
                                    return
                                }
                                this.clickPath.push({
                                    index: Number(button.uindex),
                                    name: park_element.cell.pk_status.name
                                })
                                graphentity.add_alarm(`${park_element.cell.pk_status.name} ${this.element_op_name[this.status]}`)
                                this.commit_action()
                                return
                            }
                            break
                        }
                }
            },

            // 手动管理股道车辆信息
            manualAddTrains(section_name, train_name) {
                let nowTrainName = train_name
                let preTrainName = ""
                let preId = ""
                if (graphentity.manual_add_trains.hasOwnProperty(section_name)) {
                    preTrainName = graphentity.manual_add_trains[section_name]['name']
                    preId = graphentity.manual_add_trains[section_name]['id']
                }

                let nowId = preId ? preId : moment().valueOf()
                    // 根据输入信息, 编辑车辆信息, 并添加操作记录
                self.manual_add_trains[section_name] = {
                    "name": nowTrainName,
                    "id": nowId
                }
                localStorage.manual_add_trains = JSON.stringify(self.manual_add_trains)
                if (preTrainName != nowTrainName) { // 前后车辆数据不一致
                    if (preTrainName) { // 移除开始的车
                        $(`#manualtrain${preId}`).remove()
                    }

                    if (nowTrainName) { // 添加新的车
                        if (!self.manual_add_train_container[section_name]) {
                            let traincell = self.graph.insertVertex(self.graph.model.cells[1], null, self.map_elements['TRAIN'].cloneValue(), 0, 0, 2, 30, "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#FFFFFF;");
                            let label_txt = `<div style="visibility:unset}" class='train_container train_container_train' id="train_container_manual_${nowId}"></div>`
                            self.setLabelText(traincell, label_txt)
                            self.manual_add_train_container[section_name] = traincell

                            let road = self.map_elements[section_name].getSubCell('road')[0]
                            let GX = self.graph.view.getState(road).cellBounds.getCenterX()
                            let GY = self.graph.view.getState(road).cellBounds.getCenterY()

                            self.graph.translateCell(
                                traincell,
                                GX - traincell.geometry.x - traincell.geometry.width / 2,
                                GY - traincell.geometry.y - traincell.geometry.height - 3)
                        }

                        let train = $(`<div class='trainbk trainbknone' id='manualtrain${nowId}'>${nowTrainName}</div>`)

                        let doms = $('#VMANUAL' + nowId).append(train)
                        graphentity.graph.setAttributeForCell(
                            graphentity.manual_add_train_container[section_name],
                            'label',
                            doms.get(0).outerHTML)
                    }

                    if (graphentity.add_alarm) {
                        if (preTrainName) {
                            if (nowTrainName) {
                                graphentity.add_alarm(`${section_name}设置现车${nowTrainName}`)
                            } else {
                                graphentity.add_alarm(`${section_name}移除现车${preTrainName}`)
                            }
                        } else {
                            graphentity.add_alarm(`${section_name}设置现车${nowTrainName}`)
                        }
                    }
                }
            }
        }
    };

    /**
     * 添加图形事件监听
     */
    add_graph_event_listener() {
        this.graph.addMouseListener({
            currentState: null,
            previousStyle: null,

            mouseDown: function(sender, me) {
                // if (this.currentState != null) {
                //     this.dragLeave(me.getEvent(), this.currentState);
                //     this.currentState = null;
                // }
            },

            mouseMove: function(sender, me) {
                // if (this.currentState != null 
                //     && me.getState() == this.currentState) 
                // {
                //     return;
                // }

                // var tmp = graph.view.getState(me.getCell());

                // // Ignores everything but vertices
                // if (graph.isMouseDown || (tmp != null && !
                //     graph.getModel().isVertex(tmp.cell))) {
                //     tmp = null;
                // }

                // if (tmp != this.currentState) {
                //     if (this.currentState != null) {
                //         this.dragLeave(me.getEvent(), this.currentState);
                //     }

                //     this.currentState = tmp;

                //     if (this.currentState != null) {
                //         this.dragEnter(me.getEvent(), this.currentState);
                //     }
                // }
            },
            mouseUp: function(sender, me) {

            },

            dragEnter: function(evt, state) {
                // // 如果当前是个列车容器的话就高亮
                // if (state != null) {
                //     this.previousStyle = state.style;
                //     state.style = mxUtils.clone(state.style);
                //     updateStyle(state, true);
                //     state.shape.apply(state);
                //     state.shape.redraw();

                //     if (state.text != null) {
                //         state.text.apply(state);
                //         state.text.redraw();
                //     }
                // }
            },

            dragLeave: function(evt, state) {
                // if (state != null) {
                //     state.style = this.previousStyle;
                //     updateStyle(state, false);
                //     state.shape.apply(state);
                //     state.shape.redraw();

                //     if (state.text != null) {
                //         state.text.apply(state);
                //         state.text.redraw();
                //     }
                // }
            }
        });
    }

    /**
     * 绑定底部按扭的点击事件
     */
    bind_btn_clcick() {
        let self = this
            // 底部功能按钮事件处理，居然是按照索引来
        this.$('#graphactionbtn button.actionlevelone').click(function() {
            switch ($(this).index()) {
                case 1:
                    //引导总锁this
                    self.graphAction.buttonClick('alllock')
                    break

                case 2:
                    //总取消
                    self.graphAction.buttonClick('allcancel')
                    break

                case 3:
                    //取消引导进路
                    self.graphAction.buttonClick('allrelieve')
                    break

                case 4:
                    //区段故障解锁
                    self.graphAction.buttonClick('sectorfaultunlock')
                    break

                case 5:
                    //道岔总定
                    self.graphAction.buttonClick('switchdirect')
                    break

                case 6:
                    //道岔总反
                    self.graphAction.buttonClick('switchreverse')
                    break

                case 7:
                    //清除
                    self.graphAction.buttonClick('clear_action')
                    break

                case 8:
                    //道岔单锁
                    self.graphAction.buttonClick('switchlock')
                    break

                case 9:
                    //道岔解锁
                    self.graphAction.buttonClick('switchunlock')
                    break

                case 10:
                    //道岔解锁
                    self.graphAction.buttonClick('signalblock')
                    break

                case 11:
                    //道岔解锁
                    self.graphAction.buttonClick('signalunblock')
                    break

                case 12:
                    //道岔单封
                    self.graphAction.buttonClick('switchblock')
                    break

                case 13:
                    //道岔解封
                    self.graphAction.buttonClick('switchunblock')
                    break
            }
        })
    };

    init_keyboard() {
        let self = this
            // keyboard插件初始化
        this.$('#graph_action_hidden')
            .keyboard({
                layout: 'qwerty',
                position: {
                    of: $('#grap_haction_hidden'),
                    my: 'center top',
                    at: 'center top'
                }
            }).addTyping();

        this.ikeyboard = this.$('#graph_action_hidden').getkeyboard()
        this.$('.ui-keyboard-input').bind(
            'visible hidden beforeClose accepted canceled restricted',
            function(event, keyboard, el, status) {
                switch (event.type) {
                    case 'visible':
                        $('.covergraph').show()
                        break;
                    case 'hidden':
                        $('.covergraph').hide()
                        break;
                    case 'accepted':
                        //把点击按钮和部件发送给graphAction处理
                        if (self.graphAction.status == 17) { // 添加车辆信息
                            self.graphAction.graphActionCallback()
                        } else if (self.ikeyboard.getValue() == '123') { // 123为输入密码操作
                            switch (self.graphAction.status) {
                                case 3:
                                    self.add_alarm('引导进路口令正确')
                                    self.graphAction.buttonClick('confirm_ya')
                                    break
                                case 5:
                                    self.add_alarm('总人解口令正确')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 13:
                                    self.add_alarm('区故解口令正确')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 14:
                                    self.add_alarm('引导总锁口令正确')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 110:
                                    self.add_alarm('非进路故障解锁1口令正确')
                                    self.graphAction.graphActionCallback()
                                    break
                            }
                        } else {
                            switch (self.graphAction.status) {
                                case 3:
                                    self.add_alarm('引导进路口令错误')
                                    self.graphAction.buttonClick('confirm_ya')
                                    break
                                case 5:
                                    self.add_alarm('总人解口令错误')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 13:
                                    self.add_alarm('区故解口令错误')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 14:
                                    self.add_alarm('引导总锁口令错误')
                                    self.graphAction.graphActionCallback()
                                    break
                                case 110:
                                    self.add_alarm('非进路故障解锁1口令错误')
                                    self.graphAction.graphActionCallback()
                                    break
                            }

                            self.graphAction.reset_status()
                        }
                        break;
                    case 'canceled':
                        graphentity.graphAction.reset_status()
                        break;
                    case 'restricted':
                        break;
                    case 'beforeClose':
                        break;
                }
                this.$('#graph_action_hidden').val('')
            });
    }

    load_btn_table() {
        let self = this
        let def = $.Deferred();
        // 对应战场按钮表
        $.ajax({
            url: `/data/${location}/mapbuttonindex.json`,
            type: "GET",
            dataType: "json",
            success: function(data) {
                self.bnt_table = data
                def.resolve()
            }
        });
        return def
    }

    load_switch_section_map() {
        let self = this
        let def = $.Deferred();
        // 有叉区段对应道岔关系
        $.ajax({
            url: `/data/${location}/stationswitchbelongsector.json`,
            type: "GET",
            dataType: "json",
            success: function(data) {
                self.switch_blong_sector = data
                def.resolve()
            }
        });
        return def
    }

    load_bottom_btns() {
        let def = $.Deferred();
        // 加载图对应的底部按钮
        $.ajax({
            url: `/data/parkbottombutton/parkbottombtn.json`,
            type: "GET",
            dataType: "json",
            success: data => {
                data = data[location][0].split(' = ')
                this.bottombutton = {
                    index: data[0],
                    name: data[1],
                    type: data[2]
                };
                // 设置底部btn
                this.$('#parkbottombtn1').html(data[1])
                def.resolve()
            }
        });
        return def
    }

    /**
     * 加载rtu
     */
    load_rtu_id(location) {
        let def = $.Deferred();
        let self = this
            // 加载ats显示规则，用于判断出了站场的位置帧
        $.ajax({
            url: `/data/rtu_info/rtu_info.json`,
            type: "GET",
            dataType: "json",
            success: function(data) {
                self.rtu_id = data[location] || ""
                def.resolve()
            }
        })
        return def
    }

    /**
     * 加载ats rule
     */
    load_ats_rule(location) {
        let def = $.Deferred();
        let self = this
            // 加载ats显示规则，用于判断出了站场的位置帧
        $.ajax({
            url: `/data/${location}/atsrule.json`,
            type: "GET",
            dataType: "json",
            success: function(data) {
                self.special_dev_name_map = data
                def.resolve()
            }
        })
        return def
    };

    /**
     * 初始化资源
     */
    init_resource() {
        let def = $.Deferred();
        mxResources.loadDefaultBundle = false;
        var bundle = mxResources.getDefaultBundle(
            RESOURCE_BASE, mxLanguage) || mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);

        mxUtils.getAll([bundle, STYLE_PATH + '/default.xml', this.defualtxmldoc], xhr => {
            mxResources.parse(xhr[0].getText());
            var themes = new Object();
            themes[Graph.prototype.defaultThemeName] = xhr[1].getDocumentElement();

            this.editor_ui = new EditorUi(new Editor(urlParams['chrome'] == '0', themes), this.$el);
            this.graph = this.editor_ui.editor.graph
            this.editor = this.editor_ui.editor

            // 加载资源
            this.graph.importGraphModel(xhr[2].getDocumentElement())
            this.graph.setEnabled(!!isinteractive)

            // 取消rubber处理
            this.graph.getRubberband().destroy()

            def.resolve()
        }, function() {
            console.log('load mxgraph resource error!')
        })
        return def
    };

    /**
     * hook cell add 函数
     */
    hook_cell_add() {
        let self = this
        let _super = this.graph.getModel().cellAdded
        this.graph.getModel().cellAdded = function(cell) {
            _super.apply(this, arguments)
                // 带有uid的为站场元素
            if (cell.getAttribute('uid')) {
                self.map_elements[cell.getAttribute('uid')] = cell
                let uid = cell.getAttribute('uid').toUpperCase()
                if (uid.indexOf('BTN') > -1) {
                    uid = uid.split('BTN')[0]
                }
                // 给所有按钮添加联锁按钮index
                self.bnt_table.map(item => {
                    let ar = item.split(' = ')
                    let index = ar[0]
                    let name = ar[1]
                    let type = ar[2]

                    if (name == uid) {
                        if (cell.value.getAttribute('type') == 'BTN') {
                            cell.setAttribute('button_index', index)
                            return
                        }

                        if (cell.getSubCell('light').length == 0 &&
                            cell.getSubCell('button').length == 0) {
                            cell.setAttribute('button_index', index)
                            return
                        }

                        cell.getSubCell('light').map(light => {
                            if (light.getAttribute('type') &&
                                light.getAttribute('type').toUpperCase() == type) {
                                light.setAttribute('buttonindex', index)
                            }
                        })

                        cell.getSubCell('button').map(button => {
                            if (button.getAttribute('type') &&
                                button.getAttribute('type').toUpperCase() == type) {
                                button.setAttribute('buttonindex', index)
                            }
                        })

                        return true
                    } else {
                        return false
                    }
                })
            }

            // 保存道岔区段label
            if (cell.getAttribute('belong_sector') && !cell.children) {
                self.map_elements[cell.getAttribute('belong_sector').toLowerCase()] = cell
            }
        }
    }

    load_manual_added_train() {
        // 加载手动加载车辆数据
        if (localStorage.manual_add_trains) {
            let manual_trains = JSON.parse(localStorage.manual_add_trains)
            for (let item in manual_trains) {
                this.graphAction.manualAddTrains(item, manual_trains[item]['name'])
            }
        }
    };

    init_mx_constants() {
        mxConstants.DROP_TARGET_COLOR = '#ff0'
        mxConstants.HIGHLIGHT_OPACITY = 70
    };

    //添加占线版图标
    addBusyicon(park_element, busy_type) {
        let popid = 'confirm_pop_' + this.popid++
            let busyiconsrc
        let $el
        let devicename
        let callback

        // 检查非法部件
        if (!park_element || !park_element.pk_status) {
            return
        }

        // 在部件对象上添加一个占线版状态字典
        if (!park_element.busy_types) {
            park_element.busy_types = {}
        }

        // 已存在当前状态
        if (park_element.busy_types[busy_type]) {
            return
        }

        // console.log('占线版放下位置：', equipcell.pk_status)
        $el = this.$(park_element.getSubCell('label')[0].getAttribute('label'))
        switch (park_element.pk_status.type) {
            case 2: // 区段
                $el = $(park_element.getSubCell('road')[0].getAttribute('label'))
                devicename = '区段'
                break
            case 1: // 道岔
                devicename = '道岔'
                break
            case 3: // 出站信号
                devicename = '出站信号'
                break
            case 4: // 进站信号
                devicename = '进站信号'
                break
            case 5: // 调车信号
                devicename = '调车信号'
                break
            case 6: // 信号灯
                break
        }

        // 确认放下的回调
        on_drop = () => {
            pop.close(popid)

            //添加占线状态到当前部件对象
            park_element.busy_types[busy_type] = true
            if ($el.length == 0) {
                $el = $(`<div class='train_container ain_container_busy'></div>`)
            }

            //寻找到占线版图标src
            this.$('#dragicons img').map(function() {
                if (Number(this.dataset.type) == busy_type) {
                    busyiconsrc = this.src
                }
            })

            if (!!this.show_busy_icon) {
                $el.append(
                    $(`<img class='placedbusyicon busytype-${busy_type}' style='width:30px;display:block;height:30px;' src="${busyiconsrc}" >`))
            } else {
                $el.append(
                    $(`<img class='placedbusyicon busytype-${busy_type}' style='width:30px;display:none;height:30px;' src="${busyiconsrc}" >`))
            }

            switch (park_element.pk_status.type) {
                case 2: // 区段
                    this.graph.setAttributeForCell(
                        park_element.getSubCell('road')[0], 'label', `<div class='train_container'>${$el.html()}</div>`)
                    break
                case 1: // 道岔
                case 3: // 出站信号
                case 4: // 进站信号
                case 5: // 调车信号
                    this.graph.setAttributeForCell(
                        park_element.getSubCell('label')[0], 'label', `<div class='train_container'>${$el.html()}</div>`)
                    break
                case 6: // 信号灯
                    break
            }
        }

        // 弹出确认弹出框, 同时还需要同步到后羰
        pop.confirm({
            title: "添加占线版状态",
            sizeAdapt: false,
            content: `确定在[${park_element.pk_status.name}-${devicename}]上添加${this.busy_types[busy_type]}吗？`,
            button: [
                ["success", "确定", on_drop],
                ["default", "取消",
                    function(e) {
                        pop.close(e)
                    }
                ]
            ],
            buttonSpcl: "",
            anim: "fadeIn-zoom",
            width: 350,
            height: 180,
            id: popid,
            place: 5,
            drag: true,
            index: true,
            toClose: false,
            mask: true,
            class: false
        });
    }

    /**
     * 递归向上取得cell的id
     * @param {*} cell 
     */
    get_cell_uid(cell) {
        if (cell.getAttribute('uid')) {
            return cell.getAttribute('uid')
        } else {
            if (cell.parent != null) {
                return this.get_cell_uid(cell.parent)
            } else {
                return null
            }
        }
    }

    /**
     * 向上取得带uid的cell, 带uid的cell为站场图元素
     * @param {} cell 
     */
    get_park_element_cell(cell) {
        if (cell.getAttribute('uid')) {
            return cell
        } else {
            if (cell.parent != null) {
                return this.get_park_element_cell(cell.parent)
            } else {
                return null
            }
        }
    }

    /**
     * 调车现车管理
     */
    set_current_train_state(train_states) {

        if (!train_states) {
            return
        }

        if (!train_states.length) {
            return
        }

        train_states.map((train_state, index) => {
            let exist_train = this.current_train_state.find(x => x.name == train_state.name)
            if (exist_train) {
                this.current_train_state = this.current_train_state.filter(x => x.name != train_state.name)
            }
            this.current_train_state.push(train_state)

            /**
             * 为目标位置创建cell 如VD1G,
             * 在cell的label中放入代表列车状态的div
             */
            // 道岔区段转换为头部道岔
            if (this.switch_blong_sector[train_state.position.replace('-', '_')]) {
                train_state.position = String(this.switch_blong_sector[train_state.position.replace('-', '_')][0])
            }

            if (train_state.delete) {
                // 这里应当从container里面移除掉
                this.$(`#train${train_state.name}`).remove()
                let dom = $('#V' + this.train_position_cache[train_state.name])
                if (dom.length) {
                    this.train_container[
                        this.train_position_cache[train_state.name]].value.setAttribute(
                        'label', dom.get(0).outerHTML)
                }
            } else {
                this.setTrainStatus(train_state, 'currenttrain')
            }
        })
    }

    /**
     * 重写, 通过当前元素进行查找
     * @param {*} selector 
     */
    $(selector) {
        if (selector === undefined) {
            return this.$el;
        }
        return this.$el.find(selector);
    };

    // 设置ATS现车状态
    set_globaltrain_state(train_states) {
        if (!train_states) {
            return
        }

        if (!train_states.length) {
            return
        }

        // console.log('ATS:', trainstate)
        train_states.map((state) => {
            let existtrain = this.all_train_state.find(x => x.name == state.Train_id)

            if (existtrain) {
                this.all_train_state = this.all_train_state.filter(x => x.name != state.Train_id)
            }

            this.all_train_state.push(state)

            /**
             * 为目标位置创建cell 如VD1G,
             * 在cell的label中放入代表列车状态的div
             */

            // 判断信息合法性，排除非本站场的数据

            // 修正不一致区段名称
            let rtu_str = String(state.Rtu_id)
            let ats_dev_name = state.Dev_name
            if (rtu_str in this.special_dev_name_map) {
                if (state.Dev_name in this.special_dev_name_map[rtu_str]) {
                    state.Dev_name = this.special_dev_name_map[rtu_str][state.Dev_name]
                }
            }

            // console.log(`\n ATS现车数据：${i.Train_id} >>>> ${i.Dev_name}, @${i.Rtu_id}\n`)

            if (rtu_str == this.rtu_id ||
                (rtu_str in this.special_dev_name_map &&
                    Object.keys(this.special_dev_name_map[rtu_str]).includes(ats_dev_name))) {
                this.setTrainStatus(state)
            } else if (this.$(`#train_${state.Train_id}`).length) {
                // 删除列车逻辑，走出了转换轨且在本站存在
                this.$(`#train${state.Train_id}`).remove()
                let dom = this.$('#V' + this.train_position_cache[state.Train_id])
                let cell = this.train_container[this.train_position_cache[state.Train_id]]
                cell.value.setAttribute('label', dom.get(0).outerHTML)
            }
        })
    }

    // 设置全局状态
    set_global_state(state) {

        if (!state) {
            return
        }

        let self = this
        let model = self.graph.getModel()

        if (['DATA_SDI', 'DATA_SDCI'].includes(state['data_type'])) {
            // 设置正在全局更新, 不要进行闪烁
            this.global_updating = true
            model.beginUpdate()
            state.data.map((tmp_data, index) => {
                tmp_data.name = tmp_data.name.toUpperCase()

                // 不在graph上的dom控制，位于下方的按钮
                if (tmp_data.name == this.bottombutton.name ||
                    tmp_data.name == this.bottombutton.name + 'BTN') {
                    if (tmp_data.light) {
                        this.$('#park_bottom_btn1').css({
                            background: "#E7BA28",
                            color: "red"
                        })
                    } else {
                        // 这里是为什么呢?
                        $('body').trigger('click')
                        this.$('#park_bottom_btn1').attr('style', 'color:red')
                    }
                    return
                }

                if (!this.map_elements[tmp_data.name]) {
                    console.error('不合法名称：', tmp_data.name)
                    return
                }

                switch (tmp_data.type) {
                    case 1: // 道岔
                        self.set_switch_status(tmp_data.name, tmp_data)
                        break
                    case 2: // 区段
                        self.setSectorStatus(tmp_data.name, tmp_data)
                        break
                    case 3: // 出站信号
                    case 4: // 进站信号
                    case 5: // 调车信号
                        self.setSignalStatus(tmp_data.name, tmp_data)
                        break
                    case 6: // 信号灯
                        self.setLightStatus(tmp_data.name, tmp_data)
                        break
                    case 8: // 报警
                        if (tmp_data.value) {
                            if (!self.alarm_cache[tmp_data.name]) {
                                self.setAlarmStatus(tmp_data)
                                self.alarm_cache[tmp_data.name] = true
                            }
                        } else {
                            if (self.alarm_cache[tmp_data.name]) {
                                self.setAlarmStatus({
                                    name: tmp_data.name + '恢复'
                                })
                                self.alarm_cache[tmp_data.name] = 0
                            }
                        }
                        break
                }
            })
            model.endUpdate()
            this.global_updating = false
        }

        // 处理故障
        else if (['DATA_FIR'].includes(state['data_type'])) {
            this.$('#signal_name').html('')
                /*
                *  故障信息报告帧
                // */
                // struct FIR_NODE {
                //     BYTE op_code;           // 操作号
                //     BYTE notice_code;       // 提示信息代码
                //     WORD equip_code;        // 设备号
                //     BYTE equip_property;    // 设备性质
                //     BYTE revered;           // 预留
                // };
                // state.data.equip_code
            let equip = null

            for (let i in this.map_elements) {
                if (this.map_elements[i].pk_status &&
                    this.map_elements[i].pk_status.index == state.data.equip_code) {
                    equip = this.map_elements[i]
                }
            }

            let equiptype = [{
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

            let et = equiptype.find(p => {
                return p.type == state.data.equip_property
            })

            let equiptypeinfo = ['', '进路选不出', '信号不能保持', '命令不能执行', '信号不能开放', '灯丝断丝', '2灯丝断丝', '操作错误', '操作无效', '不能自动解锁', '进路不能闭锁']

            this.add_alarm(et.name + equip.pk_status.name + equiptypeinfo[state.data.notice_code])
        }

        // 处理状态
        else if (['DATA_RSR'].includes(state['data_type'])) {
            /*
            *  运行状态报告帧
            // */
            // struct RSR_NODE {
            //     BYTE server_status //主备机;
            //     BYTE control_status 站控非站控;
            // };
            if (state.data.server_status == 0x55) {

            } else if (state.data.server_status == 0xaa) {

            }

            if (state.data.control_status == 0x55) {
                // 自律控制绿色
                let nc = this
                let cell = this.map_elements['自律控制']
                let light = cell.getSubCell('light')[0]

                nc.set_fill_color(light, '#0f0')
                this.mdias_control = true

                if (1) {
                    let cell = this.map_elements['集控模式']
                    let light = cell.getSubCell('button')[0]

                    nc.set_fill_color(light, '#ffd966')
                    light = cell.getSubCell('light')[0]

                    let cell2 = this.map_elements['自控模式']
                    let light2 = cell2.getSubCell('button')[0]

                    nc.set_fill_color(light2, '#ffd966')
                    light2 = cell2.getSubCell('light')[0]

                    if (this.self_control_plan) {
                        nc.set_fill_color(light, '#000')
                        nc.set_fill_color(light2, '#0f0')
                    } else {
                        nc.set_fill_color(light, '#0f0')
                        nc.set_fill_color(light2, '#000')
                    }
                }
            } else if (state.data.control_status == 0xaa) {
                // 自律控制灭灯
                let nc = this
                let cell = this.map_elements['自律控制']
                let light = cell.getSubCell('light')[0]

                nc.set_fill_color(light, '#000')
                this.mdias_control = false

                if (1) {
                    let cell = this.map_elements['集控模式']
                    let light = cell.getSubCell('button')[0]

                    nc.set_fill_color(light, '#b3b3b3')
                    light = cell.getSubCell('light')[0]
                    nc.set_fill_color(light, '#000')

                    let cell2 = this.map_elements['自控模式']
                    let light2 = cell2.getSubCell('button')[0]

                    nc.set_fill_color(light2, '#b3b3b3')
                    light2 = cell2.getSubCell('light')[0]
                    nc.set_fill_color(light2, '#000')
                }
            }

            cef_send({
                type: "setPlanControl",
                selfcontrolplan: this.self_control_plan,
                mdiasControl: this.mdias_control
            })
        }

        // 通信状态
        else if (['DATA_NETINFO'].includes(state['data_type'])) {
            let nc = this
            if (state.data.type) { // 联锁
                if (this.interlock_state == state.data.status) {
                    return
                }
                this.interlock_state = state.data.status;
                if (state.data.status == 1) {
                    let cell = this.map_elements['允许MDIAS控']
                    let light = cell.getSubCell('light')[0]
                    nc.set_fill_color(light, '#000')

                    this.blockout()
                    self.setAlarmStatus({
                        name: 'MDIAS与联锁通信中断'
                    })
                } else if (state.data.status == 0) {
                    let cell = this.map_elements['允许MDIAS控']
                    let light = cell.getSubCell('light')[0]

                    nc.set_fill_color(light, '#0f0')
                    if (this.front_machine_state == 0) {
                        this.blockin()
                        self.setAlarmStatus({
                            name: 'MDIAS与联锁通信恢复'
                        })
                    }
                } else if (state.data.status == 2) {
                    this.blockout()
                    self.setAlarmStatus({
                        name: '联锁机器故障'
                    })
                } else if (state.data.status == 3) {
                    this.blockout()
                    self.setAlarmStatus({
                        name: '联锁通信数据错误'
                    })
                } else if (state.data.status == 4) {
                    self.setAlarmStatus({
                        name: '联锁协议版本不一致'
                    })
                }
            } else { // 前置机
                if (this.front_machine_state == state.data.status) {
                    return
                }
                this.front_machine_state = state.data.status;
                if (state.data.status == 1) {
                    let cell = this.map_elements['允许MDIAS控']
                    let light = cell.getSubCell('light')[0]
                    nc.set_fill_color(light, '#000')

                    this.blockout()
                    self.setAlarmStatus({
                        name: '前置机通信中断'
                    })
                } else if (state.data.status == 0) {
                    let cell = this.map_elements['允许MDIAS控']
                    let light = cell.getSubCell('light')[0]
                    nc.set_fill_color(light, '#0f0')

                    if (this.interlock_state == 0) {
                        this.blockin()
                        self.setAlarmStatus({
                            name: '前置机通信恢复'
                        })
                    }
                } else if (state.data.status == 2) {
                    this.blockout()
                    self.setAlarmStatus({
                        name: '前置机机器故障'
                    })
                } else if (state.data.status == 3) {
                    this.blockout()
                    self.setAlarmStatus({
                        name: '前置机通信数据错误'
                    })
                }
            }
        }

        // 列车位置数据
        else if (['DATA_ATS'].includes(state['data_type'])) {
            // console.log('ATSdata:', state.data)

            // 列车信息全体消息
            if (state.data.msg_id && state.data.msg_id == 9) {
                if (state.data.trains) {
                    this.set_globaltrain_state(state.data.trains)
                }
            }

            // 列车信息变化消息
            if (state.data.msg_id && state.data.msg_id == 16) {
                if (state.data) {
                    this.set_globaltrain_state([state.data])
                }
            }

            // 列车删除消息
            if (state.data.msg_id && state.data.msg_id == 17) {
                $(`#train${state.data.Train_id}`).remove()
                let doms = $('#V' + this['preposition' + state.data.Train_id])
                if (this.train_container[this['preposition' + state.data.Train_id]]) {
                    this.train_container[this['preposition' + state.data.Train_id]].value.setAttribute('label', doms.get(0).outerHTML)
                }
            }

            // 删除全体列车，由于信号断开
            // 列车删除消息
            if (state.data.msg_id === 0) {
                this.all_train_state.map(i => {
                    let Train_id = i.Train_id
                    $(`#train${Train_id}`).remove()
                    let doms = $('#V' + this['preposition' + Train_id])
                    if (this.train_container[this['preposition' + Train_id]]) {
                        this.train_container[this['preposition' + Train_id]].value.setAttribute('label', doms.get(0).outerHTML)
                    }
                })
            }
        }
    }

    // 通过id获取cell
    get_map_element_id(uid) {
        return this.map_elements[uid]
    }

    // 获取道岔或股道的中心定位点
    getroadturnoutcenter(uid) {
        uid = uid.toUpperCase()
        let road, ovdirect, ovreverse
        if (this.map_elements[uid].getAttribute('type') == 'ca') {

            ovdirect = !!this.map_elements[uid].getSubCell('direct')[0].visible
            ovreverse = !!this.map_elements[uid].getSubCell('reverse')[0].visible

            //显示出正位和反位的两条线才能获取到rotation的属性
            this.map_elements[uid].getSubCell('direct').map(x => {
                this.graph.model.setVisible(x, 1)
            })
            this.map_elements[uid].getSubCell('reverse').map(x => {
                this.graph.model.setVisible(x, 1)
            })

            if (Math.abs(this.graph.view.getState(this.map_elements[uid].getSubCell('direct')[0]).shape.rotation) > 10) {
                road = this.map_elements[uid].getSubCell('reverse')[0]
            } else {
                road = this.map_elements[uid].getSubCell('direct')[0]
            }
        } else {
            road = this.map_elements[uid].getSubCell('road')[0]
        }

        let centerx = this.graph.view.getState(road).cellBounds.getCenterX()

        this.map_elements[uid].getSubCell('direct').map(x => {
            this.graph.model.setVisible(x, ovdirect)
        })
        this.map_elements[uid].getSubCell('reverse').map(x => {
            this.graph.model.setVisible(x, ovreverse)
        })
        return centerx
    }

    // 生成目标容器
    generateVessel(position, CB, type) {
        let def = $.Deferred();
        if (this.train_container[vesselid]) {
            def.resolve()
        } else {
            let train_cell
            let train_style = "text;html=1;strokeColor=none;fillColor=none;align=center;" +
                "verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#FFFFFF;"
            if (!type) {
                // 新建股道和道岔的列车容器cell
                train_cell = this.graph.insertVertex(
                    this.graph.model.cells[1], null, this.map_elements['TRAIN'].cloneValue(), 0, 0, 2, 30, train_style);
                // 设置标签文本
                this.setLabelText(train_cell,
                    `<div style="visibility:${this.show_train_container ?
                        'unset' : 'hidden'}" class='train_container train_container_train' id="train_container_${position}"></div>`)
                this.train_container[position] = train_cell
            } else {
                // 新建股道和道岔的列车容器cell
                train_cell = this.graph.insertVertex(
                    this.graph.model.cells[1], null, this.map_elements['TRAIN'].cloneValue(), 0, 0, 2, 30, train_style);
                train_cell.value.setAttribute('istrain', 'true')
                    // 设置标签文本
                this.setLabelText(train_cell,
                    `<div style="visibility:unset" class='train_container train_container_train' id="train_container_${position}"></div>`)
                this.train_container[position] = train_cell
            }

            // 移动到股道和道岔位置
            let road, center_x, center_y, ovdirect, ovreverse
            if (this.map_elements[position].getAttribute('type') == 'ca') {
                ovdirect = !!this.map_elements[position].getSubCell('direct')[0].visible
                ovreverse = !!this.map_elements[position].getSubCell('reverse')[0].visible

                // 显示出正位和反位的两条线才能获取到rotation的属性
                this.map_elements[position].getSubCell('direct').map(x => {
                    this.graph.model.setVisible(x, 1)
                })

                this.map_elements[position].getSubCell('reverse').map(x => {
                    this.graph.model.setVisible(x, 1)
                })

                if (Math.abs(this.graph.view.getState(
                        this.map_elements[position].getSubCell('direct')[0]).shape.rotation) > 10) {
                    road = this.map_elements[position].getSubCell('reverse')[0]
                } else {
                    road = this.map_elements[position].getSubCell('direct')[0]
                }
            } else {
                road = this.map_elements[position].getSubCell('road')[0]
            }

            // 如果是股道则放到水平的那个叉上面
            center_x = this.graph.view.getState(road).cellBounds.getCenterX()
            center_y = this.graph.view.getState(road).cellBounds.getCenterY()

            if (this.map_elements[position].getAttribute('type') == 'ca') {
                this.map_elements[position].getSubCell('direct').map(cell => {
                    this.graph.model.setVisible(cell, ovdirect)
                })
                this.map_elements[position].getSubCell('reverse').map(cell => {
                    this.graph.model.setVisible(cell, ovreverse)
                })
            }

            // 移动到目标位置上面
            if (!type) {
                this.graph.translateCell(train_cell,
                    center_x - train_cell.geometry.x - train_cell.geometry.width / 2,
                    center_y - train_cell.geometry.y - train_cell.geometry.height - 3)
            } else {
                this.graph.translateCell(train_cell,
                    center_x - train_cell.geometry.x - train_cell.geometry.width / 2,
                    center_y - train_cell.geometry.y - train_cell.geometry.height)
            }

            // 保证容器已经生成
            setTimeout(() => { def.resolve() }, 10);
        }
        return def
    }

    // 列车信息, 数据格式
    // {
    //     name: 'a', //名称
    //     position: 'd37g', //位置’
    // }
    setTrainStatus(status, type) {
        if (!type) {
            status.position = status.Dev_name.replace('-', '_').replace('/', '_')
            status.name = status.Train_id

            // 排除非法部件
            if (!status.position) {
                console.log("数据没有设置位置")
                return
            }

            // 道岔区段转化
            if (this.switch_blong_sector[status.position]) {
                status.position = String(this.switch_blong_sector[status.position][0])
            }

            // 排除非法部件
            // 排除非本站场非法部件
            if (!this.map_elements[status.position]) {
                return
            }
        }

        let vesselid = status.position.toUpperCase()
        this.this.generateVessel(vesselid, type).then(() => {
            let direction = 'right'
                //根据列车上次目标点与当前目标点和方向来判定
            if (!this.train_position_cache['preposition' + status.name]) {
                //如果没有记录为第一次渲染则默认
                direction = 'trainbknone'
            } else if (this['preposition' + status.name] == status.position) {
                //如果上次位置和本次相同，直接返回
                return
            } else if (this['preposition' + status.name] != status.position) {
                //把列车从上一个位置移除,移除后保存到cell
                this.$(`#train_${status.name}`).remove()
                let doms = $('#V' + this['preposition' + status.name])
                this.train_container[this['preposition' + status.name]].value.setAttribute('label', doms.get(0).outerHTML)
                    //如果上次位置和本次不同，获取上次位置和本次位置的坐标进行比对
                if (this.getroadturnoutcenter(status.position) > this.getroadturnoutcenter(this['preposition' + status.name])) {
                    direction = 'right'
                } else {
                    direction = 'left'
                }
            }
            let train
            if (!type) {
                //生成列车
                if (direction == 'right') {
                    train = $(`<div class='trainbk' id='train${status.name}'>${status.name}</div>`)
                } else if (direction == 'trainbknone') {
                    train = $(`<div class='trainbk trainbknone' id='train${status.name}'>${status.name}</div>`)
                } else {
                    train = $(`<div class='trainbk trainbkleft' id='train${status.name}'>${status.name}</div>`)
                }
            } else {
                //生成列车
                if (status.type == 1) {
                    train = $(`<div class='trainbk ctrainbk traintype${status.status}' id='train${status.name}'>${status.name}</div>`)
                } else if (status.type == 2) {
                    train = $(`<div class='trainbk fctrainbk flattraintype${status.status}' id='train${status.name}'>${status.name}</div>`)
                }
            }
            //把列车放入目标位置label的的div中
            let doms = $('#V' + vesselid).append(train)
            this.graph.setAttributeForCell(this.train_container[vesselid], 'label', doms.get(0).outerHTML)
                //记录本次位置
            this['preposition' + status.name] = status.position.toUpperCase()
        })
    }

    /**
     * 设置报警信息
     * @param {} i 
     */
    setAlarmStatus(i) {
        if (this.$('.alarmplane div p').length >= 1000) {
            this.$('.alarmplane div p:last-child').remove()
        }
        this.$('.alarmplane div').prepend(`<p>${moment().format('MM-DD HH:mm:ss')} ${i.name}</p>`)
        this.$('.alarmplane').scrollTop(0)
    }

    /**
     * 设置道岔状态
     * @param {*} uid 
     * @param {*} status 
     */
    set_switch_status(uid, status) {
        let cell = this.get_map_element_id(uid)
        if (!cell) return

        cell.pk_status = status
            // 获取零件
        let road_entrance = cell.getSubCell('road-entrance')
        let roaddirect = cell.getSubCell('road-direct')
        let roadreverse = cell.getSubCell('road-reverse')
        let reverses_cells = cell.getSubCell('reverse')
        let direct = cell.getSubCell('direct')
        let name_labels = cell.getSubCell('label')
        let boundarys = cell.getSubCell('boundary')

        let parts = [reverses_cells, direct, roadreverse, roaddirect, road_entrance]
        parts.map(cells => {
            cells.map(cell => this.graph.model.setVisible(cell, true) + this.set_fill_color(cell, '#5578b6'))
        })

        // 重置lable颜色
        name_labels.map(label => this.setLabelText(
            label, `<div style="background:none;color:#fff;">${uid}</div>`))

        // 隐藏边框
        if (boundarys.length) {
            boundarys.map(i => {
                this.graph.model.setVisible(i, 0)
            })
        }

        // 移除闪烁
        let tmp_parts = [reverses_cells, direct]
        tmp_parts.map(cells => {
            cells.map(cell => {
                this.flash_cells.delete(cell)
                this.showcell(1)
            })
        })

        /**
         * 开始设置零件样式
         */
        if (status.switch_crowded) {
            // 挤岔
            if (!this.switch_crowded_cache[uid]) {
                this.setAlarmStatus({
                    name: `道岔${uid}#挤岔`
                })
                this.switch_crowded_cache[uid] = true
            }

            let tmp_parts = [reverses_cells, direct]
            tmp_parts.map(cells => {
                cells.map(cell => {
                    this.set_fill_color(cell, '#f00')
                    this.graph.model.setVisible(cell, true)
                    this.flash_cells.add(cell)
                })
            })
            name_labels.map(label => this.setLabelText(label, `<div style="color:#f00;">${uid}</div>`))
            return
        } else {
            if (this.switch_crowded_cache[uid]) {
                this.setAlarmStatus({
                    name: `道岔${uid}#挤岔恢复`
                })
                this.switch_crowded_cache[uid] = 0
            }
        }

        // 绿色稳定显示：表示道岔此时处于定位位置；
        if (status.pos) {
            direct.map(i => {
                if (!this.turnouttogglekey) {
                    this.set_fill_color(i, '#0f0')
                }
            })
            name_labels.map(i => this.setLabelText(i, `<div style="color:#0f0;">${uid}</div>`))
        } else {
            direct.map(i => {
                this.graph.model.setVisible(i, 0)
            })
        }

        // 黄色稳定显示：表示道岔此时处于反位位置；
        if (status.pos_reverse) {
            reverses_cells.map(i => {
                if (!this.turnouttogglekey) {
                    this.set_fill_color(i, '#ff0')
                }
            })
            name_labels.map(label => this.setLabelText(label, `<div style="color:#ff0;">${uid}</div>`))
        } else {
            reverses_cells.map(cell => {
                this.graph.model.setVisible(cell, 0)
            })
        }

        // 黑色稳定显示：表示道岔刚失去表示
        if (status.pos == 0 && status.pos_reverse == 0) {
            let parts = [reverses_cells, direct]
            parts.map(cells => {
                cells.map(cell => {
                    this.graph.model.setVisible(cell, false)
                })
            })
            name_labels.map(label => this.setLabelText(label, `<div style="color:#f00;">${uid}</div>`))
        }

        if (this.lightbeltkey) {
            let parts = [road_entrance]
            if (status.pos == 1 && status.pos_reverse == 0) {
                parts.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                parts.push(roadreverse, reverses_cells)
            }

            parts.map(cells => {
                cells.map(cell => {
                    this.set_fill_color(cell, '#ff0')
                })
            })
        }

        if (this.turnoutnamekey) {
            name_labels.map(label => this.setLabelText(label, `<div style="visibility:hidden">${uid}</div>`))
        }

        // 白色光带：道岔所在的轨道区段处于空闲锁闭状态
        if (status.hold == 0 && status.lock == 1) {
            let parts = [road_entrance]

            if (status.pos == 1 && status.pos_reverse == 0) {
                parts.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                parts.push(roadreverse, reverses_cells)
            }

            parts.map(cells => {
                cells.map(cell => {
                    this.set_fill_color(cell, '#fff')
                })
            })
        }

        // 红色光带：道岔所在的轨道区段处于占用或轨道电路故障；
        if (status.hold == 1) {
            let parts = [road_entrance]

            if (status.pos == 1 && status.pos_reverse == 0) {
                parts.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                parts.push(roadreverse, reverses_cells)
            }

            parts.map(cells => {
                cells.map(cell => {
                    this.set_fill_color(cell, '#f00')
                })
            })
        }

        if (status.closed) {
            name_labels.map(label => this.setLabelText(label,
                '<div style="border:1px solid #f00">' + label.getAttribute('label') + '</div>'))
        }

        if (status.lock_s || status.lock_protect || status.lock_gt) {
            boundarys.map(boundary => {
                this.graph.model.setVisible(boundary, true)
            })
        }

        // 预排兰光带
        if (status.pos_blue || status.reverse_blue) {
            let parts = [road_entrance]

            if (status.pos_blue == 1) {
                parts.push(roaddirect, direct)
            }

            if (status.reverse_blue == 1) {
                parts.push(roadreverse, reverses_cells)
            }

            parts.map(cells => {
                cells.map(cell => {
                    this.set_fill_color(cell, '#00f')
                })
            })
        }

        if (status.notice != 0) {
            switch (status.notice) {
                case 1:
                    this.add_alarm(`${uid} 单锁不能动`)
                    break
                case 2:
                    this.add_alarm(`${uid} 锁闭不能动`)
                    break
                case 15:
                    this.add_alarm(`${uid} 区段道岔有封闭`)
                    break
                case 16:
                    this.add_alarm(`${uid} 注意超限不满足`)
                    break
                case 17:
                    this.add_alarm(`${uid} 校核错`)
                    break
                case 18:
                    this.add_alarm(`${uid} 有车移动`)
                    break
                case 19:
                    this.add_alarm(`${uid} 不能正常解锁`)
                    break
                case 20:
                    this.add_alarm(`${uid} 紧急关闭`)
                    break
                case 21:
                    this.add_alarm(`${uid} 没锁闭`)
                    break
                case 22:
                    this.add_alarm(`${uid} 要求防护道岔不到位`)
                    break
                case 23:
                    this.add_alarm(`${uid} 不在要求位置`)
                    break
                case 24:
                    this.add_alarm(`${uid} 要求防护道岔不能动`)
                    break
                case 25:
                    this.add_alarm(`${uid} 超限不满足`)
                    break
                case 26:
                    this.add_alarm(`${uid} 不能动`)
                    break
                case 27:
                    this.add_alarm(`${uid} 封闭`)
                    break
                case 28:
                    this.add_alarm(`${uid} 锁闭`)
                    break
                case 29:
                    this.add_alarm(`${uid} 在进路中`)
                    break
                case 30:
                    this.add_alarm(`${uid} 有车占用`)
                    break
                case 31:
                    this.add_alarm(`${uid} SFJ失效`)
                    break
            }
        }
    }

    //设置区段状态
    setSectorStatus(uid, status) {
        let cell = this.get_map_element_id(uid)

        if (!cell) return

        cell.pk_status = status

        // 获取零件
        let roads = cell.getSubCell('road')
        let name_labels = cell.getSubCell('label')

        uid = uid.replace('_', '/').toUpperCase()

        // 重置显示颜色
        let allparts = [roads]
        allparts.map(cells => {
            // 空闲蓝色
            cells.map(cell => this.graph.model.setVisible(cell, 1) + this.set_fill_color(cell, '#5578b6'))
        })

        if (!this.withoutturnoutsectionkey) {
            // 重置lable颜色
            name_labels.map(label => this.setLabelText(label, `<div style="background:none;color:#fff;">${uid}</div>`))
        } else {
            // 隐藏label
            name_labels.map(label => this.setLabelText(label, `<div style="visibility:hidden">${uid}</div>`))
        }

        /*** 开始设置零件样式*/
        // 白色光带：道岔所在的轨道区段处于空闲锁闭状态
        if (status.hold == 0 && status.lock == 1) {
            roads.map(cell => {
                this.set_fill_color(cell, '#fff')
            })
        }

        // 红色光带：表示区段为占用状态或区段轨道电路故障；
        if (status.hold == 1) {
            roads.map(i => {
                this.set_fill_color(i, '#f00')
            })
        }

        // 在原有区段状态上下增加粉红色线框的光带：表示区段被人工设置为轨道分路不良标记。
        if (status.badness == 1) {
            roads.map(i => {
                this.set_stroke_color(i, '#ff9393')
            })
        }

        if (status.notice != 0) {
            switch (status.notice) {
                case 22:
                    this.add_alarm(`${uid} 照查不满足`)
                    break
                case 23:
                    this.add_alarm(`${uid} 机务段不同意`)
                    break
                case 24:
                    this.add_alarm(`${uid} 事故无驱吸起`)
                    break
                case 25:
                    this.add_alarm(`${uid} 照查错误`)
                    break
                case 26:
                    this.add_alarm(`${uid} 开通条件不满足`)
                    break
                case 27:
                    this.add_alarm(`${uid} 在进路中`)
                    break
                case 28:
                    this.add_alarm(`${uid} 不能正常解锁`)
                    break
                case 29:
                    this.add_alarm(`${uid} 占用`)
                    break
                case 30:
                    this.add_alarm(`${uid} 照查敌对`)
                    break
                case 31:
                    this.add_alarm(`${uid} 较核错`)
                    break
            }
        }
    }

    //设置状态灯状态
    setLightStatus(uid, status) {
        // BYTE light : 1;               // 亮灯
        // BYTE flash : 1;               // 闪灯
        // BYTE red : 1;                 // 红灯
        // BYTE yellow : 1;              // 黄灯
        // BYTE green : 1;               // 绿灯
        // BYTE blue : 1;                // 蓝灯
        // BYTE white : 1;               // 白灯
        // BYTE yellow2 : 1;             // 黄灯

        let cell = this.get_map_element_id(uid)
        if (!cell) return

        cell.pk_status = status

        // 根据不同种类信号机初始化,特殊信号灯比如电源灯
        if (cell.getAttribute('type')) {
            let light = cell.getSubCell('light')
            let lighto

            if (light && light.length > 0) {
                lighto = light[0]
            } else {
                lighto = cell
            }

            this.flash_cells.delete(lighto)
            this.showcell(lighto)

            if (cell.getAttribute('type') == 'lightflash') {
                this.set_fill_color(lighto, '#000')
                if (status.light) {
                    this.set_fill_color(lighto, '#f00')
                    this.flash_cells.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightyellow') {
                this.set_fill_color(lighto, '#000')
                if (status.light) {
                    this.set_fill_color(lighto, '#ff0')
                }
                if (status.flash) {
                    this.flash_cells.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'BTN') {
                this.set_fill_color(lighto, '#B3B3B3')
                if (status.light) {
                    this.set_fill_color(lighto, '#ff0')
                }
                if (status.flash) {
                    this.flash_cells.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightgreen') {
                this.set_fill_color(lighto, '#000')
                if (status.light) {
                    this.set_fill_color(lighto, '#0f0')
                }
                if (status.flash) {
                    this.flash_cells.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightwhite') {
                this.set_fill_color(lighto, '#000')
                if (status.light) {
                    this.set_fill_color(lighto, '#fff')
                }
                if (status.flash) {
                    this.flash_cells.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightgray') {
                this.set_fill_color(lighto, '#676767')
                if (status.light) {
                    this.set_fill_color(lighto, '#fff')
                }
                if (status.flash) {
                    this.flash_cells.add(lighto)
                }
                return
            }
            return
        }

        // 获取零件
        let light = cell.getSubCell('light')
        let light1, light2

        if (light && light.length && light.length > 1) {
            light1 = light.find(i => i.getAttribute('type') == 'da')
            light2 = light.find(i => i.getAttribute('type') != 'da')
        }

        // 初始化
        if (light1 && light2) {
            this.set_fill_color(light1, '#000')
            this.set_fill_color(light2, '#000')
        }

        let lighto
        if (light && light.length > 0) {
            lighto = light[0]
        } else {
            lighto = cell
        }

        this.flash_cells.delete(lighto)
        this.showcell(lighto)
        this.set_fill_color(lighto, '#000')

        if (status.light == 0 && status.flash == 0 && status.red == 0 && status.yellow == 0 && status.green == 0 && status.blue == 0 && status.white == 0 && status.yellow2 == 0) {
            if (light1 && light2) {
                this.set_fill_color(light1, '#f00')
                this.set_fill_color(light2, '#000')
            }
        }

        if (status.light) {
            this.set_fill_color(lighto, '#f00')
        }

        if (status.yellow2) {
            this.set_fill_color(lighto, '#ff0')
        }

        if (status.white) {
            this.set_fill_color(lighto, '#fff')
        }

        if (status.blue) {
            this.set_fill_color(lighto, '#00f')
        }

        if (status.green) {
            this.set_fill_color(lighto, '#0f0')
        }

        if (status.yellow) {
            this.set_fill_color(lighto, '#ff0')
        }

        if (status.red) {
            this.set_fill_color(lighto, '#f00')
            if (light1 && light2) {
                this.set_fill_color(light1, '#f00')
                this.set_fill_color(light2, '#ff0')
            }
        }

        if (status.flash) {
            this.flash_cells.add(lighto)
        }
    }

    /**
     * 设置信号机状态
     * @param {*} uid 
     * @param {*} status 
     */
    setSignalStatus(uid, status) {
        let cell = this.get_map_element_id(uid)
        if (!cell) return

        cell.pk_status = status

        // 获取零件
        let lights = cell.getSubCell('light')
        let buttons = cell.getSubCell('button')
        let name_labels = cell.getSubCell('label')
        let boundarys = cell.getSubCell('boundary')
            // fork 为覆盖物
        boundarys = boundarys.concat(cell.getSubCell('fork'))

        /**
         * 初始化所有组件
         */
        lights.map(light => {
            if (!!light.getAttribute('defaultcolor') && !this.cell_seprate_color_cache[light.id]) {
                this.cell_seprate_color_cache[light.id] = light.getAttribute('defaultcolor')
            }
            this.set_fill_color(light, this.cell_seprate_color_cache[light.id])
            this.set_stroke_color(light, '#5578b6')
        })

        // 重置lable颜色
        if (!this.delayCountdown || !this.delayCountdown[uid]) {
            if (!this.sigalnametogglekey) {
                name_labels.map(i => this.setLabelText(i, `<div style="background:none;color:#fff;">${uid}</div>`))
            } else if (this.sigalnametogglekey && status.delay_30s == 0 && status.delay_180s == 0) {
                name_labels.map(i => this.setLabelText(i, `<div style="visibility:hidden">${uid}</div>`))
            }
        }

        let button_la = buttons.find(i => i.getAttribute('type') == 'la')
        let button_ya = buttons.find(i => i.getAttribute('type') == 'ya')
        let light_da = lights.find(i => i.getAttribute('type') == 'da')
        let light0 = lights.find(i => i.getAttribute('type') != 'da')

        this.flash_cells.delete(button_la)
        this.flash_cells.delete(button_ya)
        this.flash_cells.delete(light_da)
        this.flash_cells.delete(light0)
        this.flash_cells.delete(name_labels[0])

        this.showcell(name_labels[0])
        this.showcell(button_la)
        this.showcell(button_ya)
        this.showcell(light_da)
        this.showcell(light0)

        // 加边框显示
        let condition_single_da = false
        if (buttons.length == 1 && buttons[0].getAttribute('type') == 'da') {
            condition_single_da = true
        }

        if (!boundarys.length) {
            // 获取调车灯坐标作为参考,创建一个叉
            let lightda = lights.find(i => i.getAttribute('type') == 'da')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)

                boundaryvalue.setAttribute('name', 'fork')
                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x + 3, referenceposition.y + 3, 14, 14, "shape=umlDestroy;whiteSpace=wrap;strokeWidth=2;html=1;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");

                newboundary.value = boundaryvalue
                boundarys.push(newboundary)
            }

            // 方框
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'boundary')

                // 是否有两个灯
                let newboundary
                if (lights.length == 2) {
                    // 是否在左边
                    let lightnone = lights.find(i => i.getAttribute('type') != 'da')
                    if (lightda.geometry.x > lightnone.geometry.x) {
                        newboundary = this.graph.insertVertex(
                            lightda.parent, null, '', referenceposition.x - 21, referenceposition.y, 42, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                    } else {
                        newboundary = this.graph.insertVertex(
                            lightda.parent, null, '', referenceposition.x, referenceposition.y, 42, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                    }
                } else {
                    newboundary = this.graph.insertVertex(
                        lightda.parent, null, '', referenceposition.x, referenceposition.y, 19, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                }

                newboundary.value = boundaryvalue
                newboundary.specialname = 'rect'
                boundarys.push(newboundary)
            }

            // 获取列车信号坐标作为参考, 创建一个叉
            lightda = lights.find(i => i.getAttribute('type') != 'da')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)

                boundaryvalue.setAttribute('name', 'fork')

                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x + 3, referenceposition.y + 3, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");

                newboundary.value = boundaryvalue
                boundarys.push(newboundary)
            }

            // 获取列车信号按钮坐标作为参考,创建一个叉
            lightda = buttons.find(i => i.getAttribute('type') == 'la')

            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)

                boundaryvalue.setAttribute('name', 'fork')

                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");

                newboundary.value = boundaryvalue
                boundarys.push(newboundary)
            }

            // 获取引导按钮坐标作为参考,创建一个叉
            lightda = buttons.find(i => i.getAttribute('type') == 'ya' || condition_single_da)
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)

                boundaryvalue.setAttribute('name', 'fork')

                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");

                newboundary.value = boundaryvalue
                boundarys.push(newboundary)
            }
        }

        // 隐藏边框
        if (boundarys.length) {
            boundarys.map(i => {
                this.set_stroke_color(i, '#f00')
                this.graph.model.setVisible(i, 0)
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
            if (condition_single_da) {
                boundarys.map(i => {
                    this.graph.model.setVisible(i, 1)
                })
            } else if (button_la) {
                // 有列车按钮就全部按钮红叉
                boundarys.map(i => {
                    if (i.value.getAttribute('name') == 'fork' && (i.value.getAttribute('type') == 'la' || i.value.getAttribute('type') == 'ya')) {
                        this.graph.model.setVisible(i, 1)
                    }
                })
            } else {
                // 没有列车就就把车灯红框
                boundarys.map(i => {
                    if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                        this.graph.model.setVisible(i, 1)
                    }
                })
            }
        }

        // 信号机方框显示 
        if (status.da_start == 1 && status.signal_end == 0) {
            boundarys.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    this.graph.model.setVisible(i, 1)
                    this.set_stroke_color(i, 'white')
                }
            })
        }

        if (status.da_start == 0 && status.signal_end == 1) {
            boundarys.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    this.graph.model.setVisible(i, 1)
                    this.set_stroke_color(i, '#ffff00')
                }
            })
        }

        if (status.da_start == 1 && status.signal_end == 1) {
            boundarys.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    this.graph.model.setVisible(i, 1)
                    this.set_stroke_color(i, '#00ff00')
                }
            })
        }

        // 接近锁闭
        if (status.close_lock) {
            boundarys.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    this.graph.model.setVisible(i, 1)
                    this.set_stroke_color(i, '#8B36B0')
                }
            })
        }

        if (status.red_blue) {
            lights.find(i => {
                this.set_fill_color(i, this['cellseparatecolor' + i.id])
                this.set_stroke_color(i, this['cellseparatecolor' + i.id])
            })
        }

        if (status.white) {
            if (light_da) this.set_fill_color(light_da, '#fff')
            if (light_da) this.set_stroke_color(light_da, '#fff')
        }

        if (status.guaid_flash && !status.red_white) {
            if (button_ya) this.flash_cells.add(light_da)
        }

        if (status.yellow) {
            if (button_la) this.set_fill_color(light0, '#ff0')
            if (button_la) this.set_stroke_color(light0, '#ff0')
            if (button_la) this.set_fill_color(light_da, '#000')
            if (button_la) this.set_stroke_color(light_da, 'none')
        }

        if (status.yellow_twice) {}
        if (status.green_yellow) {}

        if (status.green) {
            if (light0) this.set_fill_color(light0, '#0f0')
            if (light0) this.set_stroke_color(light0, '#0f0')
        }

        if (status.red_white) {
            if (light_da) this.set_fill_color(light_da, '#f00')
            if (light0) this.set_fill_color(light0, '#ff0')
            if (light_da) this.set_stroke_color(light_da, '#f00')
            if (light0) this.set_stroke_color(light0, '#ff0')
        }

        if (status.green_twice) {}
        if (status.train_btn_flash) {
            if (button_la) this.flash_cells.add(button_la)
        }

        if (status.ligth_broken_wire) {
            if (!this[`signallightalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `信号机${uid}灯丝断丝`
                })
                this[`signallightalarmtag${uid}`] = 1
            }
            if (light_da) {
                this.flash_cells.add(light_da)
            }
        } else {
            if (this[`signallightalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `信号机${uid}灯丝恢复`
                })
                this[`signallightalarmtag${uid}`] = 0
            }
        }

        if (status.shunt_btn_light) {
            this.flash_cells.add(name_labels[0])
        }

        if (status.delay_30s || status.delay_180s) {
            if (!this.delayCountdown) {
                this.delayCountdown = {}
            }
            //已经在倒计时中
            if (this.delayCountdown[uid]) {
                return
            }
            this.delayCountdown[uid] = true
            let remain = status.delay_30s ? 30 : 180
            let interval = setInterval(() => {

                //满足条件删除定时
                let cell = this.get_map_element_id(uid)
                let condition
                if (remain < 0) {
                    condition = true
                }
                if (!cell.pk_status.delay_30s && !cell.pk_status.delay_180s) {
                    condition = true
                }
                if (condition) {
                    clearInterval(interval)
                    this.delayCountdown[uid] = false
                    this.setSignalStatus(uid, cell.pk_status)
                } else {

                    this.delayCountdown[uid] = true
                    name_labels.map(i => {
                        this.setLabelText(i, `<div style="white-space:nowrap;background:none;color:#fff;"><span style="white-space:nowrap;background:none;color:#f00;">${remain--}s</span></div>`)
                    })
                }

            }, 1000)

            // namelabel.map(i => {
            //     this.setLabelText(i, `<div style="white-space:nowrap;background:none;color:#fff;"><span style="white-space:nowrap;background:none;color:#f00;">${uid}</span></div>`)
            //     this.globalintervalcell.add(i)
            // })
        }

        if (status.notice != 0) {
            switch (status.notice) {
                // case 1:
                // case 3:
                //     this.history_info.push(uid)
                //     break
                // case 2:
                //     this.history_info.push(uid)
                //     this.add_alarm("调车 " + this.history_info.join(" -> "))
                //     this.history_info.splice(0, this.history_info.length);
                //     break
                // case 4:
                //     this.history_info.push(uid)
                //     this.add_alarm("列车 " + this.history_info.join("->"))
                //     this.history_info.splice(0, this.history_info.length);
                case 5:
                    this.add_alarm(`变更 ${uid}`)
                    break
                case 6:
                    this.add_alarm(`重开 ${uid}`)
                    break
                    // case 7:
                    //     this.add_alarm(`引导 ${uid}`)
                    //     break
                case 8:
                    this.add_alarm(`通过 ${uid}`)
                    break
                case 9:
                    this.add_alarm(`调车取消 ${uid}`)
                    break
                case 10:
                    this.add_alarm(`列车取消 ${uid}`)
                    break
                case 11:
                    this.add_alarm(`调车人解 ${uid}`)
                    break
                case 12:
                    this.add_alarm(`列车人解 ${uid}`)
                    break
                case 17:
                    this.add_alarm(`红灯断丝 ${uid}`)
                    break
                case 18:
                    this.add_alarm(`灯丝断丝 ${uid}`)
                    break
                case 19:
                    this.add_alarm(`有车移动 ${uid}`)
                    break
                case 20:
                    this.add_alarm(`有迎面解锁可能 ${uid}`)
                    break
                case 21:
                    this.add_alarm(`非正常关闭 ${uid}`)
                    break
                case 22:
                    this.add_alarm(`不能取消 ${uid}`)
                    break
                case 23:
                    this.add_alarm(`不能通过 ${uid}`)
                    break
                case 24:
                    this.add_alarm(`不能引导 ${uid}`)
                    break
                case 25:
                    this.add_alarm(`${uid} 不是列终`)
                    break
                case 26:
                    this.add_alarm(`${uid} 不是列始`)
                    break
                case 27:
                    this.add_alarm(`${uid} 不是调终`)
                    break
                case 28:
                    this.add_alarm(`${uid} 不是调始`)
                    break
                case 29:
                    this.add_alarm(`${uid} 不构成进路`)
                    break
                case 30:
                    this.add_alarm(`${uid} 不能开放`)
                    break
                case 31:
                    this.add_alarm(`${uid} 无驱开放`)
                    break
            }
        }
    }

    /**
     * 显示隐藏cell
     * @param {*} cell 
     */
    showcell(cell) {
        if (cell && cell.setVisible) {
            this.graph.model.setVisible(cell, true)
        }
    }

    // 换label的文字html, 应当直接设置label就可以吧
    setLabelText(cell, label) {
        let oldvalue = cell.cloneValue()
        oldvalue.setAttribute('label', label)
        this.graph.model.setValue(cell, oldvalue)
    }

    /**
     * 更换cell颜色
     * @param {*} cell 
     * @param {*} color 
     * @param {*} is_flash 
     */
    set_fill_color(cell, color, is_flash) {
        if (!cell) {
            console.log("set fill color of empty cell!")
            return
        }

        if (is_flash) {
            this.color_cache[ell.id] = color
        }

        let old_style = this.graph.model.getStyle()
        let newStyle = mxUtils.setStyle(old_style, mxConstants.STYLE_FILLCOLOR, color);
        this.graph.model.setStyle(cell, newStyle)
    }

    // 换cell的边框颜色
    set_stroke_color(cell, color) {
        if (!cell) {
            console.log("set stroke of empty cell!")
            return
        }
        let old_style = this.graph.model.getStyle()
        let newStyle = mxUtils.setStyle(old_style, mxConstants.STYLE_FILLCOLOR, color);
        this.graph.model.setStyle(cell, newStyle)
    }

    init_flash_timer() {
        // 如果离开站场图页面需要清除定时器
        this.flash_timer = setInterval(() => {
            // 如果正在全局初始化或是没有闪烁的内容
            if (this.global_updating || !this.flash_cells.size) {
                return
            }

            this.graph.getModel().beginUpdate()
            for (let cell of this.flash_cells) {
                // 使用mxgraphmodel来对cell进行更新会直接刷新界面，效率更高
                let labeljdom = $(cell.getAttribute('label'))
                if (this[`oldfillcolor${cell.id}`]) {
                    if (this.gloabal_flash_key) {
                        this.set_fill_color(cell, '#000', true)
                    } else {
                        this.set_fill_color(cell, this[`oldfillcolor${cell.id}`])
                    }
                } else if (labeljdom.attr('class') == 'train_container') {
                    if (this.gloabal_flash_key) {
                        labeljdom.find('span').css({
                            'visibility': 'hidden'
                        })
                    } else {
                        labeljdom.find('span').css({
                            'visibility': 'unset'
                        })
                    }
                    this.graph.model.setVisible(cell, 1)
                    this.graph.setAttributeForCell(cell, 'label', `<div class='train_container'>${labeljdom.html()}</div>`)

                } else {
                    this.graph.model.setVisible(cell, this.gloabal_flash_key)
                }
            }
            this.graph.getModel().endUpdate()
            this.gloabal_flash_key = !this.gloabal_flash_key
        }, this.flash_million_seconds);
    };

    /**
     * 通过壳子去获取socketio配置
     */
    get_socketio_server_config() {
        var def = $.Deferred();
        if (window.cefQuery) {
            window.cefQuery({
                request: JSON.stringify({
                    cmd: "get_socketio_server_config"
                }),
                persistent: false,
                onSuccess: function(config) {
                    def.resolve(config)
                },
                onFailure: function(error_code, error_message) {
                    def.reject('获取地址错误，请检查!')
                }
            });
        } else {
            def.reject()
        }
        return def
    }

    /**
     * 初始化socketio
     */
    init_socketio() {
        let self = this;
        this.get_socketio_server_config().then((config) => {
            config = JSON.parse(config);
            let host = config.host;
            // 连接服务器的时候就加入xing_hao_lou这个room
            this.socket = io(host, {
                transports: ['websocket']
            });
            this.socket.on('on_train_position', function(data) {
                let ret = data.data;
                self.set_current_train_state(ret)
            });
            this.init_train_position()
        })
    }

    /**
     * 调用服务器方法
     * @param {*} model 
     * @param {*} method 
     * @param {*} data 
     */
    call_server_method(model, method, data) {
        let def = $.Deferred();
        try {
            this.socket.emit('funenc_socketio_client_msg', {
                "msg_type": 'call',
                "model": model,
                "name": method,
                "kwargs": data
            }, function(rst) {
                def.resolve(rst)
            })
        } catch (error) {
            def.reject(error)
        }
        return def
    }

    /**
     * 初始化现车位置
     */
    init_train_position() {
        let self = this;
        this.call_server_method('metro_park_dispatch.cur_train_manage', 'get_cur_train_map_info', {
            'location_alia': this.location
        }).then(function(ret) {
            self.set_current_train_state(ret);
        })
    };

    /**
     * 去除置灰
     */
    blockin() {
        this.sysblackout = false
        this.$('#black_out_grays').remove()
    };

    /**
     * 站场图置灰, 通过添加样式使界面变灰
     */
    blockout() {
        this.sysblackout = true
        if (!this.$('#blackoutgrays')) {
            $('head').append($(`<style id='blackoutgrays'>
            .geDiagramContainer {
                filter: grayscale(100%);
                -webkit-filter: grayscale(100%);
                -moz-filter: grayscale(100%);
                -ms-filter: grayscale(100%);
                -o-filter: grayscale(100%);
                filter: progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);
                -webkit-filter: grayscale(1)
            }
            </style>`))
        }
    };

    add_alarm() {
        // 超出100行则移除掉最后一行
        if (this.$('.alarm_pannel p').length >= 1000) {
            thisl.$('.alarm_pannel p:last-child').remove()
        }
        let record = `${moment().format("YY-MM-DD HH:mm:ss")}:      ${s}`

        // 警报窗口
        this.$('.alarm_pannel').prepend(`<p>${record}</p>`)
        this.$('.alarm_pannel').scrollTop(10000)

        // 状态栏
        this.$('.status_txt span').html(record)
    };

    /**
     * 刷新显示道岔
     */
    refreshturnou() {
        let model = this.graph.getModel()
        this.global_updating = true
        model.beginUpdate()
        for (let i in this.map_elements) {
            if (this.map_elements[i].element_info &&
                this.map_elements[i].element_info.type == 1) {
                this.setTurnoutStatus(this.map_elements[i].element_info.name, ngname.map_elements[i].element_info)
            }
        }
        model.endUpdate()
        this.global_updating = false
    };

    /**
     * 刷新显示信号机
     */
    refreshsingalsignal() {
        let model = this.graph.getModel()
        this.global_updating = true

        model.beginUpdate()
        for (let i in ngname.map_elements) {
            if (ngname.map_elements[i].element_info &&
                (ngname.map_elements[i].element_info.type == 3 ||
                    ngname.map_elements[i].element_info.type == 4 ||
                    ngname.map_elements[i].element_info.type == 5
                )) {
                this.setSignalStatus(ngname.map_elements[i].element_info.name, ngname.map_elements[i]
                    .element_info)
            }
        }
        model.endUpdate()

        this.global_updating = false
    }
}