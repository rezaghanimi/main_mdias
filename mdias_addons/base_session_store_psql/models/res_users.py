# !user/bin/env python3
# -*- coding: utf-8 -*-
# Author: Artorias
from odoo import models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def clear_session_store(self):
        cr = self.env.cr
        cr.execute(
            """DELETE FROM sessionstore WHERE uid is NULL""")
