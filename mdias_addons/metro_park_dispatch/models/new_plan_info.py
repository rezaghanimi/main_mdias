
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
from . import utility


class NewPlanInfo(models.Model):
    '''
    计划信息
    '''
    _name = 'metro_park_dispatch.new_plan_info'
    _description = '车辆设备信息'
    _track_log = True

    @api.multi
    def _get_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            if self.plan_out_end_rail:
                domain.append(('id', '!=', self.plan_out_end_rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    @api.multi
    def _get_plan_out_end_rail_domain(self):
        domain = []
        if self.env.user.cur_location:
            domain.append(('location.id', '=', self.env.user.cur_location.id))
            if self.rail:
                domain.append(('id', '!=', self.rail.id))
        else:
            domain = [('id', '=', -1)]
        return domain

    cur_train_id = fields.Many2one(string='车辆',
                                   comodel_name='metro_park_dispatch.cur_train_manage')
    type = fields.Selection(string='类型',
                            selection=[('back', '收车'), ('out', '发车')])
    plan_train_no = fields.Char(string="计划车次")
    rail = fields.Many2one(string='位置',
                           comodel_name="metro_park_base.rails_sec", domain=_get_rail_domain)
    plan_out_end_rail = fields.Many2one(string='出/入场段位置',
                                        comodel_name='metro_park_base.rails_sec',
                                        domain=_get_plan_out_end_rail_domain)

    plan_time = fields.Integer(string="计划时间",
                               default=utility.get_now_time_int_repr(),
                               required=True)

    exchange_rail_time = fields.Integer(string="转换轨时间",
                                        default=utility.get_now_time_int_repr(),
                                        required=True)

    @api.onchange("cur_train_id")
    def on_change_cur_train(self):
        '''
        改变现车的时候，默认为当前现车的位置
        :return:
        '''
        if self.cur_train_id:
            self.rail = self.cur_train_id.cur_rail.id

    @api.model
    def get_rail_domain(self, record):
        '''
        取得轨道的选择范围, 必需和出段地址相同，并且只能选择转换轨
        :return:
        '''
        if not record:
            return [('id', '=', None)]
        data = record["data"]
        if data["rail"]:
            rail_id = data["rail"]["data"]["id"]
            record = self.env["metro_park_base.rails_sec"].browse(rail_id)
            return [("location", "=", record.location.id),
                    ("rail_type.name", "=", "转换轨")]
        else:
            return [('id', '=', None)]
