
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MileRepairHistory(models.Model):
    '''
    里程修信息
    '''
    _name = 'metro_park_maintenance.mile_repair_history'
    
    remark = fields.Text(string='备注')
    dev = fields.Many2one(string='设备',
                          comodel_name='metro_park_maintenance.train_dev')
    date = fields.Date(string='日期')
    miles = fields.Float(string='公里数')

    @api.model
    def get_history_mile_info(self, date_str):
        '''
        取得上次里程修信息
        :return:
        '''
        sql = 'select distinct on(dev) dev, date, id from metro_park_maintenance_mile_repair_history' \
              ' where date < \'{date}\' order by dev, date desc'.format(date=date_str)
        self.env.cr.execute(sql)
        ids = [x[2] for x in self.env.cr.fetchall()]
        records = self.env["metro_park_maintenance.rule_info"].browse(ids)
        return records

