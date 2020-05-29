from odoo import models, fields, api, exceptions


class TrackConfig(models.TransientModel):
    """
        发车和收车管理误点预警事件范围
    """

    _inherit = 'res.config.settings'

    track_create_mode = fields.Selection([('ats_track', 'ATS跟踪'),
                                          ('interlock_compute', '联锁计算')],
                                         string='轨迹跟踪方式',
                                         default='interlock_compute',
                                         required=True,
                                         config_parameter='dispatch.track_create_mode')

    @api.model
    def action_track_config(self):
        '''
        跟踪方式配置
        :return:
        '''
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
