# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class VehicleHistoryAdd(models.TransientModel):
    _name = 'maintenance.vehicle.history.add'
    _description = '车辆公里数录入'
    _rec_name = 'date'

    train_dev_ids = fields.Many2many("metro_park_maintenance.train_dev", relation="vehicle_train_dev_add_rel", string="设备")
    date = fields.Date(string="录入日期", required=True, default=fields.Date.context_today)
    today_mileage = fields.Float(string="当日里程")
    total_mileage = fields.Float(string="公里数")
    traction_consumption = fields.Float(string="牵引能耗")
    auxiliary_consumption = fields.Float(string="辅助能耗")
    regeneration_consumption = fields.Float(string="再生能耗")

    @api.multi
    def add_vehicle_data(self):
        """
        录入车辆公里数
        :return:
        """
        self.ensure_one()
        if len(self.train_dev_ids.ids) > 1:
            tuple_train = tuple(self.train_dev_ids.ids)
            sql = """delete from funenc_tcms_vehicle_data where date='{date}' and train_dev_id in {numpy_train}""".format(date=str(self.date), numpy_train=tuple_train)
        else:
            numpy_train = self.train_dev_ids.id
            sql = """delete from funenc_tcms_vehicle_data where date='{date}' and train_dev_id={numpy_train}""".format(date=str(self.date), numpy_train=numpy_train)
        self._cr.execute(sql)
        data_list = list()
        now_time = fields.datetime.now()
        for train_dev in self.train_dev_ids:
            data_list.append({
                'name': train_dev.dev_no,
                'update_time': now_time,
                'today_mileage': self.today_mileage,
                'total_mileage': self.total_mileage,
                'traction_consumption': self.traction_consumption,
                'auxiliary_consumption': self.auxiliary_consumption,
                'regeneration_consumption': self.regeneration_consumption,
            })
        self.env['funenc.tcms.vehicle.data'].create(data_list)
        return {'type': 'ir.actions.act_window_close'}
