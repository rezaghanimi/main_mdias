# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import fields, models, api
import time
import requests
import json
import datetime
import logging
import pendulum
from odoo.tools import config
from odoo import registry
from odoo.models import SUPERUSER_ID

_logger = logging.getLogger(__name__)


class PmsInterface(models.Model):
    _name = 'mdias_pms_interface'
    _description = 'mdias和pms的接口'

    ip = fields.Char(string='接口对接IP')

    @api.multi
    def transceiver_vehicle_information(self, *args):
        '''
        列车收发车信息
        :param args:
        :return:
        '''
        time.sleep(8)
        rec = args[0]
        train_out_plan = ''
        train_back_plan = ''
        out_time = ''
        back_time = ''
        db_name = config.options['db_name']
        db_registry = registry(db_name)
        with api.Environment.manage(), db_registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            pms_ip = env['metro_park_base.system_config'].search([])[0].pms_ip
            if args[1] == 'train_out_plan':
                create_rec = env['metro_park_dispatch.train_out_plan'].search([('id', '=', rec.id)])
                train_out_plan = create_rec.train_id.train.location.name
                out_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(create_rec.exchange_rail_time))[11:] \
                    if create_rec.exchange_rail_time else ''
                inout_mark = 2
            else:
                create_rec = env['metro_park_dispatch.train_back_plan'].search([('id', '=', rec.id)])
                train_back_plan = create_rec.train_id.train.location.name
                back_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(create_rec.exchange_rail_time))[11:] \
                    if create_rec.exchange_rail_time else ''
                inout_mark = 1
            info = {
                "sourceSystemId": "MDIAS-{}-HTTP".format(self.get_line_info()),
                "eqiupCode": create_rec.train_id.train.object_code if create_rec.train_id.train.object_code else '',
                "lineNo": self.get_line_info(),
                "dataType": 1,
                "vehicleNo": create_rec.train_id.train_name,
                "outBarnDepot": train_out_plan,
                "backBarnDepot": train_back_plan,
                "outTime": out_time,
                "backTime": back_time,
                'inoutMark': inout_mark
            }
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(
            'http://{}/scgl/mdiasServlet?method=overhaulSendReceive'.format(pms_ip),
            data=json.dumps(info), headers=headers, timeout=4)
        _logger.info(req.text)

    @api.multi
    def repairing_information(self, *args):
        '''
        修程信息
        :param kwargs:
        :return:
        '''
        headers = {
            'Content-Type': 'application/json',
        }
        for data in args:
            req = requests.post(
                'http://{}/scgl/mdiasServlet?method=repairingInfo'.format(
                    self.env['metro_park_base.system_config'].search([])[0].pms_ip),
                data=json.dumps(data), headers=headers, timeout=4)
            _logger.info(req.text)

    @api.multi
    def year_month_week_day_plan(self, self_plan_data, date, datatype):
        '''
        :param self_plan_data:
        :param date:
        :param datatype:
        :return:
        '''
        models_name = self_plan_data._name
        if models_name == 'metro_park_maintenance.year_plan':
            self.year_month_pms_data_finishing(self_plan_data, date, datatype)
        elif models_name == 'metro_park_maintenance.month_plan':
            self.year_month_pms_data_finishing(self_plan_data, date, datatype)
        elif models_name == 'metro_park_maintenance.week_plan':
            self.week_day_pms_data_finishing(self_plan_data, date, datatype)
        elif models_name == 'metro_park_maintenance.day_plan':
            return_info = self.week_day_pms_data_finishing(self_plan_data, date, datatype)
            if return_info == 'err':
                return 'err'

    @api.multi
    def year_month_pms_data_finishing(self, plan_data, date, datatype):
        train_info = self.env['metro_park_maintenance.train_dev'].sudo().search([('object_code', '!=', '')])
        if date == 'Y':
            if datatype == '1':
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'year'),
                        ('send_state', '=', 'not_send'),
                        ('year', '=', plan_data.year),
                        ('dev', 'in', train_info.ids),
                    ])
            else:
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'year'),
                        ('send_state', '=', 'send'),
                        ('year', '=', plan_data.year),
                        ('dev', 'in', train_info.ids),
                    ])
            month = ''
            if not plan_data:
                return
        elif date == 'M':
            if datatype == '1':
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'month'),
                        ('send_state', '=', 'not_send'),
                        ('year', '=', plan_data.year),
                        ('month', '=', plan_data.month),
                        ('dev', 'in', train_info.ids),
                    ])
            else:
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'month'),
                        ('send_state', '=', 'send'),
                        ('year', '=', plan_data.year),
                        ('month', '=', plan_data.month),
                        ('dev', 'in', train_info.ids),
                    ])
            month = str(plan_data.month).zfill(2)
            if not plan_recs:
                return
        plan_list = []
        for plan_rec in plan_recs:
            if date == 'Y':
                plan_source_id = ''
            else:
                if plan_rec.parent_id:
                    plan_source_id = '{}-MDIAS-{}'.format(self.get_line_info(),plan_rec.parent_id)
                else:
                    plan_source_id = ''
            plan_list.append({
                "recCreator": plan_rec.create_uid.name,
                "recCreateTime": str(plan_rec.create_date)[:19].replace('-', '').replace(':', '').replace(' ',
                                                                                                          ''),
                "recRevisor": '',
                "recReviseTime": "",
                "recDeletor": "",
                "recDeleteTime": "",
                "overhaulDetailId": "{}-MDIAS-{}".format(self.get_line_info(), plan_rec.id),
                "dataType": datatype,
                "planPeriodType": date,
                "eqiupCode": plan_rec.dev.object_code if plan_rec.dev.object_code else '',
                "vehicleNo": plan_rec.dev.dev_no,
                "vehicleModel": plan_rec.dev.standard.name if plan_rec.dev.standard else '',
                "repairingTimeName": plan_rec.work_content,
                "repairingTime": plan_rec.rule_no,
                "reapirCount": '',
                "workContent": plan_rec.work_content,
                "planStartDate": str(plan_rec.date),
                "planRepairDays": plan_rec.repair_days,
                "planSourceDetailId": plan_source_id,
            })

        rec = ({
            'sourceSystemId': "MDIAS-{}-HTTP".format(self.get_line_info()),
            'lineNo': self.get_line_info(),
            'dataType': datatype,
            'planPeriodType': date,
            'overhaulPlanYear': plan_data.year,
            'overhaulPlanMonth': month,
            'overhaulDeptNo': plan_data.pms_work_class_info.department_no,  # 用年计划的工班
            'overhaulDeptName': plan_data.pms_work_class_info.department,  # 用年计划的工班名称
            'planlist': plan_list
        })
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(
            'http://{}/scgl/mdiasServlet?method=yearAndMonthPlan'.format(
                self.env['metro_park_base.system_config'].search([])[0].pms_ip),
            data=json.dumps(rec), headers=headers, timeout=5)
        _logger.info(str(req.text))
        if eval(str(req.text))['errorId'] == '10':
            if plan_recs and datatype == '1':
                for plan_rec in plan_recs:
                    plan_rec.send_state = 'send'
            elif plan_recs and datatype == '3':
                for plan_rec in plan_recs:
                    plan_rec.send_state = 'not_send'

    @api.multi
    def week_day_pms_data_finishing(self, plan_data, date, datatype):
        train_info = self.env['metro_park_maintenance.train_dev'].sudo().search([('object_code', '!=', '')])
        return_info = ''
        if date == 'W':
            if datatype == '1':
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'week'),
                        ('send_state', '=', 'not_send'),
                        ('dev', 'in', train_info.ids),
                        ('date', '>=', plan_data.start_date),
                        ('date', '<=', plan_data.end_date),
                    ]
                )
            else:
                plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                    [
                        ('data_source', '=', 'week'),
                        ('send_state', '=', 'send'),
                        ('dev', 'in', train_info.ids),
                        ('date', '>=', plan_data.start_date),
                        ('date', '<=', plan_data.end_date),
                    ]
                )
            month = str(plan_data.end_month).zfill(2)
            week_count = int(datetime.datetime.strptime(str(plan_data.end_date), '%Y-%m-%d').strftime('%W')) + 1
            day_count = int(datetime.datetime.strptime(str(plan_data.end_date), '%Y-%m-%d').strftime('%d')) + 1
            plan_start_date = str(plan_data.start_date)
            plan_end_date = str(plan_data.end_date)
            over_plan_year = plan_data.end_year
        elif date == 'D':
            plan_recs = self.env['metro_park_maintenance.rule_info'].search(
                [
                    ('data_source', '=', 'day'),
                    ('dev', 'in', train_info.ids),
                    ('date', '=', plan_data.plan_name),
                ])
            week_count = datetime.datetime.strptime((str(plan_data.year)
                                                     + str(plan_data.month)
                                                     + str(plan_data.day)), '%Y%m%d').strftime('%W')
            day_count = datetime.datetime.strptime((str(plan_data.year)
                                                    + str(plan_data.month)
                                                    + str(plan_data.day)), '%Y%m%d').strftime('%d')
            over_plan_year = plan_data.year
            month = str(plan_data.month).zfill(2)
            plan_start_date = str(plan_data.plan_date)
            plan_end_date = str(plan_data.plan_date)
        plan_list = []
        for plan_rec in plan_recs:
            if plan_rec.dispatch_users_info:
                work_status = '2'
                dispatch_person_id = plan_rec.dispatch_users_info.name
                dispatch_person_name = plan_rec.dispatch_users_info.wx_userid
            else:
                work_status = '1'
                dispatch_person_id = ''
                dispatch_person_name = ''
            if plan_rec.parent_id:
                plan_source_id = '{}-MDIAS-{}'.format(self.get_line_info(), plan_rec.parent_id)
            else:
                plan_source_id = ''
            if not plan_rec.pms_work_class.department_no:
                return_info = 'err'
            plan_list.append(
                {
                    "recCreator": plan_rec.create_uid.name,
                    "recCreateTime": str(plan_rec.create_date)[:19].replace('-', '').replace(':', '').replace(
                        ' ',
                        ''),
                    "recRevisor": plan_rec.create_uid.name,
                    "recReviseTime": "",
                    "recDeletor": "",
                    "recDeleteTime": "",
                    "overhaulDetailId": "{}-MDIAS-{}".format(self.get_line_info(), plan_rec.id),
                    "dataType": datatype,
                    "planPeriodType": date,
                    "eqiupCode": plan_rec.dev.object_code if plan_rec.dev.object_code else '',
                    "vehicleNo": plan_rec.dev.dev_no,
                    "vehicleModel": plan_rec.dev.standard.name if plan_rec.dev.standard else '',
                    "repairingTimeName": plan_rec.work_content,
                    "repairingTime": plan_rec.rule_no,
                    "reapirCount": '',
                    "workContent": plan_rec.work_content if plan_rec.work_content else '',
                    "workNote": plan_rec.remark if plan_rec.remark else '',
                    "outBarnDepot": "",
                    "workBarnDepot": "",
                    "backBarnDepot": "",
                    "workArea": "",
                    "inDepot_need": "",
                    "workTeamNo": plan_rec.pms_work_class.department_no if plan_rec.pms_work_class else '',
                    "workTeamName": plan_rec.pms_work_class.department if plan_rec.pms_work_class else '',
                    "planStartDate": str(plan_rec.date),
                    "planEndDate": str(plan_rec.date),
                    "planRepairDays": plan_rec.repair_days,
                    "planSourceDetailId": plan_source_id,
                    "workBeginTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(plan_rec.work_start_time))[
                                     11:] if plan_rec.work_start_time else '09：00',
                    "workEndTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(plan_rec.work_end_time))[
                                   11:] if plan_rec.work_end_time else '18:00',
                    "repairDays": plan_rec.repair_days,
                    "workStatus": work_status,
                    "dispatchPersonId": dispatch_person_id,
                    "dispatchPersonName": dispatch_person_name,
                }
            )
        rec = {
            "sourceSystemId": "MDIAS-{}-HTTP".format(self.get_line_info()),
            "lineNo": self.get_line_info(),
            "dataType": datatype,
            'planPeriodBeginDate': plan_start_date,
            'planPeriodEndDate': plan_end_date,
            "planPeriodType": date,
            "overhaulPlanYear": over_plan_year,
            "overhaulPlanMonth": month,
            "overhaulPlanWeek": str(week_count).zfill(3),
            "overhaulPlanDay": str(day_count).zfill(2),
            "overhaulDeptNo": plan_data.pms_work_class_info.department_no,
            "overhaulDeptName": plan_data.pms_work_class_info.department,
            "planlist": plan_list,
        }
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(
            'http://{}/scgl/mdiasServlet?method=weekAndDayPlan'.format(
                self.env['metro_park_base.system_config'].search([])[0].pms_ip),
            data=json.dumps(rec), headers=headers, timeout=4)
        if return_info == 'err':
            return 'err'
        _logger.info(req.text)
        if eval(req.text)['errorId'] == '10':
            if plan_recs and datatype == '1':
                for plan_rec in plan_recs:
                    plan_rec.send_state = 'send'
            elif plan_recs and datatype == '3':
                for plan_rec in plan_recs:
                    plan_rec.send_state = 'not_send'

    @api.multi
    def capture_organizational_structure(self, *args):
        '''
        获取组织结构的信息
        :param kwargs:
        :return:
        '''
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(
            'http://{}/scgl/mdiasServlet?method=getWorkTeamInfo'.format(
                self.env['metro_park_base.system_config'].search([])[0].pms_ip),
            data=json.dumps({'lineNo': self.get_line_info()}), headers=headers, timeout=10)
        if req.text:
            for department in eval(req.text.replace('null', '""')).get('workTeamList'):
                exist_rec = self.env['pms.department'].search([('department_no', '=', department.get('sectionCode'))])
                if not exist_rec:
                    self.env['pms.department'].create({
                        'department': department.get('sectionName'),
                        'department_no': department.get('sectionCode'),
                        'line_no': department.get('lineNo'),
                        'parent_department': department.get('fullName'),
                        'parent_department_no': department.get('parentName'),
                    })

    @api.multi
    def get_repair_tmp_rule(self, *args):
        '''
        获取检技通
        :param kwargs:
        :return:
        '''
        headers = {
            'Content-Type': 'application/json',
        }
        req = requests.post(
            'http://{}/scgl/mdiasServlet?method=getOverhaulSkill'.format(
                self.env['metro_park_base.system_config'].search([])[0].pms_ip),
            data=json.dumps({'lineNo': self.get_line_info()}), headers=headers, timeout=10)
        _logger.info(req.text)
        if req.text:
            for department in eval(req.text).get('overhaulSkillList'):
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
                # 开始时间
                cti_begin_date = department.get('ctiBeginDate')
                # 结束时间
                cti_end_date = department.get('ctiEndDate')
                dev = []
                for vehicle in cti_vehicle_no.split(','):
                    dev_id = self.env['metro_park_maintenance.train_dev'].sudo().search([('dev_name', '=', vehicle)]).id
                    dev.append(dev_id)
                # 结合修程
                combine_repair_time = department.get('combineRepairTime')
                repair_list = []
                for repair in combine_repair_time.split(','):
                    rec_repair = self.env['metro_park_maintenance.repair_rule'].sudo().search([('no', '=', repair)])
                    if rec_repair:
                        repair_list.append(rec_repair.id)
                # 属于临时修程还是检技通 1检技通，2临时修程，默认检技通"
                temp_repair_time = department.get('tempRepairTime')
                # 指定检技通的人所在的二级部门
                depart_code = department.get('departCode')
                if data_type == '1':
                    # 查询当前的记录是否已经存在
                    search_rec = self.env['metro_park_maintenance.repair_tmp_rule'].sudo().search(
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
                            'start_date': cti_begin_date if cti_begin_date else None,
                            'end_date': cti_end_date if cti_end_date else None,
                        })
                    else:
                        # 新增
                        self.env['metro_park_maintenance.repair_tmp_rule'].sudo().create({
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

    @api.multi
    def year_plan_data_send(self):
        '''
        PMS年计划发送数据
        :return:
        '''
        year_plan = self.env['metro_park_maintenance.year_plan'].search([
            ('year', '=', pendulum.today().year),
            ('state', '=', 'published'),
            ('pms_work_class_info', '!=', None),
        ])
        if year_plan:
            self.year_month_week_day_plan(year_plan, 'Y', '1')

    @api.multi
    def month_plan_data_send(self):
        year_plan = self.env['metro_park_maintenance.month_plan'].search([
            ('year', '=', pendulum.today().year),
            ('month', '=', pendulum.today().month),
            ('state', '=', 'published'),
            ('pms_work_class_info', '!=', None),
        ])
        if year_plan:
            self.year_month_week_day_plan(year_plan, 'M', '1')

    @api.multi
    def week_plan_data_send(self):
        year_plan = self.env['metro_park_maintenance.week_plan'].search([
            ('year', '=', pendulum.today().year),
            ('start_date', '<=', str(pendulum.today().today())[:10]),
            ('end_date', '>=', str(pendulum.today().today())[:10]),
            ('state', '=', 'published'),
            ('pms_work_class_info', '!=', None),
        ])
        if year_plan:
            self.year_month_week_day_plan(year_plan, 'W', '1')

    @api.multi
    def pms_organizational_structure_acquisition(self):
        try:
            self.env['mdias_pms_interface'].sudo().capture_organizational_structure()
        except Exception as e:
            _logger.info('PMS获取工班信息失败' + str(e))

    @api.multi
    def get_line_info(self):
        line_id = ''
        user = self.env['res.users'].search([('id', '=', 2)])
        if user.cur_location:
            line_id = user.cur_location.line.name
        # 每次进来都需要打开文件对比一次看看时候修改过
        if line_id == '8号线':
            return '08'
        elif line_id == '6号线':
            return '06'
        elif line_id == '10号线':
            return '10'
