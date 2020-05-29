import json

from odoo import models, api


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        """
            重写_fields_view_get 增加 view options,自定义view参数, 复杂参数可以通过这个传递
        """
        result = super(Base, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=False,
                                                    submenu=submenu)
        options = {}
        if 'view_id' in result:
            try:
                options = json.loads(self.env['ir.ui.view'].browse(result['view_id']).options)
            except:
                pass

        result['options'] = options
        return result

    def group_by(self, key):
        if isinstance(key, str):
            func = lambda record: getattr(record, key)
        else:
            func = key
        _result = {}
        for re in self:
            grp_key = func(re)
            _result.setdefault(grp_key, [])
            _result[grp_key].append(re)
        return _result
