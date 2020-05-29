
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import xlrd
import pendulum


class ImportProduceWorkClass(models.Model):
    '''
    导生生产说明
    '''
    _name = 'metro_park_base.import_produce_work_class'

    month_plan = fields.Many2one(
        comodel_name='metro_park_maintenance.month_plan',
        string="月计划")
    file = fields.Binary(string='文件')

    @api.multi
    def on_ok(self):
        '''
        导入生产说明
        :return:
        '''

        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        tmp_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []

        # 不要第一行, 前边两行不要，一行是标题栏, 一行是表格头
        for row in range(1, tmp_sheet.nrows):
            all_data.append(tmp_sheet.row_values(row))
        datas = all_data[2:]

        # 所得所有的修程
        rules = self.env["metro_park_maintenance.repair_rule"].search(
            [('target_plan_type', 'in', ['year', 'month'])])
        rule_no_array = rules.mapped("no")

        # 取得所有的车号
        devs = self.env["metro_park_maintenance.train_dev"].search([])
        dev_no_ar = devs.mapped('dev_no')

        # 取得本月的所有rule
        rule_infos = self.env["metro_park_maintenance.rule_info"].search(
            [('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                plan_id=self.month_plan.id))])
        rule_info_cache = {}
        for rule_info in rule_infos:
            rule_info_cache["{dev_no}_{date}_{rule_no}".format(
                dev_no=rule_info.dev_no,
                date=rule_info.date,
                rule_no=rule_info.rule.no)] = rule_info

        property_balance_id = self.env.ref(
            "metro_park_base.department_property_balance_work_class").id
        work_classes = self.env["funenc.wechat.department"].search(
            [('properties', 'in', [property_balance_id])])
        work_class_cache = {}
        for work_class in work_classes:
            work_class_cache[work_class.work_master] = work_class.id

        year = self.month_plan.year
        month = self.month_plan.month

        # 处理具体数据
        for row in datas:
            cell_text = row[0] or ''
            if cell_text in dev_no_ar:
                dev_no = None
                for day, txt in enumerate(row):
                    if day == 0:
                        dev_no = txt
                        continue

                    if txt and txt != '':
                        rule_no = txt[:2]
                        if rule_no in rule_no_array:
                            class_master = txt[2]
                        else:
                            rule_no = txt[0]
                            class_master = txt[1]

                        tmp_date = pendulum.date(year, month, day)
                        key = '{dev_no}_{date}_{rule_no}'.format(
                            dev_no=dev_no,
                            date=tmp_date.format('YYYY-MM-DD'), rule_no=rule_no)
                        if key in rule_info_cache and class_master in work_class_cache:
                            rule_info = rule_info_cache[key]
                            rule_info.work_class = [(6, 0, [work_class_cache[class_master]])]



