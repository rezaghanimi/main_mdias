# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

from . import util
import pendulum
import logging

_logger = logging.getLogger(__name__)


class WeekPlan(models.Model):
    '''
    周计划只是展示一个开始和一个结束的数据, 不添加新的内容，
    要添加新的内容统一到月计划里面进行
    '''
    _name = 'metro_park_maintenance.week_plan'
    _description = '周计划'
    _rec_name = 'plan_name'
    _track_log = True
    _order = "year desc, week desc"

    def _get_default_sequence(self):
        '''
        默认序号
        :return:
        '''
        return self.env['ir.sequence'] \
            .next_by_code('week.plan.number')

    plan_name = fields.Char(string="名称", required=True)
    month_plan_id = fields.Many2one(string="月计划",
                                    comodel_name="metro_park_maintenance.month_plan")

    start_date = fields.Date(string="开始日期",
                             compute="_compute_date", store=True)

    end_date = fields.Date(string="结束日期",
                           compute="_compute_date", store=True)

    year = fields.Integer(string="年")
    week = fields.Integer(string="周")

    start_month = fields.Integer(string="开始月份", compute="_compute_info", store=True)
    end_month = fields.Integer(string="结束月份", compute="_compute_info", store=True)
    start_year = fields.Integer(string="开始年份", compute="_compute_info", store=True)
    end_year = fields.Integer(string="结束年份", compute="_compute_info", store=True)

    operation_buttons = fields.Char(string='操作')
    sequence_no = fields.Char(string='序号', default=_get_default_sequence)

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布')],
                             default='draft')
    active = fields.Boolean(default=True)
    remark = fields.Char(string='备注')

    pms_work_class_info = fields.Many2one(comodel_name='pms.department',
                                          string='工班')

    mile_work_class_info = fields.One2many(
        comodel_name="metro_park_maintenance.week_work_class_info",
        inverse_name="week_plan_id",
        string="里程修工班信息")

    @api.one
    @api.constrains('year', 'week')
    def _check_description(self):
        '''
        由于使用了假删除，所以只能通过代码进行限制
        :return:
        '''
        if self.year and self.week:
            record = self.search(
                [("year", "=", self.year), ("week", "=", self.week), ('id', '!=', self.id)])
            if record:
                raise exceptions.Warning("此周计划已经存在")

    @api.one
    @api.constrains('plan_name')
    def _check_plan_name(self):
        if self.plan_name:
            record = self.search([('plan_name', '=', self.plan_name), ('id', '!=', self.id)])
            if record:
                return exceptions.ValidationError('计划名称重复! 请使用其它名称!')

    @api.depends('year', 'week')
    def _compute_date(self):
        '''
        :return:这里需要测试是否正确
        '''
        for record in self:
            if record.year and record.week:
                start_date, end_date = \
                    util.get_week_date_range(record.year, record.week)
                record.start_date = start_date.format("YYYY-MM-DD")
                record.end_date = end_date.format("YYYY-MM-DD")
            else:
                record.start_date = None
                record.end_date = None

    @api.depends('year', 'week')
    def _compute_info(self):
        '''
        计算相关信息，便于查询
        :return:
        '''
        for record in self:
            year = record.year
            start_of_year = pendulum.date(year, 1, 1)
            start_of_week = start_of_year.subtract(days=(start_of_year.day_of_week - 1))
            target_week = start_of_week.add(weeks=self.week - 1)
            record.start_month = target_week.month
            record.start_year = start_of_week.year
            assert target_week.week_of_year == record.week
            target_end_week = target_week.add(weeks=1).subtract(days=1)
            record.end_month = target_end_week.month
            record.end_year = target_end_week.year
            assert target_end_week.year == record.year and target_end_week.week_of_year == record.week

    @api.multi
    def del_plan(self):
        '''
        删除计划
        :return:
        '''
        self.unlink()

    @api.multi
    def import_week_plan(self):
        '''
        导入周计划
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.import_week_plan",
            'view_mode': 'form',
            "target": 'new',
            'context': {
                'week_plan_id': self.id,
            },
            "views": [[self.env.ref(
                'metro_park_maintenance.import_week_plan_form').id, "form"]]
        }

    @api.multi
    def unlink(self):
        '''
        必需要日计划删除完成以后才能删除周计划
        :return:
        '''
        for record in self:
            start_date = record.start_date
            end_date = record.end_date
            records = self.env["metro_park_maintenance.day_plan"] \
                .search([('plan_date', '>=', start_date), ('plan_date', '<=', end_date)])
            if len(records) > 0:
                raise exceptions.ValidationError(
                    "{week}还有相应的计划没有删除".format(week=record.week))

        # 删除计划数据
        for record in self:
            # 先删除具体信息
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([('date', '>=', record.start_date),
                         ('date', '<=', record.end_date),
                         ('data_source', '=', 'week')])
            records.write({
                "active": False
            })

            # 对应用很多设备, 只有具体信息删除完了以后才删除计划数据
            records = self.env["metro_park_maintenance.plan_data"] \
                .search([("date", '>=', record.start_date),
                         ("date", "<=", record.end_date),
                         ("plan_id", '=', "metro_park_maintenance.week_plan, {plan_id}".format(
                             plan_id=record.id))])
            for tmp_record in records:
                if tmp_record.rule_infos:
                    tmp_record.write({
                        "active": False
                    })

        self.write({
            "active": False
        })

    @api.multi
    def view_week_plan_action(self):
        '''
        查看周计划详情
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "tag": "week_plan_summary",
            "context": {
                "week_plan_id": self.id
            }
        }

    @api.multi
    def mile_work_class_manage(self):
        '''
        工班安排
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.week_plan",
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'context': {},
            "views": [[self.env.ref('metro_park_maintenance.week_plan_miel_work_class_form').id, "form"]]
        }

    @api.multi
    def view_week_plan_data_action(self):
        '''
        查看日计划数据，限定domain为某个周, 查看某个周的数据，并且能进行编辑
        :return:
        '''
        tree_id = self.env.ref(
            'metro_park_maintenance.week_rule_info_list').id

        form_id = self.env.ref(
            'metro_park_maintenance.week_rule_info_form').id

        start_date = self.start_date
        end_date = self.end_date

        return {
            "type": "ir.actions.act_window",
            "name": "{year}年第{week}周".format(year=self.year, week=self.week),
            "res_model": "metro_park_maintenance.rule_info",
            "view_mode": 'list,form',
            "context": {
                "view_type": "week",
                "state": self.state,
                "week_plan_id": self.id,
                "create_plan_id": self.id,
            },
            "domain": [('date', '>=', start_date),
                       ('date', '<=', end_date),
                       ('data_source', '=', 'week')],
            "views": [[tree_id, "list"], [form_id, "form"]]
        }

    @api.multi
    def edit_week_plan(self):
        '''
        编辑周计划
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "name": "周计划编辑",
            "context": {
                "week_plan_id": self.id
            },
            "tag": "week_plan_editor"
        }

    @api.multi
    def publish_week_plan(self):
        '''
        发布周计划
        :return:
        '''
        self.state = "published"

        # 发布相关数据
        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('第{week}周，周计划发布成功!'.format(week=self.week))

        # 更新对应的计划数据
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('date', '>=', str(self.start_date)),
                     ('date', '<=', str(self.end_date)),
                     ('data_source', '=', 'week')])
        rule_infos.write({
            "state": "published"
        })
        try:
            use_pms_maintaince = self.env['metro_park_base.system_config'].search_read(
                [])[0].get('start_pms')
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'W', '1')
        except Exception as e:
            _logger.info('pms基础信息未配置' + str(e))

    @api.multi
    def reback_plan(self):
        '''
        撤回周计划
        :return:
        '''
        day_plans = self.env['metro_park_maintenance.day_plan'].search(
            [('plan_date', '>=', str(self.start_date)),
             ('plan_date', '<=', str(self.end_date)),
             ('state', '=', 'published')])
        if len(day_plans) > 0:
            raise exceptions.ValidationError('当前日期范围已经有周计划处理发布状态!无法进行撤回')
        self.state = 'draft'
        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('第{week}周，周计划撤回成功!'.format(week=self.week))
        try:
            use_pms_maintaince = self.env['metro_park_base.system_config'].search_read(
                [], fields=['use_pms_maintaince'])[0].get(
                'use_pms_maintaince')
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'W', '3')
        except Exception as e:
            _logger.info('pms基础信息未配置' + str(e))

    @api.multi
    def report_view(self):
        '''
        报表模式
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "tag": "week_plan_static"
        }

    @api.multi
    def clear_week_plan(self):
        '''
        清除周计划, 只清除周计划相关的内容
        :return:
        '''
        records = self.env["metro_park_maintenance.rule_info"] \
            .search([("plan_id", "=", "metro_park_maintenance.week_plan, {plan_id}".format(plan_id=self.id))])
        records.write({
            "active": False
        })

    @api.multi
    def get_month_data(self):
        '''
        取得月计划信息
        :return:
        '''
        # 周计划要复用月计划的数据
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('date', '>=', str(self.start_date)),
                     ('date', '<=', str(self.end_date)),
                     ('data_source', 'in', ['year', 'month', 'week']),
                     ('state', '=', 'published'),
                     ('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                         plan_id=self.month_plan_id.id))])
        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'week',
                'date': str(info.date),
                'parent_id': info.id,
                'plan_id':
                    'metro_park_maintenance.week_plan, {plan_id}'
                        .format(plan_id=self.id)
            })

        # 创建新的计划
        return self.env["metro_park_maintenance.rule_info"] \
            .create(vals)

    @api.model
    def get_compute_host(self):
        '''
        取得计算服务器地址
        :return:
        '''
        config = self.env["metro_park_base.system_config"].get_configs()
        calc_host = config["calc_host"] or "ws://127.0.0.1:9520"
        return calc_host

    @api.multi
    def get_week_plan_static_data(self):
        '''
        取得周计划数据, 表格形式展示
        :return:
        '''

        rows = {
            "0": {
                "cells": {
                    "0": {
                        "text": "运营二分公司车辆检修四车间10号线周生产计划({start}-{end})".format(
                            start=str(self.start_date),
                            end=str(self.end_date)),
                        "merge": [0, 7],
                        "style": 2,
                    }
                },
                "height": 40
            },
            "1": {
                "cells": {
                    "0": {
                        "text": "编号{year}{month}{week}".format(
                            year=self.year,
                            month=self.month_plan_id.month,
                            week=self.week),
                        "merge": [0, 7],
                        "style": 1,
                        "height": 30,
                    }
                }
            },
            "2": {
                "cells": {
                    "0": {
                        "text": "日期",
                        "style": 0
                    },
                    "1": {
                        "text": "工作内容",
                        "style": 0
                    },
                    "2": {
                        "text": "列车",
                        "style": 0
                    },
                    "3": {
                        "text": "设备号",
                        "style": 0
                    },
                    "4": {
                        "text": "作业区域",
                        "style": 0
                    },
                    "5": {
                        "text": "作业人",
                        "style": 0
                    },
                    "6": {
                        "text": "备注",
                        "style": 0
                    },
                    "7": {
                        "text": "其它",
                        "style": 0
                    },
                },
                "height": 30
            }
        }

        merges = ['A1:H1', 'C3:D4']
        styles = [{
            "textwrap": True,
            "border": {
                "top": ['thin', '#CDCDCD'],
                "bottom": ['thin', '#CDCDCD'],
                "right": ['thin', '#CDCDCD'],
                "left": ['thin', '#CDCDCD'],
            }
        }, {
            "height": 36,
            "align": 'right',
            "textwrap": True,
            "border": {
                "top": ['thin', '#CDCDCD'],
                "bottom": ['thin', '#CDCDCD'],
                "right": ['thin', '#CDCDCD'],
                "left": ['thin', '#CDCDCD'],
            }
        }, {
            "height": 36,
            "align": 'center',
            "textwrap": True,
            "border": {
                "top": ['thin', '#CDCDCD'],
                "bottom": ['thin', '#CDCDCD'],
                "right": ['thin', '#CDCDCD'],
                "left": ['thin', '#CDCDCD'],
            }
        }
        ]

        row_index = 3
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'
                      .format(plan_id=self.id))])

        start_date = pendulum.parse(str(self.start_date))
        for day in range(0, 7):
            start_date = start_date.add(days=day)
            start_date_str = start_date.format("YYYY-MM-DD")

            day_rules = {}
            for info in rule_infos:
                if str(info["date"]) == start_date_str:
                    location_names = info.locations.mapped("name")
                    location = ",".join(location_names)
                    key = '{rule_no}_{work_class_name}_{locations}'.format(
                        rule_no=info.rule.no,
                        work_class_name=info.work_class_name,
                        locations=location)
                    day_rules.setdefault(key, []).append(info)

            # 工班、作业地点、
            keys = day_rules.keys()
            if len(day_rules) > 0:
                for index, key in enumerate(keys):
                    infos = day_rules[key]
                    devs = set([info["dev"]["dev_no"] for info in infos])
                    if index == 0:
                        rows[str(row_index)] = {
                            "cells": {
                                "0": start_date_str,
                                "2": key,
                                "3": ",".join(devs)
                            },
                            "style": 0
                        }
                row_index = row_index + 1

        return {
            "styles": styles,
            "rows": rows,
            "merges": merges,
        }

    @api.multi
    def check_if_has_balance_rule(self, var_info):
        '''
        检查是否有均衡修程, 暂时是如果有均衡修的话则不安排
        :return:
        '''
        self.ensure_one()

        start_date = pendulum.parse(var_info["date"])
        positive_offset = var_info["positive_offset"]
        negative_offset = var_info["negative_offset"]
        rule_id = var_info["rule_id"]
        overlapped_rules = \
            self.env["metro_park_maintenance.repair_rule"].search(
                [("overlap_rules", "in", [rule_id])])
        tmp_start = start_date.subtract(days=negative_offset)
        tmp_end = start_date.add(days=positive_offset)
        records = self.env["metro_park_maintenance.rule_info"].search(
            [("date", ">=", tmp_start.format('YYYY-MM-DD')),
             ('date', "<=", tmp_end.format('YYYY-MM-DD')),
             ('rule', 'in', overlapped_rules.ids),
             ('data_source', '=', 'week'),
             ('dev.id', '=', var_info['dev_id'])], order="date asc")
        if len(records) > 0:
            var_info["val"] = 0

    @api.model
    def get_week_plan_compute_data(self, info):
        '''
        取得周计划计算数据, 周计划安排里程检和均衡修， 要求是尽量比较平均
        :return:
        '''

        calc_host = info["calc_host"]
        if not calc_host or calc_host == "":
            raise exceptions.Warning("计算服务器未配置!")

        week_plan_id = info["week_plan_id"]
        week_plan = self.env["metro_park_maintenance.week_plan"] \
            .browse(week_plan_id)

        # 取得周计划修程
        rules = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', '=', 'week')])

        special_days_cache = {}
        holidays = {}
        white_list = []

        # 取得历史数据
        start_date = pendulum.parse(str(week_plan.start_date))
        end_date = pendulum.parse(str(week_plan.end_date))

        # 最长周期不超过5年
        his_infos = self.env["metro_park_maintenance.rule_info"] \
            .get_week_history_info(start_date, start_date.subtract(years=5))
        history_repair_info = {}
        for info in his_infos:
            key = "{dev_id}_{rule_id}".format(dev_id=info.dev.id, rule_id=info.rule.id)
            history_repair_info[key] = info.date

        # 均衡修的历史信息
        his_balance_infos = self.env["metro_park_maintenance.rule_info"] \
            .get_week_history_balance_info(start_date, start_date.subtract(years=5))
        history_balance_repair_info = {}
        for info in his_balance_infos:
            key = "{dev_id}_{rule_id}".format(dev_id=info.dev.id, rule_id=info.rule.id)
            history_balance_repair_info[key] = info.date

        # 取得所有的设备
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train').id
        devs = self.env["metro_park_maintenance.train_dev"] \
            .search([('dev_type', '=', dev_type_electric_train)])

        # 取得本周的均衡修信息，洗车要使用, 洗车等要排到均衡修的最后一天或后一天,
        # 这里只能取月计划的，月计划会根据年计划进行调整
        balance_rule_info = {}
        infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'.format(plan_id=week_plan_id)),
                     ('rule.target_plan_type', '=', 'year')], order='date asc')
        for info in infos:
            date = pendulum.parse(str(info.date))
            week_day = date.day_of_week - 1 if date.day_of_week != 0 else 6
            dev_id = info.dev.id
            balance_rule_info.setdefault(dev_id, []).append(week_day)

        # 补全信息
        for dev_id in devs.ids:
            if dev_id not in balance_rule_info:
                balance_rule_info.setdefault(dev_id, [])

        var_index = 0
        dev_rules_infos = []
        task_vars = []

        # 修程所有天的变量统计
        rule_day_vars = {}

        # dev_rule_info 包含 rules, 和 balance_rules, rules包含vars
        for dev in devs:

            dev_rule_info = {
                "dev_id": dev.id,
                "rules": [],
                "balance_rules": balance_rule_info[dev.id]
            }

            for rule in rules:

                # 单个rule信息, 1个rule的变量对应于30或31个变量，变量值为1则安排，否则不安排
                rule_vars_info = {
                    "rule_id": rule.id,
                    "dev_id": dev.id,
                    "vars": [],
                    "expired": False,
                    "rule_start_index": var_index,
                    "ignore_balance": False if rule.no in ['G'] else True,
                    "overlaps_balance": True if rule.no in ['G'] else False
                }
                key = '{dev_id}_{rule_id}'.format(dev_id=dev.id, rule_id=rule.id)
                his_plan_date = history_repair_info.get(key, None)

                # 找到所有覆盖的修程,找时间靠前的项
                overlapped_rules = \
                    self.env["metro_park_maintenance.repair_rule"].search(
                        [("overlap_rules", "in", [rule.id])])
                tmp_ids = overlapped_rules.ids
                for tmp_id in tmp_ids:
                    tmp_key = '{dev_id}_{rule_id}'.format(dev_id=dev.id, rule_id=tmp_id)
                    tmp_date = history_balance_repair_info.get(tmp_key, None)
                    if tmp_date:
                        tmp_date = pendulum.parse(str(tmp_date))
                        if not his_plan_date:
                            his_plan_date = tmp_date
                        elif pendulum.parse(str(tmp_date)) > pendulum.parse(str(his_plan_date)):
                            his_plan_date = tmp_date

                tmp_vars = []
                week_days = 7
                if his_plan_date:

                    last_plan_date = pendulum.parse(str(his_plan_date))
                    # 注意, 这里由于是算的中间间隔天数，所以这里要加1
                    next_plan_date = last_plan_date.add(days=rule.period + 1)

                    # 如果小于开始或是在区间中, 如果加上正的偏移都达不到那么肯定是要马上安排
                    min_start_date = start_date.subtract(days=rule.positive_offset)
                    if next_plan_date < min_start_date \
                            or min_start_date <= next_plan_date <= end_date:

                        # 在月份之前, 那么时间肯定到了
                        rule_vars_info["positive_offset"] = rule.positive_offset
                        rule_vars_info["negative_offset"] = rule.negative_offset
                        rule_vars_info["expired"] = False
                        rule_vars_info["period"] = rule.period

                        if next_plan_date < min_start_date:
                            # 时间到了立即安排,可能太多, 所以没有限定正向区间
                            rule_vars_info["next_plan_day"] = 0
                            rule_vars_info["expired"] = True
                            rule_vars_info["next_day_negative_offset"] = 0
                            # 留下一定的冗余
                            rule_vars_info["next_day_positive_offset"] = rule.positive_offset
                        elif next_plan_date < start_date:
                            # 添加负区间，肯定大于等于周的第一天
                            tmp_next_plan_date = next_plan_date.add(days=rule.positive_offset)
                            # 这里有可能出现负值
                            rule_vars_info["next_plan_day"] = 0
                            # 这里比较特别, 转换了下偏差, 这里应当减去用了的天数，为了方便，在计算那边处理，如果小于0就给丢掉
                            rule_vars_info["next_day_negative_offset"] = rule.positive_offset
                            delta = tmp_next_plan_date - start_date
                            rule_vars_info["next_day_positive_offset"] = delta.days
                        else:
                            # 此处day为一个周中的哪天, 由于0为星期天, 所以要特别处理
                            rule_vars_info["next_plan_day"] = \
                                next_plan_date.day_of_week - 1 if next_plan_date.day_of_week != 0 else 6
                            rule_vars_info["next_day_negative_offset"] = rule.negative_offset
                            rule_vars_info["next_day_positive_offset"] = rule.positive_offset

                        for index, day in enumerate(range(0, week_days)):

                            tmp_date = start_date.add(days=day)
                            tmp_date_str = tmp_date.format("YYYY-MM-DD")

                            # 周未为零，其它为1-6, 这里转换下
                            week_day = tmp_date.day_of_week - 1 if tmp_date.day_of_week != 0 else 6

                            if index == 0:
                                tmp_var = {
                                    "day": day,
                                    "expired": rule_vars_info["expired"],
                                    "dev_id": dev.id,
                                    "rule_id": rule.id,
                                    "period": rule.period,
                                    "positive_offset": rule.positive_offset,
                                    "negative_offset": rule.negative_offset,
                                    "date": tmp_date_str,
                                    "var_index": var_index,
                                    "sub_index": index,
                                    "week_day": week_day,
                                    "start_index": rule_vars_info["next_plan_day"],
                                    "is_start": True,
                                    "val": -1,  # -1 表示未指定,
                                    "ignore_balance": rule_vars_info["ignore_balance"]
                                }
                            else:
                                tmp_var = {
                                    "day": day,
                                    "expired": False,
                                    "dev_id": dev.id,
                                    "rule_id": rule.id,
                                    "period": rule.period,
                                    "positive_offset": rule.positive_offset,
                                    "negative_offset": rule.negative_offset,
                                    "date": tmp_date_str,
                                    "var_index": var_index,
                                    "sub_index": index,
                                    "week_day": week_day,
                                    "start_index": rule_vars_info["next_plan_day"],
                                    "is_start": False,
                                    'val': -1,
                                    "ignore_balance": rule_vars_info["ignore_balance"]
                                }

                            var_index += 1
                            var_index += 1

                            # 5有周六，6为周天, 这里进行了转化
                            if week_day == 5 \
                                    or week_day == 6 \
                                    or tmp_date_str in special_days_cache:
                                tmp_var["is_holiday"] = True

                            assert tmp_var['week_day'] == tmp_var['sub_index']
                            tmp_vars.append(tmp_var)
                            task_vars.append(tmp_var)

                            key = '{rule_id}_{day}'.format(rule_id=rule.id, day=week_day)
                            rule_day_vars.setdefault(key, []).append(tmp_var["var_index"])
                else:
                    # 超过1周同时又没有历史信息的则当周进行检修
                    rule_vars_info["next_day_negative_offset"] = rule.negative_offset
                    rule_vars_info["next_day_positive_offset"] = rule.positive_offset
                    rule_vars_info["expired"] = True
                    # 一些地方写死算了，要不然配置太多了
                    rule_vars_info["ignore_balance"] = False if rule.no == 'G' else True

                    if rule.period > 7:
                        rule_vars_info["next_plan_day"] = 0
                        rule_vars_info["period"] = rule.period
                        # 可以安排在7天中的任一天, 这里只是为了增加灵活性
                        rule_vars_info["positive_offset"] = 7
                        rule_vars_info["negative_offset"] = 0
                    else:
                        rule_vars_info["next_plan_day"] = 0
                        rule_vars_info["period"] = rule.period
                        rule_vars_info["positive_offset"] = rule.positive_offset
                        rule_vars_info["negative_offset"] = rule.negative_offset

                    # rule_vars_info 下边的变量，每一天都是一个变量
                    # 变量为1则安排，变量值为0则不安排
                    for index, day in enumerate(range(0, week_days)):
                        tmp_date = start_date.add(days=day)
                        tmp_date_str = tmp_date.format("YYYY-MM-DD")
                        week_day = tmp_date.day_of_week - 1 if tmp_date.day_of_week != 0 else 6
                        if index == 0:
                            tmp_var = {
                                "day": day,
                                "expired": False,
                                "dev_id": dev.id,
                                "rule_id": rule.id,
                                "period": rule.period,
                                "positive_offset": rule_vars_info["next_day_positive_offset"],
                                "negative_offset": rule_vars_info["next_day_negative_offset"],
                                "date": tmp_date.format("YYYY-MM-DD"),  # 标识代表的日期
                                "var_index": var_index,
                                "sub_index": index,
                                "start_index": rule_vars_info["next_plan_day"],
                                "week_day": week_day,
                                "is_start": True,
                                "val": 1,  # 已经超期, 第一天必需安排
                                "ignore_balance": rule_vars_info["ignore_balance"]
                            }
                        else:
                            tmp_var = {
                                "day": day,
                                "expired": False,
                                "dev_id": dev.id,
                                "rule_id": rule.id,
                                "period": rule.period,
                                "positive_offset": rule["positive_offset"],
                                "negative_offset": rule["negative_offset"],
                                "date": tmp_date.format("YYYY-MM-DD"),  # 标识代表的日期
                                "var_index": var_index,
                                "sub_index": index,
                                "start_index": rule_vars_info["next_plan_day"],
                                "week_day": week_day,
                                "is_start": False,
                                "val": -1,
                                "ignore_balance": rule_vars_info["ignore_balance"]
                            }

                        var_index += 1
                        # 节假日， 0为周日，6为周六
                        week_day = tmp_date.day_of_week - 1 if tmp_date.day_of_week != 0 else 6
                        if (week_day == 5 or week_day == 6 or tmp_date_str in special_days_cache) \
                                and tmp_date_str not in white_list:
                            tmp_var["is_holiday"] = True

                        assert tmp_var['week_day'] == tmp_var['sub_index']
                        task_vars.append(tmp_var)
                        tmp_vars.append(tmp_var)

                        # 保证每一天不超过数里, 里程修一天不超过8个， 洗车一天不超过7个
                        key = '{rule_id}_{day}'.format(rule_id=rule.id, day=week_day)
                        rule_day_vars.setdefault(key, []).append(tmp_var["var_index"])

                rule_vars_info["vars"] = tmp_vars
                if len(tmp_vars) > 0:
                    dev_rule_info["rules"].append(rule_vars_info)

            if len(dev_rule_info["rules"]) > 0:
                dev_rules_infos.append(dev_rule_info)

        return {
            "cmd": "plan_week",
            "data": {
                "rules": rules.read(fields=["id", "name"]),
                "dev_rules_infos": dev_rules_infos,
                "task_vars": task_vars,  # 仅用于数量, 其它没啥大用
                "days": 7,
                "holidays": holidays,
                "year": week_plan.year,
                "week": week_plan.week,
                "constrains": [],
                "rule_day_vars": rule_day_vars,
                "calc_host": calc_host,
                "plan_id": week_plan_id,
                "balance_rule_info": balance_rule_info
            }
        }

    @api.multi
    def syn_month_info(self):
        '''
        同步月计划信息
        :return:
        '''

        year = self.month_plan_id.year
        week = self.week

        ids = ['metro_park_maintenance.month_plan, {plan_id}'.format(
            plan_id=self.month_plan_id.id)]
        month = self.month_plan_id.month
        month_start_date = pendulum.Date(year, month, 1)
        pre_month_start = month_start_date.subtract(months=1)
        pre_year = pre_month_start.year
        pre_month = pre_month_start.month
        pre_month_plan = self.env["metro_park_maintenance.month_plan"] \
            .search([('year', '=', pre_year),
                     ('month', '=', pre_month)])
        if pre_month_plan:
            ids.append('metro_park_maintenance.month_plan, {plan_id}'.format(
                plan_id=pre_month_plan.id))

        # 周计划要复用月计划的数据, 由于周计划可能会两个月，所以这里还要特别处理
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('date', '>=', str(self.start_date)),
                     ('date', '<=', str(self.end_date)),
                     ('state', '=', 'published'),
                     ('plan_id', 'in', ids)])
        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'week',
                'date': str(info.date),
                'parent_id': info.id,
                'plan_id':
                    'metro_park_maintenance.week_plan, {plan_id}'
                        .format(plan_id=self.id)})

        # 创建新的计划
        return self.env["metro_park_maintenance.rule_info"] \
            .create(vals)

    @api.multi
    def clear_week_data(self):
        '''
        清除周数据
        :return:
        '''
        # 先清除原有的数据
        old_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'.format(
            plan_id=self.id)), ('data_source', '=', 'week'), ('parent_id', '=', False)])
        old_infos.write({
            "active": False
        })

    @api.multi
    def export_week_plan(self):
        '''
        导出周计划
        :return:
        '''
        # 先检查数据
        # rule_infos = self.env["metro_park_maintenance.rule_info"].search(
        #     [('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'.format(plan_id=self.id))])
        # for info in rule_infos:
        #     if info.rule and info.rule.target_plan_type in ['year', 'month'] and not info.work_class:
        #         raise exceptions.Warning('均衡修没有安排作业工班!')

        # 跳转下载地址
        return {
            'type': 'ir.actions.act_url',
            'url': '/export_week_plan/{plan_id}'.format(plan_id=self.id),
            'target': 'new'
        }

    @api.model
    def deal_compute_result(self, plan_data, result):
        '''
        处理周计划计算结果
        :return:
        '''
        if result["status"] != 200:
            raise exceptions.ValidationError("计算出错，请重新计算!")

        plan_id = int(plan_data['plan_id'])
        week_plan = self.browse(plan_id)

        # 取得所有的任务
        datas = result['datas']
        task_vars = plan_data['task_vars']

        vals = []
        for index, task in enumerate(task_vars):
            if datas[index] != 1:
                continue

            tmp_date = pendulum.parse(task["date"])
            dev_id = task['dev_id']

            # 这里应当清除掉原来的信息
            vals.append({
                'dev': dev_id,
                'date': tmp_date.format("YYYY-MM-DD"),
                'rule': task['rule_id'],
                'data_source': 'week',
                'plan_id': 'metro_park_maintenance.week_plan, {plan_id}'.format(
                    plan_id=week_plan.id)
            })

        # 先清除原有的数据
        old_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.week_plan, {plan_id}'.format(plan_id=week_plan.id)),
                     ('data_source', '=', 'week'), ('parent_id', '=', False)])
        old_infos.write({
            "active": False
        })

        # 先创建规程信息
        self.env["metro_park_maintenance.rule_info"].create(vals)
