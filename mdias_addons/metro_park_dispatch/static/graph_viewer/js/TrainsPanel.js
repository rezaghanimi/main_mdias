var gTrainPannel = undefined;
/**
 * 列车控制面版
 */
TrainsPannel = function (editorUi, parkMap, netWork) {
    mxEventSource.call(this);

    this.editorUi = editorUi
    this.editor = this.editorUi.editor
    this.graph = this.editor.graph
    this.parkMap = parkMap
    this.location = parkMap.location
    this.$el = undefined;
    this.netWork = netWork
    gTrainPannel = this

    // 网络连接成功时加载现车信息
    var self = this;
    netWork.addListener('socketio_connected', function () {
        self.getAllTrains();
    })

    // 每次传过来的信息就是trainInfo对象
    netWork.addListener('update_train_group_position', function (sender, event) {
        var groupsInfo = event.getProperty('msg_data')
        // 整理数据结构，兼容旧版接口
        self.updateCurtrains(groupsInfo)
    })

    // 老板本的
    netWork.addListener('update_train_position', function (sender, event) {
        var datas = event.getProperty('msg_data')
        var used_group_index = {}
        _.each(datas, (data) => {
            // 同一个组的车会一次性的全更新
            var group_index = data.group_index
            if (group_index in used_group_index)
                return
            used_group_index[group_index] = true
            self.parkMap.changeTrainPosition(data)
        })
    })

    this.init();
};

mxUtils.extend(TrainsPannel, mxEventSource);

TrainsPannel.prototype.init = function () {
    var template = '<div class="trainPannel"></div>'
    this.$el = $(template)

    this.wnd = new mxWindow('列车', this.$el[0], 10, 280, 180, null, true, true);

    this.wnd.setMaximizable(true);
    this.wnd.setScrollable(true);
    this.wnd.setResizable(true);
    this.wnd.setVisible(true);
}

TrainsPannel.prototype.addTrainItem = function (train_info) {
    var template = undefined
    var train_type = train_info.train_type
    switch (train_type) {
        case 'electric_train':
            template = `<div class="train_item" train_no="${train_info.train_no}">\
            <img class="electric_train" data-train-type="electric_train" \
            src="./images/electric_train.png"/><span>${train_info.train_no}</span></div>`
            break;
        case 'engine_train':
            template = `<div class='train_item' train_no="${train_info.train_no}">\
            <img class="engine_train" data-train-type="electric_train" \
            src="./images/electric_train.png"/><span>${train_info.train_no}</span></div>`
            break;
        default:
            break;
    }
    $(template).appendTo(this.$el)
}

/**
 * only get park element
 */
TrainsPannel.prototype.getDropTarget = function (graph, x, y, evt) {

    var cell = graph.getCellAt(x, y);
    if (!cell) {
        return
    }

    var cellType = cell.getAttribute("type")
    if (cellType == 'wc'
        || cellType == "ca"
        || cellType == "train_head"
        || cellType == "train_tail"
        || cellType == 'train_carriage') {
        return cell
    }

    return null
}

/**
 * 更新车辆的位置信息
 */
TrainsPannel.prototype.update_train_position = function (infos) {
    this.netWork.call_server_method(
        'metro_park_dispatch.cur_train_manage', 'update_train_position', {
        "infos": infos
    })
}

/**
 * 注意，这里this指向的是dragsource
 * @param {*} graph 
 * @param {*} evt 
 * @param {*} target 
 * @param {*} x 
 * @param {*} y 
 */
function dropFunction(graph, evt, target, x, y) {

    // 指向train_pannel对象
    var self = gTrainPannel

    if (!target) {
        return
    }

    var def = $.Deferred();

    // 如果dragSource为特定类型的话，可能是移动
    var dragSource = this.dragSource
    if (dragSource) {
        var dragSourceType = dragSource.getAttribute('type')
        if (dragSourceType == 'train_body'
            || dragSourceType == 'train_head'
            || dragSourceType == 'train_tail') {
            var uid = target.getAttribute('uid')
            var group_index = self.parkMap.getGroupIndex(uid, x, y)
            var train = dragSourceType == 'train_body' ? dragSource : dragSource.getParent()
            var infos = []
            var carriagesNum = train.children.length
            // 查找dragCarriage
            var dragCarriage = _.find(train.children, function (carriage) {
                var index = parseInt(carriage.getAttribute('carriage_index'))
                if (index == 1) { return true }
                return false
            })
            var dragTrainNo = dragCarriage.getAttribute('train_no')
            for (var i = 0; i < carriagesNum; i++) {
                var carriage = train.children[i]
                var type = carriage.getAttribute('type')
                var train_no = carriage.getAttribute('train_no')
                if (type == 'train_body' || type == 'train_head' || type == 'train_tail') {
                    continue
                }
                infos.push({
                    "uid": uid,
                    "train_no": train_no,
                    "carriage_index": parseInt(carriage.getAttribute('carriage_index')),
                    "drag_train_no": dragTrainNo,
                    "group_index": group_index
                })
            }
            // 先通知后端处理
            self.netWork.call_server_method(
                'metro_park_dispatch.cur_train_manage',
                'update_train_info', {
                "infos": infos,
                "location_alias": self.location
            })
            return
        } else {
            // 如果是将车拖出来的话，需要更新index信息等
            var carriage = dragSource
            var carriage_index = parseInt(carriage.getAttribute('carriage_index'))
            var train = carriage.getParent()
            var old_position = train.getAttribute('position')
            var carriages = train.children
            // 一头一尾加上自身
            if (carriages.length > 3) {
                var infos = []
                // 如果是拖动的第一节则使用2作为分组的头
                var drag_train = _.find(carriages, function (carriage) {
                    var tmp_index = parseInt(carriage.getAttribute('carriage_index'))
                    if (carriage_index == 1) {
                        return tmp_index == 2
                    } else {
                        return tmp_index == 1
                    }
                })
                var drag_train_no = drag_train.getAttribute('train_no')
                _.each(carriages, function (carriage) {
                    var tmp_carriage_index = parseInt(carriage.getAttribute('carriage_index'))
                    var type = carriage.getAttribute('type')
                    if (type == 'train_head' || type == 'train_tail' || type == 'train_body') {
                        return
                    }
                    if (tmp_carriage_index > carriage_index) {
                        var train_no = carriage.getAttribute('train_no')
                        infos.push({
                            "uid": old_position,
                            "train_no": train_no,
                            "carriage_index": tmp_carriage_index - 1,
                            "drag_train_no": drag_train_no
                        })
                    }
                })
                // 先更新考的车信息
                self.netWork.call_server_method(
                    'metro_park_dispatch.cur_train_manage',
                    'update_train_info', {
                    "infos": infos,
                    "location_alias": self.location
                }).then(function () {
                    // 更新index
                    _.each(carriages, function (carriage) {
                        var tmp_carriage_index = parseInt(carriage.getAttribute('carriage_index'))
                        var type = carriage.getAttribute('type')
                        if (type == 'train_head' || type == 'train_tail' || type == 'train_body') {
                            return
                        }
                        if (tmp_carriage_index > carriage_index) {
                            carriage.setAttribute('carriage_index', tmp_carriage_index - 1)
                        }
                    })
                    def.resolve()
                })
            } else {
                def.resolve()
            }
        }
    } else {
        def.resolve()
    }

    // 只有从pannel拖过来的才
    def.then(() => {
        var type = target.getAttribute('type')
        var train = undefined;
        switch (type) {
            case 'wc':
            case 'ca':
                // 先推送到后端，然后再前端再添加
                var uid = target.getAttribute('uid')
                var group_index = self.parkMap.getGroupIndex(uid, x, y)
                self.netWork.call_server_method(
                    'metro_park_dispatch.cur_train_manage',
                    'update_train_info', {
                    "infos": [{
                        "uid": uid,
                        "train_no": this.train_no,
                        "carriage_index": 0,
                        "drag_train_no": this.train_no,
                        "group_index": group_index
                    }],
                    "location_alias": self.location
                })
                break;

            // 拖动到train_carriage上面
            case 'train_carriage':
                var infos = []
                var carriage_index = parseInt(target.getAttribute('carriage_index'))
                var train = target.getParent()
                var carriagesNum = train.children.length
                // 查找drag_train
                var dragCarriage = _.find(train.children, function (carriage) {
                    var index = parseInt(carriage.getAttribute('carriage_index'))
                    // train_head为0
                    if (index == 1) {
                        return true
                    }
                    return false
                })
                if (!dragCarriage) {
                    console.log('can not find the drag carriage')
                    dragCarriage = _.find(train.children, function (carriage) {
                        return carriage.getAttribute('is_carriage')
                    })
                }
                var dragTrainNo = dragCarriage.getAttribute("train_no")
                var uid = train.getAttribute('position')
                var group_index = train.getAttribute('group_index')

                for (var i = 0; i < carriagesNum; i++) {
                    var carriage = train.children[i]
                    var train_no = carriage.getAttribute('train_no')
                    var type = carriage.getAttribute('type')
                    if (type == 'train_body' || type == 'train_head' || type == 'train_tail') {
                        continue
                    }
                    var index = parseInt(carriage.getAttribute("carriage_index"))
                    if (index < carriage_index + 1) {
                        infos.push({
                            "uid": uid,
                            "train_no": train_no,
                            "carriage_index": index,
                            "drag_train_no": dragTrainNo,
                            "group_index": group_index
                        })
                    } else {
                        infos.push({
                            "uid": uid,
                            "train_no": train_no,
                            "carriage_index": index + 1,
                            "drag_train_no": dragTrainNo,
                            "group_index": group_index
                        })
                    }
                }
                infos.push({
                    "uid": uid,
                    "train_no": this.train_no,
                    "carriage_index": carriage_index + 1,
                    "drag_train_no": dragTrainNo,
                    "group_index": group_index
                })
                self.netWork.call_server_method(
                    'metro_park_dispatch.cur_train_manage',
                    'update_train_info', {
                    "infos": infos,
                    "location_alias": self.location
                })
                break;

            case 'train_head':
                var infos = []
                var carriage_index = parseInt(target.getAttribute('carriage_index'))
                var train = target.getParent()
                var carriagesNum = train.children.length
                var group_index = train.getAttribute('train_index')
                // 查找drag_train
                var dragCarriage = _.find(train.children, function (carriage) {
                    var index = parseInt(carriage.getAttribute('carriage_index'))
                    // train_head为0
                    if (index == 1) {
                        return true
                    }
                    return false
                })
                var dragTrainNo = dragCarriage.getAttribute('train_no')
                for (var i = 0; i < carriagesNum; i++) {
                    var carriage = train.children[i]
                    var type = carriage.getAttribute('type')
                    if (type == 'train_body' || type == 'train_head' || type == 'train_tail') {
                        continue
                    }
                    infos.push({
                        "uid": uid,
                        "train_no": this.train_no,
                        "carriage_index": parseInt(carriage.getAttribute('carriage_index')) + 1,
                        "drag_train_no": dragTrainNo,
                        "group_index": group_index
                    })
                }
                infos.push({
                    "uid": uid,
                    "train_no": this.train_no,
                    "carriage_index": 1, // 从1开始
                    "drag_train_no": dragTrainNo,
                    "group_index": group_index
                })
                self.netWork.call_server_method(
                    'metro_park_dispatch.cur_train_manage',
                    'update_train_info', {
                    "infos": infos,
                    "location_alias": self.location
                })
                break;

            case 'train_tail':
                var infos = []
                var carriage_index = parseInt(target.getAttribute('carriage_index'))
                var train = target.getParent()
                var group_index = train.getAttribute('group_index')
                // 查找drag_train
                var dragCarriage = _.find(train.children, function (carriage) {
                    var index = carriage.getAttribute('carriage_index')
                    // train_head为0
                    if (index == 1) {
                        return true
                    }
                    return false
                })
                var dragTrainNo = dragCarriage.getAttribute('train_no')
                var carriagesNum = train.children
                infos.push({
                    "uid": uid,
                    "train_no": this.train_no,
                    "carriage_index": carriagesNum,
                    "drag_train_no": dragTrainNo,
                    "group_index": group_index
                })
                self.netWork.call_server_method(
                    'metro_park_dispatch.cur_train_manage',
                    'update_train_info', {
                    "infos": infos,
                    "location_alias": self.location
                })
                break;
        }
    })
};

TrainsPannel.prototype.makeDraggable = function () {

    mxConstants.DROP_TARGET_COLOR = '#FF0000'

    // Enables guides
    mxGraphHandler.prototype.guidesEnabled = true;

    // Alt disables guides
    mxGuide.prototype.isEnabledForEvent = function (evt) {
        return !mxEvent.isAltDown(evt);
    };

    // Enables snapping waypoints to terminals
    mxEdgeHandler.prototype.snapToTerminals = true;

    // Creates the element that is being for the actual preview.
    var trains = this.$el.find(".train_item")

    // Disables built-in DnD in IE (this is needed for cross-frame DnD, see below)
    if (mxClient.IS_IE) {
        mxEvent.addListener(trains, 'dragstart', function (evt) {
            evt.returnValue = false;
        });
    }

    var self = this
    function findGraphFunc(evt) {
        var x = mxEvent.getClientX(evt);
        var y = mxEvent.getClientY(evt);
        var elt = document.elementFromPoint(x, y);

        if (mxUtils.isAncestorNode(self.graph.container, elt)) {
            return self.graph;
        }

        return null;
    };

    // set the train draggable
    for (var i = 0; i < trains.length; i++) {
        var train = trains[i]
        var el = $(train).find('img')[0]
        // 动态生成一个dragSource对象
        var ds = mxUtils.makeDraggable(
            el,                                     // element
            findGraphFunc,                          // graphF
            dropFunction,                           // funct
            el,                                     // dragElement
            null,                                   // dx
            null,                                   // dy
            true,                                   // auto scroll
            true,                                   // scalePreview,
            true,                                   // highlight drop target
            this.getDropTarget                      // getDropTarget
        );
        // Restores original drag icon while outside of graph
        ds.dragSource = undefined
        ds.train_no = $(train).attr('train_no')
        ds.createDragElement = function () {
            if (!this.dragImg) {
                this.dragImg = el.cloneNode(true);
            }
            return this.dragImg.cloneNode(true);
        };
    }
}

/**
 * 是否显示
 */
TrainsPannel.prototype.isVisible = function () {
    return this.wnd.isVisible()
}

/**
 * 显示隐藏窗口
 */
TrainsPannel.prototype.setVisible = function (show) {
    this.wnd.setVisible(show)
}

/**
 * 让cells可以拖动
 */
TrainsPannel.prototype.makeCellDraggable = function (cells) {
    var self = this

    function findGraphFunc(evt) {
        var x = mxEvent.getClientX(evt);
        var y = mxEvent.getClientY(evt);
        var elt = document.elementFromPoint(x, y);

        if (mxUtils.isAncestorNode(self.graph.container, elt)) {
            return self.graph;
        }
        return null;
    };

    self.graph.model.beginUpdate();
    try {
        // 显示的img
        var dragImg = $('<img class="electric_train train_item" \
        data-train-type="electric_train" src="./images/electric_train.png"/>')
        _.each(cells, function (cell) {
            var train_no = cell.getAttribute('train_no')

            // 让车可以拖动
            // 这里有时获取不到, 有点奇怪
            var state = self.graph.getView().getState(cell);
            if (!state) {
                console.log('can not get the state!')
                return
            }
            var node = state.shape.node
            if (state.text) {
                var $text = $(state.text.node)
                $text.css('pointer-events', 'none')
            }
            var ds = mxUtils.makeDraggable(
                node,                                           // element
                findGraphFunc,                                  // graphF
                dropFunction,                                   // funct
                dragImg[0],                                     // dragElement
                null,                                           // dx
                null,                                           // dy
                true,                                           // auto scroll
                true,                                           // scalePreview,
                true,                                           // highlight drop target
                self.getDropTarget                              // getDropTarget
            );

            ds.dragSource = cell
            ds.train_no = train_no
            ds.createDragElement = function () {
                if (!this.dragImg) {
                    this.dragImg = dragImg[0].cloneNode(true);
                }
                return this.dragImg.cloneNode(true);
            };
        })
    }
    finally {
        self.graph.model.endUpdate();
    }
}

/**
 * 更新现车位置
 */
TrainsPannel.prototype.updateCurtrains = function (groupsInfo) {
    var self = this
    this.parkMap.initTrainPosition(groupsInfo).then(function (cells) {
        self.makeCellDraggable(cells)
    })
}

/**
 * 取得所有的车辆
 */
TrainsPannel.prototype.getAllTrains = function () {
    var self = this
    this.netWork.call_server_method(
        'metro_park_dispatch.cur_train_manage', 'get_cur_trains', {}).then(function (trains) {
            for (var i = 0; i < trains.length; i++) {
                var train = trains[i]
                self.addTrainItem(train)
            }
            self.makeDraggable()
            return self.parkMap.initTrainPosition()
        }).then(function (cells) {
            self.makeCellDraggable(cells)
        })
}
