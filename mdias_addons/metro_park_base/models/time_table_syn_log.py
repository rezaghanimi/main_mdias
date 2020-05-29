
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class TimeTableSynLog(models.Model):
    '''
    运行图同步日志
    '''
    _name = 'metro_park_base.time_table_syn_log'
    _description = '运行图(时刻表)同步记录'
    _track_log = True
    
    time_table = fields.Many2one(string='时刻表',
                                 comodel_name='metro_park_base.time_table')
    no = fields.Char(string='编号')
    time = fields.Datetime(string='时间', default=lambda x: pendulum.now('UTC')
                           .format('YYYY-MM-DD HH:mm:ss'))
    date = fields.Date(string="日期", compute="_compute_date", store=True)
    syn_type = fields.Selection(string='同步方式',
                                selection=[('auto', '自动'), ('manual', '手动')],
                                default="manual")
    syn_status = fields.Selection(string='状态',
                                  selection=[('success', '成功'),
                                             ('unknown', '未知'),
                                             ('fail', '失败')],
                                  default="unknown")
    user = fields.Many2one(string='用户',
                           comodel_name='res.users')
    content = fields.Text(string="内容")
    ip_address = fields.Char(string='ip地址')
    button = fields.Char(string="按扭", help="用于占位")

    @api.model
    def add_log(self, data):
        return self.create([{
            "no": self.env['ir.sequence'].next_by_code('timetable.log'),
            "content": data['content'],
            "user": self.env.user.id,
            "syn_type": data.get('syn_type', False),
            "syn_status": data.get('syn_status', 'unknown'),
            "time_table": data.get('time_table', False)
        }])

    @api.model
    def download_attachment(self):
        '''
        下载附件
        '''
        return {
            'name': '下载附件',
            'type': 'ir.action.act_url',
            'url':  '/dispatch/download_attachment'
        }

    @api.depends("time")
    def _compute_date(self):
        '''
        计算日期
        :return:
        '''
        for record in self:
            date_obj = pendulum.parse(str(record.time)).add(hours=8)
            record.date = date_obj.format('YYYY-MM-DD')
