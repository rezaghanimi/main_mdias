
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import pendulum


class TrainMilesSetWizard(models.TransientModel):
    '''
    公里数录入
    '''
    _name = 'metro_park_maintenance.train_miles_set_wizard'
    _description = '公里数录入向导'
    
    train_dev_id = fields.Many2many(string='设备',
                                    comodel_name='metro_park_maintenance.train_dev',
                                    required=True,
                                    relation='set_mile_train_dev',
                                    column1='mile_id',
                                    column2='dev_id')
    miles = fields.Float(string='里程')
    year_target_miles = fields.Float(string="年度目标公里数")
    remark = fields.Char(string='备注')

    @api.multi
    def on_ok(self):
        '''
        设置公里数
        :return:
        '''
        model = self.env['metro_park_maintenance.train_dev']
        for train in self.train_dev_id:
            record = model.browse(train.id)
            old_miles = record.miles
            record.miles = self.miles
            record_mode = self.env['metro_park_maintenance.operation_record']
            #
            tm = pendulum.now()
            date = tm.format('YYYY/MM/DD')
            lens = len(self.env['metro_park_maintenance.operation_record']
                       .search([('tm', '=', date)]))
            if lens > 100:
                num = str(lens + 1)
            elif lens > 10:
                num = '0' + str(lens + 1)
            else:
                num = '00' + str(lens + 1)
            record_num = tm.format('YYYYMMDD') + num
            record_mode.create({
                'record_no': record_num,
                'tm': date,
                'manipulate_type': 'manual',
                'train': self.train_dev_id.id,
                'last_miles': old_miles,
                'cur_miles': self.miles,
                'inc_miles': self.miles - old_miles,
                'ip_address': request.httprequest.environ['REMOTE_ADDR']
            })

    @api.multi
    def on_click(self):
        """
        设置预估公里数的年度目标
        :return:
        """
        year = pendulum.now().year
        month = pendulum.now().month

        # 应当是当月和当月以后
        for tmp_month in range(month, 13):
            self.env["metro_park_maintenance.history_miles"].check_dev(year, tmp_month)

        for train in self.train_dev_id:
            history_miles = self.env['metro_park_maintenance.history_miles']\
                .search([('train_dev', '=', train.id),
                         ('year', '=', year)], order="month asc")
            for history_mile in history_miles:
                # 这里会触发重新计算
                history_mile.year_target_miles = self.year_target_miles
