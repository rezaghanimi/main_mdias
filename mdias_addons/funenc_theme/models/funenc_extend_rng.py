# -*- coding: utf-8 -*-

from odoo import tools
from odoo.tools import view_validation
from lxml import etree
from odoo import tools

import os, logging

_logger = logging.getLogger(__name__)


def relaxng(view_type):
    """ Return a validator for the given view type, or None. """
    cur_path, _ = os.path.split(os.path.realpath(__file__))
    if view_type not in view_validation._relaxng_cache:
        with tools.file_open(os.path.join(cur_path, '..', 'rng', '%s_view.rng' % view_type)) as frng:
            try:
                relaxng_doc = etree.parse(frng)
                view_validation._relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
            except Exception:
                _logger.exception('Failed to load RelaxNG XML schema for views validation')
                view_validation._relaxng_cache[view_type] = None
    return view_validation._relaxng_cache[view_type]

for index, pred in enumerate(view_validation._validators['tree']):
    if pred.__name__ == 'valid_field_in_tree':
        view_validation._validators['tree'].pop(index)
        break

view_validation.relaxng = relaxng




