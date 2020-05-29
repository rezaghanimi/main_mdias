
# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api


class ReportContent(models.Model):
    '''
    汇报内容
    '''
    _name = 'project_manage.report_content'

    report_time = fields.Datetime(string='汇报时间', default=lambda self: datetime.now())
    content = fields.Html(string='内容')
    send_to_master = fields.Boolean(string='推送给领导')
    project_id = fields.Many2one(string="项目",
                                 comodel_name="project_manage.project_manage")
