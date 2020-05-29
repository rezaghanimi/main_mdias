
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Hour(models.Model):
    '''
    时间, 由于有个次日概念
    '''
    _name = 'metro_park_base.hour'
    _order = 'val'
    
    hour = fields.Char(string='时')
    val = fields.Char(string='值')
    is_next_day = fields.Boolean(string="是否次日",
                                 compute="_compute_is_next_day")
    next_day_val = fields.Integer(string="第二日",
                                  compute="_compute_is_next_day", default=0)

    @api.one
    @api.model
    def _compute_is_next_day(self):
        '''
        计算
        :return:
        '''
        if self.val >= 24:
            self.is_next_day = True
            self.next_day_val = self.hour - 24




