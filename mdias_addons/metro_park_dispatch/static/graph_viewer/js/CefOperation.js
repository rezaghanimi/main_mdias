
CefOperation = function (parkMap, container) {
    mxEventSource.call(this);
};

mxUtils.extend(CefOperation, mxEventSource);

CefOperation.prototype.call_server_method = function (model, method, data) {
    let def = $.Deferred();
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

// cef数据, 发送数据给联锁
CefOperation.prototype.send_interlock_cmd = function (data) {
    if (!window.cefQuery) {
        window.cefQuery = i => { }
    }
    console.log('给联锁发送命令:', data)
    window.cefQuery({
        request: JSON.stringify({
            cmd: "commit_action",
            data: data
        }),
        persistent: false,
    })
}

// 发送数据给子页面
CefOperation.prototype.cef_send_sub = (data) => {
    if (!window.cefQuery) {
        window.cefQuery = function () { }
    }
    window.cefQuery({
        request: JSON.stringify({
            cmd: "page_transfer",
            data: data
        }),
        persistent: false,
    })
}


CefOperation.prototype.cef_send = (data) => {
    var def = $.Deferred();
    if (window.cefQuery) {
        console.log('send cef data,', data)
        window.cefQuery({
            request: JSON.stringify(data),
            persistent: false,
            onSuccess: function (response) {
                console.log(response)
                def.resolve(response)
            },
            onFailure: function (error_code, error_message) {
                console.log(arguments)
                def.reject(error_message)
            }
        })
    } else {
        def.reject('it in not in shell env')
    }
    return def
}

