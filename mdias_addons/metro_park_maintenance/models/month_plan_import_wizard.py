# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import xlrd
import base64
import re
import pendulum
import datetime
import time
import logging

_logger = logging.getLogger(__name__)


class MonthPlanImportWizard(models.TransientModel):
    '''
    月计划导入向导
    '''
    _name = 'metro_park_maintenance.month_plan_import_wizard'

    remark = fields.Text(string='备注')
    file = fields.Binary(string='文件')

    @api.multi
    def on_ok_btn_clicked(self):
        '''
        确认按扭点击
        :return:
        '''
        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        context = self.env.context
        month_plan_id = context.get('month_plan_id', False)
        record = self.env["metro_park_maintenance.month_plan"] \
            .browse(month_plan_id)
        plan_year = record.year
        plan_month = record.month

        start_date = pendulum.date(plan_year, plan_month, 1)

        # 根据sheet索引或者名称获取sheet内容
        sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
        rows = []
        for row in range(0, sheet2.nrows):
            rows.append(sheet2.row_values(row))
        if len(rows) < 3:
            raise exceptions.Warning("数据错误！请检查格式是否正确")

        title = rows[0][1] if rows[0][1] and rows[0][1] != '' else rows[0][0]
        match = re.match(r'(\d{4})年(\d{1,2})月.*?', title, re.U)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
        else:
            raise exceptions.ValidationError("无法找到年月标识，请检查文件是否正确!")

        if year != plan_year or month != plan_month:
            raise exceptions.ValidationError("年或月与计划不匹配！")

        # 规程
        rules = self.env["metro_park_maintenance.repair_rule"].search([])
        rule_cache = {rule["no"]: rule["id"] for rule in rules}

        # 设备缓存
        devs = self.env["metro_park_maintenance.train_dev"].search([])
        dev_cache = {dev["dev_no"]: dev["id"] for dev in devs}

        datas = []
        rows = rows[3:]
        for index, row in enumerate(rows):
            train_no = row[0].strip()
            if train_no == '备注' or train_no == "":
                break

            # 暂时没有考虑多个分隔的情况
            for day in range(1, start_date.days_in_month + 1):
                rule_no = row[day].strip()
                if not rule_no or rule_no == "":
                    continue
                rule_id = rule_cache.get(rule_no, False)
                if not rule_id:
                    raise exceptions.ValidationError(
                        '第{row}行{col}列规程{rule}无法找到!'.format(row=index + 1, col=day, rule=rule_no))
                dev_no = row[0].strip()
                if dev_no not in dev_cache:
                    raise exceptions.ValidationError("车辆没有找到, 请先在设备管理中添加车辆!")

                dev_id = dev_cache.get(dev_no)
                datas.append({
                    "dev": dev_id,
                    "year": year,
                    "month": month,
                    "day": day,
                    "date": pendulum.date(year, month, day).format('YYYY-MM-DD'),
                    "rule_type": "normal",
                    "data_source": "month",
                    "rule": rule_id,
                    "plan_id": "metro_park_maintenance.month_plan, {plan_id}".format(plan_id=month_plan_id)
                })

        # 删除老的数据
        old_records = self.env["metro_park_maintenance.rule_info"].search(
            [("plan_id", "=", "metro_park_maintenance.month_plan, {plan_id}".format(
                plan_id=month_plan_id))])
        old_records.write({"active": False})
        self.env["metro_park_maintenance.rule_info"].create(datas)

    @api.multi
    def view_month_plan_works_import(self):
        month_id = self._context.get('active_id')
        year_date = self.env['metro_park_maintenance.month_plan'].search([('id', '=', month_id)]).year
        month_date = self.env['metro_park_maintenance.month_plan'].search([('id', '=', month_id)]).month
        if len(str(month_date)) == 1:
            month_date = '0' + str(month_date)
        year_month = '{}年{}月'.format(str(year_date), str(month_date))
        data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=data)
        all_data = []
        sheet = workbook.sheet_by_index(0)
        for row in range(0, sheet.nrows):
            all_data.append(sheet.row_values(row))
        create_list = []
        for key, rec in enumerate(all_data):
            try:
                if '年' in rec[0] and '月' in rec[0] and len(rec[0]) < 11:
                    try:
                        year = rec[0] if int(rec[0][5:7]) else ''
                    except Exception:
                        # 处理年的格式
                        _logger.error('月计划导入格式内部数据不符合')
                        year = rec[0][:5] + '0' + rec[0][5:]
                    self.deal_excel_plan_works_import(rec, year, year_month)
            except Exception:
                try:
                    self.deal_excel_plan_works_import(rec, year, year_month)
                except Exception:
                    # 处理错误的格式
                    _logger.error('月计划导入格式内部数据不符合')
        self.env['metro_park_maintenance.rule_info'].create(create_list)

    @api.multi
    def deal_excel_plan_works_import(self, rec, year, month_rec_date):
        create_list = []
        date = rec[0]
        for rule_row, rule in enumerate(rec):
            try:
                # 获取当前是哪个车辆
                if type(rule) is str and rule:
                    dev_no = rule_row + 10999
                    dev_id = self.env['metro_park_maintenance.train_dev'].search([('dev_name', '=', dev_no)])
                    # 获取当前修程的no
                    if len(rule) > 1:
                        # 切割
                        rule_split_rec = re.split('(D\d)', rule)
                        if len(rule_split_rec) == 1:
                            for many_rule in rule_split_rec[0]:
                                many_no_rec = self.env['metro_park_maintenance.repair_rule'].search(
                                    [('no', '=', many_rule)])
                                if dev_id and many_no_rec:
                                    if month_rec_date == year:
                                        create_list.append({
                                            'date': str(date_type_time)[:10],
                                            'dev': dev_id.id,
                                            'data_source': 'month',
                                            'plan_id': 'metro_park_maintenance.month_plan, {}'.format(
                                                self._context.get("active_id")),
                                            'rule': many_no_rec.id,
                                        })
                        else:
                            # 一个空格有多个修程
                            for many_many_rule in rule_split_rec:
                                if many_many_rule in ['D1', 'D2', 'D3', 'D4']:
                                    many_many_rule_d = self.env['metro_park_maintenance.repair_rule'].search(
                                        [('no', '=', many_many_rule)])
                                    if month_rec_date == year:
                                        create_list.append({
                                            'date': str(date_type_time)[:10],
                                            'dev': dev_id.id,
                                            'data_source': 'month',
                                            'plan_id': 'metro_park_maintenance.month_plan, {}'.format(
                                                self._context.get("active_id")),
                                            'rule': many_many_rule_d.id,
                                        })
                                else:
                                    # 当前空格内没有地板卫生
                                    for no_many_rule_d in many_many_rule:
                                        many_no_rec = self.env['metro_park_maintenance.repair_rule'].search(
                                            [('no', '=', no_many_rule_d)])
                                        if dev_id and many_no_rec:
                                            if month_rec_date == year:
                                                create_list.append({
                                                    'date': str(date_type_time)[:10],
                                                    'dev': dev_id.id,
                                                    'data_source': 'month',
                                                    'plan_id': 'metro_park_maintenance.month_plan, {}'.format(
                                                        self._context.get("active_id")),
                                                    'rule': many_no_rec.id,
                                                })

                    no_rec = self.env['metro_park_maintenance.repair_rule'].search([('no', '=', rule)])
                    if dev_id and no_rec:
                        date_time = year + str(int(date)) + '日' if float(date) > 10 else year + '0' + str(
                            int(date)) + '日'
                        date_type_time = datetime.datetime.strptime(
                            date_time.replace('年', '-').replace('月', '-').replace('日', ''), '%Y-%m-%d')
                        if month_rec_date == year:
                            create_list.append({
                                'date': str(date_type_time)[:10],
                                'dev': dev_id.id,
                                'data_source': 'month',
                                'plan_id': 'metro_park_maintenance.month_plan, {}'.format(
                                    self._context.get("active_id")),
                                'rule': no_rec.id,
                            })
            # 取消对应的数据
            except Exception:
                _logger.error('月计划导入格式内部数据不符合')
        self.env['metro_park_maintenance.rule_info'].create(create_list)
