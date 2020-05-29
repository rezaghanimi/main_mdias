# -*- coding: utf-8 -*-

import hashlib

import pendulum

from odoo import models, fields, api


class TimeTableData(models.Model):
    '''
    时刻表数据
    '''
    _name = 'metro_park_base.time_table_data'
    _description = '时刻表数据'
    _track_log = True

    sequence = fields.Integer(string="出车序号")
    time_table_id = fields.Many2one(string="所属时刻表",
                                    comodel_name='metro_park_base.time_table',
                                    ondelete="cascade")
    train_no = fields.Char(string='车次', required=True)

    out_location = fields.Many2one(string='出场场段',
                                   comodel_name='metro_park_base.location', required=True)
    back_location = fields.Many2one(string='入场场段',
                                    comodel_name='metro_park_base.location')

    plan_in_time = fields.Datetime(string='计划回库时间')
    plan_out_time = fields.Datetime(string='计划出库时间')

    plan_in_val = fields.Integer(string="计划回库数值(分钟)",
                                 compute="_compute_vals", help="用于排计划, 便于比较")
    plan_out_val = fields.Integer(string="计划出库数值(分钟)",
                                  compute="_compute_vals", help="用于排计划, 便于比较")

    # 高峰车回去以后还要以安排检修
    high_time_train = fields.Boolean(string='高峰时段')
    miles = fields.Float(string="周转公里数")
    md5_str = fields.Char(string="MD5值")

    @api.one
    @api.depends('plan_in_time', 'plan_out_time')
    def _compute_vals(self):
        '''
        将时间转换为数值便于进行计算
        :return:
        '''
        if self.plan_in_time and self.plan_out_time:
            in_time = pendulum.parse(str(self.plan_in_time)).add(hours=8)
            out_time = pendulum.parse(str(self.plan_out_time)).add(hours=8)
            if in_time.day > out_time.day:
                self.plan_in_val = (in_time.hour + 24) * 60 + in_time.minute
            else:
                self.plan_in_val = in_time.hour * 60 + in_time.minute

            if out_time.hour < 2:
                raise
            else:
                self.plan_out_val = out_time.hour * 60 + out_time.minute

    @api.multi
    def name_get(self):
        result = []
        name = self._rec_name
        if name in self._fields:
            convert = self._fields[name].convert_to_display_name
            for record in self:
                result.append((record.id, convert(record[name], record)))
        else:
            for record in self:
                start_time = str(record.plan_out_time).split(" ")[1].split(".")[0]
                end_time = str(record.plan_in_time).split(" ")[1].split(".")[0]
                result.append((record.id, "车次：%s,时间：%s" % (record.train_no, start_time + "-" + end_time)))

        return result

    @classmethod
    def _val_to_md5(cls, val):
        md5 = hashlib.md5()
        md5.update(str(val).encode('utf-8'))
        return md5.hexdigest()

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, values):
        ids = []
        for val in values:
            md5 = self._val_to_md5(val)
            record = self.search([('md5_str', '=', md5)])
            if not record:
                val['md5_str'] = md5
                record = super(TimeTableData, self).create(val)
            ids.append(record.id)
        return self.browse(ids)

