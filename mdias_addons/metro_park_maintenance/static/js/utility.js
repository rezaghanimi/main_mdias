odoo.define('metro_park_maintenance.utility', function (require) {
    "use strict";

    var core = require('web.core')
    
    /*
    * 获取本地配置
    */
    function get_config(key) {
        var def = $.Deferred();
        if (window.cefQuery) {
            window.cefQuery({
                request: JSON.stringify({
                    cmd: "get_config",
                    key: key
                }),
                persistent: false,
                onSuccess: function (response) {
                    def.resolve(response)
                },
                onFailure: function (error_code, error_message) {
                    def.reject(error_message)
                }
            })
        } else {
            def.reject('it in not in shell env')
        }
        return def
    }

    /*
    * 小屏显示信息接口
    */
    function small_screen_show_msg(msg_type, data) {
        var def = $.Deferred();
        if (window.cefQuery) {
            window.cefQuery({
                request: JSON.stringify({
                    cmd: "small_screen_show_msg",
                    msg_type: msg_type,
                    msg_data: JSON.stringify(data)
                }),
                persistent: false,
                onSuccess: function (response) {
                    def.resolve(response)
                },
                onFailure: function (error_code, error_message) {
                    def.reject(error_message)
                }
            })
        } else {
            def.reject('it in not in shell env')
        }
        return def
    }

    /*
    * 语音接口
    */
    function tts_speak(txt) {
        var def = $.Deferred();
        if (window.cefQuery) {
            window.cefQuery({
                request: JSON.stringify({
                    cmd: "tts_speak",
                    txt: txt
                }),
                persistent: false,
                onSuccess: function (response) {
                    def.resolve(response)
                },
                onFailure: function (error_code, error_message) {
                    def.reject(error_message)
                }
            })
        } else {
            def.reject('it in not in shell env')
        }
        return def
    }

    /**
     * 是否在cef环境中
     */
    function is_in_cef() {
        if (window.cefQuery) {
            return true
        } else {
            return false
        }
    }

    /*
    * 调用本地服务生成轮乘计划, data json字典
    */
    function do_plan_by_local(data) {
        var def = $.Deferred();
        if (window.cefQuery) {
            window.localPlanNotify = function (success, data) {
                if (success) {
                    var rst = JSON.parse(data)
                    def.resolve(rst)
                } else {
                    def.reject()
                }
            }
            window.cefQuery({
                request: JSON.stringify({
                    cmd: "do_plan_by_local",
                    data: JSON.stringify(data)
                }),
                persistent: false,
                onSuccess: function (response) { },
                onFailure: function (error_code, error_message) {
                    def.reject(error_message)
                }
            })
        } else {
            def.reject('it in not in shell env')
        }
        return def
    }

    /**
     * web socket 联接服务器进行计算
     */
    function do_plan_by_websocket(host, data) {
        var def = $.Deferred()

        // 触发loading
        core.bus.trigger('rpc_request');

        try {
            var ws = new WebSocket(host);
            var success = false;
    
            ws.onopen = function () {
                ws.send(JSON.stringify(data));
            };
    
            ws.onmessage = function (evt) {
                var received_msg = evt.data;
                var rst = JSON.parse(received_msg);
    
                success = true
                ws.close();
                
                def.resolve(rst);
            };
    
            ws.onclose = function () {
                core.bus.trigger('rpc_response');
                if (!success) {
                    def.reject('联接计算服务器出错');
                }
            };     
        } catch (error) {
            core.bus.trigger('rpc_response_failed');
            def.reject('连接服务器出错');
        }

        return def
    }

    return {
        get_config: get_config,
        tts_speak: tts_speak,
        small_screen_show_msg: small_screen_show_msg,
        do_plan_by_local: do_plan_by_local,
        is_in_cef: is_in_cef,
        do_plan_by_websocket: do_plan_by_websocket
    }
});
