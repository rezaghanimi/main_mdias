# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import xlrd
import base64
import logging
import pendulum
import re

_logger = logging.getLogger(__name__)


class PlanDataImportWizard(models.TransientModel):
    '''
    全年计划数据导入
    '''
    _name = "metro_park_maintenance.year_plan_import_wizard"

    @api.model
    def _get_template_type_domain(self):
        '''
        取得年计划模板类型
        :return:
        '''
        year_plan_template = self.env.ref('metro_park_base.selection_import_by_year_plan_template')
        month_plan_template = self.env.ref('metro_park_base.selection_import_by_month_plan_template')
        return [('id', 'in', [year_plan_template.id, month_plan_template.id])]

    template_type = fields.Many2one(string="导入类型",
                                    comodel_name="metro_park_base.selections",
                                    domain=_get_template_type_domain)
    year_plan_id = fields.Many2one(string="年计划",
                                   comodel_name="metro_park_maintenance.year_plan")
    start_date = fields.Date(string="开始日期", help="开始日期")
    start_date_visible = fields.Boolean(string="开始日期是否显示",
                                        help="用于控制开始日期是否显示",
                                        compute="_compute_month_visible")
    month = fields.Many2one(comodel_name="metro_park_maintenance.month", string="月份")
    month_visible = fields.Boolean(string="月份是否显示",
                                   compute="_compute_month_visible", default=False)
    xls_file = fields.Binary(string='文件', required=True)
    file_name = fields.Char(string='文件名称')

    @api.depends("template_type")
    def _compute_month_visible(self):
        '''
        计算年计划是否显示
        :return:
        '''
        for record in self:
            if record.template_type.value == 'year_plan_template':
                record.month_visible = False
                record.start_date_visible = True
            else:
                record.month_visible = True
                record.start_date_visible = False

    @api.multi
    def import_by_year_template(self):

        # 获取execl中数据
        bin_data = base64.b64decode(self.xls_file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        tmp_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []
        for row in range(0, tmp_sheet.nrows):
            all_data.append(tmp_sheet.row_values(row))
        datas = all_data

        vals = []

        # 取得所有的设备
        dev_model = self.env['metro_park_maintenance.train_dev']
        devs = dev_model.search_read([])
        devs_cache = {dev['dev_no']: dev['id'] for dev in devs}

        # 先一次性的取出所有的规程和所有的设备编码
        dev_index_cache = {}
        dev_no_row = datas[0]
        for row_index, cell in enumerate(dev_no_row):
            if row_index < 3:
                continue

            try:
                dev_no = str(int(cell))
            except Exception as e:
                _logger.info("import error {error}".format(error=e))
                dev_no = cell

            if not dev_no or dev_no == "":
                break

            if dev_no not in devs_cache:
                raise exceptions.ValidationError('没有找到正确的设备, 行数{row}'.format(
                    row=row_index + 2))

            dev_index_cache[row_index] = dev_no

        rule_model = self.env['metro_park_maintenance.repair_rule']
        rules = rule_model.search([])
        rules_cache = {rule['no']: rule['id'] for rule in rules}

        # 限定开始日期
        start_date = pendulum.parse(str(self.start_date))
        start_date = pendulum.date(start_date.year, start_date.month, start_date.day)

        # 设备日期缓存
        date_dev_cache = dict()

        def get_repair_num(tmp_dev_no, tmp_date, tmp_rule_id):
            '''
            取得修次，根据前一天的修程去确定
            :return:
            '''
            tmp_repair_num = 0
            pre_date = tmp_date.subtract(days=1)
            tmp_key = '{dev_no}_{date}'.format(dev_no=tmp_dev_no, date=pre_date.format('YYYY-MM-DD'))
            while tmp_key in date_dev_cache and date_dev_cache[tmp_key] == tmp_rule_id:
                tmp_repair_num = tmp_repair_num + 1
                pre_date = pre_date.subtract(days=1)
                tmp_key = '{dev_no}_{date}'.format(dev_no=tmp_dev_no, date=pre_date.format('YYYY-MM-DD'))
            return tmp_repair_num

        for row_index, row in enumerate(datas):
            if row_index == 0:
                continue

            # 判断是时间戳还是时间
            try:
                date = xlrd.xldate_as_tuple(tmp_sheet.cell_value(row_index, 0), 0)
            except Exception as error:
                _logger.info("the plan is error {error}".format(error=error))
                date = tmp_sheet.cell_value(row_index, 0).split('/')

            date = pendulum.Date(int(date[0]), int(date[1]), int(date[2]))
            if date.year != self.year_plan_id.year:
                continue

            if date < start_date:
                continue

            for col_index, cell in enumerate(row):
                if col_index < 3 or col_index > len(dev_no_row) - 1 \
                        or col_index not in dev_index_cache:
                    continue

                val = dict()
                dev_no = dev_index_cache[col_index]

                key = '{dev_no}_{date}'.format(dev_no=dev_no, date=date.format('YYYY-MM-DD'))
                val['dev'] = devs_cache[dev_no]

                # 没有安排计划
                rule = cell.strip()
                if not rule or rule == '':
                    continue

                if rule not in rules_cache:
                    _logger.info('没有找到对应的规程, 行数{row}名称{rule}'
                                 .format(row=row_index, rule=rule))
                    continue

                date_str = date.format('YYYY-MM-DD')
                rule_id = rules_cache[rule.upper()]
                val['rule'] = rule_id
                val['date'] = date_str
                val['rule_type'] = 'normal'
                val['data_source'] = 'year'
                val['state'] = 'published'
                val['repair_num'] = get_repair_num(dev_no, date, rule_id)
                val['plan_id'] = 'metro_park_maintenance.year_plan, {plan_id}' \
                    .format(plan_id=self.year_plan_id.id)
                vals.append(val)
                date_dev_cache[key] = rule_id

        # 删除原有的计划数据
        records = self.env["metro_park_maintenance.rule_info"].search(
            [("plan_id", "=", "metro_park_maintenance.year_plan, {plan_id}"
              .format(plan_id=self.year_plan_id.id))])
        records.write({
            "active": False
        })

        # 自身会创建对应的日计划信息
        self.env["metro_park_maintenance.rule_info"].create(vals)

    @api.model
    def import_by_month_template(self):
        '''
        通过月计划模板导入
        :return:
        '''
        # 获取execl中数据
        bin_data = base64.b64decode(self.xls_file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        plan_year = self.year_plan_id.year
        plan_month = self.month.val

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
        rules = self.env["metro_park_maintenance.repair_rule"].search(
            [('target_plan_type', 'in', ['year'])])
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
                        '第{row}行{col}列规程{rule}无法找到!'.format(
                            row=index + 1, col=day, rule=rule_no))
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
                    "data_source": "year",
                    "rule": rule_id,
                    "plan_id": "metro_park_maintenance.year_plan, {plan_id}".format(
                        plan_id=self.year_plan_id.id)
                })

        # 删除老的数据
        old_records = self.env["metro_park_maintenance.rule_info"].search(
            [("plan_id", "=", "metro_park_maintenance.year_plan, {plan_id}".format(
                plan_id=self.year_plan_id.id)), ('month', '=', plan_month)])
        old_records.write({
            "active": False
        })
        self.env["metro_park_maintenance.rule_info"].create(datas)

    @api.multi
    def import_by_month_work_template(self):
        '''
        能过月生产计划模板导入
        :return:
        '''
        pass

    @api.multi
    def on_click(self):
        '''
        确定按扭点击
        :return:
        '''
        if self.template_type.value == 'year_plan_template':
            self.import_by_year_template()
        elif self.template_type.value == 'month_plan_template':
            self.import_by_month_template()

