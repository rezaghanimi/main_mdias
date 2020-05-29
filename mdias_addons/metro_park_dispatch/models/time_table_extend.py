
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum


class TimeTableExtend(models.Model):
    '''
    时刻表扩展
    '''
    _inherit = "metro_park_base.time_table"
    _description = '时刻表扩展'
    
    @api.multi
    def change_status(self):
        '''
        更改状态
        :return:
        '''
        self.ensure_one()
        if self.state == "active":
            self.state = 'disabled'
            # 移除掉基础配置中的时刻表
            records = self.env['metro_park_dispatch.nor_time_table_config']\
                .search([('time_table', '=', self.id)])
            for record in records:
                record.time_table = False
        else:
            self.state = "active"



