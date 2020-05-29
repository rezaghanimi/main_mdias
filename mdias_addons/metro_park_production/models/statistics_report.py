# -*- coding: utf-8 -*-

import random

import pendulum

from odoo import models, fields, api

WEEKS = {
    0: '一',
    1: '二',
    2: '三',
    3: '四',
    4: '五',
    5: '六',
    6: '日'
}


class StatisticsReport(models.Model):
    '''
    统计报表
    '''
    _name = 'metro_park_production.statistics_report'

    name = fields.Char()
    begin_time = fields.Date(string="开始时间", required=True)
    end_time = fields.Date(string="结束时间", required=True)

    dispatch_cmd_statistics_time_interval = fields.Integer(string='调车勾计划数量统计间隔', default=60)

    @property
    def statistics_query_datetime(self):
        """
            数据查询时间范围
        :return:
        """
        now = pendulum.now()
        end_time = pendulum.datetime(year=now.year, month=now.month, day=now.day, hour=20).subtract(days=1)
        start_time = end_time.subtract(days=7)
        return [start_time, end_time]

    @api.model
    def request_dispatch_cmds(self):
        start_time, end_time = self.statistics_query_datetime
        obj = self.env['metro_park_dispatch.dispatch_request']
        data = []
        xtime = []
        tmp_time = start_time
        while start_time < end_time:
            start_time = tmp_time.add(days=1)
            xtime.append('周%s' % WEEKS[start_time.add(hours=8).weekday()])
            data.append(obj.search_count([('state', '=', 'finished'),
                                          ('start_time', '>=', tmp_time), ('start_time', '<=', start_time)]))
            tmp_time = start_time
        return {
            'data': data,
            'xtime': xtime
        }

    @api.model
    def dispatch_train_production_indicator(self):
        start_time, end_time = self.statistics_query_datetime
        start_time = start_time.format('YYYY-MM-DD hh:mm:ss')
        end_time = end_time.format('YYYY-MM-DD hh:mm:ss')
        cr = self._cr
        # 调车计划完成率计算
        sql_query = """
            SELECT COUNT(*) FROM metro_park_dispatch_dispatch_request 
                WHERE start_time >= %(start_time)s 
                     AND   start_time <= %(end_time)s
        """
        cr.execute(sql_query, dict(start_time=start_time, end_time=end_time))
        sum_dispatch_num = cr.fetchone()[0]
        dispatch_percent = 0.00
        if sum_dispatch_num:
            cr.execute(sql_query + "AND state='finished'", dict(start_time=start_time, end_time=end_time))
            finished_dispatch_num = cr.fetchone()[0]
            dispatch_percent = finished_dispatch_num / sum_dispatch_num
        # 收车计划完成率计算
        sql_query = """
                   SELECT COUNT(*) FROM metro_park_dispatch_train_back_plan 
                       WHERE  date >= %(start_time)s 
                            AND   date <= %(end_time)s
               """
        cr.execute(sql_query, dict(start_time=start_time, end_time=end_time))
        sum_train_back_num = cr.fetchone()[0]
        train_back_percent = 0.00
        if sum_train_back_num:
            cr.execute(sql_query + "AND state='finished'", dict(start_time=start_time, end_time=end_time))
            sum_train_back_finished_num = cr.fetchone()[0]
            train_back_percent = sum_train_back_finished_num / sum_train_back_num
        # 发车计划完成率计算
        sql_query = """
                           SELECT COUNT(*) FROM metro_park_dispatch_train_out_plan 
                               WHERE  date >= %(start_time)s 
                                    AND   date <= %(end_time)s
                       """
        cr.execute(sql_query, dict(start_time=start_time, end_time=end_time))
        sum_train_out_num = cr.fetchone()[0]
        train_out_percent = 0.00
        if sum_train_out_num:
            cr.execute(sql_query + "AND state='finished'", dict(start_time=start_time, end_time=end_time))
            sum_train_out_finished_num = cr.fetchone()[0]
            train_out_percent = sum_train_out_finished_num / sum_train_out_num
        return {
            'dispatch_percent': dispatch_percent,
            'train_back_percent': train_back_percent,
            'train_out_percent': train_out_percent
        }

    @api.model
    def construction_department_finished_and_unfinished(self):
        start_time, end_time = self.statistics_query_datetime
        sql_query = """
            SELECT DISTINCT  out_work_department, COUNT(*) OVER (PARTITION BY out_work_department) 
                FROM metro_park_dispatch_construction_plan
                    WHERE out_work_start_time >= %(start_time)s AND out_work_start_time <= %(end_time)s
        """
        self._cr.execute(sql_query + "AND out_state !='Finished' ORDER BY out_work_department",
                         dict(start_time=start_time, end_time=end_time))
        unfinished_result = self._cr.fetchall()
        unfinished_data = []

        department_data = []
        for val in unfinished_result:
            unfinished_data.append(val[1])
        self._cr.execute(sql_query + "AND out_state ='Finished' ORDER BY out_work_department",
                         dict(start_time=start_time, end_time=end_time))
        finished_result = self._cr.fetchall()
        finished_data = []
        for val in finished_result:
            department_data.append(val[0])
            finished_data.append(val[1])
        return {
            'finished_data': finished_data,
            'department_data': department_data,
            'unfinished_data': unfinished_data
        }

    CONSTRUCTION_PLAN_TYPES = [('Monthly', '月计划'), ('Weekly', '周计划'), ('Supplementary', '日补充计划'),
                               ('Temporary', '临时补充计划')]

    @api.model
    def construction_plan_type_num(self):
        start_time, end_time = self.statistics_query_datetime
        sql_query = """
                    SELECT DISTINCT  out_work_department, out_plan_type, COUNT(*) 
                    OVER (PARTITION BY out_work_department, out_plan_type) 
                        FROM metro_park_dispatch_construction_plan
                            WHERE out_work_start_time >= %(start_time)s AND out_work_start_time <= %(end_time)s
                             AND out_state ='Finished' ORDER BY out_work_department
                """
        query_departments = """
                SELECT DISTINCT out_work_department FROM metro_park_dispatch_construction_plan WHERE 
                out_work_start_time >= %(start_time)s AND out_work_start_time <= %(end_time)s
                             AND out_state ='Finished' ORDER BY out_work_department
        """
        department_names = []
        self._cr.execute(query_departments, dict(start_time=start_time, end_time=end_time))
        dep_result = self._cr.fetchall()
        for val in dep_result:
            department_names.append(val[0])
        self._cr.execute(sql_query, dict(start_time=start_time, end_time=end_time))
        result = self._cr.fetchall()
        types = ['Monthly', 'Weekly', 'Supplementary', 'Temporary']
        monthly_data = []
        weekly_data = []
        day_data = []
        temp_data = []
        for name in department_names:
            monthly_data.append(0)
            weekly_data.append(0)
            day_data.append(0)
            temp_data.append(0)
            for ty in types:
                for val in result:
                    if val[0] == name and val[1] == ty:
                        if val[1] == 'Monthly':
                            monthly_data[-1] = val[2]
                        elif val[1] == 'Weekly':
                            weekly_data[-1] = val[2]
                        elif val[1] == 'Supplementary':
                            day_data[-1] = val[2]
                        elif val[1] == 'Temporary':
                            temp_data[-1] = val[2]
                        continue
        return {
            'monthly_data': monthly_data,
            'temp_data': temp_data,
            'weekly_data': weekly_data,
            'day_data': day_data,
            'department_names': department_names
        }

    @api.model
    def construction_area_top(self):
        start_time, end_time = self.statistics_query_datetime
        query_sql = """
            WITH area_number AS (
                SELECT DISTINCT area_id, count(*) OVER (PARTITION BY area_id) as num 
                FROM construction_work_area_ref WHERE  plan_id IN ( SELECT id FROM metro_park_dispatch_construction_plan 
                WHERE out_work_start_time >= %(start_time)s AND out_work_start_time <= %(end_time)s AND out_state ='Finished') 
                ORDER BY num DESC LIMIT 10)
            SELECT l.area_id, r.park_element_code, element_type , l.num 
            FROM area_number AS l JOIN
             metro_park_dispatch_construction_area_relation r ON (r.id = l.area_id)           
        """
        self._cr.execute(query_sql, dict(start_time=start_time, end_time=end_time))
        result = self._cr.fetchall()
        xaixs = []
        data = []
        for val in result:
            element_type = val[2]
            if element_type == 'rail':
                name = val[1] + '区段'
            else:
                name = val[1] + '道岔'
            xaixs.append(name)
            data.append(val[3])
        return {
            'xaixs': xaixs,
            'data': data
        }

    @api.model
    def train_run_number(self):
        start_time, end_time = self.statistics_query_datetime
        query_sql = """
                    WITH train_run_num AS (
                        SELECT DISTINCT train_id , count(*) OVER (PARTITION BY train_id) AS num FROM metro_park_dispatch_train_out_plan WHERE 
                                date >= %(start_time)s  AND date <= %(end_time)s AND state = 'finished'
                                ORDER BY train_id
                        )
                        SELECT l.num, t.dev_name  FROM  metro_park_maintenance_train_dev t 
                            INNER JOIN metro_park_dispatch_cur_train_manage r  ON(t.id = r.train)
                            LEFT JOIN train_run_num l ON(l.train_id = r.id) 
                """
        self._cr.execute(query_sql, dict(start_time=start_time, end_time=end_time))
        result = self._cr.fetchall()
        xaixs = []
        data = []
        for val in result:
            xaixs.append(val[1])
            data.append(val[0] or 0)
        return {
            'xaixs': xaixs,
            'data': data
        }

    @api.model
    def train_use_condition(self):
        query_sql = """
            SELECT train_status, detain, train 
                    FROM metro_park_dispatch_cur_train_manage
        """
        self._cr.execute(query_sql)
        result = self._cr.fetchall()
        detain_data_ids = []
        repair_data_ids = []
        fault_data_ids = []
        other_ids = []
        for val in result:
            if val[0] == 'detain' or val[0] == 'fault':
                fault_data_ids.append(val[2])
            elif val[0] == 'repair':
                repair_data_ids.append(val[2])
            else:
                other_ids.append(val[2])
        return {
            'data': [{
                'value': len(fault_data_ids), 'name': '故障'
            }, {
                'value': len(other_ids), 'name': '用车'
            }, {
                'value': len(repair_data_ids), 'name': '检修'
            }]
        }

    @api.multi
    def jump_static_action(self):
        '''
        跳转到页面
        :return:
        '''
        url = '/web?begin_time={begin_time}&end_time={end_time}&config_id{config_id}#action=report_client' \
            .format(begin_time=self.begin_time, end_time=self.end_time, config_id=self.id)
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    def echart_report(self):
        data = {}

        # 收发车趋势
        series_14 = [
            {
                'name': '收车量',
                'label': {
                    'show': True,
                    'position': 'top'
                },
                'data': [12, 20, 15, 28, 21, 11, 13],
                'type': 'line'
            },
            {
                'name': '发车量',
                'label': {
                    'show': True,
                    'position': 'top'
                },
                'data': [13, 10, 25, 20, 19, 15, 23],
                'type': 'line'
            }
        ]
        # 吊车钩计划数量分布
        data_13 = [12, 20, 15, 28, 17, 11, 13]
        # 生产指标
        data_12 = {}
        data_12['value1_on'] = 60
        data_12['value2_on'] = 40
        data_12['value3_on'] = 70
        data_12['value1_off'] = 40
        data_12['value2_off'] = 60
        data_12['value3_off'] = 30
        # 施工计划完成情况
        department_data = ['运营二分公司机电四车间', '维保分公司信号三车间', '运营二分公司车辆检修四车间', '维保分公司接触网一车间',
                           '运营三分公司18号线运营中心', '运营二分公司车辆设备车间', '维保分公司工务一车间']
        data_11 = {}
        data_11['data_done'] = [[10, 0],
                                [20, 1],
                                [30, 2],
                                [230, 3],
                                [200, 4],
                                [5, 5],
                                [12, 6],
                                [10, 7],
                                ]
        data_11['data'] = [
            [100, 0],
            [270, 1],
            [60, 2],
            [30, 3],
            [130, 4],
            [10, 5],
            [30, 6],
            [5, 7], ]
        # 施工计划时间使用率
        data_10 = [120, 200, 150, 80, 70, 110, 130, 50]

        # 施工计划分布图
        data_9 = {}
        data_9.update(value1=100)
        data_9.update(value2=60)
        data_9.update(value3=50)
        data_9.update(value4=40)
        data_9.update(value5=30)
        data_9.update(value6=20)
        data_9.update(value7=10)
        data_9.update(value8=10)

        # 施工计划兑现率
        data_8 = {}
        indicator = []
        for i in department_data:
            val = {
                'name': i,
                'max': 1000
            }
            indicator.append(val)
        data_8['indicator'] = indicator
        data_8['value1'] = [300, 900, 280, 250, 400, 900, 600, 700]
        data_8['value2'] = [800, 200, 680, 850, 920, 400, 900, 100]
        data_8['value3'] = [400, 900, 600, 700, 450, 680, 839, 693, 690]
        # 作业区域分布
        data_7 = [120, 200, 150, 80, 70, 110, 130, 120, 200, ]
        # 各部门施工计划数量
        series_6 = {}
        series_6['data1'] = [[0, 210], [1, 100], [2, 190], [3, 177], [4, 220], [5, 30], [6, 100], [7, 50]]
        series_6['data2'] = [[0, 150], [1, 160], [2, 200], [3, 210], [4, 30], [5, 60], [6, 10], [7, 150]]
        series_6['data3'] = [[0, 170], [1, 280], [2, 100], [3, 190], [4, 130], [5, 40], [6, 80], [7, 90]]
        # 施工计划统计
        series_5 = {}
        series_5['data1'] = [[0, 230], [1, 180], [2, 90], ]
        series_5['data2'] = [[0, 180], [1, 130], [2, 150], ]
        series_5['data3'] = [[0, 123], [1, 200], [2, 210], ]

        #####################################检修统计start
        repair_process = ['月修1', '月修2', '月修3', '月修4A', '月修4B', '月修5A', '月修5B', '月修6', '月修7',
                          '月修8', '月修9', '月修10', '月修11A', '月修11B', '月修12']

        repair_team = ['均衡修1班', '均衡修2班', '均衡修3班', '均衡修4班', '均衡修5班', '均衡修6班', '列检1班', '列检2班', '列检3班', '列检4班',
                       '综合1班', '综合2班', '综合3班', '综合4班',
                       ]
        balanced_repair = [
            '里程检',
            '半年保洁',
            '空调专检',
            '专项修N1',
            '专项修N2',
            '接车',
            '洗车',
            '车内保洁'
        ]

        # 班组执行修程统计
        data_3 = {}
        series_3 = []
        for i in repair_process:
            data_unit = []
            for j in range(len(repair_team)):
                unit = [j, random.randint(0, 99)]
                data_unit.append(unit)
            val = {
                'name': i,
                'type': 'bar',
                'barCategoryGap': '70%',
                'stack': '总量',
                'label': {
                    'normal': {
                        'show': True,
                        'position': 'inside'
                    }
                },
                'data': data_unit
            }
            series_3.append(val)
            data_3['series'] = series_3

        # 均衡修
        data_2 = {}
        repair_indicator = []
        for i in balanced_repair:
            val = {
                'name': i,
                'max': 100,
            }
            repair_indicator.append(val)
        data_2['indicator'] = repair_indicator
        data_2['data'] = [43, 10, 28, 35, 50, 19, 30, 41, ]
        # 作业区段
        data_1 = [120, 80, 110, ]
        data['department_data'] = department_data
        data['series_14'] = series_14
        data['data_13'] = data_13
        data['data_12'] = data_12
        data['data_11'] = data_11
        data['data_10'] = data_10
        data['data_9'] = data_9
        data['data_8'] = data_8
        data['data_7'] = data_7
        data['series_6'] = series_6
        data['series_5'] = series_5

        data['balanced_repair'] = balanced_repair
        data['repair_process'] = repair_process
        data['repair_team'] = repair_team
        data['data_3'] = data_3
        data['data_2'] = data_2
        data['data_1'] = data_1

        return data

    @api.model
    def class_task_perform_state(self):
        start_time, end_time = self.statistics_query_datetime
        start_time = start_time.format('YYYY-MM-DD hh:mm:ss')
        end_time = end_time.format('YYYY-MM-DD hh:mm:ss')
        cr = self._cr
        sql = '''
        select count(a.id),b.work_class_id 
        from (select id ,date from metro_park_maintenance_rule_info where "date" >  '{}'   and "data_source" = 'day' ) a
            left join plan_data_rule_info_work_class_rel b on a.id = b.work_class_id 
            where b.work_class_id is not null group by work_class_id'''.format(
            str(start_time)[:10])
        # sql = '''
        #  SELECT count(id), pms_work_class FROM metro_park_maintenance_rule_info where "date" > '{}'
        #  and "data_source" = 'day' and pms_work_class is not null group by "pms_work_class"
        # '''.format(str(start_time)[:10])
        cr.execute(sql)
        data = cr.fetchall()
        data_key = []
        data_value = []

        def calculate_data(x):
            department = self.env['pms.department'].search([('id', '=', x[1])]).department
            data_key.append(x[0])
            data_value.append(department)
            return data_key, data_value

        rec_data = list(map(calculate_data, data))
        if rec_data:
            return rec_data
        else:
            return [[0], ['无']]

    @api.model
    def phase_work_demand(self):
        start_time, end_time = self.statistics_query_datetime
        start_time = start_time.format('YYYY-MM-DD hh:mm:ss')
        end_time = end_time.format('YYYY-MM-DD hh:mm:ss')
        cr = self._cr
        sql = '''
        SELECT b.* from (
        SELECT a.repair_days,a.name,a.id,(SELECT count(1) FROM metro_park_maintenance_rule_info 
        where rule_name= a.name and "date" >= '{}' and "date" <= '{}'
        ) as count_name FROM metro_park_maintenance_repair_rule as a 
        ) as b 
        where b.count_name >0;'''.format(str(start_time)[:10], str(end_time)[:10])
        cr.execute(sql)
        datas = cr.fetchall()
        all_name_data = []
        all_key_data = []
        for data in datas:
            recs = self.env['metro_park_maintenance.repair_rule'].search([('id', '=', data[2])])
            for rec in recs.work_requirement:
                if rec.name not in all_name_data:
                    all_name_data.append(rec.name)
                    all_key_data.append(data[3])

                else:
                    for key, name in enumerate(all_name_data):
                        if name == rec.name:
                            all_key_data[key] += data[3]

        rec_data = [all_key_data, all_name_data]
        if rec_data:
            return rec_data
        else:
            return [0, '无']

    @api.model
    def repair_schedule_equilibrium_statistics(self):
        start_time, end_time = self.statistics_query_datetime
        start_time = start_time.format('YYYY-MM-DD hh:mm:ss')
        end_time = end_time.format('YYYY-MM-DD hh:mm:ss')
        cr = self._cr
        sql = '''
         SELECT count(id), rule_name FROM metro_park_maintenance_rule_info where "date" > '{}' and "date" < '{}'
         group by "rule_name"
        '''.format(str(start_time)[:10], str(end_time)[:10])
        cr.execute(sql)
        data = cr.fetchall()
        data_key = []
        data_value = []

        def calculate_data(x):
            data_key.append(x[1])
            data_value.append(x[0])
            return data_key, data_value

        rec_data = list(map(calculate_data, data))
        if rec_data:
            return rec_data
        else:
            return [['无'], [{'name': '无', 'value': 0}]]
