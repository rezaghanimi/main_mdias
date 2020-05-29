# -*- coding: utf-8 -*-
from odoo import http

# class BaseData(http.Controller):
#     @http.route('/base_data/base_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_data/base_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_data.listing', {
#             'root': '/base_data/base_data',
#             'objects': http.request.env['base_data.base_data'].search([]),
#         })

#     @http.route('/base_data/base_data/objects/<model("base_data.base_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_data.object', {
#             'object': obj
#         })