
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class ProjectManage(models.Model):
    '''
    项目信息
    '''
    _name = 'project_manage.project_manage'
    
    name = fields.Char(string='名称')
    plan_start_date = fields.Date(string='开始日期')
    plan_end_date = fields.Date(string="结束日期")
    project_info = fields.Text(string='项目描述')
    responsible = fields.Char(string='责任人')
    cur_progress = fields.Float(string='当前进度(百分比)')
    finish_date = fields.Date(string='计划完成日期')
    report_content = fields.One2many(string='汇报内容',
                                     comodel_name='project_manage.report_content',
                                     inverse_name='project_id')
    project_type = fields.Many2one(string='项目类型',
                                   comodel_name='project_manage.project_type')
    state = fields.Selection(selection=[('draft', '草稿'),
                                        ('rejected', '已拒绝'),
                                        ('passed', '已通过')], string="状态", default='draft')
    button = fields.Boolean(string="操作")

    @api.multi
    def pass_project(self):
        '''
        通过
        :return:
        '''
        self.state = 'passed'

    @api.multi
    def reject_project(self):
        '''
        通过
        :return:
        '''
        self.state = 'rejected'

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        '''
        重写，添加判断
        :param vals_list:
        :return:
        '''
        for val in vals_list:
            if val['plan_start_date'] > val['plan_end_date']:
                raise exceptions.ValidationError('项目开始时间不能大于结束时间')
        return super(ProjectManage, self).create(vals_list)

