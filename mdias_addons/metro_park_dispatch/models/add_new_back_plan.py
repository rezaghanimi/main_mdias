
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
from . import utility


class AddNewBackPlan(models.TransientModel):
    '''
    添加新的收车计划
    '''
    _name = 'metro_park_dispatch.add_new_back_plan'
    _description = '添加新的收车计划'
    _track_log = True

    # 不要用today, today是算的当日开始的时间，加上8小时仍然不正确
    plan_date = fields.Date(string="计划日期",
                            default=lambda self: pendulum.now(
                                "UTC").add(hours=8).format('YYYY-MM-DD'),
                            required=True)

    cur_devs = fields.Many2many(string='现车列表',
                                comodel_name='metro_park_dispatch.cur_train_manage',
                                relation='new_back_plan_cur_train_dev_rel',
                                column1='plan_id',
                                column2='dev_id')

    plan_infos = fields.Many2many(string='加开列表',
                                  comodel_name='metro_park_dispatch.new_plan_info',
                                  relation='new_plan_info_rel',
                                  column1='plan_id',
                                  column2='info_id', required=True)

    @api.onchange('cur_devs')
    def on_change_cur_devs(self):
        '''
        加开只能是
        :return:
        '''
        ids = self.cur_devs.ids
        rail_cache = {dev.id: dev.cur_rail.id for dev in self.cur_devs}
        old_dev_ids = self.plan_infos.mapped('cur_train_id.id')
        items = []

        # 要添加的项
        for tmp_id in ids:
            if tmp_id not in old_dev_ids:
                items.append((0, 0, {
                    'cur_train_id': tmp_id,
                    'rail': rail_cache[tmp_id],
                    'exchange_rail_time': utility.get_now_time_int_repr() + 10 * 60,
                    'type': 'back'
                }))
            else:
                # 要更新的项
                for info in self.plan_infos:
                    if info.cur_train_id.id == tmp_id:
                        items.append((1, info.id, {
                            'cur_train_id': tmp_id,
                            'rail': rail_cache[tmp_id],
                            'type': 'back'
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
        点击确定
        :return:
        '''
        vals_list = []
        log_list = []

        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有配置场段！请在右上角头像处配置!")

        back_train_need_min = location.receive_train_need_min

        for info in self.plan_infos:
            if not info.plan_time or not info.rail:
                raise exceptions.Warning("信息填写不完整")

            val = {
                'status': 'unpublish',
                'train_id': info.cur_train_id.id,
                'plan_back_location': location.id,
                'date': self.plan_date,
                'plan_back_time': info.plan_time,
                'plan_back_rail': info.rail.id,
                'exchange_rail_time': info.exchange_rail_time,
                "plan_train_no": info.plan_train_no
            }
            if info.exchange_rail_time:
                val["plan_back_time"] = info.exchange_rail_time - \
                    back_train_need_min * 60
            else:
                val["plan_back_time"] = None
            vals_list.append(val)
            log = {
                'type': 'in_plan',
                'train_dev': info.cur_train_id.train.id,
                'operation': '新增收车计划'
            }
            log_list.append(log)

        self.env['metro_park_dispatch.train_back_plan'].create(vals_list)
        self.env['metro_park_dispatch.train_in_out_log'].create(log_list)
