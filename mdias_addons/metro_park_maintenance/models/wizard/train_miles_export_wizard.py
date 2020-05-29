# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.http import request
import xlrd
import xlwt
import base64
import logging
from datetime import datetime
from datetime import timedelta
_logger = logging.getLogger(__name__)


class GetMilesExportWizard(models.TransientModel):
    '''
    公里数统计表导出向导
    '''

    _name = "metro_park_maintenance.train_miles_export_wizard"

    year = fields.Many2one(string="年份",
                           comodel_name="metro_park_maintenance.year")
    month = fields.Many2one(string="月份",
                            comodel_name="metro_park_maintenance.month")
