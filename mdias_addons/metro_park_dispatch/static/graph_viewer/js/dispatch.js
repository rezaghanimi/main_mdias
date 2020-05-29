function leaveWarning() {
    return "请不要关闭此窗口!";
}

Array.prototype.remove = function (val) {
    let index = this.indexOf(val);
    if (index > -1) {
        this.splice(index, 1);
    }
}

window.cef_get_map_state = (data) => {
    if (!window.cefQuery) {
        window.cefQuery = i => {}
    }
    window.cefQuery({
        request: JSON.stringify({
            cmd: "commit_action",
            data: {
                "cmd": "get_map_state",
                "data": {}
            }
        }),
        persistent: false,
    })
}

window.format_speak_msg = (data) => {
    let special_key = {
        '1': '幺',
        '2': '两',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '拐',
        '8': '八',
        '9': '九',
        '0': '洞',
        '调': '掉'
    }

    for (let key in special_key) {
        let regexp = new RegExp(key, 'g')
        data = data.replace(regexp, special_key[key])
    }

    return data
}

window.cef_speak_msg = (data) => {
    if (!window.cefQuery) {
        window.cefQuery = i => {}
    }

    window.cefQuery({
        request: JSON.stringify({
            cmd: "tts_speak",
            txt: format_speak_msg(data)
        }),
        persistent: false,
    })
}

/**
 * 禁止缩放
 */
$(document).ready(function () {
    // chrome 浏览器直接加上下面这个样式就行了，但是ff不识别
    $('body').css('zoom', 'reset');

    $(document).keydown(function (event) {
        //event.metaKey mac的command键
        if ((event.ctrlKey === true || event.metaKey === true) &&
            (event.which === 61 || event.which === 107 ||
                event.which === 173 || event.which === 109 ||
                event.which === 187 || event.which === 189)) {
            event.preventDefault();
        }
    });

    $(window).bind('mousewheel DOMMouseScroll', function (event) {
        if (event.ctrlKey === true || event.metaKey) {
            event.preventDefault();
        }
    });

    Vue.prototype.$moment = moment

    /**
     * selfcontrolplan == true
     * 如果集控模式则隐藏调车列表按钮
     * 如果手动模式则点击排列进路确定后发送进路
     * 弹出倒计时框触发进路
     *
     * 接车计划）
     * 收到ats车到转换轨则触发
     * 发车计划）
     * 倒计时发车
     * 调车车计划）
     * 倒计时发车
     * 计划完成后都会取一条挂起列表中的计划
     */
    new Vue({
        el: '.dispatch_list',
        data() {
            return {
                // 收发车计划
                train_in_out_plans: [],

                // 调车计划
                dispatch_plans: [],

                map_name: "gaodalu",
                location: "gaodalu",

                time_out_plan: [],

                instruct_status_monitors: [],

                // 自控 或 集控
                selfcontrolplan: false,

                mdiasControl: false,

                system_logs: [],

                // socketio
                socket: undefined,

                // 全局帧缓存
                sdi_data: [],

                // 条件不满足时,待执行计划
                wait_execute_plan: [],
                wait_timer: undefined,

                // 冲突检测规则
                conflict_rules: {},

                // 双动道岔
                double_acting_switch: [],

                plan_type_name: {
                    'train_dispatch': '调车',
                    'train_back': '收车',
                    'train_out': '发车'
                },

                // 别名
                alias_name: {},

                // 提示弹框列表
                notify_list: {}
            }
        },

        beforeMount() {
            if (location.search.indexOf('mapname') > 0) {
                this.map_name = location.search.split('=')[1]
                this.location = this.map_name
            }

            let self = this

            // 转换轨和照查对应关系
            $.ajax({
                url: `/station_data/${this.location}/conflict_rules.json`,
                type: "GET",
                dataType: "json",
                success: function (data) {
                    self.conflict_rules = data
                    self.double_acting_switch = data.double_acting_switch
                }
            });

            // 别名
            $.ajax({
                url: `/station_data/${this.location}/alias_name.json`,
                type: "GET",
                dataType: "json",
                success: function (data) {
                    self.alias_name = data
                }
            });
        },

        mounted() {
            // 启动冲突检测定时器
            this.start_conflict_timer();

            window.get_vue_data = () => {
                return this
            }

            // 接收cef发送过来的数据
            window.set_global_state = state => {
                this.change_global_state(state)
            }

            // 手动获取一次全局帧
            cef_get_map_state()

            // 取得控制模式
            this.send_to_main_wnd({
                type: "getControlPlan"
            })

            // 取得服务器配置，然后连接socketio
            this.get_socketio_server_config().then((config) => {
                config = JSON.parse(config)
                let host = config.host
                // 连接服务器的时候就加入xing_hao_lou这个room
                this.socket = io(host, {
                    transports: ['websocket'],
                    query: {
                        room: 'xing_hao_lou'
                    }
                });

                this.socket.on('connect', () => {
                    this.system_log('websocket 已经连接!')
                    this.get_all_plans()
                });

                this.socket.on('funenc_socketio_server_msg', (data, callback) => {
                    let msg = data.data
                    let location = data.data.location

                    // 接收计划, 由于一次接收多条, 所以从数据中去过滤位置
                    if (msg.msg_type == "add_plan") {
                        this.system_log('收到后端添加计划指令!')
                        this.resolve_train_plan(msg.msg_data)
                        if (callback) {
                            callback(msg.msg_data, this.map_name)
                        }
                    }
                    // 变更计划, 更新dispatch_plans->instructs中为待执行状态的记录
                    else if (msg.msg_type == "change_plan") {
                        this.system_log('收到后端新的变更计划指令!')
                        let new_plans = msg.msg_data
                        this.resolve_onchang_train_plan(new_plans)
                        if (callback) {
                            callback(msg.msg_data, this.map_name)
                        }
                    }

                    // 司机手持短调车操作
                    else if (msg.msg_type == "request_start_plan") {
                        let plan = this.dispatch_plans.find(x => {
                            return x.id == msg.msg_data.request_id && x.type == "train_dispatch"
                        })

                        if (plan) {
                            // execute_request_dispatch 请求调车
                            // execute_start_dispatch 开始执行
                            // execute_finished_dispatch 车已经停稳
                            let cmd_type = msg.msg_data.cmd_type
                            if (cmd_type) {
                                let instruct = plan.instructs.find(item => {
                                    return item.id == msg.msg_data.instruct_id
                                })
                                if (instruct) {
                                    let text_info = this.get_instruct_desc(plan, instruct)
                                    if (cmd_type == "execute_request_dispatch") {
                                        text_info = `司机请求调车${text_info}`
                                        instruct.condition = "请求中"
                                        this.execute_plan(plan)
                                    } else if (cmd_type == "execute_start_dispatch") {
                                        text_info = `司机确认${text_info}已动车`
                                        instruct.condition = "已动车"
                                    } else if (cmd_type == "execute_finished_dispatch") {
                                        text_info = `司机确认${text_info}车已停稳`
                                        instruct.condition = "已停稳"
                                    }
                                    this.show_message_box(text_info);
                                    this.system_log(text_info)
                                    cef_speak_msg(text_info)
                                } else {
                                    this.system_log("未找到司机请求的钩计划")
                                }
                            }
                        }
                    }

                    // 如果位置不同则不接收, 删除、更新等从消息中去处理
                    else if (location != this.location) {
                        return
                    }

                    // 执行收车计划
                    else if (msg.msg_type == "excute_plan") {
                        if (callback) {
                            console.log('call callback')
                            callback(msg.msg_data, this.map_name)
                        }

                        if (this.mdiasControl) {
                            if (this.selfcontrolplan) {
                                let plan = this.train_in_out_plans.concat(this.dispatch_plans).find(x => {
                                    return x.id == msg.msg_data.id && x.type == msg.msg_data.type
                                })
                                if (plan && plan.type == "train_back" && !('executed' in plan)) {
                                    this.execute_plan(plan)
                                    plan['executed'] = true
                                    this.system_log(`收到执行${this.get_plan_desc(plan)}命令!`)
                                }
                            } else {
                                this.show_message_box(`当前模式为非自控模式，无法自动执行计划!`)
                            }
                        } else {
                            this.show_message_box(`当前非MDIAS控制模式，无法执行计划!`)
                        }
                    }

                    // 撤回计划 取消/删除计划
                    else if (["reback_plan", "delete_plan"].includes(msg.msg_type)) {
                        msg.msg_data.map(p => {
                            p.operation = 'delete'
                        })
                        this.resolve_train_plan(msg.msg_data)
                    }

                    // 后台未创建对应收车计划
                    else if (msg.msg_type == "notice_no_plan") {
                        this.show_message_box(`${msg.msg_data.train_id}车回场段, 未找到对应的收车计划, 请通知场调创建!`, "error")
                    } else {
                        console.log("未知的消息类型!")
                    }
                });

                this.socket.on('disconnect', () => {
                    this.system_log("websocket 已断开!")
                });
            });
        },

        methods: {
            // 获取所有计划
            get_all_plans() {
                // 发送消息到服务器，取得所有的计划
                this.socket.emit('funenc_socketio_client_msg', {
                    "msg_type": 'call',
                    "model": 'funenc.socket_io',
                    "name": "get_all_unfinished_plan",
                    "kwargs": {
                        "location_alias": this.map_name
                    }
                }, (state) => {
                    // console.log('取得计划数据成功:', state)
                    this.sio_log('取得计划成功!')
                    this.system_log('取得计划成功!')
                    this.resolve_train_plan(state)
                })
            },

            // 撤回计划
            reback_plan(plan) {
                this.sio_log(`撤回计划 ${plan.id}`);
                let model_name = undefined
                if (plan.type == "train_out") { // 发车
                    model_name = "metro_park_dispatch.train_out_plan"
                } else if (plan.type == "train_back") { // 收车
                    model_name = "metro_park_dispatch.train_back_plan"
                } else if (plan.type == "train_dispatch") { //调车
                    model_name = "metro_park_dispatch.dispatch_request"
                } else {
                    this.sio_log(`未知的计划类型 ${JSON.stringify(plan)}`)
                    return
                }

                this.call_server_method(model_name, "reback_plan", {
                    "id": plan.id
                }).then(() => {
                    this.remove_plan_and_monitors(plan);
                })
            },

            /**
             * 计划列表变化后触发，为新进的计划添加倒计时
             * 转换轨触发的，则添加到转换轨触发列表
             * 挂起计划添加到挂起列表，当前计划执行完毕后，取出挂起列表中最前一条执行
             */
            // 解析新计划
            resolve_train_plan(new_plans) {
                console.log("receive train plans:", new_plans)

                new_plans.map(new_plan => {
                    // 删除倒计时, 重新开始
                    switch (new_plan.operation) {
                        case 'delete':
                        case 'update':
                            this.remove_plan_timer(new_plan)
                            break;
                    }

                    // 判断计划是否已经存在
                    let old_plan = this.train_in_out_plans.concat(this.dispatch_plans).find(tmp_plan => {
                        return tmp_plan.id == new_plan.id && tmp_plan.type == new_plan.type
                    })

                    if (old_plan) {
                        /* 
                        几种特殊情况的边界处理 
                        1.未触发的
                        2.已触发弹窗, 待确认的
                        3.已经确认, 但信号未开放的
                        4.信号已开放的, 执行中的
                        5.已完成的 (时间差太大, 应该不会存在这种情况, 除非网络问题, 但可以操作段为准排除)
                        */
                        if (["update", "add"].includes(new_plan.operation)) {
                            // 执行中, 已完成, 已经触发了的收车, 已经确认了但信号未开放的, 已弹窗的 均不做处理
                            let is_pop_or_confirmed = old_plan.instructs && old_plan.instructs.some(instruct => {
                                return ['wait_confirm', 'confirmed'].includes(instruct.prepare)
                            })
                            if (["执行中", "已完成"].includes(old_plan.state) || is_pop_or_confirmed ||
                                (old_plan.type == "train_back" && 'executed' in old_plan)) {
                                this.sio_log(`${this.get_plan_desc(old_plan)}执行中, 不更新!`)
                                return
                            }
                        }
                    }

                    switch (new_plan.operation) {
                        case 'delete':
                            // 删除计划
                            if (old_plan) {
                                this.show_message_box(`场调已删除 ${this.get_plan_desc(old_plan)}!`, "warning")
                                this.remove_plan_and_monitors(old_plan)
                            }
                            break
                        case 'update':
                        case 'add':
                            // 检查位置是否一致, 否则加到别的位置的计划去了
                            if (new_plan.location !== this.location) {
                                return
                            }

                            // 若计划已经开始,后台应限制不能更新, 此处默认未开始
                            if (old_plan) {
                                this.show_message_box(`${this.get_plan_desc(old_plan)}已更新!`);
                            }

                            // 深拷贝替换, 更新
                            if (old_plan) {
                                if (new_plan.type == 'train_dispatch') {
                                    let index = _.findIndex(this.dispatch_plans, {
                                        "id": new_plan.id
                                    })
                                    this.$set(this.dispatch_plans, index, new_plan)
                                } else {
                                    // 收发车计划放一起了，要通过type来进行区分
                                    let index = _.findIndex(this.train_in_out_plans, {
                                        "id": new_plan.id,
                                        "type": new_plan.type
                                    })
                                    this.$set(this.train_in_out_plans, index, new_plan)
                                }
                            } else {
                                if (new_plan.type == 'train_dispatch') {
                                    this.dispatch_plans.push(new_plan)
                                } else {
                                    this.train_in_out_plans.push(new_plan)
                                }
                            }

                            // 默认第一条未完成指令可执行状态
                            let has_set = false
                            for (let item of new_plan.instructs) {
                                if (!has_set && item.state != "已完成") {
                                    item.prepare = "prepare"
                                    has_set = true
                                } else {
                                    item.prepare = "unprepare"
                                }

                                if (item.state == "执行中") {
                                    // this._execute_instruct(new_plan, item, false)
                                    // todo 恢复监控的状态
                                }
                            }

                            // 需要后端传过来的时候就转换成为本地时间
                            let start_time = this.$moment(new_plan.start_time).valueOf()
                            let millseconds = start_time - Date.now()
                            // B轨的发车, 提前10分钟触发调车到A轨
                            let b2a_time = millseconds - 600000
                            let b_section_train_out_plan = new_plan.type == "train_out" && new_plan.instructs.some(instruct => {
                                return instruct.type == "train_dispatch"
                            })

                            // 收车计划不添加计时器
                            if (new_plan.type != "train_back") {
                                // 如果是已经过时了的则去除掉则不在启动定时器
                                if (millseconds <= 0) {
                                    this.sio_log(`${this.get_plan_desc(new_plan)}已经超时, 不再提醒执行! `)
                                    return
                                }

                                // 如果是计划已经完成或是已经取消了的则不再启动定时器
                                if (new_plan.state == '已完成' || new_plan.state == '已取消') {
                                    return
                                }

                                this.sio_log(`${this.get_plan_desc(new_plan)}开始计时!`, millseconds)

                                let str = ''
                                // 添加到倒计时列表
                                let timer_id = setTimeout(i => {
                                    // 倒计时列表中删除原有的定时器
                                    this.remove_plan_timer(new_plan)

                                    str = `${this.get_plan_desc(new_plan)} 快到执行时间，注意查看!`;
                                    this.sio_log(str);
                                    this.show_message_box(str);

                                    if (new_plan.type == "train_out") {
                                        this.execute_plan(new_plan);
                                    }
                                }, b_section_train_out_plan ? b2a_time : millseconds)

                                // 每个发车计划添加一个定时器
                                this.time_out_plan.push({
                                    planid: new_plan.id,
                                    type: new_plan.type,
                                    timeid: timer_id
                                })
                            }
                            break
                    }
                })

                this.toggleExecutingPlan()
            },

            // 解析全局帧, 更新监控部件状态
            change_global_state(state) {
                if (!state)
                    return

                let sdi_state = state
                state = state.data

                if (state.type == "setPlanControl") {
                    console.log('the control plan state is:', state)
                    // 设置控制状态
                    this.selfcontrolplan = state.selfcontrolplan
                    this.mdiasControl = state.mdiasControl

                    // console.log('the control state is:', state)
                    this.system_log(this.mdiasControl ? "MDIAS控" : "非MDIAS控")
                    if (this.mdiasControl) {
                        this.system_log((this.selfcontrolplan ? "自控" : "集控"))
                    } else { // 非mdias控时,移除计划执行定时器和冲突检测
                        this.train_in_out_plans.concat(this.dispatch_plans).map(plan => {
                            // 移除定时记录和定时器
                            this.remove_plan_timer(plan);
                            // 移除冲突检测监控
                            this.remove_wait_plan_timer(plan);
                        })
                    }
                    this.system_log((this.selfcontrolplan ? "自控" : "集控") + " " + (this.mdiasControl ? "MDIAS控" : "非MDIAS控"))

                } else if (['DATA_SDI', 'DATA_SDCI'].includes(sdi_state['data_type'])) {
                    this.get_sdci_data(sdi_state).map((i) => {
                        i.name = i.name.toUpperCase()
                        switch (i.type) {
                            case 1:
                            case 2:
                            case 3:
                            case 4:
                            case 5:
                                this.change_plan_progress(i.name, i)
                                break
                        }
                    })
                }
            },

            // 设备监控计划执行进度
            // 一条指令触发后监察 ："operation_btns": "D35DA D7DA"
            // 立即更新指令状态：信号未开放
            // 检查 D35DA (equipStatus.yellow && (x.type == '发车' || x.type == '收车') )(equipStatus.white && x.type == '调车')
            // 如果满足就认定按钮点击成功, 更新指令状态：执行中
            // 检查出清情况  
            // 股道{"block":0,"hold":0,"index":104,"lock":0,"name":"38G","notice":0,"type":2}
            // 道岔{"closed":0,"hold":0,"index":22,"lock":1,"lock_gt":0,"lock_protect":0,"lock_s":0,"name":"43","notice":0,"pos":1,"pos_reverse":0,"preline_blue_belt":0,"reversed":0,"type":1}
            change_plan_progress(uid, equipStatus) {
                // 遍历勾指令监控列表，更新状态。完成一条勾指令后，执行对应的下一条，没有下一条则更新进行中计划状态
                // console.log(uid, equipStatus)

                this.instruct_status_monitors.map(({
                    instruct,
                    plan,
                    operation_btns,
                    sections,
                    callback
                }) => {
                    // 遍历勾指令中的监控项列表
                    for (let i = 0; i < sections.length; i++) {
                        let equip = sections[i];
                        // 监控：按下按钮和进路经过区段、道岔
                        if (equip.uid.toUpperCase() == uid.toUpperCase() ||
                            operation_btns.toUpperCase() == uid.toUpperCase()) {
                            // 更新监听列表的部件状态状态
                            if (instruct.progress) {
                                if (equip.state == 2 &&
                                    equipStatus.lock == 1 &&
                                    equipStatus.hold == 0) { // 占用 -> 锁闭
                                    equip.state = 3
                                } else if (equip.state == 1 &&
                                    equipStatus.hold == 1) { // 锁闭 -> 占用
                                    equip.state = 2
                                } else if (equipStatus.lock == 0 &&
                                    equipStatus.hold == 0) { // 锁闭 -> 空闲
                                    // 不一定会有占用到闭锁这个状态，所以这里可以等于2
                                    if (equip.state == 3 || equip.state == 2) {
                                        equip.state = 4
                                    } else if (this.formated_name(
                                            instruct.start_rail).includes(equipStatus.name) && equip.state == 0) { // 起始股道出清
                                        equip.state = 4
                                    }
                                }
                            } else {
                                if (equip.state == 0 &&
                                    equipStatus.lock == 1 &&
                                    equipStatus.hold == 0) { // 空闲 -> 锁闭
                                    equip.state = 1
                                }
                            }

                            // 是否亮灯 
                            let lighted = (equipStatus.yellow &&
                                    (instruct.type == 'train_out' || instruct.type == 'train_back')) ||
                                (equipStatus.white && instruct.type == 'train_dispatch')
                            if (lighted &&
                                operation_btns.toUpperCase() == uid.toUpperCase()) {
                                // console.log(lighted, (equipStatus.white && plan.type == 'train_dispatch'), equipStatus, plan.type)
                            }

                            // 如果亮灯而且指令未开始更新
                            if (lighted && !instruct.progress) {
                                console.log("白光带已经排，计划进行中...")

                                if (instruct.check_started_timer) {
                                    clearTimeout(instruct.check_started_timer)
                                    instruct.check_started_timer = undefined
                                }

                                // 指令执行状态
                                instruct.progress = 1
                                // 计划状态修改
                                this.update_instruct_status(plan, instruct, 'executing')

                                // 通知服务器更新计划状态, plan中包含plan_type, 由于计划中有些乱七八糟的数据
                                this.toggleRowExpansion(plan)
                            }

                            // 灯灭了，但进路又没有执行完成
                            if (!lighted &&
                                instruct.progress &&
                                !instruct.instruct_combined &&
                                sections.every(x => x.state < 2)) {
                                // 之前1714出现这种情况
                                let start_rails = this.formated_name(instruct.start_rail)
                                if (!start_rails.includes(uid.toUpperCase())) {
                                    console.info('%c恢复信号未开放：', 'font-size:25px;color:red;', instruct)
                                    equip.state = 0
                                    instruct.progress = 0
                                    instruct.state = "信号未开放"
                                    this.remove_plan_monitors(plan, instruct)
                                }
                            }

                            if (instruct.progress) {
                                // 结束rail可能为道岔, 需特殊处理
                                let end_rails = this.formated_name(instruct.end_rail)
                                let end_sections = sections.filter((x) => {
                                    return end_rails.includes(x.uid)
                                })

                                // 判断是否结束
                                if (end_sections.length) {
                                    let other_sections = sections.filter((x) => {
                                        return !end_rails.includes(x.uid)
                                    })
                                    if (!other_sections.every(z => z.state >= 3) || end_sections.some(z => z.state < 2)) {
                                        continue
                                    }
                                } else if (!sections.every(z => z.state >= 3)) {
                                    continue
                                }

                                this.sio_log(`${JSON.stringify(instruct)}计划执行完毕!`)
                                console.info('%c指令执行完毕：', 'font-size:25px;color:red;', instruct)

                                this.update_instruct_status(plan, instruct, 'finished')

                                // 去除已经完成的监听
                                this.remove_plan_monitors(plan, instruct)

                                // 执行指令完成后的回调，如果是作业内容则需人工确认
                                callback.apply(this)
                                break;
                            }
                        }
                    }
                })
            },

            update_instruct_status(plan, instruct, status) {

                let all_plans = plan.type == "train_dispatch" ? this.dispatch_plans : this.train_in_out_plans

                let plan_index = _.findIndex(all_plans, {
                    "id": plan.id,
                    "type": plan.type
                })

                let status_text = status == "executing" ? "执行中" : "已完成"
                instruct.state = status_text
                // 只会传入两种状态
                if (status == "executing") {
                    instruct.start_time = Date.now()
                } else {
                    instruct.end_time = Date.now()
                }
                this.system_log(`更新${this.get_instruct_desc(plan, instruct)}状态！`)

                let index = _.findIndex(plan.instructs, {
                    "id": instruct.id
                })
                this.$set(plan.instructs, index, instruct)

                this.system_log(`计划历史状态${plan.state}状态, 请确认界面是否更新！`)
                this.$set(plan, "state", "执行中")
                this.system_log(`开始更新外层计划${this.get_instruct_desc(plan, instruct)}状态, 更改为${plan.state}！`)

                // 更新计划状态
                this.$set(all_plans, plan_index, plan)
                // 查看更新后的状态
                this.system_log(`最终更新后的计划状态为:${all_plans[plan_index].state}`)

                // 检查是否更新，如果没有更新则暴力更新, 之前出现过不更新的情况
                this.$nextTick(() => {
                    let state_span = document.querySelector(`.instruct_${instruct.id}_${plan.type}`);
                    // 有可能已经被移除
                    if (state_span) {
                        let text = state_span.innerText
                        if (text != status_text) {
                            this.system_log(`发现状态未更新，暴力更新为: ${status_text}! 请确认状态`)
                            state_span.innerText = status_text
                        }
                    }
                });

                this.update_plan_server_status(status, plan, instruct)
            },

            update_plan_server_status(status, plan, instruct) {
                let plan_state = {
                    "id": plan.id,
                    "type": plan.type,
                    "state": instruct ? "executing" : status
                }

                if (instruct) {
                    plan_state['detail_state'] = {
                        'id': instruct.id,
                        'state': status
                    }
                }

                this.call_server_method(
                    "funenc.socket_io",
                    "update_plan_state", {
                        "plan_state": plan_state
                    });
            },

            resolve_onchang_train_plan(new_plans) {
                console.log("receive onchang train plans:", new_plans)
                new_plans.map(new_plan => {
                    // 判断计划是否已经存在
                    let old_plan = this.train_in_out_plans.concat(this.dispatch_plans).find(tmp_plan => {
                        return tmp_plan.id == new_plan.id && tmp_plan.type == new_plan.type
                    })
                    if (old_plan) {
                        if (["update", "add"].includes(new_plan.operation)) {
                            // 执行中, 已完成, 已经触发了的收车, 已经确认了但信号未开放的, 已弹窗的 均不做处理
                            let is_pop_or_confirmed = old_plan.instructs && old_plan.instructs.some(instruct => {
                                return ['wait_confirm', 'confirmed'].includes(instruct.prepare)
                            })
                            if (["已完成"].includes(old_plan.state) || is_pop_or_confirmed ||
                                (old_plan.type == "train_back" && 'executed' in old_plan)) {
                                this.sio_log(`${this.get_plan_desc(old_plan)}已完成, 不更新!`)
                                return
                            }
                        }
                    }
                    switch (new_plan.operation) {
                        case 'delete':
                            // 删除计划
                            if (old_plan) {
                                this.show_message_box(`场调已删除 ${this.get_plan_desc(old_plan)}!`, "warning")
                                this.remove_plan_and_monitors(old_plan)
                            }
                            break
                        case 'update':
                        case 'add':
                            // 检查位置是否一致, 否则加到别的位置的计划去了
                            if (new_plan.location !== this.location) {
                                return
                            }
                            // 若计划已经开始,后台应限制不能更新, 此处默认未开始
                            if (old_plan) {
                                this.show_message_box(`${this.get_plan_desc(old_plan)}已更新!`);
                            }
                            // 深拷贝替换, 更新
                            if (old_plan) {
                                if (new_plan.type == 'train_dispatch') {
                                    let index = _.findIndex(this.dispatch_plans, {
                                        "id": new_plan.id
                                    })
                                    this.$set(this.dispatch_plans, index, new_plan)
                                } else {
                                    // 收发车计划放一起了，要通过type来进行区分
                                    let index = _.findIndex(this.train_in_out_plans, {
                                        "id": new_plan.id,
                                        "type": new_plan.type
                                    })
                                    this.$set(this.train_in_out_plans, index, new_plan)
                                }
                            } else {
                                if (new_plan.type == 'train_dispatch') {
                                    this.dispatch_plans.push(new_plan)
                                } else {
                                    this.train_in_out_plans.push(new_plan)
                                }
                            }
                            // 默认第一条未完成指令可执行状态
                            let has_set = false
                            for (let item of new_plan.instructs) {
                                if (!has_set && item.state != "已完成") {
                                    item.prepare = "prepare"
                                    has_set = true
                                } else {
                                    item.prepare = "unprepare"
                                }
                            }
                            // 需要后端传过来的时候就转换成为本地时间
                            let start_time = this.$moment(new_plan.start_time).valueOf()
                            let millseconds = start_time - Date.now()
                            // B轨的发车, 提前10分钟触发调车到A轨
                            let b2a_time = millseconds - 600000
                            let b_section_train_out_plan = new_plan.type == "train_out" && new_plan.instructs.some(instruct => {
                                return instruct.type == "train_dispatch"
                            })

                            // 收车计划不添加计时器
                            if (new_plan.type != "train_back") {
                                // 如果是已经过时了的则去除掉则不在启动定时器
                                if (millseconds <= 0) {
                                    this.sio_log(`${this.get_plan_desc(new_plan)}已经超时, 不再提醒执行! `)
                                    return
                                }

                                // 如果是计划已经完成或是已经取消了的则不再启动定时器
                                if (new_plan.state == '已完成' || new_plan.state == '已取消') {
                                    return
                                }
                                this.sio_log(`${this.get_plan_desc(new_plan)}开始计时!`, millseconds)
                                let str = ''
                                // 添加到倒计时列表
                                let timer_id = setTimeout(i => {
                                    // 倒计时列表中删除原有的定时器
                                    this.remove_plan_timer(new_plan)

                                    str = `${this.get_plan_desc(new_plan)} 快到执行时间，注意查看!`;
                                    this.sio_log(str);
                                    this.show_message_box(str);

                                    if (new_plan.type == "train_out") {
                                        this.execute_plan(new_plan);
                                    }
                                }, b_section_train_out_plan ? b2a_time : millseconds)

                                // 每个发车计划添加一个定时器
                                this.time_out_plan.push({
                                    planid: new_plan.id,
                                    type: new_plan.type,
                                    timeid: timer_id
                                })
                            }
                            break
                    }
                })
            },

            // 执行计划
            execute_plan(plan) {

                // 移除计划定时器
                this.remove_plan_timer(plan)

                if (!this.mdiasControl) {
                    this.show_message_box(`当前非MDIAS控制模式，无法执行计划!`, "warning")
                    return
                }

                // 非自控模式不能执行
                if (!this.selfcontrolplan) {
                    this.show_message_box('当前模式非自控模式，无法进行操作！如需操作请先切换为自控模式！', "warning")
                    return
                }

                this._execute_plan(plan)
            },

            /**
             * 执行计划, 找到需要执行的指令
             * @param {*} plan
             */
            _execute_plan(plan) {
                // 发车计划指令已经合并执行
                if (plan.instruct_combined) {
                    return
                }

                let self = this
                // 取得第一条可执行的指令
                let instruct = _.find(plan.instructs, {
                    "prepare": "prepare"
                })

                if (!instruct) {
                    instruct = _.find(plan.instructs, {
                        "prepare": "unprepare"
                    })
                }

                if (!instruct) {
                    instruct = _.find(plan.instructs, {
                        "prepare": "confirmed"
                    })
                }

                if (instruct) {
                    this.sio_log(`%c执行计划${JSON.stringify(plan)}命令${JSON.stringify(instruct)}!`)
                    // 若计划执行中, 则提示返回
                    if (this.check_plan_run_state(plan, instruct)) {
                        return
                    }
                    // 集控模式不发送指令，但需要执行监控
                    if (this.selfcontrolplan) {
                        // 不存在冲突, 弹窗提示执行
                        let ret = this.conflict_check(plan, instruct)
                        if (ret != 1) {
                            this._pop_execute_plan(plan, instruct, ret == 2)
                        }
                    }
                } else {
                    this.sio_log('没有找到可执行的计划指令, somethine is error!')
                }
            },

            /**
             *
             * @param {*} plan
             * @param {*} instruct
             * @param {*} shading_signal 是否执行补信号
             */
            _pop_execute_plan(plan, instruct, shading_signal) {

                if (!this.mdiasControl) {
                    this.show_message_box(`当前非MDIAS控制模式，无法执行计划!`, "warning")
                    return
                }

                // 非自控模式不能执行
                if (!this.selfcontrolplan) {
                    this.show_message_box('当前模式非自控模式，无法进行操作！如需操作请先切换为自控模式！', "warning");
                    return
                }

                // 若计划执行中, 则提示返回
                if (this.check_plan_run_state(plan, instruct)) {
                    return
                }

                var notify_id = plan.type + "_" + plan.id + "_" + instruct.id
                if (notify_id in this.notify_list) {
                    this.show_message_box(`弹窗已弹出，不再得复弹出!`, "warning")
                    return
                }

                let self = this
                const h = this.$createElement;
                instruct.prepare = "wait_confirm"

                this.system_log(`开始${this.get_instruct_desc(plan, instruct)}, 等侍值班人员确认！`)

                // 弹出确认对话框
                let $notify = this.$notify({
                    showClose: false,
                    duration: 0,
                    onClose() {
                        delete self.notify_list[notify_id]
                    },
                    title: shading_signal ? '确认执行补信号!' : '确认执行进路指令!',
                    message: h('i', {
                        style: 'color: teal'
                    }, [
                        h('div', `${this.plan_type_name[plan.type]}计划(${plan.trainId})待执行`),
                        h('div', `${instruct.condition ? "已确认" : "未确认"}`),
                        h('div', `股道${this.formatter_rail_name(instruct.start_rail)}—>${this.formatter_rail_name(instruct.end_rail)}`),
                        h('div', {
                            class: "iconfirmbtn",
                            style: 'cursor: pointer',
                            on: {
                                click() {
                                    // 确认点击执行回调
                                    $notify.close()
                                    instruct.prepare = "confirmed"
                                    self._execute_instruct(plan, instruct, true)
                                }
                            },
                        }, "确认"),
                        h('div', {
                            class: "icancelbtn",
                            style: 'cursor: pointer',
                            on: {
                                click() {
                                    $notify.close()
                                    instruct.prepare = "prepare"
                                }
                            },
                        }, "取消"),
                    ])
                });
                this.notify_list[notify_id] = $notify
            },

            /**
             * 创建执行回调，供弹出框确认使用
             * @param {*} plan
             * @param {*} instruct
             * @param {*} send_cmd 是否发送指令
             */
            _execute_instruct(plan, instruct, send_cmd) {

                if (!this.mdiasControl) {
                    this.show_message_box(`当前非MDIAS控制模式，无法执行计划!`, "warning")
                    return
                }

                let self = this
                let shading_signal = false
                if (send_cmd) {
                    // 进行冲突检测, 若存在冲突, 则返回, 若不存在冲突, 则执行指令. 
                    let ret = this.conflict_check(plan, instruct)
                    if (ret == 1) { // 冲突返回
                        return
                    } else if (ret == 2) { // 补信号
                        let resolvedButton = instruct.operation_btns.split(' ').map(x => {
                            return {
                                equip: x.slice(0, -2),
                                type: x.slice(-2, x.length)
                            }
                        })[0]

                        this.sio_log(`计划发送后端指令${JSON.stringify(resolvedButton)}`)
                        this.send_to_main_wnd({
                            type: "shadingSignal",
                            command: resolvedButton,
                            operation: `重开${resolvedButton.equip}`
                        })
                        shading_signal = true
                    } else { // 不冲突
                        let resolvedButton = instruct.operation_btns.split(' ').map(x => {
                            return {
                                equip: x.slice(0, -2),
                                type: x.slice(-2, x.length)
                            }
                        })

                        // 检测发车计划是否能合并执行
                        // 发车, 非最后一条指令条件满足时, 检测是否有合并条件
                        if (instruct.type == "train_out" &&
                            plan.instructs.length >= 2 &&
                            !(instruct.end_rail in this.conflict_rules.section)) {
                            let instruct_size = plan.instructs.length
                            let end_instruct = plan.instructs[instruct_size - 1]
                            let booby_instruct = plan.instructs[instruct_size - 2]
                            let switch_rail = end_instruct.end_rail

                            let zc_conflicted = false
                            let lxj_green = false
                            let switch_rail_avalible = false
                            let rail_avalible = false
                            if (end_instruct.type == "train_out" && switch_rail in this.conflict_rules.section) {
                                // 照查状态
                                let zc_item = this.sdi_data.find(x => {
                                    return x.name == this.conflict_rules.section[switch_rail]['ZCJ']
                                })
                                zc_conflicted = zc_item && zc_item.light

                                // 正线信号灯状态
                                let lxj_item = this.sdi_data.find(x => {
                                    return x.name == this.conflict_rules.section[switch_rail]['LXJ']
                                })
                                lxj_green = lxj_item && lxj_item.green

                                // 转换轨的状态
                                let switch_rail_item = this.sdi_data.find(x => {
                                    return x.name == switch_rail
                                })
                                switch_rail_avalible = !switch_rail_item.hold && !switch_rail_item.lock && !switch_rail_item.block

                                // 出入段线状态
                                let rail_item = this.sdi_data.find(x => {
                                    return x.name == this.conflict_rules.section[switch_rail]['RAIL']
                                })
                                rail_avalible = rail_item && !rail_item.hold && !rail_item.lock && !rail_item.block

                                // 照查未冲突, LXJ绿灯, 转换轨未占压, 出入短线未占压
                                if (!zc_conflicted && lxj_green && switch_rail_avalible && rail_avalible) {
                                    resolvedButton = [booby_instruct.operation_btns.split(' ').map(x => {
                                        return {
                                            equip: x.slice(0, -2),
                                            type: x.slice(-2, x.length)
                                        }
                                    })[0]]
                                    resolvedButton.push(end_instruct.operation_btns.split(' ').map(x => {
                                        return {
                                            equip: x.slice(0, -2),
                                            type: x.slice(-2, x.length)
                                        }
                                    })[1])
                                    this.show_message_box(`${this.formatter_train_id(plan)}车直接发到${this.formatter_rail_name(switch_rail)}!`, "warning", 10000)
                                    plan.instruct_combined = true
                                    end_instruct.prepare = 'confirmed'
                                }
                            }
                        }

                        this.sio_log(`计划发送后端指令${JSON.stringify(resolvedButton)}`)
                        this.send_to_main_wnd({
                            type: "executeInstruct",
                            command: resolvedButton,
                            operation: plan.instruct_combined ? "列车进路" : instruct == "train_dispatch" ? "调车进路" : "列车进路",
                            "start_rail": plan.instruct_combined ? plan.instructs.slice(-2)[0].start_rail : instruct.start_rail,
                            "end_rail": plan.instruct_combined ? plan.instructs.slice(-1)[0].end_rail : instruct.end_rail
                        })
                    }
                }

                // 移除冲突检测，用户可能自己手动点开始计划, 
                // 由于一条计划同时只能执行一条指令，所以这里就全都去除掉了
                this.remove_wait_plan_timer(plan)

                // 移除老的监听, 由于计划编号不能重复，所以要判断计划
                this.remove_plan_monitors(plan, instruct)

                // 开始监控指令执行情况
                this.instruct_status_monitors.push({
                    instruct: instruct, //指令
                    plan: plan, //计划引用
                    operation_btns: instruct.operation_btns.split(' ')[0].slice(0, -2), //监控信号机
                    // 监控的元素
                    sections: instruct.sections.map(sec => {
                        let ret_sec = {}
                        // 以G结尾特殊处理
                        if (!_.endsWith(sec, "G") && sec.indexOf("/") != -1) {
                            let tmp_ar = sec.split("/")
                            ret_sec = {
                                uid: tmp_ar[0],
                                state: 0 // 记录状态
                            }
                        } else {
                            ret_sec = {
                                uid: sec,
                                state: shading_signal && sec == instruct.end_rail ? 1 : 0 // 记录状态
                            }
                        }
                        // 调车的首端和终端去掉检测判断 默认状态设为4
                        if (plan.type == 'train_dispatch' && (this.formated_name(instruct.start_rail).includes(ret_sec['uid']) || this.formated_name(instruct.end_rail).includes(ret_sec['uid']))) {
                            let rail_item = this.sdi_data.find(x => {
                                return x.name == ret_sec['uid']
                            })
                            // 若终端为空闲,则检查最终的占压状态,初始状态设为0
                            if ('hold' in rail_item) {
                                ret_sec['state'] = rail_item['hold'] ? 4 : 0
                            } else {
                                ret_sec['state'] = 4
                            }
                        }

                        return ret_sec

                    }),
                    // 监控到指令执行完毕后的回调, 设置下一条的进路按钮显示
                    callback: () => {
                        instruct.prepare = "finished"
                        let next_instruct = _.find(plan.instructs, (instruct) => {
                            return instruct.prepare != 'finished'
                        })

                        // 发车计划被合并执行或没有下一条instruct，就确认当前计划执行完毕
                        if ((plan.instruct_combined || !next_instruct)) {
                            if (plan.instructs.every(item => {
                                    return item.prepare == "finished"
                                })) {

                                plan.end_time = Date.now()

                                let plan_index = _.findIndex(this.train_in_out_plans, {
                                    "id": plan.id,
                                    "type": plan.type
                                })
                                this.$set(plan, "state", "已完成")
                                this.$set(this.train_in_out_plans, plan_index, plan)

                                // 检查是否更新，如果没有更新则暴力更新，之前出现过不更新状态的情况
                                this.$nextTick(() => {
                                    let state_span = document.querySelector(`.plan_${plan.id}_${plan.type}`);
                                    if (state_span) {
                                        let text = state_span.innerText
                                        if (text != "已完成") {
                                            this.system_log(`发现计划状态未更新，暴力更新为: 执行中! 请确认状态`)
                                            state_span.innerText = "已完成"
                                        }
                                    }
                                });

                                this.sio_log(`${plan.trainId}${this.plan_type_name[plan.type]}计划{plan.state}`);
                                this.system_log(`${this.get_plan_desc(plan)} 执行完成`)

                                this.update_plan_server_status("finished", plan)

                                // 收起计划显示
                                this.toggleRowExpansion(plan)
                            }
                        } else {
                            if (plan.type != "train_out" || next_instruct.prepare != "prepare") {
                                // 指定下一条指令为状态为true
                                next_instruct.prepare = "prepare"
                                // 如果当前非作业指令才能自动开始下一条
                                if (plan.type != "train_dispatch") {
                                    let start_time = this.$moment(plan.start_time).valueOf()
                                    let millseconds = start_time - Date.now()
                                    let b_section_train_out_to_a = plan.type == "train_out" && instruct.type == "train_dispatch"
                                    if (b_section_train_out_to_a && millseconds > 0) {
                                        // A轨的发车, 看到到A轨的时间择机执行
                                        let timer_id = setTimeout(i => {
                                            // 倒计时列表中删除原有的定时器
                                            this.remove_plan_timer(plan)
                                            let str = `${this.get_plan_desc(plan)} 快到执行时间，注意查看!`;
                                            this.sio_log(str);
                                            this.show_message_box(str);

                                            if (plan.type == "train_out") {
                                                this.execute_plan(plan);
                                            }
                                        }, millseconds)

                                        // 每个发车计划添加一个定时器
                                        this.time_out_plan.push({
                                            planid: plan.id,
                                            type: plan.type,
                                            timeid: timer_id
                                        })

                                    } else {
                                        self._execute_plan(plan)
                                    }
                                }
                            }
                        }
                    },
                    send_cmd: send_cmd
                })
                this.sio_log(`the current instruct monitor is ${JSON.stringify(this.instruct_status_monitors)}`)

                if (send_cmd || plan.instruct_combined) {
                    instruct.check_started_timer = setTimeout(() => {
                        if (!plan.instructs.some(instruct => {
                                return instruct.state == "执行中"
                            })) {
                            this.system_log(`移除超时${this.get_plan_desc(plan)}`)
                            this.remove_plan_monitors(plan, instruct)
                            // 移除标识
                            if (plan.instruct_combined) {
                                plan.instruct_combined = false
                            }
                        }
                    }, 60000)

                    // 发车 非最后一钩的发车指令时, 自动执行最后一钩(需弹窗, 确认后执行指令)
                    if (plan.type == "train_out" && !plan.instruct_combined && instruct.type == "train_out") {
                        let len = plan.instructs.length
                        // 若非最后一条发车指令,则请求执行
                        if (instruct.id != plan.instructs[len - 1].id) {
                            this.execute_plan(plan)
                        }
                    }

                    // 自动将最后一钩指令加入执行队列(不需弹窗, 指令已执行, 只是加入执行队列)
                    if (send_cmd && plan.instruct_combined) {
                        this._execute_instruct(plan, plan.instructs.slice(-1)[0], false)
                    }
                }
            },

            /**
             * 冲突检测
             * @param {*} plan
             * @param {*} instruct
             * @param {*} timer_check
             * return 0 无冲突,正常执行 1 冲突 2 发车未正常出清,转换轨残留白光带
             */
            conflict_check(plan, instruct, timer_check = false) {
                let start_rails = this.formated_name(instruct.start_rail)

                // 是否为发车的最后一条指令
                let end_rail = this.formated_name(instruct.end_rail)
                let is_special_instruct = instruct.type == "train_out" && end_rail in this.conflict_rules.section

                // 是否能补信号
                let shading_signal = false

                // 区段和道岔的冲突检测
                let normal_conflicted = instruct.sections.some(x => {
                    if (start_rails.includes(x)) { // 排除原始位置的
                        return false
                    } else {
                        // 检查当前状态
                        let item = this.sdi_data.find(y => {
                            return y.name == x
                        })
                        if (item) {
                            if (item.type == 1) { // 道岔 (单锁状态需加上方向判断)
                                let rst = item.hold || item.lock || item.closed ||
                                    item.lock_gt || item.preline_blue_belt || item.lock_protect
                                if (rst) {
                                    let log = ""
                                    if (item.hold) {
                                        log = `${item.name}处于占用状态 `
                                    } else if (item.lock) {
                                        log = `${item.name}处于锁闭状态 `
                                    } else if (item.closed) {
                                        log = `${item.name}处于封闭状态 `
                                    } else if (item.lock_gt) {
                                        log = `${item.name}处于引导总锁闭状态 `
                                    } else if (item.switch_crowded) {
                                        log = `${item.name}处于挤岔状态 `
                                    } else if (item.lock_protect) {
                                        log = `${item.name}处于防护锁闭状态 `
                                    }
                                    if (log) {
                                        log = '进路冲突: 道岔' + log
                                        this.system_log(`${this.get_instruct_desc(plan, instruct)} ${log}`)
                                    }
                                }

                                if (item.lock_s) {
                                    if (item.name in instruct.switches_direction) {
                                        let dirction_info = instruct.switches_direction[item.name]
                                        let lock_s_ret = dirction_info.is_reverse && item.pos || !dirction_info.is_reverse && item.pos_reverse
                                        if (lock_s_ret) {
                                            let log = `进路冲突: ${x}道岔单锁于${item.pos ? "定位" : "反位"}`
                                            this.system_log(`${this.get_instruct_desc(plan, instruct)} ${log}`)
                                        }
                                        rst = rst || lock_s_ret
                                    } else {
                                        console.log(`未找到${item.name}道岔的方向信息...`)
                                    }
                                }

                                // 双动道岔, 只包含单个道岔的进路, 只需判断另一个未包含道岔是否处于反位占用状态(防护的处理)
                                let switches = this.double_acting_switch.filter(z => {
                                    return z.includes(Number(x))
                                })

                                if (switches.length) {
                                    switches = switches[0]
                                    let check_switch = switches[Number(Number(x) != switches[1])].toString()
                                    if (!instruct.sections.includes(check_switch)) {
                                        let item = this.sdi_data.find(m => {
                                            return m.name == check_switch
                                        })

                                        let protect_rst = (item.hold || item.lock || item.closed ||
                                            item.lock_gt || item.preline_blue_belt || item.lock_protect) && item.pos_reverse
                                        if (protect_rst) {
                                            let log = `进路冲突: ${x}道岔的联动道岔${check_switch}处于反位占用状态`
                                            this.system_log(`${this.get_instruct_desc(plan, instruct)} ${log}`)
                                        }
                                        rst = rst || protect_rst
                                    }
                                }

                                return rst
                            } else if (item.type == 2) { // 区段
                                let rst = item.hold || item.lock || item.block
                                if (rst) {
                                    let log = ""
                                    if (item.hold) {
                                        log = `${item.name}处于hold状态 `
                                    } else if (item.lock) {
                                        log = `${item.name}处于lock状态 `
                                    } else if (item.block) {
                                        log = `${item.name}处于block状态 `
                                    }
                                    if (log) {
                                        log = '进路冲突: 区段' + log
                                        this.system_log(`${this.get_instruct_desc(plan, instruct)} ${log}`)
                                    }
                                }

                                // 发车的转换轨的锁闭特殊处理
                                if (is_special_instruct && item.name == end_rail && item.lock) {
                                    shading_signal = true
                                    return false
                                }

                                // 调车的目的股道占压不是冲突, 白光带为照查敌对需报处理
                                if (instruct.type == "train_dispatch" && item.name == end_rail && item.hold) {
                                    return false
                                }

                                return rst
                            }
                        } else {
                            console.log(`未找到 ${x} 的状态信息`)
                        }
                        return false
                    }
                })

                // 防护道岔的冲突检测
                let protect_switches_conflicted = instruct.protect_switches.some(x => {
                    let item = this.sdi_data.find(y => {
                        return y.name == x
                    })

                    if (item) {
                        if (item.type == 1) {
                            let ret = item.hold || item.lock || item.closed ||
                                item.lock_gt || item.preline_blue_belt || item.lock_protect
                            if (ret) {
                                let log = ""
                                if (item.hold) {
                                    log = `处于hold状态 `
                                } else if (item.lock) {
                                    log = `处于lock状态 `
                                } else if (item.closed) {
                                    log = `处于closed状态 `
                                } else if (item.lock_gt) {
                                    log = `处于lock_gt状态 `
                                } else if (item.preline_blue_belt) {
                                    log = `处于preline_blue_belt状态 `
                                } else if (item.lock_protect) {
                                    log = `处于lock_protect状态 `
                                }
                                if (log) {
                                    log = `进路冲突(道岔): ${item.name}${log}`
                                    this.system_log(`${this.get_instruct_desc(plan, instruct)} ${log}`)
                                }
                            }
                            return ret
                        } else {
                            console.log(`${x}的类型为${item.type}, 检测后端数据`)
                        }
                    } else {
                        console.log(`未找到道岔 ${x} 的状态信息`)
                    }
                    return false
                })

                // 发车的照查, 正线信号, 出入段线状态, 或者发车是否能通过补信号解决
                let zc_conflicted = false
                let lxj_green = false
                let rail_avalible = false
                let train_out_conflicted = false
                if (is_special_instruct) {
                    // 照查状态
                    let zc_item = this.sdi_data.find(x => {
                        return x.name == this.conflict_rules.section[end_rail]['ZCJ']
                    })
                    zc_conflicted = zc_item && zc_item.light
                    if (zc_conflicted) {
                        this.system_log(`${this.get_instruct_desc(plan, instruct)} 照查冲突`)
                    }

                    //  正线信号状态
                    let lxj_item = this.sdi_data.find(x => {
                        return x.name == this.conflict_rules.section[end_rail]['LXJ']
                    })
                    lxj_green = lxj_item && lxj_item.green
                    if (!lxj_green) {
                        this.system_log(`${this.get_instruct_desc(plan, instruct)} 正线信号未开放`)
                    }

                    // 出入段线状态
                    let rail_item = this.sdi_data.find(x => {
                        return x.name == this.conflict_rules.section[end_rail]['RAIL']
                    })
                    rail_avalible = rail_item && !rail_item.hold && !rail_item.lock && !rail_item.block
                    if (!rail_avalible) {
                        this.system_log(`${this.get_instruct_desc(plan, instruct)} 出入段线占压`)
                    }

                    train_out_conflicted = zc_conflicted || !lxj_green || !rail_avalible
                }

                // 与刚加入未执行中的计划冲突(计划可能排列中, 刚加入队列), 和执行中的不同(执行中只检测状态)
                let cur_plan_conficted = this.instruct_status_monitors.some(item => {
                    return !(['已完成', '执行中'].includes(item.instruct.state)) && (item.plan.id != plan.id || item.plan.type != plan.type) && item.instruct.sections.filter(sec => {
                        return instruct.sections.includes(sec) || instruct.protect_switches.includes(sec)
                    }).length
                })
                if (cur_plan_conficted) {
                    this.system_log(`${this.get_instruct_desc(plan, instruct)} 计划冲突`)
                }

                // 超限检查 
                let overrun_conflicted = false
                // 洗车信号检查
                let wash_signal_closed = false
                if (!normal_conflicted && !protect_switches_conflicted && !train_out_conflicted && !cur_plan_conficted) {
                    overrun_conflicted = instruct.sections.some(section => {
                        if (section in this.conflict_rules.switch) {
                            let check_section_name = this.conflict_rules.switch[section]
                            let items = this.sdi_data.filter(y => {
                                return y.name == check_section_name && y.hold
                            })

                            if (items.length > 0) {
                                this.system_log(`${this.get_instruct_desc(plan, instruct)} ${check_section_name}超限`)
                                return true
                            }
                        }
                        return false
                    })

                    if (plan.type == "train_dispatch" && end_rail in this.conflict_rules.wash_signal) {
                        let signal_item = this.sdi_data.find(x => {
                            return x.name == this.conflict_rules.wash_signal[end_rail]
                        })
                        wash_signal_closed = !signal_item || !signal_item.light
                        if (wash_signal_closed) {
                            this.system_log(`${this.get_instruct_desc(plan, instruct)} 洗车信号未开放`)
                        }
                    }
                }

                // 信号状态
                let signal_conflicted = false
                let buttons = instruct.operation_btns.split(" ")
                for (let button of buttons) {
                    let button_name = button.slice(0, -2)
                    let item = this.sdi_data.find(y => {
                        return y.name == button_name
                    })
                    if (item) {
                        if (item.closed) {
                            signal_conflicted = true
                            this.system_log(`${this.get_instruct_desc(plan, instruct)} ${button_name}信号封锁`)
                        }
                    }
                }

                // 未冲突时,可能已经存在与wait_execute_plan数组中,需要处理, 直接执行还是返回冲突不执行
                if (normal_conflicted || protect_switches_conflicted || train_out_conflicted || cur_plan_conficted || overrun_conflicted || wash_signal_closed || signal_conflicted) {
                    if (!timer_check) {
                        this.show_message_box(`${this.get_instruct_desc(plan, instruct)} 进路条件不满足, 待满足条件自动触发!`, "error")
                    }
                    // 冲突时, 若已存在等待执行队列中, 则不做处理
                    if (!this.wait_execute_plan.find(x => {
                            return x['plan'].id == plan.id && x['plan'].type == plan.type && x['instruct'].id == instruct.id
                        })) {
                        this.wait_execute_plan.push({
                            'plan': plan,
                            'instruct': instruct
                        })
                    }
                    return 1
                }

                return shading_signal ? 2 : 0
            },

            start_conflict_timer() {
                this.wait_timer = setInterval(() => {
                    for (let i = 0; i < this.wait_execute_plan.length && this.mdiasControl; ++i) {
                        let wait_item = this.wait_execute_plan[i]
                        let ret = this.conflict_check(wait_item.plan, wait_item.instruct, true)
                        if (ret != 1) {
                            // 弹出并移除
                            this._pop_execute_plan(wait_item.plan, wait_item.instruct, ret == 2);
                            this.wait_execute_plan.splice(i, 1)
                            break
                        }
                    }
                    if (!this.mdiasControl) {
                        this.wait_execute_plan = []
                    }
                }, 1000)
            },

            // 移除对应计划数据和监控数据
            remove_plan_and_monitors(plan, instruct) {
                // 移除计划
                this.remove_plan(plan);

                // 移除计划监控
                this.remove_plan_monitors(plan, instruct);

                // 移除定时记录和定时器
                this.remove_plan_timer(plan);

                // 移除冲突检测监控
                this.remove_wait_plan_timer(plan);

                // 去除可能未点确定和取消的提示框
                var notify_start = plan.type + "_" + plan.id + "_"
                _.each(this.notify_list, (notify_id) => {
                    if (_.startsWith(notify_id, notify_start)) {
                        this.notify_list[notify_id].close()
                    }
                })
            },

            remove_plan(plan) {
                // 移除计划
                if (plan.type == "train_out" || plan.type == "train_back") {
                    this.train_in_out_plans = this.train_in_out_plans.filter((tmp) => {
                        return tmp.id != plan.id || tmp.type != plan.type
                    })
                } else if (plan.type == "train_dispatch") {
                    this.dispatch_plans = this.dispatch_plans.filter((tmp) => {
                        return tmp.id != plan.id || tmp.type != plan.type
                    })
                }
            },

            remove_plan_monitors(plan, instruct) {
                this.instruct_status_monitors = this.instruct_status_monitors.filter(monitor => {
                    return monitor.plan.id != plan.id || monitor.plan.type != plan.type || (instruct && monitor.instruct.id != instruct.id)
                })
            },

            remove_plan_timer(plan) {
                this.time_out_plan = this.time_out_plan.filter(x => {
                    if (x.planid == plan.id && x.type == plan.type) {
                        clearTimeout(x.timeid)
                        return false
                    } else {
                        return true
                    }
                })
            },

            remove_wait_plan_timer(plan) {
                this.wait_execute_plan = this.wait_execute_plan.filter(x => {
                    return x.plan.id != plan.id || x.plan.type != plan.type
                })
            },

            check_plan_run_state(plan, instruct) {
                let executing_plan = _.find(this.instruct_status_monitors, (monitor) => {
                    if (monitor.plan.id == plan.id && monitor.plan.type == plan.type) {
                        // 发车的钩计划不做计划冲突处理
                        if (instruct.type == "train_out" &&
                            monitor.instruct.type == "train_out" &&
                            instruct.id != monitor.instruct.id) {
                            return false
                        }
                        return true
                    }
                    return false
                })

                if (executing_plan) {
                    this.show_message_box(`${this.get_plan_desc(plan)} 进路正在进行中!`, "error")
                    return true
                }
                return false
            },

            // 每次过来的数据只取变化的部分
            get_sdci_data(state) {
                let data_type = state['data_type']
                let sdci_data = []
                let datas = state.data
                if (data_type == "DATA_SDI") { // 全局帧
                    if (this.sdi_data.length) { // 已有数据时
                        datas.map((item, index) => {
                            let temp_item_str = JSON.stringify(item)
                            if (JSON.stringify(this.sdi_data[index]) != temp_item_str) {
                                this.sdi_data[index] = item
                                sdci_data.push(item)
                            }
                        })
                    } else { // 初始为空时
                        Object.assign(this.sdi_data, datas)
                        Object.assign(sdci_data, datas)
                    }
                } else if (data_type == "DATA_SDCI") { // 变化帧, 找到对应节点并判断是否相同
                    sdci_data = datas
                    datas.map((item, index) => {
                        let old_item = this.sdi_data.find(x => {
                            return x.index == item.index && x.name == item.name
                        })
                        if (old_item) { // 更新缓存节点
                            Object.assign(old_item, item)
                        }
                    })
                }

                return sdci_data
            },

            formated_name(name) {
                let formated_name = []
                if (name.endsWith('DG')) {
                    return name.replace('DG', '').replace('/', '_').split('-')
                } else {
                    formated_name.push(name.replace('/', '_').replace('-', '_'))
                }
                return formated_name
            },

            show_message_box(msg, type = "info", duration = 5000) {
                let now_time = Date.now()

                if (this.system_logs.some(item => {
                        // 消息相同, 且距上次显示时间小于5s
                        return item.msg == msg && now_time - item.time < 5000
                    })) {
                    return
                }

                this.system_log(msg, type)

                this.$message({
                    showClose: true,
                    message: msg,
                    type: type,
                    duration: duration
                })
            },

            /**
             * 打印日志，便于查询
             * @param {*} log
             */
            system_log(log, type = "info") {

                this.system_logs.splice(0, 0, {
                    'time': Date.now(),
                    'msg': log,
                    'content': `${this.$moment().format("HH:mm:ss")} ${log}`,
                    'type': type
                })

                if (this.system_logs.length > 1000) {
                    this.system_logs = this.system_logs.slice(0, 1000)
                }
            },

            // 暂时只打印在前端，后面更新到服务器端，便于收集前端日志
            sio_log(log_info, ...data) {
                console.log(log_info, data)
            },

            // 请求获取地址
            get_socketio_server_config() {
                var def = $.Deferred();
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "get_socketio_server_config"
                    }),
                    persistent: false,
                    onSuccess: function (config) {
                        def.resolve(config)
                    },
                    onFailure: function (error_code, error_message) {
                        def.reject('获取地址错误，请检查!')
                    }
                })
                return def
            },

            /**
             * 发送消息到主窗口执行
             */
            send_to_main_wnd(data) {
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "page_transfer",
                        data: data
                    }),
                    persistent: false,
                })
            },

            /**
             * 通知odoo服务器
             * @param {} msg
             */
            call_server_method(model, method, data) {
                let def = $.Deferred()
                try {
                    this.socket.emit('funenc_socketio_client_msg', {
                        "msg_type": 'call',
                        "model": model,
                        "name": method,
                        "kwargs": data
                    }, function (rst) {
                        def.resolve(rst)
                    })
                } catch (error) {
                    def.reject(error)
                }
                return def
            },

            // 通知添加计划成功
            notify_add_plan_success(datas) {
                this.socket.emit('funenc_socketio_client_msg', {
                    "msg_type": 'call',
                    "model": 'metro_park_dispatch.day_run_plan',
                    "name": "notify_publish_plan_success",
                    "kwargs": {
                        "datas": datas,
                        "location_alias": this.map_name
                    }
                }, (state) => {
                    console.log('通知计划更改成功:', state)
                })
            },

            toggleRowExpansion(plan) {
                let table = plan.type == "train_dispatch" ? this.$refs.dispatch_table : this.$refs.train_plan_table
                table.toggleRowExpansion(plan, plan.state == "执行中")
            },

            toggleExecutingPlan() {
                this.dispatch_plans.map(plan => {
                    this.toggleRowExpansion(plan)
                })

                this.train_in_out_plans.map(plan => {
                    this.toggleRowExpansion(plan)
                })
            },

            get_in_out_plan_key(row) {
                return `in_out_${row.id}_${row.type}`
            },

            get_in_out_instruct_row_key(row) {
                return `in_out_instruct_${row.id}_${row.type}`
            },

            get_row_key(row) {
                return `${row.id}-${row.type}`
            },

            // 添加下划线样式
            get_row_class({
                row,
                rowIndex
            }) {
                if (row.state == "已完成") {
                    return "middlelinePlan"
                } else if (row.state == "执行中") {
                    return "plan_executing"
                } else {
                    return null
                }
            },

            get_detail_row_class({
                row,
                rowIndex
            }) {
                if (row.state == "已完成") {
                    return "middlelinePlan dispatch_detail"
                } else if (row.state == "执行中") {
                    return "plan_executing"
                } else {
                    return null
                }
            },

            get_log_row_class({
                row,
                rowIndex
            }) {
                return row.type || ""
            },

            formatter_start_rail(row, column) {
                return this.formatter_rail_name(row.start_rail_alias)
            },

            formatter_end_rail(row, column) {
                return this.formatter_rail_name(row.end_rail_alias)
            },

            formatter_rail_name(name) {
                // 别名
                if (name in this.alias_name) {
                    return this.alias_name[name]
                }

                // AB轨处理
                if (name && (name.endsWith('AG') || name.endsWith("BG"))) {
                    return name.slice(0, -1)
                }

                return name
            },

            formatter_train_id(row, column) {
                return row.trainId ? row.trainId.slice(-2) : ""
            },

            get_plan_desc(plan) {
                return `${this.formatter_train_id(plan)}${this.plan_type_name[plan.type]}计划 ${this.formatter_rail_name(plan.start_rail)}->${this.formatter_rail_name(plan.end_rail)}`
            },

            get_instruct_desc(plan, instruct) {
                return `${this.formatter_train_id(plan)}${this.plan_type_name[plan.type]} ${this.formatter_rail_name(instruct.start_rail)}至${this.formatter_rail_name(instruct.end_rail)}`
            },
            manual_complete_plan(plan, all = false) {
                let instruct = _.find(plan.instructs, (instruct) => {
                    return instruct.prepare != 'finished';
                })
                if (instruct) {
                    this.remove_plan_timer(plan);
                    this.remove_wait_plan_timer(plan);

                    do {
                        this.update_instruct_status(plan, instruct, 'finished')
                        this.remove_plan_monitors(plan, instruct)
                        instruct.prepare = 'finished'
                        instruct = _.find(plan.instructs, (instruct) => {
                            return instruct.prepare != 'finished';
                        })
                        if (instruct) {
                            instruct.prepare = 'prepare'
                        }
                    } while (all && instruct)
                }

                if (all || !instruct) {
                    plan.end_time = Date.now()
                    let plan_index = _.findIndex(this.train_in_out_plans, {
                        "id": plan.id,
                        "type": plan.type
                    })
                    this.$set(plan, "state", "已完成")
                    this.$set(this.train_in_out_plans, plan_index, plan)
                    this.update_plan_server_status('finished', plan)
                    this.toggleRowExpansion(plan)
                }
            },
            clear_finish_plan(plan) {
                // 调车
                if (plan.type == "train_dispatch") {
                    this.dispatch_plans = this.dispatch_plans.filter((data) => {
                        return data.id != plan.id || data.type != plan.type
                    })
                } else { // 收发车
                    this.train_in_out_plans = this.train_in_out_plans.filter((data) => {
                        return data.id != plan.id || data.type != plan.type
                    })
                }
            }
        }
    })
});