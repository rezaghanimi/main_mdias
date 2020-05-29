OperationToolBar = function (editorUi, parkMap) {
    mxEventSource.call(this);

    this.editorUi = editorUi
    this.editor = this.editorUi.editor
    this.graph = this.editor.graph
    this.container = editorUi.container
    this.parkMap = parkMap
    this.$el = undefined;
    this.init();
};

mxUtils.extend(OperationToolBar, mxEventSource);

OperationToolBar.prototype.init = function () {
    var template = '<div class="operation_toolbar">\
        <input id="graph_action_hidden" style="display:none;" type="text" />\
        <button class="btn btn-light action_button" action="all_lock" style="color:red" type="button">引导<br>总锁</button>\
        <button class="btn btn-light action_button" action="all_cancel" type="button">总取消</button>\
        <button class="btn btn-light action_button" action="all_relieve" style="color:red" type="button">总人解</button>\
        <button class="btn btn-light action_button" action="sector_fault_unlock" style="color:red" type="button">区故解</button>\
        <button class="btn btn-light action_button" action="switch_direct" type="button">总定位</button>\
        <button class="btn btn-light action_button" action="switch_reverse" type="button">总反位</button>\
        <button class="btn btn-light action_button no_focus" action="clear_action" type="button">清除</button>\
        <button class="btn btn-light action_button" action="switch_lock" type="button">单锁</button>\
        <button class="btn btn-light action_button" action="switch_unlock" type="button">单解</button>\
        <button class="btn btn-light action_button" action="signal_block" type="button">按钮<br>封锁</button>\
        <button class="btn btn-light action_button" action="signal_unblock" type="button">按钮<br>解封</button>\
        <button class="btn btn-light action_button" action="switch_block" type="button">道岔<br>封锁</button>\
        <button class="btn btn-light action_button" action="switch_unblock" type="button">道岔<br>解封</button>\
        <button class="btn btn-light action_button asist_menu" type="button">辅助<br>菜单</button>\
        <div class="sub_menu" style="display: none;">\
            <button class="btn btn-light manual_confirm_mode_toggle" type="button">人工确认模式</button>\
            <button class="btn btn-light toggle_switch_name" type="button">道岔名称隐藏</button>\
            <button class="btn btn-light toggle_signal_name" type="button">信号名称隐藏</button>\
            <button class="btn btn-light toggle_switch_section_name" type="button">道岔区段名称隐藏</button>\
            <button class="btn btn-light toggle_normal_section_name" type="button">无岔区段名称隐藏</button>\
            <button class="btn btn-light toggle_switch_positon" type="button">道岔位置隐藏</button>\
            <button class="btn btn-light light_belt" type="button">接通光带</button>\
            <button class="btn btn-light pofeng_statistic" type="button">破封统计</button>\
            <button class="btn btn-light toggle_alarm_window" type="button">报警窗口隐藏</button>\
            <button class="btn btn-light dispatch_plan" type="button">调度计划</button>\
            <button class="btn btn-light toggle_busy_board" type="button">占 线 板</button>\
            <button class="btn btn-light toggle_train" type="button">隐藏列车</button>\
            <button class="btn btn-light toggle_train_orders" type="button">列车置顶</button>\
            <button class="btn btn-light close_sub_menu" type="button">退出菜单</button>\
        </div>\
    </div>'

    // <button class="btn btn-light action_button" action="guide_open" style="color:red" type="button">开放引导</button>\
    // <button class="btn btn-light action_button" action="switch_block" type="button">道岔<br>封锁</button>\
    // <button class="btn btn-light action_button" action="switch_unblock" type="button">道岔<br>解封</button>\
    if (this.parkMap.location == "yuanhua") {
        template = '<div class="operation_toolbar">\
        <input id="graph_action_hidden" style="display:none;" type="text" />\
        <button class="btn btn-light action_button" action="all_lock" style="color:red" type="button">引导<br>总锁</button>\
        <button class="btn btn-light action_button" action="guide_road"  style="color:red" type="button">引导<br>进路</button>\
        <button class="btn btn-light action_button" action="another_road_way type="button">变通<br>进路</button>\
        <button class="btn btn-light action_button" action="all_cancel" type="button">总取消</button>\
        <button class="btn btn-light action_button" action="all_relieve" style="color:red" type="button">总人解</button>\
        <button class="btn btn-light action_button" action="sector_fault_unlock" style="color:red" type="button">区故解</button>\
        <button class="btn btn-light action_button" action="switch_direct" type="button">道岔<br>总定</button>\
        <button class="btn btn-light action_button" action="switch_reverse" type="button">道岔<br>总反</button>\
        <button class="btn btn-light action_button" action="switch_lock" type="button">道岔<br>单锁</button>\
        <button class="btn btn-light action_button" action="switch_unlock" type="button">道岔<br>单解</button>\
        <button class="btn btn-light action_button" action="signal_block" type="button">封锁<br>按钮</button>\
        <button class="btn btn-light action_button" action="signal_unblock" type="button">解封<br>按钮</button>\
        <button class="btn btn-light action_button no_focus" action="clear_action" type="button">清除</button>\
        <button class="btn btn-light action_button asist_menu" type="button">辅助<br>菜单</button>\
        <div class="sub_menu" style="display: none;">\
            <button class="btn btn-light manual_confirm_mode_toggle" type="button">人工确认模式</button>\
            <button class="btn btn-light toggle_switch_name" type="button">道岔名称隐藏</button>\
            <button class="btn btn-light toggle_signal_name" type="button">信号名称隐藏</button>\
            <button class="btn btn-light toggle_switch_section_name" type="button">道岔区段名称隐藏</button>\
            <button class="btn btn-light toggle_normal_section_name" type="button">无岔区段名称隐藏</button>\
            <button class="btn btn-light toggle_switch_positon" type="button">道岔位置隐藏</button>\
            <button class="btn btn-light light_belt" type="button">接通光带</button>\
            <button class="btn btn-light pofeng_statistic" type="button">破封统计</button>\
            <button class="btn btn-light toggle_alarm_window" type="button">报警窗口隐藏</button>\
            <button class="btn btn-light dispatch_plan" type="button">调度计划</button>\
            <button class="btn btn-light toggle_busy_board" type="button">占 线 板</button>\
            <button class="btn btn-light toggle_train" type="button">隐藏列车</button>\
            <button class="btn btn-light toggle_train_orders" type="button">列车置顶</button>\
            <button class="btn btn-light close_sub_menu" type="button">退出菜单</button>\
        </div>\
    </div>'
    }


    var self = this;
    this.$el = $(template);
    this.$el.appendTo(this.container);

    /**
     * 辅助菜单，包含Vue和jquery实现的一些功能
     */
    mxEvent.addListener(this.$el.find('.sub_menu button')[0], 'click', function (event) {
        self.$('.sub_menu').hide()
    });

    mxEvent.addListener(this.$el.find('.asist_menu')[0], 'click', function (event) {
        self.$el.find('.sub_menu').show()
    });

    mxEvent.addListener(this.$el.find('.close_sub_menu')[0], 'click', function (event) {
        self.$('.sub_menu').hide()
    });

    // 按扭响应事件
    this.$el.find('button.action_button').on('click', function (event) {
        var target = $(event.target)
        var action = target.attr("action")
        switch (action) {
            case 'all_lock':
                //引导总锁
                self.parkMap.buttonClick('all_lock')
                break
            case 'guide_road':
                //引导进路办理
                self.parkMap.buttonClick('guide_road')
                break
            case 'guide_open':
                //开放引导
                self.parkMap.buttonClick('guide_open')
                break
            case 'another_road_way':
                //变通进路
                self.parkMap.buttonClick('another_road_way')
                break
            case 'all_cancel':
                //总取消
                self.parkMap.buttonClick('all_cancel')
                break
            case 'all_relieve':
                //取消引导进路
                self.parkMap.buttonClick('all_relieve')
                break
            case 'sector_fault_unlock':
                //区段故障解锁
                self.parkMap.buttonClick('sector_fault_unlock')
                break
            case 'switch_direct':
                //道岔总定
                self.parkMap.buttonClick('switch_direct')
                break
            case 'switch_reverse':
                //道岔总反
                self.parkMap.buttonClick('switch_reverse')
                break
            case 'clear_action':
                //清除
                self.parkMap.buttonClick('clear_action')
                break
            case 'switch_lock':
                //道岔单锁
                self.parkMap.buttonClick('switch_lock')
                break
            case 'switch_unlock':
                //道岔解锁
                self.parkMap.buttonClick('switch_unlock')
                break
            case 'signal_block':
                //道岔解锁
                self.parkMap.buttonClick('signal_block')
                break
            case 'signal_unblock':
                //道岔解锁
                self.parkMap.buttonClick('signal_unblock')
                break
            case 'switch_block':
                //道岔单封
                self.parkMap.buttonClick('switch_block')
                break
            case 'switch_unblock':
                //道岔解封
                self.parkMap.buttonClick('switch_unblock')
                break
        }
    })

    // 点击其它按扭时候
    this.$('.action_button').on('click', function (event) {
        self.$('.graph_action_sub_menu').toggle()
    })

    // 人工确认模式
    mxEvent.addListener(this.$('.manual_confirm_mode_toggle')[0], 'click', function (event) {
        if (self.manualConfirmPlan) {
            self.manualConfirmPlan = true
        } else {
            self.manualConfirmPlan = false
        }
    });

    // 显示隐藏道岔名称
    mxEvent.addListener(this.$('.toggle_switch_name')[0], 'click', function (event) {
        self.parkMap.hideSwitchName = !self.parkMap.hideSwitchName
        if (self.parkMap.hideSwitchName) {
            self.$('.toggle_switch_name').html('道岔名称显示')
        } else {
            self.$('.toggle_switch_name').html('道岔名称隐藏')
        }
        self.parkMap.updateSwitches()
    });

    // 显示隐藏道岔区段名称
    mxEvent.addListener(this.$('.toggle_switch_section_name')[0], 'click', function (event) {
        self.parkMap.hideSwitchSectionName = !self.parkMap.hideSwitchSectionName
        if (self.parkMap.hideSwitchSectionName) {
            self.$('.toggle_switch_section_name').html('道岔区段名称显示')
        } else {
            self.$('.toggle_switch_section_name').html('道岔区段名称隐藏')
        }
        // 这个处理比较特殊
        self.parkMap.UpdateSwitchSectionName()
    });

    // 显示隐藏信号机名称
    mxEvent.addListener(this.$('.toggle_signal_name')[0], 'click', function (event) {
        self.parkMap.hideSignalName = !self.parkMap.hideSignalName
        if (self.parkMap.hideSignalName) {
            self.$('.toggle_signal_name').html('信号名称显示')
        } else {
            self.$('.toggle_signal_name').html('信号名称隐藏')
        }
        self.parkMap.UpdateSignal()
    });

    // 显示无岔区段显示隐藏名称
    mxEvent.addListener(this.$('.toggle_normal_section_name')[0], 'click', function (event) {
        self.parkMap.hideSectionName = !self.parkMap.hideSectionName
        if (self.parkMap.hideSectionName) {
            self.$('.toggle_normal_section_name').html('无岔区段名称显示')
        } else {
            self.$('.toggle_normal_section_name').html('无岔区段名称隐藏')
        }
        self.parkMap.udpateRailSec()
    });

    // 显示道岔位置
    mxEvent.addListener(this.$('.toggle_switch_positon')[0], 'click', function (event) {
        self.parkMap.hideSwitchPosition = !self.parkMap.hideSwitchPosition
        if (self.parkMap.hideSwitchPosition) {
            self.$('.toggle_switch_positon').html('道岔位置显示')
        } else {
            self.$('.toggle_switch_positon').html('道岔位置隐藏')
        }
        self.parkMap.updateSwitches()
    });

    // 接通光带
    mxEvent.addListener(this.$('.light_belt')[0], 'click', function (event) {
        if (!self.parkMap.showLightBelt) {

            // 5秒后解除
            setTimeout(() => {
                self.parkMap.showLightBelt = false
                // 恢复显示
                self.parkMap.updateSwitches()
            }, 15000);

            self.parkMap.showLightBelt = true
            self.parkMap.updateSwitches()
        }
    });

    // 破封统计
    mxEvent.addListener(this.$el.find('.pofeng_statistic')[0], 'click', function (event) {
        pop.alert({
            title: "破封统计",
            content: (() => {
                var x = ''
                self.parkMap.breakStatistics.map(static => {
                    var y = static.key + ':' + static.value
                    x += `<p>${y}</p>`
                })
                return x
            })(),
            button: ["primary", "确定", function (e) {
                pop.close(e)
            }],
            buttonSpcl: "",
            sizeAdapt: false,
            anim: "fadeIn-zoom",
            width: 450,
            height: 200,
            id: "mdias_pop_" + self.parkMap.popId++,
            place: 5,
            drag: true,
            index: true,
            toClose: true,
            mask: false,
            class: false
        });
    });

    // 显示警告窗口
    mxEvent.addListener(this.$el.find('.toggle_alarm_window')[0], 'click', function (event) {
        self.fireEvent(new mxEventObject('toggle_alarm_window'));
    });

    // 显示调车计划窗口
    mxEvent.addListener(this.$el.find('.dispatch_plan')[0], 'click', function (event) {
        self.fireEvent(new mxEventObject('show_dispatch_window'));
    });

    // 占线板
    mxEvent.addListener(this.$el.find('.toggle_busy_board')[0], 'click', function (event) {
        self.fireEvent(new mxEventObject('toggle_busy_board'));
    });

    // 显示隐藏列车
    mxEvent.addListener(this.$el.find('.toggle_train')[0], 'click', function (event) {
        self.fireEvent(new mxEventObject('toggle_train'));
    });

    // 列车置顶
    mxEvent.addListener(this.$el.find('.toggle_train_orders')[0], 'click', function (event) {
        self.fireEvent(new mxEventObject('toggle_train_orders'));
    });

    /**
     * 设置update_bottom_btn_style
     */
    this.parkMap.addListener('update_bottom_btn_style', function (sender, evt) {
        var css = evt.getProperty('css');
        var status = evt.getProperty('status');
        var $el = self.$el.find("[action='all_lock']")
        if (status.light) {
            $el.css(css)
        } else {
            $el.attr('style', css)
        }
    })
}

OperationToolBar.prototype.$ = function (selector) {
    return this.$el.find(selector)
}

OperationToolBar.prototype.getAllRelieveBtn = function (selector) {
    return this.$('[action="all_relieve"]')
}

OperationToolBar.prototype.getSectorDefaultUnlockBtn = function (selector) {
    return this.$('[action="sector_fault_unlock"]')
}

OperationToolBar.prototype.getGuidedRoadBtn = function (selector) {
    return this.$('[action="guide_road"]')
}

OperationToolBar.prototype.getGuidedOpenBtn = function (selector) {
    return this.$('[action="guide_open"]')
}

OperationToolBar.prototype.getAllLockBtn = function (selector) {
    return this.$('[action="all_lock"]')
}