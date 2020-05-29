from odoo import models, fields, api


class ProductionFiles(models.Model):
    _name = 'metro_park_production.files'
    _description = '电子归档'
    _rec_name = 'file_name'
    _track_log = True

    file_name = fields.Char('文件名')
    file_size = fields.Char(compute='_compute_file', string='文件大小')
    file_content = fields.Binary('文件', attachment=True)

    file_type_id = fields.Many2one('metro_park_production.file_type', string='文件类型')

    def _compute_file(self):
        for record in self:
            record.file_size = '%s KB' % round(len(record.file_content) * 3 / 4 / 1024, 2)
