# -*- coding: utf-8 -*-
from odoo import api, models, fields
from ...odoo_operation_log.model_extend import LogManage
import datetime

LogManage.register_type('export', '导出')


class CallRecord(models.Model):
    _name = 'maintenance_management.call_record'
    _description = '报警记录'
    _track_log = True
    _order = 'create_date desc'

    place = fields.Char(compute="_compute_place_name", store=True, string='地点')
    site = fields.Char(compute="_compute_site_name", store=True, string='位置')
    equipment = fields.Many2one('maintenance_equipment', string='设备')
    content = fields.Char(string='内容')
    ip_site = fields.Char(string='IP地址')
    maintenance_advice = fields.Char(string='维护建议')
    alarm_level = fields.Char(string='维护等级', default='低')
    failure_time = fields.Datetime(string='发生时间')

    @api.one
    @api.depends('equipment')
    def _compute_place_name(self):
        self.place = self.equipment.place.station.name

    @api.one
    @api.depends('equipment')
    def _compute_site_name(self):
        self.site = self.equipment.place.name

    @api.model
    def export_data_rec(self):
        LogManage.put_log(content='报警记录导出', mode='export')
        return {
            'name': '数据导出',
            'target': 'new',
            'type': 'ir.actions.act_url',
            'url': '/maintenance_management/call_api_task/export_data'
        }

    @api.model
    def print_data_rec(self):
        lis = {'detail': []}
        all_recs = self.search_read(
            [('id', 'in', self._context.get('print_rec'))],
            fields=['write_date', 'place', 'site', 'equipment', 'content', 'ip_site', 'maintenance_advice',
                    'alarm_level'])

        for all_rec in all_recs:
            lis['detail'].append({
                'write_date': str(all_rec.get('write_date') + datetime.timedelta(hours=8))[:19] if all_rec.get(
                    'write_date') else '',
                'place': all_rec.get('place') if all_rec.get('place') else '',
                'site': all_rec.get('site') if all_rec.get('site') else '',
                'equipment': all_rec.get('equipment')[1] if all_rec.get('equipment') else '',
                'content': all_rec.get('content') if all_rec.get('content') else '',
                'ip_site': all_rec.get('ip_site') if all_rec.get('ip_site') else '',
                'maintenance_advice': all_rec.get('maintenance_advice') if all_rec.get('maintenance_advice') else '',
                'alarm_level': all_rec.get('alarm_level') if all_rec.get('alarm_level') else '',
            })

        return {
            "name": "报警记录打印",
            "type": "ir.actions.client",
            "tag": "maintenance_print",
            'target': 'new',
            'context': {"vue_data": lis, 'main_template': 'call_record_template'},
        }
