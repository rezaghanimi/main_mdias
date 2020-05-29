
Keyboard = function (parkMap, editorUI) {
    mxEventSource.call(this);

    this.parkMap = parkMap;
    this.editorUI = editorUI;
    this.container = editorUI.container;
    this.keyboard = undefined;

    this.render();
    this.initKeyboard();
};

mxUtils.extend(Keyboard, mxEventSource);

Keyboard.prototype.render = function () {
    this.$el = $('<input id="keyboard" type="text" style="display:none; position=absolute; bottom: 0px;" />')
    $(this.container).append(this.$el)
    this.$overlay = $('<div class="keyboardOverlay" />')
    $(this.container).append(this.$overlay)
}

Keyboard.prototype.setPosition = function (element) {
    console.log(element)
    this.keyboard.options.position.of = element
    this.keyboard.reposition();
}

/**
 * 显示键盘
 */
Keyboard.prototype.reveal = function (callBack) {
    if (callBack) {
        this.callBack = callBack
    } else {
        this.callBack = function () { }
    }
    this.keyboard.reveal().insertText('')
}

Keyboard.prototype.initKeyboard = function () {

    // keyboard插件初始化
    this.$el.keyboard({
        layout: 'qwerty',
        position: {
            of: this.$el,
            my: 'center top',
            at: 'center top'
        }
    }).addTyping();

    var self = this
    this.keyboard = this.$el.getkeyboard()
    $('.ui-keyboard-input').bind(
        'visible hidden beforeClose accepted canceled restricted',
        function (e, keyboard, el, status) {
            switch (e.type) {
                case 'visible':
                    self.$overlay.show()
                    break;

                case 'hidden':
                    self.$overlay.hide()
                    break;

                case 'accepted':
                    //把点击按钮和部件发送给graphAction处理
                    if (self.parkMap.status == 17) { 
                        // 添加车辆信息
                        self.parkMap.graphActionCallback()
                    } else if (self.keyboard.getValue() == '123') {
                        switch (self.parkMap.status) {

                            case 3:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '引导进路口令正确'));
                                self.parkMap.buttonClick('confirmya')
                                break

                            case 5:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '总人解口令正确'));
                                self.callBack()
                                break

                            case 13:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '区故解口令正确'));
                                self.callBack()
                                break

                            case 14:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '引导总锁口令正确'));
                                self.callBack()
                                break

                            case 110:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '非进路故障解锁1口令正确'));
                                self.callBack()
                                break
                        }
                    } else {
                        switch (self.parkMap.status) {
                            case 3:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '引导进路口令错误'));
                                self.parkMap.buttonClick('confirmya')
                                break

                            case 5:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '总人解口令错误'));
                                self.callBack()
                                break

                            case 13:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '区故解口令错误'));
                                self.callBack()
                                break

                            case 14:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '引导总锁口令错误'));
                                self.callBack()
                                break

                            case 110:
                                self.parkMap.fireEvent(new mxEventObject(
                                    'add_warning', 'msg', '非进路故障解锁1口令错误'));
                                self.callBack()
                                break
                        }

                        self.parkMap.resetStatus()
                    }
                    break;

                case 'canceled':
                    self.parkMap.resetStatus()
                    break;

                case 'restricted':
                    break;

                case 'beforeClose':
                    break;
            }

            self.$el.val('')
        });
}