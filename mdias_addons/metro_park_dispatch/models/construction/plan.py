# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime

import pendulum

from odoo import models, fields, api

# 施工调度数据对应关系
DATA_KEY_RELATION = {
    'planId': 'plan_id',
    'planIdSource': 'source_plan_id',
    'lineId': 'out_line_id',
    'lineName': 'out_line_name',
    'depotId': 'out_deport_id',
    'depotName': 'out_deport_name',
    'planTypeCode': 'out_plan_type',
    'formStatusCode': 'out_state',
    'planBeginTime': 'out_work_tart_utime',
    'planEndTime': 'out_work_end_utime',
    'workTimeDesc': 'out_work_date_desc',
    'workCode': 'out_work_code',
    'workContent': 'out_work_content',
    'workAreaDesc': 'out_work_area_desc',
    'affectScope': 'out_affect_scope',
    'powerAreaDesc': 'out_power_desc',
    'guardMeasure': 'out_guard_measure',
    'workOrgName': 'out_work_department',
    'applyUserName': 'out_apply_user_name',
    'personInChargeName': 'out_person_in_charge_name',
    'contactPhone': 'out_connect_phone',
    'changeCancelReason': 'out_change_reason',
    'recordNote': 'out_remark',
    'checkInApproveTimeUnix': 'out_checkin_approve_time',
    'checkOutApproveTimeUnix': 'out_checkout_approve_time'
}


class ConstructionPlan(models.Model):
    """
        施工调度计划
    """

    _name = 'metro_park_dispatch.construction_plan'

    # 施工计划同步多少日期之后
    _syn_after_date = '2019-10-30'
    _order = 'out_work_tart_utime DESC'

    plan_id = fields.Integer(string='计划ID')
    source_plan_id = fields.Integer()
    out_deport_id = fields.Integer()
    out_deport_name = fields.Char()
    out_line_id = fields.Integer(string='施工调度线路ID')
    out_line_name = fields.Char(string='施工调度线路Name')
    out_depot_id = fields.Integer(string='施工调度场段ID')
    out_depot_name = fields.Char(string='施工调度场段NAME')
    out_plan_type = fields.Selection([('Monthly', '月计划'),
                                      ('Weekly', '周计划'),
                                      ('Supplementary', '日补充计划'),
                                      ('Temporary', '临时补充计划')],
                                     string='计划类型')
    out_state = fields.Selection([('Approved', '已批准'),
                                  ('Cancelled', '已取消'),
                                  ('Changed', '已变更'),
                                  ('EntryPassed', '已请点'),
                                  ('Finished', '已完成'),
                                  ('OrderIssued', '已签发')
                                  ], string='计划状态')
    out_work_tart_utime = fields.Integer()
    out_work_end_utime = fields.Integer()
    out_work_start_time = fields.Datetime(string='作业开始时间',
                                          compute='compute_out_work_start_time', store=True)
    out_work_end_time = fields.Datetime(string='作业结束时间',
                                        compute='compute_out_work_end_time', store=True)
    out_work_date_desc = fields.Char()
    out_work_code = fields.Char(string='作业代码')
    out_work_content = fields.Text(string='作业内容')
    out_work_area_desc = fields.Text(string='作业区域描述')
    out_affect_scope = fields.Text(strin='影响区域')
    out_power_desc = fields.Text(string='供电区域描述')
    out_guard_measure = fields.Text(string='防护措施')
    out_work_department = fields.Char(string='施工部门')
    out_apply_user_name = fields.Char(string='施工申报人')
    out_person_in_charge_name = fields.Char(string='施工负责人')
    out_change_reason = fields.Text(string='变更原因')
    out_connect_phone = fields.Char(string='施工负责人联系方式')
    out_remark = fields.Text(string='备注信息')
    out_plan_begin_time = fields.Datetime(string='计划占用开始时间')
    out_plan_end_time = fields.Datetime(string='计划占用结束时间')
    out_construction_require = fields.Selection([(1, '停电'),
                                                 (2, '带电'),
                                                 (3, '停电挂地线'),
                                                 (4, '反复停送电'),
                                                 (5, '无供电要求'),
                                                 (6, '供电受影响'),
                                                 (7, '行车受影响')
                                                 ], string='施工要求')

    work_areas = fields.Many2many('metro_park_dispatch.construction_area_relation',
                                  'construction_work_area_ref',
                                  'plan_id',
                                  'area_id',
                                  string='作业区域')

    affect_areas = fields.Many2many('metro_park_dispatch.construction_area_relation',
                                    'construction_affect_area_ref',
                                    'plan_id',
                                    'area_id',
                                    string='供电区域')

    out_checkin_approve_time = fields.Integer()
    out_checkout_approve_time = fields.Integer()

    md5_string = fields.Char()
    http_value = fields.Text(string='请求数据值')

    @api.one
    @api.depends('out_work_tart_utime')
    def compute_out_work_start_time(self):
        self.out_work_start_time = datetime.fromtimestamp(self.out_work_tart_utime)

    @api.one
    @api.depends('out_work_end_utime')
    def compute_out_work_end_time(self):
        self.out_work_end_time = datetime.fromtimestamp(self.out_work_end_utime)

    @api.model
    def _add_md5_to_values(self, values_list):
        """
            生成md5 key 验证数据是否改动
        :param values_list:
        :return:
        """

        def _md5(val):
            """
                计算更新val的md5,防止数据重复更新
            :param val:
            :return:
            """
            md5 = hashlib.md5()
            md5.update(str(val).encode('utf-8'))
            return md5.hexdigest()

        for val in values_list:
            val['md5_string'] = _md5(val)
        return values_list

    def _write_or_update_plan(self, value_list):
        '''
        写入或更新计划
        :param value_list:
        :return:
        '''
        value_list = self._add_md5_to_values(value_list)
        md5s = set([])
        out_plan_ids = set([])
        for val in value_list:
            pid = val['plan_id']
            if not pid:
                continue
            out_plan_ids.add(pid)
            md5s.add(val['md5_string'])

        # 筛选已经存在的计划并且需要更新的
        update_plan_ids = self.search(
            [('plan_id', 'in', list(out_plan_ids)),
             ('md5_string', 'not in', list(md5s))]).mapped('plan_id')

        not_update_ids = self.search(
            [('plan_id', 'in', list(out_plan_ids)),
             ('md5_string', 'in', list(md5s))]).mapped('plan_id')

        create_plan_ids = out_plan_ids - set(not_update_ids + update_plan_ids)
        create_values = filter(lambda cpid: cpid['plan_id'] in create_plan_ids, value_list)
        update_values = filter(lambda upid: upid['plan_id'] in update_plan_ids, value_list)
        create_values = list(create_values)

        self.create(create_values)

        for val in update_values:
            pid = val.get('plan_id')
            old_plan = self.search([('plan_id', '=', pid)], limit=1)
            if not old_plan: continue
            old_plan.write(val)

    @classmethod
    def _merge_data(cls, plan_data, plan_status_data):
        '''
        融合数据
        :param plan_data:
        :param plan_status_data:
        :return:
        '''
        value_list = []
        values = {}
        for d in plan_data:
            values[d['planId']] = d
        for pdv in plan_status_data:
            val = values.get(pdv['planId'], {})
            val.update(pdv)
        for val in values.values():
            value_list.append(val)
        return value_list

    def _request_plan_data(self, out_line_id, out_location_id, data):
        """
        请求施工调度计划
        :param out_line_id: 施工调度系统线路id
        :param out_location_id:  施工调度系统位置id
        :param data<datetime>: 请求多少日之后的数据
        :return: list
        """
        value_list = []
        api_obj = self.env['metro_park_dispatch.construction.http']
        plan_data = api_obj.construction_plans(
            out_line_id, out_location_id, data)
        plan_status_data = api_obj.construction_work_plan_status(
            out_line_id, out_location_id, data)
        area_obj = self.env['metro_park_dispatch.construction_area_relation']
        values_list = self._merge_data(plan_data, plan_status_data)
        for d in values_list:
            value = {}
            for k in DATA_KEY_RELATION.keys():
                _k = DATA_KEY_RELATION[k]
                if _k in ['out_work_tart_utime',
                          'out_work_end_utime',
                          'out_checkin_approve_time',
                          'out_checkout_approve_time']:
                    if d.get(k, False):
                        value[_k] = d.get(k or 0, 0) / 1000
                else:
                    value[_k] = d.get(k, None)

            value_list.append(value)
            work_areas = d['workareas']
            work_area_ids = set()
            affect_area_ids = set()
            for warea in work_areas:
                if 'usageCode' in warea:
                    if 'Use' in warea['usageCode']:
                        work_area_ids.add(warea['workAreaId'])
                    elif 'Signal' in warea['usageCode']:
                        affect_area_ids.add(warea['workAreaId'])
            work_areas = area_obj.search([('area_id', 'in', list(work_area_ids))]).ids
            affect_area = area_obj.search([('area_id', 'in', list(affect_area_ids))]).ids
            value['work_areas'] = [(6, False, work_areas)]
            value['affect_areas'] = [(6, False, affect_area)]
            value['http_value'] = str(d)
        return value_list

    @api.model
    def corn_synchronization(self, syn_date=None):
        """
        施工计划同步, 同步完成之后将信息同步到占线板
        :return:
        """
        if not syn_date:
            if not self.search([], limit=1):
                syn_date = datetime.strptime('2019-10-29', "%Y-%m-%d")
            else:
                syn_date = datetime.utcnow().date()

        syn_date = pendulum.parse(str(syn_date)).subtract(hours=8)
        relation_locations = \
            self.env['metro_park_dispatch.construction_location_relation'].search([])
        data_list = []
        for loc in relation_locations:
            data_list += self._request_plan_data(
                loc.out_line_id, loc.out_location_id, syn_date)
        self._write_or_update_plan(data_list)
        # 更新占线板信息
        self.env['metro_park_base.busy_board'].update_construction_icons()

    def action_edit(self):
        '''
        编辑动作
        :return:
        '''
        view_id = self.env.ref('metro_park_dispatch.construction_plan_form').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'target': 'new',
            'res_id': self.id,
            'context': dict(self._context),
            'flags': {'mode': 'readonly'},
        }

    @api.model
    def action_synchronization_wizard(self):
        '''
        同步向导
        :return:
        '''
        view_id = self.env.ref('metro_park_dispatch.form_wizard_plan_syn').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'metro_park_dispatch.wizard.plan_syn',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': dict(self._context, dialog_size='medium'),
        }
