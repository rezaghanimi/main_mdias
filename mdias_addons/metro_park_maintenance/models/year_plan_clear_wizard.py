# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class YearPlanClearWizard(models.Model):
    '''
    年计划
    '''
    _name = 'metro_park_maintenance.year_plan_clear_wizard'
    
    start_month = fields.Many2one(comodel_name='metro_park_maintenance.month', string='起始月份', required=True)
    end_month = fields.Many2one(comodel_name="metro_park_maintenance.month", string="截止月份", required=True)

    @api.multi
    def on_ok(self):
        """
            点击确认按扭, 执行清除
        :return:
        :return:
        """
        self.ensure_one()
        year_plan_id = self.env.context.get('year_plan_id')   # 获取上下文的年计划id
        start_month = self.start_month.val
        end_month = self.end_month.val
        if start_month > end_month:
            raise exceptions.UserError("截止日期不能小于起始日期！")
        self.env["metro_park_maintenance.year_plan"].browse(year_plan_id).clear_year_info(start_month, end_month)
        return {'type': 'ir.actions.act_window_close'}

    @api.onchange('start_month')
    def _onchange_start_month(self):
        """
        当起始日期发生变更时，自动补全截止日期
        :return:
        """
        for res in self:
            if res.start_month:
                res.end_month = res.start_month.id
