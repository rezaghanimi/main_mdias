/**
 * 站场图
 */
odoo.define('funenc.metro_park.maintenance_park_map', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractAction = require('web.AbstractAction');
    var MaintenanceParkMap = AbstractAction.extend({
        /**
         * 初始化
         * @param {} parent
         * @param {*} action
         */
        init: function (parent, action) {
            this.vue = new Vue({});
            this._super.apply(this, arguments);
            this.graph = {};
            this.map = undefined;
            this.map_info = undefined;
            this.zabbix_judge = true;
        },

        /**
         * 渲染结束，组件初始化
         */
        willStart: function () {
            var self = this
            var def = $.Deferred();

            // Adds required resources (disables loading of fallback properties, this can only
            // be used if we know that all keys are defined in the language specific file)
            mxResources.loadDefaultBundle = false;
            var bundle = mxResources.getDefaultBundle(RESOURCE_BASE, mxLanguage)
                || mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);
            mxUtils.getAll([bundle, STYLE_PATH + '/default.xml'], function (xhr) {
                var bundle_cache = {
                    valid: false,
                    part0: undefined,
                    part1: undefined
                }

                // Adds bundle text to resources
                bundle_cache.part0 = xhr[0].getText()
                bundle_cache.part1 = xhr[1].getDocumentElement();
                bundle_cache.valid = true

                mxResources.parse(bundle_cache.part0);

                // Configures the default graph theme
                self.themes = new Object();
                self.themes[Graph.prototype.defaultThemeName] = bundle_cache.part1;

                def.resolve()
            }, function () {
                def.reject()
            })

            var map_data = self._rpc({
                model: 'maintenance_management.maintenance_management',
                method: 'get_map_info',
            }).then(function (res) {
                if (res && res instanceof Array) {
                    self.map_info = res[0]
                }
            })
            return def, map_data;
        },

        deal_zabbix: function (notifications) {
            var self = this;
            var hxj_icon = ['hxjh_m', 'hxjh_s']
            var jrj_icon = ['jrjh_m', 'jrjh_s', 'jrzj2_m', 'jrzj2_s', 'tpy_jrjh_m',
                'tpy_jrjh_s', 'gdl_jrjh_m', 'gdl_jrjh_s', 'gdl_jrjh_s_1', 'gdl_jrjh_m_1']
            var ser_icon = ['CI_s', 'CI_m', 'PSCADA_m', 'TCMS_m', 'PMS_m', 'sg_m',
                'mdyy_m', 'mdyy_s', 'mdsj_m', 'mdsj_s', 'mdjl_m', 'mdjl_s', 'mdjl_m_1',
                'mdjl_s_1', 'ctqzd', 'tpy_ctqzd', 'gdl_ci_s', 'gdl_ci_m',
                'PSCADA_m', 'gdl_ctqzd']
            var gzz_icon = ['whgz_m', 'jxdd', 'ccjx', 'ccdd', 'xhycz', 'zbycz', 'pbgzz', 'tpy_ctqzd',
                'tpy_pbgzz', 'gdl_jxdd', 'gdl_ccjx', 'gdl_ccdd', 'gdl_xhycz', 'gdl_zbycz', 'gdl_pbgzz']
            var qzj_icon = ['mdtxqzj_s', 'mdtxqzj_m', 'gdl_qzj_m', 'gdl_qzj_s',]
            try {
                _.each(notifications[0][1].zabbix_warning_data, function (notification) {
                    var message = notification.name;
                    var value = notification.msg;
                    var zbx = notification.zbx
                    var warning_image = ''
                    for (var i in self.graph.model.cells) {
                        if (self.graph.model.cells[i].getAttribute('act_button') == zbx) {
                            if (hxj_icon.indexOf(zbx) > -1) {
                                warning_image = 'Concentrator_128x128.svg'
                            } else if (jrj_icon.indexOf(zbx) > -1) {
                                warning_image = 'access_switch.svg'
                            } else if (ser_icon.indexOf(zbx) > -1) {
                                warning_image = 'Workstation_128x128.svg'
                            } else if (gzz_icon.indexOf(zbx)) {
                                warning_image = 'Monitor_Tower_128x128.svg'
                            } else if (qzj_icon.indexOf(zbx)) {
                                warning_image = 'Monitor_Tower_128x128.svg'
                            }
                            self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                            ))
                            self.graph.refresh()
                        }
                    }
                    if (message) {
                        // 彈出提示
                        if (self.zabbix_judge) {
                            self.vue.$message({
                                dangerouslyUseHTMLString: true,
                                offset: 500,
                                duration: 3000,
                                center: true,
                                showClose: true,
                                customClass: '一级报警',
                                message: '<div style="text-align: center;color: red">服务器</div>\n' +
                                    '<div style="text-align:center;margin-top: 10px;color: red">故障设备：' + message + '</div>' +
                                    '<div style="text-align:center;margin-top: 10px;color: red">故障信息：' + value + '</div>'
                            });
                        }
                    }
                });
            } catch (e) {
                console.log(e)
            }
        },

        deal_battery: function (notification) {
            var self = this;
            try {
                _.each(notification[0][1].err_info, function (notification) {
                    var message = notification.name;
                    var value = notification.value;
                    if (message) {
                        // 彈出提示
                        if (self.zabbix_judge) {
                            self.vue.$message({
                                    dangerouslyUseHTMLString: true,
                                    offset: 500,
                                    duration: 3000,
                                    center: true,
                                    showClose: true,
                                    customClass: '一级报警',
                                    message: '<div style="text-align: center;color: red">电源报警</div>\n' +
                                        '<div style="text-align:center;margin-top: 10px;color: red">故障信息：' + message + '</div>' +
                                        '<div style="text-align:center;margin-top: 10px;color: red">警告值：' + value + '</div>'
                                }
                            );
                        }
                    }
                });
            } catch (e) {
                console.log(e)
            }
        },

        start: function () {
            var self = this
            self.on_bus('battery_err_data', function (data, call) {
                self.deal_battery(data.message)
            });

            self.on_bus('connect_waring_prompt', function (data, call) {
                self.connect_waring_prompt(data)
            });

            self.on_bus('zabbix_warning_data', function (data, call) {
                self.deal_zabbix(data.message)
            });

            // 用来刷新页面的状态
            self.on_bus('equipment_state_page_refresh', function (data, call) {
                self.init_connect_state()
            });

            if (self.map_info) {
                self.reload_map(Base64.decode(self.map_info.name))
                setTimeout(function () {
                    try {
                        self.graph.addMouseListener({
                            mouseDown: function (sender, evt) {
                                sender.background = '#FFFFFF'
                                try {
                                    var act_button = evt.sourceState.cell.getAttribute('act_button');
                                    var get_switch_data = ['hxjh_m', 'hxjh_s', 'gdl_jrjh_s_1', 'gdl_jrjh_s', 'jrjh_m', 'jrjh_s',
                                        'gdl_jrjh_m_1', 'tpy_jrjh_s', 'tpy_jrjh_m',
                                        'jrzj2_s', 'jrzj2_m', 'gdl_jrjh_m']
                                    var interface_state = ['CI_m', 'CI_s', 'PSCADA_m', 'PSCADA_s',
                                        'sg_s', 'gdl_ci_s', 'ATS_m', 'ATS_s', 'gdl_ci_m',
                                        'gdl_pscada_m', 'gdl_pscada_s',]
                                    var server_client = ['jxdd', 'ccjx', 'ccdd', 'xhycz', 'zbycz',
                                        'mdyy_m', 'mdyy_s', 'mdsj_m', 'mdsj_s', 'mdjl_m', 'mdjl_s',
                                        'mdjl_m_1', 'mdjl_s_1', 'mdtxqzj_m', 'mdtxqzj_s', 'whgz_m',
                                        'gdl_qzj_m', 'gdl_qzj_s', 'gdl_jxdd', 'gdl_ccjx', 'gdl_ccdd',
                                        'gdl_xhycz', 'gdl_zbycz', 'gdl_ctqzd', 'gdl_pbgzz', 'tpy_pbgzz',
                                        'pbgzz', 'ctqzd', 'tpy_ctqzd',]
                                    var battery = ['tpy_ups', 'ups_m', 'gdl_ups']

                                    if (get_switch_data.indexOf(act_button) > -1) {
                                        self.page_operation_record(act_button)
                                        self.deal_get_switch_data(act_button)
                                    } else if (interface_state.indexOf(act_button) > -1) {
                                        self.page_operation_record(act_button)
                                        self.deal_interface_state(act_button)

                                    } else if (server_client.indexOf(act_button) > -1) {
                                        self.page_operation_record(act_button)
                                        self.deal_work_client(act_button)
                                    } else if (battery.indexOf(act_button) > -1) {
                                        self.page_operation_record(act_button)
                                        self.deal_battery_status(act_button)
                                    }
                                } catch (e) {
                                    console.log(e)
                                }
                            },
                            mouseMove: function (e, e1) {
                                e.background = '#FFFFFF'
                            },
                            mouseUp: function (e, e1) {
                                e.background = '#FFFFFF'
                            }
                        })
                    } catch (e) {
                        console.log(e)
                    }
                }, 150)
                self.init_connect_state()
            }
        },

        reload_map: function (map_data) {
            this.editorUI = new EditorUi(new Editor(false, this.themes), this.$el[0]);
            this.graph = this.editorUI.editor.graph
            if (map_data) {
                var doc = $.parseXML(map_data);
                // 保存data
                this.graph.importGraphModel(doc.documentElement)
                this.graph.setCellsSelectable(false)
                this.graph.setCellsMovable(false)
                this.graph.setCellsEditable(false)
                this.graph.center(-0.00001,0.02,-0.00001,0.02);
            }
        },

        init_connect_state: function () {
            var self = this;
            try {
                self.graph.addMouseListener({
                    mouseDown: function (sender, evt) {
                        sender.background = '#FFFFFF'
                        try {
                            var act_button = evt.sourceState.cell.getAttribute('act_button');
                            var get_switch_data = ['hxjh_m', 'hxjh_s', 'gdl_jrjh_s_1', 'gdl_jrjh_s', 'jrjh_m', 'jrjh_s',
                                'gdl_jrjh_m_1', 'tpy_jrjh_s', 'tpy_jrjh_m',
                                'jrzj2_s', 'jrzj2_m', 'gdl_jrjh_m']
                            var interface_state = ['CI_m', 'CI_s', 'PSCADA_m', 'PSCADA_s',
                                'sg_s', 'gdl_ci_s', 'ATS_m', 'ATS_s', 'gdl_ci_m',
                                'gdl_pscada_m', 'gdl_pscada_s',]
                            var work_client = ['jxdd', 'ccjx', 'ccdd', 'xhycz', 'zbycz',
                                'mdyy_m', 'mdyy_s', 'mdsj_m', 'mdsj_s', 'mdjl_m', 'mdjl_s',
                                'mdjl_m_1', 'mdjl_s_1', 'mdtxqzj_m', 'mdtxqzj_s', 'whgz_m',
                                'gdl_qzj_m', 'gdl_qzj_s', 'gdl_jxdd', 'gdl_ccjx', 'gdl_ccdd',
                                'gdl_xhycz', 'gdl_zbycz', 'gdl_ctqzd', 'gdl_pbgzz', 'tpy_pbgzz',
                                'pbgzz', 'ctqzd', 'tpy_ctqzd',]
                            var battery = ['tpy_ups', 'ups_m', 'gdl_ups']

                            if (get_switch_data.indexOf(act_button) > -1) {
                                self.page_operation_record(act_button)
                                self.deal_get_switch_data(act_button)
                            } else if (interface_state.indexOf(act_button) > -1) {
                                self.page_operation_record(act_button)
                                self.deal_interface_state(act_button)

                            } else if (work_client.indexOf(act_button) > -1) {
                                self.page_operation_record(act_button)
                                self.deal_work_client(act_button)
                            } else if (battery.indexOf(act_button) > -1) {
                                self.page_operation_record(act_button)
                                self.deal_battery_status(act_button)
                            }
                        } catch (e) {
                            console.log(e)
                        }
                    },
                    mouseMove: function (e, e1) {
                        e.background = '#FFFFFF'
                    },
                    mouseUp: function (e, e1) {
                        e.background = '#FFFFFF'
                    }
                })
            } catch (e) {
                console.log(e)
            }
            self._rpc({
                model: 'maintenance_management.equipment_state',
                method: 'according_maintenance_connect_state',
            }).then(function (res) {
                var jr_switch_data = ['gdl_jrjh_s_1', 'gdl_jrjh_s', 'jrjh_m', 'jrjh_s',
                    'gdl_jrjh_m_1', 'tpy_jrjh_s', 'tpy_jrjh_m',
                    'jrzj2_s', 'jrzj2_m', 'gdl_jrjh_m']
                var hx_switch_data = ['hxjh_m', 'hxjh_s',]
                var interface_state = ['CI_m', 'CI_s', 'PSCADA_m', 'PSCADA_s',
                    'sg_s', 'gdl_ci_s', 'ATS_m', 'ATS_s', 'gdl_ci_m',
                    'gdl_pscada_m', 'gdl_pscada_s',]
                var work_client = ['jxdd', 'ccjx', 'ccdd', 'xhycz', 'zbycz',
                    'mdyy_m', 'mdyy_s', 'mdsj_m', 'mdsj_s', 'mdjl_m', 'mdjl_s',
                    'mdjl_m_1', 'mdjl_s_1', 'mdtxqzj_m', 'mdtxqzj_s', 'whgz_m',
                    'gdl_qzj_m', 'gdl_qzj_s', 'gdl_jxdd', 'gdl_ccjx', 'gdl_ccdd',
                    'gdl_xhycz', 'gdl_zbycz', 'gdl_ctqzd', 'gdl_pbgzz', 'tpy_pbgzz',
                    'pbgzz', 'ctqzd', 'tpy_ctqzd',]
                var battery = ['tpy_ups', 'ups_m', 'gdl_ups',
                    'mdyy_m', 'mdyy_s', 'mdsj_m', 'mdsj_s', 'mdjl_m', 'mdjl_s',
                    'mdjl_m_1', 'mdjl_s_1', 'mdtxqzj_m', 'mdtxqzj_s'
                ]
                var warning_image = ''
                _.each(res, function (data) {
                    if (data.state == 'disconnect') {
                        for (var i in self.graph.model.cells) {
                            if (self.graph.model.cells[i].getAttribute('act_button') == data.name) {
                                if (battery.indexOf(data.name) > -1) {
                                    warning_image = 'UPS_128x128.svg'
                                    self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                        "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                                    ))
                                } else if (work_client.indexOf(data.name) > -1) {
                                    warning_image = 'Monitor_Tower_128x128.svg'
                                    self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                        "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                                    ))
                                } else if (interface_state.indexOf(data.name) > -1) {
                                    warning_image = 'Workstation_128x128.svg'
                                    self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                        "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                                    ))

                                } else if (jr_switch_data.indexOf(data.name) > -1) {
                                    warning_image = 'access_switch.svg'
                                    self.graph.model.cells[i].setStyle(graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                        "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                                    ))

                                } else if (hx_switch_data.indexOf(data.name) > -1) {
                                    warning_image = 'Concentrator_128x128.svg'
                                    self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(self.graph.model.cells[i].style,
                                        "image;html=1;image=/maintenance_management/static/img/lib/clip_art/warning_image/" + warning_image + ";strokeColor=#000000;fillColor=#F2F2F2;gradientColor=none;fontSize=18;fontColor=#006633;fontStyle=1;labelBackgroundColor=none;verticalAlign=top;"
                                    ))
                                }
                            } else if (self.graph.model.cells[i].getAttribute('line') == data.line) {
                                self.graph.model.cells[i].setStyle(self.graph.model.cells[i].style.replace(/strokeColor.*?;/,
                                    'strokeColor=red;'))
                            }
                        }
                    }
                })
                self.graph.refresh()
            })
        },

        connect_waring_prompt: function (data) {
            var self = this;
            if (self.zabbix_judge) {
                self.vue.$message({
                    dangerouslyUseHTMLString: true,
                    offset: 500,
                    duration: 3000,
                    center: true,
                    showClose: true,
                    customClass: '一级报警',
                    message: '<div style="text-align:center;margin-top: 10px;color: red">故障设备：' + data.data + '</div>' +
                        '<div style="text-align:center;margin-top: 10px;color: red">故障信息：' + '连接断开' + '</div>'
                });
            }
        },

        page_operation_record: function (data) {
            var self = this;
            self._rpc({
                model: 'maintenance_management.page_operation_record',
                method: 'create_data',
                args: [data],
            })
        },

        deal_get_switch_data: function (data) {
            var self = this;
            self.do_action({
                "name": "交换机数据",
                "type": "ir.actions.client",
                "tag": 'light_module_data',
                "send_data": data,
            })
        },

        deal_interface_state: function (data) {
            var self = this
            self.do_action({
                "name": "接口状态",
                "type": "ir.actions.client",
                "tag": 'interface_state',
                "send_data": data,
            })
        },

        deal_work_client: function (data) {
            var self = this;
            self.do_action({
                "name": "服务器状态",
                "type": "ir.actions.client",
                "tag": 'server_client',
                "params_data": data,
            })
        },

        deal_battery_status: function (data) {
            var self = this;
            self.do_action({
                "name": "电源状态",
                "type": "ir.actions.client",
                "tag": 'battery_status',
                "parameter": data,
            })
        },

        destroy: function () {
            this._super.apply(this, arguments)
            this.zabbix_judge = false
            if (this.editorUI) {
                this.editorUI.destroy();
            }
        }
    });

    core.action_registry.add('MaintenanceParkMap', MaintenanceParkMap);

    return MaintenanceParkMap;
});
