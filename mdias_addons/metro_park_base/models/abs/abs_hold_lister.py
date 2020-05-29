# -*- coding: utf-8 -*-

import datetime
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HoldListener(models.AbstractModel):
    # 占压状态发生变化记录变化时间
    _name = 'metro_park_base.abs_hold_lister'

    hold_write = fields.Datetime(default=lambda self: datetime.datetime.now())

    @api.multi
    def write(self, vals):
        if 'hold' in vals:
            hold = vals['hold']
            for re in self:
                old_hold = re.hold
                if hold != old_hold:
                    _logger.info('TRAIN TRACK %s 占压发生变化,更新占压时间,<New %s, Old %s>' % (re.name, hold, old_hold))
                    value = dict(vals, hold_write=datetime.datetime.now())
                    super(HoldListener, re).write(value)
            return self
        else:
            return super(HoldListener, self).write(vals)
