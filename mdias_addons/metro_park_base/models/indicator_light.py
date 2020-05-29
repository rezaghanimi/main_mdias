
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import json
import pendulum


_logger = logging.getLogger(__name__)

'''
// 表示灯
struct IndicatorLightStatus {
    BYTE light : 1;               // 亮灯
    BYTE flash : 1;               // 闪灯
    BYTE red : 1;                 // 红灯
    BYTE yellow : 1;              // 黄灯
    BYTE green : 1;               // 绿灯
    BYTE blue : 1;                // 蓝灯
    BYTE white : 1;               // 白灯
    BYTE yellow2 : 1;             // 黄灯
};
'''


class IndicatorLight(models.Model):
    '''
    表示灯
    '''
    _name = 'metro_park_base.indicator_light'
    _description = '表示灯'
    _track_log = True

    name = fields.Char(string='名称')
    location = fields.Many2one(string="位置",
                               comodel_name="metro_park_base.location")

    index = fields.Integer(string="码位序号")
    type = fields.Integer(string="类型编号")
    light = fields.Integer(string="亮灯")
    flash = fields.Integer(string="闪灯")
    red = fields.Integer(string="红灯")
    yellow = fields.Integer(string="黄灯")
    green = fields.Integer(string="绿灯")
    blue = fields.Integer(string="蓝灯")
    white = fields.Integer(string="白灯")
    yellow2 = fields.Integer(string="黄灯")

    @api.model
    def update_status(self, location, data):
        '''
        更新状态
        :param data:
        :param location:
        :return:
        '''
        name = data["name"]
        if (name == 'ZCJ2' or name == 'ZCJ1' or name == 'ZCJ3' or name == 'ZCJ4') and data['light'] == 1:
            _logger.info('get indicator info: {data}'.format(data=data))

        record = self.search(
            [("name", "=", data["name"]), ('location', '=', location)])
        if record:
            if data['light'] == 1:
                _logger.info('udpate indicator status: {data}'.format(data=data))
            record.write(data)
            if data['light'] == 1:
                _logger.info('after udpate indicator status: {light}'.format(light=record.light))
            return record
        else:
            data['location'] = location
            self.create(data)

