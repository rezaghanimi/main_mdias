# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
from . import util


class TrainBackPlan(models.Model):
    '''
    发车计划
    '''
    _inherit = 'metro_park_dispatch.train_back_plan'

    @api.multi
    def get_location_spell(self):
        '''
        取得位置
        :return:
        '''
        self.ensure_one()

        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        if self.plan_back_rail:
            if self.plan_back_rail.location.id == ban_qiao:
                location = 'banqiao'
            elif self.plan_back_rail.location.id == gao_da_lu:
                location = 'gaodalu'
            else:
                location = self.env.user.cur_location.alias

            return location

        return None

    @api.model
    def dynamic_plan_rail(self, train_id, location_id):
        '''
        如果回来的车位置被占用了，那么动态的去找一个轨道进行安排
        :return:
        '''

        # 不占用别的车要用的轨道
        # 如果第二天有检修任务的话那么则要考虑检修的需求
        # 不能挡住要回的车的轨道
        # 按优先级进行排列
        # 如果找不到则提醒场调自己去安排
        # 不能挡住要发车的轨道

        today = pendulum.today('UTC')
        next_day = today.date(days=1)

        # 取得未完成的收车计划
        train_back_plans = \
            self.search([('date', '=', today.format('YYYY-MM-DD')),
                         ('state', '=', 'preparing'),
                         ('train_id', '!=', train_id)])
        plan_rail_ids = train_back_plans.mapped('plan_back_rail.id')

        # 取得当天的发车计划, 不要把路给挡了
        train_out_plans = \
            self.search([('date', '=', today.format('YYYY-MM-DD')),
                         ('state', '=', 'preparing'),
                         ('plan_out_rail.port', '=', 'B')])
        out_rails = train_out_plans.mapped('plan_out_rail.reverse_port.id')

        # 查看设备的检修要求
        rule_infos = self.env["metro_park_maintenance.rule_info"].search(
            [('date', 'in', [today.format("YYYY-MM-DD"), next_day.format('YYYY-MM-DD')]),
             ('rule', '!=', False),
             ('state', '=', 'published'),
             ('back_location_id', '=', location_id)])
        work_requirement = rule_infos.mapped("work_requirement.ids")

        # 取得所有可停车的股道, 然后扣除现车占用的和计划需要占用的
        usable_rails = self.env["metro_park_base.rails_sec"] \
            .search([('can_stop', '=', True),
                     ('location', '=', location_id),
                     ('id', 'not in', plan_rail_ids + out_rails),
                     ('rail_property', 'in', work_requirement)],
                    order="stop_order asc")

        return usable_rails


