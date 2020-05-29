# -*- coding: utf-8 -*-

import logging
import time
import pytz
import odoo

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

_logger = logging.getLogger(__name__)

# 说明，扩展增加定时任务传参功能

_intervalTypes = {
    'days': lambda interval: relativedelta(days=interval),
    'hours': lambda interval: relativedelta(hours=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'minutes': lambda interval: relativedelta(minutes=interval),
}


class IrCronExtend(models.Model):
    '''
    扩展添加用户数据
    '''
    _inherit = 'ir.cron'

    data = fields.Text(string="user data")

    @api.model
    def _callback(self, cron_name, server_action_id, job_id, job_data = None):
        """ Run the method associated to a given job. It takes care of logging
        and exception handling. Note that the user running the server action
        is the user calling this method. """
        try:
            if self.pool != self.pool.check_signaling():
                # the registry has changed, reload self in the new registry
                self.env.reset()
                self = self.env()[self._name]

            log_depth = (None if _logger.isEnabledFor(logging.DEBUG) else 1)
            odoo.netsvc.log(_logger, logging.DEBUG, 'cron.object.execute', (self._cr.dbname, self._uid, '*', cron_name, server_action_id), depth=log_depth)
            start_time = False
            if _logger.isEnabledFor(logging.DEBUG):
                start_time = time.time()

            self.env['ir.actions.server'].browse(server_action_id).with_context(job_data=job_data).run()

            if start_time and _logger.isEnabledFor(logging.DEBUG):
                end_time = time.time()
                _logger.debug('%.3fs (cron %s, server action %d with uid %d)', end_time - start_time, cron_name, server_action_id, self.env.uid)
            self.pool.signal_changes()
        except Exception as e:
            self.pool.reset_changes()
            _logger.exception("Call from cron %s for server action #%s failed in Job #%s",
                              cron_name, server_action_id, job_id)
            self._handle_callback_exception(cron_name, server_action_id, job_id, e)


    @classmethod
    def _process_job(cls, job_cr, job, cron_cr):
        """ Run a given job taking care of the repetition.

        :param job_cr: cursor to use to execute the job, safe to commit/rollback
        :param job: job to be run (as a dictionary).
        :param cron_cr: cursor holding lock on the cron job row, to use to update the next exec date,
            must not be committed/rolled back!
        """
        try:
            with api.Environment.manage():
                cron = api.Environment(job_cr, job['user_id'], {})[cls._name]
                # Use the user's timezone to compare and compute datetimes,
                # otherwise unexpected results may appear. For instance, adding
                # 1 month in UTC to July 1st at midnight in GMT+2 gives July 30
                # instead of August 1st!
                now = fields.Datetime.context_timestamp(cron, datetime.now())
                nextcall = fields.Datetime.context_timestamp(cron, fields.Datetime.from_string(job['nextcall']))
                numbercall = job['numbercall']

                ok = False
                while nextcall < now and numbercall:
                    if numbercall > 0:
                        numbercall -= 1
                    if not ok or job['doall']:
                        cron._callback(job['cron_name'], job['ir_actions_server_id'], job['id'], job['data'])
                    if numbercall:
                        nextcall += _intervalTypes[job['interval_type']](job['interval_number'])
                    ok = True
                addsql = ''
                if not numbercall:
                    addsql = ', active=False'
                cron_cr.execute("UPDATE ir_cron SET nextcall=%s, numbercall=%s"+addsql+" WHERE id=%s",
                                (fields.Datetime.to_string(nextcall.astimezone(pytz.UTC)), numbercall, job['id']))
                cron.invalidate_cache()

        finally:
            job_cr.commit()
            cron_cr.commit()
