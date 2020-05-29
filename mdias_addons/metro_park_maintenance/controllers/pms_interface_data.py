# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import http
from odoo.http import request, route
from odoo.http import JsonRequest
from odoo.tools import ustr
import json
import datetime
import logging
import requests

_logger = logging.getLogger(__name__)


class PmsInterfaceDate(http.Controller):

    @http.route('/detainVehicle', type='json', auth='public', csrf=False)
    def button_vehicle_info(self, **kwargs):
        '''
        扣车信息
        :param kwargs:
        :return:
        '''
        sys_config = request.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = sys_config.get('start_pms', False)
        if use_pms_maintaince != 'yes':
            return {
                "errorId": "20",
                "errorInfo": "mdias 没有开放pms接口"
            }
        # 故障编号
        fault_code = request.jsonrequest.get('faultCode')
        # 线别
        line_no = request.jsonrequest.get('lineNo')
        # 数据类型
        data_type = request.jsonrequest.get('dataType')
        # 对象编码
        object_code = request.jsonrequest.get('objectCode')
        # 对象名称
        object_name = request.jsonrequest.get('objectName')
        # 扣车状态  "2：扣车；3：扣车关闭；4：扣车作废"
        deduction_order_status = request.jsonrequest.get('deductionOrderStatus')
        train_id = request.env['metro_park_maintenance.train_dev'].sudo().search([('dev_name', '=', object_name)]).id
        if deduction_order_status == '2':
            request.env['metro_park_dispatch.cur_train_manage'].sudo().search([('train', '=', train_id)]).detain = True
            request.env['metro_park_dispatch.cur_train_manage'].sudo().search(
                [('train', '=', train_id)]).train_status = 'detain'
            request.env.cr.commit()
        else:
            request.env['metro_park_dispatch.cur_train_manage'].sudo().search([('train', '=', train_id)]).detain = False
            request.env['metro_park_dispatch.cur_train_manage'].sudo().search(
                [('train', '=', train_id)]).train_status = 'wait'
            request.env.cr.commit()

        return {
            "errorId": "10",
            "errorInfo": "成功"
        }

    @http.route('/vehicleInfo', type='json', auth='public', csrf=False)
    def vehicle_information(self, **kwargs):
        '''
        车辆信息
        :param kwargs:
        :return:
        '''
        sys_config = request.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = sys_config.get('start_pms', False)
        if use_pms_maintaince != 'yes':
            return {
                "errorId": "20",
                "errorInfo": "mdias 没有开放pms接口"
            }
        vehicle_lists = request.jsonrequest.get('vehicleList')
        for vehicle_list in vehicle_lists:
            # 对象编码
            object_code = vehicle_list.get('objectCode')
            # 对象名称
            object_name = vehicle_list.get('objectName')
            # 线别
            line_no = vehicle_list.get('lineNo')
            # 数据类型
            data_type = vehicle_list.get('dataType')
            # 车辆型号
            vehicle_model = vehicle_list.get('vehicleModel')
            # 传入物资编码
            mat_code = vehicle_list.get('matCode')
            if data_type == '3':
                search_object_code = request.env['metro_park_maintenance.train_dev'].sudo().search(
                    [('dev_no', '=', object_name)])
                search_object_code.object_code = ''
            else:
                exist_dev_standard = request.env['metro_park_base.dev_standard'].search([('name', '=', vehicle_model)])
                if not exist_dev_standard and vehicle_model:
                    dev_standard = request.env['metro_park_base.dev_standard'].create({
                        'name': vehicle_model,
                    })
                else:
                    dev_standard = exist_dev_standard
                search_object_code = request.env['metro_park_maintenance.train_dev'].sudo().search(
                    [('object_code', '=', object_code)])
                if search_object_code:
                    for object_code_value in search_object_code:
                        object_code_value.object_code = ''
                request.env['metro_park_maintenance.train_dev'].sudo().search([('dev_no', '=', object_name)]).write({
                    'object_code': object_code,
                    'standard': dev_standard.id,
                    'mat_code': mat_code,
                })
            request.env.cr.commit()

        return {
            "errorId": "10",
            "errorInfo": "成功"
        }

    @http.route('/overhaulOrder', type='json', auth="none", csrf=False)
    def check_list_status(self, **kwargs):
        '''
        检修工单
        :param kwargs:
        :return:
        '''
        sys_config = request.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = sys_config.get('start_pms', False)
        if use_pms_maintaince != 'yes':
            return {
                "errorId": "20",
                "errorInfo": "mdias 没有开放pms接口"
            }
        try:
            for orderList in request.jsonrequest.get('orderList'):
                # 工单编号
                order_code = orderList.get('orderCode')
                # 线别
                line_no = orderList.get('lineNo')
                # 数据类型
                data_type = orderList.get('dataType')
                # 计划标识
                overhaulPlanId = orderList.get('overhaulPlanId')
                # 更新时间
                update_time = orderList.get('updateTime')
                # 对象编码
                object_code = orderList.get('objectCode')
                # 编码名称
                object_name = orderList.get('objectName')
                # 工作状态 1：发布；2：派工；3：开工；4：完工；5：完工确认；6：作废；7：关闭
                work_status = orderList.get('workStatus')
                state_map = {
                    '1': 'assigned',
                    '2': 'accept',
                    '3': 'started',
                    '4': 'finished',
                    '5': 'finish_accept',
                    '6': 'obsolete',
                    '7': 'un_assign',
                }
                if data_type == '1':
                    request.env['metro_park_maintenance.maintaince_order'].sudo().create({
                        'pms_order_no': order_code,
                        'pms_plan_name': object_name,
                        'state': state_map.get(work_status),
                        'pms_plan_no': object_code,
                    })
                    request.env.cr.commit()
                elif data_type == '2':
                    rec = request.env['metro_park_maintenance.maintaince_order'].sudo().search([
                        ('order_no', '=', order_code)])
                    if rec:
                        rec.write({
                            'pms_plan_name': object_name,
                            'state': state_map.get(work_status),
                            'pms_plan_no': object_code,
                        })
                    else:
                        request.env['metro_park_maintenance.maintaince_order'].sudo().create({
                            'pms_order_no': order_code,
                            'pms_plan_name': object_name,
                            'state': state_map.get(work_status),
                            'pms_plan_no': object_code,
                        })
                elif data_type == '3':
                    rec = request.env['metro_park_maintenance.maintaince_order'].sudo().search([
                        ('order_no', '=', order_code)])
                    if rec:
                        rec.unlink()
            return {
                "errorId": "10",
                "errorInfo": "成功"
            }
        except Exception as e:
            return {
                "errorId": "20",
                "errorInfo": "失败{}".format(str(e))
            }

    @http.route('/faultOrder', type='json', auth='public', csrf=False)
    def break_list_status(self, **kwargs):
        '''
        故障工单信息
        :param kwargs:
        :return:
        '''
        try:
            # 判断是否使用PMS的接口
            sys_config = request.env['metro_park_base.system_config'].get_configs()
            use_pms_maintaince = sys_config.get('start_pms', False)
            if use_pms_maintaince != 'yes':
                return {
                    "errorId": "20",
                    "errorInfo": "mdias 没有开放pms接口"
                }
            fault_code = request.jsonrequest.get('faultCode')
            # 线别
            line_no = request.jsonrequest.get('lineNo')
            # 数据类型
            data_type = request.jsonrequest.get('dataType')
            # 更新时间
            update_time = request.jsonrequest.get('updateTime')
            # 故障位置代码
            train_structure_code = request.jsonrequest.get('trainStructureCode')
            # 故障位置名称
            train_structure_name = request.jsonrequest.get('trainStructureName')
            # 故障现象
            fault_describe = request.jsonrequest.get('faultDescribe')
            # 对象编码
            object_code = request.jsonrequest.get('objectCode')
            # 对象名称
            object_name = request.jsonrequest.get('objectName')
            # 故障信息只有关闭
            # 工作状态 0：发布；3：派工；4：开工；5：完工；6：完工确认；9：作废；8：关闭
            workStatus = request.jsonrequest.get('workStatus')
            train_id = request.env['metro_park_maintenance.train_dev'].sudo().search(
                [('dev_name', '=', object_name)]).id
            request.env['metro_park_dispatch.cur_train_manage'].sudo().search(
                [('train', '=', train_id)]).train_status = 'fault'
            request.env.cr.commit()
            return {
                "errorId": "10",
                "errorInfo": "成功"
            }
        except Exception as e:
            return {
                "errorId": "20",
                "errorInfo": "失败{}".format(str(e))
            }

    @http.route('/overhaulSkill', type='json', auth='public', csrf=False)
    def technical_information(self, **kwargs):
        '''
        检技通信息
        :param kwargs:
        :return:
        '''
        try:
            sys_config = request.env['metro_park_base.system_config'].get_configs()
            use_pms_maintaince = sys_config.get('start_pms', False)
            if use_pms_maintaince != 'yes':
                return {
                    "errorId": "20",
                    "errorInfo": "mdias 没有开放pms接口"
                }
            check_tech_info_id = request.jsonrequest.get('checkTechInfoId')
            # 数据类型
            data_type = request.jsonrequest.get('dataType')
            # 检技通号
            check_tech_info_no = request.jsonrequest.get('checkTechInfoNo')
            # 检技通名称
            cti_name = request.jsonrequest.get('ctiName')
            # 检技通内容
            detailed = request.jsonrequest.get('detailed')
            # 针对车辆
            cti_vehicle_no = request.jsonrequest.get('ctiVehicleNo')
            # 开始时间
            cti_begin_date = request.jsonrequest.get('ctiBeginDate')
            # 结束时间
            cti_end_date = request.jsonrequest.get('ctiEndDate')
            # 结合修程
            combine_repair_time = request.jsonrequest.get('combineRepairTime')
            # 属于临时修程还是检技通 1检技通，2临时修程，默认检技通"
            temp_repair_time = request.jsonrequest.get('tempRepairTime')
            dev = []
            for vehicle in cti_vehicle_no.split(','):
                dev_id = request.env['metro_park_maintenance.train_dev'].sudo().search([('dev_name', '=', vehicle)]).id
                if dev_id:
                    dev.append(dev_id)
            # 结合修程
            repair_list = []
            for repair in combine_repair_time.split(','):
                rec_repair = request.env['metro_park_maintenance.repair_rule'].sudo().search([('no', '=', repair)])
                if rec_repair:
                    repair_list.append(rec_repair.id)
            if data_type == '1':
                # 新增
                request.env['metro_park_maintenance.repair_tmp_rule'].sudo().create({
                    'check_tech_info_id': check_tech_info_id,
                    'no': check_tech_info_no,
                    'name': cti_name,
                    'content': detailed,
                    'trains': [(6, 0, dev)],
                    'repair_rules': [(6, 0, repair_list)],
                    'data_source': 'pms',
                    'start_date': cti_begin_date if cti_begin_date else None,
                    'end_date': cti_end_date if cti_end_date else None,
                })
            elif data_type == '2':
                # 修改
                request.env['metro_park_maintenance.repair_tmp_rule'].sudo().search(
                    [('check_tech_info_id', '=', check_tech_info_id)]).write(
                    {
                        'name': cti_name,
                        'content': detailed,
                        'trains': [(6, 0, dev)],
                        'repair_rules': [(6, 0, repair_list)],
                    }
                )
            elif data_type == '3':
                # 删除
                request.env['metro_park_maintenance.repair_tmp_rule'].sudo().search(
                    [
                        ('check_tech_info_id', '=', check_tech_info_id),
                        ('data_source', '=', 'pms'),
                    ]).unlink()
            request.env.cr.commit()
            return {
                "errorId": "10",
                "errorInfo": "成功"
            }
        except Exception as e:
            return {
                "errorId": "20",
                "errorInfo": "失败{}".format(str(e))
            }

    @http.route('/getWorkTeamInfo', type='json', auth='public', csrf=False)
    def get_work_team_info(self, *args):
        '''
        获取组织结构的信息
        :param kwargs:
        :return:
        '''
        if request.jsonrequest.get('workTeamList'):
            try:
                for department in request.jsonrequest.get('workTeamList'):
                    if department.get('dataType') == '1':
                        exist_rec = request.env['pms.department'].search(
                            [('department_no', '=', department.get('sectionCode'))])
                        if not exist_rec:
                            request.env['pms.department'].create({
                                'department': department.get('sectionName'),
                                'department_no': department.get('sectionCode'),
                                'line_no': department.get('lineNo'),
                                'parent_department': department.get('fullName'),
                                'parent_department_no': department.get('parentName'),
                            })
                    elif department.get('dataType') == '2':
                        exist_rec = request.env['pms.department'].search(
                            [('department_no', '=', department.get('sectionCode'))])
                        if exist_rec:
                            exist_rec.write({
                                'department': department.get('sectionName'),
                                'department_no': department.get('sectionCode'),
                                'line_no': department.get('lineNo'),
                                'parent_department': department.get('fullName'),
                                'parent_department_no': department.get('parentName'),
                            })
                    elif department.get('dataType') == '3':
                        exist_rec = request.env['pms.department'].search(
                            [('department_no', '=', department.get('sectionCode'))])
                        if exist_rec:
                            exist_rec.unlink()
                return {
                    "errorId": "10",
                    "errorInfo": "成功"
                }
            except Exception as e:
                _logger.error(e)
                return {
                    "errorId": "20",
                    "errorInfo": "失败{}".format(str(e))
                }

    @http.route('/getOverhaulSkill', type='json', auth='public', csrf=False)
    def get_over_haul_skill(self, *args):
        '''
        Pms获取检技通信息
        :param kwargs:
        :return:
        '''
        line_id = request.env['mdias_pms_interface'].get_line_info()
        headers = {
            'Content-Type': 'application/json',
        }
        lis = []
        dev_standard = request.env['metro_park_base.dev_standard'].search([('name', '=', 'SFM46')])
        search_rec = request.env['metro_park_maintenance.repair_rule'].search([('dev_standard', '=', dev_standard.id)])
        for data in search_rec:
            data = {
                "sourceSystemId": "MDIAS-{}-HTTP".format(line_id),
                "repairingTimeId": '{}-MDIAS-{}'.format(line_id, data.id),
                "dataType": '1',
                "vehicleModel": data.dev_standard.name,
                "repaireTypeName": data.name,
                "repaireCode": data.no,
                "repairDays": data.repair_days,
                "workDeptNo": data.pms_department.department_no if data.pms_department else '',
                "workDeptName": data.pms_department.department if data.pms_department else '',
            }
            lis.append(data)
            requests.post(
                'http://{}/scgl/mdiasServlet?method=repairingInfo'.format(
                    request.env['metro_park_base.system_config'].search([])[0].pms_ip),
                data=json.dumps(data), headers=headers, timeout=4)

    @http.route('/test_data', type='http', auth="none", csrf=False)
    def test_data(self, **kwargs):
        '''
        仅仅是测试接口，数据都是假的
        :param kwargs:
        :return:
        '''
        rec = {"overhaulSkillList": [{"checkTechInfoId": 415, "dataType": "1", "checkTechInfoNo": "2017—64",
                                      "ctiName": "关于7号线司机室侧门行程开关卡滞普查及整改的通知",
                                      "detailed": "调度组、各班组：\n自7号线空载以来，多次报司机室侧门打开时“司机室门全关闭灯”常亮且HMI显示门状态为绿色（关门状态）故障。本车间组织康尼分析该故障原因为行程开关安装底板质量问题导致开关摆臂压缩力增大引起的复位杆无法正常弹出，并对故障原因完成了模拟和验证。现决定对7号线所有列车司机室侧门行程开关卡滞进行普查并对故障件进行更换。具体作业要求如下。\n一、作业范围\n7号线：10701-10744列。\n二、作业人员及职责\n    康尼售后人员负责作业，班组人员做好确认。\n三、作业时间\n9月30日前完成。\n四、作业内容\n1、手动扳动开关复位杆，微动开关摆臂应无卡滞现象，否则需更换底板。\n                         \n                            图1 行程开关卡滞\n2、拆下微动开关，观察安装开关底板和固定开关销的连接处无翻边现象，否则需更换底板。\n\n图2 翻边与无翻边对比\n3、若需更换底座，拆掉底板固定螺栓和微动开关固定螺栓后，更换标准件并按标准扭力紧固（微动开关螺栓扭力1.4N·m，底板安装螺栓扭力8.8N·m），画好防松线。\n\n图3 紧固螺栓分布\n五、其他\n1、作业完毕后，需检查防松标记清晰无错位。\n2、手动按压回弹开关，无卡滞现象。\n3、微动开关与底板接触良好无缝隙。\n4、投蓄电池后，手动开关门，司机室门全关闭指示灯和HMI屏车门状态显示正常。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n\n检修三车间技术组\n2017年9月19日\n\n\n\n\n\n\n周宇\t审 核\t李侠\t批 准\t杨成军\n日检1班：            日检2班：           日检3班                   \n\n\n日检4班：            月检1班：           月检2班：       \n\n\n定修1班：            定修2班：                                           \n\n\n调 度 组： \n首做列车\t\t首做确认工程师\t\n完工确认工程师",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R,BJ",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 416, "dataType": "1", "checkTechInfoNo": "2017-70",
                                      "ctiName": "关于7号线司机室侧门平衡轮润滑及状态检查的通知",
                                      "detailed": "调度组、各班组：\n近期发现7号线司机室侧门平衡轮表面干燥，有磨损平衡轮，造成车门故障的隐患。现决定对7号线所有司机室侧门平衡轮进行润滑及状态检查，具体操作和要求如下：\n一、作业范围\n7号线10701-10744全部车辆。\n二、作业人员及职责\n检修班组进行润滑和状态检查作业，康尼人员对班组发现故障进行处理，完成作业后做好签字记录。\n三、作业时间\n预计1列车所需工时为15分钟，请在10月30日前完成。\n四、作业内容及要求\n1、打开司机室门门立柱上部维修口盖板。\n      \n图1司机室司机室门门立柱上部维修口盖板\n2、打开司机室侧门，使用毛刷将克鲁勃润滑脂均匀涂抹在平衡轮表面。\n\n图2 平衡轮\n3、完成润滑脂涂抹后，手动开关门5次。\n4、司机室门打开状态，用手转动平衡轮（需着手套），平衡轮转动平顺无异响。\n5、关闭司机室门，用力手转动平衡轮（需着手套），压轮应很难转动。\n6、若平衡轮状态不满足要求，通知厂家进行处理。（调整方法：松开螺母可调整平衡轮上下位置，通过增减垫片可调整前后左右位置，完成调整后，用乐泰243胶加固紧固螺钉，并用所需力矩将其旋紧）\n\n图3 平衡轮调整\n7、作业完成后，复位盖板，清除门上脏污和油渍。\n五、班组确认内容\n1、司机室门关闭时平衡轮转动灵活，司机室门关闭时，用力手转动平衡轮，压轮应很难转动。\n2、司机室门无脏污。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n\n\n\n\n\n\n\n\n\n\n检修三车间技术组\n2017年9月25日\n\n\n\n\n\n\n\n\n\n\n\n\n\n周宇\t审 核\t李侠\t批 准\t杨成军\n日检1班：            日检2班：           日检3班                   \n\n\n日检4班：            月检1班：           月检2班：       \n\n\n定修1班：            定修2班：                                           \n\n\n调 度 组： \n首做列车\t\t首做确认工程师\t\n完工确认工程师",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 419, "dataType": "1", "checkTechInfoNo": "检三技[2017]第074号",
                                      "ctiName": "关于对7、10号线电客车CCU-D软件升级的通知",
                                      "detailed": "在近期的维保服务中，发现牵引辅助系统对部分设备的监控信号记录不全，不能有效反映故障时刻的设备状态，对故障的原因分析造成了困难。为解决该问题，根据室技【2017】第076号《关于7、10号线牵引辅助系统软件升级到1.1.2.4版本的通知》，车间将组织厂家对电客车CCU-D软件进行升级",
                                      "ctiVehicleNo": "11005", "combineRepairTime": " ", "tempRepairTime": "1",
                                      "departCode": "11442"},
                                     {"checkTechInfoId": 421, "dataType": "1", "checkTechInfoNo": "检三技[2017] 第074号",
                                      "ctiName": "关于对7、10号线电客车CCU-D软件升级的通知",
                                      "detailed": "在近期的维保服务中，发现牵引辅助系统对部分设备的监控信号记录不全，不能有效反映故障时刻的设备状态，对故障的原因分析造成了困难。鉴于此，庞巴迪公司决定对CCU-D软件进行升级，升级后的软件将增加如下记录信息：高压使能信号、方向手柄前后向硬线信号、方向手柄前后向网络信号、零压启动激活信号等。升级后，CCU-D软件版本变更为1.1.2.4。根据室技【2017】第076号《关于7、10号线牵引辅助系统软件升级到1.1.2.4版本的通知》，车间将组织厂家对电客车CCU-D软件进行升级",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R,BJ,CNBJ",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 429, "dataType": "1", "checkTechInfoNo": "检三技[2017]第076号",
                                      "ctiName": "关于7、10号线电客车TCMS系统软件升级V2.4的通知", "detailed": " ",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 430, "dataType": "1", "checkTechInfoNo": "检三技[2017]第077号",
                                      "ctiName": "关于7、10号线电客车齿轮箱润滑油更换的通知",
                                      "detailed": "根据《成都地铁7、10号线转向架维护保养与大修手册》要求，现对10号线前5列车齿轮箱润滑油进行更换，7号线全列及10号线第6列按照“运行3个月或3.75万公里(以先到者为准)进行齿轮箱润滑油更换”标准进行更换，请调度组做好各列车公里数统计，并及时组织各班组更换。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D", "tempRepairTime": "1",
                                      "departCode": "12921"},
                                     {"checkTechInfoId": 437, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第078号",
                                      "ctiName": "关于7、10号线电客车受电弓电磁阀整改的通知",
                                      "detailed": "调度组、各班组：\n班组在对7号线电客车的检修中，发现多起ADD装置失效，不能实现自动降弓的故障。经检查，该故障均为受电弓气阀箱内VE2故障所致。VE2故障将导致ADD至碳滑板间的气路被阻断，在滑板出现异常漏风时，ADD装置不能自动排气，不能实现自动降下受电弓的功能。\n为避免上述问题，使受电弓在VE2故障的情况下，ADD仍能起到自动降弓的功能，对VE2采用如下操作：\n1）将VE2调节至常通位置：使用一字螺丝刀，将电磁阀红色调节旋钮逆时针旋转，使旋钮从位置“0”调节至位置“1”，这样将使得ADD与滑板气管保持常通状态。\n2）将气阀箱内端子排内的X1.1 和X1.3完全拔出，使VE2断开电源，拔出的端子进行绝缘处理。\n一、作业范围\n7号线、10号线全部电客车，即10701列～10744列、11001列～11006列。\n二、作业人员\n四方售后人员、受电弓厂家售后人员负责作业。\n检修班人员配合并确认整改状态。\n三、作业条件及要求 \n1、电客车需停放于有登顶平台的股道列位；电客车停放股道接触网须断电。\n四、作业时间\n自检技通下发之日起至10月31日前，请调度组安排完成对所有电客车的整改。此次整改一列车作业时间约20分钟，结合登顶检、月检作业安排。\n五、作业内容及要求\n1、电客车停放股道接触网断电前，班组作业人员将电客车总风打满。总风打满后，将电客车降弓断电。\n2、接触网断电，挂好接地杆。\n3、相关人员进行登顶作业，作业人员使用十字螺丝刀拧下受电弓气阀箱的四个角的固定螺丝，取下气阀箱盖板，并妥善放置盖板。\n4、用一字螺丝刀将VE2电磁阀的红色旋钮调至常通位，即从位置“0”调整至位置“1”。\n5、用小号一字螺丝刀将气阀箱内电缆X1.13和X1.14从端子排上拔出，将拔出的端子进行绝缘处理，并将绝缘端子用扎带绑扎牢固。\n \n6、以上作业完成后，电客车投入蓄电池电压，检查VE2指示灯应熄灭（先确认Mp1车和Mp2车车内电气柜的所有空开在正常位置）。\n7、升起受电弓，进行ADD自动降弓试验：拧松一根滑板的气管紧固螺帽，拔下气管（做ADD试验时，应两人协助进行试验，一人操作，一人抬起受电弓框架，防止砸伤），受电弓应能快速降下，且ADD装置有明显排气声，受电弓降弓后，将气囊供风阀打到关断位（竖直位），ADD装置排风停止。\n8、ADD试验完成后，将气管插入滑板下的锥形气口底部，拧紧气管紧固螺帽，将气囊供风阀打到正常位置（水平位），受电弓应能正常升起。\n9、进行升降弓试验，确认升降弓正常。\n10、重新盖好气阀箱的箱盖，并拧紧盖板紧固螺栓。\n11、采用上述步骤，对另一个受电弓进行检查和处理。\n六、班组确认内容\n1、确认端子排X1.13和X1.14已拔出，并做了绝缘处理，绑扎牢固。\n2、受电弓滑板气管状态良好，螺帽紧固，气管接头无漏风。\n3、确认车顶受电弓供气阀在正常位置（水平位）。\n4、电客车投入蓄电池后，确认VE2指示灯熄灭。\n5、确认ADD试验正常。\n6、确认两受电弓升降弓正常。\n7、确认气阀箱紧固螺栓紧固良好。\n七、作业风险分析及应对措施\n1、登顶作业时佩戴安全帽、安全带等，防止高空坠落。\n2、受电弓ADD试验，落弓时有可能造成作业人员砸伤，试验时截断气路供气阀截断塞门。\n八、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n九、其他\n    调度组、各班组应对该检技通进行学习，并将学习记录填入附件1《检技通学习记录表》中。\n附件1：《检技通学习记录表》\n附件2：《7号线受电弓气阀箱电磁阀整改记录表》\n附件3：《10号线受电弓气阀箱电磁阀整改记录表》\n\n检修三车间技术组\n2017年10月20日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 442, "dataType": "1", "checkTechInfoNo": "检三技[2017]第079号",
                                      "ctiName": "关于7、10号线电客车地板布普查的通知",
                                      "detailed": "调度组、各班组：\n班组在对7、10号线电客车的检修中，发现735列地板布有严重鼓包的情况。为了确保车辆地板布质量状态，现开展对所有车辆的地板布状态普查，具体作业及要求如下：\n一、\t作业范围\n7号线、10号线全部电客车，即10701列～10744列、11001列～11006列。\n二、作业人员\n班组人员。\n三、作业条件及要求 \n电客车客室照度良好，能清晰作业。\n四、作业时间\n自检技通下发之日起至10月31日前，请调度组安排完成对所有电客车的普查，结合隔日检及以上作业安排。\n五、作业内容及要求\n1、从TC1到TC2（或TC2到TC1）进行仔细检查；\n2、检查过程用眼睛看、或用脚轻踩；\n3、发现有鼓包情况立即通知专工及四方售后；\n4、填写《地板布普查记录表》。\n六、班组确认内容\n1、确认地板布接口、与门接触部位是否有鼓包情况。\n2、确认是否有大面积地板空心情况。\n七、作业风险分析及应对措施\n    检查地板布时，车门及侧顶板应关闭，防止坠落或头部撞击。\n八、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n九、其他\n    调度组、各班组应对该检技通进行学习，并将学习记录填入附件1《检技通学习记录表》中。\n附件1：《检技通学习记录表》； \n附件2：《7号线电客车地板布普查记录表》。\n附件3：《10号线电客车地板布普查记录表》\n \n\n\n\n\n\n\n\n\n\n\n检修三车间技术组\n2017年10月23日\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 451, "dataType": "1", "checkTechInfoNo": "检三技[2017]第082号",
                                      "ctiName": "关于10号线CCTV监控屏操作界面程序更新的整改通知修改",
                                      "detailed": "调度组、各班组：\n现10号线电客车CCTV屏由于以下两方面原因，这将不便于司机及检修人员在进行视频回放和故障应急处理时的操作。\n问题1：CCTV监控显示屏不能实现按文件回放功能；\n问题2：需最高权限才能对CCTV监控显示屏进行退出操作。\n为解决以上问题，需对CCTV监控屏操作界面程序进行更新，具体要求如下。\n一、作业范围\n11001-11006列。\n二、作业人员及职责\n    鸣啸厂家售后人员：负责程序更新作业，做好确认；\n车间检修班组：配合并进行复查。\n三、作业时间：结合里程修进行作业，升级时间大概30分钟。\n四、作业内容\n1、用携带新版CCTV程序的笔记本电脑接入客室交换机对CCTV监控屏操作界面程序进行更新；（旧版程序版本号：V2.0.4；新版程序版本号：V2.0.5）\n2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序V2.0.4；\n3、程序更新完成后，操纵CCTV监控屏，能够实现按文件进行回放的功能且能够根据需要拖动进度进行回放；同时，点击屏上退出图标后屏上弹出退出的提示框，通过提示框进行确认后能够实现显示屏重启功能。\n\n五、需要确认的内容及方法\n1、确认程序版本正确以及升级过程正常；\n2、视频回放功能正常\n3、一键重启功能正常\n4、柜门锁闭。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 452, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第083号",
                                      "ctiName": "关于7、10号线电客车空调软件升级至V1.02的通知",
                                      "detailed": "调度组、各班组：\n为解决7、10号线电客车空调系统部分现存问题，厂家已对空调控制器软件进行优化、完善，现组织开展7、10号线电客车空调控制器软件升级工作，软件版本由V1.01升级至V1.02，具体作业及要求如下：\n一、作业范围\n7号线、10号线全部电客车，即10701列～10744列、11001列～11006列。\n二、作业人员\n由广州中车厂家人员负责软件升级，班组人员做好配合、确认优化功能实现情况及版本信息是否正确。\n三、作业条件及要求\n电客车上电。\n四、作业时间\n一列车作业时间为1小时左右。\n五、作业内容及要求\n1、选取1列7号线电客车进行软件试升级，升级后由跟首列车专工、班组人员和广州中车在库内共同进行空调正常功能与本次优化功能验证。如验证可靠，安排上线试运行1天。\n软件升级优化内容主要有3项：\n（1）实现空调自动工况下可以手动设置目标温度；\n（2）紧急通风切换至正常通风，当紧急通风接触器断开后，正常通风接触器由“立即吸合”优化为“延时5秒再吸合”，避免出现拉弧现象；\n（3）对低压保护、高压保护、排气保护、过流保护故障判断逻辑进行优化，确保故障信息报送准确，避免出现发生以上一个故障时可能导致其他故障同时报出的现象。\n2、试验验证：\n2.1空调自动工况下可以手动设置目标温度的验证：\n由厂家及班组人员分别对自动工况下HMI上空调系统的目标温度进行设置，共同确认能进行目标温度设置，在验证完成后，恢复到最初的目标温度值。\n2.2紧急通风切换正常通风时延时5秒验证：\n厂家与班组人员共同确认，在紧急通风状态下，切换到正常通风时，过5秒，听到TC车客室空调柜内正常通风接触器延时5秒闭合声音，HMI上显示通风功能正常。\n2.3故障判断逻辑优化验证：\n做首列车时，由厂家人员操作，班组人员配合分别模拟低压保护、高压保护、排气保护、过流保护故障，厂家人员、轮值专工和班组人员和在HMI上和空调触摸屏上观察是否有其它故障同时报出，验证完后恢复设备至最初状态。并填写附件中的记录表。\n3、7、10号线首列车试改时，需进行全部三条优化内容试验验证，后续列车只需验证前两条内容。\n4、若首列试改车正线运行正常，则追加试改5列7号线电客车试运行10天。\n5、若试改车均运行正常，则进行7号线电客车空调控制器软件批量升级，同时选取1列10号线电客车试升级。\n6、若10号线试改车运营3天均正常，则进行10号线电客车空调软件批量升级。\n7、由班组配合人员与厂家人员共同对升级后软件版本号及空调功能进行确认，班组配合人员需在作业结束后确认空调柜门锁闭，现场出清。\n8、严格按照公司、中心的相关安全和工艺、质量要求进行作业。\n9、填写《电客车空调控制器软件升级记录表》。\n六、班组确认内容\n1、7、10号线首做车试验验证，后续升级列车需做前两条功能验证。\n2、空调控制器软件版本号为V1.02。\n3、空调试验空调在各模式下工作正常。\n4、确认电气柜门锁闭良好。\n七、作业风险分析及应对措施\n1、若软件升级、验证过程中出现异常，则将软件软件刷回原V1.01版本。\n2、在进行验证试验后，恢复所有设备和参数于最初状态。\n八、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n九、调度组、各班组应对该检技通进行学习，并将学习记录填入附件1《检技通学习记录表》中。\n附件1：《检技通学习记录表》\n附件2：《7号线首列车故障模拟测试记录表》\n附件3：《10号线首列车故障模拟测试记录表》\n附件4：《7号线电客车空调控制器软件升级记录表》\n附件5：《10号线电客车空调控制器软件升级记录表》",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 453, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第084号",
                                      "ctiName": "关于开展2017年设备冬季专项检查工作的通知",
                                      "detailed": "根据《室技[2017]第082号-关于车辆二中心开展2017年设备冬季专项工作的通知》相关要求，开展2017年设备冬季专项检查。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 466, "dataType": "1", "checkTechInfoNo": "检三技[2017]第088号",
                                      "ctiName": "关于7、10号线电客车烟火报警系统滤波元件批量整改的通知",
                                      "detailed": "调度组、各班组：\n近期7、10号线电客车烟火报警系统多次报回路模块无应答、电缆开路或短路故障。经过试装实验后，效果良好。根据室技第096号通知，现组织对7、10号线电客车烟火报警系统进行批量整改，具体作业要求如下。\n一、作业范围\n    7、10号线所有车辆。\n二、作业人员及职责\n    亚通达厂家售后人员：负责滤波元件的加装作业，做好质量确认；\n车间检修班组：配合并进行质量复查。\n三、作业时间\n根据车间实际作业情况安排作业，7号线直接批量整改，10号线整改1列后观察3天无异常后进行批量整改，预计一列车耗时2小时。\n四、作业条件及要求\n滤波元件安装：列车降弓、断蓄电池。\n功能试验：投入蓄电池、升弓投入高压。\n五、作业内容\n1、对所有列车（除711、734）烟火报警系统地址单元PCB板（MP1/MP2、M1/M2）进行更换，更换后的PCB板安装有滤波电感,如下图白色框所示；\n\n2、对所有列车（除10703、10711、10715、10730、10734、10742）车厢控制器回路模块增加滤波模块EMI（TC1/TC2），如下图白色框所示；\n\n3、安装完后需完成相关接线如下：\n（1）滤波模块EMI与回路模块X3之间的接线\n（2）烟火报警系统信号线接线\n信号线1139接EMI的11针脚，信号线1140接EMI的12针脚。\n4、整列车安装模块及接线作业完成后，列车上电对烟火报警系统功能进行测试。\n六、需要确认的内容及方法\n1、确认设备及部件安装牢靠，紧固件紧固无松动；\n2、确认接线正确，接线无松脱及接磨；\n3、列车上电后，烟火报警系统无报故障和报火警，随机抽查2个探测器用喷雾剂进行试验，烟火报警系统功能正常。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n\n附件1：成都7和10号线烟火报警系统故障分析报告\n附表1：7、10号线电客车烟火报警系统增加滤波元件记录表\n附表2：7、10号线电客车烟火报警系统增加滤波元件统计表\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n检修三车间技术组\n2017年11月14日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 472, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第090号",
                                      "ctiName": "关于7、10号线牵引电机和齿轮箱温度贴片粘贴通知",
                                      "detailed": "调度组、各班组：\n目前7、10号线牵引电机和齿轮箱温度贴片已到货，请调度组结合生产计划安排班组进行温度贴片粘贴，具体要求如下： \n一、作业范围\n10号线一期工程列车、7号线所有电客车。\n二、作业人员\n需班组2名人员作业。\n三、作业条件及要求\n列车停放在高架轨或有地沟的股道上，列车降弓、断蓄电池，做好安全防护及防溜措施。\n四、作业时间\n1、该专项作业时间为11月15日至12月15日，请调度组做好生产组织安排。\n2、一列车作业时间约0.5h，结合临修、里程修、隔日检及以上修程进行。\n五、作业内容及要求\n1、请班组到卢加莉处领取温度贴片，齿轮箱和牵引电机温度贴片每列车各需16和32张，7号线齿轮箱和牵引电机温度贴片共需704和1408张（44列）；10号线齿轮箱和牵引电机温度贴片共需96和192张（6列）。\n2、班组在粘贴前应先用擦拭纸沾酒精将粘贴位置擦拭干净，60-90规格的温度贴片用于齿轮箱上粘贴，80-100规格的温度贴片用于牵引电机两端（驱动与非驱动端），齿轮箱粘贴位置如图1，牵引电机粘贴位置如图2\n\n       图1                                   图2\n3、粘贴完成后将记录填写至附件1《7、10号线牵引电机及齿轮箱温度贴片粘贴记录表》，记录表应打印存档至调度室。\n\n六、班组确认内容\n确认牵引电机两端及齿轮箱温度贴片粘贴位置是否正确，是否粘贴牢固。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n检修三车间技术组\n2017年11月14日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 476, "dataType": "1", "checkTechInfoNo": "检三技[2017]第089号",
                                      "ctiName": "关于对7、10号线电客车PH箱舱门顶杆弹簧整改的通知",
                                      "detailed": "调度组、各班组：\n7、10号线电客车在运用中多次报出“牵引系统前舱门不能关闭”故障，回库后检查前舱门均锁闭正常。该故障信息容易导致司乘人员误认为PH箱前舱门盖板处于不安全状态，造成电客车下线。\n为避免上述问题，牵引厂家新誉庞巴迪公司决定对PH箱前舱门机构进行整改，将前舱门顶杆弹簧换成更软的型号。该整改不会对车辆性能造成影响。\n针对此次整改的具体要求如下：\n一、\t作业范围\n7号线、10号线全部电客车，即10701列～10744列、11001列～11006列。\n二、作业人员\n检修班组、庞巴迪售后人员。由庞巴迪售后人员进行整改作业及质量确认，检修班组配合人员进行质量复查和状态确认。\n三、作业条件及要求 \n1、电客车停放股道须有地沟条件、接触网带电。\n2、整改作业时，电客车降弓断电。\n四、作业时间\n检技通下发后，请调度组安排在三日内完成对10713、10714、10716、10732、10741的整改。整改后，运行两周验证无异常，由专工安排对其余39列7号线电客车和6列10号线电客车进行整改。1列车整改作业的时间约为20分钟。\n五、作业内容及要求\n1、电客车停稳，降弓断电，做好防溜、防护措施。\n2、作业人员将2车PH箱的隔离接地开关打至接地位（Q1和Q2均为水平位）。\n3、作业人员到5车PH箱进行整改作业。取下高速断路器侧的箱体盖板，注意双人操作，防止盖板掉落砸伤，盖板取下后妥善进行放置（需使用四角钥匙开启箱盖锁）。\n3、使用大号一字螺丝刀拧松隔离开关PC防护板四角的固定螺栓，取下PC板。\n4、将隔离接地开关打至接地位（先将Q1打至水平位，再将Q2打至水平位）。若电客车先前处于升弓送电状态，应放电5min以上才能作业。\n5、用手压住顶杆弹簧，使用尖嘴钳拔出顶杆上的限位销子，注意防止销子掉落。\n6、往箱体侧推出顶杆，取出旧弹簧和弹簧垫圈。\n7、将新弹簧装至顶杆原来位置，套上弹簧垫圈，使用新的限位销子进行固定。\n   \n8、恢复完毕后，用手推动顶杆几次，顶杆应动作灵活，无卡滞现象。检修班组配合人员需进行确认，同时确认限位销卡扣牢固。\n   \n9、将5车隔离接地开关打至运行位（先将Q2打至竖直位，再将Q1打至竖直位）。\n10、将隔离开关防护PC板装回原位，紧固螺栓后盖好箱体盖板。班组配合人员需确认箱盖锁闭良好，二次防脱链挂扣良好。\n11、再次将本车隔离接地开关打至接地位（先将Q1打至水平位，再将Q2打至水平位），以便对2车PH箱进行整改。\n12、采用同样的方式，完成对2车PH箱前舱门顶杆弹簧的整改作业。\n13、将两个PH箱的隔离接地开关恢复至运行位（Q1和Q2均是竖直位）。\n14、锁闭PH箱前舱门盖板，注意确认舱门锁闭后与盖板无活动间隙。\n15、电客车升弓送电，在HMI屏上“现存故障”界面确认无“牵引系统前舱门不能关闭”故障。\n16、电客车降弓断电，撤除防护。\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 481, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第094号",
                                      "ctiName": "关于升级7/10号线列车PIDS系统相关软件和普查整改的通知",
                                      "detailed": "调度组、各班组：\n为解决前期7、10号线电客车PIDS系统出现的相关问题，现需对相关设备进行普查和对相应程序进行升级，根据室技[2017]第102号-关于7、10号线电客车PIDS系统现存问题的整改通知的相关要求，主要对CCTV、电子地图和功放板程序升级、CCU板卡普查、下载的监控视频有无声音普查等，具体作业要求如下。\n一、作业范围\n7号线：10701-10744列；10号线：11001-1106列（只升级CCTV程序、下载的监控视频有无声音普查）\n（一）针对7、10号线CCTV程序进行升级\n从7号线列车中选10列曾发生过单个或多个通道卡屏、黑屏故障的车进行试整改，1周后CCTV监控屏若未出现卡屏和黑屏故障，则扩大试整改范围至20列，验证2周若效果较好则对7号线余下列车以及10号线列车进行批量整改。\n（二）针对7号线电子地图和功放板程序升级\n  选10列车进行试整改，上线运行5天后若效果较好，则进行批量整改。\n二、作业人员及职责\n鸣啸厂家人员：完成程序升级和普查整改工作。\n    车间检修班组：配合作业，确认软件更新后的内容。\n三、作业条件\n结合日检、月检进行作业。\n四、作业内容\n（一）7、10号线CCTV监控显示屏卡屏、黑屏问题\n问题整改方案：对CCTV程序进行升级。\n1、将笔记本接入客室交换机对CCTV程序进行升级；（升级前版本号：V2.0.5-11.02,升级后版本号：V2.0.5-11.10）\n2、程序升级过程中，若出现异常情况，则需将程序回退至先前版本V2.0.5-11.02；\n3、程序升级完成后，查看各通道显示以及联动触发和轮巡功能正常。\n（二）7号线媒体伴音声音大小不统一\n问题整改方案：更换电阻值匹配不正确的CCU板卡。\n1、拆下CCU板卡，查看并记录板卡上媒体输入电路电阻R25和R27阻值大小（应为220欧姆，对不满足阻值大小要求的CCU板卡进行更换）；\n2、正确安装板卡并恢复相关接线。\n（三）7号线电子地图预到站界面“琉璃场”拼音错误显示为“sanwayao”\n问题整改方案：升级电子地图程序。\n1、将笔记本接入客室交换机对电子地图程序进行升级；（升级前版本号：V1.1.59,升级后版本号：V1.1.61）\n2、程序升级过程中，若出现异常情况，则需将程序回退至先前版本V1.1.59；\n3、程序升级完成后，确认电子地图预到站界面“琉璃场”拼音显示“liulichang”。\n（四）7号线电客车区间运行以“狮子山”为终点站时，终点站报站错误。\n1、将笔记本接入客室交换机对功放板程序进行升级；（升级前版本号：V20170831,升级后版本号：V20171113）\n2、程序升级过程中，若出现异常情况，则需将程序回退至先前版本V20170831；\n3、程序升级完成后，将“狮子山”站设为终点站，确认终点站播报正确。\n（五）下载7/10号线电客车监控视频，查看播放时是否有声音。\n随机下载某一时间段的视频，在电脑上播放是否有声音，做好记录。\n五、需要确认的内容及方法\n1、CCTV程序升级完成后，查看各通道显示以及联动触发和轮巡功能正常，有无黑屏卡屏等现象。\n2、鸣啸人员将版本号投屏到电子地图上，班组人员确认电子地图软件版本号？V1.1.61。\n  3、作业完成后，确认柜门已锁闭。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求。\n2、程序升级整个过程列车不能断电，CCU板卡电阻普查需断掉设备电源。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 484, "dataType": "1", "checkTechInfoNo": "检三技[2017]第096号",
                                      "ctiName": "关于7、10号线电客车司机室送回风单元变压器换型的通知",
                                      "detailed": "调度组、各班组：\n为彻底解决7、10号线电客车司机室送回风变压器冒烟问题，根据专题会议要求，厂家现对变压器进行换型，将7、10号线银利品牌变压器更换为成都2、3、4号线使用的穆尔品牌变压器（输出功率与银利相同均为245VA，厂家确认可与现用银利完全互换），同时取消多余未接线的抽头。目前穆尔变压器样机已完成绝缘耐压、温升、负载通断冲击、匝间耐压测试等，并由第三方机构完成防火测试，目前已提交各项测试报告，均符合标准。现组织开展7、10号线电客车司机室送回风单元变压器换型工作。具体作业要求如下：\n一、作业范围\n    7、10号线所有车辆。\n二、作业人员及职责\n    由广州中车厂家人员负责变压器更换及状态、功能确认工作，班组人员做好配合及二次确认。\n三、作业时间\n2017年11月22日至2017年12月10日，每列车作业需3.5小时左右。\n四、作业内容及要求\n1、选取1列7号线电客车进行试改，试改完毕后在库内完成以下测试：1）不同工作档位间切换各50次；2）正常通风与紧急通风来回切换10次(调节方法，打开空调柜，调节380V检测继电器到停止位，无380V输入，空调自动进入紧急通风)；3）司机室送回风单元持续工作一日。以上测试均无异常后组织批量整改。\n2、每列车整改完毕后均需在库内测试5次司机室送回风单元切换不同档位时功能正常，测试1次正常通风和紧急通风可正常切换。\n3、作业完毕后进行校线，确认接线牢固、线号正确（线号如下表）。\n\n\n\n4、确认部件安装牢固，画好防松标记，盖板锁闭，现场出清。\n5、严格按照公司、中心的相关安全和工艺、质量要求进行作业。\n6、填写《电客车司机室送回风单元变压器换型记录表》。\n五、班组确认内容\n1、换上件的品牌为穆尔品牌，型号为MST 0245-380/100-130-150-230；\n2、确认设备及部件安装牢靠，紧固件紧固无松动；\n3、确认接线正确，接线无松脱及接磨；\n4、司机室顶板锁闭牢固；\n5、确认作业完成后，试验司机室送回风功能正常。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 493, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第098号",
                                      "ctiName": "关于开展7、10号线冬季电源设备专项检查的通知",
                                      "detailed": "主\n\n\n要\n\n\n内\n\n\n容\n\n\t调度组、各班组：\n根据室 技 [2017] 第104号《关于开展冬季电源设备专项检查的通知》专项要求，现开展7、10号线电客车冬季电源设备专项检查。电源设备专项检查的具体操作和要求如下：\n一、作业范围\n7、10号线全部车辆。\n二、作业人员\n检修班组。\n三、作业条件及要求\n地沟。\n四、作业时间\n预计检查一列车所需工时为1小时，请于12月6日前完成所有车的专项检查。\n五、作业内容及要求\n1、无电检查：\n1.1、断开QAGB空开后，检查蓄电池箱内壁防腐涂漆完好无脱落，箱内无水渍、无腐蚀、无电解液渗漏、无异味、无异响；\n1.2、电池安装牢固，橡胶垫、尼龙垫及绝缘部件无腐蚀损伤，单体液面高度符合标准，无鼓包、漏夜、外壳变形、开裂等，接线端子外观正常；\n1.3、蓄电池控制箱内配线无老化、龟裂、破损，接线紧固，接触器、继电器、断路器安装牢固。\n1.4、辅助变流器箱（ACM）内接线紧固，无凌乱、外皮磨损，各设备外观无损伤。\n2、有电检查：:\n2.1、观察HMI屏确认蓄电池电压、电流、温度正常，Tc1与Tc2电压偏差≤5V；\n2.2、观察HMI屏显示ACM输出各项交、直流电压值均正常；\n六、班组确认内容\n1、确认蓄电池正常投入。\n2、确认蓄电池、ACM变流器箱接线无老化。\n3、确认蓄电池液面正常。\n4、作业完后确认QAGB、ACM变流器箱、蓄电池及控制箱盖板恢复到位。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 494, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第097号",
                                      "ctiName": "关于对7、10号线电客车升降弓时间进行调整的通知",
                                      "detailed": "调度组、各班组：\n目前，7、10号线电客车有崔家店停车场、金花线上检修库和川师车辆段三个检修场段。这三个检修场段的接触网高度（距轨面高度）并不完全相同，有四种型式：5300mm、5100mm、4600mm和4040mm。在崔家店检修库内，带登顶平台的检修股道接触网高度有5300mm（L9道及L10道）和4600mm；川师车辆段带登顶平台的检修股道，接触网高度约为5100mm；金花线上检修库为刚性接触网，高度为4040mm。\n按照修程，在月检作业时须对电客车受电弓升降弓时间进行测量，目前对于升降弓时间的标准是5～8s。\n对同一列电客车在不同高度接触网下的升降弓时间进行测试的结果为：在高度为5300mm的接触网下，当升降弓时间调整为5s时，在高度为4600mm的接触网下测得的升降弓时间为2～3s；而升降弓时间调整为8s时，对应的升降弓时间为3～4s。在高度为4600mm的接触网下，升降弓时间为5s时，其在高度5300mm接触网下的升降弓时间为10～11s，但是从触按升弓按钮开始到受电弓触网的时间为20～21s（TCMS计时）；当升降弓时间调整为8s时，在高度为5300mm的接触网下测得的升降弓时间为15～16s，而从触按升弓按钮开始到受电弓触网的时间为24～30s（TCMS计时）。\n因此，由于检修场段接触网高度不一致，导致受电弓升降弓时间存在明显差异。若升降弓时间均执行5～8s的标准，当4600mm的接触网下的升降弓时间符合要求的电客车，其在5300mm的接触网下TCMS的升弓时间将大于15s，这必将导致HMI屏上报“升弓故障”。同理，在高度4040mm的接触网下满足升降弓时间的电客车，其在5300mm的接触网下，也将会因升降弓时间过长而报“升降弓故障”；而在高度为5300mm的接触网下满足升降弓时间的电客车，其在4600mm的接触网下，升降弓时间将不能满足5s的下限要求，且在接触网高度4040mm时，存在冲网和砸顶现象。\n鉴于此，根据检修库实际情况，对7、10号线电客车受电弓的升降弓时间标准做如下要求：\n一、作业范围\n7号线、10号线全部电客车，即10701列～10744列、11001列～11006列。\n二、作业人员\n检修班组受电弓检修人员。\n三、作业条件及要求 \n1、电客车停放股道须有登顶平台、接触网断电。\n2、电客车断电前，应先打足风压。\n四、作业时间\n登顶检及月修作业时（受电弓检查）。\n五、作业内容及要求\n1、按登顶检检作业指导书内容对受电弓进行检查。\n2、对受电弓的升降弓时间，做如下要求：\n1）崔家店停车场电客车，在L9道和L10道的升降弓时间t，按5≤t≤8s执行，其余股道按2≤t≤4s执行；\n2）川师车辆段电客车，升降弓时间t，按5≤t≤8s执行；\n3）金花线上检修库电客车，升降弓时间t，按1≤t≤2s执行。\n4）所有以上操作，升降弓过程中均不应存在冲网和砸顶现象。\n5）10号线电客车转线至崔家店停车场或川师车辆段进行检修作业时，不对受电弓升降弓时间进行调整。\n6）班组在填写作业记录册时，应在备注栏，填写检修场段和股道号，如：崔xx道。\n六、班组确认内容\n确认停车场段及停车股道号。\n七、作业风险分析及应对措施\n1、登顶作业，可能踏空坠落，造成人身伤害。控制措施：严格佩戴安全帽和安全带进行作业。\n2、受电弓检修时，地面人员升降弓操作可能导致车顶检修人员人身伤害。控制措施：地面人员升降弓前进行呼唤操作，确认安全后，方可进行升降弓操作；车顶检修人员在作业时，可将受电弓气囊供风阀截断，在检修完毕后将阀门恢复正常位。\n八、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n九、其他\n    调度组、各班组应对该检技通进行学习，并填写学习记录。\n\n检修三车间技术组\n2017年10月27日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,G",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 503, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第099号",
                                      "ctiName": "关于对7、10号线电客车轮缘润滑箱加油的通知",
                                      "detailed": "调度组、各班组：\n近期7、10号线出现轮喷喷不出油现象，为避免该现象再次发生，请调度组结合生产计划安排班组对轮缘润滑油箱进行加油，具体要求如下： \n一、作业范围\n7号线、10号线单数电客车。\n二、作业人员\n需班组2名人员作业。\n三、作业条件及要求 \n列车停放在高架轨或有地沟的股道上，列车降弓、断蓄电池，做好安全防护及防溜措施。\n四、作业时间\n1、该专项作业时间为11月29日至12月10日，请调度组做好生产组织安排。\n2、一列车作业时间约20min，结合临修、里程修、隔日检及以上修程进行。\n五、作业内容及要求\n1、将加油箱盖打开，并用手电筒照射油箱内部，加油至黑色刻度线附近（如图1），\n\n                           图1\n2、使用长铁棍或器具将油箱搅拌，使润滑油分散并将油箱盖盖好。\n3、做静态轮喷测试，短按一次轮缘润滑控制箱测试按钮后，观察轮缘上是否有乳白色润滑剂喷出（如图2），若未出现请长按测试按钮直至喷出为止。\n           \n                                图2\n4、轮缘润滑剂存放至四方处，加油前请班组联系四方人员领取。\n5、加油完成后将记录填写至附件1《7、10号线轮缘润滑箱加油记录表》，记录表应打印存档至调度室。\n六、班组确认内容\n确认润滑剂加至刻度线附近，箱盖盖好且轮喷测试正常。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n八、其他\n    调度组、各班组应对该检技通进行学习，并填写学习记录。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 507, "dataType": "1", "checkTechInfoNo": "检三技[2017]第100号",
                                      "ctiName": "关于升级7、10号线列车PIDS系统相关软件和广播录入的通知",
                                      "detailed": "调度组、各班组：\n根据室技[2017]第110号-关于2、4、7、10号线电客车PIDS系统程序更新的通知的相关要求，现需对7号线电客车电子地图程序更新、补录10号线开通的宣传语音广播；10号线电子地图程序、CCU板程序、功放板程序更新、补录换乘7号线广播语音，具体作业要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业时间\n1、7号线电子地图程序更新、补录10号线开通的宣传语音广播在12月4日前完成；\n2、10号线补录7号线换乘语音广播开通前1天完成。\n三、作业人员及职责\n鸣啸厂家人员：完成程序升级和普查整改工作。\n    车间检修班组：配合作业，确认软件更新后的内容。\n四、作业条件\n结合日检、月检进行作业。\n五、作业内容\n（一）7号线PIDS系统程序更新\n1、7号线电客车电子地图程序更新\n1.1、用携带新版电子地图程序的笔记本电脑接入客室交换机对电子地图程序进行更新；（旧版程序版本号：V1.1.61；新版程序版本号：V1.1.63）\n1.2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序V1.1.61；\n1.3、程序更新完成后，通过手动报火车南站，确认火车南站台结构和出入站口及文字图标正确，具体画面如下图1-图3所示。\n \n图1                             图2\n\n图3\n2、补录10号线开通的宣传语音广播\n2.1、分别在火车南站-神仙树、高朋大道-太平园、武侯大道-龙爪堰、金沙博物馆-一品天下、火车北站-驷马桥、槐树店-迎晖路、成都东客站-大观、四川师大-琉璃场8个区间补录10号线开通的宣传语音广播，补录语音要求在出站广播播完后停顿2秒进行播放。\n2.2、首列车更新时专业工程师到现场完成静态验证并对广播语音是否正确进行核对，并安排专人上线跟车动态验证，确保所有站点语音报站无异常。\n\n（二）10号线电客车PIDS系统程序更新\n1、电子地图程序更新\n1.1、用携带新版电子地图程序的笔记本电脑接入客室交换机对电子地图程序进行更新；（旧版程序版本号：V1.1.36；新版程序版本号：V1.1.38）\n1.2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序V1.1.36；\n1.3、程序更新完成后，通过手动报太平园站，确认太平园站台结构和换乘信息正确，具体画面如下图4-图11所示。\n\n图4：到站上行（右侧屏）\n\n图5：到站下行（右侧屏）\n\n图6：离站上行（右侧屏）\n\n图7：离站下行（右侧屏）\n\n图8：到站上行（左侧屏）\n\n图9：到站下行（左侧屏）\n\n图10：离站上行（左侧屏）\n\n图11：离站下行（左侧屏）\n2、CCU板程序更新\n2.1、用携带新版CCU程序的笔记本电脑接入客室交换机对CCU板程序进行更新；（旧版程序版本号：590-PA-CCU-app-1-20170825；新版程序版本号：590-PA-CCU-app-1-20171127）\n2.2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序590-PA-CCU-app-1-20170825；\n2.3、程序更新完成后，需在正线对自动报站强切功能进行验证：在全自动报站模式下通过HMI屏设置“屏蔽全自动报站”（如图9），确认系统被切换到半自动报站模式，且半自动报站功能正常。\n\n图9\n3、功放板程序更新\n3.1、用携带新版功放板程序的笔记本电脑接入客室交换机对功放板程序进行更新；（旧版程序版本号：590-PA-EAMP-app-1-20170828；新版程序版本号：590-PA-EAMP-app-1-20171117）\n3.2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序590-PA-EAMP-app-1-20170828；\n3.3、程序更新完成后，需在正线对客室内车端LED屏显示进行验证：在列车达到终点站折返切换钥匙信号时，确认客室内车端LED显示为“本次列车开往XX方向”。\n4、补录7号线换乘语音广播\n4.1、通过PTU更新客室功放控制模块内的语音文件。\n4.2、首列车更新时专业工程师到现场完成静态验证并对广播语音是否正确进行核对，并安排专人上线跟车动态验证，确保所有站点语音报站无异常。\n六、需要确认的内容及方法\n1、程序升级整个过程列车不能断电；\n2、程序升级过程中需确认升级前后程序版本号正确；\n3、程序升级完成后需确认PIDS系统功能正常；\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求。\n2、程序升级整个过程列车不能断电，CCU板卡电阻普查需断掉设备电源。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R,BJ",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 518, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第102号",
                                      "ctiName": "关于7、10号线电客车空调系统软件由V1.02升级至V1.03的通知",
                                      "detailed": "\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\t调度组、各班组：\n针对7、10号线电客车电加热功能在半暖工况下无法关闭的问题，经厂家系统、软件工程师现场调查，确认空调软件控制逻辑存在缺陷，目前电加热关闭时必须满足每节车6组电加热（4个预热器+2个客室电热器）之间各自存在2s延时的条件，而半暖工况下由于一半电加热未启动，未启动的电加热均不存在2s延时，因此导致电加热无法关闭。厂家针对该问题进行软件逻辑优化：\n1.若电加热有启动记录，则判断前一个电加热关闭延时2s后，再作关闭另一个电加热的请求信号；\n2.若电加热无启动记录，则判断该电加热不对其他电加热关闭造成影响，不作延时处理。\n现组织开展7、10号线电客车空调系统软件升级工作（V1.02→V1.03），具体要求如下：\n一、作业范围\n11001-11006，10701-10744\n二、作业人员及职责\n由广州中车厂家人员负责软件升级作业及软件版本、功能确认，车间安排人员做好配合、确认。\n三、作业时间\n每列车刷新程序加验证需2小时，仅刷程序需30分钟。\n四、作业内容\n1、由车间选取2列7号线电客车试整改，1列10号线电客车试整改，正线运营1日跟踪观察，若无异常，则追加5列7号线电客车车试整改并正线运营1日跟踪观察，若仍无异常则开展批量整改。\n  2、由于之前应急处理时把每节车的Q18、Q28和Q38都断开了，因此在刷程序之前，需当日要更新程序的列车每节车空调柜内的Q18、Q28和Q38都闭合，三个空开位置如下图所示：\n\n  3、每列试改车软件升级后须库内测试空调功能正常，确认半暖及其它工况均可正常启动、切换、停止。\n验证内容和方法：由厂家人员利用自带的PTU及数据线接到空调控制器的X9接口（以太网接口）进行软件升级和工况模拟试验，如下图所示，对机组的新回风温度进行设置，分别模拟全暖、半暖、半冷、全冷工况，在HMI上观察压缩机、冷凝风机、预热器和客室电加热是否正常启动，并在客室内能清楚感受到温度有一定的上升或下降，最后在HMI上和司机室电器柜内的空调模式开关能切换为通风工况和停止工况，压缩机、冷凝风机、预热器和客室电加热能正常停止工作（电加热及预热器停止时间间隔2秒），且客室内温度明显恢复正常，最后试验应急通风功能正常。\n\n4、作业完毕后，作业人员及配合人员须共同确认软件版本号为V1.03，作业现场出清，空调控制柜柜门锁闭。\n5、严格按照公司、中心的相关安全和工艺、质量要求进行作业。\n五、班组确认内容\n1、刷新程序后版本软件为V1.03；\n  2、空调柜内Q18、Q28和Q38处于闭合位置；\n3、空调程序验证试验正常；\n    4、空调控制柜柜门锁闭，现场出清。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n编 制\t\t审 核\t\t批 准\t\n签收\t7号线班组：\n\n日检一班：      日检二班：      日检三班：      日检四班：\n\n月修一班：      月修二班：      定修一班：      定修二班：\n\n调度组：\n\n10号线班组：        \n\n金花检修班：         调 度 组：\n\n首做列车\t\t首做确认工程师\t\n完工确认工程师\t\n\n\n附件1：     \n7号线电客车空调系统软件升级记录表\n车号\t空调软件版本为V1.03\tQ18、Q28和Q38闭合\t试验验证内容正常（仅前7列车）\t空调系统功能正常\t柜门锁闭\t作业者/时间\t确认者/时间\t备注\n10701\t\t\t\t\t\t\t\t\n10702\t\t\t\t\t\t\t\t",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 522, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第103号",
                                      "ctiName": "关于7、10号线VCU2.5与HMI2.4程序更新的通知",
                                      "detailed": "调度组、各班组：\n根据室技第114号通知，需在应急广播中补录一条服务广播，同时对前期运营中暴露出的问题进行优化，现组织对7、10号线电客车VCU和HMI程序进行批量刷新，原95号专项作废，具体作业要求如下。\n一、作业范围\n7号线：10701-10744列。10号线：11001-11006。\n二、作业人员及职责\n作业由四方完成，班组人员配合进行确认。\n三、作业时间\n7、10号线首列车经过静态、试车线、末班车验证，正线运行1天后进行5列车试刷验证5天，再批量刷新。\n每列车用时30分钟，12月24日前完成。\n四、作业内容\n修改内容：\n1、在轮径设置界面增加“轮径复位”按钮，当发生轮径跳变时，点击此按钮，VCU主从切换，轮径值恢复为“840”。\n2、修改 PIDS 音量设置方式，将广播音量和媒体音量步进值修改为5。\n3、在特殊广播界面增加“换端等候”按钮。\n4、增加数据记录：增加 TC1 车 2 轴、MP1 车 2 轴、TC2 车 2 轴轮径值记录。\n5、取消里程超限在 HMI 中的故障提示。\n6、运行界面 MCM 图标在牵引状态字≥20 持续 1s 后显示红色，ACM 图标在辅\n助状态字≥20 持续 1s 后显示红色。\n7、对于三相检测相关故障，自检测到380V电压后，延时30S再开始检测。\n8、现存故障界面增加确定按键，用于对所有现存故障的确认。\n\n（1）没有现存故障时，故障提示图标显示，确认按键不可点击。\n（2）出现新的现存故障时，故障提示图标显示并且闪烁，进入现存故障界面时，如果是只有一页现存故障，则确定键可以点击。如果存在多页现存故障，司机需要点击翻页按键到最后一页后，确认键才可以点击。\n（3）点击确认键后，没有现存故障时，按照步骤（1）显示，出现新的现存故障时，按照步骤（2）显示，没有出现新的现存故障时，故障提示图标显示，但不闪烁。\n9、在运行界面增加总风压力显示。\n验证方法：（仅验证7、10号线首做列车）\n1． 在 HMI 屏【检修】-【轮径】界面修改 MP1 车 2 轴轮径为835，点击“轮径复位”，VCU主从切换，轮径值变为840。\n2． 在【设置】-【PIDS 设置】-【音量设置】界面，调节广播音量和媒体音量，增加或减小值均为 5。\n3、 在特殊广播界面点击“换端等候”按钮，播放“各位乘客，列车即将投入运营，请耐心等候，感谢您的合作”语音。若PIDS未刷新软件，则在端口查询界面查看 A8 端口，第 5 个字低字节为 31。\n4． 在累计数据界面记录当前 A、B 侧里程值，用 PTU 修改 A 侧里程，在累计数据界面确认，A 侧里程与 B 侧里程差值超过 6500km，HMI 不再报出内外环里程差值超限故障，验证完成后将 A 侧里程修改为原值并在累计数据界面进行确认。\n5． 庞巴迪模拟 MCM 牵引状态字≥20，HMI 运行界面对应车的 MCM 图标显红，庞巴迪模拟 ACM 辅助状态字≥20，HMI 运行界面对应车的 ACM 图标显红。\n6． 通过断空开等方式模拟故障：\n（1）没有现存故障，故障提示图标显示灰色，确认按键不可点击。\n（2）出现新的现存故障时，故障提示图标显示红色并且闪烁，进入现存故障界面时，如果是只有一页现存故障，则确定键可以点击。如果存在多页现存故障，司机需要点击翻页按键到最后一页后，确认键才可以点击。\n（3）点击确认键后，没有现存故障时，图标显示灰色。出现新的现存故障时，图标显示闪烁红色。没有出现新的现存故障时，故障提示图标显示红色，但不闪烁。\n7. 运行界面有总风压力显示。\n8.分别将Tc1、Tc2车空压机的三相延时继电器设置 On Delay 10秒、15秒，将列车总风降至700kpa以下。在空压机控制空开处于自动位的情况下，给列车升弓送高压，列车不报出空压机三相缺相故障。\n五、班组确认内容\n1、升级完后确认两端VCU、HMI程序版本分别为V2.5、V2.4；\n2、确认首列车验证结果正确；\n3、升级完后确认网络通信界面正常；\n4、确认柜门锁闭良好。\n六、其他\n1、作业完毕后，请填写记录表。\n2、本次升级不会对列车安全运行产生影响，若软件升级后导致列车异常，需将程序退回原版本程序。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 525, "dataType": "1", "checkTechInfoNo": "检三技[2017]第105号",
                                      "ctiName": "关于7、10号线电客车更换总风软管的通知",
                                      "detailed": "1、列车两端挂好防护牌，确认列车风压在800kPa以上，降弓断蓄电池。\n2、取下总风截断塞门锁闭装置（头车一位端无锁闭装置），截断每节车两端的总风截断塞门，使用扳手拧松总风软管接头处的功能螺母，待管路中的压缩空气排空后拆下总风软管。\n3、安装新的总风软管，安装时确认软管的锥头体插入对正，然后用手拧入功能螺母直至无法拧动，再用扳手拧紧。软管安装时应自然摆放，无较大抗力。如遇到拧入困难的情况，需拆下软管检查连接螺纹的状态，避免造成螺纹损伤。\n4、恢复总风截断塞门，使用肥皂水检查总风软管的接头无泄漏，并及时使用干抹布擦干，画黑色防松线（厂家划）。\n5、列车送电升弓，空压机自动打风至停止（约900±20kPa），司控器置于紧急制动位30s以上，进行空车全漏泄试验，要求5分钟内压力下降值小于20kPa。\n6、给所有总风截断塞门装回锁闭装置（头车一位端总风塞门除外）。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 527, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第106号",
                                      "ctiName": "关于7、10号线RIOM1.3程序更新的通知",
                                      "detailed": "调度组、各班组：\n为解决近期10号线发生TC车RIOM通讯故障问题。根据室技119号，现组织对7、10号线电客车TC车RIOM程序进行批量刷新，具体作业要求如下。\n一、作业范围\n7号线：10701-10744列。10号线：11001-11006。\n二、作业人员及职责\n作业由四方完成，班组人员配合进行确认。\n三、作业时间\n7、10号线首列车经过静态、试车线、末班车验证，正线运行1周后进行5列车试刷验证1周，再批量刷新。\n每列车用时30分钟，1月20日前完成。\n四、作业内容\n修改内容：\n优化MVB通信配置逻辑，第一次MVB通信配置失败后继续进行MVB通信配置，可以避免在上电后第一次通信配置失败后TC车RIOM通信异常的问题。\n验证方法：\nTC车RIOM启动后可以正常通信，后续继续跟踪观察列车上电后TC车RIOM无通信故障。\n五、班组确认内容\n1、检查【网络】界面，通讯正常。\n2、检查TC车RIOM版本号为1.3。\n3、作业完毕后检查柜门恢复好。\n六、其他\n1、作业完毕后，请填写记录表。\n2、本次升级不会对列车安全运行产生影响，若软件升级后导致列车异常，需将程序退回原版本程序。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 529, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第001号",
                                      "ctiName": "关于7、10号线电客车后端门电磁铁安装结构整改的通知",
                                      "detailed": "调度组、各班组：\n近期7、10号线库内及正线发生后端门电磁铁松动的情况较多，经过拆解电磁铁组装结构，发现电磁铁组装情况不良，现对电磁铁进行整改，具体作业要求如下。\n一、作业范围\n7号线：10701-10744；\n10号线：11001-11006。\n二、作业人员及职责\n厂家对电磁铁进行整改，班组人员负责确认整改情况。\n三、作业时间\n1月25日前完成。\n四、作业内容\n1、拆开门页上的电磁铁盖板，取下电磁铁紧固螺栓，去除橡胶圈，如图1所示；\n\n图1 去除橡胶圈\n2、普查电磁铁是否粘接牢固，没有粘接的电磁铁重新进行粘接，如图2所示；\n\n图2 重新粘接电磁铁\n3、安装电磁铁紧固螺栓，涂抹螺纹紧固剂后进行紧固，紧固顺序：平垫—弹垫—螺母—螺母，如图3所示；\n   \n图3  紧固螺栓\n4、组装紧固完成后在电磁铁端部画防松线，如图4所示。\n\n图4 画防松线\n5、安装完成后试验后端门开关门功能良好。\n五、班组确认内容\n1、确认电磁铁都进行的粘接处理，且粘接牢固；\n2、确认电磁铁橡胶圈都已去除；\n3、确认紧固螺栓时，按照平垫—弹垫—螺母—螺母的顺序进行紧固；\n4、确认防松线都已画好；\n5、确认后端门开关门功能良好。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐。\n七、其他\n    调度组、各班组应对该检技通进行学习，并填写学习记录。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 534, "dataType": "1", "checkTechInfoNo": "检三技[2018]第002号",
                                      "ctiName": "关于7、10号线电客车空压机延时启动时间设置的通知",
                                      "detailed": "调度组、各班组：\n7、10号线电客车在总风压力低于700kpa情况下初上电时，存在辅助逆变器并网失败的问题。经分析该故障是由于列车辅助逆变器在并网过程中，空压机启动使负载电压降低到允许电压值以下，从而导致辅逆并网失败。为解决此问题，根据《室 技[2017]第117号 关于7、10号线电客车空压机延时启动时间设置的通知》现对空压机延时启动时间进行调整。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,F", "tempRepairTime": "1",
                                      "departCode": "12921"},
                                     {"checkTechInfoId": 535, "dataType": "1", "checkTechInfoNo": "检三技[2018]第003号",
                                      "ctiName": "关于7、10号线电客车CCU-D软件升级到版本1.1.2.5的通知",
                                      "detailed": "最近正线频繁报“CCU-D故障”，经过分析，原因是CCU-D中监控数据记录工作状态的信号发现CCU-D数据记录监控不正常时，会重启CCU-D，CCU-D重启时会报“CCU-D故障”。为了解决该问题，厂家计划升级CCU-D软件，新软件优化了CCU-D数据记录的监控信号，删除了在项目前期因为调试所需的监控信号，保留了售后阶段对车辆监控和故障代码的监控信号。\n为此，根据中心下发的《关于7、10号线牵引辅助系统软件升级到1.1.2.5版本的通知》，车间将对所有电客车CCU-D进行软件升级。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 542, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第005号",
                                      "ctiName": "关于7、10号半永久牵引杆拉杆上键松动情况普查的通知",
                                      "detailed": "调度组、各班组：\n由于近期2号线班组在库内检修作业时发现部分电客车半永久牵引杆拉杆与缓冲装置间定位键松脱（如图1）。\n   \n                                   图1\n为避免7、10号线出现同类安全隐患。根据中心安排，现开展对电客车半永久牵引杆拉杆上的定位键松动情况进行普查，具体要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业时间\n1月30日前完成。可结合日检、月检进行作业。每列车作业约20分钟。\n三、作业人员\n由班组人员进行作业\n四、作业条件\n1、列车降弓、断蓄电池、停靠在有地沟的股道。\n2、作业工具：凳子、手电筒、分度值为1mm的直尺。\n五、作业内容\n1、\t每列车共有5套带缓冲器的半永久牵引杆（分别位于2车一、二位端，3车二位端，5车一、二位端之间）需要普查如图2所示中的“B”。\n+ Tc A+B MpB+C M B+C M C+B Mp B+A Tc +\n                             图2\n2、班组人员使用凳子、手电筒及分度值为1mm的直尺对带缓冲器的半永久牵引杆进行普查，普查流程见图3。\n \n                                       图3\n3、若发现定位键松动且手动不能拔出定位键，需用分度值为1mm的直尺测量活动量。定位键活动量为定位键最大抬高高度，即为图4中标识直线的长度。\n \n                                        图4\n4、班组人员按照图3流程检查完成后，在附表1、附表2中记录检查情况，并将纸质版打印放置调度室存档。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n5、调整时间旋钮是列车禁止投电，设置完成后需确认各设备箱盖锁闭良好。\n七、其他\n    调度组、各班组应对该检技通进行学习，并填写学习记录。\n\n\n\n                                        检修三车间技术组\n                                                2018年1月11日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 543, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第004号",
                                      "ctiName": "关于开展7、10号线电客车半年保洁的通知",
                                      "detailed": "调度组、各班组：\n为了保障7、10号线车辆运行过程中各部件表面干净整洁，且有利于电客车日常检修作业，目前将对车辆的车顶、车体、底架等部件表面污垢进行清洁。具体作业要求如下:\n一、作业范围\n7号线：10701-10744\n10号线：11001-11006\n二、作业人员\n保洁公司保洁人员现场作业，班组人员配合及确认保洁情况\n三、作业条件\n有登顶平台、地沟的股道，作业前车辆受电弓处于降弓状态，接触网已断电。\n四、作业内容及要求\n（一）、作业内容\n1、车顶保洁\n作业部位：受电弓各杠杆清洁；车顶熔断器箱；车顶空调机组表面清洁；车顶其他部位无异物。\n作业方法：“ND-310高效油污净洗剂”按1：10的比例兑水后，使用拖把沾湿并拖洗一遍车顶，然后用清水清洗干净。车顶设备等需使用擦布沾 湿后擦拭干净（如图1所示）。\n    \n图1 车顶保洁\n注意：a、严禁踩踏空调冷凝风扇罩板；b、上车顶作业人员系好安全带，注意作业安全。\n2、车体保洁\n作业部位：清洁车体外表面、玻璃等。\n作业方法：“ND-310高效油污净洗剂”按1：20的比例兑水后，用刷把洗刷，然后用清水冲洗干净（如图2所示）。\n    \n图2 车体保洁\n3、车底保洁\n作业部位：清洁车底转向架、悬挂装置、各类箱体设备及管路等各部件表面。\n作业方法：“ND-310高效油污净洗剂”按1：10的比例兑水后，使用擦布擦拭车底各类箱体设备、转向架部件外表，然后用清水冲洗干净。\n其中，对于车底保洁时，个别油泥较重设备则按照如下要求进行清洁：\n① 用塑料刮刀将车辆底部油泥较重部位表层油泥祛除干净；\n② 油泥祛除干净以后先用毛刷将“ND-310高效油污净洗剂”原液沾刷于部件表面，反应1-2分钟，然后再用毛刷仔细刷洗，油泥分离后用1:5～1:10兑水配比好的ND-310喷洗部件表面，清洗干净后再用清水漂洗干净；\n③ 若①、②完成后仍然特别脏的部件，则先将“NT-207A强力油污清洗剂”原液均匀的喷洒在待清洗部位表面，待2～3分钟，然后用毛刷反复刷洗（特别脏的部位重复此步骤），比较小的角落缝隙或比较难处理的部位用牙刷刷洗（在保洁时若工作人员高度不够则需垫板凳或其他增高垫，刷洗时使用加长杆），刷洗干净后，用1:5～1:10兑水配比好的ND-310喷洗，然后用清水漂洗干净（如图3所示）。\n     \n图3 车底保洁\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "BJ", "tempRepairTime": "1",
                                      "departCode": "12921"},
                                     {"checkTechInfoId": 548, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第007号",
                                      "ctiName": "关于7、10号线电客车客室门紧急解锁罩板和安全锤罩板更换的通知",
                                      "detailed": "调度组、各班组：\n因7、10号线电客车客室门紧急解锁罩板和安全锤罩板断裂点处预留的连接筋较宽，不易击碎，紧急情况下不利于乘客逃生，存在安全隐患。为保障在紧急情况下罩板可以击碎，且运营及日常检修过程中不自然断裂，现计划对7、10号线电客车客室门紧急解锁罩板和安全锤罩板进行更换，将原紧急解锁罩板断裂点连接筋宽度由3mm改为1mm，将原安全锤罩板断裂点连接筋宽度由17.7mm改为1mm，经多次试验，新罩板可满足使用要求。具体要求如下：\n一、作业范围\n安全锤罩板更换：7、10号线所有电客车；\n紧急解锁罩板更换：7号线所有列车。\n二、作业时间\n2月10日前完成。\n三、作业人员及职责\n由今创集团售后人员进行更换，由车间检修班组进行配合及确认，由质检人员进行验收。\n四、作业条件\n可结合日检、月检进行作业。\n  工具：螺丝刀、玻璃胶\n五、作业内容\n1、用螺丝刀撬下旧的紧急解锁罩板和安全车锤罩板；\n2、割掉粘接面多余的胶，避免余胶影响粘接效果；\n3、在粘接面均匀的打上玻璃胶，将新罩板按压上贴合面。适当的调整罩板贴合处，保证罩板与侧顶板面平整一致；\n4、用纸胶带固定罩板，避免罩板因玻璃胶未干而脱落。\n六、班组确认内容\n1、监督厂家对螺丝刀头部进行包裹，提醒厂家在拆旧罩板时应防止螺丝刀头刮伤漆面；\n2、新罩板安装完成后，督促厂家擦掉罩板表面多余的玻璃胶；\n3、新罩板安装完成后，需静置2小时方可撕掉保护的纸胶带。电客车上线前应确认所有纸胶带全部撕掉。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n八、其他\n调度组、各班组应对该检技通进行学习，并填写学习记录。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": " ", "tempRepairTime": "1",
                                      "departCode": "12921"},
                                     {"checkTechInfoId": 550, "dataType": "1", "checkTechInfoNo": "检三技[2018]第008号",
                                      "ctiName": "关于10号线列车电子地图程序进行更新的通知",
                                      "detailed": "调度组、各班组：\n为实现10号线电客车电子地图预到站时间提示画面显示，需要对电子地图程序进行更新，具体要求如下。\n一、作业范围\n11001-11006列。\n二、作业人员及职责\n鸣啸厂家售后人员：负责电子地图程序更新作业，做好确认。\n车间检修班组：配合并进行确认。\n三、作业时间\n按照车间实际用车情况安排，先试刷1列车上线验证1天，若无问题则批量刷新。\n四、作业内容\n1、用携带新版电子地图程序的笔记本电脑接入客室交换机对电子地图程序进行更新；（旧版程序版本号：V1.1.38；新版程序版本号：V1.1.40）\n2、程序更新过程中，若出现异常情况，则需将程序回退至旧版程序V1.1.38；\n3、首列车更新时专业工程师必须现场完成静态验证，且视情况跟车或安排专人上线跟车动态验证，确保所有站点电子地图显示画面无异常。\n五、需要确认的内容及方法\n1、程序更新完成后，确认电子地图上显示的后续站点（除下一站外）都有倒计时时间显示（站点上圈内数字为到达该站所需要的分钟数），且随时间倒计时更新，如图1所示。\n\n                         图1\n2、作业完成后，班组人员填写作业记录表（附表1）。\n六、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车；\n\n检修三车间技术组\n2018年1月18日\n\n\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 560, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第009号",
                                      "ctiName": "关于7、10号线电客车软管更换的通知",
                                      "detailed": "调度组、各班组：\n对于10732列电客车总风软管破裂故障，经查为上海加诺公司所供软管存在质量问题。为及时消除故障隐患，确保车辆安全运营，根据2018第4期《成都地铁运营有限公司 7号线车辆问题专题推进会纪要 》要求，现计划使用常州中铁供风软管将7、10号线上海加诺供风软管根据风险等级和到货计划分批次全部更换。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 563, "dataType": "1", "checkTechInfoNo": "检三技[2018] 第11号",
                                      "ctiName": "关于7、10号线电客车设备防火状态状态专项检查通知",
                                      "detailed": "调度组、各班组：\n根据《室技 [2018] 第015号关于开展电客车设备防火紧急专项检查的通知》的相关要求，为进一步加强安全生产和火灾防控意识，确保7、10号线电客车安全可靠运行，特开展设备防火状态的专项检查。具体要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业人员\n班组检修人员。\n三、作业条件\n可结合日检/里程检、月检、登顶检等修程进行本专项检查作业。\n可单独安排本专项检查作业。\n四、作业内容及要求\n1、车下连接器检查，要求2018年1月26日晚完成。\n列车断电状态下，使用手电筒，用手触摸车下所有连接器无松动、紧固牢固；目视有防松线的连接器其放松线无松动。检查完成后填写附件1。\n2、客室电加热器检查，要求2018年1月26日晚完成。\n列车断电状态下，使用手电筒，目视客室电加热器外罩板无明显变色及其他异常情况，可视部位接线线缆无异常情况。检查完成后填写附件1。\n3、灭火器检查，要求2018年1月26日晚完成。\n列车断电状态下，检查灭火器及附属配件安装牢固，目视灭火器指针在有效范围内，检查灭火器封条完好，且在有效期时间范围内。检查完成后填写附件1。\n4、司机室、客室各电气柜内接线状态检查，要求2018年2月10日前完成。\n列车断电状态下，目视检查线缆线皮无破损、无接磨，接线柱及连接器插头接线无松动，接触器、继电器、断路器安装牢固。检查完成后填写附件2。\n5、蓄电池状态检查，要求2018年2月10日前完成。\n用四角钥匙打开车下蓄电池箱箱盖，将蓄电池电源空开打至关位，用手拉出蓄电池，目视检查蓄电池外观良好、无鼓包、无裂纹，蓄电池可观液面正常、无泄漏、排气孔通畅，接线安装牢固，线缆线皮无破损、无接磨。检查完成后填写附件2。\n6、受电弓检查，要求2018年2月10日前完成。\n接触网断电、挂接地线，列车断电状态下，目视检查受电弓接线无松动，线缆线皮无破损、无接磨。检查完成后填写附件2。\n7、烟雾报警功能测试，要求2018年2月10日前完成。\n列车有电状态下，每列电客车随机触发两个烟雾报警探测器，烟雾报警功能正常。检查完成后填写附件2。\n8、空压机、齿轮箱漏油检查，要求2018年2月10日前完成。\n1）升弓，激活列车，使空压机持续工作5分钟后再停机5分钟，降弓，列车断电后，目视检查空压机油位在规定刻度线范围内，无漏油情况。\n2）列车断电状态下，目视检查齿轮箱油位在规定刻度线范围内，无漏油情况。\n检查完成后填写附件2。\n9、牵引逆变器、辅助逆变器抽查，要求2018年2月10日前完成。\n抽查列车号为：705、713、721、735、743、1003。\n列车断电状态下，用四角钥匙打开PA箱、AB箱、PH箱箱盖，目视检查箱体内接线无松动，线缆外无皮磨损、无接磨，检查箱内各元器件/设备外观良好。检查完成后填写附件2。\n五、注意事项\n1、遵守公司、中心、车间的安全、质量和工艺要求。\n2、作业时按公司要求佩戴劳动保护用品。\n3、请作业人员在作业完成后依照填表要求填写记录表。\n\n附件1：7/10号线电客车设备防火状态专项作业记录表一\n附件2：7/10号线电客车设备防火状态专项作业记录表二\n\n检修三车间技术组\n2018年1月26日\n张培华\t审 核\t李侠\t批 准\t冯利平",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 567, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第010号",
                                      "ctiName": "关于7、10号线TCMS与牵引系统程序更新的通知",
                                      "detailed": "调度组、各班组：\n根据室技第004和009号通知，为解决7、10号线TCMS系统轮径值偏差大导致牵引系统封锁，牵引变流器MCM离线等问题，现需对TCMS、牵引软件进行升级，升级后VCU版本号为2.6，HMI版本号为2.5，DCUM版本号为0.0.2.11。\n具体作业要求如下：\n一、作业范围\n7号线：10701-10744列。10号线：11001-11006。\n二、作业人员及职责\nTCMS程序升级作业由四方完成，牵引程序升级作业由庞巴迪人员完成，班组人员配合进行确认。\n三、作业时间\n7号线首列车经过静态、试车线、末班车验证，正线运行1周后，进行5列车试刷验证1周后，进行批量刷新。\n10号线首列车经过静态、试车线、末班车验证，正线运行1周后，进行5列车批量刷新。\n每列车用时30分钟，3月15日前完成。\n四、改动内容\n1、当轮径差小于8mm时,MP1车收到的参考轴轮径值为当前设置轮径值，参考轴号为2，轮径有效位为1，M1、M2、MP2车收到的参考轴轮径值为0，参考轴号为0，轮径有效位为1。当轮径差大于或等于8mm时，牵引系统MP1车收到的参考轴轮径值为当前设置轮径值，参考轴号为2，轮径有效位为0，M1、M2、MP2车收到的参考轴轮径为0，参考轴号为0，轮径有效位为0；\n2、轮径值跳变后的轮径校验积分方式由双积分改为单积分。\n3、修改牵引系统过压吸收电阻的斩波电压和温度保护参数，解决地面能馈装置退出运行导致牵引变流器故障的问题。斩波电压由原来的1950V调整为1910V，过压保护开启电压由原来的1950V调整为1980V，关闭电压由原来的1900V调整为1930V；切除电制动的阀值由原来的450℃调整为410℃，延迟时间由30s变为2min。\n4、修改了牵引变流器的底层操作系统程序，解决偶报“牵引系统MVB 通讯故障”的问题。\n五、验证内容\n静态验证：\n1、确认HMI屏【设置】-【牵引设置】界面无【轮径复位按钮】。\n2、在HMI屏上将MP1车2轴轮径值设置为840，通过PTU连接牵引系统确认MP1车收到的参考轴轮径值为840，参考轴号为2，轮径有效位为1，M1、M2、MP2车收到的参考轴轮径值为0，参考轴号为0，轮径有效位为1，与HMI屏【检修】-【端口】界面显示的参考轴轮径、参考轴轴号、轮径有效信息一致。\n3、在HMI屏上将MP1车2轴轮径值设置为831，HMI屏报出3级故障：设定轮径值超限。故障提示：维持运行，回库检修。通过PTU连接牵引系统确认MP1车收到的参考轴轮径值为831，参考轴号为2，轮径有效位为0，M1、M2、MP2车收到的参考轴轮径为0，参考轴号为0，轮径有效位为0，与HMI屏【检修】-【端口】界面显示的参考轴轮径、参考轴轴号、轮径有效信息一致。通过HMI屏【检修】-【端口】界面查看相关信息：\n端口号\t49A\t4CA\t4DA\t48A\n字3\t2车参考轴轮径\t3车参考轴轮径\t4车参考轴轮径\t5车参考轴轮径\n字4\t2车参考轴轴号\t3车参考轴轴号\t4车参考轴轴号\t5车参考轴轴号\n字13\t2车轮径有效\t3车轮径有效\t4车轮径有效\t5车轮径有效\n\n动态验证：\n记录当前牵引系统各轴轮径值。\n在 HMI屏上将MP1车2轴轮径值设置为831（大于8），确认牵引系统不封锁牵引，牵引系统不报故障，列车牵引至40km/h惰行10s以上（根据线路条件），停车后在牵引系统及HMI屏端口界面确认其他轴轮径不进行校准，轮径值维持原值。\n在HMI屏上将MP1车2轴轮径值设置为825（大于12），确认牵引系统不封锁牵引，牵引系统不报故障，列车牵引至40km/h惰行10s以上（根据线路条件），停车后在牵引系统及HMI屏端口界面确认其他轴轮径不进行校准，轮径值维持原值。\n在HMI屏上将MP1车2轴轮径值设置为833，列车惰行、牵引、制动多次更换，停车后在牵引系统及HMI屏端口界面确认其他轴轮径向833趋近（840-833之间），不低于833。\n在HMI屏上将MP1车2轴轮径值设置为833，列车牵引至 40km/h 惰行10s以上（根据线路条件），停车后在牵引系统及HMI屏端口界面确认其他轴轮径向833趋近（840-833之间），不低于833。多次重复直至轮径接近 833。\n将MP1车2轴轮径值恢复设置为840，列车牵引至40km/h惰行10s以上（根据线路条件），多次执行列车牵引至40km/h惰行10s停车，直到其他所有轴轮径接近840。\n通过HMI屏端口界面查看牵引系统反馈的轮径值，对应如下表： \n端口号\t492\t4C2\t4D2\t482\n字10\t2车1轴\t3车1轴\t4车1轴\t5车1轴\n字11\t2车2轴\t3车2轴\t4车2轴\t5车2轴\n字12\t2车3轴\t3车3轴\t4车3轴\t5车3轴\n字13\t2车4轴\t3车4轴\t4车4轴\t5车4轴\n六、班组确认内容\n1、升级完后确认两端VCU、HMI、DCU/M程序版本分别为2.6、2.5、0.0.2.11；\n2、确认首列车验证结果正确；\n3、升级完后确认网络通信界面正常；\n4、确认柜门锁闭良好；\n七、其他\n1、作业完毕后，请填写记录表。\n2、本次升级不会对列车安全运行产生影响，若软件升级后导致列车异常，需将程序退回原版本程序。\n八、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车。\n检修三车间技术组\n2018年1月25日\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 568, "dataType": "1", "checkTechInfoNo": "检三技 [2017] 第107号",
                                      "ctiName": "关于10号线电客车PIDS系统广播音量设置的通知",
                                      "detailed": "调度组、各班组：\n根据客运部1712200266号《关于调整10号线列车广播音量的工作联系单》的和室  技[2017]第120号相关要求，现需对10号线电客车PIDS系统广播和媒体音量进行如下调整，具体作业要求如下。\n一、作业范围\n10号线：11001-11006。\n二、作业人员及职责\n班组人员负责PIDS系统音量设置操作，并进行确认。\n三、作业时间\n12月30日前完成。\n四、作业内容\n1、列车投入主控，操作主控端HMI屏进入设置-PIDS设置-音量设置对广播报站音量进行设置。\n2、广播报站音量设置为75。\n3、设置完成后待车辆正线试运营时，由检修班组人员使用分贝仪测试各音量的分贝值并做好记录，报站音量对应分贝值参考范围如下：\n广播报站分贝值：77-84dB。\n五、注意事项\n除广播报站外的其他音量不做调整。\n\n\n\n\n\n检修三车间技术组\n2017年12月29日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 580, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第014号",
                                      "ctiName": "关于10号线电客车广播控制盒程序更新的通知",
                                      "detailed": "前期10号线电客车司机对讲出现无法建立对讲和对讲失效等故障，经厂家分析是由于对讲时声卡驱动异常导致，为解决此问题，根据《室 技[2018]第018号-关于4号线电客车目的地显示屏程序及10号线广播控制盒程序更新的通知》要求，对10号线电客车广播控制盒程序进行更新",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 584, "dataType": "1", "checkTechInfoNo": "检三技[2018]第015号",
                                      "ctiName": "关于7、10号线电客车车门、警惕等控制原理接线位置整改的通知",
                                      "detailed": "调度组、各班组：\n7/10号线电客车自运用以来，发现有部分设计缺陷，具体问题情况如下：\n1）7/10号线电客车在主控端断开车门控制空开后，操作零速旁路开关后，仍能进行开关门作业。\n2）10号线电客车在非信号控车下，信号模式开关转至“ATO”时会旁路警惕功能，不符合警惕功能的设计技术需求。\n3）10号线电客车应信号专业需求，在自动折返时车辆需取消后退限速的限制。\n4）7/10号线电客车PH箱保护盖的监视功能在设计联络阶段未要求采集相关信号。\n经中心组织四方股份进行分析后，确认为电路设计缺陷，现对相关控制原理接线位置进行整改，具体要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006\n二、作业人员及职责\n由四方售后人员进行整改，检修班组进行配合及确认。\n三、作业条件\n车辆在无电状态下作业整改，在有电状态下试验验证。\n四、作业时间\n7号线首列车通过静态验证，正线运行1周后，增改4列车验证1周后，进行批量整改。\n10号线首列车通过静态验证，正线运行15天后，进行5列车批量整改。\n7号线每列车用时约2小时，10号线每列车用时约4小时。\n五、作业内容与要求\n1、7号线列车\n司机室电器柜\n增加 8134（XT34/66A-SKZV/24）；\n删除原接线8134（XT34/67C-SKZV/24）；\nXT34/66-XT34/67 增加短接片，短阳极；\nMP车电器柜\n取消MP车XT41/41- XT41/42的短接片。\n2、10号线列车\n司机室电器柜\n增加 8134（XT34/67D-SKZV/24）；\n删除原接线 8134（XT34/67C-SKZV/24）；\n增加921（KAAOM/B1-KANRM2/A2）；\n增加922A（KANRM2/B2-XT32/55A）；\n删除原接线922A（KAAOM/B1- XT32/55A）；\n增加 31E（XT32/29B-KAAR1/C3）；\n增加 32（KAAR1/C2-KAR/A1）；\n删除原接线32E（XT32/29B-KAR/A1）。\nMP车电器柜\n取消MP车XT41/41- XT41/42的短接片。\n具体整改方案请参考附件3《成都地铁7、10号线车辆车门控制警惕控制原理优化说明》。\n六、验证内容\n1、车门控制（7/10号线）\n1）闭合TC车司机室电器柜断路器，切除ATP，确认柜内零速继电器KAZV1、KAZV2得电；\n2）操作激活端左右侧开关门按钮，车门开关正常，HMI查看所有车门状态与操作一致；\n3）模拟零速故障：断开司机室电器柜内XT32的83与84间的短连片，确认KAZV1、KAZV2失电。激活端操作开关门确认车门无动作；\n4）操作零速旁路开关至强制位，操作左右侧开关门车门正常动作；\n5）恢复XT32的83/84间的短连片，恢复零速旁路至正常位，断开司机室电器柜内车门控制断路器1（QFTD1），操作开关门无动作。打零速旁路并操作开关门，车门无动作\n6）恢复车门控制断路器、零速旁路开关。\n2、警惕控制（10号线）\n1）切除ATP，将司机操纵台的信号模式开关置于“ATO位”，主控端缓解停放制动，将司控器方向手柄置于前向，级位手柄置于惰行位，按下并松开司机警惕装置，蜂鸣器鸣响，3S后车辆施加紧急制动。\n2）恢复停放制动。\n七、班组确认内容\n1、整改完成后确认接线正确，牢固，新增线路的绑扎到位；\n2、根据验证内容按步骤进行相关验证；\n3、确认柜门锁闭良好；\n八、其他\n1、作业完毕后，请填写记录表。\n2、如整改后出现功能异常，需立即中止整改并将所有线路改回原接线状态。\n九、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、严禁带电进行接线操作；\n5、注意确保车辆可靠停稳、防止溜车。\n检修三车间技术组\n2018年2月5日\n\t审 核\t\t批 准\t",
                                      "ctiVehicleNo": "11005", "combineRepairTime": " ", "tempRepairTime": "1",
                                      "departCode": "11442"},
                                     {"checkTechInfoId": 586, "dataType": "1", "checkTechInfoNo": "检三技[2018]第015号",
                                      "ctiName": "关于7、10号线电客车车门、警惕等控制原理接线位置整改的通知",
                                      "detailed": "调度组、各班组：\n7/10号线电客车自运用以来，发现有部分设计缺陷，具体问题情况如下：\n1）7/10号线电客车在主控端断开车门控制空开后，操作零速旁路开关后，仍能进行开关门作业。\n2）10号线电客车在非信号控车下，信号模式开关转至“ATO”时会旁路警惕功能，不符合警惕功能的设计技术需求。\n3）10号线电客车应信号专业需求，在自动折返时车辆需取消后退限速的限制。\n4）7/10号线电客车PH箱保护盖的监视功能在设计联络阶段未要求采集相关信号。\n经中心组织四方股份进行分析后，确认为电路设计缺陷，现对相关控制原理接线位置进行整改，具体要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006\n二、作业人员及职责\n由四方售后人员进行整改，检修班组进行配合及确认。\n三、作业条件\n车辆在无电状态下作业整改，在有电状态下试验验证。\n四、作业时间\n7号线首列车通过静态验证，正线运行1周后，增改4列车验证1周后，进行批量整改。\n10号线首列车通过静态验证，正线运行15天后，进行5列车批量整改。\n7号线每列车用时约2小时，10号线每列车用时约4小时。\n五、作业内容与要求\n1、7号线列车\n司机室电器柜\n增加 8134（XT34/66A-SKZV/24）；\n删除原接线8134（XT34/67C-SKZV/24）；\nXT34/66-XT34/67 增加短接片，短阳极；\nMP车电器柜\n取消MP车XT41/41- XT41/42的短接片。\n2、10号线列车\n司机室电器柜\n增加 8134（XT34/67D-SKZV/24）；\n删除原接线 8134（XT34/67C-SKZV/24）；\n增加921（KAAOM/B1-KANRM2/A2）；\n增加922A（KANRM2/B2-XT32/55A）；\n删除原接线922A（KAAOM/B1- XT32/55A）；\n增加 31E（XT32/29B-KAAR1/C3）；\n增加 32（KAAR1/C2-KAR/A1）；\n删除原接线32E（XT32/29B-KAR/A1）。\nMP车电器柜\n取消MP车XT41/41- XT41/42的短接片。\n具体整改方案请参考附件3《成都地铁7、10号线车辆车门控制警惕控制原理优化说明》。\n六、验证内容\n1、车门控制（7/10号线）\n1）闭合TC车司机室电器柜断路器，切除ATP，确认柜内零速继电器KAZV1、KAZV2得电；\n2）操作激活端左右侧开关门按钮，车门开关正常，HMI查看所有车门状态与操作一致；\n3）模拟零速故障：断开司机室电器柜内XT32的83与84间的短连片，确认KAZV1、KAZV2失电。激活端操作开关门确认车门无动作；\n4）操作零速旁路开关至强制位，操作左右侧开关门车门正常动作；\n5）恢复XT32的83/84间的短连片，恢复零速旁路至正常位，断开司机室电器柜内车门控制断路器1（QFTD1），操作开关门无动作。打零速旁路并操作开关门，车门无动作\n6）恢复车门控制断路器、零速旁路开关。\n2、警惕控制（10号线）\n1）切除ATP，将司机操纵台的信号模式开关置于“ATO位”，主控端缓解停放制动，将司控器方向手柄置于前向，级位手柄置于惰行位，按下并松开司机警惕装置，蜂鸣器鸣响，3S后车辆施加紧急制动。\n2）恢复停放制动。\n七、班组确认内容\n1、整改完成后确认接线正确，牢固，新增线路的绑扎到位；\n2、根据验证内容按步骤进行相关验证；\n3、确认柜门锁闭良好；\n八、其他\n1、作业完毕后，请填写记录表。\n2、如整改后出现功能异常，需立即中止整改并将所有线路改回原接线状态。\n九、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、严禁带电进行接线操作；\n5、注意确保车辆可靠停稳、防止溜车。\n检修三车间技术组\n2018年2月5日\n\t审 核\t\t批 准\t",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 590, "dataType": "1", "checkTechInfoNo": "检三技[2018]第016号",
                                      "ctiName": "关于7、10号线客室照明电源模块整改的通知",
                                      "detailed": "\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\t调度组、各班组：\n针对7、10号线运营以来多次闪报客室照明故障的问题，经调查为电源模块内部功率模块控制板与铝基板连接引针出现脱焊，导致上电电路未正常工作，造成电源模块输出不稳定出现闪报现象。厂家已改进功率模块焊接工艺，为解决该问题，计划将对7、10号线电客车客室照明电源模块进行批量更换。\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业人员及职责\n由厂家售后人员进行整改，检修班组进行配合及确认。\n三、作业条件\n车辆在无电状态下作业整改，在有电状态下试验验证。\n四、作业时间\n7、10号线各选取一列车进行整改验证，待近期现场再到货3列车整改件后追加3列车试整改。从首列车试改开始累计跟踪3个月后，若运行状态良好，则开展批量整改。\n每列车用时约5小时，请调度结合生产合理安排整改。\n五、作业内容与要求\n1、更换前先确认新件（共计24块）侧面的合格证检验日期为2018年2月之后，且合格证旁的拨码器1/2均置于ON位。\n \n2、打开顶板，为了拆装方便建议以下图所示顺序进行拆除，先拆除右侧第一个模块侧面的螺栓，再拆除两端的两个插头（螺栓紧固），拆除插头时须用手固定模块保证线插不受力。\n\n再如下图所示顺序依次安装新模块，先固定两端插头后再安装模块整体。\n\n六、验证内容\n1、列车升弓供电，打开客室照明\n2、确认HMI无照明相关故障，所有客室照明亮度正常\n3、每节车单独断合照明电源1和2，照明亮度短暂变暗后能够恢复正常。\n七、班组确认内容\n1、整改完成后确认模块两端的接线牢固；\n2、电源模块的四个固定螺栓紧固到位并画防松线；\n3、确认柜门、顶板锁闭良好。\n八、其他\n1、作业完毕后，请填写记录表。\n2、如整改后出现功能异常，需立即中止整改并换回原电源模块。\n九、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、严禁带电进行接线操作；\n5、注意确保车辆可靠停稳、防止溜车；\n6、打开顶板时注意防止顶板砸人。\n\n\n\n检修三车间技术组\n2018年2月23日\n编 制\t\t审 核\t\t批 准\t\n签收\t\n7号线班组：（手签版崔家店调度室留存）\n\n日检一班：      日检二班：      日检三班：      日检四班：\n\n\n月修一班：      月修二班：      定修一班：      定修二班：\n\n调度组：\n\n10号线班组：（手签版金花调度室留存）          \n\n金花检修班：         调 度 组：\n\n首做列车\t\t首做确认工程师\t\n完工确认工程师\t\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 596, "dataType": "1", "checkTechInfoNo": "检三技[2018] 第17号",
                                      "ctiName": "关于7、10号线电客车开展2018年春检工作的通知",
                                      "detailed": "调度组、各班组：\n为确保冬春过渡期间，汛期、雷雨季节到来之前，设备运行平稳，防雷设备设施安全可靠，防洪隐患得到及时整治，防汛设备、防汛物资准备到位，为全年设备安全运行奠定基础。根据《室技[2018]第022号-关于开展2018年春检工作的通知》要求，现需对7、10号线电客车开展春检工作，具体要求如下：\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业人员及职责\n班组人员进行作业及确认。\n三、作业时间\n1、空调专检要求于4月30日前完成，其余项目要求3月31日前完成检查。\n2、结合月检及以上修程完成。\n四、作业内容与要求\n1、空调检查\n7号线车辆按照《地铁7号线SFM45型电客车均衡修规程》中空调夏季专检内容进行；10号线车辆按照《地铁10号线SFM46型电客车均衡修规程》中空调夏季专检内容进行，并填写相应记录册。\n2、避雷器专项检查\n按照《检修三车间2018-001号工艺文件-7、10号线电客车避雷器参数测试单项工艺》要求开展作业。\n3、刮雨器功能检查\n（1）检查喷淋功能，应正常无堵塞。\n（2）确认刮雨器摆臂无松动、裂纹等异常；\n（3）检查刮雨器雨刷无松动、脱落，卡扣紧固。\n（4）无电状态下检查刮雨器开关档位接线无松动，开关外观无异常。\n（5）检查刮雨器快速、低速、喷淋、洗车位、停止复位功能均正常，雨刷喷淋点能完全喷射到刷片刮刷的区域内（不可干刮）。\n4、防汛检查\n（1）清查防汛物资，确认防汛物资帐物一致，对损坏的物资进行申报，及时补充。\n（2）对川师车辆段、中环停车场及金华线上检修库区域可能存在的隐患进行全面排查。\n注：防汛检查由安全工程师牵头并记录，不在本通知中记录。\n五、作业风险点分析及应对措施\n1、避雷器测量工具不熟练、接线不规范造成设备漏检、误检。\n避免措施：工具使用应由熟练使用的人员或者班长把关；试验时，接线等操作应由不同的人复查，拿不准的地方要让熟练使用人员或者班长确认。\n2、刮雨器检修时，高架股道存在安全隐患。\n避免措施：必须使用刮雨器检修平台进行作业，不得心存侥幸；请质检人员加强检查。\n六、安全注意事项\n？ 1、使用福禄克高压绝缘电子测试仪、ZVA-4型压敏参数测试仪或者摇表进行避雷器参数测量时，严禁在测量设备带电的情况下操作测量接头/夹钳！\n？ 2、操作测试接头/夹钳时，请先切断测试设备电源！\n3、春检中涉及较多的登高作业，请注意安全。\n4、作业时做好防护作业，包括劳保用品，安全设备。\n5、相关作业规范，请遵照车间管理规定执行。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,G",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 597, "dataType": "1", "checkTechInfoNo": " 检三技 [2018] 第018号",
                                      "ctiName": "关于7号线电客车电子地图程序及10号线广播控制盒程序更新的通知",
                                      "detailed": "调度组、各班组：\n为解决7号线电客车电子地图页面切换时黑屏和10号线电客车司机对讲、紧急对讲声音较小的问题，需对7号线电客车电子地图和10号线电客车广播控制盒程序进行更新，具体要求如下：\n一、作业范围\n7号线：10701-10744列。先更新5列车，验证2周后若效果较好，则批量进行更新；\n10号线：11001-11006列。先更新2列车，验证1周后若效果较好，则批量进行更新。\n二、作业人员及职责\n    厂家售后人员：负责程序更新作业，做好确认；\n车间检修班组：配合并进行确认。\n三、作业时间：每列车用时约30分钟，请调度结合生产合理安排整改。\n四、作业内容\n（一）7号线电客车电子地图程序更新\n1、用携带新版电子地图程序的笔记本电脑接入客室交换机对电子地图程序进行更新；（旧版程序版本号：V1.1.63；新版程序版本号：V1.1.66）\n2、程序更新过程中或更新完成后，若出现异常情况，则需将程序回退至旧版程序V1.1.63;\n（二）10号线电客车广播控制盒程序更新\n1、用携带新版电子地图程序的笔记本电脑接入客室交换机对广播控制盒程序进行更新；（旧版程序版本号：590-PA-BCU-app-1-20170831；新版程序版本号：590-PA-BCU-app-1-20180222）\n2、程序更新过程中或更新完成后，若出现异常情况，则需将程序回退至旧版程序590-PA-BCU-app-1-20170831；\n五、班组确认内容\n1、程序更新完成后，确认版本号。\n2、电子地图升级后将报站从环线报站模式切换到非环线报站，确认电子地图显示正常。\n3、广播控制盒程序更新完成后，10次以上触发司机对讲和紧急对讲，确认司机对讲功能及声音大小正常。\n4、电气柜门锁闭良好。\n5、作业完成后，班组人员填写作业记录表（附表1，附表2）\n五、安全注意事项\n1.遵守公司、中心、车间的其他安全和工艺要求；\n2.现场工器具摆放整齐规范；\n3.劳保用品穿戴整齐。\n4.程序更新过程中列车不得断电\n附件1：10号线广播控制盒程序更新记录表\n附件2：7号线电客车电子地图程序更新记录表\n\n\n\n检修三车间技术组\n2018年3月7日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 603, "dataType": "1", "checkTechInfoNo": " 检三技[2018]第019号",
                                      "ctiName": "关于7、10号线PIDS系统普查的通知",
                                      "detailed": "调度组、各班组：\n目前7、10号线已开通运行半年，为降低7、10号线PIDS故障率，需对PIDS系统设备进行普查整改，具体要求如下：\n一、作业范围\n7号线：10701-10744列。\n10号线：11001-11006列。\n二、作业人员及职责\n    厂家售后人员：负责普查整改作业，做好确认。\n车间检修班组：配合并进行确认。\n三、作业时间：每列车用时约30分钟，请调度结合生产合理安排整改。\n四、作业内容\n1、广播控制盒手麦的安装方式，检查手麦安装牢固，底部无松动。\n2、检查各摄像头水印与车型实际位置一致。\n3、检查NVR网络状态正常，视频存储数据无异常。\n4、检查广播主机X3、X4面板的螺栓无松动。\n五、班组确认内容\n1、广播控制盒手麦接线无松动。\n2、摄像头水印正确。\n3、NVR网络正常，可以正常下载视频。\n4、X3、X4面板螺栓无松动。\n5、作业完成后，班组人员填写作业记录表（附表1，附表2）\n六、安全注意事项\n1.遵守公司、中心、车间的其他安全和工艺要求；\n2.现场工器具摆放整齐规范；\n3.劳保用品穿戴整齐；\n附件1：7号线PIDS系统普查记录表\n附件2：10号线PIDS系统普查记录表\n\n\n\n检修三车间技术组\n2018年3月12日\n编 制\t\t审 核\t\t审   批\t\n\n\n签收\t7号线班组：（手签版崔家店调度室留存）\n\n日检一班：      日检二班：      日检三班：      日检四班：\n\n月修一班：      月修二班：      定修一班：      定修二班：\n\n调度组：\n\n10号线班组：（手签版金花调度室留存）\n金花检修班组：",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 609, "dataType": "1", "checkTechInfoNo": "检三技[2018]第021号",
                                      "ctiName": "关于增加及优化7、10号线电客车PIDS系统日志记录功能的通知",
                                      "detailed": "调度组、各班组：\n针对近期7、10号线电客车PIDS系统出现司机对讲、报站以及人工广播等相关故障，为能够进一步查明故障原因，根据室技[2018]第028号的通知要求，需增加及优化现有的日志记录功能（升级广播控制盒及功率放大器的程序，在监控主机上部署软件），具体要求如下：\n一、作业范围\n7号线：10701-10744列。先整改2列车，验证1周后若无异常，则扩大整改到10列再验证1周，若无异常则根据专工通知开展批量整改；\n10号线：11001-11006列。先整改2列车，验证1周后若无异常，则根据专工通知开展批量整改；\n二、作业人员及职责\n    厂家售后人员：负责程序更新作业，做好确认；\n车间检修班组：配合并进行确认。\n三、作业时间：每列车用时约30分钟，请调度结合生产合理安排整改。\n四、作业内容\n1、用携带新版广播控制盒程序的笔记本电脑接入客室交换机对广播控制盒程序进行更新，升级前后程序版本号如下：\n7号线旧版程序版本号：589-PA-BCU-app-1-20170831，7号线新版程序版本号：589-PA-BCU-app-1-20180316；\n10号线旧版程序版本号：590-PA-BCU-app-1-20180222，10号线新版程序版本号：590-PA-BCU-app-1-20180315。）\n2、将携带CD-BCU-Data-Record-Serve软件的笔记本电脑接入客室交换机，对监控主机部署该软件；\n3、用携带新版功率放大器程序的笔记本电脑接入客室交换机对功率放大器程序进行更新，升级前后程序版本号如下：\n7号线旧版程序版本号：589-PA-EAMP-app-1-20171202，7号线新版程序版本号：589-PA-EAMP-app-2-20180316；\n10号线旧版程序版本号：590-PA-EAMP-app-1-20171202，10号线新版程序版本号：590-PA-EAMP-app-2-20180315。）\n4、程序更新过程中或更新完成后，若出现异常情况，则需将各程序回退至旧版程序;\n五、班组确认内容\n1、程序更新完成后，确认版本号。\n2、司机对讲、紧急对讲、人工广播及广播报站等功能正常；\n3、电气柜门锁闭良好。\n4、作业完成后，班组人员填写作业记录表（附表1，附表2）\n六、安全注意事项\n1.遵守公司、中心、车间的其他安全和工艺要求；\n2.现场工器具摆放整齐规范；\n3.劳保用品穿戴整齐。\n4.程序更新过程中列车不得断电。\n\n附件1：10号线广播控制盒程序更新记录表\n附件2：7号线广播控制盒程序更新记录表\n\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 610, "dataType": "1", "checkTechInfoNo": "检三技[2018]第022号",
                                      "ctiName": "关于7、10号线CCU-D软件升级到版本1.1.2.7的通知",
                                      "detailed": "针对704、708和713列频繁报“CCU-D故障”的问题，牵引厂家在前期做了如下的工作：1）更换报故障的CCU-D硬件；2）更新CCU-D应用层软件；3）刷新临时软件；4）测试整车MVB通讯质量。综合前期的测试和处理结果，厂家拟对CCU-D软件进行升级。新软件优化了CCU-D的底层程序，增强了操作系统的稳定性，同时还增加了部分监控信号。\n为此，根据中心下发的室技[2018]第026号《关于7、10号线CCU－D软件升级到1.1.2.7版本的通知》，车间将对所有电客车的CCU-D软件进行升级到1.1.2.7。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 613, "dataType": "1", "checkTechInfoNo": "检三技[2018]第024号",
                                      "ctiName": "关于7、10号线电客车空调控制器MVB网卡整改的通知",
                                      "detailed": "调度组、各班组：\n针对7、10号线电客车空调与TCMS通讯异常问题，现对7、10号线所有电客车空调控制器MVB网卡进行批量整改。本次MVB网卡整改主要对网卡波形发送电路阻容匹配进行优化，避免中继器将不符合条件的从帧波形过滤后未转发至列车总线，导致VCU检测不到空调控制器从帧从而显示通讯异常。\n一、作业范围\n10号线：11001-11006列\n7号线：10701-10744列（除前期10列试改车:703、708、712、713、719、723、724、731、732、733）\n二、作业人员及职责\n由广州中车厂家人员负责整改作业及状态、功能确认，班组人员做好配合及二次确认。\n三、作业时间\n每列车需要3.5小时，请调度结合生产合理安排整改。\n四、作业内容\n1、打开空调控制柜，取下控制器各接线及禁锢螺栓，取出旧版MVB网卡。\n2、更换新版MVB网卡。\n3、重新安装好控制器各接线及紧固螺栓。\n五、班组确认内容\n1、检查空调控制器各接线是否连接正确牢固、紧固螺栓是否安装牢固。\n2、检查空调功能正常，在HMI屏上操作“通风”、“全冷”、“全暖”等空调模式，该节车空调能正常工作，全冷工况时压缩机全部启动。\n3、作业人员及配合人员须共同确认设备安装牢固，作业现场出清，空调控制柜柜门锁闭。\n4、作业完成后，班组人员填写作业记录表。\n六、安全注意事项\n1、严格按照公司、中心的相关安全和工艺、质量要求进行作业。\n2、作业时做好防护作业，包括劳保用品，安全设备。\n3、相关作业规范，请遵照车间管理规定执行。\n\n\n\n\n\n检修三车间技术组\n2018年3月23日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 617, "dataType": "1", "checkTechInfoNo": "检三技[2018]第025号",
                                      "ctiName": "关于7、10号线电客车司机室门同步杆固定座及螺栓整改的通知",
                                      "detailed": "调度组、各班组：\n7号线在运行期间，出现司机室门同步杆固定座的安装螺栓有断裂、松动，该问题有导致司机室门不好关闭、甚至无法正常关闭的隐患。经分析为现有结构采用固定座和垫板分体式结构、紧固方式为沉头螺栓紧固的设计，因沉头螺栓螺纹过度区较长，且90度沉头螺栓不能可靠紧固等原因造成螺栓断裂或松动，现根据《室  技[2018]第011号关于7、10号线电客车司机室门同步杆固定座及螺栓整改的通知》相关要求，决定对7、10号线司机室门同步杆固定座及螺栓进行更换整改，具体要求如下：\n一、作业范围\n7号线：701-744列（分阶段分批量完成）\n10号线：1001-1006列（分阶段分批量完成）\n二、作业人员及职责\n由4名康尼厂家人员负责整改作业及状态、功能确认，1名班组车门专员做好配合及二次确认。\n三、作业时间\n每列车需要4小时，请调度结合生产合理安排整改。\n第一阶段：7号线2列、10号线1列进行试整改，要求于2018年3月31日前完成，验证1月，于4月30日完成验证，进入第二阶段；\n第二阶段：验证无异常后扩大试整改范围，7号线增加10列车（共计12列）、10号线增加1列车（共计2列），要求于2018年5月7日前完成整改，验证1月，于6月月7日完成验证，进入第三阶段；\n第三阶段：试整改无异常后填写附表1、附表2《电客车整改项目实施效果评价表》，经审批同意后进行批量整改，要求于2018年6月30日前完成7、10号线所有车辆的整改。  \n若整改或验证过程中发现问题则立即终止整改。\n四、作业内容\n1、由康尼售后人员对7/10号线司机室门同步杆支架左右固定板组件MS560DW02-30002L/R（分体式结构）更换为MS570DW01L/R-30003（整体式结构）,原螺栓“沉头螺钉”更换为“圆柱头螺钉”，并增加“蝶形垫圈”，班组员工做好配合确认工作。\n  \n图1.整改前                                 图2.整改后\n2、同步杆支架左右固定板组件更换完成后，由班组人员按照车间司机室门开关状态确认方式，确认车门状态良好，并填写《附件1-7、10号线司机室门同步杆固定座及螺栓整改后确认记录表》。\n五、班组确认内容\n1、司机室同步杆支架左右固定板组件安装状态良好，紧固件无松动，防松线清晰、整齐。\n2、作业拆下的各门机构紧固件恢复安装状态良好，紧固件无松动，无松动，防松线清晰、整齐。\n3、司机室侧门各尺寸正常，开关门状态良好：\n7号线要求大、小力度关门及甩关至少各3次，均要求能正常关门；\n10号线为司机室门为电动塞拉门，开关门10次，要求打开通风，同时在司机室门快关到位时向外施加适当推力能正常关门，开关门顺畅，无抖动、卡滞等异常；\n4、每次开关司机室门时全关闭灯及HMI屏显示正常，行程开关动作良好、无卡滞。\n六、安全注意事项\n1、严格按照公司、中心的相关安全和工艺、质量要求进行作业。\n2、作业时做好防护作业，包括劳保用品，安全设备。\n3、相关作业规范，请遵照车间管理规定执行。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 621, "dataType": "1", "checkTechInfoNo": "检三技【2018】-第026号",
                                      "ctiName": "关于对10号线电客车牵引电机加润滑油脂的通知",
                                      "detailed": "根据牵引厂家《成都7&10项目MJA250-23型牵引电机维护计划》的要求，且根据《成都项目MJA250-23牵引电机维护手册》，现决定对10号线电客车牵引电机轴承进行加油。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,R,BJ,XC",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 623, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第027号",
                                      "ctiName": "关于7、10号线电客车2018-002号检技通回退的通知",
                                      "detailed": "调度组、各班组：\n经四方设计核实，因空压机三相检测继电器选型问题，7/10号线电客车空压机并不具备初上电延时启动功能。根据现型号三相检测继电器工作特性，将继电器重新调回延时断开位（即OFF DELAY位）能有效防止因三相电压短时波动导致空压机停止工作的故障，故现需对2018-002号检技通执行的整改进行回退，具体要求如下：\n一、作业范围\n7号线：10701-10744列\n   10号线：11001-11006列\n二、作业时间\n4月30日前完成。\n三、作业人员及职责\n由四方售后人员进行三相检测继电器设置回退工作，由车间检修班组进行调整后的状态及功能确认。\n四、作业条件\n作业时间：可结合日检、月检进行作业。每列车作业约30分钟。\n  作业工具：小一字螺丝刀、四角钥匙。\n五、作业内容\n1、用四角钥匙分别打开TC1车和TC2车空压机控制箱，擦掉三相检测继电器（KACP）上电压旋钮上的防错位标记，并将旋钮旋至“OFF DELAY”侧的380刻度处；\n\n2、确认三相检测继电器上时间旋钮的设置值：TC1车设置为3s，TC2车设置为6s。若不正确，擦掉三相检测继电器上的时间旋钮上的防错位标记，并将旋钮旋至指定值。旋钮如下图红色框内所示。\n\n3、划上新的防错位标记，关闭空压机控制箱柜门。\n六、班组确认内容\n1、确认两端三相检测继电器设定值符合要求；\n2、确认两端空压机控制箱柜门锁闭到位；\n3、电客车上电后，强泵启动空压机连续运行2分钟，未报空压机缺相故障。\n七、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、注意确保车辆可靠停稳、防止溜车；\n5、调整时间旋钮是列车禁止投电，设置完成后需确认各设备箱盖锁闭良好。\n八、其他\n    调度组、各班组应对该检技通进行学习，并填写学习记录。\n\n\n\n                                    检修三车间技术组\n                                                2018.4.4",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 625, "dataType": "1", "checkTechInfoNo": "检三技[2018]第028号",
                                      "ctiName": "关于普查7.10号线司机室媒体服务器时间的通知",
                                      "detailed": "调度组、各班组：\n针对近期7、10号线电客车PIDS系统出现LCD时间和HMI或CCTV屏显示时间不一致故障，现普查媒体服务器（LCD时间通过媒体服务器校时）硬件时间和系统时间（CCTV屏显示时间），具体要求如下：\n一、作业范围\n7号线：10701-10744列。\n10号线：11001-11006列。\n二、作业人员及职责\n    厂家售后人员：负责普查作业，做好确认；\n车间检修班组：配合并进行确认。\n三、作业时间：每列车用时约10分钟，请调度结合生产合理安排整改。\n四、作业内容\n1、用携带可查看媒体服务器程序的笔记本电脑接入客室交换机，查看硬件时间和系统时间，如图所示：\n\n\n\n\n            硬件时间                                    系统时间（CCTV屏显示时间） \n2、若两者时间不一致，则通过媒体服务器程序同步即可。\n五、班组确认内容\n1、普查完成后，确认硬件时间和系统时间显示时间一致；\n2、CCTV屏各画面切换正常，显示正常；\n3、电气柜门锁闭良好；\n4、作业完成后，班组人员填写作业记录表（附表1）\n六、安全注意事项\n1.遵守公司、中心、车间的其他安全和工艺要求；\n2.现场工器具摆放整齐规范；\n3.劳保用品穿戴整齐。\n4.普查过程中列车不得断电。\n附件1：7.10号线司机室媒体服务器时间普查统计表\n\n检修三车间技术组\n2018年4月8日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 629, "dataType": "1", "checkTechInfoNo": "检三技 [2018] 第030号",
                                      "ctiName": "关于优化10号线电客车司机室后端门锁闭原理的通知",
                                      "detailed": "\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\n\t调度组、各班组：\n因10号线电客车后端门电磁锁故障率偏高，主要原因为司机室后端门电磁锁常得电，当司机室与客室压差过大或闭门器关门力不足时，电磁锁锁体和锁板在门未关闭到位的情况下就吸合，导致门关到位行程开关未被触发，HMI屏上显示门未关闭故障，司机换端后发现此故障需到另一端司机室检查确认。为保障电磁锁锁闭可靠，现计划对10号线电客车司机室后端门的锁闭原理进行优化改造，将现有的门关到位行程开关ZCP29（触点类型：2NC）更换为ZCP39(触点类型：2NC+1NO)，即在电磁锁控制回路中串联一组常开触点，只有在门关到位行程开关被触发后电磁铁才得电吸合，确保后端门实际锁闭状态和HMI屏显示信息一致，具体内容如下：\n一、作业范围\n10号线：11001-11006列。\n二、作业人员及职责\n    厂家及售后人员：负责后端门锁闭电路的整改；\n车间检修班组：配合并进行确认。\n三、作业时间\n每列车用时约90分钟，请调度结合生产合理安排整改。先选取1列车进行试整改，上线跟踪验证1个月无异常后进行评价，经审批同意后进行批量整改。\n四、作业内容\n1、关闭后端门电源，拆下后端门限位开关防护盖板，并拆下限位开关，如图1所示：\n \n图1 拆防护盖板                图2 及限位开关 \n2、拆除原ZCP29限位开关的四条线路，对线进行包扎绝缘处理。\n3、对改款ZCP39的限位开关安装在原ZCP29限位开关位置并进行布线，具体布线情况如下：\n（1）ZCP39限位开关新增两条线路，以控制后端门的有电与无电，具体方式见图3所示；\n\n图3 zcp39限位开关\n（2）打开司机室灯顶板，从限位开关位置出发，从司机室灯顶板走线至电器柜内，如图4所示；\n\n图4 司机室灯顶板走线示意图\n（3）打开司机室电气柜空气开关面板，原XT31线排中线号432L3？43D线更换成新线，原XT31线排中线号441B？53C更换成新线，原有走线包扎绝缘处理，如图5所示。\n\n图5 电气柜空气开关面板内走线示意图\n（4）打开司机室电气柜客室柜门，原XT36线排中线号4263？54A更换成新线，原XT34线排中线号5302E？39C更换成新线，原有走线进行包扎绝缘处理；将原XT34线排中线号8515A？93A插孔改到94A，并在XT34线排中新增8515C？93A，8515B？94D，如图6所示。\n\n图6 司机室电气柜内走线示意图\n4、检查各线路接线情况，对后端门进行开关试验，验证功能后关闭柜门、空气开关面板及司机室灯顶板。\n5、功能验证\n（1）打开后端门，上下两块电磁铁处于失电状态，状态灯不亮，HMI屏后端门显示黄色，司机室灯亮，CCTV屏显示后端门打开；\n（2）关闭后端门，电磁铁得电，状态灯为红色（此时没有吸合），同时司机室灯灭，HMI屏显示后端门为绿色，CCTV监控屏正常显示，4s后电磁铁状态灯变为绿色（此时已吸合）。\n6、后端门改造原理图，如图7、图8所示。\n    \n图7                                         图8\n五、班组确认内容\n1、确认限位开关六条线路的接线是否正确，牢固；\n2、确认多余的线路是否包扎绝缘处理；\n3、确认后端门是否在门关到位后电磁铁才得电吸合，且有4s延迟；\n4、确认后端门关闭后实际锁闭状态和HMI屏显示信息一致；\n5、作业完成后，班组人员填写作业确认表（附表1）\n六、安全注意事项\n1.遵守公司、中心、车间的其他安全和工艺要求；\n2.现场工器具摆放整齐规范；\n3.劳保用品穿戴整齐；\n4.普查过程中列车不得断电。\n附件1：10号线司机室后端门整改确认表\n\n\n检修三车间技术组\n2018年4月13日",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 633, "dataType": "1", "checkTechInfoNo": "检三技[2018]第031号",
                                      "ctiName": "关于对7、10号线电客车司控器及雨刮器进行整改的通知",
                                      "detailed": "7、10号电客车在运用中多次报出“AI（冗余AI）检测牵引制动力大小故障”，故障司控器返厂后，厂家检测发现司控器电位器存在不同程度的损坏。根据现场调查，司控器电源存在较强的电磁干扰，通过随机启停司机室设备的方式进行试验，试验发现在转动雨刷开关时，司控器电源干扰尤为强烈。鉴于此，决定对司控器和雨刮器进行改造，降低司控器电源干扰，获得较稳定的电源输入和信号输出。",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G,N,R,BJ,CNBJ",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 635, "dataType": "1", "checkTechInfoNo": "检三技[2018]第032号",
                                      "ctiName": "关于7号线电客车CCTV及电子地图程序升级和10号线广播控制盒的整改通知",
                                      "detailed": "调度组、各班组：\n针对近期7号线电客车PIDS系统出现电子地图偶发出现不停重启问题、CCTV监控校时不准问题，以及10号线电客车广播控制盒黑屏问题，需对相关程序进行升级和对相关硬件进行整改",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,G",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 636, "dataType": "1", "checkTechInfoNo": "检三技[2018]第033号",
                                      "ctiName": "关于7、10号线刮雨器水箱增加刻度线的通知",
                                      "detailed": "车辆二中心技术通知单\n检三技 [2018] 第033号\n\t关于7、10号线刮雨器增加刻度线的通知\n\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\n\n\n\n\n\n\n主\n\n\n要\n\n\n内\n\n\n容\n\t调度组、各班组：\n为统一7、10号线刮雨器水箱水位检查标准，现对7、10号线电客车刮雨器水箱观察软管增画刻度线，请各班组按以下要求执行。\n一、作业范围\n7号线：10701-10744列\n10号线：11001-11006列\n二、作业人员及职责\n由检修班组进行整改及确认。\n三、作业条件及工具\n车辆在静止状态下作业整改及确认。\n卷尺、油漆笔。\n四、作业时间\n每列车用时约15分钟，请调度结合生产合理安排整改，于5月30日前完成。\n五、作业内容与要求\n刻度线分最低刻度、中间刻度、最高刻度。用卷尺标定软管长度，在底部向上30mm、75mm处和顶部向下5mm处软管的正面使用油漆笔标记刻度线。\n \n要求使用油漆笔的细笔芯（油漆笔笔芯可拆装，一端为粗一端为细），刻度线标记应清晰、水平，覆盖软管正面半圈。\n\n\n六、验证内容\n无。\n七、班组确认内容\n1、刻度线清晰、整齐，软管其他部位无油漆笔迹残留；\n2、确认柜门锁闭良好。\n八、其他\n1、作业完毕后，请填写记录表。\n九、安全注意事项\n1、遵守公司、中心、车间的其他安全和工艺要求；\n2、现场工器具摆放整齐规范；\n3、劳保用品穿戴整齐；\n4、严禁带电进行接线操作；\n5、注意确保车辆可靠停稳、防止溜车；\n6、打开顶板时注意防止顶板砸人。\n\n\n\n\n\n\n\n\n\n\n\n检修三车间技术组\n2018年4月26日\n编 制\t\t审 核\t\t批 准\t\n签收\t\n7号线班组：（手签版崔家店调度室留存）\n\n日检一班：      日检二班：      日检三班：      日检四班：\n\n\n月修一班：      月修二班：      定修一班：      定修二班：\n\n调度组：\n\n10号线班组：（手签版金花调度室留存）          \n\n金花检修班：         调 度 组：\n\n首做列车\t\t首做确认工程师\t\n完工确认工程师\t\n\n",
                                      "ctiVehicleNo": "11005", "combineRepairTime": "A,B,C,D,D,D,D,D,F,N,R",
                                      "tempRepairTime": "1", "departCode": "12921"},
                                     {"checkTechInfoId": 185593, "dataType": "1", "checkTechInfoNo": "2020-030",
                                      "ctiName": "测试新增", "detailed": "测试新增", "ctiVehicleNo": "11039,11040,11041",
                                      "combineRepairTime": "G,J", "tempRepairTime": "1", "departCode": "12837"}]}
        for department in rec.get('overhaulSkillList'):
            check_tech_info_id = department.get('checkTechInfoId')
            # 数据类型
            data_type = department.get('dataType')
            # 检技通号
            check_tech_info_no = department.get('checkTechInfoNo')
            # 检技通名称
            cti_name = department.get('ctiName')
            # 检技通内容
            detailed = department.get('detailed')
            # 针对车辆
            cti_vehicle_no = department.get('ctiVehicleNo')
            dev = []
            for vehicle in cti_vehicle_no.split(','):
                dev_id = request.env['metro_park_maintenance.train_dev'].sudo().search([('dev_name', '=', vehicle)]).id
                dev.append(dev_id)
            # 结合修程
            combine_repair_time = department.get('combineRepairTime')
            repair_list = []
            for repair in combine_repair_time.split(','):
                rec_repair = request.env['metro_park_maintenance.repair_rule'].sudo().search([('no', '=', repair)])
                if rec_repair:
                    repair_list.append(rec_repair.id)
            # 属于临时修程还是检技通 1检技通，2临时修程，默认检技通"
            temp_repair_time = department.get('tempRepairTime')
            # 指定检技通的人所在的二级部门
            depart_code = department.get('departCode')
            if data_type == '1':
                # 查询当前的记录是否已经存在
                search_rec = request.env['metro_park_maintenance.repair_tmp_rule'].sudo().search(
                    [('check_tech_info_id', '=', check_tech_info_id)])
                if search_rec:
                    search_rec.write({
                        'check_tech_info_id': check_tech_info_id,
                        'no': check_tech_info_no,
                        'name': cti_name,
                        'content': detailed,
                        'trains': [(6, 0, dev)],
                        'repair_rules': [(6, 0, repair_list)],
                        'data_source': 'pms',
                        'start_date': str(datetime.datetime.now())[:10],
                        'end_date': str(datetime.datetime.now())[:10],
                    })
                else:
                    # 新增
                    request.env['metro_park_maintenance.repair_tmp_rule'].sudo().create({
                        'check_tech_info_id': check_tech_info_id,
                        'no': check_tech_info_no,
                        'name': cti_name,
                        'content': detailed,
                        'trains': [(6, 0, dev)],
                        'repair_rules': [(6, 0, repair_list)],
                        'data_source': 'pms',
                        'start_date': str(datetime.datetime.now())[:10],
                        'end_date': str(datetime.datetime.now())[:10],
                    })


def _fnt_response(self, result=None, error=None):
    '''
    修改掉odoo json会包一层版本问题
    :param self:
    :param result:
    :param error:
    :return:
    '''
    response = {
        'jsonrpc': '2.0',
        'id': self.jsonrequest.get('id')
    }
    if error is not None:
        response['error'] = error
    if result is not None:
        response['result'] = result
    from collections import Iterable
    if isinstance(result, Iterable) and 'errorId' in result and 'errorInfo' in result:
        response = result
    if self.jsonp:
        # If we use jsonp, that's mean we are called from another host
        # Some browser (IE and Safari) do no allow third party cookies
        # We need then to manage http sessions manually.
        response['session_id'] = self.session.sid
        mime = 'application/javascript'
        body = "%s(%s);" % (self.jsonp, json.dumps(response, default=ustr))
    else:
        mime = 'application/json'
        body = json.dumps(response, default=ustr)

    return http.Response(
        body, status=error and error.pop('http_status', 200) or 200,
        headers=[('Content-Type', mime), ('Content-Length', len(body))]
    )


JsonRequest._json_response = _fnt_response
