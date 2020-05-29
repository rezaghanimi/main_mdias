
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectType(models.Model):
    '''
    项目类型
    '''
    _name = 'project_manage.project_type'
    
    name = fields.Char(string='名称')

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "项目名称不能重复")]

