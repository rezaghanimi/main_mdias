layui.define([], function (exports) {
    const API_LIST = {
        //司机信息
        driver: {
            //查询所有司机信息
            listAll: {
                type: "post",
                url: "/api/admin/driver/list-all"
            },
            //添加司机信息
            save: {
                type: 'post',
                url: '/api/admin/driver'
            },
            //修改司机信息
            update: {
                type: 'put',
                url: '/api/admin/driver'
            },
            //删除司机信息
            delete: {
                type: 'delete',
                url: '/api/admin/driver'
            },
            //删除司机信息
            findAll: {
                type: 'get',
                url: '/api/admin/driver/list'
            },
            downloadDriverTemplate: {
                type: 'get',
                url: '/api/admin/driver/template/download'
            },
            uploadDriverTemplate: {
                type: 'post',
                url: '/api/admin/driver/template/upload'
            }
        },
        //时刻表管理
        train_schedule: {
            //上传时刻表
            upload: {
                type: 'post',
                url: '/api/admin/train-schedule/upload'
            },
            //查询所有时刻表上传记录
            list_table: {
                type: 'get',
                url: '/api/admin/train-schedule/list-all-train-schedule-table'
            },
            //查询所有时刻表上传记录
            list_all_table: {
                type: 'get',
                url: '/api/admin/train-schedule/list-all'
            },
            delete: {
                type: 'delete',
                url: '/api/admin/train-schedule/table'
            },
            //查询时刻表对应列车信息
            list_schedule: {
                type: 'post',
                url: '/api/admin/train-schedule/list-all-train-schedule'
            },
            list_all_station: {
                type: 'get',
                url: '/api/admin/train-schedule/list-all-station'
            },
            list_all_route: {
                type: 'get',
                url: '/api/admin/train-schedule/list-all-route'
            }
        },
        accident_card: {
            //查询所有司机信息
            listAll: {
                type: "post",
                url: "/api/admin/accident-card/list-all"
            },
            //添加司机信息
            save: {
                type: 'post',
                url: '/api/admin/accident-card'
            },
            //修改司机信息
            update: {
                type: 'put',
                url: '/api/admin/accident-card'
            },
            //删除司机信息
            delete: {
                type: 'delete',
                url: '/api/admin/accident-card'
            }
        },
        //司机位置图编制
        driver_position: {
            ga: {
                type: 'get',
                url: '/api/admin/driver-position/ga'
            },
            save: {
                type: 'post',
                url: '/api/admin/driver-position/save'
            },
            findDriverPositionPage: {
                type: 'post',
                url: '/api/admin/driver-position/position-page'
            },
            findDriverPositionById: {
                type: 'get',
                url: '/api/admin/driver-position'
            },
            findAllDriverPosition: {
                type: 'get',
                url: '/api/admin/driver-position'
            },
            exportDriverPositionToExcel: {
                type: 'get',
                url: '/api/admin/driver-position/export'
            },
            uploadDriverPositionExcel: {
                type: 'post',
                url: '/api/admin/driver-position/import'
            },
            analysisDriverPosition: {
                type: "get",
                url: "/api/admin/driver-position/analysis"
            },
            deleteDriverPositionById: {
                type: 'delete',
                url: '/api/admin/driver-position'
            },
        },
        //规则
        rule: {
            saveNormalRule: {
                type: 'post',
                url: '/api/admin/rule/normal'
            },
            saveExtraRule: {
                type: 'post',
                url: '/api/admin/rule/extra'
            },
            findNormalRulePage: {
                type: 'post',
                url: '/api/admin/rule/normal-page'
            },
            findExtraRulePage: {
                type: 'post',
                url: '/api/admin/rule/extra-page'
            },
            findByRuleId: {
                type: 'get',
                url: '/api/admin/rule'
            },
            deleteByRuleId: {
                type: 'delete',
                url: '/api/admin/rule'
            },
            updateNormalRule: {
                type: 'put',
                url: '/api/admin/rule/normal'
            },
            findAllNormalRules: {
                type: 'get',
                url: '/api/admin/rule/normals'
            },
            findAllExtraRules: {
                type: 'get',
                url: '/api/admin/rule/extras'
            }
        },
        //schedule派班计划表
        schedule: {
            saveSchedule: {
                type: 'post',
                url: '/api/admin/schedule-table/save'
            },
            createSchedule: {
                type: 'post',
                url: '/api/admin/schedule-table/create'
            },
            updateSchedule: {
                type: 'put',
                url: '/api/admin/schedule-table/update'
            },
            //分页查询
            findScheduleTablePageable: {
                type: 'post',
                url: '/api/admin/schedule-table/list-all'
            },
            getAllNoDistributeTables: {
                type: 'get',
                url: '/api/admin/schedule-table/get-no-distribute-schedule'
            },
            findScheduleTableDetailById: {
                type: 'get',
                url: '/api/admin/schedule-table'
            },
            findLatestSchedules: {
                type: "get",
                url: "/api/admin/schedule-table/find-latest"
            },
            deleteById: {
                type: 'delete',
                url: '/api/admin/schedule-table'
            },
            exportScheduleTable: {
                type: 'get',
                url: '/api/admin/schedule-table/export'
            }
        },
        //schedule下发派班计划表
        schedule_distribute: {
            distribute: {
                type: 'post',
                url: '/api/admin/schedule-table-feedback/distribute'
            },
            findPage: {
                type: 'post',
                url: '/api/admin/schedule-table-feedback/list-all'
            },
            feedback: {
                type: 'get',
                url: '/api/admin/schedule-table-feedback/driver-feedback'
            },
            deleteDistribute: {
                type: 'delete',
                url: '/api/admin/schedule-table-feedback'
            },
            urgentDistribute: {
                type: 'get',
                url: '/api/admin/schedule-table-feedback/urgent'
            }
        },
        screenDisplay: {
            saveScreenDisplay: {
                type: 'post',
                url: '/api/admin/screen-display'
            },
            updateScreenDisplay: {
                type: 'put',
                url: '/api/admin/screen-display'
            },
            deleteScreenDisplay: {
                type: 'delete',
                url: '/api/admin/screen-display'
            },
            findScreenDisplayPage: {
                type: 'post',
                url: '/api/admin/screen-display/list-all'
            }
        },
        driverPunchCard: {
            findPunchRecordPage: {
                type: 'post',
                url: '/api/admin/driver-punch-card/list-all'
            },
            replacePunchCard: {
                type: 'post',
                url: '/api/admin/driver-punch-card/replace-punch-card'
            }
        },
        mileage: {
            //查询所有交路信息
            listAll: {
                type: "post",
                url: "/api/admin/crossing/list-all"
            },
            //添加交路信息
            save: {
                type: 'post',
                url: '/api/admin/crossing'
            },
            //修改交路信息
            update: {
                type: 'put',
                url: '/api/admin/crossing'
            },
            //删除交路信息
            delete: {
                type: 'delete',
                url: '/api/admin/crossing'
            },
        },
        scheduleDriver: {
            findAllDriverMileage: {
                type: 'post',
                url: '/api/admin/schedule-driver/list-all'
            }
        },
        base_url: 'http://localhost:9027',      //本地开发地址
        // base_url: 'http://172.21.0.3:9027', //现场地址
        // base_url: 'http://cs2.huiztech.cn:9027' //服务器地址
    };
    //输出test接口
    exports('api', API_LIST);
});
