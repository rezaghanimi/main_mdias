
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DetainWizard(models.Model):
    '''
    扣车向导
    '''
    _name = 'metro_park_dispatch.detain_wizard'

    cur_train = fields.Many2one(string="现车",
                                comodel_name="metro_park_dispatch.cur_train_manage")
    reason = fields.Many2one(string='故报原因',
                             comodel_name="metro_park_dispatch.detain_reason")
    start_date = fields.Date(string="开始日期(包含)", required=True)
    end_date = fields.Date(string="结束日期(包含)", required=True)
    extra_reason_visible = fields.Boolean(string="其它原因是否显示")
    extra_reason = fields.Text(string='其它原因')

    @api.multi
    def on_ok(self):
        '''
        点击确定按扭
        :return:
        '''
        if self.extra_reason_visible:
            tmp_reason = self.extra_reason
        else:
            tmp_reason = self.reason.reason

        self.env["metro_park_dispatch.detain_his_info"].create({
            "reason": tmp_reason,
            "cur_train": self.cur_train.id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "type": "detain"
        })

    @api.onchange("reason")
    def on_change_reason(self):
        '''
        改变扣车原因，如果是其它的话则显示extra_reason
        :return:
        '''
        extra_reason_id = self.env.ref("metro_park_dispatch.detain_reason_extra").id
        for record in self:
            if record.reason.id == extra_reason_id:
                record.extra_reason_visible = True
            else:
                record.extra_reason_visible = False





