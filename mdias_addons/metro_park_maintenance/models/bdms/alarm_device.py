from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class AlarmDevice(models.Model):
    _name = "funenc.alarm.device"
    _description = "报警设备"
    _order = 'id desc'
    _track_log = True
    
    name = fields.Char(string="设备名称", required=True)
    composition_unit = fields.Char(string="户口页组成单元")
    alarm_level = fields.Integer(string="报警等级", default=1)


