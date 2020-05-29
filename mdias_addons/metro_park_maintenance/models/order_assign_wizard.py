
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrderAssignWizard(models.Model):
    '''
    工单派发
    '''
    _name = 'metro_park_maintenance.order_assign_wizard'
    _track_log = True
    
    department = fields.Many2one(string='工班',
                                 comodel_name='funenc.wechat.department')
    worker = fields.Many2one(string='检修人员',
                             comodel_name='funenc.wechat.user')
