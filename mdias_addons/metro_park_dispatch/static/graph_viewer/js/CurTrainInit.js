(function () {

    mxResources.loadDefaultBundle = false;
    var bundle = mxResources.getDefaultBundle(RESOURCE_BASE, mxLanguage) ||
        mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);

    // Fixes possible asynchronous requests
    var location = urlParams['location'] || 'banqiao'
    var url = STATION_DATA_PATH + '/' + location + '/cur_train.xml'
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
        var location = urlParams['location'] || 'banqiao'
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
                "disableOperation": true,
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
                "disableOperation": true,
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

        // 列车
        var train_pannel = new TrainsPannel(editorUi, parkMap, netWork);

        // 报警
        var alarm_lsit = new AlarmList(editorUi, parkMap)

        // 占线板
        var busy_board = new BusyBoard(editorUi, parkMap, netWork)

        // 底部
        new ParkFooter(editorUi, parkMap)

        window.block_out = new BlackOut(editorUi, parkMap)

        // 为了防止其它对象收不到消息，所以将start放在最后
        netWork.start();

        // 定义全局函数供cef调用
        window.set_global_state = function (state) {
            // 设置场段和车辆的状态
            parkMap.setGlobalState(state);
        }

        if (urlParams['debug']) {
            var state = JSON.parse(xhr[xhr.length - 1].getText())
            set_global_state(state)
        }

        if (urlParams['show_type']) {
            train_pannel.setVisible(false)
            alarm_lsit.setVisible(false)
            busy_board.setVisible(false)
        }

        // 让后端发送数据
        var operation = new CefOperation()
        operation.cef_send({
            cmd: "load_finish",
            data: {
                title: window.document.title
            }
        })

        if (location == 'banqiao') {
            editorUi.editor.graph.getView().setScale(0.92)
        }

        // 隐藏loading
        $('.loading_pic').hide();

        block_out.ShowBlockout();

    }, function () {
        document.body.innerHTML = '<center style="margin-top:10%;">加载资源出错!</center>';
    });
})();