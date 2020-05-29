# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, models, fields


class MaintenanceManagementEquipmentState(models.Model):
    _name = 'maintenance_management.equipment_state'
    _description = '设备的连接状态'

    name = fields.Char(string='设备')
    equipment = fields.Many2one('maintenance_equipment', string='设备关联')
    line = fields.Char(string='连接线')
    state = fields.Selection([('disconnect', '断开'), ('connection', '连接')], string='状态', default='connection')

    @api.model
    def according_maintenance_connect_state(self):
        '''
        显示维保状态
        断开链接页面链接状态修改
        :return:
        '''
        all_rec = self.env['maintenance_management.equipment_state'].sudo().search_read([], ['name', 'line', 'state'])
        return all_rec

    @api.multi
    def equipment_state_page_refresh(self):
        self.trigger_up_event('equipment_state_page_refresh', '页面刷新')
