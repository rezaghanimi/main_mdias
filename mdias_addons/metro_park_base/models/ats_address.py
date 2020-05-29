
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AtsAddress(models.Model):
    '''
    ats地址, 时刻表传入过来的时候是以这个编号
    [
        {
            "End_station_id": 0,
            "Start_station_id": 0,
            "date": "2019-8-9 0:0:0",
            "line_id": 10,
            "msg_id": 34,
            "sub_id": 2,
            "trip_cnt": 47,
            "trip_list": [
                {
                    "Global_id": "1041",
                    "destination_id": 822083584,
                    "rec_cnt": 3,
                    "train_id": "",
                    "trip_rec_list": [
                        {}
                    ]
                }
            ]
        }
    ]
    '''
    _name = 'metro_park_base.ats_address'
    _track_log = True
    
    no = fields.Char(string='编号')
    name = fields.Char(string='名称')
    line = fields.Many2one(string="线路", comodel_name="metro_park_base.line")
    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location',
                               domain="[('line.id', '=', line)]")
    remark = fields.Char(string='备注')
