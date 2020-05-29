
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
from . import utility


class AddNewOutPlan(models.TransientModel):
    '''
    添加新的发车计划
    '''
    _name = 'metro_park_dispatch.add_new_out_plan'
    _description = '添加新的发车计划'
    _track_log = True

    plan_date = fields.Date(string="发车日期",
                            default=lambda self: pendulum.now("UTC").add(hours=8).format('YYYY-MM-DD'),
                            required=True)
    cur_devs = fields.Many2many(string='现车列表',
                                comodel_name='metro_park_dispatch.cur_train_manage',
                                relation='new_out_plan_plan_cur_dev_rel',
                                column1='dev_id',
                                column2='plan_id')
    split_routes = fields.Boolean(string='路径拆分', default=True)

    plan_infos = fields.Many2many(string='已选车辆',
                                  comodel_name='metro_park_dispatch.new_plan_info',
                                  relation='new_out_plan_info_rel',
                                  column1='plan_id',
                                  column2='info_id', required=True)

    @api.onchange('cur_devs')
    def on_change_cur_devs(self):
        '''
        要据选择的设备添加具体的信息
        :return:
        '''
        ids = self.cur_devs.ids
        rail_cache = {dev.id: dev.cur_rail for dev in self.cur_devs}
        old_dev_ids = self.plan_infos.mapped('cur_train_id.id')
        items = []

        location = self.env.user.cur_location
        user_location_id = location.id
        exchange_rail1 = self.env["metro_park_base.rails_sec"].search([
            ("alias", "=", "转换轨1"),
            ("location", "=", user_location_id)
        ])

        def get_rail(train_id):
            '''
            只能取本场段的位置
            :return:
            '''
            rail = rail_cache[train_id]
            if rail.location.id != user_location_id:
                return None
            else:
                return rail.id

        # 要添加的项
        for tmp_id in ids:
            if tmp_id not in old_dev_ids:
                items.append((0, 0, {
                    'cur_train_id': tmp_id,
                    'rail': get_rail(tmp_id),
                    'plan_time': utility.get_now_time_int_repr() + 5 * 60,
                    'type': 'out',
                    'plan_out_end_rail': exchange_rail1.id if exchange_rail1 else None
                }))
            else:
                # 要更新的项
                for info in self.plan_infos:
                    if info.cur_train_id.id == tmp_id:
                        items.append((1, info.id, {
                            'cur_train_id': tmp_id,
                            'rail': info["rail"],
                            'type': 'out',
                            'plan_out_end_rail': info.plan_out_end_rail
                        }))
                        break

        # 要删除的项
        for tmp in self.plan_infos:
            if tmp.cur_train_id.id not in ids:
                items.append((2, tmp.id))

        self.plan_infos = items

    @api.multi
    def on_ok(self):
        '''
        添加新的出车计划
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有配置场段！请在右上角头像处配置!")

        vals_list = []
        log_list = []

        out_train_pre_min = location.send_train_pre_min
        for info in self.plan_infos:
            val = {
                'status': 'unpublish',
                'train_id': info.cur_train_id.id,
                'plan_out_location': location.id,
                'date': self.plan_date,
                'plan_out_rail': info.rail.id,
                'plan_out_time': info.plan_time,
                'exchange_rail_time': info.exchange_rail_time,
                "plan_train_no": info.plan_train_no,
                "plan_out_end_rail": info.plan_out_end_rail.id
            }
            if info.plan_time:
                val["exchange_rail_time"] = info.plan_time + \
                    out_train_pre_min * 60
            else:
                val["exchange_rail_time"] = None
            vals_list.append(val)
            log = {
                'type': 'out_plan',
                'train_dev': info.cur_train_id.train.id,
                'operation': '新增发车计划'
            }
            log_list.append(log)
        self.env['metro_park_dispatch.train_out_plan'].create(vals_list)
        self.env['metro_park_dispatch.train_in_out_log'].create(log_list)
