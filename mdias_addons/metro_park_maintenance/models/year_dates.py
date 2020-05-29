
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class YearDates(models.Model):
    '''
    年计划中的天
    '''
    _name = 'metro_park_maintenance.year_dates'

    name = fields.Char(string='名称')

    year = fields.Integer(string="年")
    month = fields.Integer(string="月")
    day = fields.Integer(string="日")

    @api.model
    def init_dates(self):
        '''
        创建日期
        :return:
        '''
        records = self.search([], limit=1)
        if len(records) == 0:
            vals = []
            for year in range(2018, 2050):
                year_start = pendulum.date(year, 1, 1)
                year_end = pendulum.date(year, 12, 31)
                days = year_end.day_of_year
                for day in range(0, days):
                    tmp_date = year_start.add(days=day)
                    vals.append({
                        "year": tmp_date.year,
                        "month": tmp_date.month,
                        "day": tmp_date.day,
                        "name": tmp_date.format('YYYY-MM-DD')
                    })
            self.create(vals)
