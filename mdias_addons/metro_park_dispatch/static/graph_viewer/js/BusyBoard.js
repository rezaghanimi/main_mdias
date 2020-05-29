
BusyBoard = function (editorUi, parkMap, netWork) {
    mxEventSource.call(this);

    this.editorUi = editorUi
    this.editor = this.editorUi.editor
    this.graph = this.editor.graph
    this.parkMap = parkMap
    this.$el = undefined;
    this.netWork = netWork

    this.init();
};

mxUtils.extend(BusyBoard, mxEventSource);

BusyBoard.prototype.init = function () {
    var template =
        '<div class="busy_board">\
            <img class="busy_item" busy-type="construction" src="./images/construction.png" />\
            <img class="busy_item" busy-type="electric_stoped" src="./images/electric.png" />\
            <img class="busy_item" busy-type="area_block" src="./images/block.png" /></div>'
    this.$el = $(template)

    this.wnd = new mxWindow('占线板', this.$el[0], 1920 - 120, 60, 100, null, true, true);
    this.wnd.setMaximizable(true);
    this.wnd.setScrollable(true);
    this.wnd.setResizable(true);
    this.wnd.setVisible(true);

    // make the train dragable
    this.makeDragable()

    // 每次传过来的信息就是trainInfo对象
    var self = this
    this.netWork.addListener('update_busy_icons', function (sender, event) {
        console.log('update busy icons')
        var busyInfos = event.getProperty('msg_data')
        _.each(busyInfos, function (busyInfo) {
            var icons = busyInfo.icons
            var uid = busyInfo.uid.replace('/', '_')
            _.each(icons, function (icon) {
                if (icon == '') {
                    return
                }
                self.parkMap.SetBusyIconStatus({
                    "position": uid,
                    "busy_type": icon
                })
            })
        })
    })
}

BusyBoard.prototype.notifyServerAddBusyType = function (uid, busy_types) {
    var self = this
    var location = this.parkMap.location
    this.netWork.call_server_method('metro_park_base.busy_board',
        'set_busy_icon_status', {
        location_alias: location,
        operation: 'add',
        uid: uid,
        busy_types: busy_types
    }).then(function (res) {
        if (res == 'error') {
            // 后端更新以后再设置状态
            self.fireEvent(new mxEventObject('socket error, 更新占线板信息出错!'));
        }
    })
}

/**
 * 是否显示
 */
BusyBoard.prototype.isVisible = function () {
    return this.wnd.isVisible()
}

/**
 * 显示隐藏窗口
 */
BusyBoard.prototype.setVisible = function (show) {
    this.wnd.setVisible(show)
}

BusyBoard.prototype.makeDragable = function () {

    // 设置颜色
    mxConstants.DROP_TARGET_COLOR = '#FF0000'

    // Enables guides
    mxGraphHandler.prototype.guidesEnabled = true;

    // Alt disables guides
    mxGuide.prototype.isEnabledForEvent = function (evt) {
        return !mxEvent.isAltDown(evt);
    };

    // Enables snapping waypoints to terminals
    mxEdgeHandler.prototype.snapToTerminals = true;

    // Returns the graph under the mouse
    var self = this
    var graphF = function (evt) {
        var x = mxEvent.getClientX(evt);
        var y = mxEvent.getClientY(evt);
        var elt = document.elementFromPoint(x, y);

        if (mxUtils.isAncestorNode(self.graph.container, elt)) {
            return self.graph;
        }

        return null;
    };

    // Inserts a cell at the given location
    var self = this
    var funct = function (graph, evt, target, x, y) {
        if (target) {
            var busyType = $(this.element).attr('busy-type');
            var uid = target.getAttribute('uid');
            // 先从后端添加，再反馈到前端
            self.notifyServerAddBusyType(uid, [busyType])
        }
    };

    // Creates the element that is being for the actual preview.
    var busyIcons = this.$el.find(".busy_item")

    // Disables built-in DnD in IE (this is needed for cross-frame DnD, see below)
    if (mxClient.IS_IE) {
        mxEvent.addListener(busyIcons[0], 'dragstart', function (evt) {
            evt.returnValue = false;
        });
    }

    for (var i = 0; i < busyIcons.length; i++) {
        var el = busyIcons[i]
        var ds = mxUtils.makeDraggable(
            el,                         // element
            graphF,                     // graphF
            funct,                      // funct
            el,                         // dragElement
            null,                       // dx
            null,                       // dy
            true,                       // auto scroll
            true,                       // scalePreview,
            true,                       // highlight drop target
            this.getDropTarget          // getDropTarget
        );
        // Restores original drag icon while outside of graph
        ds.createDragElement = mxDragSource.prototype.createDragElement;
    }
}


/**
 * only get park element
 */
BusyBoard.prototype.getDropTarget = function (graph, x, y, evt) {

    var cell = graph.getCellAt(x, y);
    if (!cell) {
        return
    }

    // get the parent park element which has a uid attr
    cell = cell.getParkElement();
    if (!cell) {
        return
    }

    var cellType = cell.getAttribute("type")
    if (cellType == 'wc' || cellType == "ca") {
        return cell
    }

    return null
}
