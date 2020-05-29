
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
from ...odoo_operation_log.model_extend import LogManage

LogManage.register_type('change_operating_chart', '更换运行图')
LogManage.register_type('download_diagram', '更换运行图')


class NorTimeTableConfig(models.Model):
    '''
    日常时刻表配置
    '''
    _name = 'metro_park_dispatch.nor_time_table_config'
    _description = '日常时刻表配置'
    _track_log = True
    
    day_type = fields.Many2one(string='日常类型', comodel_name='metro_park_dispatch.day_types')
    time_table = fields.Many2one(string='时刻表',
                                 comodel_name='metro_park_base.time_table')
    widget_place_holder = fields.Char(string="操作", default="")

    @api.multi
    def edit_config(self):
        '''
        更换时刻表
        :return:
        '''
        form_id = self.env.ref('metro_park_dispatch.change_time_table_wizard_form').id
        LogManage.put_log(content='运行图配置更换运行图', mode='change_operating_chart')
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.change_time_table_wizard",
            'view_mode': 'form',
            "name": "修改配置",
            # 'res_id': self.id,
            'target': 'new',
            "views": [[form_id, "form"]]
        }

    @api.multi
    def download_time_table(self):
        '''
       下载运行图
        :return:
        '''
        all_rec = self.env['metro_park_base.time_table_data'].search_read(
            [('time_table_id', '=', self.id)])
        if not all_rec:
            raise exceptions.ValidationError('当前记录不存在或已删除！')
        LogManage.put_log(content='运行图配置下载运行图', mode='download_diagram')
        return {
            'name': '下载运行图',
            "type": "ir.actions.act_url",
            'url': '/dispatch/download/time_table/%s' % self.time_table.id
        }

    @api.model
    def get_date_config(self, date_str):
        '''
        取得日期配置
        :return:
        '''
        tmp_date = pendulum.parse(date_str)
        day_of_week = tmp_date.day_of_week
        day_name_cache = {
            '周一': 1,
            '周二': 2,
            '周三': 3,
            '周四': 4,
            '周五': 5,
            '周六': 6,
            '周日': 0
        }

        # 先取得所有星期的安排
        nor_config_model = self.env['metro_park_dispatch.nor_time_table_config']
        records = nor_config_model.search([])
        # 正常配置
        nor_config_cache = {day_name_cache[record.day_type.name]: record for record in records}
        # 特殊日期的安排
        special_config_model = self.env['metro_park_dispatch.special_days_config']
        # 这个是个区间还有点小麻烦
        special_records = special_config_model.search([('date', '=', date_str)])

        special_cache = {}
        for special_record in special_records:
            tmp_start = pendulum.parse(special_record.start_date)
            tmp_end = pendulum.parse(special_record.end_date)
            while tmp_start <= tmp_end:
                special_cache[tmp_start.format('YYYY-MM-DD')] = special_record
                tmp_start.add(days=1)

        if not special_cache.get(date_str, False):
            plan_data = nor_config_cache.get(day_of_week, False)
        else:
            plan_data = special_cache.get(date_str, False)

        if plan_data:
            return plan_data.time_table.id
        else:
            raise exceptions.ValidationError('当日没有计划安排')

    @api.model
    def get_time_table_config_info(self, year, month):
        '''
        取得运行图配置信息
        :return:
        '''
        tmp_date_start = pendulum.datetime(year, month, 1)
        tmp_date_start_str = tmp_date_start.format('YYYY-MM-DD')
        days = tmp_date_start.days_in_month
        tmp_date_end = pendulum.datetime(year, month, days)
        tmp_date_end_str = tmp_date_end.format('YYYY-MM-DD')

        day_name_cache = {
            '周一': 1,
            '周二': 2,
            '周三': 3,
            '周四': 4,
            '周五': 5,
            '周六': 6,
            '周天': 7
        }

        # 先取得所有星期的安排
        nor_config_model = self.env['metro_park_dispatch.nor_time_table_config']
        records = nor_config_model.search([])
        nor_config_cache = {day_name_cache[record.day_type.name]: record for record in records}

        # 特殊日期的安排
        special_config_model = self.env['metro_park_dispatch.special_days_config']
        # 这个是个区间还有点小麻烦
        special_records = special_config_model.search([('start_date', '<=', tmp_date_start_str),
                                                       ('end_date', '>=', tmp_date_end_str)])
        special_cache = {}
        for special_record in special_records:
            tmp_start = pendulum.parse(special_record.start_date)
            tmp_end = pendulum.parse(special_record.end_date)
            while tmp_start <= tmp_end:
                special_cache[tmp_start.format('YYYY-MM-DD')] = special_record
                tmp_start.add(days=1)

        # 用户自定义的安排, 手动更改, 后续添加，这个优先级最高，暂时没有

        # 找出实际时刻表
        time_table_model = self.env['metro_park_base.real_time_table']
        real_records = time_table_model.search([('date', '>=', tmp_date_start_str),
                                                ('date', '<=', tmp_date_end_str)])
        real_data_cache = {record.date: record for record in real_records}

        # 找出正常情况下的时刻表
        events = []
        for day in range(1, days + 1):
            tmp_date = pendulum.datetime(year, month, day)
            day_of_week = tmp_date.day_of_week
            date_str = tmp_date.format('YYYY-MM-DD')
            if not special_cache.get(date_str, False):
                plan_data = nor_config_cache.get(day_of_week, False)
            else:
                plan_data = special_cache.get(date_str, False)
            real = real_data_cache.get(date_str, False)
            events.append({
                'date': date_str,
                'plan_time_table_id': plan_data.time_table.id if plan_data else 0,
                'plan_time_table_name': plan_data.time_table.name if plan_data else '',
                'real_table_name': real.time_table.name if real else '',
            })

