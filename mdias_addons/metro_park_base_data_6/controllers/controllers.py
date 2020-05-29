# -*- coding: utf-8 -*-
from odoo import http

# class MetroParkBaseData6(http.Controller):
#     @http.route('/metro_park_base_data_6/metro_park_base_data_6/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/metro_park_base_data_6/metro_park_base_data_6/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('metro_park_base_data_6.listing', {
#             'root': '/metro_park_base_data_6/metro_park_base_data_6',
#             'objects': http.request.env['metro_park_base_data_6.metro_park_base_data_6'].search([]),
#         })

#     @http.route('/metro_park_base_data_6/metro_park_base_data_6/objects/<model("metro_park_base_data_6.metro_park_base_data_6"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('metro_park_base_data_6.object', {
#             'object': obj
#         })