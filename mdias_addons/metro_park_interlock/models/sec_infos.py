
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SecInfos(models.Model):
    '''
    区段信息
    '''
    _name = 'metro_park.interlock.sec_infos'
    _description = '区段信息'
    _track_log = True

    route_id = fields.Many2one(string="所属进路",
                               comodel_name="metro_park.interlock.route",
                               ondelete="cascade",
                               help="进路是进路指令")
    index = fields.Char(string='序号')
    sec = fields.Many2one(string='区段',
                          comodel_name="metro_park_base.rails_sec")


