# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging
import copy

_logger = logging.getLogger(__name__)


class MonthPlan(models.Model):
    '''
    月计划, 用计划计算的时候才将年计划的数据拿出来，然后更新. 月计划重新计算规则，
    找到最后执行的计划，之后的以此作为历史记录，然后进行偏移。
    '''
    _name = 'metro_park_maintenance.month_plan'
    _description = '月计划，月计划中添加里程修'
    _rec_name = 'plan_name'
    _track_log = True
    _order = "year desc, month desc"

    year_plan = fields.Many2one(string="所属年计划",
                                comodel_name="metro_park_maintenance.year_plan",
                                ondelete="restrict",
                                help="必需要月计划删除了以后年计划才能删除，"
                                     "防止不小心删除年计划把所有的数据都删除了")

    year = fields.Integer(string="年")
    month = fields.Integer(string="月")

    start_date = fields.Date(string="开始时间",
                             compute="compute_date",
                             store=True,
                             help='这个字段用于搜索')

    end_date = fields.Date(string="结束时间",
                           compute="compute_date",
                           store=True,
                           help='这个字段用于搜索')
    pms_work_class_info = fields.Many2one(comodel_name='pms.department', string='工班')

    def get_default_sequence(self):
        '''
        取得默认的序号
        :return:
        '''
        return self.env['ir.sequence'].next_by_code('month.plan.number')

    plan_no = fields.Char(string='计划编号')
    plan_name = fields.Char(string='计划名称')

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布')],
                             default='draft')
    operation_buttons = fields.Char(string='操作')
    plan_datas = fields.Many2many(string="月计划数据",
                                  comodel_name="metro_park_maintenance.plan_data",
                                  relation="month_plan_and_plan_data_rel",
                                  column1="plan_id",
                                  column2="data_id")
    remark = fields.Char(string='备注')
    active = fields.Boolean(default=True)

    _sql_constraints = [('plan_no_unique', 'UNIQUE(plan_no)', "计划编号不能重复")]

    @api.one
    @api.constrains('plan_name')
    def _check_plan_name(self):
        '''
        检查年计划名称
        :return:
        '''
        records = self.search([('plan_name', '=', self.plan_name), ('id', '!=', self.id)])
        if records:
            raise exceptions.ValidationError("年计划名称重复，请选用其它名称!")

    # 这里实际上显示年月用
    @api.one
    @api.depends('year', 'month')
    def compute_date(self):
        '''
        计算日期
        :return:
        '''
        if self.month and self.year:
            tmp_date = pendulum.Date(int(self.year), int(self.month), 1)
            self.start_date = tmp_date.format('YYYY-MM-DD')
            days = tmp_date.days_in_month
            end_date = tmp_date.add(days=days - 1)
            self.end_date = end_date.format('YYYY-MM-DD')

    @api.multi
    def publish_plan(self):
        '''
        发布计划
        '''
        self.ensure_one()
        self.state = 'published'

        # 相关的数据设置为published
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([("month", "=", self.month),
                     ("year", "=", self.year),
                     ("data_source", "=", "month")])
        for info in rule_infos:
            if not info.work_class and not info.pms_work_class:
                pass
                # raise exceptions.Warning("没有安排工班, 无法发布!")

        rule_infos.write({
            "state": "published"
        })

        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('{year}年{month}，月计划发布成功!'
                          .format(year=self.year, month=self.month))

        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)

        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'M', '1')
        except Exception as error:
            _logger.error('PMS接口获取失败{error}'.format(error=error))

    @api.multi
    def reback_plan(self):
        '''
        撤回计划
        :return:
        '''
        year = self.year
        month = self.month
        date_start = pendulum.Date(year, month, 1)
        date_start_str = date_start.format('YYYY-MM-DD')
        date_end_str = pendulum.Date(year, month, date_start.days_in_month) \
            .format('YYYY-MM-DD')
        # 查询当前是否已经有发布了的周计划
        week_plans = self.env['metro_park_maintenance.week_plan'] \
            .search(['|',
                     '&',
                     ('start_date', '>=', date_start_str),
                     ('start_date', '<=', date_end_str),
                     '&',
                     ('end_date', '>=', date_start_str),
                     ('end_date', '<=', date_end_str),
                     ('state', '=', 'published')])
        if len(week_plans) > 0:
            raise exceptions.ValidationError('当前月份有周计划已经发布，无法撤回，请先撤回相应的周计划!')

        self.state = 'draft'
        try:
            config = self.env['metro_park_base.system_config'].get_configs()
            use_pms_maintaince = config.get('start_pms', False)
        except Exception as e:
            _logger.error('PMS基础信息配置错误{error}'.format(error=e))
        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'M', '3')
        except Exception as error:
            _logger.error('PMS接口获取失败{error}'.format(error=error))

    @api.multi
    def view_month_plan_action(self):
        '''
        取得月计划
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "name": "{year}_{month}".format(year=self.year, month=self.month),
            "tag": "month_month_plan_editor",
            "context": {
                "month_plan_id": self.id
            }
        }

    @api.multi
    def view_month_plan_works(self):
        '''
        查看生产作业大表
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "name": "生产作业{year}_{month}".format(year=self.year, month=self.month),
            "tag": "month_plan_works",
            "context": {
                "month_plan_id": self.id
            }
        }

    @api.multi
    def view_month_plan_works_import(self):
        form_id = self.env.ref("metro_park_maintenance.view_month_plan_works_import").id

        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.month_plan_import_wizard",
            'target': 'new',
        }

    @api.multi
    def month_plan_export(self):
        """
        导出月计划
        :return:
        """
        return {
            'name': '月计划下载',
            'type': 'ir.actions.act_url',
            'url': '/export_month_plan/{month_plan_id}'.format(month_plan_id=self.id)
        }

    @api.multi
    def unlink(self):
        '''
        必需要周计划删除以后才能删除月计划
        :return:
        '''
        for record in self:
            start_date = record.start_date
            end_date = record.end_date
            records = self.env["metro_park_maintenance.week_plan"] \
                .search(['|',
                         '&',
                         ('start_date', '>=', start_date),
                         ('start_date', '<=', end_date),
                         '&',
                         ('end_date', '>=', start_date),
                         ('end_date', '<=', end_date)])
            if len(records) > 0:
                raise exceptions.ValidationError(
                    "{month}还有相应的计划没有删除".format(month=record.month))

        for record in self:
            # 先删除具体信息
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([('date', '>=', record.start_date),
                         ('date', '<=', record.end_date),
                         ('data_source', '=', 'month')])
            records.write({
                "active": False
            })

            # 对应用很多设备, 只有具体信息删除完了以后才删除计划数据
            records = self.env["metro_park_maintenance.plan_data"] \
                .search([("date", '>=', record.start_date), ("date", "<=", record.end_date)])
            for tmp_record in records:
                if tmp_record.rule_infos:
                    tmp_record.write({
                        "active": False
                    })

    @api.multi
    def unlink(self):
        '''
        删除月计划, 改成软删除
        :return:
        '''
        for record in self:
            # 删除月计划数据。
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([("plan_id", '=', 'metro_park_maintenance.month_plan, {plan_id}'
                          .format(plan_id=record.id))])
            records.write({
                "active": False
            })
        self.write({
            "active": False
        })

    @api.multi
    def clear_month_info(self):
        '''
        删除当月的月计划产生的数据
        :return:
        '''
        for record in self:
            # 删除月计划数据。
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([("plan_id", '=', 'metro_park_maintenance.month_plan, {plan_id}'
                          .format(plan_id=record.id))])
            records.write({
                "active": False
            })

    @api.multi
    def import_month_works(self):
        '''
        导入生产作业
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.import_month_works",
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "month_plan_id": self.id,
            },
            "views": [[self.env.ref('metro_park_maintenance.import_month_works_form').id,
                       "form"]]
        }

    @api.multi
    def re_compute_plan(self):
        '''
        校正月计划，如果历史记划没有执行则进行校正, 扣车等要自动移动检修
        :return:
        '''
        rule_infos = self.env["metro_park_maintenance.rule_info"]\
            .search([[('year', '=', self.year),
                      ('month', '=', self.month), ('rule_type', '=', self.month)]])
        return rule_infos

    @api.multi
    def get_plan_work_class_data(self):
        '''
        安排工班, 工班选择按照轮换的方式，要求任务均衡，
        :return:
        '''

        department_property_work_class = \
            self.env.ref("metro_park_base.department_property_balance_work_class").id

        # 取得有均衡修工班属性的工班
        work_classes = self.env["funenc.wechat.department"].search(
            [("properties", "in", [department_property_work_class])])
        work_class_count = len(work_classes)

        # 取得所有的任务, 由于数据复制了一份，所以这里还是要限制计划id
        works = self.env["metro_park_maintenance.rule_info"].search(
            [("rule.target_plan_type", "in", ["year", "month"]),
             ('date', '>=', str(self.start_date)),
             ('date', '<=', str(self.end_date)),
             ('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                 plan_id=self.id))], order="dev asc, date asc")

        tasks = []
        date_tasks = {}
        pre_task = None
        for work in works:
            # 默认都有第几天，导入的时候要处理下
            task_index = len(tasks)
            task = {
                "index": task_index,
                "date": str(work.date),
                "dev": work.dev.id,
                "val": 0,
                "rule_id": work.rule.id,
                "need_platform": True if 'D' in work.rule_no else False,
                "same_with_pre_task": -1,
                "id": work.id
            }
            if pre_task:
                pre_date = pendulum.parse(pre_task["date"]).add(days=1)
                cur_date = pendulum.parse(task["date"])
                if pre_date == cur_date \
                        and pre_task["rule_id"] == task["rule_id"] \
                        and pre_task["dev"] == task["dev"]:
                    task["same_with_pre_task"] = pre_task["index"]
            tasks.append(task)

            pre_task = task
            date_tasks.setdefault(str(work.date), []).append(task_index)

        # 统计每个地方的工班数量, 原则上一个工班只属于一个地方
        location_work_class_info = {}
        for work_class in work_classes:
            if len(work_class.locations) > 0:
                location = work_class.locations[0]
                location_work_class_info.setdefault(location.id, []).append(work_class.id)

        # 取得本月的天数
        start_date = pendulum.parse(str(self.start_date))

        # 取得服务器配置
        config = self.env["metro_park_base.system_config"].get_configs()

        return {
            "work_classes": work_classes.mapped("id"),
            "work_class_count": work_class_count,
            "tasks": tasks,
            "tasks_count": len(tasks),
            "location_work_class_info": location_work_class_info,
            "day_count": start_date.days_in_month,
            "date_tasks": date_tasks,
            "calc_host": config.get("calc_host")
        }

    @api.model
    def deal_plan_work_class_result(self, plan_data, rst):
        '''
        处理计划结果数据, 将工班结果写入
        :return:
        '''
        rst = rst["datas"]
        tasks = plan_data["tasks"]
        work_classes = plan_data["work_classes"]
        for index, task in enumerate(tasks):
            rule_info = self.env["metro_park_maintenance.rule_info"]\
                    .browse(task["id"])
            val = rst[index]
            _logger.info('the val is:{val}'.format(val=val))
            rule_info.work_class = [(6, 0, [work_classes[val - 1]])]

    @api.multi
    def get_month_plan_data(self, wizard_id):
        '''
        计算月计划，本月原来安排的只能优选选择
        :return:
        '''
        wizard_info = \
            self.env["metro_park_maintenance.month_plan_compute_wizard"].browse(wizard_id)

        # 当月的计划, 有可能是扣车移动过来的，同时可能有月计划的内容
        real_infos = self.env["metro_park_maintenance.rule_info"]\
            .search([('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                         plan_id=self.id)),
                     ('rule.target_plan_type', '=', 'year')], order="date asc")

        # 年计划就要求均衡
        dev_tasks_cache = dict()
        for info in real_infos:
            dev_tasks_cache.setdefault(info.dev.id, []).append(info)

        # 暂时没有考虑跨月的项，跨月的项要要作预先安排
        # for key in dev_tasks_cache:
        #     infos = dev_tasks_cache[key]
        #     if len(infos) > 0 and infos[0].repair_num != 1:
        #         while len(infos) > 0 and infos[0].repair_num != 1:
        #             infos = infos[1:]
        #     dev_tasks_cache[key] = infos

        month_start = pendulum.date(self.year, self.month, 1)
        month_days = month_start.days_in_month

        # 白名单
        month_end = month_start.add(days=month_days)
        white_list = self.env["metro_park_maintenance.white_list"]\
            .search([("date", ">=", month_start.format('YYYY-MM-DD')),
                     ('date', '<=', month_end.format('YYYY-MM-DD'))])
        white_dates = []
        for record in white_list:
            white_dates.append(
                pendulum.parse(str(record.date)).format("YYYY-MM-DD"))

        # 查询特殊日期配置, 黑名单
        special_days = \
            self.env['metro_park_maintenance.holidays'].search([])
        special_days_cache = {str(record.date): True for record in special_days}

        # 节假日
        holidays = []
        for tmp_index in range(1, month_days + 1):
            tmp_date = pendulum.date(self.year, self.month, tmp_index)
            tmp_date_str = tmp_date.format('YYYY-MM-DD')
            if (tmp_date.day_of_week == 6 or tmp_date.day_of_week == 0) \
                    and tmp_date_str not in white_dates:
                holidays.append(tmp_index)
            if tmp_date_str in special_days_cache and tmp_date_str not in white_dates:
                holidays.append(tmp_index)

        # 取得缓存信息, 扣车等会自动挪动，或是用户手动移动
        month_start_date = pendulum.date(self.year, self.month, 1)
        history_plans = self.env["metro_park_maintenance.rule_info"]\
            .get_year_plan_history_info(month_start_date, False)
        history_plan_cache = {plan.dev.id: plan for plan in history_plans}

        tasks = []
        for dev_id in dev_tasks_cache:

            dev_tasks = []
            infos = dev_tasks_cache[dev_id]
            pre_info = None
            for tmp_index, info in enumerate(infos):

                # 过滤掉复复的情况
                if pre_info and pre_info.rule.id == info.rule.id:
                    pre_info = info
                    continue
                else:
                    pre_info = info

                rule = info.rule

                task = {
                    "index": len(tasks),
                    "id": info.id,
                    "rule_id": info.rule.id,
                    "dev": dev_id,
                    # 同一设备不限定
                    "pre_index": len(tasks) - 1 if tmp_index != 0 else -1,
                    "period": info.rule.period,
                    "positive_offset": info.rule.positive_offset,
                    "negative_offset": info.rule.negative_offset,
                    "repeat_index": -1,
                    # 检修第一天
                    "repair_day": 1,
                    "repair_days": info.rule.repair_days,
                    "left_days": info.rule.period,
                    "info_count": len(infos),
                    "month_start_val": 1,
                    "month_end_val": month_days,
                    "repeat": False,
                    "repair_num": info.repair_num,
                    "attach_index": -1,
                    "is_extra": False
                }

                # 第一个月需要考虑历史信息, 但是这个不考虑修次，决定了最终的位置
                if tmp_index == 0:
                    history_repair_info = history_plan_cache.get(dev_id, False)
                    if history_repair_info:

                        # 最后一个计划开始的日期
                        tmp_date = pendulum.parse(str(history_repair_info["date"]))
                        tmp_delta = month_start_date - tmp_date

                        # 已经使用了的天数
                        offset_days = tmp_delta.days - 1

                        # 已经超超期,需要直接安排
                        if offset_days > rule['period'] + rule['positive_offset']:
                            task['left_days'] = 0
                            task['positive_offset'] = 0
                            task['negative_offset'] = 0
                        # 在负区间内
                        elif rule['period'] - rule['negative_offset'] <= offset_days < rule['period']:
                            task['left_days'] = rule['period'] - offset_days
                            task['negative_offset'] = rule['period'] - offset_days
                        # 在正区间内, 这个有可能刚好剩下的就是星期六和星期天，这个就有点尴尬了
                        elif rule['period'] <= offset_days <= rule['period'] + rule['positive_offset']:
                            task['left_days'] = 0
                            task['negative_offset'] = 0
                            task['positive_offset'] = \
                                rule['period'] + rule['positive_offset'] - offset_days
                        else:
                            # 还没有到达检修周期, 肯定是在上个月进行的，所以无论如何都可以排
                            task['left_days'] = rule['period'] - offset_days

                tasks.append(task)
                dev_tasks.append(task)

                # 时于按时间排序，均衡修不可能同一天进行多个，所以，后面的几个正好是重复的
                repair_days = rule.repair_days
                is_extra = False
                for day in range(1, repair_days):
                    tmp_task = copy.copy(task)

                    # 跨月的情况, 从下月找到相应的数据
                    if tmp_index + day > len(infos) - 1:
                        is_extra = True
                        tmp_year = self.year
                        next_month = self.month + 1
                        if next_month > 12:
                            next_month = 1
                            tmp_year += 1
                        left_rule_infos = \
                            self.env["metro_park_maintenance.rule_info"].search(
                                [('year', '=', tmp_year),
                                 ('month', "=", next_month),
                                 ('dev', '=', dev_id),
                                 ('rule', '=', rule.id)], order="date asc")
                        for tmp_info in left_rule_infos:
                            infos.append(tmp_info)

                    # assert infos[tmp_index + day].rule.id == info.rule.id
                    # assert infos[tmp_index + day].id != info.id

                    tmp_info = infos[tmp_index + day]
                    tmp_task["id"] = tmp_info.id
                    tmp_task["repeat_index"] = len(tasks) - 1
                    tmp_task["pre_index"] = len(tasks) - 1
                    tmp_task["repair_day"] = day + 1
                    tmp_task["index"] = len(tasks)
                    tmp_task["repeat"] = True
                    tmp_task["is_extra"] = is_extra

                    tasks.append(tmp_task)

        # 取得计算服务器
        config = self.env['metro_park_base.system_config'].get_configs()
        calc_host = config.get('calc_host', False)

        attach_tasks = []

        # 附加空调专检的task 如果是第一月份的话, 第一个月尽量安排
        plan_kt_month_1 = self.env.ref("metro_park_base.plan_kt_month_1").id
        plan_kt_month_2 = self.env.ref("metro_park_base.plan_kt_month_2").id
        if wizard_info.plan_kt \
                and wizard_info.plan_kt_month == plan_kt_month_1:
            attach_tasks = []
            for task in tasks:
                # 只按排修程只有一天的
                if task["repair_days"] == 1 and task["repair_day"] == 1:
                    attach_task = {
                        "index": len(attach_tasks),
                        "attach_index": task["index"],
                        "force": False,
                        "dev_id": task['dev']
                    }
                    # 相互关联
                    task["attach_index"] = attach_task["index"]
                    repair_num = task["repair_num"]
                    # 下一次没法进行的情况
                    next_repair_info = \
                        self.env['metro_park_maintenance.plan_config_data'].get_next_repair_info(repair_num)
                    if next_repair_info.repair_days > 1:
                        attach_task["force"] = True
                    attach_tasks.append(attach_task)
        elif wizard_info.plan_kt \
                and wizard_info.plan_kt_month.id == plan_kt_month_2:
            # 如果上一个月没有安排空调专检的话这个月就必需要安排
            kt_rule_id = self.env.ref("metro_park_base_data_10.repair_rule_kt").id
            prev_month = self.month - 1
            prev_year = self.year
            if prev_month <= 0:
                prev_month = 12
                prev_year = prev_year - 1
            his_kt_infos = self.env["metro_park_maintenance.rule_info"].search(
                [("rule", '=', kt_rule_id),
                 ("month", "=", prev_month),
                 ("year", '=', prev_year)])

            his_kt_info_cache = dict()
            for tmp_info in his_kt_infos:
                his_kt_info_cache[tmp_info.dev.id] = tmp_info

            black_dev = []
            for task in tasks:
                if task["dev"] not in his_kt_info_cache \
                        and task['repair_day'] == 1 and task["dev"] not in black_dev:
                    black_dev.append(task['dev'])
                    attach_task = {
                        "index": len(attach_tasks),
                        "attach_index": task["index"],
                        "force": False,
                        "dev_id": task['dev']
                    }
                    # 相互关联
                    task["attach_index"] = len(attach_tasks)
                    attach_tasks.append(attach_task)

        return {
            "tasks": tasks,
            "month": self.month,
            "year": self.year,
            "month_days": month_days,
            "holidays": holidays,
            "calc_host": calc_host,
            "max_plan_per_day": wizard_info.max_plan_per_day,
            "attach_tasks": attach_tasks or [],
            "plan_kt": True if wizard_info.plan_kt.value == 'yes' else False,
            "plan_kt_month": 1 if wizard_info.plan_kt_month.id == plan_kt_month_1 else 2
        }

    @api.multi
    def deal_month_plan_data(self, plan_data, result):
        '''
        处理月计划数据, 只是调整计划时间
        :return:
        '''
        if result['status'] != 200:
            raise exceptions.ValidationError("计算错错，未能找正确解")

        result = result['datas']
        plan_result = result["plan_result"]

        year = plan_data["year"]
        month = plan_data["month"]
        month_start = pendulum.date(year, month, 1)
        plan_id = self.id
        kt_rule_id = self.env.ref("metro_park_base_data_10.repair_rule_kt").id

        vals = []
        attach_result = result['attach_result']
        tasks = plan_data['tasks']
        for task in tasks:
            info_id = task["id"]
            index = task["index"]
            value = plan_result[index]

            # value是从1开始
            plan_date = month_start.add(days=value - 1)
            record = self.env["metro_park_maintenance.rule_info"].browse(info_id)
            if not task["is_extra"]:
                record.write({
                    "date": plan_date.format("YYYY-MM-DD"),
                    "year": plan_date.year,
                    "month": plan_date.month,
                    "day": plan_date.day_of_year
                })
            else:
                # 下月放在本月的情况,创建本月数据
                self.env["metro_park_maintenance.rule_info"].create([{
                    "date": plan_date.format("YYYY-MM-DD"),
                    "dev": task['dev'],
                    "year": plan_date.year,
                    "month": plan_date.month,
                    "day": plan_date.day,
                    "plan_id": "metro_park_maintenance.month_plan, {plan_id}".format(
                        plan_id=plan_id),
                    "rule": task["rule_id"],
                    'data_source': 'month'
                }])

            attach_index = task["attach_index"]
            if attach_index != -1 and attach_result[attach_index] == 1:
                plan_date = plan_date.subtract(days=1)
                vals.append({
                    "date": plan_date.format("YYYY-MM-DD"),
                    "dev": task['dev'],
                    "year": plan_date.year,
                    "month": plan_date.month,
                    "day": plan_date.day,
                    "plan_id": "metro_park_maintenance.month_plan, {plan_id}".format(
                        plan_id=plan_id),
                    "rule": kt_rule_id,
                    'data_source': 'month'
                })

        self.env["metro_park_maintenance.rule_info"].create(vals)

    @api.multi
    def view_delta(self):
        '''
        查看本月修程和上月的间隔
        :return:
        '''
        month = self.month
        year = self.year

        pre_year = year
        pre_month = month - 1
        if month == 1:
            pre_year = year - 1
            pre_month = 12

        # 取得历修程信息, 取得后一天的
        history_plan_cache = dict()
        pre_date = pendulum.date(pre_year, pre_month, 1)
        pre_date = pendulum.date(pre_year, pre_month, pre_date.days_in_month)
        pre_plans = self.env["metro_park_maintenance.rule_info"].search(
            [("date", '<', pre_date),
             ('year', '=', pre_year),
             ('data_source', '=', 'month')],
            order='date asc')
        for tmp_plan in pre_plans:
            history_plan_cache[tmp_plan.dev.id] = tmp_plan

        # 取得当月的信息
        month_plans = self.env["metro_park_maintenance.rule_info"].search(
            [("year", '=', year),
             ('month', '=', month),
             ('data_source', '=', 'month')],
            order='date asc')
        cur_month_cache = {}
        for month_plan in month_plans:
            cur_month_cache.setdefault(month_plan.dev.id, []).append(month_plan)

        vals = []
        for dev_id in cur_month_cache:
            plan = cur_month_cache[dev_id][0]
            tmp_end_date = pendulum.parse(str(plan.date))
            if dev_id in history_plan_cache:
                his_plan = history_plan_cache.get(dev_id, None)
                if his_plan:
                    tmp_start_date = pendulum.parse(str(his_plan.date))
                    delta = tmp_end_date - tmp_start_date
                    vals.append({
                        "dev": dev_id,
                        "days": delta.days
                    })

        records = self.env["metro_park_maintenance.month_plan_delta_info"].create(vals)

        tree_id = self.env.ref(
            'metro_park_maintenance.month_plan_delta_info_list').id

        return {
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "metro_park_maintenance.month_plan_delta_info",
            "name": "计划偏移",
            "views": [[tree_id, 'list'], [False, 'form']],
            "domain": [("id", "in", records.ids)]
        }

    @api.multi
    def syn_year_info(self):
        '''
        同步年计划数据
        :return:
        '''

        # 清除自身的内容
        infos = self.env["metro_park_maintenance.rule_info"].search(
            [('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                plan_id=self.id))])
        infos.write({
            "active": False
        })

        rule_infos = self.env["metro_park_maintenance.rule_info"].search(
            [('data_source', '=', 'year'),
             ('month', '=', self.month),
             ('plan_id', '=', "metro_park_maintenance.year_plan, {plan_id}".format(
                 plan_id=self.year_plan.id))])

        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'month',
                'date': str(info.date),
                'parent_id': info.id,
                'repair_num': info.repair_num,
                'repair_day': info.repair_day,
                'plan_id': 'metro_park_maintenance.month_plan, {plan_id}'.format(
                    plan_id=self.id)
            })

        return self.env["metro_park_maintenance.rule_info"] \
            .create(vals)

    @api.model
    def export_produce_plan(self):
        """
        导出生产计划
        :return:
        """
        now_day = pendulum.today()
        pre_year = now_day.subtract(years=1)

        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.export_produce_plan_wizard",
            'view_mode': 'form',
            "target": "new",
            'context': {
                "default_start_year":
                    self.env["metro_park_maintenance.year"].search(
                        domain=[("val", "=", pre_year.year)]).id,
                "default_start_month":
                    self.env["metro_park_maintenance.month"].search(
                        domain=[("val", "=", pre_year.month)]).id,
                "default_end_year":
                    self.env["metro_park_maintenance.year"].search(
                        domain=[("val", "=", now_day.year)]).id,
                "default_end_month":
                    self.env["metro_park_maintenance.month"].search(
                        domain=[("val", "=", now_day.month)]).id,
            },
            "views": [[self.env.ref(
                'metro_park_maintenance.export_produce_plan_wizard_form').id, "form"]]
        }

    @api.multi
    def clear_duplicate(self):
        '''
        去除一个月排了多个修程的情况
        :return:
        '''
        dev_rule_cache = {}
        records = self.env["metro_park_maintenance.rule_info"].search(
            [('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                plan_id=self.id))], order='date asc')
        for record in records:
            dev_rule_cache.setdefault(record.dev.id, []).append(record.rule.id)

        # 去除一个月排了多个修程
        del_info = []
        for key in dev_rule_cache:
            rules = set(dev_rule_cache[key])
            if len(rules) > 1:
                del_info.append({
                    "dev_id": int(key),
                    "rule": list(rules)[-1]
                })

        # 数量不会太多，一个一个进行删除
        for info in del_info:
            record = self.env["metro_park_maintenance.rule_info"].search(
                [('dev', '=', info['dev_id']), ('rule.id', '=', info['rule'])])
            # 移动到下一个月去
            record.unlink()

    @api.multi
    def import_work_class_info(self):
        '''
        导入生产说明，
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_base.import_produce_work_class",
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_month_plan': self.id,
            },
            "views": [[self.env.ref('metro_park_maintenance.import_produce_work_class_form').id, "form"]]
        }

