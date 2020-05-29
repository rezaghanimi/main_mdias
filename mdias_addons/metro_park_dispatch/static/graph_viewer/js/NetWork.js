
NetWork = function (location) {
    mxEventSource.call(this);

    this.socket = undefined
    this.location = location
};

mxUtils.extend(NetWork, mxEventSource);

NetWork.prototype.start = function () {
    var self = this;
    this.get_socketio_server_config().then((config) => {
        config = JSON.parse(config);
        var host = config.host;

        // 连接服务器的时候就加入xing_hao_lou这个room
        this.socket = io(host, {
            'transports': ['websocket'],
            'force new connection': true,
            'query': {
                'room': 'xing_hao_lou'
            }
        });

        this.socket.on('connect', () => {
            console.log('net work connected!')
            self.fireEvent(new mxEventObject('socketio_connected', 'msg', ''));
        });

        this.socket.on('funenc_socketio_server_msg', function (data) {
            var msg = data.data;
            if (msg.location_alias == self.location) {
                if (msg.msg_type == "update_train_position") {
                    self.fireEvent(new mxEventObject(
                        'update_train_position', 'msg_data', msg.msg_data));
                } else if (msg.msg_type == "update_train_group_position") {
                    self.fireEvent(new mxEventObject(
                        'update_train_group_position', 'msg_data', msg.msg_data));
                } else if (msg.msg_type == 'update_busy_icons') {
                    self.fireEvent(new mxEventObject(
                        'update_busy_icons', 'msg_data', msg.msg_data));
                }  
                else {
                    self.fireEvent(new mxEventObject(
                        'funenc_socketio_server_msg', 'msg', msg));
                }
            }
        });
    })
}

NetWork.prototype.call_server_method = function (model, method, data) {
    var def = $.Deferred();
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
}

NetWork.prototype.get_socketio_server_config = function () {
    var def = $.Deferred();
    if (window.cefQuery) {
        // 通过cef读取本地文件配置
        window.cefQuery({
            request: JSON.stringify({
                cmd: "get_socketio_server_config"
            }),
            persistent: false,
            onSuccess: function (config) {
                console.log('network get socket config success!!')
                def.resolve(config)
            },
            onFailure: function (error_code, error_message) {
                def.reject('获取地址错误，请检查!')
            }
        });
    } else {
        // 各自在这个地方添加各自的配置
        var coder = urlParams['coder'] || 'crax'
        switch (coder) {
            case 'crax':
                def.resolve(JSON.stringify({
                    "host": "127.0.0.1:9080"
                }))
                break
        }
    }

    return def
}
