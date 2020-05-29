
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging

_logger = logging.getLogger(__name__)


class BalanceRuleOffset(models.Model):
    '''
    修程偏移, 这个是记录初始的偏移，这里实际上是个修次管理
    '''
    _name = 'metro_park_maintenance.balance_rule_offset'

    dev = fields.Many2one(string='设备',
                          comodel_name='metro_park_maintenance.train_dev')

    year = fields.Many2one(string='年',
                           comodel_name="metro_park_maintenance.year",
                           required=True,
                           help="起始年份")

    month = fields.Many2one(string='月',
                            comodel_name="metro_park_maintenance.month",
                            required=True,
                            help="起始月份")

    @api.model
    def _get_default_offset(self):
        '''
        取得默认修次
        :return:
        '''
        record = self.env["metro_park_maintenance.plan_config_data"]\
            .search([], limit=1, order="index asc")
        return record.id

    offset_num = fields.Integer(string='修次', default=0)
    offset = fields.Many2one(string='修次',
                             comodel_name="metro_park_maintenance.plan_config_data",
                             compute="_compute_offset")

    rule = fields.Many2one(string="规程",
                           comodel_name="metro_park_maintenance.repair_rule",
                           compute="_compute_rule")

    @api.model
    def get_offset_cache(self):
        '''
        取得设备的偏移缓存, 使用设备id作为key
        :return:
        '''
        records = self.search([])
        return {record.dev.id: record for record in records}

    @api.depends('year', 'month')
    def _compute_rule(self):
        '''
        计算当月的规程
        :return:
        '''
        model = self.env["metro_park_maintenance.plan_config_data"]
        config_data = model.search([], order="index asc")
        config_cache = {config.index: config.rule.id for config in config_data}

        for record in self:
            offset = record.offset_num or 0
            if offset not in config_cache:
                continue
            else:
                record.rule = config_cache[offset % len(config_data)]

    @api.depends("offset_num")
    def _compute_offset(self):
        '''
        计算偏移到的项
        :return:
        '''
        model = self.env["metro_park_maintenance.plan_config_data"]
        config_data = model.search([], order="index asc")
        config_cache = {config.index: config.id for config in config_data}

        for record in self:
            offset = record.offset_num or 0
            if offset not in config_cache:
                continue
            else:
                record.rule = config_cache[offset % len(config_data)]

    @api.model
    def init_balance_offset(self):
        '''
        初始化修程偏移，这里只是刷新没有添加的设备
        :return:
        '''
        records = self.search([])
        old_train_ids = records.mapped("dev.id")

        months = self.env["metro_park_maintenance.month"].search([])
        months_cache = {month.val: month.id for month in months}

        years = self.env["metro_park_maintenance.year"].search([])
        year_cache = {year.val: year.id for year in years}

        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"]\
            .search([('dev_type', '=', dev_type_electric_train.id)])

        today = pendulum.today("UTC")
        datas = []
        for index, dev in enumerate(devs):
            if dev.id not in old_train_ids:
                datas.append({
                    "dev": dev.id,
                    "year": year_cache[today.year],
                    "month": months_cache[today.month],
                    "offset": 0
                })
        self.create(datas)

    @api.model
    def get_month_info(self, year, month):
        '''
        取得月份应当进行的计划
        :return:
        '''
        config_datas = self.env["metro_park_maintenance.plan_config_data"]\
            .search([], order="index asc")

        # 有修次信息的设备
        records = self.search([])
        rst = {}
        target = pendulum.date(year, month, 1)
        for record in records:
            offset_month = pendulum.Date(record.year, record.month, 1)
            delta = target - offset_month
            delta_month = delta.months
            offset_num = (record.offset_num + delta_month) % len(config_datas)
            rst[record.dev.id] = {
                "offset_num": offset_num,
                "year": record.year,
                "month": record.month
            }

        # 没有设置则默认进行第一个修程
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"]\
            .search([('dev_type', '=', dev_type_electric_train.id)])
        for dev in devs:
            if dev.id not in rst:
                rst[dev.id] = {
                    "offset": 0,
                    "year": year,
                    "month": month
                }

        return rst

    @api.multi
    def set_offset(self):
        '''
        设置修次
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.balance_offset_wizard",
            'view_mode': 'form',
            "target": "new",
            'context': {
                'dev_id': self.dev.id,
                'default_year': self.year.id,
                'default_month': self.month.id
            },
            "views": [[self.env.ref(
                'metro_park_maintenance.balance_offset_wizard_form').id, "form"]]
        }

    @api.model
    def update_balance_offset_year_month(self, year, month):
        '''
        更新修次时间
        :param year:
        :param month:
        :return:
        '''
        year_id = self.env["metro_park_maintenance.year"].search([('val', '=', year)]).id
        month_id = self.env["metro_park_maintenance.month"].search([('val', '=', month)]).id

        target_date = pendulum.date(year, month, 1)
        model = self.env["metro_park_maintenance.plan_config_data"]
        config_datas = model.search([], order="index asc")
        offsets = self.search([])
        for record in offsets:
            tmp_date = pendulum.date(record.year.val, record.month.val, 1)
            # 倒回去的情况
            if tmp_date > target_date:
                delta_month = self.get_delta_month(target_date, tmp_date)
                old_index = record.offset_num
                index = old_index - delta_month
                while index < 0:
                    index += len(config_datas)
                record.offset_num = index
            else:
                delta_month = self.get_delta_month(tmp_date, target_date)
                old_index = record.offset_num
                index = old_index + delta_month
                while index > len(config_datas):
                    index -= len(config_datas)
                record.offset_num = index

            record.year = year_id
            record.month = month_id

    @api.model
    def get_delta_month(self, start, end):
        '''
        取得两个时间相关的月份, pendulum中的delta的month是不对的
        :return:
        '''
        if end < start:
            raise exceptions.ValidationError('开始时间不能小于结束时间')

        start_year = start.year
        start_month = start.month

        end_year = end.year
        end_month = end.month

        if end_year > start_year:
            delta = 12 - start_month + 1
            delta += (end_year - start_year - 1) * 12
            delta += end_month
        else:
            delta = end_month - start_month

        return delta

    @api.model
    def syn_to_repair(self):
        '''
        同步到检修, 按时间排倒序的最后一个
        :return:
        '''
        records = self.search([])
        for record in records:
            year = record.year.val
            month = record.month.val
            rule_infos = self.env["metro_park_maintenance.rule_info"].search(
                [('year', '=', year),
                 ('month', '=', month),
                 ('dev', '=', record.dev.id),
                 ('data_source', '=', 'year')], order='date desc')
            if rule_infos:
                rule_info = rule_infos[0]
                rule_info.repair_num = record.offset_num

    @api.model
    def syn_from_repair(self, year, month):
        '''
        从检修同步
        :return:
        '''
        records = self.search([])
        tmp_cache = {record.dev.id: record for record in records}
        start_date = pendulum.date(year, month, 1)
        history_plans = self.env['metro_park_maintenance.rule_info'] \
            .get_year_plan_history_info(start_date.format('YYYY-MM-DD'))
        history_plan_cache = {plan.dev.id: plan for plan in history_plans}
        for dev_id in history_plan_cache:
            tmp_cache[dev_id].offset_num = history_plan_cache[dev_id].repair_num

    @api.model
    def import_offset(self):
        '''
        导入偏移
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.import_offset_wizard",
            'view_mode': 'form',
            "target": "new",
            'context': {},
            "views": [[
                self.env.ref(
                    'metro_park_maintenance.import_offset_wizard_form').id, "form"]]
        }

    @api.model
    def export_offset(self):
        '''
        导出偏移
        :return:
        '''
        return {
           'type': 'ir.actions.act_url',
           'url': '/export_balance_offset',
           'target': 'self',
           'res_id': self.id
        }








