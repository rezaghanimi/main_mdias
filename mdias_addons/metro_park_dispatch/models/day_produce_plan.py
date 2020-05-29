
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DayProducePlan(models.Model):
    '''
    车间日生产计划
    '''
    _name = 'metro_park_dispatch.day_produce_plan'
    _description = '车间日生产计划'
    _track_log = True
    
    train = fields.Many2one(string='车辆', comodel_name='metro_park_dispatch.cur_train')
    work_start_tm = fields.Datetime(string='开始时间')
    work_end_tm = fields.Datetime(string='作业结束时间')
    work_content = fields.Char(string='作业内容')

    # 检修会不会占用多根轨道呢，如果是的话那么就添个表来存信息
    rail = fields.Many2one(string='作业地点', comodel_name='metro_park_base.rails_sec')

    work_requirement = fields.Many2one(string='作业要求', comodel_name="metro_park_base.rail_type")
    location = fields.Many2one(string='位置', comodel_name='metro_park_base.location')
    work_class = fields.Many2one(string='作业工班', comodel_name='funenc.wechat.department')

    rule_type = fields.Selection(string="规程类型", selection=[('normal', '修程'), ('temp', '检技通')], default="normal")
    rule_id = fields.Many2one(string="规程", comodel_name="metro_park_maintenance.repair_rule")
    temp_rule_id = fields.Many2one(string="检技通", comodel_name="metro_park_maintenance.repair_tmp_rule")

    train_status = fields.Selection(string='车辆状态', selection=[('normal', '正常'), ('backup', '库备')])
    back_location = fields.Many2one(string='夜回库状态', comodel_name='metro_park_base.location')
    next_day_work = fields.Char(string='次日作业')
    work_remark = fields.Text(string='作业备注')
    remark = fields.Text(string='备注')
