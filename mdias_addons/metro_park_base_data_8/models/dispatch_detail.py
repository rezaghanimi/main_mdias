# -*- coding: utf-8 -*-

from odoo import models, api
import logging
_logger = logging.getLogger(__name__)


class DispatchDetail(models.Model):
    '''
    调车详情，用于保存调车通知单的列表内容 一个勾计划
    '''
    _inherit = 'metro_park_dispatch.dispatch_detail'

    @api.depends('source_rail', 'rail')
    def _compute_from_wash(self):
        '''
        计算是否从洗车线经过
        :return:
        '''
        # 高大路牵三
        drag_line1 = self.env.ref('metro_park_base_data_8.gao_da_lu_rail_D22G')
        # 高大路牵二
        drag_line2 = self.env.ref('metro_park_base_data_8.gao_da_lu_rail_D2G')
        for record in self:
            if record.source_rail and record.rail and record.source_rail.id == drag_line1.id and record.rail.id == drag_line2.id:
                record.from_wash = True
            else:
                record.from_wass = False
