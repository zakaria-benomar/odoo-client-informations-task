# -*- coding: utf-8 -*-
from odoo import http

# class ClientModule(http.Controller):
#     @http.route('/client_module/client_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_module/client_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_module.listing', {
#             'root': '/client_module/client_module',
#             'objects': http.request.env['client_module.client_module'].search([]),
#         })

#     @http.route('/client_module/client_module/objects/<model("client_module.client_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_module.object', {
#             'object': obj
#         })