from odoo import models, fields, api


class TrackGraphRelation(models.Model):
    """
        描述道岔和道岔,轨道和轨道图形关系
    """

    _name = 'metro_park_base.graph_relation'

    x_rail = fields.Many2one(comodel_name='metro_park_base.rails_sec', string="x区段")
    y_rail = fields.Many2one(comodel_name='metro_park_base.rails_sec', string="y区段")
    x_switch = fields.Many2one(comodel_name='metro_park_base.switches', string="x道岔")
    y_switch = fields.Many2one(comodel_name='metro_park_base.switches', string="y道岔")

    @property
    def switch_ids(self):
        return (self.mapped('x_switch') + self.mapped('y_switch')).ids

    @property
    def rail_ids(self):
        return (self.mapped('x_rail') + self.mapped('y_rail')).ids
