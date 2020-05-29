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


    //获取道岔或股道的中心定位点
    getroadturnoutcenter(uid) {
        uid = uid.toUpperCase()
        let road
        if (parkequip[uid].getAttribute('type') == 'ca') {

            if (Math.abs(graph.view.getState(parkequip[uid].getSubCell('direct')[0]).shape.rotation) > 10) {
                road = parkequip[uid].getSubCell('reverse')[0]
            } else {
                road = parkequip[uid].getSubCell('direct')[0]
            }

        } else {
            road = parkequip[uid].getSubCell('road')[0]
        }

        return graph.view.getState(road).cellBounds.getCenterX()

    }
    //生成目标容器
    generateVessel(position, CB) {

        //新建股道和道岔的列车容器cell
        let traincell = graph.insertVertex(graph.model.cells[1], null, parkequip['TRAIN'].cloneValue(), 0, 0, 220, 30, "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#FFFFFF;");
        this.setLabelText(traincell, `<div  style="visibility:${window.showvessel?'unset':'hidden'}" class='trainvessel trainvesseltrain' id="V${position}"></div>`)
        parkequipvessel[position] = traincell

        //移动到股道和道岔位置
        let road, GX, GY
        if (parkequip[position].getAttribute('type') == 'ca') {

            if (Math.abs(graph.view.getState(parkequip[position].getSubCell('direct')[0]).shape.rotation) > 10) {
                road = parkequip[position].getSubCell('reverse')[0]
            } else {
                road = parkequip[position].getSubCell('direct')[0]
            }

        } else {
            road = parkequip[position].getSubCell('road')[0]
        }
        //如果是股道则放到水平的那个叉上面


        GX = graph.view.getState(road).cellBounds.getCenterX()
        GY = graph.view.getState(road).cellBounds.getCenterY()




        graph.translateCell(traincell, GX - traincell.geometry.x - traincell.geometry.width / 2, GY - traincell.geometry.y - traincell.geometry.height - 7)
        //执行后续逻辑

        setTimeout(() => {
            CB()
        }, 10);
    }




    //列车信息
    // {
    //     name: 'a', //名称
    //     position: 'd37g', //位置’
    // }



    setTrainStatus(status) {
        status.position = status.Dev_name
        status.name = status.MDIAS_window

        //排除非法部件
        if(!parkequip[status.position]){
            return
        }

        let vesselid = status.position.toUpperCase()


        let CB = () => {




            let direction = 'right'
            //根据列车上次目标点与当前目标点和方向来判定

            if (!window['preposition' + status.name]) {
                //如果没有记录为第一次渲染则默认
                direction = 'right'
            } else if (window['preposition' + status.name] == status.position) {
                //如果上次位置和本次相同，直接返回
                return
            } else if (window['preposition' + status.name] != status.position) {
                //把列车从上一个位置移除,移除后保存到cell
                $(`#train${status.name}`).remove()
                let doms = $('#V' + window['preposition' + status.name])
                parkequipvessel[window['preposition' + status.name]].value.setAttribute('label', doms.get(0).outerHTML)
                //如果上次位置和本次不同，获取上次位置和本次位置的坐标进行比对
                if (this.getroadturnoutcenter(status.position) > this.getroadturnoutcenter(window['preposition' + status.name])) {
                    direction = 'right'
                } else {
                    direction = 'left'
                }
            }


            let train
            if (direction == 'right') {
                train = $(`<div class='trainbk' id='train${status.name}'>${status.name}</div>`)
            } else {
                train = $(`<div class='trainbk trainbkleft' id='train${status.name}'>${status.name}</div>`)
            }
            //把列车放入目标位置label的的div中
            let doms = $('#V' + vesselid).append(train)
            graph.setAttributeForCell(parkequipvessel[vesselid], 'label', doms.get(0).outerHTML)

            //记录本次位置
            window['preposition' + status.name] = status.position.toUpperCase()
        }
        //为目标位置创建容器,然后完成逻辑

        if (parkequipvessel[vesselid]) {
            CB()
        } else {
            this.generateVessel(vesselid, CB)
        }

    }


    setAlarmStatus(i) {
        if ($('.alarmplane div p').length < 22) {} else {
            $('.alarmplane div p:first-child').remove()
        }
        $('.alarmplane div').append(`<p>${moment().format('MM-DD HH:mm:ss')} ${i.name}</p>`)
        document.querySelector('.alarmplane').scrollTop = 10000
    }

    setTurnoutStatus(uid, status) {
        let cell = this.getEquip(uid)
        if (!cell) return
        cell.equipstatus = status

        changeplanprogress(uid, status)

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


        if (status.switch) {
            //预排蓝光变挤岔
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




        //黑色稳定显示：表示道岔刚失去表示
        if (status.pos == 0 && status.pos_reverse == 0) {
            let a = [reverse, direct]
            a.map(ip => {
                ip.map(i => {
                    window.graph.model.setVisible(i, 0)
                })
            })
            namelabel.map(i => this.setLabelText(i, `<div style="color:#f00;">${uid}</div>`))
        }
        if (lightbeltkey) {
            let a = [roadentrance]

            if (status.pos == 1 && status.pos_reverse == 0) {
                a.push(roaddirect, direct)
            }

            if (status.pos == 0 && status.pos_reverse == 1) {
                a.push(roadreverse, reverse)
            }

            a.map(ip => {
                ip.map(i => {
                    this.setFillColor(i, '#ff0')
                })
            })
        }

        if (turnoutnamekey == 1) {
            namelabel.map(i => this.setLabelText(i, `<div style="visibility:hidden">${uid}</div>`))
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

        changeplanprogress(uid, status)
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
        if (withoutturnoutsectionkey == 0) {
            //重置lable颜色
            namelabel.map(i => this.setLabelText(i, `<div style="background:none;color:#fff;">${uid}</div>`))
        } else {
            //隐藏label
            namelabel.map(i => this.setLabelText(i, `<div style="visibility:hidden">${uid}</div>`))
        }

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

        changeplanprogress(uid, status)

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
 * 站场操作相关的内容都放到graphAction对象
 * 
 */

window.graphAction = {
    //0：当前空闲没有操作
    //1：列车进路
    //2：调车进路
    //3：引导进路
    //4：进路取消
    //5：总人解
    //6: 道岔总定

    status: 0,
    //当前命令stamp
    actionMark: null,
    //当前触发命令按钮路径
    clickPath: [],
    //操作开始时间，超过失效
    startTime: null,
    //计时函数
    startCounting() {
        this.startTime = Date.now()
        let actionMark = Math.random()
        this.actionMark = actionMark
        let temporaryid = setInterval(() => {
            if (this.actionMark != actionMark) {
                clearInterval(temporaryid)
                $('#countingdown').html('空闲')
                return
            }
            // console.log(Math.floor(15000 - (Date.now() - this.startTime)))
            $('#countingdown').html('操作剩余时间：<span style="color:red">' + Math.ceil((15000 - (Date.now() - this.startTime)) / 1000) + 's</span>')
        }, 800);
        setTimeout(i => {
            if (this.actionMark != actionMark) return
            this.resetStatus()
        }, 15000)
    },
    //重置状态
    resetStatus() {

        this.startTime = null
        this.status = 0
        this.actionMark = Math.random()
        this.clickPath = []
    },
    //发送命令重置状态
    commitAction() {


        switch (this.status) {
            case 1:
                this.status = 0x05
                break
            case 2:
                this.status = 0x05
                break
            case 3:
                this.status = 0xCA
                break
            case 4:
                this.status = 0x1A
                break
            case 5:
                this.status = 0x45
                break
            case 6:
                this.status = 0x25
                this.clickPath.push(0x01)
                break
            case 7:
                this.status = 0x25
                this.clickPath.push(0x02)
                break
            case 8:
                this.status = 0x25
                this.clickPath.push(0x03)
                break
            case 9:
                this.status = 0x25
                this.clickPath.push(0x04)
                break
            case 10:
                this.status = 0x25
                this.clickPath.push(0x05)
                break
            case 11:
                this.status = 0x25
                this.clickPath.push(0x06)
                break
            case 12:
                this.status = 0x45
                break
            case 13:
                this.status = 0x5A
                break
            case 14:

                // if ($($('#graphactionbtn button')[0]).attr('style').indexOf('back') > -1) {
                //     this.status = 0x7B
                // } else {
                this.status = 0x7A
                // }
                break

            case 15:
                this.status = 0XB5
                this.clickPath.push(0x01)
                break
            case 16:
                this.status = 0XB5
                this.clickPath.push(0x02)
                break
            case 17:
                this.status = 0X3A
                break
        }

        let copy = JSON.parse(JSON.stringify({
            status: this.status,
            clickPath: this.clickPath
        }))



        this.resetStatus()

        if (copy.clickPath[0] == copy.clickPath[1]) {
            return
        }
        console.log('前端发出命令', copy)
        window.cefQuery({
            request: JSON.stringify({
                cmd: "commit_action",
                data: copy
            }),
            persistent: false,
            onSuccess: function (response) {
                // def.resolve(response)
            },
            onFailure: function (error_code, error_message) {
                // def.reject(error_message)
            }
        })


    },

    //按钮点击处理
    buttonClick(equip, button, e) {
        console.log('点击按钮', equip, button)
        //通信中断后不可操作
        if (window.sysblackout) {
            return
        }

        //空闲时
        if (this.status == 0) {

            //closed按钮不能点

            if (equip && equip.cell && equip.cell.equipstatus && equip.cell.equipstatus.closed == 1) {
                return
            }

            //BTN按钮
            if (button && button.type && button.type == 'BTN') {
                console.log('前端发出命令', {
                    clickPath: [{
                        index: Number(button.uindex),
                        name: equip.cell.equipstatus.name
                    }],
                    status: 0xAA
                })
                window.cefQuery({
                    request: JSON.stringify({
                        cmd: "commit_action",
                        data: {
                            clickPath: [{
                                index: Number(button.uindex),
                                name: equip.cell.equipstatus.name
                            }],
                            status: 0xAA
                        }
                    }),
                    persistent: false,
                    onSuccess: function (response) {
                        // def.resolve(response)
                    },
                    onFailure: function (error_code, error_message) {
                        // def.reject(error_message)
                    }
                })
                return
            }


            //始端列车按钮（LA）
            if (button && button.type && button.type == 'la') {
                if (!button.uindex) {
                    return
                }
                if (equip.cell.equipstatus.da_start == 1, equip.cell.equipstatus.signal_end == 1) {
                    console.log('前端发出命令', {
                        clickPath: [{
                            index: Number(button.uindex),
                            name: equip.cell.equipstatus.name
                        }],
                        status: 0x3A
                    })
                    window.cefQuery({
                        request: JSON.stringify({
                            cmd: "commit_action",
                            data: {
                                clickPath: [{
                                    index: Number(button.uindex),
                                    name: equip.cell.equipstatus.name
                                }],
                                status: 0x3A
                            }
                        }),
                        persistent: false,
                        onSuccess: function (response) {
                            // def.resolve(response)
                        },
                        onFailure: function (error_code, error_message) {
                            // def.reject(error_message)
                        }
                    })
                    return
                }
                document.querySelector('#signalname').innerHTML = ('始列' + equip.cell.equipstatus.name)
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.status = 1
                this.startCounting()
                return
            }
            //始端调车按钮（DA）
            if (button && button.type && button.type == 'da') {


                if (!button.uindex) {
                    return
                }

                if (equip.cell.equipstatus.da_start == 1 && equip.cell.equipstatus.signal_end == 0) {
                    console.log('前端发出命令', {
                        clickPath: [{
                            index: Number(button.uindex),
                            name: equip.cell.equipstatus.name
                        }],
                        status: 0x3A
                    })
                    window.cefQuery({
                        request: JSON.stringify({
                            cmd: "commit_action",
                            data: {
                                clickPath: [{
                                    index: Number(button.uindex),
                                    name: equip.cell.equipstatus.name
                                }],
                                status: 0x3A
                            }
                        }),
                        persistent: false,
                        onSuccess: function (response) {
                            // def.resolve(response)
                        },
                        onFailure: function (error_code, error_message) {
                            // def.reject(error_message)
                        }
                    })
                    return
                }

                document.querySelector('#signalname').innerHTML = ('始调' + equip.cell.equipstatus.name)
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.status = 2
                this.startCounting()
                return
            }
            //信号机引导按钮(YA)
            if (button && button.type && button.type == 'ya') {

                if (!button.uindex) {
                    return
                }

                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.status = 3
                this.startCounting()


                //引导状态发送指令


                if (equip.cell.equipstatus.guaid_10s) {
                    this.commitAction()
                    return
                }

                if (equip.cell.equipstatus.red_white) {
                    return
                }

                //调出键盘
                ikeyboard.options.position.of = e
                ikeyboard.reveal().insertText('')
                return
            }
            //进路取消
            if (equip == 'allcancel') {

                this.status = 4
                this.startCounting()
                return
            }
            //取消引导进路
            if (equip == 'allrelieve') {

                //调出键盘
                ikeyboard.options.position.of = $('#graphactionbtn button:nth-child(4)')
                ikeyboard.reveal().insertText('')
                this.status = 5
                window.graphActionCallback = i => {
                    this.startCounting()
                    window.graphActionCallback = null
                }
                return
            }
            //道岔总定
            if (equip == 'switchdirect') {

                this.status = 6
                this.startCounting()
                return
            }
            //道岔总反
            if (equip == 'switchreverse') {

                this.status = 7
                this.startCounting()
                return
            }
            //道岔单锁
            if (equip == 'switchlock') {

                this.status = 8
                this.startCounting()
                return
            }
            //道岔解锁
            if (equip == 'switchunlock') {

                this.status = 9
                this.startCounting()
                return
            }
            //道岔单封
            if (equip == 'switchblock') {

                this.status = 10
                this.startCounting()
                return
            }
            //道岔解封
            if (equip == 'switchunblock') {

                this.status = 11
                this.startCounting()
                return
            }
            //区段故障解锁
            if (equip == 'sectorfaultunlock') {

                //调出键盘
                ikeyboard.options.position.of = $('#graphactionbtn button:nth-child(5)')
                ikeyboard.reveal().insertText('')
                this.status = 13
                window.graphActionCallback = i => {
                    //在区故解时显示全部区段
                    Object.keys(window.switchbelongsector).map(k => {
                        let c = window.parkequip[k.toLowerCase()]

                        if (c) {
                            window.graph.model.setVisible(c, 1)
                        }
                    })

                    this.startCounting()
                    window.graphActionCallback = null
                }
                return
            }
            //引导总锁
            if (equip == 'alllock') {
                //调出键盘
                ikeyboard.options.position.of = $('#graphactionbtn button:nth-child(2)')
                ikeyboard.reveal().insertText('')
                this.status = 14
                window.graphActionCallback = i => {
                    this.clickPath.push(Number(bottombutton.index))
                    this.commitAction()
                    window.graphActionCallback = null
                }
                return
            }
            //按钮封闭
            if (equip == 'signalblock') {

                this.status = 15
                this.startCounting()
                return
            }
            //按钮解封
            if (equip == 'signalunblock') {

                this.status = 16
                this.startCounting()
                return
            }
        }

        /**
         * 
         * 处理函数
         * 
         */

        //处理列车进路
        if (this.status == 1) {
            if (equip && equip.cell && equip.cell.equipstatus && equip.cell.equipstatus.closed == 1) {
                return
            }
            if (button && button.type && button.type == 'la' && equip.uid != this.clickPath[0]) {
                if (!button.uindex) {
                    return
                }

                document.querySelector('#signalname').innerHTML += ('——终列' + equip.cell.equipstatus.name)
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }

        //处理调车进路
        if (this.status == 2) {
            if (equip && equip.cell && equip.cell.equipstatus && equip.cell.equipstatus.closed == 1) {
                return
            }
            if (button && button.type && button.type == 'da' && equip.uid != this.clickPath[0]) {
                if (!button.uindex) {
                    return
                }

                document.querySelector('#signalname').innerHTML += ('——终调' + equip.cell.equipstatus.name)
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }

        //引导进路
        if (this.status == 3) {
            if (equip == 'confirmya') {
                this.commitAction()
                return
            }
        }

        //进路取消
        if (this.status == 4) {
            if (equip && equip.cell && equip.cell.equipstatus && equip.cell.equipstatus.closed == 1) {
                return
            }

            if (button && button.type && (button.type == 'da' || button.type == 'la')) {

                if (!button.uindex) {
                    return
                }
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //进路取消
        if (this.status == 5) {



            if (equip && equip.cell && equip.cell.equipstatus && equip.cell.equipstatus.closed == 1) {
                return
            }

            if (equip && equip.cell && equip.cell.equipstatus.red_white || equip.cell.equipstatus.guaid_flash) {
                //取消引导进路
                this.status = 5
                if (button && button.type && (button.type == 'la' || button.type == 'ya')) {

                    if (!button.uindex) {
                        return
                    }
                    let buttonla = equip.cell.getSubCell('button').find(i => i.getAttribute('type') == 'la')
                    this.clickPath.push({
                        index: Number(equipcellindex[buttonla.id]),
                        name: equip.cell.equipstatus.name
                    })
                    this.commitAction()
                    return
                }
            } else if (equip.cell) {

                this.status = 12
                if (button && button.type && (button.type == 'la' || button.type == 'da')) {

                    if (!button.uindex) {
                        return
                    }
                    this.clickPath.push({
                        index: Number(button.uindex),
                        name: equip.cell.equipstatus.name
                    })
                    this.commitAction()
                    return
                }
            }

        }
        //道岔总定
        if (this.status == 6) {
            if (equip.type == 'ca') {



                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //道岔总反
        if (this.status == 7) {
            if (equip.type == 'ca') {


                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //道岔单锁
        if (this.status == 8) {
            if (equip.type == 'ca') {


                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //道岔解锁
        if (this.status == 9) {
            if (equip.type == 'ca') {


                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //道岔单封
        if (this.status == 10) {
            if (equip.type == 'ca') {


                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //道岔解封
        if (this.status == 11) {
            if (equip.type == 'ca') {


                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //区段故障解锁
        if (this.status == 13) {

            if (equip.type == 'wc' || equip.type == 'cq') {

                //隐藏cq股道
                //在区故解时显示全部区段
                Object.keys(window.switchbelongsector).map(k => {
                    let c = window.parkequip[k.toLowerCase()]
                    window.graph.model.setVisible(c, 0)
                })

                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //按钮封闭
        if (this.status == 15) {
            if (button && button.type && (button.type == 'da' || button.type == 'la')) {

                if (!button.uindex) {
                    return
                }
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //按钮解封
        if (this.status == 16) {
            if (button && button.type && (button.type == 'da' || button.type == 'la')) {

                if (!button.uindex) {
                    return
                }
                this.clickPath.push({
                    index: Number(button.uindex),
                    name: equip.cell.equipstatus.name
                })
                this.commitAction()
                return
            }
        }
        //清除
        if (equip == 'clearaction') {

            this.resetStatus()
            return
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

    if (!state) {
        return
    }

    //1 道岔
    //2 区段
    //345 出站信号 进站信号 调车信号

    let controlgraph = new graphx()
    let model = controlgraph.graph.getModel()

    if (['DATA_SDI', 'DATA_SDCI'].includes(state['data_type'])) {

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
                case 3:
                case 4:
                case 5:
                    controlgraph.setSignalStatus(i.name, i)
                    break
                case 6:
                    controlgraph.setLightStatus(i.name, i)
                    break
                case 8:

                    if (i.value) {
                        if (!window[i.name + 'galarmkey']) {
                            controlgraph.setAlarmStatus(i)
                            window[i.name + 'galarmkey'] = 1
                        }

                    } else {
                        if (window[i.name + 'galarmkey']) {
                            controlgraph.setAlarmStatus({
                                name: i.name + '恢复'
                            })
                            window[i.name + 'galarmkey'] = 0
                        }
                    }
                    break
            }
        })
        model.endUpdate()
        window.globalupdata = false
    }
    //处理故障
    if (['DATA_FIR'].includes(state['data_type'])) {

        document.querySelector('#signalname').innerHTML = ''
        /*
        *  故障信息报告帧
        // */
        // struct FIR_NODE {
        //     BYTE op_code;           // 操作号
        //     BYTE notice_code;       // 提示信息代码
        //     WORD equip_code;        // 设备号
        //     BYTE equip_property;    // 设备性质
        //     BYTE revered;           // 预留
        // };
        // state.data.equip_code


        let equip

        for (let i in parkequip) {
            if (parkequip[i].equipstatus && parkequip[i].equipstatus.index == state.data.equip_code) {
                equip = parkequip[i]
            }
        }

        let equiptype = [{
            type: 0x55,
            name: '列车信号'
        }, {
            type: 0xaa,
            name: '调车信号'
        }, {
            type: 0x1F,
            name: '道岔'
        }, {
            type: 0x1E,
            name: '区段'
        }, {
            type: 0x21,
            name: '非进路调车'
        }, {
            type: 0xA5,
            name: '按钮'
        }]

        let et = equiptype.find(p => {
            return p.type == state.data.equip_property
        })

        let equiptypeinfo = [{
            type: 0,
            name: ''
        }, {
            type: 1,
            name: '进路选不出'
        }, {
            type: 2,
            name: '信号不能保持'
        }, {
            type: 3,
            name: '命令不能执行'
        }, {
            type: 4,
            name: '信号不能开放'
        }, {
            type: 5,
            name: '灯丝断丝'
        }, {
            type: 6,
            name: '2灯丝断丝'
        }, {
            type: 6,
            name: '操作错误'
        }, {
            type: 6,
            name: '操作无效'
        }, {
            type: 6,
            name: '不能自动解锁'
        }, {
            type: 0x0a,
            name: '进路不能闭锁'
        }]

        let eti = equiptypeinfo.find(p => {
            return p.type == state.data.notice_code
        })


        alarmwarninglistadd(et.name + equip.equipstatus.name + eti.name)



    }
    //处理状态
    if (['DATA_RSR'].includes(state['data_type'])) {
        /*
        *  运行状态报告帧
        // */
        // struct RSR_NODE {
        //     BYTE server_status //主备机;
        //     BYTE control_status 站控非站控;
        // };

        if (state.data.server_status == 0x55) {

        } else if (state.data.server_status == 0xaa) {

        }

        if (state.data.control_status == 0x55) {

            //自律控制绿色
            let nc = new graphx()
            let cell = parkequip['自律控制']
            let light = cell.getSubCell('light')[0]
            nc.setFillColor(light, '#0f0')

            window.mdiadcontrol = true

            if (1) {

                if (window.selfcontrolplan) {
                    let cell = parkequip['集控模式']
                    let light = cell.getSubCell('button')[0]
                    nc.setFillColor(light, '#ffd966')
                    light = cell.getSubCell('light')[0]
                    nc.setFillColor(light, '#000')

                    let cell2 = parkequip['自控模式']
                    let light2 = cell2.getSubCell('button')[0]
                    nc.setFillColor(light2, '#ffd966')
                    light2 = cell2.getSubCell('light')[0]
                    nc.setFillColor(light2, '#0f0')
                } else {
                    let cell = parkequip['集控模式']
                    let light = cell.getSubCell('button')[0]
                    nc.setFillColor(light, '#ffd966')
                    light = cell.getSubCell('light')[0]
                    nc.setFillColor(light, '#0f0')

                    let cell2 = parkequip['自控模式']
                    let light2 = cell2.getSubCell('button')[0]
                    nc.setFillColor(light2, '#ffd966')
                    light2 = cell2.getSubCell('light')[0]
                    nc.setFillColor(light2, '#000')
                }


            }




        } else if (state.data.control_status == 0xaa) {

            //自律控制灭灯
            let nc = new graphx()
            let cell = parkequip['自律控制']
            let light = cell.getSubCell('light')[0]
            nc.setFillColor(light, '#000')

            window.mdiadcontrol = false



            if (1) {
                let cell = parkequip['集控模式']
                let light = cell.getSubCell('button')[0]
                nc.setFillColor(light, '#b3b3b3')
                light = cell.getSubCell('light')[0]
                nc.setFillColor(light, '#000')

                let cell2 = parkequip['自控模式']
                let light2 = cell2.getSubCell('button')[0]
                nc.setFillColor(light2, '#b3b3b3')
                light2 = cell2.getSubCell('light')[0]
                nc.setFillColor(light2, '#000')
            }

        }

    }

    //通信状态
    if (['DATA_NETINFO'].includes(state['data_type'])) {


        let nc = new graphx()
        let cell = parkequip['允许MDIAS控']
        let light = cell.getSubCell('light')[0]
        nc.setFillColor(light, '#000')


        if (state.data.type) {
            if (state.data.status == 1) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: 'MDIAS与CI通信中断'
                })
            } else if (state.data.status == 0) {

                let cell = parkequip['允许MDIAS控']
                let light = cell.getSubCell('light')[0]
                nc.setFillColor(light, '#0f0')
                blockin()
                controlgraph.setAlarmStatus({
                    name: 'MDIAS与CI通信恢复'
                })
            } else if (state.data.status == 2) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: '连锁机器故障'
                })
            } else if (state.data.status == 3) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: '连锁通信数据错误'
                })
            }
        } else {

            if (state.data.status == 1) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: '前置机通信中断'
                })
            } else if (state.data.status == 0) {

                let cell = parkequip['允许MDIAS控']
                let light = cell.getSubCell('light')[0]
                nc.setFillColor(light, '#0f0')
                blockin()
                controlgraph.setAlarmStatus({
                    name: '前置机通信恢复'
                })
            } else if (state.data.status == 2) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: '前置机机器故障'
                })
            } else if (state.data.status == 3) {
                blockout()
                controlgraph.setAlarmStatus({
                    name: '前置机通信数据错误'
                })
            }
        }

    }

    //列车位置数据
    if (['DATA_ATS'].includes(state['data_type'])) {
        //列车信息全体消息
        if (state.data.msg_id && state.data.msg_id == 15) {
            set_globaltrain_state(state.data.trains)
        }
    }


}

//设置现车状态
window.set_globaltrain_state = trainstate => {
    let controlgraph = new graphx()
    trainstate.map((i, index) => {
        /**
         * 
         * 为目标位置创建cell 如VD1G,
         * 在cell的label中放入代表列车状态的div
         * 
         */
        controlgraph.setTrainStatus(i)
    })

}

//存放全部部件细粒度到包含道岔 区段 和信号机 按钮
window.parkequip = {}

window.parkequipvessel = {}


/**
 * 
 * 配置地图文件
 * 
 */


//道岔对应区段的json文件

let loadmap = mapname => {

    //加载图对应的底部按钮
    $.ajax({
        url: `../parkbottombutton/parkbottombtn.json`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            let index = data[mapname][0].split(' = ')[0]
            let name = data[mapname][0].split(' = ')[1]
            let ty = data[mapname][0].split(' = ')[2]

            window.bottombutton = {
                index,
                name,
                type: ty
            }

            //设置底部btn
            $('#parkbottombtn1').html(name)

        }
    })

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

        //给灯加一个底圈
        if (cell.getAttribute('name') == 'light' && /^[^\u4e00-\u9fa5]+$/.test(getCellUid(cell))) {
            let referenceposition = cell.geometry,
                newboundary = window.graph.insertVertex(cell.parent, null, '', referenceposition.x, referenceposition.y, 19, 19, "shape=ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeColor=#3694FF;fillColor=black;cursor=pointer;");
            window.graph.orderCells(1, [newboundary])

            if (getEquipCell(cell)) {
                getEquipCell(cell).children.map(c => {
                    if (c.geometry.width == 6) {
                        window.graph.orderCells(1, [c])
                    }
                })
            }
        }


        //处理道岔
        if (cell.getAttribute('type') == 'ca') {

            //获取正位反位的旋转值
            let originreverse = cell.getSubCell('reverse')[0]
            let origindirect = cell.getSubCell('direct')[0]
            let originroad
            let originrotateroad
            if (Math.abs(graph.getCellStyle(origindirect).rotation) > Math.abs(graph.getCellStyle(originreverse).rotation)) {
                originroad = originreverse
                originrotateroad = origindirect
            } else {
                originroad = origindirect
                originrotateroad = originreverse
            }
            let angle
            if (graph.getCellStyle(originrotateroad).rotation > 0) {
                angle = graph.getCellStyle(originrotateroad).rotation
            } else {
                angle = 360 + graph.getCellStyle(originrotateroad).rotation
            }

            let upon
            let rightward = true
            if (originrotateroad.geometry.y > originroad.geometry.y) {
                upon = false
            } else {
                upon = true
            }

            if ((angle > 0 && angle < 90) || (angle > 180 && angle < 270)) {
                //  \
                if (upon) {
                    rightward = false
                }
            }
            if ((angle > 90 && angle < 180) || (angle > 270 && angle < 360)) {
                //  /
                if (!upon) {
                    rightward = false
                }
            }



            //获取direct的坐标作为参考,创建一个圆形边框
            let referenceposition = originroad.geometry
            let boundaryvalue = originroad.value.cloneNode(true)
            boundaryvalue.setAttribute('name', 'boundary')
            let newboundary
            if (!rightward) {
                newboundary = window.graph.insertVertex(cell, null, '', referenceposition.x - 15 + referenceposition.width, referenceposition.y - 9, 23, 23, "shape=ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");
            } else {
                newboundary = window.graph.insertVertex(cell, null, '', referenceposition.x - 6, referenceposition.y - 9, 23, 23, "shape=ellipse;whiteSpace=wrap;html=1;aspect=fixed;strokeColor=red;fillColor=none;cursor=pointer;");
            }
            newboundary.value = boundaryvalue
            newboundary.specialname = 'lock'


        }


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
            //默认隐藏
            window.graph.model.setVisible(cell, 0)
        }

        //给带有name属性的cell添加手势
        if (cell.getAttribute('name')) {
            setTimeout(i => {
                if (window.graph.view.getState(cell)) window.graph.view.getState(cell).setCursor('pointer')
            }, 0)

        }
        //处理所有edge
        if (cell.edge && cell.target) {
            window.graph.model.setVisible(cell, 0)
        }
    }


    //注册graph的鼠标事件处理
    window.graph.addMouseListener({
        mouseDown: function (sender, evt) {

            //过滤鼠标右键
            if (evt.evt.button == 2) {

                if (evt.evt.target && evt.evt.target.className && evt.evt.target.className.indexOf && evt.evt.target.className.indexOf('placedbusyicon') > -1) {
                    //占线板图标右键
                    if (evt.sourceState.cell && getCellUid(evt.sourceState.cell)) {
                        window.busytypedata = getCellUid(evt.sourceState.cell)

                    }
                }
                return
            }
            //过滤非点击区域
            if (evt.sourceState) {

                if (getCellUid(evt.sourceState.cell)) {

                    console.log('元件状态：', getEquipCell(evt.sourceState.cell).equipstatus)




                    //把点击按钮和部件发送给graphAction处理
                    let uindex = equipcellindex[evt.sourceState.cell.id] ? equipcellindex[evt.sourceState.cell.id] : equipcellindex[getEquipCell(evt.sourceState.cell).id]

                    if (getEquipCell(evt.sourceState.cell).getAttribute('type') == 'selfcontrolplan') {
                        if (window.mdiadcontrol) {
                            let nc = new graphx()
                            if (getEquipCell(evt.sourceState.cell).getAttribute('uid') == '自控模式') {


                                pop.confirm({
                                    title: "提示",
                                    sizeAdapt: false,
                                    content: "请确定是否切换到自控模式",
                                    button: [
                                        ["success", "确定",
                                            function (e) {
                                                pop.close(e)
                                                window.selfcontrolplan = true
                                                let cell = parkequip['集控模式']
                                                let light = cell.getSubCell('button')[0]
                                                nc.setFillColor(light, '#ffd966')
                                                light = cell.getSubCell('light')[0]
                                                nc.setFillColor(light, '#000')

                                                let cell2 = parkequip['自控模式']
                                                let light2 = cell2.getSubCell('button')[0]
                                                nc.setFillColor(light2, '#ffd966')
                                                light2 = cell2.getSubCell('light')[0]
                                                nc.setFillColor(light2, '#0f0')
                                            }
                                        ],
                                        ["default", "取消",
                                            function (e) {
                                                pop.close(e)
                                            }
                                        ]
                                    ],
                                    buttonSpcl: "",
                                    anim: "fadeIn-zoom",
                                    width: 450,
                                    height: 180,
                                    id: "random-72160",
                                    place: 5,
                                    drag: true,
                                    index: true,
                                    toClose: true,
                                    mask: false,
                                    class: false
                                });




                            } else {


                                pop.confirm({
                                    title: "提示",
                                    sizeAdapt: false,
                                    content: "请确定是否切换到集控模式",
                                    button: [
                                        ["success", "确定",
                                            function (e) {
                                                pop.close(e)
                                                window.selfcontrolplan = false
                                                let cell = parkequip['集控模式']
                                                let light = cell.getSubCell('button')[0]
                                                nc.setFillColor(light, '#ffd966')
                                                light = cell.getSubCell('light')[0]
                                                nc.setFillColor(light, '#0f0')

                                                let cell2 = parkequip['自控模式']
                                                let light2 = cell2.getSubCell('button')[0]
                                                nc.setFillColor(light2, '#ffd966')
                                                light2 = cell2.getSubCell('light')[0]
                                                nc.setFillColor(light2, '#000')
                                            }
                                        ],
                                        ["default", "取消",
                                            function (e) {
                                                pop.close(e)
                                            }
                                        ]
                                    ],
                                    buttonSpcl: "",
                                    anim: "fadeIn-zoom",
                                    width: 450,
                                    height: 180,
                                    id: "random-72160",
                                    place: 5,
                                    drag: true,
                                    index: true,
                                    toClose: true,
                                    mask: false,
                                    class: false
                                });



                            }


                        }

                    }

                    if (getEquipCell(evt.sourceState.cell).value.getAttribute('type') == 'BTN') {

                        //获取btntype
                        if (getEquipCell(evt.sourceState.cell).getAttribute('btntype') == 'confirm') {


                            pop.confirm({
                                title: "提示",
                                sizeAdapt: false,
                                content: getEquipCell(evt.sourceState.cell).equipstatus.light == 0 ? "请确定是否按下按钮！" : "请确定是否抬起按钮！",
                                button: [
                                    ["success", "确定",
                                        function (e) {
                                            pop.close(e)
                                            window.graphAction.buttonClick({
                                                cell: getEquipCell(evt.sourceState.cell),
                                            }, {
                                                type: 'BTN',
                                                uindex
                                            }, evt.evt)
                                        }
                                    ],
                                    ["default", "取消",
                                        function (e) {
                                            pop.close(e)
                                        }
                                    ]
                                ],
                                buttonSpcl: "",
                                anim: "fadeIn-zoom",
                                width: 450,
                                height: 180,
                                id: "random-72160",
                                place: 5,
                                drag: true,
                                index: true,
                                toClose: true,
                                mask: false,
                                class: false
                            });

                        }
                        if (getEquipCell(evt.sourceState.cell).getAttribute('btntype') == 'password') {

                            //调出键盘
                            ikeyboard.options.position.of = evt.evt
                            ikeyboard.reveal().insertText('')
                            window.graphAction.status = 110
                            window.graphActionCallback = i => {
                                window.graphAction.status = 0
                                window.graphAction.buttonClick({
                                    cell: getEquipCell(evt.sourceState.cell),
                                }, {
                                    type: 'BTN',
                                    uindex
                                }, evt.evt)
                                window.graphActionCallback = null
                            }
                            return

                        }



                    }


                    if (evt.sourceState.cell.value.getAttribute) {
                        if (evt.sourceState.cell.value.getAttribute('name') == 'fork') {

                            getEquipCell(evt.sourceState.cell).getSubCell('button').map(l => {
                                if (l.value.getAttribute('type').toUpperCase() == evt.sourceState.cell.value.getAttribute('type').toUpperCase()) {
                                    uindex = equipcellindex[l.id]
                                }
                            })

                        }

                        if (evt.sourceState.cell.value.getAttribute('name') == 'boundary') {
                            getEquipCell(evt.sourceState.cell).getSubCell('light').map(l => {
                                if (l.value && l.value.getAttribute('type').toUpperCase() == evt.sourceState.cell.value.getAttribute('type').toUpperCase()) {
                                    uindex = equipcellindex[l.id]
                                }
                            })
                        }
                    }

                    window.graphAction.buttonClick({
                        cell: getEquipCell(evt.sourceState.cell),
                        type: getEquipCell(evt.sourceState.cell).getAttribute('type')
                    }, {
                        name: evt.sourceState.cell.getAttribute('name'),
                        uindex,
                        type: evt.sourceState.cell.getAttribute('type')
                    }, evt.evt)
                }

                // 如果是道岔区段和道岔
                let belongsectors = false,
                    cqid = 0
                for (let i in window.switchbelongsector) {
                    if (window.switchbelongsector[i].includes(Number(getCellUid(evt.sourceState.cell)))) {
                        belongsectors = true
                        cqid = i
                        break
                    }
                }



                if (belongsectors) {

                    let cqindex

                    equipindex.map(s => {
                        let index = s.split(' = ')[0]
                        let name = s.split(' = ')[1]
                        let ty = s.split(' = ')[2]

                        if (name == cqid) {
                            cqindex = index
                        }
                    })
                    window.graphAction.buttonClick({
                        cell: getEquipCell(evt.sourceState.cell),
                        type: 'cq'
                    }, {
                        name: evt.sourceState.cell.getAttribute('name'),
                        uindex: cqindex,
                        type: evt.sourceState.cell.getAttribute('type')
                    }, evt.evt)
                } else if (evt.sourceState.cell.getAttribute('belongsector')) {


                    let cqindex

                    equipindex.map(s => {
                        let index = s.split(' = ')[0]
                        let name = s.split(' = ')[1]
                        let ty = s.split(' = ')[2]

                        if (name.toLowerCase() == evt.sourceState.cell.getAttribute('belongsector').toLowerCase()) {
                            cqindex = index
                        }
                    })

                    window.graphAction.buttonClick({
                        cell: getEquipCell(evt.sourceState.cell),
                        type: 'cq'
                    }, {
                        name: evt.sourceState.cell.getAttribute('name'),
                        uindex: cqindex,
                        type: evt.sourceState.cell.getAttribute('type')
                    }, evt.evt)
                }





            }
            mxLog.debug('mouseDown');
        },
        mouseMove: function (sender, evt) {
            mxLog.debug('mouseMove');
        },
        mouseUp: function (sender, evt) {

            mxLog.debug('mouseUp');
        }
    })


    window.graph.refresh()
    //xml加载完成

    window.document_load_ready()

    //滚动视图到中心

    window.graph.center()



    //添加拖拽图标的放下逻辑

    let dragcallback = function (graph, evt, cell, x, y) {
        if (!this.findtargetcell) return
        let equipcell = window.getEquipCell(this.findtargetcell),
            busytype = Number(this.element.dataset.type),
            popid = 'random' + Math.round(Math.random() * 1000)

        //判断是否可以放下
        if (!equipcell || !equipcell.value.getAttribute('type')) {
            return
        }
        let equiptype = equipcell.value.getAttribute('type').toLowerCase()
        if (!['wc', 'gd'].includes(equiptype)) {
            return
        }

        if (!equipcell.busytypes) {
            equipcell.busytypes = {}
        }
        if (!equipcell.busytypes[busytype]) {

            //确认放下的回调
            callback = () => {
                pop.close(popid)

                //如果放置位置是wc
                if (equiptype == 'wc') {
                    equipcell.busytypes[busytype] = true

                    //放置图标到roadlabel上
                    let doms = $(equipcell.getSubCell('road')[0].value.getAttribute('label'))
                    if (doms.length == 0) {
                        doms = $(`<div class='trainvessel trainvesselbusy'></div>`)
                    }
                    doms.append($(`<img class='placedbusyicon busytype-${busytype}' style='width:30px; height:30px;' src="${this.element.src}" >`))
                    graph.setAttributeForCell(equipcell.getSubCell('road')[0], 'label', `<div class='trainvessel'>${doms.html()}</div>`)
                }

            }

            //把状态放到equip上

            //弹出确认弹出框
            switch (busytype) {
                case 1:
                    pop.confirm({
                        title: "接触网送电",
                        sizeAdapt: false,
                        content: "请确定是否继续操作",
                        button: [
                            ["success", "确定",
                                callback
                            ],
                            ["default", "取消",
                                function (e) {
                                    pop.close(e)
                                }
                            ]
                        ],
                        buttonSpcl: "",
                        anim: "fadeIn-zoom",
                        width: 350,
                        height: 180,
                        id: popid,
                        place: 5,
                        drag: true,
                        index: true,
                        toClose: false,
                        mask: false,
                        class: false
                    });
                    break
                case 2:
                    pop.confirm({
                        title: "接触网断电",
                        sizeAdapt: false,
                        content: "请确定是否继续操作",
                        button: [
                            ["success", "确定",
                                callback
                            ],
                            ["default", "取消",
                                function (e) {
                                    pop.close(e)
                                }
                            ]
                        ],
                        buttonSpcl: "",
                        anim: "fadeIn-zoom",
                        width: 350,
                        height: 180,
                        id: popid,
                        place: 5,
                        drag: true,
                        index: true,
                        toClose: false,
                        mask: false,
                        class: false
                    });
                    break
            }
        }




    }

    //初始化占线板图标的拖拽
    mxUtils.makeDraggable(document.querySelector('#dragicons img:nth-child(1)'), window.graph, dragcallback, document.querySelector('#dragicons img:nth-child(1)').cloneNode(), -15, -15, false, false, true);
    mxUtils.makeDraggable(document.querySelector('#dragicons img:nth-child(2)'), window.graph, dragcallback, document.querySelector('#dragicons img:nth-child(2)').cloneNode(), -15, -15, false, false, true);

    /**
    setTimeout(() => {

        window.shunttrainvue.resolvetrainplan([{
            'id': 123,
            "start_time": Date.now() + 20000,
            "start": "21AG",
            "end": "T1714G",
            "type": "发车",
            "status": "发车",
            "executory": null,
            "instruct": [{
                "type": "发车",
                "id": 228,
                "status": 0,
                "start_pos": "21AG",
                "end_pos": "T1710G",
                "section": "55-59DG,51-53DG,21/51WG,21DG,15-17DG,11DG,T1714G,T1710G",
                "now_press_btn": "X21LA SCZALA"
            }]
        }, {
            'id': 1243,
            "start_time": Date.now() + 20000,
            "start": "20G",
            "end": "26AG",
            "type": "调车",
            "status": "调车",
            "executory": null,
            "instruct": [{
                    "type": "调车",
                    "id": 2287,
                    "status": 0,
                    "start_pos": "20G",
                    "end_pos": "D7G",
                    "section": "61DG,23/61WG,23DG,9/23WG,9DG,D7G",
                    "now_press_btn": "D35DA D7DA"
                },
                {
                    "type": "调车",
                    "id": 229,
                    "status": 0,
                    "start_pos": "D7G",
                    "end_pos": "26AG",
                    "section": "9DG,15-17DG,21DG,21/51WG,51-53DG,26AG",
                    "now_press_btn": "D7DA X26DA"
                }
            ]
        }])


    }, 1000);

 */

}, function () {
    document.body.innerHTML =
        '<center style="margin-top:10%;">Error loading resource files. Please check browser console.</center>';
});








//keyboard插件初始化
$('#graphactionhidden')
    .keyboard({
        layout: 'qwerty',
        position: {
            of: $('#graphactionhidden'),
            my: 'center top',
            at: 'center top'
        }
    })
    .addTyping();
window.ikeyboard = $('#graphactionhidden').getkeyboard()
$('.ui-keyboard-input').bind('visible hidden beforeClose accepted canceled restricted', function (e, keyboard, el, status) {
    switch (e.type) {
        case 'visible':
            $('.covergraph').show()
            break;
        case 'hidden':
            $('.covergraph').hide()
            break;
        case 'accepted':
            //把点击按钮和部件发送给graphAction处理
            if (window.ikeyboard.getValue() == '123') {

                switch (window.graphAction.status) {
                    case 3:
                        window.graphAction.buttonClick('confirmya')
                        break
                    case 5:
                        window.graphActionCallback()
                        break
                    case 12:
                        window.graphActionCallback()
                        break
                    case 13:
                        window.graphActionCallback()
                        break
                    case 14:
                        window.graphActionCallback()
                        break
                    case 110:
                        window.graphActionCallback()
                        break
                }

            } else {
                window.graphAction.resetStatus()
            }
            break;
        case 'canceled':
            window.graphAction.resetStatus()
            break;
        case 'restricted':
            break;
        case 'beforeClose':
            break;
    }
    $('#graphactionhidden').val('')
});
//底部功能按钮事件处理
$('#graphactionbtn button.actionlevelone').click(function () {
    switch ($(this).index()) {
        case 1:
            //引导总锁
            window.graphAction.buttonClick('alllock')
            break
        case 2:
            //总取消
            window.graphAction.buttonClick('allcancel')
            break
        case 3:
            //取消引导进路
            window.graphAction.buttonClick('allrelieve')
            break
        case 4:
            //区段故障解锁
            window.graphAction.buttonClick('sectorfaultunlock')
            break
        case 5:
            //道岔总定
            window.graphAction.buttonClick('switchdirect')
            break
        case 6:
            //道岔总反
            window.graphAction.buttonClick('switchreverse')
            break
        case 7:
            //清除
            window.graphAction.buttonClick('clearaction')
            break
        case 8:
            //道岔单锁
            window.graphAction.buttonClick('switchlock')
            break
        case 9:
            //道岔解锁
            window.graphAction.buttonClick('switchunlock')
            break
        case 10:
            //道岔解锁
            window.graphAction.buttonClick('signalblock')
            break
        case 11:
            //道岔解锁
            window.graphAction.buttonClick('signalunblock')
            break
        case 12:
            //道岔单封
            window.graphAction.buttonClick('switchblock')
            break
        case 13:
            //道岔解封
            window.graphAction.buttonClick('switchunblock')
            break



    }
})

//辅助菜单js
$('#graphactionbtnsub1>button').on('click', function () {
    $('#graphactionbtnsub1').toggle()
})
$('.assistmenulevel1').on('click', function () {
    $('#graphactionbtnsub1').show()
})
$('.outassistmenu').on('click', function () {
    $('#graphactionbtnsub1').hide()
})


$('.assistbut0').on('mouseenter', function () {
    $('#graphactionbtnsub2').show()
})
$('.assistbut0').on('mouseleave', function () {
    $('#graphactionbtnsub2').hide()
})

$('.supplyelectric').on('click', function () {
    window.open("/electric.html")
})
$('.currenttrain').on('click', function () {
    window.open("/currenttrain.html")
})



$('.assistbut01').on('mouseenter', function () {
    $('#graphactionbtnsub2').show()
    $('#graphactionbtnsub3').show()
    $('#graphactionbtnsub4').hide()
})

$('.assistbut02').on('mouseenter', function () {
    $('#graphactionbtnsub2').show()
    $('#graphactionbtnsub3').hide()
    $('#graphactionbtnsub4').show()

})

$('#graphactionbtnsub4').on('mouseleave', function () {
    $('#graphactionbtnsub2').hide()
})
$('#graphactionbtnsub3').on('mouseleave', function () {
    $('#graphactionbtnsub2').hide()
})
$('#graphactionbtnsub4').on('click', function () {
    $('#graphactionbtnsub2').hide()
})
$('#graphactionbtnsub3').on('click', function () {
    $('#graphactionbtnsub2').hide()
})



let triggelalarmplane = 0
$('.triggeralarmplane').on('click', function (e) {
    if (triggelalarmplane == 0) {
        $('.triggeralarmplane').html('报警窗口显示')
        triggelalarmplane = 1
    } else {
        $('.triggeralarmplane').html('报警窗口隐藏')
        triggelalarmplane = 0
    }
    $('.alarmplane').toggle()
})

let radiopausekey = 0
$('.radiopause').on('click', function (e) {
    if (radiopausekey == 0) {
        //暂停语音
        $('.radiopause').html('开启语音')
        radiopausekey = 1
    } else {
        //开启语音
        $('.radiopause').html('暂停语音')
        radiopausekey = 0
    }
})

window.lightbeltkey = 0
$('.lightbelt').on('click', function (e) {
    if (lightbeltkey == 0) {
        //15秒后解除
        setTimeout(() => {
            lightbeltkey = 0
            //恢复显示
            refreshturnou()
        }, 15000);
        lightbeltkey = 1
        refreshturnou()
    }
})

window.turnoutnamekey = 0
$('.turnoutname').on('click', function (e) {

    if (turnoutnamekey == 0) {
        //暂停语音
        $('.turnoutname').html('道岔名称显示')
        turnoutnamekey = 1
    } else {
        //开启语音
        $('.turnoutname').html('道岔名称隐藏')
        turnoutnamekey = 0
    }
    refreshturnou()

})

let turnoutsectionkey = 0
$('.turnoutsection').on('click', function (e) {
    if (turnoutsectionkey == 0) {
        //暂停语音
        $('.turnoutsection').html('道岔区段名称隐藏')
        turnoutsectionkey = 1
    } else {
        //开启语音
        $('.turnoutsection').html('道岔区段名称显示')
        turnoutsectionkey = 0
    }

    let controlgraph = new graphx()
    let model = graph.getModel()
    window.globalupdata = true
    model.beginUpdate()
    //在区故解时显示全部区段
    Object.keys(window.switchbelongsector).map(k => {
        let c = window.parkequip[k.toLowerCase()]
        if (c) {
            window.graph.model.setVisible(c, turnoutsectionkey)
        }
    })
    model.endUpdate()
    window.globalupdata = false
})

window.sigalnametogglekey = 0
$('.sigalnametoggle').on('click', function (e) {
    if (sigalnametogglekey == 0) {
        $('.sigalnametoggle').html('信号名称显示')
        sigalnametogglekey = 1
    } else {
        $('.sigalnametoggle').html('信号名称隐藏')
        sigalnametogglekey = 0
    }

    refreshsingalsignal()

})

window.refreshsingalsignal = () => {
    //刷新显示信号机
    let controlgraph = new graphx()
    let model = graph.getModel()
    window.globalupdata = true
    model.beginUpdate()
    for (let i in parkequip) {
        if (parkequip[i].equipstatus && (parkequip[i].equipstatus.type == 3 || parkequip[i].equipstatus.type == 4 || parkequip[i].equipstatus.type == 5)) {
            controlgraph.setSignalStatus(parkequip[i].equipstatus.name, parkequip[i].equipstatus)
        }
    }
    model.endUpdate()
    window.globalupdata = false
}

window.refreshturnou = () => {
    //刷新显示道岔
    let controlgraph = new graphx()
    let model = graph.getModel()
    window.globalupdata = true
    model.beginUpdate()
    for (let i in parkequip) {
        if (parkequip[i].equipstatus && parkequip[i].equipstatus.type == 1) {
            controlgraph.setTurnoutStatus(parkequip[i].equipstatus.name, parkequip[i].equipstatus)
        }
    }
    model.endUpdate()
    window.globalupdata = false
}


let withoutturnoutsectionkey = 0
$('.withoutturnoutsection').on('click', function (e) {
    if (withoutturnoutsectionkey == 0) {
        //暂停语音
        $('.withoutturnoutsection').html('无岔区段名称显示')
        withoutturnoutsectionkey = 1
    } else {
        //开启语音
        $('.withoutturnoutsection').html('无岔区段名称隐藏')
        withoutturnoutsectionkey = 0
    }
    //刷新显示道岔
    let controlgraph = new graphx()
    let model = graph.getModel()
    window.globalupdata = true
    model.beginUpdate()
    for (let i in parkequip) {
        if (parkequip[i].equipstatus && parkequip[i].equipstatus.type == 2) {
            controlgraph.setSectorStatus(parkequip[i].equipstatus.name, parkequip[i].equipstatus)
        }
    }
    model.endUpdate()
    window.globalupdata = false
})

window.turnouttogglekey = 0
$('.turnouttoggle').on('click', function (e) {
    if (turnouttogglekey == 0) {
        $('.turnouttoggle').html('道岔位置显示')
        turnouttogglekey = 1
    } else {
        $('.turnouttoggle').html('道岔位置隐藏')
        turnouttogglekey = 0
    }

    refreshturnou()

})

$('.pofengstatistic').on('click', function (e) {
    pop.alert({
        title: "破封统计",
        content: `
        <p>11111</p>
        <p>11111</p>
        <p>11111</p>
        <p>11111</p>
        <p>11111</p>
        `,
        button: ["primary", "确定", function (e) {
            pop.close(e)
        }],
        buttonSpcl: "",
        sizeAdapt: false,
        anim: "fadeIn-zoom",
        width: 450,
        height: 200,
        id: "random-70032",
        place: 5,
        drag: true,
        index: true,
        toClose: true,
        mask: false,
        class: false
    });
})

//占线板右键移除
$('body').on('click', '.placedbusyicon', function (e) {

    if (3 == e.which) {
        alert('这是右键单击事件');
    } else if (1 == e.which) {
        alert('这是左键单击事件');
    }
})

$('.busywire').on('click', function (e) {
    if (e.target.innerText == '占线板') {
        $('#dragicons').show()
        setTimeout(() => {
            $('.placedbusyicon').css({
                'visibility': 'unset'
            })
        }, 10);
        e.target.innerText = '关占线板'

    } else {
        $('#dragicons').hide()
        setTimeout(() => {
            $('.placedbusyicon').css({
                'visibility': 'hidden'
            })
        }, 10);
        e.target.innerText = '占线板'
    }

})

$('.triggertrain').on('click', function (e) {
    if (e.target.innerText == '显示列车') {
        window.showvessel = true
        setTimeout(() => {
            $('.trainvesseltrain').css({
                'visibility': 'unset'
            })
        }, 10);
        let model = graph.getModel()
        window.globalupdata = true
        model.beginUpdate()
        for (let ind in parkequipvessel) {
            vessel = parkequipvessel[ind]
            window.graph.orderCells(0, [vessel])
        }
        model.endUpdate()
        window.globalupdata = false
        e.target.innerText = '隐藏列车'

    } else {
        window.showvessel = false
        setTimeout(() => {
            $('.trainvesseltrain').css({
                'visibility': 'hidden'
            })
        }, 10);
        let model = graph.getModel()
        window.globalupdata = true
        model.beginUpdate()
        for (let ind in parkequipvessel) {
            vessel = parkequipvessel[ind]
            window.graph.orderCells(1, [vessel])
        }
        model.endUpdate()
        window.globalupdata = false
        e.target.innerText = '显示列车'
    }

})





$('.assistbutshunttrain').on('click', function () {
    $('.shunttrain').css({
        'z-index': 999
    })
})
let ishunttrainTdrag = setInterval(() => {
    if ($(".shunttrain").Tdrag) {
        $(".shunttrain").Tdrag();
        clearInterval(ishunttrainTdrag)
    }
}, 100);



/**
 * 
 * window.mdiadcontrol == true
 * window.selfcontrolplan == true
 * window.automaticcontrolplan == true
 * 如果集控模式则隐藏调车列表按钮
 * 如果手动模式则点击排列进路确定后发送进路
 * 弹出倒计时框触发进路
 * 
 * 接车计划）
 * 收到ats车到转换轨则触发
 * 发车计划）
 * 倒计时发车
 * 调车车计划）
 * 倒计时发车
 * 所有计划完成后都会取一条挂起列表中的计划
 */
//初始化vue


$('.planexecutemode0').on('click', function (e) {
    window.automaticcontrolplan = false
})

$('.planexecutemode1').on('click', function (e) {
    window.automaticcontrolplan = true
})

//定时器列表
window.planTimeout = []
//监控元件列表
window.equipstatuslisten = []
//注册Vue全局属性
if (!window.cefQuery) {
    window.cefQuery = i => {}
}
Vue.prototype.$moment = moment
window.shunttrainvue = new Vue({
    el: '.shunttrain',
    data: {
        solvedtableDatadepart: [],
        solvedtableDatashunt: []
    },

    methods: {

        /**
         * 
         * 计划列表变化后触发，为新进的计划添加倒计时
         * 转换轨触发的，则添加到转换轨触发列表
         * 挂起计划添加到挂起列表，当前计划执行完毕后，取出挂起列表中最前一条执行
         * 
         * 
         */

        //分解新计划

        resolvetrainplan(newplan) {
            console.info('%c添加计划:', 'font-size:25px;color:red;', newplan)
            //遍历当前倒计时列表中的是否有这条计划，如果有查看时间是否变更
            newplan.map(np => {
                let hasplan = planTimeout.find(x => x.planid == np.id)
                if (hasplan) {
                    console.info('%c已存在计划列表中：', 'font-size:25px;color:red;', hasplan)
                    //删除已有回调和列表中数据
                    planTimeout = planTimeout.filter(x => {
                        clearTimeout(x.timeid)
                        return x.planid != np.id
                    })
                    this.solvedtableDatadepart = this.solvedtableDatadepart.filter(x => {
                        return x.id != np.id
                    })
                    this.solvedtableDatashunt = this.solvedtableDatashunt.filter(x => {
                        return x.id != np.id
                    })


                }
                //提前时间
                let aheadtime = 1000
                /**
                 * 处理新的发车计划
                 */
                if (np.type == '发车') {
                    //添加计划到计划列表
                    this.solvedtableDatadepart = this.solvedtableDatadepart.concat([np])
                }

                /**
                 * 处理调车计划
                 * 
                 */

                if (np.type == '调车') {
                    //添加计划到计划列表
                    this.solvedtableDatashunt = this.solvedtableDatashunt.concat([np])
                }

                //添加定时器，定时器id添加到定时器列表
                //计划执行时间提前xx毫秒-当前毫秒

                if (np.start_time > 0) {
                    let countdown = np.start_time - aheadtime - Date.now()
                    let timeid = setTimeout(i => {
                        this.executeplan(np.id)
                    }, countdown)
                    console.info('%c添加计划定时器', 'font-size:25px;color:red;', countdown / 1000, np.id)
                    planTimeout.push({
                        planid: np.id,
                        timeid
                    })
                }


            })


        },
        //执行计划
        executeplan(planid) {
            console.info('%c执行计划', 'font-size:25px;color:red;', planid)
            //更新定时器列表
            planTimeout = planTimeout.filter(x => {
                return x.planid != planid
            })

            //获取计划
            let plan = this.solvedtableDatadepart.find(x => {
                return x.id == planid
            })
            if (!plan) {
                plan = this.solvedtableDatashunt.find(x => {
                    return x.id == planid
                })
            }

            plan = JSON.parse(JSON.stringify(plan))
            //发送第一条命令并且链式运行下一条
            let applyinstruct = () => {
                let instruct = plan.instruct.shift()
                if (instruct) {
                    let resolvedi = instruct.now_press_btn.split(' ').map(x => {
                        return {
                            equip: x.slice(0, -2),
                            type: x.slice(-2, x.length)
                        }
                    })
                    //找出按钮的index
                    let btnindex1 = equipcellindex[parkequip[resolvedi[0].equip].getSubCell('button').concat(parkequip[resolvedi[0].equip].getSubCell('light')).find(b => String(b.getAttribute('type')).toUpperCase() == resolvedi[0].type).id]
                    let btnindex2 = equipcellindex[parkequip[resolvedi[1].equip].getSubCell('button').concat(parkequip[resolvedi[1].equip].getSubCell('light')).find(b => String(b.getAttribute('type')).toUpperCase() == resolvedi[0].type).id]

                    let clickPath = [{
                        index: Number(btnindex1),
                        name: resolvedi[0].equip
                    }, {
                        index: Number(btnindex2),
                        name: resolvedi[1].equip
                    }]


                    this.solvedtableDatadepart = this.solvedtableDatadepart.map(x => {
                        if (x.id == planid) {
                            x.type = '信号未开放'
                        }
                        return x
                    })
                    this.solvedtableDatashunt = this.solvedtableDatashunt.map(x => {
                        if (x.id == planid) {
                            x.type = '信号未开放'
                        }
                        return x
                    })


                    let sendinstruct = () => {
                        if (window.planinstructstamp && Date.now() - window.planinstructstamp < 5000) {
                            setTimeout(sendinstruct, 1000)
                        } else {

                            let cb = issend => {
                                //发出时stamp
                                window.planinstructstamp = Date.now()
                                //只有在selfcontrolplan自控模式才自动发指令
                                if (issend) {
                                    console.info('%c计划指令发送后端', 'font-size:25px;color:red;', {
                                        status: 0x05,
                                        clickPath
                                    })
                                    window.cefQuery({
                                        request: JSON.stringify({
                                            cmd: "commit_action",
                                            data: {
                                                status: 0x05,
                                                clickPath
                                            }
                                        }),
                                        persistent: false,
                                        onSuccess: function (response) {
                                            // def.resolve(response)
                                        },
                                        onFailure: function (error_code, error_message) {
                                            // def.reject(error_message)
                                        }
                                    })
                                }
                            }

                            //自控模式执行监控
                            if (window.selfcontrolplan) {
                                //进路人工模式时需要弹出框回调执行
                                if (window.automaticcontrolplan) {
                                    cb(1)
                                } else {
                                    popShuntTrain(plan, cb)
                                }
                            } else {
                                //集控模式执行监控不发送指令
                                cb(0)
                            }

                        }
                    }
                    sendinstruct()


                    //处理section，找出道岔区段，替换为头部道岔
                    let listens = instruct.section.split(',').map(x => {
                        let equip = x.replace('-', '_').replace('/', '_')

                        if (Object.keys(switchbelongsector).includes(equip)) {
                            //道岔区体会为道岔
                            return String(switchbelongsector[equip][0])
                        } else {
                            return equip
                        }

                    })

                    console.info('%c当前指令需要监听部件：', 'font-size:25px;color:red;', listens)
                    //如果监听区段为道岔区段，取前端道岔
                    //开始监控section的状态变化,监控到完成状态后 删除监控并且触发callback读取instruct

                    /**
                     * 
                     * 以进路的前面除开最后一节的区段状态都出清为监控依据
                     * 
                     */
                    equipstatuslisten.push({
                        id: instruct.id,
                        planid,
                        type: instruct.type,
                        progress: 0,
                        now_press_btn: instruct.now_press_btn.split(' ')[0].slice(0, -2),
                        instructid: instruct.id,
                        states: listens.map(x => {
                            return {
                                uid: x,
                                state: 0
                            }
                        }),
                        callback: applyinstruct
                    })



                } else {
                    //已经执行完毕了
                    console.info('%c当前计划执行完毕', 'font-size:25px;color:red;', planid)
                    //更新列表

                    this.solvedtableDatadepart = this.solvedtableDatadepart.map(x => {
                        if (x.id == planid) {
                            x.type = '已完成'
                        }
                        return x
                    })
                    this.solvedtableDatashunt = this.solvedtableDatashunt.map(x => {
                        if (x.id == planid) {
                            x.type = '已完成'
                        }
                        return x
                    })
                }
            }

            applyinstruct()



        },
        arrange(scope) {
            console.log(scope.row)
        },
        cancel(scope) {
            console.log(scope.row)
        },
        shunt(command) {
            console.log(command)
        }
    },
})

//设备监控计划执行进度
window.selfcontrolplan = true
window.changeplanprogress = (uid, status) => {

    equipstatuslisten.map(x => {
        return !!x.states.map(y => {
            if (y.uid == uid.toUpperCase() || x.now_press_btn == uid.toUpperCase()) {
                //更新监听列表的部件状态状态
                if (x.progress) {
                    switch (y.state) {
                        case 0:
                            if (status.hold == 1) {
                                y.state = 2
                            }
                            if (status.hold == 0 && status.lock == 0 && x.states.filter((xx, xi) => xi < x.states.length - 1).every(z => z.state > 0)) {
                                /**
                                 * 白光带变空闲，表示取消当前进路指令
                                 * 当前指令挂起，后续人工继续执行
                                 */
                                console.info('%c恢复信号未开放：', 'font-size:25px;color:red;', x)
                                y.state = 0
                                x.progress = 0
                                window.shunttrainvue.solvedtableDatadepart = window.shunttrainvue.solvedtableDatadepart.map(z => {
                                    if (z.id == x.planid) {
                                        z.type = '信号未开放'
                                    }
                                    return z
                                })
                                window.shunttrainvue.solvedtableDatashunt = window.shunttrainvue.solvedtableDatashunt.map(z => {
                                    if (z.id == x.planid) {
                                        z.type = '信号未开放'
                                    }
                                    return z
                                })
                            }
                            break
                        case 2:
                            if (status.hold == 0 && status.lock == 0) {
                                y.state = 3
                            }
                            break
                    }
                }

                //是否亮灯 
                let lighted = (status.yellow && (x.type == '发车' || x.type == '收车')) || (status.white && x.type == '调车')
                if (lighted && !x.progress) {

                    //变更计划状态执行中
                    x.progress = 1

                    window.shunttrainvue.solvedtableDatadepart = window.shunttrainvue.solvedtableDatadepart.map(z => {
                        if (z.id == x.planid) {
                            let findcurrentinstruct = z.instruct.find(y => y.id == x.id)
                            z.type = '执行中'
                            z.executory = findcurrentinstruct.start_pos + '—' + findcurrentinstruct.end_pos
                        }
                        return z
                    })
                    window.shunttrainvue.solvedtableDatashunt = window.shunttrainvue.solvedtableDatashunt.map(z => {
                        if (z.id == x.planid) {
                            let findcurrentinstruct = z.instruct.find(y => y.id == x.id)
                            z.type = '执行中'
                            z.executory = findcurrentinstruct.start_pos + '—' + findcurrentinstruct.end_pos
                        }
                        return z
                    })
                }
                if (!lighted && x.progress && x.states.every(x => x.state < 2)) {

                    console.info('%c恢复信号未开放：', 'font-size:25px;color:red;', x)
                    y.state = 0
                    x.progress = 0
                    window.shunttrainvue.solvedtableDatadepart = window.shunttrainvue.solvedtableDatadepart.map(z => {
                        if (z.id == x.planid) {
                            z.type = '信号未开放'
                        }
                        return z
                    })
                    window.shunttrainvue.solvedtableDatashunt = window.shunttrainvue.solvedtableDatashunt.map(z => {
                        if (z.id == x.planid) {
                            z.type = '信号未开放'
                        }
                        return z
                    })
                }


                if (x.states.filter((xx, xi) => xi < x.states.length - 1).every(z => z.state > 2) && x.progress) {
                    console.info('%c指令执行完毕：', 'font-size:25px;color:red;', x)
                    //更新监听，去除已经完成的监听
                    equipstatuslisten = equipstatuslisten.filter(z => {
                        return z.planid != x.planid
                    })

                    window.shunttrainvue.solvedtableDatadepart = window.shunttrainvue.solvedtableDatadepart.map(z => {
                        if (z.id == x.planid) {
                            z.instruct = z.instruct.map(c => {
                                if (c.id == x.id) {
                                    c.status = 1
                                }
                                return c
                            })
                        }
                        return z
                    })
                    window.shunttrainvue.solvedtableDatashunt = window.shunttrainvue.solvedtableDatashunt.map(z => {
                        if (z.id == x.planid) {
                            z.instruct = z.instruct.map(c => {
                                if (c.id == x.id) {
                                    c.status = 1
                                }
                                return c
                            })
                        }
                        return z
                    })


                    //执行下一条指令
                    x.callback()

                }


                return true
            } else {
                return false
            }
        })
    })
}

//调车弹出层
//pop的倒计时确认
window.popShuntTrain = (plan, cb) => {

    let popid = 'random' + Math.round(Math.random() * 1000)
    let timecountdown = 10
    let popidinterval = setInterval(() => {
        timecountdown--
        $(`#${popid} .pop-button[type=success]`).html(`确定（${timecountdown}）`)
        if (timecountdown == 0) {
            clearInterval(popidinterval)
            pop.close(popid)
            //执行调车
            shunttrainpopcallback()
        }
    }, 1000);

    let shunttrainpopcallback = () => {
        clearInterval(popidinterval)
        //确认调车
        pop.close(popid)
        cb(1)
    }
    let shunttrainpopcancel = () => {
        clearInterval(popidinterval)
        //取消执行
        cb(0)
    }

    pop.alert({
        title: "提醒",
        content: `${plan.status}计划等待执行，${plan.start}——${plan.end}`,
        button: [
            ["success", "确定（10）",
                shunttrainpopcallback
            ],
            ["default", "取消执行",
                function (e) {
                    shunttrainpopcancel()
                    pop.close(e)
                }
            ]
        ],
        buttonSpcl: "",
        sizeAdapt: false,
        anim: "slide-bottom",
        width: 450,
        height: 200,
        id: popid,
        place: 9,
        drag: true,
        index: true,
        mask: false,
        class: false
    });
}
//右键菜单配置
$(document).ready(function () {
    context.init({
        preventDoubleContext: false
    });
    //给不同占线右键添加action
    context.attach('.busytype-2', [{
        text: '移除',
        action: function (e) {
            e.preventDefault()
            if (window.busytypedata) {
                let uid = window.busytypedata
                //去掉cell的label中的图标还有cell的状态
                parkequip[uid].busytypes['2'] = false
                let jdom = $(parkequip[uid].getSubCell('road')[0].value.getAttribute('label'))
                jdom.find('.busytype-2').remove()
                graph.setAttributeForCell(parkequip[uid].getSubCell('road')[0], 'label', `<div class='trainvessel'>${jdom.html()}</div>`)

            }

        }
    }]);
    context.attach('.busytype-1', [{
        text: '移除',
        action: function (e) {
            e.preventDefault()
            if (window.busytypedata) {
                let uid = window.busytypedata
                //去掉cell的label中的图标还有cell的状态
                parkequip[uid].busytypes['1'] = false
                let jdom = $(parkequip[uid].getSubCell('road')[0].value.getAttribute('label'))
                jdom.find('.busytype-1').remove()
                graph.setAttributeForCell(parkequip[uid].getSubCell('road')[0], 'label', `<div class='trainvessel'>${jdom.html()}</div>`)

            }

        }
    }]);

    $(document).on('mouseover', '.me-codesta', function () {
        $('.finale h1:first').css({
            opacity: 0
        });
        $('.finale h1:last').css({
            opacity: 1
        });
    });
    $(document).on('mouseout', '.me-codesta', function () {
        $('.finale h1:last').css({
            opacity: 0
        });
        $('.finale h1:first').css({
            opacity: 1
        });
    });

    $('#firnode').on('mouseover', x => {
        $('#alarmwarninglist').show()
    })
    $('#firnode').on('mouseout', x => {
        $('#alarmwarninglist').hide()
    })
    $('#alarmwarninglist').on('mouseout', x => {
        $('#alarmwarninglist').hide()
    })
    $('#alarmwarninglist').on('mouseover', x => {
        $('#alarmwarninglist').show()
    })
});
//火车不可移动
window.istrainmovable = false

window.alarmwarninglistadd = s => {
    if ($('#alarmwarninglist p').length < 10) {} else {
        $('#alarmwarninglist p:first-child').remove()
    }
    $('#alarmwarninglist').append(`<p>${s}</p>`)
    $('#firnode span').html(s)
    document.querySelector('#alarmwarninglist').scrollTop = 10000
}

window.blockout = () => {
    window.sysblackout = true
    $('head').append($(`<style id='blackoutgrays'>
    .geDiagramContainer {
        filter: grayscale(100%);
        -webkit-filter: grayscale(100%);
        -moz-filter: grayscale(100%);
        -ms-filter: grayscale(100%);
        -o-filter: grayscale(100%);
        filter: progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);
        -webkit-filter: grayscale(1)
    }
    </style>`))


}
window.blockin = () => {
    window.sysblackout = false
    $('#blackoutgrays').remove()
}