# -*- coding: utf-8 -*-

from odoo import models


class API(models.AbstractModel):
    _name = 'metro_park_dispatch.construction.api'

    def _get_construction_area_id_by_code(self, code, area_type):
        relation_area = self.env['metro_park_dispatch.construction_area_relation'] \
            .search([('park_element_code', '=', code),
                     ('element_type', '=', area_type)], limit=1)
        if relation_area:
            return relation_area.area_id
        return False

    def query_area_construction_status(self, code_infos):
        """
        查询指定区域的施工状态
        :param code_infos: 区域状态信息数据列表 [{'code': 'T1XX', 'type': 'xx<switch, rail>' }]
             @code 查询区域编码，道岔或区段编码
             @type (rail->区段; switch->道岔)
        :return: 区域施工信息
        """
        area_ids = set([])
        for info in code_infos:
            code = info.get('code')
            atype = info.get('type')
            if not (code and atype):
                continue
            aid = self._get_construction_area_id_by_code(code, atype)
            if not aid:
                return {
                    'status': -1,
                    'message': '查询不到指定区域供电分区:%s' % code
                }
            area_ids.add(aid)

