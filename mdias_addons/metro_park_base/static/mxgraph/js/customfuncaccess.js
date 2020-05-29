/**
 * 
 * graph初始化后，开始注册自定义的一些方法，通过这些方法控制graph中的cell原件的展示属性。
 * 
 * 
 */


class graphx {


    constructor() {
        this.graph = window.graph
    }

    //通过id获取cell
    getEquip(uid) {
        return window.parkequip[uid]
    }







    setTurnoutStatus(uid, status) {
        let cell = this.getEquip(uid)
        if (!cell) return
        cell.equipstatus = status
        //获取零件
        let roadentrance = cell.getSubCell('road-entrance'),
            roaddirect = cell.getSubCell('road-direct'),
            roadreverse = cell.getSubCell('road-reverse'),
            reverse = cell.getSubCell('reverse'),
            direct = cell.getSubCell('direct'),
            namelabel = cell.getSubCell('label'),
            boundary = cell.getSubCell('boundary')

        /**
         * 
         * 初始化所有零件
         * 
         */

        //重置显示颜色
        let allparts = [reverse, direct, roadreverse, roaddirect, roadentrance]
        allparts.map(a => {
            a.map(i => window.graph.model.setVisible(i, 1) + this.setFillColor(i, '#5578b6'))
        })


        //重置lable颜色
        namelabel.map(i => this.setLabelText(i, `<div style="background:none;color:#fff;">${uid}</div>`))



        //隐藏边框
        if (boundary.length) {
            boundary.map(i => {
                window.graph.model.setVisible(i, 0)
            })
        }
        let ay = [reverse, direct]
        ay.map(ip => {
            ip.map(i => {
                window.globalintervalcell.delete(i)
                this.showcell(1)
            })
        })

        /**
         * 
         * 开始设置零件样式
         * 
         */


        if (status.switch_crowded) {
            // 挤岔
            if (!window[`turnoutalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `道岔${uid}#挤岔`
                })
                window[`turnoutalarmtag${uid}`] = 1
            }


            let a = [reverse, direct]
            a.map(ip => {
                ip.map(i => {
                    this.setFillColor(i, '#f00')
                    window.graph.model.setVisible(i, 1)
                    window.globalintervalcell.add(i)
                })
            })
            namelabel.map(i => this.setLabelText(i, `<div style="color:#f00;">${uid}</div>`))
            return
        } else {
            if (window[`turnoutalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `道岔${uid}#挤岔恢复`
                })
                window[`turnoutalarmtag${uid}`] = 0
            }
        }


        //绿色稳定显示：表示道岔此时处于定位位置；
        if (status.pos) {
            direct.map(i => {
                if (window.turnouttogglekey == 0) {
                    this.setFillColor(i, '#0f0')
                }
            })
            namelabel.map(i => this.setLabelText(i, `<div style="color:#0f0;">${uid}</div>`))
        } else {
            direct.map(i => {
                window.graph.model.setVisible(i, 0)
            })
        }

        //黄色稳定显示：表示道岔此时处于反位位置；
        if (status.pos_reverse) {
            reverse.map(i => {
                if (window.turnouttogglekey == 0) {
                    this.setFillColor(i, '#ff0')
                }
            })
            namelabel.map(i => this.setLabelText(i, `<div style="color:#ff0;">${uid}</div>`))
        } else {
            reverse.map(i => {
                window.graph.model.setVisible(i, 0)
            })
        }





        //白色光带：道岔所在的轨道区段处于空闲锁闭状态
        if (status.hold == 0 && status.lock == 1) {
            let a = [roadentrance]

            if (status.pos == 1 && status.pos_reverse == 0) {
                a.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                a.push(roadreverse, reverse)
            }

            a.map(ip => {
                ip.map(i => {
                    this.setFillColor(i, '#fff')
                })
            })
        }

        //红色光带：道岔所在的轨道区段处于占用或轨道电路故障；
        if (status.hold == 1) {
            let a = [roadentrance]

            if (status.pos == 1 && status.pos_reverse == 0) {
                a.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                a.push(roadreverse, reverse)
            }

            a.map(ip => {
                ip.map(i => {
                    this.setFillColor(i, '#f00')
                })
            })
        }

        if (status.closed) {
            namelabel.map(i => this.setLabelText(i, '<div style="border:1px solid #f00">' + i.getAttribute('label') + '</div>'))
        }

        if (status.lock_s || status.lock_protect || status.lock_gt) {
            boundary.map(i => {
                window.graph.model.setVisible(i, 1)
            })
        }



        if (status.notice != 0) {

            switch (status.notice) {
                case 1:
                    alarmwarninglistadd(uid + '单锁不能动')
                    break
                case 2:
                    alarmwarninglistadd(uid + '锁闭不能动')
                    break
                case 15:
                    alarmwarninglistadd(uid + '区段道岔有封闭')
                    break
                case 16:
                    alarmwarninglistadd(uid + '注意超限不满足')
                    break
                case 17:
                    alarmwarninglistadd(uid + '校核错')
                    break
                case 18:
                    alarmwarninglistadd(uid + '有车移动')
                    break
                case 19:
                    alarmwarninglistadd(uid + '不能正常解锁')
                    break
                case 20:
                    alarmwarninglistadd(uid + '紧急关闭')
                    break
                case 21:
                    alarmwarninglistadd(uid + '没锁闭')
                    break
                case 22:
                    alarmwarninglistadd(uid + '要求防护道岔不到位')
                    break
                case 23:
                    alarmwarninglistadd(uid + '不在要求位置')
                    break
                case 24:
                    alarmwarninglistadd(uid + '要求防护道岔不能动')
                    break
                case 25:
                    alarmwarninglistadd(uid + '超限不满足')
                    break
                case 26:
                    alarmwarninglistadd(uid + '不能动')
                    break
                case 27:
                    alarmwarninglistadd(uid + '封闭')
                    break
                case 28:
                    alarmwarninglistadd(uid + '锁闭')
                    break
                case 29:
                    alarmwarninglistadd(uid + '在进路中')
                    break
                case 30:
                    alarmwarninglistadd(uid + '有车占用')
                    break
                case 31:
                    alarmwarninglistadd(uid + 'SFJ失效')
                    break
            }
        }





    }


    setSectorStatus(uid, status) {
        let cell = this.getEquip(uid)
        if (!cell) return
        cell.equipstatus = status
        //获取零件
        let road = cell.getSubCell('road'),
            namelabel = cell.getSubCell('label')

        /**
         * 
         * 初始化所有零件
         * 
         */

        uid = uid.replace('_', '/')

        //重置显示颜色
        let allparts = [road]
        allparts.map(a => {
            //空闲蓝色
            a.map(i => window.graph.model.setVisible(i, 1) + this.setFillColor(i, '#5578b6'))
        })
        //重置lable颜色
        namelabel.map(i => this.setLabelText(i, `<div style="background:none;color:#fff;">${uid}</div>`))


        /**
         * 
         * 开始设置零件样式
         * 
         * 
         * 
         */


        //白色光带：道岔所在的轨道区段处于空闲锁闭状态
        if (status.hold == 0 && status.lock == 1) {
            road.map(i => {
                this.setFillColor(i, '#fff')
            })
        }


        //红色光带：表示区段为占用状态或区段轨道电路故障；
        if (status.hold == 1) {
            road.map(i => {
                this.setFillColor(i, '#f00')
            })
        }

        //在原有区段状态上下增加粉红色线框的光带：表示区段被人工设置为轨道分路不良标记。
        if (status.badness == 1) {
            road.map(i => {
                this.setStrokeColor(i, '#ff9393')
            })
        }




        if (status.notice != 0) {

            switch (status.notice) {
                case 22:
                    alarmwarninglistadd(uid + '照查不满足')
                    break
                case 23:
                    alarmwarninglistadd(uid + '机务段不同意')
                    break
                case 24:
                    alarmwarninglistadd(uid + '事故无驱吸起')
                    break
                case 25:
                    alarmwarninglistadd(uid + '照查错误')
                    break
                case 26:
                    alarmwarninglistadd(uid + '开通条件不满足')
                    break
                case 27:
                    alarmwarninglistadd(uid + '在进路中')
                    break
                case 28:
                    alarmwarninglistadd(uid + '不能正常解锁')
                    break
                case 29:
                    alarmwarninglistadd(uid + '占用')
                    break
                case 30:
                    alarmwarninglistadd(uid + '照查敌对')
                    break
                case 31:
                    alarmwarninglistadd(uid + '较核错')
                    break
            }
        }



    }

    setLightStatus(uid, status) {




        //不在graph上的dom控制，位于下方的按钮
        if (uid == bottombutton.name + 'BTN') {
            if (status.light) {
                $('#parkbottombtn1').css({
                    background: "#ffff57"
                })
            } else {
                $('body').trigger('click')
                $('#parkbottombtn1').attr('style', '')
            }

            return
        }


        // BYTE light : 1;               // 亮灯
        // BYTE flash : 1;               // 闪灯
        // BYTE red : 1;                 // 红灯
        // BYTE yellow : 1;              // 黄灯
        // BYTE green : 1;               // 绿灯
        // BYTE blue : 1;                // 蓝灯
        // BYTE white : 1;               // 白灯
        // BYTE yellow2 : 1;             // 黄灯



        let cell = this.getEquip(uid)
        if (!cell) return
        cell.equipstatus = status




        //根据不同种类信号机初始化
        if (cell.getAttribute('type')) {

            if (cell.getAttribute('type') == 'lightflash') {
                let light = cell.getSubCell('light')
                let lighto
                if (light && light.length > 0) {
                    lighto = light[0]
                } else {
                    lighto = cell
                }
                window.globalintervalcell.delete(lighto)
                this.showcell(lighto)
                this.setFillColor(lighto, '#000')
                if (status.light) {
                    this.setFillColor(lighto, '#f00')
                    window.globalintervalcell.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightyellow') {
                let light = cell.getSubCell('light')
                let lighto
                if (light && light.length > 0) {
                    lighto = light[0]
                } else {
                    lighto = cell
                }
                window.globalintervalcell.delete(lighto)
                this.showcell(lighto)
                this.setFillColor(lighto, '#000')
                if (status.light) {
                    this.setFillColor(lighto, '#ff0')
                }
                if (status.flash) {
                    window.globalintervalcell.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'BTN') {
                let light = cell.getSubCell('light')
                let lighto
                if (light && light.length > 0) {
                    lighto = light[0]
                } else {
                    lighto = cell
                }
                window.globalintervalcell.delete(lighto)
                this.showcell(lighto)
                this.setFillColor(lighto, '#B3B3B3')
                if (status.light) {
                    this.setFillColor(lighto, '#ff0')
                }
                if (status.flash) {
                    window.globalintervalcell.add(lighto)
                }
                return
            }

            if (cell.getAttribute('type') == 'lightgreen') {
                let light = cell.getSubCell('light')
                let lighto
                if (light && light.length > 0) {
                    lighto = light[0]
                } else {
                    lighto = cell
                }
                window.globalintervalcell.delete(lighto)
                this.showcell(lighto)
                this.setFillColor(lighto, '#000')
                if (status.light) {
                    this.setFillColor(lighto, '#0f0')
                }
                if (status.flash) {
                    window.globalintervalcell.add(lighto)
                }
                return
            }

            return
        }




        //获取零件
        let light = cell.getSubCell('light')
        let light1, light2
        if (light && light.length && light.length > 1) {
            light1 = light.find(i => i.getAttribute('type') == 'da')
            light2 = light.find(i => i.getAttribute('type') != 'da')
        }
        //初始化
        if (light1 && light2) {
            this.setFillColor(light1, '#000')
            this.setFillColor(light2, '#000')
        }

        let lighto
        if (light && light.length > 0) {
            lighto = light[0]
        } else {
            lighto = cell
        }
        window.globalintervalcell.delete(lighto)
        this.showcell(lighto)

        this.setFillColor(lighto, '#000')

        if (status.light == 0 && status.flash == 0 && status.red == 0 && status.yellow == 0 && status.green == 0 && status.blue == 0 && status.white == 0 && status.yellow2 == 0) {
            if (light1 && light2) {
                this.setFillColor(light1, '#f00')
                this.setFillColor(light2, '#000')
            }
        }

        if (status.light) {
            this.setFillColor(lighto, '#f00')
        }
        if (status.yellow2) {
            this.setFillColor(lighto, '#ff0')
        }
        if (status.white) {
            this.setFillColor(lighto, '#fff')
        }
        if (status.blue) {
            this.setFillColor(lighto, '#00f')
        }
        if (status.green) {
            this.setFillColor(lighto, '#0f0')
        }
        if (status.yellow) {
            this.setFillColor(lighto, '#ff0')
        }
        if (status.red) {
            this.setFillColor(lighto, '#f00')
            if (light1 && light2) {
                this.setFillColor(light1, '#f00')
                this.setFillColor(light2, '#ff0')
            }
        }
        if (status.flash) {
            window.globalintervalcell.add(lighto)
        }


    }

    setSignalStatus(uid, status) {
        let cell = this.getEquip(uid)
        if (!cell) return
        cell.equipstatus = status
        //获取零件
        let light = cell.getSubCell('light'),
            button = cell.getSubCell('button'),
            namelabel = cell.getSubCell('label'),
            boundary = cell.getSubCell('boundary')
        boundary = boundary.concat(cell.getSubCell('fork'))

        /**
         * 
         * 初始化所有零件
         * 
         */

        //重置显示颜色
        light.map(i => {
            if (!!i.getAttribute('defaultcolor') && !window['cellseparatecolor' + i.id]) {
                window['cellseparatecolor' + i.id] = i.getAttribute('defaultcolor')
            }
            this.setFillColor(i, window['cellseparatecolor' + i.id])
            this.setStrokeColor(i, '#5578b6')

        })
        //重置lable颜色
        if (sigalnametogglekey == 0) {
            namelabel.map(i => this.setLabelText(i, `<div style="background:none;color:#fff;">${uid}</div>`))
        } else if (sigalnametogglekey == 1 && status.delay_30s == 0 && status.delay_180s == 0) {
            namelabel.map(i => this.setLabelText(i, `<div style="visibility:hidden">${uid}</div>`))

        }
        let buttonla = button.find(i => i.getAttribute('type') == 'la')
        let buttonya = button.find(i => i.getAttribute('type') == 'ya')
        let lightda = light.find(i => i.getAttribute('type') == 'da')
        let light0 = light.find(i => i.getAttribute('type') != 'da')
        window.globalintervalcell.delete(buttonla)
        window.globalintervalcell.delete(buttonya)
        window.globalintervalcell.delete(lightda)
        window.globalintervalcell.delete(light0)
        window.globalintervalcell.delete(namelabel[0])
        this.showcell(namelabel[0])
        this.showcell(buttonla)
        this.showcell(buttonya)
        this.showcell(lightda)
        this.showcell(light0)
        //加边框显示
        if (!boundary.length) {

            //获取调车灯坐标作为参考,创建一个叉
            let lightda = light.find(i => i.getAttribute('type') == 'da')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'fork')
                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x + 3, referenceposition.y + 3, 14, 14, "shape=umlDestroy;whiteSpace=wrap;strokeWidth=2;html=1;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");
                newboundary.value = boundaryvalue
                boundary.push(newboundary)
            }
            //方框
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'boundary')
                //是否有两个灯
                let newboundary
                if (light.length == 2) {
                    //是否在左边
                    let lightnone = light.find(i => i.getAttribute('type') != 'da')
                    if (lightda.geometry.x > lightnone.geometry.x) {
                        newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x - 21, referenceposition.y, 42, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");

                    } else {
                        newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 42, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                    }
                } else {
                    newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 19, 19, "whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                }
                newboundary.value = boundaryvalue
                newboundary.specialname = 'rect'
                boundary.push(newboundary)
            }

            //获取列车信号坐标作为参考,创建一个叉
            lightda = light.find(i => i.getAttribute('type') != 'da')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'fork')
                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x + 3, referenceposition.y + 3, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;strokeWidth=2;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");
                newboundary.value = boundaryvalue
                boundary.push(newboundary)
            }



            //获取列车信号按钮坐标作为参考,创建一个叉
            lightda = button.find(i => i.getAttribute('type') == 'la')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'fork')
                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                newboundary.value = boundaryvalue
                boundary.push(newboundary)
            }

            //获取引导按钮坐标作为参考,创建一个叉
            lightda = button.find(i => i.getAttribute('type') == 'ya')
            if (lightda) {
                let referenceposition = lightda.geometry
                let boundaryvalue = lightda.value.cloneNode(true)
                boundaryvalue.setAttribute('name', 'fork')
                let newboundary = this.graph.insertVertex(lightda.parent, null, '', referenceposition.x, referenceposition.y, 14, 14, "shape=umlDestroy;whiteSpace=wrap;html=1;aspect=fixed;strokeWidth=2;strokeColor=red;fillColor=none;cursor=pointer;");
                newboundary.value = boundaryvalue
                boundary.push(newboundary)
            }



        }
        // 隐藏边框
        if (boundary.length) {
            boundary.map(i => {
                this.setStrokeColor(i, '#f00')
                window.graph.model.setVisible(i, 0)
            })
        }

        /**
         * 
         * 开始设置零件样式
         * 
         * / 信号状态
         * 
        struct SignalStatus {
    BYTE red_blue: 1;             // 红/兰
    BYTE white : 1;               // 白灯
    BYTE yellow : 1;              // 黄灯
    BYTE yellow_twice : 1;        // 双黄
    BYTE green_yellow : 1;        // 绿黄
    BYTE green : 1;               // 绿灯
    BYTE red_white : 1;           // 红白
    BYTE green_twice : 1;         // 双绿

    BYTE train_btn_flash : 1;     // 列车按钮闪亮
    BYTE ligth_broken_wire : 1;   // 灯丝断丝
    BYTE shunt_btn_light : 1;     // 调车按钮闪亮
    BYTE flash : 1;               // 闪光
    BYTE reversed : 1;            // 0
    BYTE reversed2 : 1;           // 0
    BYTE delay_180s : 1;          // 延时3分钟
    BYTE delay_30s : 1;           // 延时30秒
                                  
    BYTE guaid_10s : 1;           // 引导10s
    BYTE guaid_flash : 1;     // 坡道延时解锁
    BYTE closed : 1;              // 封闭
    BYTE notice : 5;              // 提示信息
};
         * 
         */

        if (status.closed) {


            let buttonla = button.find(i => i.getAttribute('type') == 'la')
            if (buttonla) {
                //有列车按钮就全部按钮红叉
                boundary.map(i => {
                    if (i.value.getAttribute('name') == 'fork' && (i.value.getAttribute('type') == 'la' || i.value.getAttribute('type') == 'ya')) {
                        window.graph.model.setVisible(i, 1)
                    }
                })
            } else {
                //没有列车就就把车灯红框
                boundary.map(i => {
                    if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                        window.graph.model.setVisible(i, 1)
                    }
                })
            }


        }

        //信号机方框显示 




        if (status.da_start == 1 && status.signal_end == 0) {
            boundary.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    window.graph.model.setVisible(i, 1)
                    this.setStrokeColor(i, 'white')
                }
            })
        }
        if (status.da_start == 0 && status.signal_end == 1) {
            boundary.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    window.graph.model.setVisible(i, 1)
                    this.setStrokeColor(i, '#ffff00')
                }
            })
        }
        if (status.da_start == 1 && status.signal_end == 1) {
            boundary.map(i => {
                if (i.value.getAttribute('name') == 'boundary' && (i.value.getAttribute('type') == 'da' || !i.value.getAttribute('type'))) {
                    window.graph.model.setVisible(i, 1)
                    this.setStrokeColor(i, '#00ff00')
                }
            })
        }



        if (status.red_blue) {

            light.find(i => {
                this.setFillColor(i, window['cellseparatecolor' + i.id])
                this.setStrokeColor(i, window['cellseparatecolor' + i.id])
            })

        }

        if (status.white) {

            let lightda = light.find(i => i.getAttribute('type') == 'da')
            if (lightda) this.setFillColor(lightda, '#fff')
            if (lightda) this.setStrokeColor(lightda, '#fff')

        }

        if (status.guaid_flash && !status.red_white) {
            let lightda = button.find(i => i.getAttribute('type') == 'ya')
            if (lightda) window.globalintervalcell.add(lightda)
        }


        if (status.yellow) {

            let buttonla = button.find(i => i.getAttribute('type') == 'la')
            let light0 = light.find(i => i.getAttribute('type') != 'da')
            let light1 = light.find(i => i.getAttribute('type') == 'da')
            if (buttonla) this.setFillColor(light0, '#ff0')
            if (buttonla) this.setStrokeColor(light0, '#ff0')
            if (buttonla) this.setFillColor(light1, '#000')
            if (buttonla) this.setStrokeColor(light1, 'none')

        }

        if (status.yellow_twice) {

        }

        if (status.green_yellow) {

        }

        if (status.green) {
            let light0 = light.find(i => i.getAttribute('type') != 'da')
            this.setFillColor(light0, '#0f0')
            this.setStrokeColor(light0, '#0f0')
        }

        if (status.red_white) {

            let lightda = light.find(i => i.getAttribute('type') == 'da')
            let light0 = light.find(i => i.getAttribute('type') != 'da')
            if (lightda) this.setFillColor(lightda, '#f00')
            if (light0) this.setFillColor(light0, '#ff0')
            if (lightda) this.setStrokeColor(lightda, '#f00')
            if (light0) this.setStrokeColor(light0, '#ff0')
        }

        if (status.green_twice) {

        }

        if (status.train_btn_flash) {
            let buttonla = button.find(i => i.getAttribute('type') == 'la')
            if (buttonla) window.globalintervalcell.add(buttonla)
        }

        if (status.ligth_broken_wire) {
            if (!window[`signallightalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `信号机${uid}灯丝断丝`
                })
                window[`signallightalarmtag${uid}`] = 1
            }


            let lightda = light.find(i => i.getAttribute('type') == 'da')
            if (lightda) window.globalintervalcell.add(lightda)

        } else {
            if (window[`signallightalarmtag${uid}`]) {
                this.setAlarmStatus({
                    name: `信号机${uid}灯丝恢复`
                })
                window[`signallightalarmtag${uid}`] = 0
            }

        }

        if (status.shunt_btn_light) {

            window.globalintervalcell.add(namelabel[0])
        }

        if (status.flash) {

        }

        if (status.delay_30s || status.delay_180s) {
            namelabel.map(i => {
                this.setLabelText(i, `<div style="white-space:nowrap;background:none;color:#fff;"><span style="white-space:nowrap;background:none;color:#f00;">${uid}</span></div>`)
                window.globalintervalcell.add(i)
            })
        }




        if (status.notice != 0) {

            switch (status.notice) {
                case 1:
                    alarmwarninglistadd(uid + '调始')
                    break
                case 2:
                    alarmwarninglistadd(uid + '调终')
                    break
                case 3:
                    alarmwarninglistadd(uid + '列始')
                    break
                case 4:
                    alarmwarninglistadd(uid + '列终')
                    break
                case 5:
                    alarmwarninglistadd(uid + '变更')
                    break
                case 6:
                    alarmwarninglistadd(uid + '重开')
                    break
                case 7:
                    alarmwarninglistadd(uid + '引导')
                    break
                case 8:
                    alarmwarninglistadd(uid + '通过')
                    break
                case 9:
                    alarmwarninglistadd(uid + '调车取消')
                    break
                case 10:
                    alarmwarninglistadd(uid + '列车取消')
                    break
                case 11:
                    alarmwarninglistadd(uid + '调车人解')
                    break
                case 12:
                    alarmwarninglistadd(uid + '列车人解')
                    break
                case 17:
                    alarmwarninglistadd(uid + '红灯断丝')
                    break
                case 18:
                    alarmwarninglistadd(uid + '灯丝断丝')
                    break
                case 19:
                    alarmwarninglistadd(uid + '有车移动')
                    break
                case 20:
                    alarmwarninglistadd(uid + '有迎面解锁可能')
                    break
                case 21:
                    alarmwarninglistadd(uid + '非正常关闭')
                    break
                case 22:
                    alarmwarninglistadd(uid + '不能取消')
                    break
                case 23:
                    alarmwarninglistadd(uid + '不能通过')
                    break
                case 24:
                    alarmwarninglistadd(uid + '不能引导')
                    break
                case 25:
                    alarmwarninglistadd(uid + '不是列终')
                    break
                case 26:
                    alarmwarninglistadd(uid + '不是列始')
                    break
                case 27:
                    alarmwarninglistadd(uid + '不是调终')
                    break
                case 28:
                    alarmwarninglistadd(uid + '不是调始')
                    break
                case 29:
                    alarmwarninglistadd(uid + '不构成进路')
                    break
                case 30:
                    alarmwarninglistadd(uid + '不能开放')
                    break
                case 31:
                    alarmwarninglistadd(uid + '无驱开放')
                    break

            }
        }


    }



    showcell(c) {
        if (c && c.setVisible) {
            window.graph.model.setVisible(c, 1)
        }
    }
    //换label的文字html
    setLabelText(cell, code) {
        let oldvalue = cell.cloneValue()
        oldvalue.setAttribute('label', code)
        graph.model.setValue(cell, oldvalue)
    }


    //换cell的背景颜色
    setFillColor(cell, color, isFlash) {
        if (!cell) {
            return
        }
        let s = cell.style
        if (!isFlash) {
            window[`oldfillcolor${cell.id}`] = color
        }
        if (s.match(/fillColor=#[^;]*;/ig)) {
            let sarray = s.split(s.match(/fillColor=#[^;]*;/ig)[0])
            let news = sarray[0] + 'fillColor=' + color + ';' + sarray[1]

            graph.model.setStyle(cell, news)

        } else {
            graph.model.setStyle(cell, s + 'fillColor=' + color + ';')
        }
    }

    //换cell的边框颜色
    setStrokeColor(cell, color) {
        if (!cell) {
            return
        }
        let s = cell.style
        if (s.match(/strokeColor=#[^;]*;/ig)) {
            let sarray = s.split(s.match(/strokeColor=#[^;]*;/ig)[0])
            let news = sarray[0] + 'strokeColor=' + color + ';' + sarray[1]
            graph.model.setStyle(cell, news)
        } else {
            graph.model.setStyle(cell, s + 'strokeColor=' + color + ';')
        }
    }



}



/**
 * 
 * 注册一些全局便利方法
 * 
 */

//闪烁
let globalintervalcellflashkey = 0
window.globalintervalcell = new Set()
window.globalinterval = setInterval(() => {
    if (window.globalupdata || !globalintervalcell.size) {
        return
    }
    graph.getModel().beginUpdate()
    for (let cell of globalintervalcell) {
        //使用mxgraphmodel来对cell进行更新会直接刷新界面，效率更高

        if (window[`oldfillcolor${cell.id}`]) {
            let nc = new graphx()
            if (globalintervalcellflashkey) {
                nc.setFillColor(cell, '#000', true)
            } else {
                nc.setFillColor(cell, window[`oldfillcolor${cell.id}`])
            }

        } else {
            window.graph.model.setVisible(cell, globalintervalcellflashkey)
        }

    }
    graph.getModel().endUpdate()

    globalintervalcellflashkey = !globalintervalcellflashkey
}, 500);

//获取cell
window.getCellUid = cell => {

    if (cell.getAttribute('uid')) {
        return cell.getAttribute('uid')
    } else {
        if (cell.parent != null) {
            return getCellUid(cell.parent)
        } else {
            return null
        }
    }

}
window.getEquipCell = cell => {

    if (cell.getAttribute('uid')) {
        return cell
    } else {
        if (cell.parent != null) {
            return getEquipCell(cell.parent)
        } else {
            return null
        }
    }

}
window.getNamedCell = cell => {

    if (cell.getAttribute('name')) {
        return cell
    } else {
        if (cell.parent != null) {
            return getNamedCell(cell.parent)
        } else {
            return null
        }
    }

}

mxCell.prototype.getSubCell = function (name) {

    if (this.children) {
        let loop = cells => {
            let cellarray = []
            for (let i = 0; i < cells.length; i++) {
                if (cells[i].children) {
                    cellarray = cellarray.concat(loop(cells[i].children))
                } else if (cells[i].getAttribute('name') == name) {
                    cellarray.push(cells[i])
                }
            }
            return cellarray
        }
        return loop(this.children)
    } else {
        return null
    }
}



let has_get_plan = false
let cur_plans = []


//设置全局状态


window.set_global_state = state => {

    console.log('接受到数据帧：', state)

    // ['9/11,13/15,51,(57),(17/19),[13/]', '11dg,15-17dg,21/51wg']
    let turnout = [],
        sector = []
    state[0].split(',').filter(x => {
        if (x.indexOf('[') > -1) {
            return false
        } else {
            return true
        }

    }).map(x => {
        if (x.indexOf('/') > -1) {
            x.split('/').map(xx => {
                turnout.push(xx)
            })
        } else {
            turnout.push(x)
        }
    })

    sector = state[1].split(',')

    console.log(turnout, sector)

    // [
    //         ['9', '11', '13', '15', '17', '19', '21', '23', '51', '55', '(57)', '(59)'],
    //         ['11dg', '15-17dg', '51-53dg', '55-59dg', '21dg', '21/51wg', '21ag']
    //     ]

    state = [turnout, sector]

    let na = [],
        cq = []

    state.map((i, inx) => {
        if (!inx) {
            i.map(si => {
                if ((/\(\d*\)|\(\d*|\d*\)/).test(si)) {
                    na.push({
                        name: si.match(/\d+/)[0],
                        type: 1,
                        pos: 0,
                        pos_reverse: 1,
                        hold: 0,
                        lock: 1
                    })
                } else {
                    na.push({
                        name: si.match(/\d+/)[0],
                        type: 1,
                        pos: 1,
                        pos_reverse: 0,
                        hold: 0,
                        lock: 1
                    })
                }

            })
        } else {
            i.map(si => {

                si = si.replace('-', '_')
                cq = cq.concat(si, switchbelongsector[si.toUpperCase()])
                cq = cq.filter(x => !isNaN(x))
                if (!switchbelongsector[si.toUpperCase()]) {
                    na.push({
                        name: si.replace('/', '_'),
                        type: 2,
                        hold: 0,
                        lock: 1
                    })
                }

            })
        }
    })

    console.log(na, cq)

    na = na.filter(x => {
        if (!Number(x.name) || cq.includes(Number(x.name))) {
            return true
        } else {
            return false

        }
    })

    console.log(na)
    state = {
        data: na
    }




    if (!state) {
        return
    }

    //1 道岔
    //2 区段
    //345 出站信号 进站信号 调车信号

    let controlgraph = new graphx()
    let model = controlgraph.graph.getModel()

    window.globalupdata = true
    model.beginUpdate()
    state.data.map((i, index) => {
        i.name = i.name.toUpperCase()
        switch (i.type) {
            case 1:
                controlgraph.setTurnoutStatus(i.name, i)
                break
            case 2:
                controlgraph.setSectorStatus(i.name, i)
                break
        }
    })
    model.endUpdate()
    window.globalupdata = false



}



//存放全部部件细粒度到包含道岔 区段 和信号机 按钮
window.parkequip = {}

/**
 * 
 * 配置地图文件
 * 
 */


//道岔对应区段的json文件

let loadmap = mapname => {



    //有叉区段对应道岔关系
    $.ajax({
        url: `/${mapname}/stationswitchbelongsector.json`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            window.switchbelongsector = data
        }
    })
    //图的xml
    if (location.href.split('?').includes('test')) {
        window.defualtxmldoc = `/${mapname}/station2.xml`
    } else if (location.href.split('?').includes('long')) {
        window.defualtxmldoc = `/${mapname}/stationlong.xml`
    } else {
        window.defualtxmldoc = `/${mapname}/station.xml`
    }
    //按钮表
    $.ajax({
        url: `/${mapname}/mapbuttonindex.json`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            window.equipindex = data
        }
    })

}


loadmap('banqiao')

/**
 * 
 * 开始初始化EditorUI
 * 
 */
//配置mxConstants
mxConstants.DROP_TARGET_COLOR = '#ff0'
mxConstants.HIGHLIGHT_OPACITY = 70

var editorUiInit = EditorUi.prototype.init;
EditorUi.prototype.init = function () {
    editorUiInit.apply(this, arguments);
    this.actions.get('export').setEnabled(false);
};
// Adds required resources (disables loading of fallback properties, this can only
// be used if we know that all keys are defined in the language specific file)
mxResources.loadDefaultBundle = false;
var bundle = mxResources.getDefaultBundle(RESOURCE_BASE, mxLanguage) ||
    mxResources.getSpecialBundle(RESOURCE_BASE, mxLanguage);
// Fixes possible asynchronous requests
mxUtils.getAll([bundle, STYLE_PATH + '/default.xml', defualtxmldoc], function (xhr) {
    // Adds bundle text to resources
    mxResources.parse(xhr[0].getText());
    // Configures the default graph theme
    var themes = new Object();
    themes[Graph.prototype.defaultThemeName] = xhr[1].getDocumentElement();
    new EditorUi(new Editor(urlParams['chrome'] == '0', themes), document.querySelector('.graphbody'));

    /**
     * 
     * 引入xml后初始化配置和显示特性
     * 
     * 
     */
    window.equipcellindex = {}
    window.graph.importGraphModel(xhr[2].getDocumentElement())
    window.graph.setCellsSelectable(false)
    // window.graph.setCellsMovable(false)
    window.graph.setCellsEditable(false)


    for (let i in window.graph.getModel().cells) {
        let cell = window.graph.getModel().cells[i]




        //如果发现uid属性则加入全局存放
        if (cell.getAttribute('uid')) {





            //把road放置到最上面，保证添加占线图标后图标在road的label上能显示到最前
            if (cell.getSubCell('road')) {
                graph.orderCells(0, [cell.getSubCell('road')[0]])
            }
            let ouid = cell.getAttribute('uid').toUpperCase()
            let uid = cell.getAttribute('uid').toUpperCase()
            uid = uid.replace('/', '_')
            cell.setAttribute('uid', uid)
            window.parkequip[cell.getAttribute('uid')] = cell
            //给所有部件的label添加文字
            if (cell.getSubCell('label') && cell.getSubCell('label')[0]) {
                cell.getSubCell('label')[0].setAttribute('label', ouid)

                window.graph.orderCells(1, cell.getSubCell('label'))

            }



            //把cell按钮的cellid 和 按钮表的index 对应起来 放到equipcellindex中
            equipindex.map(s => {


                let index = s.split(' = ')[0]
                let name = s.split(' = ')[1]
                let ty = s.split(' = ')[2]


                if (uid.indexOf('BTN') > -1) {
                    uid = uid.split('BTN')[0]
                }


                if (name == uid) {


                    if (cell.value.getAttribute('type') == 'BTN') {
                        equipcellindex[cell.id] = index
                        return
                    }

                    if (cell.getSubCell('light').length == 0 && cell.getSubCell('button').length == 0) {
                        equipcellindex[cell.id] = index
                        return
                    }


                    cell.getSubCell('light').map(light => {

                        if (light.getAttribute('type') && light.getAttribute('type').toUpperCase() == ty) {
                            equipcellindex[light.id] = index
                        }

                    })
                    cell.getSubCell('button').map(button => {
                        if (button.getAttribute('type') && button.getAttribute('type').toUpperCase() == ty) {
                            equipcellindex[button.id] = index
                        }
                    })
                }

            })

        }

        //默认隐藏有叉区段的名称lable
        if (cell.getAttribute('belongsector') && !cell.children) {
            cell.setAttribute('label', `  <div xmlns="http://www.w3.org/1999/xhtml" style="white-space: nowrap;">${cell.getAttribute('belongsector').toUpperCase().replace('_', '-')}</div>`)
            window.parkequip[cell.getAttribute('belongsector').toLowerCase()] = cell
        }

        //处理所有edge
        if (cell.edge && cell.target) {
            window.graph.model.setVisible(cell, 0)
        }
    }



    window.graph.refresh()
    //xml加载完成


    //滚动视图到中心

    window.graph.center()






}, function () {
    document.body.innerHTML =
        '<center style="margin-top:10%;">Error loading resource files. Please check browser console.</center>';
});