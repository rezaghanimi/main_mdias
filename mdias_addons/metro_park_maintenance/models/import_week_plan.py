
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import base64
import xlrd
import pendulum
import logging
import re

_logger = logging.getLogger(__name__)


class ImportWeekPlan(models.Model):
    '''
    导入周计划
    '''
    _name = 'metro_park_maintenance.import_week_plan'

    file = fields.Binary(string='文件')

    @api.multi
    def on_ok_btn_click(self):
        '''
        导入周计划
        :return:
        '''
        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        context = self.env.context
        week_plan_id = context.get('week_plan_id', False)
        record = self.env["metro_park_maintenance.week_plan"]\
            .browse(week_plan_id)

        start_date = pendulum.parse(str(record.start_date))
        end_date = pendulum.parse(str(record.end_date))

        # 根据sheet索引或者名称获取sheet内容
        first_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        rows = []
        for tmp_row in range(0, first_sheet.nrows):
            rows.append(first_sheet.row_values(tmp_row))
        if len(rows) < 5:
            raise exceptions.Warning("数据错误！请检查格式是否正确, 行数至少要大于3")

        # 设备缓存
        devs = self.env["metro_park_maintenance.train_dev"].search([])
        dev_cache = {dev["dev_no"]: dev["id"] for dev in devs}

        # 取得设备行
        dev_names = rows[4][2:]
        for dev_no in dev_names:
            if str(dev_no) not in dev_cache and '1' + str(dev_no) not in dev_cache:
                raise exceptions.ValidationError(
                    "找到未识别的设备名称，请添加设备或修改导入文件{dev_no}".format(dev_no=dev_no))

        # 规程
        rules = self.env["metro_park_maintenance.repair_rule"].search(
            [('target_plan_type', '=', 'week')])
        rule_cache = {rule["no"]: rule for rule in rules}

        # 添加D1 D2等
        keys = list(rule_cache.keys())

        # 根据长度进行排序
        def sort_func(item):
            return len(item)
        keys.sort(key=sort_func, reverse=True)

        vals = []
        for index, tmp_row in enumerate(rows):
            txt = str(tmp_row[0])
            match = re.match(r'(\d{4})年(\d{1,2})月.*?', txt, re.U)
            if match:
                year = int(match.group(1))
                month = int(match.group(2))

                # 读取一个月时间
                days = pendulum.date(year, month, 1).days_in_month
                for day_index in range(1, days + 1):
                    if index + day_index >= len(rows):
                        break

                    cur_row = rows[index + day_index]
                    if cur_row[0] == "":
                        continue

                    day_txt = int(float(str(cur_row[0]).strip()))
                    if day_txt == "":
                        continue

                    if day_txt != day_index:
                        raise exceptions.ValidationError("计划格式不正确, 第一列应为天数")

                    tmp_date = pendulum.datetime(year, month, day_index)
                    if start_date <= tmp_date <= end_date:

                        for dev_col, dev_no in enumerate(dev_names):

                            if dev_no not in dev_cache:
                                dev_no = '1' + dev_no
                            rule_no = cur_row[dev_col + 2].strip()

                            if not rule_no or rule_no == "":
                                continue

                            rule_ids = []
                            if rule_no not in rule_cache:
                                # 最多也就是5个重合，实际上已经不可能出现
                                for i in range(0, 5):
                                    for key in keys:
                                        if key in rule_no or key == rule_no:
                                            # 已经有的就替换掉
                                            rule_ids.append(rule_cache[key].id)
                                            rule_no = rule_no.replace(key, "")
                            else:
                                rule_id = rule_cache[rule_no].id
                                rule_ids.append(rule_id)

                            if len(rule_ids) > 0:
                                _logger.info("找到多个修程!")

                            dev_id = dev_cache.get(dev_no)
                            for rule_id in rule_ids:
                                vals.append({
                                    "dev": dev_id,
                                    "year": year,
                                    "month": month,
                                    "day": day_index,
                                    "date": pendulum.date(year, month, day_index).format('YYYY-MM-DD'),
                                    "rule_type": "normal",
                                    "data_source": "week",
                                    "rule": rule_id,
                                    "plan_id": "metro_park_maintenance.week_plan, {plan_id}".format(
                                        plan_id=week_plan_id)
                                })
        #  创建年计划信息
        if len(vals) > 0:
            # 先删除原有的计划
            old_records = self.env["metro_park_maintenance.rule_info"]\
                .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'
                          .format(plan_id=week_plan_id)), ('rule.target_plan_type', '=', 'week')])
            old_records.write({
                "active": False
            })
            self.env["metro_park_maintenance.rule_info"].create(vals)
        else:
            raise exceptions.ValidationError("没有找到当周数据!")
