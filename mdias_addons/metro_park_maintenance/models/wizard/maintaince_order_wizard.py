from odoo import models, fields, api
from datetime import datetime
from .. import util


class MaintainceOrderLog(models.TransientModel):
    """
    工单日志记录
    """
    _name = "metro_park_maintenance.maintaince_order_log"

    maintaince_order = fields.Many2one(string="检修工单", comodel_name="metro_park_maintenance.maintaince_order", readonly=1)
    record_time = fields.Datetime(string="操作时间", default=datetime.now(), readonly=1)
    action = fields.Char(string="动作", readonly=1)
    operator = fields.Many2one(string="操作人", comodel_name="funenc.wechat.user", readonly=1)
    assigned_user = fields.Many2one(string="被操作人", comodel_name="funenc.wechat.user", readonly=1)


class MaintainceOrderWizard(models.TransientModel):
    """
    检修工单向导
    """
    _name = "metro_park_maintenance.maintaince_order_wizard"

    work_class = fields.Many2one(string="检修班组", comodel_name="funenc.wechat.department", default=1)
    work_user = fields.Many2one(string="作业人员",
                                comodel_name="funenc.wechat.user",
                                domain="[('department_ids', 'in', work_class)]")
    dispatch_user = fields.Many2one(string="确认人员", comodel_name="funenc.wechat.user", readonly=True,
                                    default=lambda self: self.env['funenc.wechat.user'].search([('user_id', '=', self.env.user.id)]).id)
    statr_time = fields.Datetime(string="开工时间")
    end_time = fields.Datetime(string="完工时间")
    repair_des = fields.Char(string="检修情况")
    repair_detail = fields.Text(string="检修情况说明")
    now_time = fields.Datetime(string="选择时间", default=datetime.now())

    @api.multi
    def send_job_on_click(self):
        """
        派工确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.state = "assigned"
            order.work_user = self.work_user
            order.work_department = self.work_class
            order.dispatch_user = dispatch_user
            order.previous_user = [self.work_user.id]
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "派工",
                'operator': dispatch_user.id,
                'assigned_user': self.work_user.id
            })

    @api.multi
    def start_job_on_click(self):
        """
        开工确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.real_start_time = util.time_str_to_int(str(self.statr_time))
            order.state = "started"
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "开工",
                'operator': dispatch_user.id,
            })

    @api.multi
    def finish_job_on_click(self):
        """
        完工确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.real_end_time = util.time_str_to_int(str(self.end_time))
            order.report_user = dispatch_user
            order.state = "finished"
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "完工",
                'operator': dispatch_user.id,
            })
            if order.rule_name == '里程检':
                year = order.real_end_time.year
                month = order.real_end_time.month
                day = order.real_end_time.day
                train_id = order.day_plan_info.plan_data.dev.id
                history = self.env['metro_park_maintenance.history_miles'].\
                    search([('train_dev', '=', train_id), ('year', '=', year), ('month', '=', month)])
                history.miles_after_last_repair = 0
                history.last_repair_miles = getattr(history, "day%s" % day)

    @api.multi
    def finish_job_confirm_on_click(self):
        """
        完工确认的确认按钮
        :return:
        """
        context = self.env.context
        confirm_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.state = "finish_accept"
            order.confirm_user = confirm_user
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "完工确认",
                'operator': confirm_user.id,
            })

    @api.multi
    def force_close_on_click(self):
        """
        强制关闭的确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.state = "finish_accept"
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "强制关闭",
                'operator': dispatch_user.id,
            })

    @api.multi
    def obsolete_on_click(self):
        """
        工单作废的确认按钮
        :return:
        """
        context = self.env.context
        dispatch_user = self.env["funenc.wechat.user"].search([("user_id", "=", context['uid'])])
        orders = self.env["metro_park_maintenance.maintaince_order"].search([("id", "in", context['ids'])])
        for order in orders:
            order.state = "obsolete"
            order.state = "finish_accept"
            self.env["metro_park_maintenance.maintaince_order_log"].create({
                'maintaince_order': order.id,
                'action': "强制关闭",
                'operator': dispatch_user.id,
            })
