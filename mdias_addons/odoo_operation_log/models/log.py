import traceback

import pendulum
from playhouse.shortcuts import model_to_dict
from pytz import timezone

from odoo import models, api, fields
from ..lib.management import LogManage

tz_cn = timezone('Asia/Shanghai')


class LogSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    log_reserve_days = fields.Integer(string='日志保留天数',
                                      config_parameter='odoo_operation_log.log_reserve_days',
                                      default=90)

    def get_values(self):
        res = super(LogSettings, self).get_values()
        res['log_reserve_days'] = int(self.env['ir.config_parameter']
                                      .sudo().get_param('odoo_operation_log.log_reserve_days', default=90))

        return res

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('odoo_operation_log.log_reserve_days', self.log_reserve_days)
        super(LogSettings, self).set_values()


class OperationLog(models.AbstractModel):
    LIMIT = 200

    _name = 'odoo_operation_log.log'

    @api.model
    def get_logs(self, page_num=1, limit=LIMIT, log_type=None, user_login=None, date_range=None):
        records = LogManage.paginate(page_num, limit, log_type=log_type,
                                     user_login=user_login, date_range=date_range)
        return list(map(model_to_dict, records))

    @api.model
    def get_fields_log(self, log_id=None):
        if log_id:
            try:
                records = LogManage.query_field_by_log(log_id)
                return list(map(model_to_dict, records))
            except:
                return []

    @api.model
    def get_logs_info(self, log_type=None, user_login=None, date_range=None):
        try:
            print(log_type, user_login, date_range)
            where = LogManage.where(log_type, user_login, date_range)
            query = LogManage.log.select()
            if where:
                query = query.where(*where)
            result = {
                'sum_count': query.count(),
                'log_types': LogManage.OPERATION_TYPE_MAP
            }
            print(result)
            return result
        except:
            traceback.print_exc()
            return []

    @api.model
    def auto_clear_log(self):
        """
            自动删除大于配置天数的日志
        :return:
        """
        reserve_days = self.env['res.config.settings'].get_values().get('log_reserve_days', 90)
        ahead_date = pendulum.now(tz=tz_cn).subtract(days=reserve_days).strftime(models.DEFAULT_SERVER_DATE_FORMAT)
        log_model = LogManage.log
        logfeild_model = LogManage.logfield
        logs = log_model.select().where(log_model.create_data < ahead_date)
        logfeild_model.delete().where(logfeild_model.log_id.in_(logs)).execute()
        log_model.delete().where(log_model.id.in_(logs)).execute()
