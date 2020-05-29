
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
import pendulum
from datetime import datetime
import logging
from ...odoo_operation_log.model_extend import LogManage

_logger = logging.getLogger(__name__)


class TimeTable(models.Model):
    '''
    运行图管理
    '''
    _name = 'metro_park_base.time_table'
    _rec_name = 'no'
    _order = 'id desc'
    _description = '时刻表'
    _track_log = True

    def _default_sequence(self):
        '''
        取得默认的序号
        :return:
        '''
        return self.env['ir.sequence'].next_by_code('time_table.number')
    
    no = fields.Char(string='运行图编号', default="_default_sequence")
    time_table_type = fields.Selection(string='运行图类型',
                                       selection=[('weekday', '平日'),
                                                  ('weekend', '周未')])
    update_time = fields.Datetime(string='更新时间')
    # 时刻表数据
    time_table_data = fields.One2many(string="时刻表数据",
                                      comodel_name="metro_park_base.time_table_data",
                                      inverse_name="time_table_id")
    state = fields.Selection(string='状态',
                             selection=[('active', '启用'),
                                        ('disabled', '失效')], default='active')
    button = fields.Char(string="按扭", help="用于占位")

    @api.multi
    def del_time_table(self):
        '''
        删除时刻表
        :return:
        '''
        self.unlink()

    @api.multi
    def view_time_table(self):
        '''
        查看运行图
        :return:
        '''
        action = self.env.ref('metro_park_base.time_table_data_act_window').read()[0]
        action['target'] = 'new'
        action['domain'] = [('time_table_id', '=', self.id)]
        return action

    @api.multi
    def download_time_table(self):
        '''
        下载运行图
        :return:
        '''
        all_rec = self.env['metro_park_base.time_table_data'].search_read(
            [('time_table_id', '=', self.id)])
        if not all_rec:
            raise ValidationError('当前记录不存在或已删除！')
        return {
            'name': '运行图下载',
            'type': 'ir.actions.act_url',
            'url': '/dispatch/download/time_table/%s' % self.id
        }

    @api.multi
    def change_status(self):
        '''
        禁用运行图
        :return:
        '''
        self.ensure_one()
        if self.state == "active":
            self.state = 'disabled'
        else:
            self.state = "active"

    @api.model
    def sync_time_table(self):
        '''
        同步ats时刻表, 1、如果查看当天是否已经同步，如果已经同步则不在进行
        :return:
        '''
        today_obj = pendulum.today("UTC").add(hours=8)
        today_str = today_obj.format("YYYY-MM-DD")

        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        self.env["metro_park_dispatch.msg_client"] \
            .get_time_tables([{
                "location": ban_qiao,
                "date": today_str
            }, {
                "location": gao_da_lu,
                "date": today_str
            }])
        LogManage.put_log(content='手动同步', mode='manual_sync')

    @api.model
    def deal_new_time_table_data(self, datas):
        '''
        处理新的时刻表数据, 从ats获取到数据以后
        [
            {
                "End_station_id": 0,
                "Start_station_id": 0,
                "date": "2019-8-9 0:0:0",
                "line_id": 10,
                "msg_id": 34,
                "sub_id": 2,
                "trip_cnt": 47,
                "trip_list": [
                    {
                        "Global_id": "1041",
                        "destination_id": 822083584,
                        "rec_cnt": 3,
                        "train_id": "",
                        "trip_rec_list": [
                            {
                                "Flag": 0,
                                "a_time": "2019-8-9 6:14:34",
                                "d_time": "2019-8-9 6:14:34",
                                "platform_id": 1,
                                "station_id": 14
                            },
                            {
                                "Flag": 0,
                                "a_time": "2019-8-9 6:16:22",
                                "d_time": "2019-8-9 6:17:7",
                                "platform_id": 1,
                                "station_id": 15
                            },
                            {
                                "Flag": 0,
                                "a_time": "2019-8-9 6:18:26",
                                "d_time": "2019-8-9 6:18:56",
                                "platform_id": 1,
                                "station_id": 16
                            }
                        ]
                    },
            ...
        :return:
        '''
        _logger.info("get time table data:")
        if len(datas) == 0:
            return

        # 缓存所有的地址
        ats_addresses = self.env["metro_park_base.ats_address"]\
            .search([])
        ats_address_cache = {address.no: address.location.id for address in ats_addresses}

        # 如果时刻表已经存在了的话则只是更新，
        # 如果数据不相同，那么则是计划时刻表与实际时刻表不相同
        time_table_data = []
        sequence = 1
        for data in datas:
            trip_list = data['trip_list']
            date = data["date"]

            for index, trip in enumerate(trip_list):
                train_no = trip['Global_id']
                trip_rec_list = trip['trip_rec_list']
                if len(trip_rec_list) >= 1:
                    start_data = trip_rec_list[0]
                    out_location = start_data["station_id"]
                    plan_out_time = start_data["d_time"]
                    end_data = trip_rec_list[-1]
                    back_location = end_data["station_id"]
                    plan_in_time = end_data["a_time"]
                    time_table_data.append((0, 0, {
                        "sequence": sequence,
                        "train_no": train_no,
                        "out_location": ats_address_cache.get(str(out_location)),
                        "back_location": ats_address_cache.get(str(back_location)),
                        "plan_out_time": plan_out_time,
                        "plan_in_time": plan_in_time
                    }))
                    sequence += 1
                else:
                    raise exceptions.Warning("时刻表数据错误")

        self.create([{
            "no": date,
            "update_time": pendulum.now('UTC').format('YYYY-MM-DD HH:mm:ss'),
            "time_table_data": time_table_data,
        }])

    @api.model
    def auto_get_time_table(self):
        '''
        自动获取时刻表数据，分别获取时刻表数据
        :return:
        '''
        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        self.env["metro_park_dispatch.msg_client"]\
            .get_time_table(ban_qiao, pendulum.today("UTC")
                            .add(hours=8)
                            .format("YYYY-MM-DD"))
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id
        self.env["metro_park_dispatch.msg_client"] \
            .get_time_table(gao_da_lu, pendulum.today("UTC")
                            .add(hours=8)
                            .format("YYYY-MM-DD"))

    def get_clndr_events(self, year, month):
        '''
        日历计划运行图，实际运行图
        :return:
        '''
        events = []
        weeks = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        # 获取特殊时刻表
        others = self.env['metro_park_dispatch.special_days_config'].search([])
        # 月初
        year_month = pendulum.datetime(year, month+1, 1, tz='UTC')
        # 本月天数
        days = year_month.days_in_month
        for day in range(days):
            day_time = pendulum.datetime(year, month + 1, day+1, tz='UTC')
            day_week = day_time.day_of_week
            day_date = datetime.date(datetime.strptime(day_time.format('YYYY-MM-DD'), '%Y-%m-%d'))
            special_available = others.filtered(lambda x: x.date == day_date)

            if special_available:
                val = {
                    'date': day_time.format('YYYY-MM-DD'),
                    'plan': special_available.time_table.no,
                    'actual': special_available.time_table.no,
                    'plan_id': special_available.time_table.id,
                    'actual_id': special_available.time_table.id
                }
            else:
                default = self.env['metro_park_dispatch.nor_time_table_config'].search(
                    [('day_type.name', '=', weeks[day_week])])
                if default:
                    val = {
                        'date': day_time.format('YYYY-MM-DD'),
                        'plan': default.time_table.no,
                        'actual': default.time_table.no,
                        'plan_id': default.time_table.id,
                        'actual_id': default.time_table.id
                    }
            if val:
                events.append(val)

        return events

