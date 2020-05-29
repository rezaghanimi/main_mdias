# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo.tools.view_validation import validate
from odoo import tools


@validate('tree')
def valid_field_in_tree(arch):
    """ Children of ``tree`` view must be ``field`` or ``button``."""
    return all(
        child.tag in ('field', 'button', 'widget')
        for child in arch.xpath('/tree/*')
    )


setattr(tools, 'valid_field_in_tree', valid_field_in_tree)
