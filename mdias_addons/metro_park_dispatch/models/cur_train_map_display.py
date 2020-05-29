
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import base64
import io
import json


class CurTrainMapDisplay(models.Model):
    '''
    现车管理站场图显示
    '''
    _name = 'metro_park_dispatch.cur_train_map_display'
    _description = '现车管理地图显示'
    _track_log = True

    def _get_default_location(self):
        '''
        取得用户线别
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise exceptions.Warning('当前用户没有配置位置,请先配置用户位置!')
        return location.id

    def _get_default_location_domain(self):
        '''
        取得默认位置domain
        :return:
        '''
        locations = self.env.user.locations
        location_ids = locations.ids
        install_mode = self.env.context.get('install_mode', False)
        if len(location_ids) == 0 and not install_mode:
            raise exceptions.Warning('当前用户没有配置场段信息')
        return [('id', 'in', location_ids)]

    def _get_default_line(self):
        '''
        取得当前线路
        :return:
        '''
        location = self.env.user.cur_location
        install_mode = self.env.context.get('install_mode', False)
        if not location and not install_mode :
            raise exceptions.Warning('当前用户没有配置位置,请先配置用户位置!')
        return location.line.id

    line_id = fields.Many2one(string='线路',
                              comodel_name='metro_park_base.line',
                              default=_get_default_line)

    location_id = fields.Many2one(string='位置',
                                  comodel_name='metro_park_base.location',
                                  domain=_get_default_location_domain,
                                  default=_get_default_location)

    @api.model
    def get_location_map_data(self, location_id):
        ''''
        取得站场图数据
        '''
        location_model = self.env['metro_park_base.location']
        record = location_model.browse(location_id)
        location_map = record.location_map
        if not location_map:
            raise exceptions.ValidationError('当前场段没有配置位置信息')
        data = location_map.read()[0]
        tmp_io = io.BytesIO(base64.decodebytes(data['xml']))
        line = tmp_io.read()
        data['xml'] = line.decode('utf-8')
        return data

    @api.model
    def get_map_info(self):
        '''
        取得站场图信息
        :return:
        '''
        location_id = self._get_default_location()
        location_model = self.env['metro_park_base.location']
        record = location_model.browse(location_id)
        location_map = record.location_map
        if not location_map:
            raise exceptions.ValidationError('当前场段没有配置位置信息')
        data = location_map.read()[0]
        tmp_io = io.BytesIO(base64.decodebytes(data['xml']))
        line = tmp_io.read()
        data['xml'] = line.decode('utf-8')
        return data

    @api.model
    def jump_cur_train_map(self):
        '''
        跳转到现车管理
        :return:
        '''
        return self.jump_url()

    @api.model
    def jump_url(self):
        '''
        跳转路由, 应当单独开一个页面比较明智
        :return:
        '''
        records = self.env['metro_park_base.system_config'].search([])
        record = records[0]
        url = '{host}/web?debug=assets#action=cur_train_client'\
            .format(host=record.base_url)
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new"
        }

    @api.model
    def get_cur_train_map_info(self):
        '''
        取得现车
        :return:
        '''
        user = self.env.user
        if not user.cur_location:
            raise exceptions.ValidationError("当前用户没有配置位置")
        location_id = user.cur_location.id
        train_info = self.get_cur_train_data(location_id)
        btn_map = json.loads(user.cur_location.park_btns)
        return {
            "train_info": train_info,
            "btn_map": btn_map
        }

    @api.model
    def get_cur_train_data(self, location_id):
        '''
        取得现车数据
        :return:
        '''
        if not location_id:
            raise exceptions.ValidationError('参数错误')

        model = self.env['metro_park_dispatch.cur_train_manage']
        records = model.search([('cur_rail.location.id', '=', location_id)])

        vals = []
        for record in records:
            val = dict()
            val['id'] = record.id
            val['type'] = record.train_type.id
            val['name'] = record.train_no
            val['position'] = record.cur_rail.name
            val['status'] = record.train_status
            vals.append(val)

        return vals



