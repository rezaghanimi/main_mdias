
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ParkMap(models.Model):
    '''
    站场图
    '''
    _name = 'metro_park_base.park_map'
    _description = '站场图管理'
    _track_log = True
    
    name = fields.Char(string='名称')
    xml = fields.Binary(string='文件')
    xml_name = fields.Char(string='文件名称')
    remark = fields.Text(string='备注')

    @api.multi
    def get_map_info(self):
        '''
        取得地图数据
        :return:
        '''
        return self.read()

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "名称不能得重复")]

