# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError
import os
import pendulum


class Video(models.Model):

    _name = 'metro_park_production.video'

    upload_data = fields.Datetime(default=fields.Datetime.now)
    attachment_id = fields.Many2one('ir.attachment', string='视频文件')
    location_id = fields.Many2one('metro_park_base.ats_rail_location_map')
    machine_name = fields.Char()
    ip = fields.Char()
    datas = fields.Binary(compute='compute_datas', string='下载内容')
    datas_fname= fields.Char(compute='compute_datas_fname')

    @api.one
    def compute_datas(self):
        self.datas = self.sudo().attachment_id.datas

    @api.one
    def compute_datas_fname(self):
        self.datas_fname= self.sudo().attachment_id.name + '.mp4'

    @api.model
    def action_track_config(self):
        form_id = self.env.ref('metro_park_dispatch.res_config_train_run_track_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(form_id, 'form')],
            'target': 'new',
            'context': dict(self._context, dialog_size='medium'),
        }

    @api.model
    def cron_task_delete_video(self):
        screen_video_reserve_days = self.env['ir.config_parameter'].sudo().\
            get_param('metro_park_production.screen_video_reserve_days')
        delete_after_date = pendulum.now().subtract(days=int(screen_video_reserve_days)).date()
        video_ids = self.search([('create_date', '<=', delete_after_date)])
        attachment_ids = video_ids.mapped('attachment_id')
        attachment_ids.sudo().unlink()
        video_ids.sudo().unlink()
