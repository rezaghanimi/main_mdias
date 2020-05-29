# -*- coding: utf-8 -*-

from collections import Counter
from random import random
import datetime
import time
from odoo import models, fields, api, exceptions


class ReportData(models.AbstractModel):
    """
    报表渲染所需数据
    """

    _name = 'metro_park_production.report_data'

    name = fields.Char()

    @api.model
    def static_report(self, period):
        """
        返回统计报表数据
        :param time: 时间段参数，列表形式，[0]是开始时间，[1]是结束时间
        :return:
        """
        vue_data = {}
        table1 = table2 = table3 = False
        if self.user_has_groups('metro_park_production.group_production_manage_statistical_form_car_service'):
            table1 = True
        if self.user_has_groups('metro_park_production.group_production_manage_statistical_form_construction_task'):
            table2 = True
        if self.user_has_groups('metro_park_production.group_production_manage_statistical_form_dispatch_plan'):
            table3 = True
        vue_data['table1'] = table1
        vue_data['table2'] = table2
        vue_data['table3'] = table3
        start_date = period[0].split('T')[0]
        end_date = period[1].split('T')[0]
        year, month, day = end_date.split('-')
        end_date = datetime.datetime(int(year), int(month), int(day)) + datetime.timedelta(days=1)
        vue_data = self.car_service_data(vue_data, start_date, end_date)
        vue_data = self.construction_task_data(vue_data, start_date, end_date)
        vue_data = self.scheduling_plan_data(vue_data, start_date, end_date)

        return vue_data

    @property
    def rule_obj(self):
        return self.env['metro_park_maintenance.rule_info']

    def car_service_data(self, vue_data, start_date, end_date):
        domain = [('date', '>=', start_date), ('date', '<', end_date), ('state', 'in', ['published', 'finished'])]

        # 获取日期内的规则信息
        rule_infos = self.rule_obj.search(domain)

        Chart1 = []
        chart4 = {}
        order_state = {'un_asign': '未指派', 'asigned': '已指派', 'accept': '已接报',
                       'started': '已开始', 'finished': '已完成', 'finish_accept': '已确认'}
        charts1 = {}
        Chart2 = {}

        for rule_info in rule_infos:
            # 计划状态统计-myChart4
            maintance_order = self.env['metro_park_maintenance.maintaince_order'].search(
                [('day_plan_info', '=', rule_info.id),
                 ('state', '!=', 'un_asign')])
            if maintance_order:
                work_class = maintance_order.work_department.name
                state = order_state[maintance_order.state]
                if work_class in chart4:
                    if state in chart4[work_class]:
                        chart4[work_class][state] += 1
                    else:
                        chart4[work_class][state] = 1
                else:
                    chart4[work_class] = {state: 1}

            if rule_info.rule:
                rule = rule_info.rule

                # 段内计划需求-myChart1
                for i in rule.work_requirement:
                    Chart1.append(i.name)

                # 修程统计-myCharts1
                work_class = rule.work_class
                if work_class:
                    for i in work_class:
                        if i.name in charts1:
                            if rule.name in charts1[i.name]:
                                charts1[i.name][rule.name] += 1
                            else:
                                charts1[i.name][rule.name] = 1
                        else:
                            charts1[i.name] = {rule.name: 1}

                # 修程均衡统计-myChart2
                if rule.name in Chart2:
                    Chart2[rule.name] += 1
                else:
                    Chart2[rule.name] = 1

        myChart1Data = []
        for key, value in dict(Counter(Chart1)).items():
            myChart1Data.append({key: value})
        vue_data['myChart1Data'] = myChart1Data

        # 计划状态统计-myChart4
        if chart4:
            vue_data['myChart4Data'] = chart4
        else:
            vue_data['myChart4Data'] = {'无计划': {'无计划': 0}}

        # 修程统计-myCharts1
        if charts1:
            vue_data['charts1Data'] = charts1
        else:
            vue_data['charts1Data'] = {'无计划': {'无计划': 0}}

        # 修程均衡统计-myChart2
        if Chart2:
            myChart2 = []
            for key, value in Chart2.items():
                myChart2.append({key: value})
            vue_data['myChart2Data'] = myChart2
        else:
            vue_data['myChart2Data'] = [{'无修程': 0}]

        return vue_data

    def construction_task_data(self, vue_data, start_date, end_date):
        domain = [('date', '>=', start_date), ('date', '<', end_date), ('state', 'in', ['published', 'finished'])]

        # 获取日期内的规则信息
        rule_infos = self.rule_obj.search(domain)

        Chart7 = []
        Chart11 = {}
        Chart10 = {}
        rule_state = {'published': '未完成', 'finished': '完成'}
        Chart6 = {}
        data_source = {'year': '年计划', 'month': '月计划', 'day': '日计划', 'user': '用户'}
        Chart9 = []
        Charts6 = {}
        Chart8 = {'value': [], 'maintance': []}

        for rule_info in rule_infos:
            # 作业区域分布图-myChart7
            if rule_info.rail:
                Chart7.append(rule_info.rail.alias)

            # 各部门计划完成情况-myChart11
            if rule_info.work_class:
                work_class = rule_info.work_class.name
                state = rule_state[rule_info.state]
                if work_class in Chart11:
                    if state in Chart11[work_class]:
                        Chart11[work_class][state] += 1
                    else:
                        Chart11[work_class][state] = 1
                else:
                    Chart11[work_class] = {state: 1}

                # 计划分布统计-Chart9
                Chart9.append(work_class)

                # 计划类型统计-Chart6
                if work_class in Chart6:
                    Chart6[work_class].append(data_source[rule_info.data_source])
                else:
                    Chart6[work_class] = [data_source[rule_info.data_source]]

            # 时间使用率-myChart10
            maintance_order = self.env['metro_park_maintenance.maintaince_order'].search(
                [('day_plan_info', '=', rule_info.id), ('state', '=', 'finished')])
            if maintance_order:
                name = maintance_order.work_department.name
                plan_time = maintance_order.plan_end_time - maintance_order.plan_start_time
                real_time = maintance_order.real_end_time - maintance_order.real_end_time
                if name in Chart10:
                    Chart10[name]['value'] += real_time / plan_time
                    Chart10[name]['len'] += 1
                else:
                    Chart10[name] = {'value': real_time / plan_time, 'len': 1, 'finished': 0}

                # 计划兑换率-myChart8
                if maintance_order.plan_end_time > maintance_order.real_end_time:
                    Chart10[name]['finished'] += 1

        # 计划类型统计（在施工任务统计中）
        dispatchs = self.env['metro_park_dispatch.construction_dispatch'].search([('plan_date', '>=', start_date),
                                                                                  ('plan_date', '<=', end_date)])
        for dispatch in dispatchs:
            if dispatch.department in Charts6:
                Charts6[dispatch.department.name].append(dispatch.work_category)
            else:
                Charts6[dispatch.department.name] = [dispatch.work_category]

        # 各部门计划数量-myChart7
        myChart7Data = []
        if Chart7:
            for key, value in dict(Counter(Chart7)).items():
                myChart7Data.append({'value': value, 'name': key})
            vue_data['myChart7Data'] = myChart7Data
        else:
            vue_data['myChart7Data'] = [{'value': 0, 'name': '无计划'}]

        # 各部门计划完成情况-myChart11
        if Chart11:
            vue_data['myChart11Data'] = Chart11
        else:
            vue_data['myChart11Data'] = {'无计划': {'完成': 0, '未完成': 0}}

        # 时间使用率-myChart10
        myChart10Data = []
        if Chart10:
            for i in Chart10:
                myChart10Data.append({'value': Chart10[i]['value'] / Chart10[i]['len'], 'name': i})
                # 计划兑换率-myChart8
                Chart8['value'].append(Chart10[i]['finished'] / Chart10[i]['len'])
                Chart8['maintance'].append({'name': i, 'max': 1})
            vue_data['myChart8Data'] = {}
            vue_data['myChart8Data']['value'] = Chart8['value']
            vue_data['myChart8Data']['maintance'] = Chart8['maintance']
            vue_data['myChart10Data'] = myChart10Data
        else:
            vue_data['myChart10Data'] = [{'value': 0, 'name': '无计划'}]
            vue_data['myChart8Data'] = {}
            vue_data['myChart8Data']['value'] = [0]
            vue_data['myChart8Data']['maintance'] = [{'name': '无计划', 'max': 1}]

        # 计划类型统计-Chart6
        if Chart6:
            for i in Chart6:
                Chart6[i] = dict(Counter(Chart6[i]))
            vue_data['myChart6Data'] = Chart6
        else:
            vue_data['myChart6Data'] = {'无计划': {'无计划': 0}}

        # 施工计划分布图
        myChart9Data = []
        if Chart9:
            for key, value in dict(Counter(Chart9)).items():
                myChart9Data.append({'value': value, 'name': key})
            vue_data['myChart9Data'] = myChart9Data
        else:
            vue_data['myChart9Data'] = [{'value': 0, 'name': '无计划'}]

        # 计划类型统计
        if Charts6:
            for i in Charts6:
                Charts6[i] = dict(Counter(Charts6[i]))
            vue_data['myCharts6Data'] = Charts6
        else:
            vue_data['myCharts6Data'] = {'无计划': {'无计划': 0}}

        return vue_data

    def scheduling_plan_data(self, vue_data, start_date, end_date):
        car_domain = [('state', 'in', ['preparing', 'wait_accept', 'excuting', 'finished'])]
        di_domain = [('state', 'in', ['accepted', 'wait_excuting', 'excuting', 'finished'])]
        di_time_domain = [('dispatch_date', '>=', start_date), ('dispatch_date', '<', end_date)]
        route_domain = [('end_time', '>=', start_date), ('start_time', '<', end_date)]
        domain = [('date', '>=', start_date), ('date', '<', end_date), ('state', 'in', ['published', 'finished'])]

        # 接车、发车
        receive_car = len(self.rule_obj.search(domain + [('rule_type', '=', 'recieve_train')]))
        send_car = len(self.rule_obj.search(domain + [('rule_type', '=', 'send_train')]))
        # 调车辆数
        dispatchs = self.env['metro_park_dispatch.dispatch_request'].search(di_domain + di_time_domain)
        dispatch_num = len(dispatchs)
        # 调车钩数
        route_detail = self.env['metro_park_dispatch.dispatch_route_detail'].search(route_domain)
        route_num = len(route_detail)
        vue_data['myChartData'] = [receive_car, send_car, dispatch_num, route_num]

        # 完成率饼图-Chart12
        vue_data['quota'] = {}

        # 收车完成率
        receive_finished = len(self.rule_obj.search(domain + [('rule_type', '=', 'recieve_train'),
                                                              ('state', '=', 'finished')]))
        receive_published = len(self.rule_obj.search(domain + [('rule_type', '=', 'recieve_train'),
                                                               ('state', '=', 'published')]))
        vue_data['quota']['receive'] = [receive_finished, receive_published]

        # 发车完成率
        send_finished = len(self.rule_obj.search(domain + [('rule_type', '=', 'send_train'),
                                                           ('state', '=', 'finished')]))
        send_published = len(self.rule_obj.search(domain + [('rule_type', '=', 'send_train'),
                                                            ('state', '=', 'published')]))
        vue_data['quota']['send'] = [send_finished, send_published]

        # 调车完成率
        dispatch_fi = self.env['metro_park_dispatch.dispatch_request'].search(di_time_domain + [('state', '=', 'finished')])
        dispatch_finish_num = len(dispatch_fi)
        vue_data['quota']['dispatch'] = [dispatch_finish_num, dispatch_num - dispatch_finish_num]

        # 收发车趋势图
        year1, month1, day1 = start_date.split("-")
        start_time = datetime.datetime(int(year1), int(month1), int(day1))
        vue_data['car_trend'] = {'date': [], 'receive': [], 'send': [], 'route': []}

        # 发车
        send_cars = self.env['metro_park_dispatch.train_out_plan']\
            .search([('date', '>', start_date), ('date', '<', end_date)] + car_domain)
        send_list = []
        for i in send_cars:
            send_list.append(i.plan_out_time.strftime("%m-%d %H:%M"))
        send_dict = dict(Counter(send_list))

        # 收车
        receive_cars = self.env['metro_park_dispatch.train_back_plan']\
            .search([('date', '>', start_date), ('date', '<', end_date)] + car_domain)
        receive_list = []
        for i in receive_cars:
            receive_list.append(i.plan_back_time.strftime("%m-%d %H:%M"))
        receive_dict = dict(Counter(receive_list))

        now = start_time
        while now < end_date:
            x = now.strftime("%m-%d %H:%M")
            vue_data['car_trend']['date'].append(x)
            if x in send_dict:
                vue_data['car_trend']['send'].append(send_dict[x])
            else:
                vue_data['car_trend']['send'].append(0)
            if x in receive_dict:
                vue_data['car_trend']['receive'].append(receive_dict[x])
            else:
                vue_data['car_trend']['receive'].append(0)
            now += datetime.timedelta(minutes=1)
            count = 0
            for i in route_detail:
                if i.start_time < now < i.end_time:
                    count += 1
            vue_data['car_trend']['route'].append(count)
        return vue_data
