
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import utility


class InterlockTable(models.Model):
    '''
    联锁表
    '''
    _name = 'metro_park.interlock.table'
    _description = '联锁表信息'
    _track_log = True

    location = fields.Many2one(string="线路",
                               comodel_name="metro_park_base.location",
                               required=True)

    route_ids = fields.One2many(string='列车进路',
                                comodel_name='metro_park.interlock.route',
                                inverse_name='table_id')

    file_data = fields.Binary(string='联锁文件', required=True)
    file_name = fields.Char(string='文件名称', required=True)

    @api.model
    def get_inter_lock_table_data(self, time_table_id):
        '''
        取得联锁表数据, 把这些信息全部拿到前端去，要的时候再去取，省得在这里组合来组合去，麻烦
        :return:
        '''

        record = self.browse(time_table_id)

        # 取得所有的进路
        routes = record.route_ids
        route_records = utility.datetime_to_str(routes.read())

        # 取得轨道区段信息
        rail_secs = routes.mapped('sec_infos.sec')
        sec_info_records = utility.datetime_to_str(rail_secs.read())
        sec_info_cache = {info['id']: info for info in sec_info_records}

        # 取得信号机信息
        signals = routes.mapped('signals_infos.signal')
        extra_signals = routes.mapped('hostile_signal_infos.signal')
        signals = signals.union(extra_signals)
        signals_records = utility.datetime_to_str(signals.read())
        signal_cahce = {info['id']: info for info in signals_records}

        # 取得信号机信息
        signals_infos = routes.mapped('signals_infos')
        signals_infos = utility.datetime_to_str(signals_infos.read())
        signals_infos_cache = {info['id']: info for info in signals_infos}

        # 取得道岔信息
        switches = routes.mapped('switch_infos.switch')
        switch_records = utility.datetime_to_str(switches.read())
        switch_cahce = {info['id']: info for info in switch_records}

        # 道岔信息
        switch_infos = routes.mapped('switch_infos')
        switch_infos = utility.datetime_to_str(switch_infos.read())
        switch_info_cahce = {info['id']: info for info in switch_infos}

        # 敌对信号信息
        hostile_info = routes.mapped('hostile_signal_infos')
        hostile_info_records = utility.datetime_to_str(hostile_info.read())
        hostile_info_cahce = {info['id']: info for info in hostile_info_records}

        # 敌对信号条件道岔信息，这个是个单独的表
        condition_switches = routes.mapped('hostile_signal_infos.condition_switches')
        condition_switches_records = utility.datetime_to_str(condition_switches.read())
        condition_switches_cache = {info['id']: info for info in condition_switches_records}

        return {
            'route_records': route_records,
            'sec_info_cache': sec_info_cache,
            'signals_info_cache': signals_infos_cache,
            'signal_cahce': signal_cahce,
            'switch_info_cahce': switch_info_cahce,
            'switch_cahce': switch_cahce,
            'hostile_info_cahce': hostile_info_cahce,
            'condition_switches_cache': condition_switches_cache
        }
