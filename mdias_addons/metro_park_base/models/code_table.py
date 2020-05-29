# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CodeTable(models.Model):
    '''
    按扭表
    '''
    _name = 'metro_park_base.code_table'
    _rec_name = 'code'
    _order = 'index'
    _track_log = True

    code = fields.Char(string='码位')
    location = fields.Many2one(string='位置', comodel_name='metro_park_base.location')
    index = fields.Char(string='索引')
    code_type = fields.Selection(selection=[("switch", "道岔"),
                                            ("rail_sec", "区段"),
                                            ("back_signal", "进站信号"),
                                            ("out_signal", "出站信号"),
                                            ("dispatch_signal", "调车信号"),
                                            ("indicator", "指示灯"),
                                            ("sealed_counter", "铅封计数"),
                                            ("alarm", "报警")])


