# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError


class MaintainceOrder(models.Model):
    '''
    作业工单
    '''
    _name = 'metro_park_maintenance.maintaince_order'
    _track_log = True

    day_plan_info = fields.Many2one(string='日计划',
                                    comodel_name='metro_park_maintenance.rule_info', ondelete="restrict")

    rule_name = fields.Char(string="修程", related="day_plan_info.rule_name")
    order_no = fields.Char(string="工单编号", compute="_compute_order_no", store=True)

    plan_name = fields.Char(string="计划名称", compute="_compute_plan_name")
    plan_no = fields.Char(string="计划编号", compute="_compute_plan_no")

    plan_date = fields.Date(string="日期", related="day_plan_info.date")
    line = fields.Many2one(string="线路", related="day_plan_info.dev.line")
    location = fields.Many2one(string="位置", related="day_plan_info.dev.location")
    major = fields.Many2one(string="专业", related="day_plan_info.dev.major")
    dev_type = fields.Many2one(string="类型", related="day_plan_info.dev.dev_type")
    plan_start_time = fields.Integer(string="计划开始时间",
                                     related="day_plan_info.work_start_time")
    plan_end_time = fields.Integer(string="计划结束时间",
                                   related="day_plan_info.work_end_time")

    real_date = fields.Date(string='实际开工日期')
    real_start_time = fields.Integer(string='实际开始时间')
    real_end_time = fields.Integer(string='实际结束时间')

    work_department = fields.Many2one(string="作业单位", comodel_name="funenc.wechat.department")
    wx_id = fields.Integer(string="作业单位编码", related="work_department.wx_id", store=True)

    dispatch_user = fields.Many2one(string="派工人员", comodel_name="funenc.wechat.user")
    work_user = fields.Many2one(string="作业人员", comodel_name="funenc.wechat.user")
    report_user = fields.Many2one(string="报告人员", comodel_name="funenc.wechat.user")
    confirm_user = fields.Many2one(string="确认人", comodel_name="funenc.wechat.user")
    previous_user = fields.Char(string="退回给谁", help="这里记载了工单经手的人员列表")

    repair_des = fields.Char(string="检修情况")
    repair_detail = fields.Text(string="检修情况说明")

    state = fields.Selection(selection=[('un_assign', '未指派'),
                                        ('assigned', '已指派'),
                                        ('accept', '已接报'),
                                        ('started', '已开工'),
                                        ('finished', '已完工'),
                                        ('finish_accept', '已确认'),
                                        ('obsolete', '已作废')],
                             default="un_assign",
                             string="工单状态")

    remark = fields.Text(string="备注")
    operation_btns = fields.Char(string="操作")
    order_log = fields.One2many(string="操作记录",
                                comodel_name="metro_park_maintenance.maintaince_order_log",
                                inverse_name="maintaince_order")
    # 判断是PMS 传递过来的还是系统创建的
    pms_order_no = fields.Char(string="pms工单号")
    pms_plan_name = fields.Char(string="pms工单名称")
    pms_plan_no = fields.Char(string="pms计划编号")

    @api.depends("plan_date", "rule_name")
    def _compute_order_no(self):
        '''
        计算工单编号
        :return:
        '''
        for record in self:
            if record.pms_order_no:
                record.order_no = record.pms_order_no
            elif not record.order_no:
                new_no = self.env['ir.sequence'] \
                    .with_context(ir_sequence_date=record.plan_date) \
                    .next_by_code('maintaince.order.number')
                record.order_no = 'JX{rule_name}{no}' \
                    .format(rule_name=record.rule_name, no=new_no)

    def _compute_plan_no(self):
        """
        计算计划编号
        :return:
        """
        for record in self:
            if record.pms_order_no:
                record.plan_no = record.pms_plan_no
            elif record.plan_date:
                year, mon, day = str(record.plan_date).split("-")
                record.plan_no = year + mon + day

    @api.depends('plan_start_time', 'plan_end_time')
    def _compute_plan_name(self):
        '''
        计算计划名称
        :return:
        '''
        for record in self:
            if record.pms_plan_name:
                record.plan_name = record.pms_plan_name
            elif record.plan_start_time and record.plan_end_time:
                start_time = str(record.plan_start_time).split(" ")[-1]
                end_time = str(record.plan_end_time).split(" ")[-1]
                record.plan_name = record.day_plan_info.dev_no + " " + start_time + "-" + end_time + (
                    record.rule_name if record.rule_name else "")
            else:
                start_time = "09:00"
                end_time = "17:00"
                record.plan_name = record.day_plan_info.dev_no + " " + start_time + "-" + end_time + (
                    record.rule_name if record.rule_name else "")

    @api.multi
    def assign(self):
        """
        指派按钮
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.send_job_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.maintaince_order_wizard",
            'context': {
                'form_view_initial_mode': 'edit',
                'propertie_ids':
                    [self.env.ref('metro_park_base.department_property_balance_work_class').id]
            },
            'target': 'new'
        }

    @api.multi
    def reasigned(self):
        """
        转报
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.reasigned_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'res_id': self.id,
            'context': {
                'form_view_initial_mode': 'edit',
                'propertie_ids':
                    [self.env.ref('metro_park_base.department_property_balance_work_class').id]
            },
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.maintaince_order",
            'target': 'new',
        }

    @api.multi
    def un_assign_on_click(self):
        """
        转报确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"] \
            .search([("user_id", "=", context['uid'])])
        if not dispatch_user:
            raise
        previous_user = eval(self.previous_user)
        previous_user.append(self.work_user.id)
        self.previous_user = previous_user
        self.env["metro_park_maintenance.maintaince_order_log"].create({
            'maintaince_order': self.id,
            'action': "转报",
            'operator': dispatch_user.id,
            'assigned_user': self.work_user.id
        })

    @api.multi
    def rebacked(self):
        """
        退回按钮
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.rebacked_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_id': self.id,
            'context': {
                'form_view_initial_mode': 'edit'
            },
            'res_model': "metro_park_maintenance.maintaince_order",
            'target': 'new',
        }

    @api.multi
    def rebacked_on_click(self):
        """
        退回确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"] \
            .search([("user_id", "=", context['uid'])])
        previous_user = eval(self.previous_user)
        previous_user.pop()
        if previous_user:
            self.work_user = self.env['funenc.wechat.user'] \
                .search([('id', '=', previous_user[-1])])
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': self.id,
                'action': "退回",
                'operator': dispatch_user.id,
                'assigned_user': self.work_user.id
            })
        else:
            self.work_user = None
            self.state = "un_assign"
            self.work_department = None
            self.dispatch_user = None
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': self.id,
                'action': "退回",
                'operator': dispatch_user.id,
                'assigned_user': None
            })
        self.previous_user = previous_user

    @api.multi
    def auto_compute(self):
        """
        接报按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        self.state = "accept"
        self.env["metro_park_maintenance.maintaince_order_log"].create({
            'maintaince_order': self.id,
            'action': "接报",
            'operator': dispatch_user.id,
            'assigned_user': None
        })

    @api.multi
    def start_work(self):
        """
        开工按钮
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.start_job_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.maintaince_order_wizard",
            'target': 'new',
            'context': {'ids': [self.id]}
        }

    @api.multi
    def finish_work(self):
        """
        完工按钮
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.finish_job_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.maintaince_order_wizard",
            'target': 'new',
            'context': {'ids': [self.id]}
        }

    @api.multi
    def finish_work_confirm(self):
        """
        完工确认按钮
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.finish_job_confirm_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.maintaince_order_wizard",
            'target': 'new',
            'context': {'ids': [self.id]}
        }

    @api.model
    def send_job(self, ids):
        """
        批量派工
        :param ids:
        :return:
        """
        if ids:
            orders = self.env["metro_park_maintenance.maintaince_order"].search([('id', 'in', ids)])
            for order in orders:
                if order.state != 'un_assign':
                    raise ValidationError("所选工单存在不是<未指派>状态的工单")
            form_id = self.env.ref("metro_park_maintenance.send_job_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")

    @api.model
    def start_job(self, ids):
        """
        批量开工
        :param ids:
        :return:
        """
        if ids:
            orders = self.env["metro_park_maintenance.maintaince_order"].search([('id', 'in', ids)])
            for order in orders:
                if order.state != 'accept':
                    raise ValidationError("所选工单存在不是<已接报>状态的工单")
            form_id = self.env.ref("metro_park_maintenance.start_job_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")

    @api.model
    def finish_job(self, ids):
        """
        批量完工
        :param ids:
        :return:
        """
        if ids:
            orders = self.env["metro_park_maintenance.maintaince_order"].search([('id', 'in', ids)])
            for order in orders:
                if order.state != 'started':
                    raise ValidationError("所选工单存在不是<已开工>状态的工单")
            form_id = self.env.ref("metro_park_maintenance.finish_job_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")

    @api.model
    def finish_job_confirm(self, ids):
        """
        批量完工确认
        :param ids:
        :return:
        """
        if ids:
            orders = self.env["metro_park_maintenance.maintaince_order"].search([('id', 'in', ids)])
            for order in orders:
                if order.state != 'finished':
                    raise ValidationError("所选工单存在不是<已完工>状态的工单")
            form_id = self.env.ref("metro_park_maintenance.finish_job_confirm_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")

    @api.model
    def force_close(self, ids):
        """
        批量强制关闭
        :param ids:
        :return:
        """
        if ids:
            form_id = self.env.ref("metro_park_maintenance.force_close_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")

    @api.model
    def order_obsolete(self, ids):
        """
        批量工单作废
        :param ids:
        :return:
        """
        if ids:
            form_id = self.env.ref("metro_park_maintenance.order_obsolete_wizard_form").id
            return {
                'type': 'ir.actions.act_window',
                'views': [[form_id, 'form']],
                'view_mode': 'form',
                'res_model': "metro_park_maintenance.maintaince_order_wizard",
                'target': 'new',
                'context': {'ids': ids}
            }
        else:
            raise ValidationError("未选择工单！")
