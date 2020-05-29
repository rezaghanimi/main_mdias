ParkFooter = function (editorUI, parkMap) {
    mxEventSource.call(this);
    this.parkMap = parkMap
    this.editorUI = editorUI
    this.container = editorUI.container
    this.init()
    this.timeTick()
};

mxUtils.extend(ParkFooter, mxEventSource);

ParkFooter.prototype.init = function (data) {
    var template =
        '<div class="park_footer">\
            <div class="signal_name"></div>\
            <div></div>\
            <div class="warning_container">\
                <span></span>\
                <div class="alarm_warning_list">\
                </div>\
            </div>\
            <div class="counting_down"></div>\
            <div class="timer">time</div>\
        </div>'

    this.$el = $(template)
    this.$el.appendTo(this.container)

    this.initListener()
}

ParkFooter.prototype.timeTick = function () {
    setInterval(() => {
        this.$el.find('.timer').html(moment().format('YYYY-MM-DD HH:mm:ss'))
    }, 1000);
}

ParkFooter.prototype.getSignalNameHtml = function () {
    return this.$el.find('.signal_name').html()
}

ParkFooter.prototype.setSignalNameHtml = function (html) {
    return this.$el.find('.signal_name').html(html)
}

ParkFooter.prototype.getCountingDownHtml = function () {
    return this.$el.find('.counting_down').html()
}

ParkFooter.prototype.setCountingDownHtml = function (html) {
    return this.$el.find('.counting_down').html(html)
}

ParkFooter.prototype.$ = function (selector) {
    return this.$el.find(selector)
}

ParkFooter.prototype.initListener = function () {
    var self = this

    mxEvent.addListener(this.$el.find('.warning_container')[0], 'mouseover', function (event) {
        self.$el.find('.alarm_warning_list').show()
    });

    mxEvent.addListener(this.$el.find('.warning_container')[0], 'mouseout', function (event) {
        self.$el.find('.alarm_warning_list').hide()
    });

    mxEvent.addListener(this.$el.find('.alarm_warning_list')[0], 'mouseout', function (event) {
        self.$el.find('.alarm_warning_list').hide()
    });

    mxEvent.addListener(this.$el.find('.alarm_warning_list')[0], 'mouseover', function (event) {
        self.$el.find('.alarm_warning_list').show()
    });

    /**
     * 取得signal_name_html
     */
    this.parkMap.addListener('get_signal_name_html', function (sender, evt) {
        var call_back = evt.getProperty('call_back');
        var html = self.getSignalNameHtml();
        call_back(html)
    })

    /**
     * 设置signal name
     */
    this.parkMap.addListener('set_signal_html', function (sender, evt) {
        var html = evt.getProperty('html');
        self.setSignalNameHtml(html);
    })

    /**
     * 设置counting down
     */
    this.parkMap.addListener('countingDown', function (sender, evt) {
        var html = evt.getProperty('html');
        self.setCountingDownHtml(html);
    })

    /**
     * 添加operation warning
     */
    this.parkMap.addListener('add_warning', function (sender, evt) {
        var msg = evt.getProperty('msg');
        if (self.$('.alarm_warning_list p').length < 1000) {} else {
            self.$('.alarm_warning_list p:last-child').remove()
        }
        var record = `${moment().format("YY-MM-DD HH:mm:ss")}:      ${msg}`
        self.$('.alarm_warning_list').prepend(`<p>${record}</p>`)
        self.$('.warning_container span').html(record)
        self.$('.warning_container').scrollTop(10000)
    })
}