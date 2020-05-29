
AlarmList = function (editorUI, parkMap) {
    mxEventSource.call(this);

    this.parkMap = parkMap
    this.editorUI = editorUI
    this.$list = undefined;
    this.wnd = undefined;
    this.$el = undefined;

    this.render();
    this.initListener();
};

mxUtils.extend(AlarmList, mxEventSource);

AlarmList.prototype.render = function() {

    var windowContent = 
    '<div class="alarm_list"\
        style="width:100%; height: 100%; background:white; overflow-y: auto; background: #e03030;">\
    </div>'
    this.$el = $(windowContent);

    this.wnd = new mxWindow('提示信息', this.$el[0], 10, 10, 260, 220, true, true);
    this.wnd.setMaximizable(true);
    this.wnd.setScrollable(true);
    this.wnd.setResizable(true);
    this.wnd.setVisible(true);

    this.$el = $(this.wnd.getElement())
    this.$list = this.$el.find(".alarm_list")
}

AlarmList.prototype.addAlarm = function(msg) {
    var items = this.$list.find('p')
    if (items.length > 1000) {
        items[items.length - 1].remove()
    }
    var record = `${moment().format("YY-MM-DD HH:mm:ss")}:      ${msg}`
    this.$list.prepend(`<p>${record}</p>`)
    this.$list.scrollTop(0)
}

/**
 * 初始化事件监听
 */
AlarmList.prototype.initListener = function() {
    var self = this
    this.parkMap.addListener('add_interlock_alarm', function (sender, evt) {
        var msg = evt.getProperty('msg');
        self.addAlarm(msg)
    })
}

/**
 * 是否显示
 */
AlarmList.prototype.isVisible = function () {
    return this.wnd.isVisible()
}

/**
 * 显示隐藏窗口
 */
AlarmList.prototype.setVisible = function (show) {
    this.wnd.setVisible(show)
}