from odoo import models, fields


class LogSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    screen_video_reserve_days = fields.Integer(string='视频保留天数',
                                               config_parameter='metro_park_production.screen_video_reserve_days',
                                               default=90)
