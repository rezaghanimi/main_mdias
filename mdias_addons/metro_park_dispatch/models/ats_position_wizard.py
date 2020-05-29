
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AtsPositionWizard(models.Model):
    '''
    ats车辆位置模拟
    '''
    _name = 'metro_park_dispatch.ats_position_wizard'

    train_id = fields.Many2one(string="车辆",
                               required=True,
                               comodel_name='metro_park_maintenance.train_dev')
    location = fields.Many2one(string="位置",
                               required=True,
                               comodel_name="metro_park_base.location")
    position = fields.Many2one(string="区段",
                               required=True,
                               comodel_name="metro_park_base.rails_sec")

    @api.multi
    def on_ok(self):
        '''
        确认按扭点击
        :return:
        '''
        self.env["metro_park_dispatch.cur_train_manage"]\
            .update_position(self.position.location.id,
                             self.train_id.dev_no,
                             self.position.no)


