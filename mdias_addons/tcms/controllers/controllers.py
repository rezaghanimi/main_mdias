# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import pendulum


class TcmsDateGet(http.Controller):

    @http.route('/tcms/driver_cracked/', type='http', auth='none', cors=False)
    def get_driver_cracked_data(self):
        rec = request.env['tcms.driver_cracked'].search_read([])
        return rec

    @http.route('/tcms/sync_distance/<int:month>', type='http', auth='none', cors=False)
    def get_station_distance_data(self, month):
        days = pendulum.date(2019, month, 1).days_in_month
        for day in range(1, days+1):
            date = pendulum.date(2019, month, day)
            distances = request.env['tcms.station_distance'].search([('create_date', '=', date)])
            for distance in distances:
                if distance.total_mileage:
                    train_dev = request.env['metro_park_maintenance.train_dev'].search(
                        [('dev_name', '=', '1' + distance.name)])
                    history = request.env['metro_park_maintenance.history_miles'].search(
                        [('year', '=', 2019), ('month', '=', month), ('train_dev', '=', train_dev.id)])
                    history.write({'day%s' % day: distance.total_mileage, 'day%s_is_manual' % day: True}, 0)
        return "sync success"

