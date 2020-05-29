# -*- coding: utf-8 -*-
# @author    magicianliang
from odoo import api, models, fields


class BreakInfo(models.Model):
    _name = 'tcms.break_info'

    trainCode = fields.Char(string='列车代码')
    faultCode = fields.Char(string='故障代码')
    faultLocat = fields.Char(string='故障状态')
    faultState = fields.Char(string='故障状态')
    faultLevel = fields.Char(string='故障等级')
    getTime = fields.Char(string='故障发生时间')

    def get_tcms_break_info(self):
        rec = self.search_read([])
        return rec


class BreakInformation(models.Model):
    _name = 'tcms.break_information'

    BigCode = fields.Char()
    paraCode = fields.Char()
    Desc = fields.Char()
