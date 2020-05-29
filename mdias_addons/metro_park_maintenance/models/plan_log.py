
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class PlanLog(models.Model):
    '''
    检修计划日志
    '''
    _name = 'metro_park_maintenance.plan_log'

    sequence = fields.Char(string="检作序号")
    content = fields.Text(string='内容')
    plan_time = fields.Datetime(string='时间')

    @api.model
    def add_plan_log(self, log):
        '''
        添加检修日志
        :return:
        '''
        self.create([{
            "sequence": self.env['ir.sequence'].next_by_code('plan.order.number'),
            "content": log,
            "plan_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss')
        }])

