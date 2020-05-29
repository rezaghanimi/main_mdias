import logging
import traceback
from collections import defaultdict

from odoo import api, models
from odoo.tools import pycompat
from .lib.management import LogManage

_logger = logging.getLogger(__name__)

LogManage.register_type('write', '修改')
LogManage.register_type('delete', '删除')
LogManage.register_type('create', '创建')

model = models.BaseModel

super_create = model.create

super_unlink = model.unlink

super_write = model.write


def make_fields_log_value(record, res_id=None, values=None, mode='edit'):
    if mode == 'write':
        field_names = list(values.keys())
        res = record.search_read([('id', '=', res_id)], field_names)
        if not res:
            return False
        old_values = res[0]
        new_values = values
    elif mode == 'create':
        old_values = defaultdict(str)
        new_values = values
        field_names = list(values.keys())
    elif mode == 'delete':
        res = record.search_read([('id', '=', res_id)])
        if not res:
            return False
        old_values = record.search_read([('id', '=', res_id)])[0]
        field_names = list(old_values.keys())
        new_values = defaultdict(str)
    else:
        return
    values = []

    for field_name in field_names:

        if field_name not in record._fields:
            continue
        field = getattr(record, '_fields')[field_name]

        field_type = field.type
        old_v = old_values[field_name]
        new_v = new_values[field_name]
        if field_type in ['one2many', 'many2many', 'one2many']:
            new_v = str(new_v)
            old_v = str(old_v)
        elif field_type in ['datetime', 'date']:
            new_v = str(new_v)
            old_v = str(old_v)
        elif field_type == 'text':
            new_v = field.convert_to_column(new_v, record)
            old_v = field.convert_to_column(old_v, record)
        if old_v == new_v:
            continue
        display_name = field.string
        values.append({
            'filed_name': field_name,
            'filed_display': display_name,
            'new_value': new_v,
            'old_value': old_v,
            'field_type': field_type
        })
    return values


def write_log(records, mode, values=None):
    if not getattr(records, '_track_log', False):
        return False
    for record in records:
        try:
            field_values = make_fields_log_value(record, values=values, res_id=record.id, mode=mode)
            if not field_values:
                continue
            LogManage.put_log(record=record, mode=mode, res_id=record.id, fields=field_values)
        except:
            _logger.info('write log fail, mode is %s', mode)
            traceback.print_exc()


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.multi
    def unlink(self):
        write_log(self, 'delete')
        res = super(Base, self).unlink()
        return res

    @api.multi
    def write(self, vals):
        write_log(self, 'write', values=vals)
        res = super(Base, self).write(vals)
        return res

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        result = super(Base, self).create(vals_list)
        for record, values in pycompat.izip(result, vals_list):
            if not values:
                continue
            write_log(record, 'create', values)
        return result
