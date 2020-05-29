# -*- coding: utf-8 -*-

from odoo.tools.convert import xml_import
import os.path

from odoo.tools import convert
from odoo.tools import pycompat
from lxml import etree
from odoo.tools.misc import ustr

import os, logging

_logger = logging.getLogger(__name__)

def funenc_convert_import(cr, module, xmlfile, idref=None, mode='init', noupdate=False, report=None):
    doc = etree.parse(xmlfile)
    cur_path, _ = os.path.split(os.path.realpath(__file__))
    # relaxng = etree.RelaxNG(
    #     etree.parse(os.path.join(cur_path, '..', 'rng', 'import_xml.rng')))
    # try:
    #     relaxng.assert_(doc)
    # except Exception:
    #     _logger.info("The XML file '%s' does not fit the required schema !", xmlfile.name, exc_info=True)
    #     _logger.info(ustr(relaxng.error_log.last_error))
    #     raise

    if idref is None:
        idref={}
    if isinstance(xmlfile, pycompat.string_types):
        xml_filename = xmlfile
    else:
        xml_filename = xmlfile.name
    obj = xml_import(cr, module, idref, mode, report=report, noupdate=noupdate, xml_filename=xml_filename)
    obj.parse(doc.getroot(), mode=mode)
    return True

convert.convert_xml_import = funenc_convert_import

