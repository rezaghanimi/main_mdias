
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SpecialDaysConfig(models.Model):
    '''
    特殊日期配置, 特殊日期使用哪个运行图
    '''
    _name = 'metro_park_dispatch.special_days_config'
    _description = '特殊日期配置'
    _track_log = True
    
    date = fields.Date(string='日期')
    time_table = fields.Many2one(string='时刻表',
                                 comodel_name='metro_park_base.time_table')

    @api.model
    def get_special_day_config(self, date):
        '''
        取得特殊日期config
        :return:
        '''
        records = self.search([('date', '=', date)])
        return records[0]

    @api.one
    @api.constrains('date')
    def _check_time_span(self):
        '''
        说明，只有两种情况，一个的问在另一个的中间，至于两端都在中间特殊情况
        1、需要测试的点
        :return:
        '''
        records = self.search([('id', '!=', self.id),
                               ('date', '=', self.date)])
        if len(records) > 0:
            raise ValidationError('这天已设置特殊日期')

    @api.multi
    def delete_config(self):
        '''
        删除这个配置
        :return:
        '''
        self.unlink()

    @api.model
    def get_res_id(self, date):
        special_days = self.env['metro_park_dispatch.special_days_config']\
            .search([('date', '=', date)])
        if special_days:
            print(special_days.id)
            return special_days.id
        else:
            return False
