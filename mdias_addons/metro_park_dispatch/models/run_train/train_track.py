# -*- coding: utf-8 -*-
import logging
import traceback

from odoo import models, fields, api
from ....odoo_operation_log.model_extend import LogManage
from datetime import datetime
_logger = logging.getLogger(__name__)

RAIL_OUT_AND_IN = ['T1710G', 'T2604G', 'T1705G', 'T2615G']

LogManage.register_type('train_track', "现车跟踪")


class TrainPosTrack(models.Model):
    """
        当轨迹道岔和轨道都为空时表示该车已经不在站场
    """
    _name = 'metro_park_dispatch.train_track'
    _track_log = True
    _order = 'create_date desc'
    _description = 'train track'

    track_type = fields.Selection([('switch', '道岔'), ('rail', '轨道')], string='轨迹类型')
    cur_train_id = fields.Many2one(string='现车',
                                   comodel_name='metro_park_dispatch.cur_train_manage')
    rail_id = fields.Many2one(string='股道',
                              comodel_name='metro_park_base.rails_sec')
    switch_id = fields.Many2one('metro_park_base.switches', string='道岔')
    arrive_time = fields.Datetime(string='到达时间', default=fields.Datetime.now)
    leave_time = fields.Datetime(string='离开时间')
    description = fields.Text(string="描述")
    remark = fields.Char(string='备注')
    back_id = fields.Many2one('metro_park_dispatch.train_back_plan', string='收车计划')
    out_id = fields.Many2one('metro_park_dispatch.train_out_plan', string='发车计划')
    dispatch_id = fields.Many2one('metro_park_dispatch.dispatch_notice', string='调车计划')

    def _get_back_and_out_plan(self, train_id):
        back_res = self.env['metro_park_dispatch.train_back_plan']. \
            search([('train_id', '=', train_id), ('state', '=', 'executing')])
        if back_res:
            back_id = back_res.id
            return [back_id, None, None]
        dispatch_res = self.env['metro_park_dispatch.dispatch_notice']. \
            search([('train', '=', train_id), ('state', '=', 'executing')])
        if dispatch_res:
            dispatch_id = dispatch_res.id
            return [None, None, dispatch_id]

        out_res = self.env['metro_park_dispatch.train_out_plan']. \
            search([('train_id', '=', train_id), ('state', '=', 'executing')])
        if out_res:
            out_id = out_res.id
            return [None, out_id, None]
        return [None, None, None]

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        result = self.browse()
        if isinstance(vals, dict):
            vals = [vals]
        for val in vals:
            if 'cur_train_id' not in val:
                continue
            train_id = val['cur_train_id']
            back_id, out_id, dispatch_id = self._get_back_and_out_plan(train_id)
            val.update({
                'back_id': back_id,
                'out_id': out_id,
                'dispatch_id': dispatch_id
            })
            result += super(TrainPosTrack, self).create(val)
        return result

    def update_track(self, train_id, switch_id=None, rail_id=None, level=False):
        '''
        更新轨道
        :param train_id:
        :param switch_id:
        :param rail_id:
        :param level:
        :return:
        '''
        try:
            if not (switch_id or rail_id):
                return False
            if not level:
                self.create([{
                    'cur_train_id': train_id,
                    'rail_id': rail_id,
                    'switch_id': switch_id
                }])
            else:
                track_id = self.search([('cur_train_id', '=', train_id), '|',
                                        ('rail_id', '=', rail_id), ('switch_id', '=', switch_id)])
                if track_id:
                    track_id.write({
                        'leave_time': datetime.now()
                    })
        except Exception as e:
            _logger.info('update track exception!', e)
            traceback.print_exc()
