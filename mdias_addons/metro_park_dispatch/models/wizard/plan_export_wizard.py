# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api


class WizardExportPlan(models.TransientModel):
    _name = 'metro_park_dispatch.wizard.plan_export'

    export_plan_date = fields.Date(string='导出日期',
                                   required=True,
                                   default=lambda self: date.today())

    @api.multi
    def action_export(self):
        return [{
            'name': '收发车计划导出',
            'target': 'self',
            'type': 'ir.actions.act_url',
            'url': '/metro_park_dispatch/export_train_plan?plan_date=%s' %
                   self.export_plan_date
        }, {'type': 'ir.actions.act_window_close'}]
