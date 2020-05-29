# -*- coding: utf-8 -*-
from odoo import http

# class OdooModeler(http.Controller):
#     @http.route('/odoo_modeler/odoo_modeler/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_modeler/odoo_modeler/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_modeler.listing', {
#             'root': '/odoo_modeler/odoo_modeler',
#             'objects': http.request.env['odoo_modeler.odoo_modeler'].search([]),
#         })