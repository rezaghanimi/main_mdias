
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum


LAST_TRAIN_INFO = {}


class ChosePosWizard(models.TransientModel):
    '''
    位置选择向导, 车辆到达时如果没有选择轨道的话则弹出对话框让用户选择
    '''
    _name = 'metro_park_dispatch.chose_pos_wizard'

    method = fields.Selection(
        selection=[('recommend', '推荐选择'), ('user_decide', '用户决定')],
        default='user_decide',
        string="方式")

    train_id = fields.Many2one(string="车辆",
                               comodel_name="metro_park_dispatch.cur_train_manage")

    start_rail = fields.Many2one(string="起始轨道",
                                 comodel_name="metro_park_base.rails_sec",
                                 required=True,
                                 help="开始的转换轨")
    # 这个要动态获取domain
    end_rail = fields.Many2one(string="轨道",
                               comodel_name="metro_park_base.rails_sec",
                               required=True,
                               help="选择的哪根轨道")

    decision_info = fields.Text(string="决策信息")

    recommend_rail = fields.Many2one(string="推荐轨道",
                                     comodel_name="metro_park_base.rails_sec")

    @api.onchange('recommend_rail')
    def on_change_recommend_rial(self):
        '''
        选择推荐轨道
        :return:
        '''
        self.end_rail = self.recommend_rail.id

    @api.model
    def get_position_wizard(self, train_id, location_alias, rail_no):
        '''
        没有安排的时候弹出对话框,
        1、提供当前车辆的检修信息
        2、提供提供轨道信息属性信息
        :param train_id:
        :param location_alias:
        :param rail_no:
        :return:
        '''
        # 防止重复
        global LAST_TRAIN_INFO

        # 没有配置位置不作处理
        location = self.env.user.cur_location
        if not location:
            return None

        cur_train = self.env['metro_park_dispatch.cur_train_manage'].browse(train_id)

        # 配置为不作处理
        train_back_deal_method = location.temp_train_back_deal_method.value
        # 用户自行选择
        if train_back_deal_method == 'user_select':

            if LAST_TRAIN_INFO and\
                    location_alias == LAST_TRAIN_INFO["location_alias"] \
                    and train_id == LAST_TRAIN_INFO["train_id"]:
                now_time = pendulum.now("UTC")
                delta = now_time - LAST_TRAIN_INFO["time"]
                if delta.minutes < 2:
                    return

            LAST_TRAIN_INFO = {
                'train_id': train_id,
                'location_alias': location_alias,
                'time': pendulum.now("UTC")
            }

            start_rail = self.env["metro_park_base.rails_sec"]\
                .search(['|', ('no', '=', rail_no),
                         ('alias', '=', rail_no),
                         ('location.alias', '=', location_alias)])

            # 动态查找可用轨道, 提供推荐轨道
            rails = self.env['metro_park_dispatch.train_back_plan'].dynamic_plan_rail()

            # 当日作业相关
            today = pendulum.today('UTC')
            next_day = today.add(days=1)
            rule_infos = self.env['metro_park_maintenance.rule_info'].search(
                [('dev', '=', cur_train.dev.id),
                 ('date', '=', today.format('YYYY-MM-DD')),
                 ('rule', '!=', False),
                 ('data_source', '=', 'day'),
                 ('rule.target_plan_type', 'in', ['year', 'month', 'week']),
                 ('state', '!=', 'finished')])
            rules = rule_infos.mapped('rule.no')
            work_requirements = rule_infos.mapped('work_requirement.name')

            # 次日作业相关
            rule_infos = self.env['metro_park_maintenance.rule_info'].search(
                [('dev', '=', cur_train.dev.id),
                 ('date', '=', next_day.format('YYYY-MM-DD')),
                 ('rule', '!=', False),
                 ('data_source', '=', 'day'),
                 ('rule.target_plan_type', 'in', ['year', 'month', 'week']),
                 ('state', '!=', 'finished')])
            next_day_rules = rule_infos.mapped('rule.no')
            next_day_work_requirements = rule_infos.mapped('work_requirement.name')

            text = ''
            if len(rules) > 0:
                text += '当日作业:' + ','.join(rules) + "\n"

            if len(work_requirements) > 0:
                text += '当日作业要求:' + ','.join(work_requirements) + "\n"

            if len(next_day_rules) > 0:
                text += '次日作业:' + ','.join(next_day_rules) + "\n"

            if len(next_day_work_requirements) > 0:
                text += '次日作业要求:' + ','.join(next_day_work_requirements) + "\n"

            return {
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "metro_park_dispatch.chose_pos_wizard",
                "name": "收车位置向导",
                "target": "new",
                "context": {
                    "default_train_id": train_id,
                    "default_start_rail": start_rail.id,
                    "location_alias": location_alias,
                    "default_recommend_rails": rails.ids[0] if rails else False,
                    "default_decision_info": text
                },
                "domain": {
                    "recommend_rails": [('id', 'in', rails.ids)]
                },
                "views": [[False, "form"]]
            }

    @api.model
    def get_rail_domain(self, record):
        '''
        取得轨道的domain, 先来个简单版本的
        :param record:
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError('当前用户没有设置场段信息')

        cur_train = self.env["metro_park_dispatch.cur_train_manage"]\
            .search([('cur_rail', '!=', False)])
        rails = cur_train.mapped('cur_rail.id')

        rail_type_stop_and_check = \
            self.env.ref("metro_park_base.rail_type_stop_and_check").id

        free_rails = self.env["metro_park_base.rails_sec"]\
            .search([('id', 'not in', rails),
                     ('rail_type', '=', rail_type_stop_and_check),
                     ('location', '=', location.id)])

        return [('id', 'in', free_rails.ids)]

    @api.multi
    def on_chose_position(self):
        '''
        选择位置
        :return:
        '''

        # 创建计划
        data = dict()
        data['train_id'] = self.train_id.id
        data['state'] = 'unpublish'
        data['plan_back_time'] = pendulum.now("UTC")
        data['exchange_rail_time'] = pendulum.now("UTC")
        data['date'] = pendulum.now('UTC').add(hours=8).format('YYYY-MM-DD')
        data['real_start_rail'] = self.start_rail.id
        data['plan_back_rail'] = self.end_rail.id
        data['real_back_rail'] = self.end_rail.id

        data['plan_back_location'] = self.start_rail.location.id

        record = self.env["metro_park_dispatch.train_back_plan"].create(data)

        # 推送到信号楼
        location = record.get_location_spell()
        data = record.get_plan_data()
        if data:
            record.state = 'preparing'
            self.trigger_up_event("funenc_socketio_server_msg", data={
                "msg_type": "add_plan",
                "msg_data": [data],
                "location": location
            }, room="xing_hao_lou")

        return False
