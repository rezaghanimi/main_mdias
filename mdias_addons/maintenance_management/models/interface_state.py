# -*- conding:utf-8 -*-

from odoo import api, fields, models


class InterfaceState(models.Model):
    _name = 'maintenance_management.interface_state'
    _description = '接口状态数据'
    _track_log = True

    type = fields.Char(string='类型')
    send_count = fields.Char(string='发送')
    recv_count = fields.Char(string='接收')
    tms = fields.Char(string='时间')
    place = fields.Char(string='地点')
