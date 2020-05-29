# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)

class LocationRelation(models.Model):
    _name = 'metro_park_dispatch.construction_location_relation'

    out_line_id = fields.Integer()
    out_location_id = fields.Integer()
    location_id = fields.Many2one('metro_park_base.location', string='MDIAS位置')


class ConstructionRelation(models.Model):
    _name = 'metro_park_dispatch.construction_area_relation'

    area_id = fields.Integer(string='区域ID')
    area_name = fields.Char(string='区域名')
    area_code = fields.Char(string='区域编码')
    park_element_code = fields.Char(string='区段编码', help='编码对应MDIAS中的区段no或switch name')
    element_type = fields.Selection([('rail', '股道'), ('switch', '道岔')],
                                    default='rail',
                                    required=True)
    out_line_id = fields.Integer(string="线路")
    out_location_id = fields.Integer(string="位置")
    out_work_status_code = fields.Selection([('Idle', '空闲'),
                                             ('A1Use', 'A1施工占用'),
                                             ('A2Use', 'A2施工占用'),
                                             ('A3Use', 'A3施工占用'),
                                             ('B1Use', 'B1施工占用'),
                                             ('B2Use', 'B2施工占用'),
                                             ('C1Use', 'C1施工占用'),
                                             ('unknown', '未知')
                                             ], string='施工状态', default='unknown')
    out_area_active = fields.Selection(selection=[(1, '启用'), (0, '禁用'), (-1, '未知')],
                                       string='区域启用状态', default=-1)
    out_power_status_update_time = fields.Integer()
    out_power_status_code = fields.Selection([('On', '带电'),
                                              ('Off', '停电'),
                                              ('unknown', '未知')],
                                             default='unknown',
                                             string='供电状态')

    def _request_area_data(self, locations):
        api_obj = self.env['metro_park_dispatch.construction.http']
        work_data = []
        for loc in locations:
            work_data += api_obj.construction_work_area_status(loc[0], loc[1])

        update_values = {}
        for wrd in work_data:
            if 'workAreaId' not in wrd:
                continue
            update_values[wrd['workAreaId']] = {
                'out_work_status_code': wrd.get('statusCode', 'unknown'),
                'out_area_active': wrd.get('recordStatus', -1),
                'out_power_status_update_time': wrd.get('statusChangeTime', 0) / 1000
            }
        return update_values

    def _clear_update_values(self, values):
        """
            筛选需要更新的数据
        :param values: {'area_id: val<{}>}」
        :return:
        """
        areas = self.search_read([('area_id', 'in', list(values.keys()))],
                                 ['id', 'area_id',
                                  'out_power_status_code',
                                  'out_work_status_code',
                                  'out_area_active',
                                  'out_power_status_update_time'])
        write_values = []
        for area in areas:
            aid = area['area_id']
            new_val = values[aid]
            for fid in new_val.keys():
                if new_val[fid] != area[fid]:
                    write_values.append(dict(new_val, id=area['id']))
                    continue
        return write_values

    def _write_update_values(self, values):
        for val in values:
            aid = val['id']
            if not aid:
                continue
            record = self.browse(aid)
            if record:
                del val['id']
                record.write(val)

    @api.model
    def corn_synchronization(self):
        locations = []
        relation_locations = self.env['metro_park_dispatch.construction_location_relation'].search([])
        for loc in relation_locations:
            locations.append([loc.out_line_id, loc.out_location_id])
        try:
            update_values = self._request_area_data(locations)
        except Exception as e:
            _logger.info("执行施工调度区域状态同步接口异常：{}".format(str(e)))
            return False
        if not update_values:
            return False
        values = self._clear_update_values(update_values)
        self._write_update_values(values)
