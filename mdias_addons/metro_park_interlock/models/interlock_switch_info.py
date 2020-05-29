
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InterlockSwitchInfo(models.Model):
    '''
    道岔
    '''
    _name = 'metro_park.interlock.switch_info'
    _order = 'index'
    _description = '道岔信息'
    _track_log = True

    route_id = fields.Many2one(comodel_name='metro_park.interlock.route',
                               string='进路',
                               ondelete="cascade")
    index = fields.Integer(string='索引')
    is_reverse = fields.Boolean(string='是否反位')
    is_protect = fields.Boolean(string='是否防护')

    switches = fields.One2many(string='道岔',
                               comodel_name="metro_park.interlock.switch_sub_info",
                               inverse_name="switch_info_id")

    display = fields.Char(string="显示", compute="_compute_display")

    representation = fields.Text(string="描述")

    @api.depends('is_reverse', 'is_protect', 'switches')
    def _compute_display(self):
        '''
        计算显示
        :return:
        '''
        for record in self:
            names = record.mapped("switches.switch.name")
            name = '/'.join(names)
            if record.is_protect and record.is_reverse:
                name = '[({name})]'.format(name=name)
            elif record.is_protect:
                name = '[{name}]'.format(name=name)
            elif record.is_reverse:
                name = '({name})'.format(name=name)
            record.display = name
