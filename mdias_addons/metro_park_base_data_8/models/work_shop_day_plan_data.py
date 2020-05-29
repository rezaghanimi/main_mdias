
# -*- coding: utf-8 -*-

from odoo import models, fields, api

CUR_TRAIN_STATUS = [('fault', '故障'),
                    ('repair', '检修'),
                    ('detain', '扣车'),
                    ('wait', '待命')]


class WorkShopDayPlan(models.Model):
    '''
    车间日生产计划
    '''
    _inherit = 'metro_park_dispatch.work_shop_day_plan_data'

    @api.multi
    def get_next_run_task(self):
        '''
        当前是一个收车任务，但后面还有运行， 高峰车的情况, 这个也是判断高峰车的标准 train_no
        :return:
        '''
        date_str = str(self.plan_date)
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id
        # 同一车跑了两个任务, 那么第一个不用考虑
        # 第二天的检修任务，但轨道要对应上
        records = self.search([('rule', '=', main_line_rule_id),
                               ('dev', '=', self.dev.id),
                               ('plan_date', '=', date_str),
                               ('work_start_tm', '>', self.work_end_tm)],
                              order="work_start_tm asc")
        return records[0] if records else None

    @api.multi
    def get_prev_run_task(self):
        '''
        取得之前的任务
        :return:
        '''
        date_str = str(self.plan_date)
        main_line_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_run_rule').id
        # 同一车跑了两个任务, 那么第一个不用考虑, 但第二个要考虑要发得出去, 不要被其它车给挡了
        records = self.search([('rule', '=', main_line_rule_id),
                               ('dev', '=', self.dev.id),
                               ('plan_date', '=', date_str),
                               ('work_end_tm', '<', self.work_start_tm)],
                              order="work_start_tm asc")
        return records[0] if records else None

    @api.multi
    def get_tasks_after_run(self):
        '''
        取处运营任务之后的检修任务，
        一般是找到这些任务后查看作业要求,
        如果是有多个的话可能还要调到多处去才行
        :return:
        '''
        self.ensure_one()

        main_line_rule_id = \
            self.env.ref('metro_park_base_data_8.main_line_run_rule').id

        run_task = self.get_next_run_task()
        if not run_task:
            # 后边没有运营任务就取当天所有的
            tasks = self.search(
                [('plan_date', '=', str(self.plan_date)),
                 ('dev', '=', self.dev.id),
                 ('work_start_tm', '>=', str(self.work_end_tm)),
                 ('rule', 'not in', [main_line_rule_id])],
                order="work_start_tm asc")
        else:
            # 后边有运营任务就取到下一个运营任务的
            tasks = self.search(
                [('plan_date', '=', str(self.plan_date)),
                 ('dev', '=', self.dev.id),
                 ('work_start_time', '>=', str(self.work_end_tm)),
                 ('work_end_time', "<=", str(run_task.work_end_tm)),
                 ('rule', 'not in', [main_line_rule_id])],
                order="work_start_tm asc")

        return tasks
