
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WeekWorkClassInfo(models.Model):
    '''
    周计划工班信息，主要用于里程
    '''
    _name = 'metro_park_maintenance.week_work_class_info'
    
    date = fields.Date(string='日期')
    work_class_name = fields.Char(string='工班名称', help="里程修工班名称, 暂时没有去和工班做关联")
    work_class = fields.Many2many(string='工班',
                                  comodel_name='funenc.wechat.department',
                                  relation='week_plan_work_class_rel',
                                  col1='week_plan_id',
                                  col2='class_id')
    week_plan_id = fields.Many2one(string='周计划',
                                   comodel_name='metro_park_maintenance.week_plan',
                                   ondelete='cascade')
    remark = fields.Text(string="备注文字")
