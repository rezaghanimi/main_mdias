
from odoo import models, api, fields
import json
import logging
import traceback
_logger = logging.getLogger(__name__)


class View(models.Model):
    _inherit = 'ir.ui.view'

    options_db = fields.Char()
    options = fields.Char(compute='_compute_options', inverse='_inverse_options')

    def _inverse_options(self):
        for view in self:
            data = dict(options_db=view.options)
            view.write(data)

    def _compute_options(self):
        for view in self:
            options_db = view.options_db
            options = "{}"
            if options_db:
                    options = options_db
            view.options = options


# {
#     "tab_domain": {
#         "我的项目": "[['create_uid', '=', user.id]]",
#         "审核中的项目": "[['state', '=', 'approving']]"
#     }
# }
# json.dumps()