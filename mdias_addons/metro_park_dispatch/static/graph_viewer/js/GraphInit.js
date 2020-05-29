(function () {

    mxResources.loadDefaultBundle = false;
    var bundle = mxResources.getDefaultBundle(RESOURCE_BASE, mxLanguage) ||
        mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);

    // Fixes possible asynchronous requests
    var location = urlParams['location'] || 'banqiao'
    var url = STATION_DATA_PATH + '/' + location + '/station.xml'
    var bounds = [
        bundle,
        STYLE_PATH + '/default.xml',
        url,
        STATION_DATA_PATH + '/' + location + '/button_table.json', // 3
        STATION_DATA_PATH + '/' + location + '/switch_belong_info.json', // 4
        STATION_DATA_PATH + '/parkbottombutton/parkbottombtn.json', // 5
    ]

    if (urlParams['debug']) {
        bounds.push(STATION_DATA_PATH + '/' + location + '/park_test_data.txt')
        bounds.push(STATION_DATA_PATH + '/' + location + '/park_test_data_sec.txt')
    }

    mxUtils.getAll(bounds, function (xhr) {

        // Adds bundle text to resources
        mxResources.parse(xhr[0].getText());

        // Configures the default graph theme
        var themes = new Object();
        themes[Graph.prototype.defaultThemeName] = xhr[1].getDocumentElement();

        // 站场图
        var location = urlParams['location']
        if (!location) {
            location = urlParams['mapname'] || 'banqiao'
        }
        var netWork = new NetWork(location);
        var editorUi = new EditorUi(
            new Editor(urlParams['chrome'] == '0', themes));

        var buttonTable = JSON.parse(xhr[3].getText())
        var switchBelongSec = JSON.parse(xhr[4].getText())

        var bottomButton = JSON.parse(xhr[5].getText())
        var tmpAr = bottomButton[location][0].split(' = ')

        var parkMap = undefined
        if (location == "yuanhua") {
            parkMap = new ParkMapForXiandi(editorUi, netWork, {
                "location": location,
                "disableOperation": false,
                "buttonTable": buttonTable, // 按扭表
                "switchBelongSec": switchBelongSec, // 无岔区段和道岔的对应关系
                "bottomButton": {
                    index: tmpAr[0],
                    name: tmpAr[1],
                    type: tmpAr[2]
                }
            })
        } else {
            parkMap = new ParkMap(editorUi, netWork, {
                "location": location,
                "disableOperation": false,
                "buttonTable": buttonTable, // 按扭表
                "switchBelongSec": switchBelongSec, // 无岔区段和道岔的对应关系
                "bottomButton": {
                    index: tmpAr[0],
                    name: tmpAr[1],
                    type: tmpAr[2]
                }
            })
        }

        // 打开xml模型, parkMap需要监听cell added 所以这里放在parkMap初始化后面
        editorUi.open_xml_model(xhr[2].getDocumentElement())

        // 底部toolbar
        var tool_bar = new OperationToolBar(editorUi, parkMap);
        // 列车
        var train_pannel = new TrainsPannel(editorUi, parkMap, netWork);
        // 报警
        var alarm_lsit = new AlarmList(editorUi, parkMap)
        // 占线板
        var busy_board = new BusyBoard(editorUi, parkMap, netWork)
        // 底部
        new ParkFooter(editorUi, parkMap)

        window.block_out = new BlackOut(editorUi, parkMap)

        // 切换占线板状态
        tool_bar.addListener('toggle_busy_board', function () {
            if (busy_board.isVisible()) {
                busy_board.setVisible(false)
            } else {
                busy_board.setVisible(true)
            }
        })

        // 取得 总取消按扭
        parkMap.addListener('get_all_relieve_btn', function (sender, evt) {
            var call_back = evt.getProperty('call_back');
            var all_relieve_btn = tool_bar.getAllRelieveBtn()
            call_back(all_relieve_btn)
        })

        // 取得 区故解按扭
        parkMap.addListener('get_sector_fault_unlock_btn', function (sender, evt) {
            var call_back = evt.getProperty('call_back');
            var unlock_btn = tool_bar.getSectorDefaultUnlockBtn()
            call_back(unlock_btn)
        })

        // 引导进路
        parkMap.addListener('get_guide_road_btn', function (sender, evt) {
            var call_back = evt.getProperty('call_back');
            var guide_road_btn = tool_bar.getGuidedRoadBtn()
            call_back(guide_road_btn)
        })

        // 开放引导
        parkMap.addListener('get_guide_open_btn', function (sender, evt) {
            var call_back = evt.getProperty('call_back');
            var guide_open_btn = tool_bar.getGuidedOpenBtn()
            call_back(guide_open_btn)
        })

        // 取得引导总锁
        parkMap.addListener('get_all_lock_btn', function (sender, evt) {
            var call_back = evt.getProperty('call_back');
            var all_lock_btn = tool_bar.getAllLockBtn()
            call_back(all_lock_btn)
        })

        // 切换列车状态
        tool_bar.addListener('toggle_train', function (sender, evt) {
            if (train_pannel.isVisible()) {
                train_pannel.setVisible(false)
            } else {
                train_pannel.setVisible(true)
            }
            parkMap.showTrains(train_pannel.isVisible())
            this.$el.find('.toggle_train')[0].innerHTML = train_pannel.isVisible() ? "隐藏列车" : "显示列车"
        })

        // 列车置顶或下移
        tool_bar.addListener('toggle_train_orders', function (sender, evt) {
            parkMap.toggle_train_orders()
        })

        tool_bar.addListener('show_dispatch_window', function (sender, evt) {
            window.open("dispatch.html?mapname=" + location, "_blank")
        })

        setTimeout(() => {
            window.open("dispatch.html?mapname=" + location, "_blank")
        }, 3000);

        tool_bar.addListener('toggle_alarm_window', function (sender, evt) {
            if (alarm_lsit.isVisible()) {
                alarm_lsit.setVisible(false)
            } else {
                alarm_lsit.setVisible(true)
            }
            this.$el.find('.toggle_alarm_window')[0].innerHTML = alarm_lsit.isVisible() ? "报警窗口隐藏" : "报警窗口显示"
        })

        // 为了防止其它对象收不到消息，所以将start放在最后
        netWork.start();

        // 定义全局函数供cef调用
        window.set_global_state = function (state) {

            // 设置场段和车辆的状态
            parkMap.setGlobalState(state);

            //处理计划勾指令
            state = state.data

            if (state.type == 'executeInstruct') {
                parkMap.executeInstruct(state)
            } else if (state.type == 'shadingSignal') {
                parkMap.shadingSignal(state)
            } else if (state.type == 'getControlPlan') { // 发送状态
                console.log('get get control plan msg:', state)
                // 发送给其它页面
                parkMap.sendControlPlan()
            }
        }

        if (urlParams['debug']) {
            var state = JSON.parse(xhr[xhr.length - 1].getText())
            set_global_state(state)
        }

        // 让后端发送数据
        var operation = new CefOperation()
        operation.cef_send({
            cmd: "load_finish",
            data: {
                title: window.document.title
            }
        })

        if (location == 'banqiao' || location == 'gaodalu') {
            editorUi.editor.graph.getView().setScale(0.92)
        }

        // 隐藏loading
        $('.loading_pic').hide();

        block_out.ShowBlockout();

    }, function () {
        document.body.innerHTML = '<center style="margin-top:10%;">加载资源出错!</center>';
    });
})();