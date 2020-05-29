# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class VehicleHistoryDelete(models.TransientModel):
    _name = 'maintenance.vehicle.history.delete'
    _description = '批量删除'
    _rec_name = 'start_date'
    
    delete_type = fields.Selection(string="删除类型", selection=[('dev', '按车辆设备'), ('date', '按起止日期'), ('all', '两者皆是')],
                                   required=True, default='dev')
    train_dev_ids = fields.Many2many("metro_park_maintenance.train_dev",
                                     relation="vehicle_train_dev_delete_rel", string="设备")
    start_date = fields.Date(string="起始日期", default=fields.Date.context_today)
    end_date = fields.Date(string="截止日期", default=fields.Date.context_today)

    @api.multi
    def delete_vehicle_data(self):
        """
        批量删除车辆历史公里数记录
        :return:
        """
        self.ensure_one()
        if self.delete_type == 'dev':
            if len(self.train_dev_ids) > 1:
                tuple_train = tuple(self.train_dev_ids.ids)
                sql = "delete from funenc_tcms_vehicle_data where train_dev_id in {numpy_train}".format(numpy_train=tuple_train)
            else:
                numpy_train = self.train_dev_ids.id
                sql = "delete from funenc_tcms_vehicle_data where train_dev_id={}".format(numpy_train)
        elif self.delete_type == 'date':
            sql = "delete from funenc_tcms_vehicle_data where date>='{start_date}' and date <='{end_date}'".\
                format(start_date=str(self.start_date), end_date=str(self.end_date))
        elif self.delete_type == 'all':
            if len(self.train_dev_ids) > 1:
                tuple_train = tuple(self.train_dev_ids.ids)
                sql = "delete from funenc_tcms_vehicle_data where date>='{start_date}' and date <='{end_date}' and train_dev_id in {numpy_train}".format(
                    start_date=str(self.start_date), end_date=str(self.end_date), numpy_train=tuple_train
                )
            else:
                numpy_train = self.train_dev_ids.id
                sql = "delete from funenc_tcms_vehicle_data where date>='{start_date}' and date <='{end_date}' and train_dev_id={numpy_train}".format(
                    start_date=str(self.start_date), end_date=str(self.end_date), numpy_train=numpy_train
                )
        else:
            raise UserError("请选择批量删除的类型！")
        self._cr.execute(sql)
        return {'type': 'ir.actions.act_window_close'}
