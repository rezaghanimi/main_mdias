
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ConstructionDispatch(models.Model):
    '''
    同步施工调度信息
    '''
    _name = 'metro_park_dispatch.construction_dispatch'
    _description = '施工调度数据'
    _track_log = True
    
    line_id = fields.Many2one(string='线路',
                              comodel_name='metro_park_base.line')
    work_category = fields.Many2one(string="作业类别")
    plan_date = fields.Date(string='作业日期')
    work_code = fields.Char(string='作业代码')
    department = fields.Many2one(string='作业部门',
                                 comodel_name='funenc.wechat.department')
    area = fields.Text(string='作业区域')
    work_content = fields.Text(string='作业内容')
    influence_area = fields.Text(string='作业范围')
    electric_info = fields.Text(string='接触网供电')
    principal = fields.Many2one(string='负责人',
                                comodel_name='funenc.wechat.user')
    work_time_start = fields.Datetime(string='作业开始时间')
    work_time_end = fields.Datetime(string='作业结束时间')
    request_addr = fields.Char(string='请点地址')
    backout_addr = fields.Char(string='销点地址')
    assist_station_info = fields.Char(string='辅站信息')
    request_time = fields.Datetime(string='请点时间')
    backout_time = fields.Datetime(string='销点时间')
    recognize_num = fields.Char(string='施工承认号')
    status = fields.Char(string='作业状态')
    remarks = fields.Text(string='备注信息')

    @api.model
    def manual_sync(self):
        '''
        同步施工调度信息
        :return:
        '''
        self.env["metro_park_dispatch.msg_client"]\
            .send_broadcast_msg("mdias_msg", {"msg_type": 'test'})
