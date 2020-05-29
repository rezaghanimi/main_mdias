
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RepairParam(models.Model):
    '''
    修程参数
    '''
    _name = 'metro_park_maintenance.repair_param'
    _description = '修程参数'
    
    name = fields.Char(string='参数名称', required=True)
    val = fields.Char(string='参数度量值', required=True)
    unit = fields.Char(string='参数单位', required=True)
    use = fields.Boolean(string='是否启用')
    related_duration = fields.Many2many(string="关联修程",
                                        comodel_name="metro_park_maintenance.repair_rule",
                                        relation="repair_param_duration_rel",
                                        column1="param_id",
                                        column2="duration_id")

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "参数名称不能重复")]

    @api.multi
    def change_param(self):
        '''
        修改参数
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.repair_param",
            'view_mode': 'form',
            'res_id': self.id,
            'context': {
                'form_view_initial_mode': 'edit'
            },
            'target': 'new',
            "views": [[self.env.ref('metro_park_maintenance.repair_param_form').id, "form"]]
        }
