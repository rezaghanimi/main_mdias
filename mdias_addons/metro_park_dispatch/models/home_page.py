# -*- coding: utf-8 -*-

import pendulum

from odoo import models, api


class HomePage(models.TransientModel):
    '''
    初始化向导, 为了防止错误的进行初始化操作
    '''
    _name = 'metro_park_dispatch.home_page'
    _track_log = True

    @api.model
    def get_today_info(self):
        '''
        取得当天的统计信息
        :return:
        '''
        today = pendulum.today("UTC")
        today_str = today.format("YYYY-MM-DD")
        return self.search_home_page_info(today_str, today_str)

    @api.model
    def search_home_page_info(self, start_date, end_date):
        '''
        取得调车计划
        :return:
        '''
        return {
            "dispatch_info": self.sudo().get_dispatch_plan_info(start_date, end_date),
            "out_plan_info": self.sudo().get_out_plan_info(start_date, end_date),
            "back_plan_info": self.sudo().get_back_plan_info(start_date, end_date),
            "repair_plan_info": self.sudo().get_repair_plan_info(start_date, end_date),
            "vehicle_running": self.sudo().search_vehicle_running_status(start_date, end_date),
        }

    @api.model
    def search_vehicle_running_status(self, start_date, end_date):
        self.daily_inspection_car()
        # 备用车
        standby = [0, ['未设置']]
        # 日检车
        inspection = self.daily_inspection_car()
        # 洗车安排
        wash = self.wash_car_arrangement()
        # 登顶车
        top = self.top_car()
        # 维修故障车
        defective = self.repair_faulty_vehicles()
        # 不可运用车
        unserviceable = self.non_serviceable_vehicle()
        # 专业作业车
        special = self.special_operation_vehicle()
        # 计划维修车
        scheduled = self.repair_faulty_vehicles()
        # 一共有多少车
        all_status = 0

        # 计算出一共有多少车辆
        all_status = standby[0] + inspection[0] + wash[0] + top[0] + defective[0] + \
                     unserviceable[0] + special[0] + scheduled[0]

        return {
            'standby': standby if standby[1] else [0, ['无']],
            'inspection': inspection if inspection[1] else [0, ['无']],
            'wash': wash if wash[1] else [0, ['无']],
            'top': top if top[1] else [0, ['无']],
            'defective': defective if defective[1] else [0, ['无']],
            'unserviceable': unserviceable if unserviceable[1] else [0, ['无']],
            'special': special if special[1] else [0, ['无']],
            'scheduled': scheduled if scheduled[1] else [0, ['无']],
            'all_status': all_status,
        }

    @api.multi
    def daily_inspection_car(self):
        # 日检车
        car_list = []
        all_data = self.env['metro_park_maintenance.rule_info'].search(
            [('data_source', '=', 'day'), ('rule_name', '=', '里程检')])
        for data in all_data:
            if data.dev.dev_name not in car_list:
                car_list.append(data.dev.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def wash_car_arrangement(self):
        # 洗车安排
        car_list = []
        all_data = self.env['metro_park_maintenance.rule_info'].search(
            [('data_source', '=', 'day'), ('rule_name', '=', '洗车')])
        for data in all_data:
            if data.dev.dev_name not in car_list:
                car_list.append(data.dev.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def top_car(self):
        # 登顶车
        car_list = []
        all_data = self.env['metro_park_maintenance.rule_info'].search(
            [('data_source', '=', 'day'), ('rule_name', '=', '登顶')])
        for data in all_data:
            if data.dev.dev_name not in car_list:
                car_list.append(data.dev.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def repair_faulty_vehicles(self):
        # 维修故障车
        car_list = []
        all_data = self.env['metro_park_dispatch.cur_train_manage'].search(
            [('train_status', '=', 'fault')])
        for data in all_data:
            if data.train.dev_name not in car_list:
                car_list.append(data.train.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def non_serviceable_vehicle(self):
        # 不可运用车
        car_list = []
        all_data = self.env['metro_park_dispatch.cur_train_manage'].search(
            [('train_status', '=', 'detain')])
        for data in all_data:
            if data.train.dev_name not in car_list:
                car_list.append(data.train.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def special_operation_vehicle(self):
        # 专项作业车
        car_list = []
        all_data = self.env['metro_park_maintenance.rule_info'].search(
            [('data_source', '=', 'day'), ('rule_name', '=', '里程检')])
        for data in all_data:
            if data.dev.dev_name not in car_list:
                car_list.append(data.dev.dev_name)
        return [len(all_data), car_list]

    @api.multi
    def scheduled_service_vehicle(self):
        # 计划维修车
        car_list = []
        all_data = self.env['metro_park_maintenance.rule_info'].search(
            [('data_source', '=', 'day'), ('rule_name', 'not in', ['正线运营', '接车', '发车'])])
        for data in all_data:
            if data.dev.dev_name not in car_list:
                car_list.append(data.dev.dev_name)
        return [len(all_data), car_list]

    @api.model
    def get_dispatch_plan_info(self, start_date, end_date):
        '''
        取得调车计划数据
        :return:
        '''
        records = self.env["metro_park_dispatch.dispatch_request"] \
            .sudo().search([('dispatch_date', '>=', start_date),
                            ('dispatch_date', '<=', end_date)])
        date_cache = {}
        for record in records:
            date_cache.setdefault(str(record.dispatch_date), []).append(record)

        tmp_rst = {}
        for key, items in date_cache.items():
            count = len(items)
            finished_count = 0
            for item in items:
                if item.state == 'finished':
                    finished_count = finished_count + 1
            tmp_rst[key] = {
                "count": count,
                "finished": finished_count
            }

        rst = {}

        for key, item in tmp_rst.items():
            rst.setdefault("all", []).append(item["count"])
            rst.setdefault("finished", []).append(item["finished"])
            rst.setdefault("days", []).append(key)
        if rst.get('all'):
            rst['all_summary'] = sum(rst['all'])
            rst['finished_summary'] = sum(rst['finished'])
        else:
            rst['all'] = [0]
            rst['finished'] = [0]

        return rst

    @api.model
    def get_out_plan_info(self, start_date, end_date):
        '''
        取得发车计划数据
        :return:
        '''
        records = self.env["metro_park_dispatch.train_out_plan"] \
            .sudo().search([('date', '>=', start_date),
                            ('date', '<=', end_date)])

        date_cache = {}
        for record in records:
            date_cache.setdefault(str(record.date), []).append(record)

        tmp_rst = {}
        for key, items in date_cache.items():
            count = len(items)
            finished_count = 0
            for item in items:
                if item.state == 'finished':
                    finished_count = finished_count + 1
            tmp_rst[key] = {
                "all": count,
                "finished": finished_count
            }

        rst = {}
        for key, item in tmp_rst.items():
            rst.setdefault("all", []).append(item["all"])
            rst.setdefault("finished", []).append(item["finished"])
            rst.setdefault("days", []).append(key)
        if rst.get('all'):
            rst['all_summary'] = sum(rst['all'])
            rst['finished_summary'] = sum(rst['finished'])
        else:
            rst['all_summary'] = [0]
            rst['finished_summary'] = [0]

        return rst

    @api.model
    def get_back_plan_info(self, start_date, end_date):
        '''
        取得收车计划
        :return:
        '''
        records = self.env["metro_park_dispatch.train_back_plan"] \
            .sudo().search([('date', '>=', start_date),
                            ('date', '<=', end_date)])

        date_cache = {}
        for record in records:
            date_cache.setdefault(str(record.date), []).append(record)

        tmp_rst = {}
        for key, items in date_cache.items():
            count = len(items)
            finished_count = 0
            for item in items:
                if item.state == 'finished':
                    finished_count = finished_count + 1
            tmp_rst[key] = {
                "all": count,
                "finished": finished_count
            }

        rst = {}

        for key, item in tmp_rst.items():
            rst.setdefault("all", []).append(item["all"])
            rst.setdefault("finished", []).append(item["finished"])
            rst.setdefault("days", []).append(key)
        if rst.get('all'):
            rst['all_summary'] = sum(rst['all'])
            rst['finished_summary'] = sum(rst['finished'])
        else:
            rst['all'] = [0]
            rst['finished'] = [0]

        return rst

    @api.model
    def get_repair_plan_info(self, start_date, end_date):
        '''
        取得检修计划
        :return:
        '''
        records = self.env["metro_park_maintenance.rule_info"] \
            .sudo().search([('date', '>=', start_date),
                            ('date', '<=', end_date),
                            ('rule_type', '=', 'normal'),
                            ])

        date_cache = {}
        for record in records:
            date_cache.setdefault(str(record.date), []).append(record)

        tmp_rst = {}
        for key, items in date_cache.items():
            count = len(items)
            finished_count = 0
            for item in items:
                if item.state == 'finished':
                    finished_count = finished_count + 1
            tmp_rst[key] = {
                "all": count,
                "finished": finished_count
            }

        rst = {}
        for key, item in tmp_rst.items():
            rst.setdefault("all", []).append(item["all"])
            rst.setdefault("finished", []).append(item["finished"])
            rst.setdefault("days", []).append(key)
        if rst.get('all'):
            rst['all_summary'] = sum(rst['all'])
            rst['finished_summary'] = sum(rst['finished'])
        else:
            rst['all_summary'] = [0]
            rst['finished_summary'] = [0]

        return rst
