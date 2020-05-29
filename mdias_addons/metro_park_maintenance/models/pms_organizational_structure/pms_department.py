# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class PmsDepartment(models.Model):
    '''
    pms部门管理
    '''
    _name = 'pms.department'
    _rec_name = 'department'
    _description = 'pms的组织架构'

    department = fields.Char('部门')
    department_no = fields.Char('部门编码')
    line_no = fields.Char('线路')
    parent_department = fields.Char('父部门')
    parent_department_no = fields.Char('父部门编码')


