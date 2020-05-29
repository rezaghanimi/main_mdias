# -*- coding: utf-8 -*-

from odoo import models, api


class AttachmentExtend(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def get_attrachment_data(self, res_model, res_id):
        '''
        取得附件数据
        :return:
        '''
        return self.search_read([('res_model', '=', res_model)])