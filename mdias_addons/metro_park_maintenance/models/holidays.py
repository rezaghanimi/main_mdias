
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Holidays(models.Model):
    '''
    节假日
    '''
    _name = 'metro_park_maintenance.holidays'
    
    date = fields.Date(string='日期')
    name = fields.Char(string='名称')
    remark = fields.Char(string='备注')

    @api.one
    @api.constrains('name')
    def _check_description(self):
        records = self.search([('date', '=', self.date), ('id', '!=', self.id)])
        if records:
            raise exceptions.Warning("日期不能重复!")


