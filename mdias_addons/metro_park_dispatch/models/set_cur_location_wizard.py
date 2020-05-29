# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SetCurLocationWizard(models.TransientModel):
    '''
    设置车辆当前位置
    '''
    _name = 'metro_park_dispatch.set_cur_location_wizard'
    _track_log = True

    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location',
                               required=True)
    rail = fields.Many2one(string='轨道',
                           comodel_name='metro_park_base.rails_sec',
                           required=True)

    @api.onchange('location')
    def on_change_location(self):
        '''
        当位置发生改变的时候, 只能选择location下面的rail
        :return:
        '''
        domain = []
        if self.location:
            domain.append(('location', '=', self.location.id))
        else:
            domain.append(('location', 'in', []))

        return {
            "domain": {
                "rail": domain
            }
        }

    @api.multi
    def on_ok(self):
        '''
        确定
        :return:
        '''
        active_id = self.env.context.get('active_id')
        model = self.env["metro_park_dispatch.cur_train_manage"]
        record = model.browse(active_id)
        record.write({
            'location': self.location.id,
        })
        # 创建轨迹
        self.env['metro_park_dispatch.train_track'].update_track(True, self.location.id,
                                                                 run_train_id=active_id,
                                                                 rail_id=self.rail.id)
