# -*- coding: utf-8 -*-

from odoo import http
import json


class RRWeb(http.Controller):
    @http.route('/rrweb/add_events', type='json', auth="public", cors="*", csrf=False)
    def add_events(self, **kw):
        '''
        添加日志
        :param kw:
        :return:
        '''
        json_request = http.request.jsonrequest
        start_time = json_request.get("start_time")
        end_time = json_request.get("end_time")
        events = json_request.get("data")
        http.request.env['metro_park_base.rrweb_events']\
            .sudo()\
            .create([{
            "start_time": start_time,
            "end_time": end_time,
            "events": json.dumps(events)
        }])
