from odoo import models, fields


class FileType(models.Model):
    _name = 'metro_park_production.file_type'
    _description = '电子归档文件分类'
    _rec_name = 'name'
    _track_log = True

    name = fields.Char('分类名称')
    file_ids = fields.One2many('metro_park_production.files', 'file_type_id', string='文件')