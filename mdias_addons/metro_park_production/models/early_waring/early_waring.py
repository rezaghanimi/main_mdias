# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.models import SUPERUSER_ID


class EarlyWaringTranManage(models.TransientModel):
    """
        发车和收车管理误点预警事件范围
    """

    _inherit = 'res.config.settings'
    # 延误
    retard_second = fields.Integer(default=60)
    # 提前
    ahead_second = fields.Integer(default=60)

    @api.model
    def early_waring_notify_action(self):
        form_id = self.env.ref('metro_park_production.res_config_production_train_view_form').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'tree',
            'views': [(form_id, 'form')],
            'target': 'new',
            'context': dict(self._context),
        }


class EarlyWaringSettingLine(models.Model):

    _name = 'metro_park_production.early_waring.line'

    waring_line_name = fields.Char()
    single_threshold_value_percentage = fields.Float(string='单个阀值')
    all_threshold_value_percentage = fields.Float(string='总体阀值')
    all_color = fields.Char(string='色值')
    single_color = fields.Char(string='色值')
    all_open = fields.Boolean(string='开关状态', default=True)
    single_open = fields.Boolean(string='开关状态', default=True)
    waring_setting_id = fields.Many2one('metro_park_production.early_waring')


class EarlyWaringSetting(models.Model):

    _name = 'metro_park_production.early_waring'

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)', 'The name of waring!'),
        ('name_tag', 'UNIQUE (apply_tag)', 'The apply tag of waring!'),
    ]

    name = fields.Char(string='预警名称')
    apply_tag = fields.Char()
    settings = fields.One2many('metro_park_production.early_waring.line', 'waring_setting_id', string='预警设置项')
    waring_type_description = fields.Char()

    @api.model
    def get_early_data(self):
        result = []
        all_record = self.search([])
        for record in all_record:
             result.append({
                'name': record.name,
                'tag': record.apply_tag,
                'id': record.id,
                'settings': record.settings.read([
                    'waring_line_name', 'single_threshold_value_percentage', 'id',
                    'all_threshold_value_percentage', 'all_color', 'single_color', 'all_open', 'single_open'
                ])
            })
        return result

    def unlink(self):
        if self.env.user.id != SUPERUSER_ID:
            return False

        return super(EarlyWaringSetting, self).unlink()
