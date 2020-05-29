# -*- coding: utf-8 -*-
import datetime
import calendar
from odoo import models, fields, api, exceptions
import pendulum
import logging
import copy
import random

_logger = logging.getLogger(__name__)

STATE = [('draft', '草稿'), ('published', '发布'), ('deleted', '已删除')]


class YearPlan(models.Model):
    '''
    年计划, 年计划创建的时候就创建了全年的数据，然后真实计算的时候往里边填就是了。
    一些展示使用临时表来进行展示
    '''
    _name = 'metro_park_maintenance.year_plan'
    _rec_name = 'plan_name'
    _description = '年计划'
    _order = "year desc"

    year = fields.Integer(string="年份", required=True)
    start_month = fields.Integer(string="月份", default=1)

    # 取得默认计划编号，使用sequence生成年计划编号
    plan_no = fields.Char(string='计划编号',
                          required=True,
                          default=lambda self: self.env['ir.sequence'].next_by_code(
                              'year.plan.number'))
    plan_name = fields.Char(string='计划名称', required=True)

    state = fields.Selection(STATE, string='状态', default='draft')
    active = fields.Boolean(default=True)
    remark = fields.Char(string='备注')

    # 取得默认计划编号，使用sequence生成年计划编号,
    # 根据系统配置，选择使用企业微信工班还是pms工班
    work_unit = fields.Many2one('funenc.wechat.department',
                                string='作业单位',
                                readonly=True,
                                default=lambda self: self.env.user.cur_wx_user_id.cur_department)
    pms_work_class_info = fields.Many2one(comodel_name='pms.department',
                                          string='工班',
                                          help="由于pms的原因，只能走pms的工班")
    work_class = fields.Char(string="工班", compute="_compute_work_class", store=True)

    operation_buttons = fields.Char(string="操作按扭", help="这个只是个占位符")

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

    @api.depends("work_unit", "pms_work_class_info")
    def _compute_work_class(self):
        '''
        计算显示部门, 如果是使用pms则显示pms的作业工作，如果不是则显示部门工班信息
        :return:
        '''
        sys_config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = sys_config.get('start_pms', False)
        for record in self:
            if use_pms_maintaince:
                record.work_class = record.pms_work_class_info
            else:
                record.work_class = record.work_unit.name

    @api.multi
    def get_work_units(self):
        '''
        取得当前用户的工班信息
        :return:
        '''
        user = self.env.user
        if user.cur_location:
            line_id = user.cur_location.line.id
        else:
            raise exceptions.ValidationError('当前用户没有配置所属场段或车辆段!')

        locations_ids = self.env['metro_park_base.location'] \
            .search([('line', '=', line_id)]).ids
        work_class_property_id = self.env.ref("department_property_work_class").id
        work_units = self.env['funenc.wechat.department'].search([
            ('properties', 'in', work_class_property_id),
            ('location', 'in', locations_ids)])

        return work_units

    @api.multi
    def get_user_line(self):
        '''
        取得用户所在线别
        :return:
        '''
        return self.env.user.user.get_user_line()

    @api.model
    def get_year_plan_compute_data(self, info):
        '''
        取得修程上的历史数据, 如果已经超了的话则从第一天开始算起
        取得计划数据，用于前端计算
        调用websocket计算, 每个设备对应多个变量，每个变量的取值范围是1-当年天数，约束条件如下：
        1、相互之间的差必需要在周期之内 30 +-5。
        2、每日工作量不能超限。不用关心，月计划会进行处理
        3、计算的时候需要考虑历史数据。
        4、如果是年中间则计算本年剩余的月份。
        5、年计划只是个参考，真实际算是有月计划中。
        6、单日单个修程不能超限。
        7、最佳状态是每个月修理的任务相关不大
        :param info:
        :return:
        '''
        try:
            year_plan_id = info["year_plan_id"]
            year_plan = self.browse(year_plan_id)
            year = year_plan.year
            start_month = info["month"]
            end_month = info["end_month"]

            # 检查第一个月是否已经进行了安排，防止误排
            rule_infos = self.env["metro_park_maintenance.rule_info"].search(
                [('plan_id', '=', 'metro_park_maintenance.year_plan, {plan_id}'.format(plan_id=year_plan_id)),
                 ('month', '=', start_month)])
            if len(rule_infos) > 0:
                raise exceptions.ValidationError('开始月份已经排列计划，请先清除当月的计划!')

            end_date = pendulum.Date(year, end_month, pendulum.date(year, end_month, 1).days_in_month)
            start_date = pendulum.date(year, start_month, 1)

            # 查询特殊日期配置, 黑名单
            special_days = \
                self.env['metro_park_maintenance.holidays'].search([])
            special_days_cache = {str(record.date): True for record in special_days}

            # 取得白名单配置
            plan_start_date = pendulum.date(year, 1, 1).format("YYYY-MM-DD")
            plan_end_date = pendulum.date(
                year, end_month, pendulum.date(year, end_month, 1).days_in_month).format("YYYY-MM-DD")
            white_list = self.env["metro_park_maintenance.white_list"].search(
                [('date', ">=", plan_start_date), ('date', "<=", plan_end_date)])
            white_dates = white_list.mapped("date")

            # 取得时间范围中的星期六和星期天的索引，这些要排除除值的范围
            holidays = []
            index_var_cache = {}

            # 收集所有的周六周天和节假日
            plan_start_date = pendulum.date(year_plan.year, start_month, 1)
            for month in range(start_month, end_month + 1):
                tmp_month = pendulum.date(year, month, 1)
                tmp_days = tmp_month.days_in_month
                for tmp_day in range(1, tmp_days + 1):
                    tmp_date = pendulum.date(year, month, tmp_day)
                    day_val = tmp_date.day_of_year
                    last_plan_date_str = tmp_date.format('YYYY-MM-DD')
                    week_day = tmp_date.day_of_week
                    if (week_day == 0 or week_day == 6) and last_plan_date_str not in white_dates:
                        holidays.append(day_val)
                    elif last_plan_date_str in special_days_cache and last_plan_date_str not in white_dates:
                        holidays.append(day_val)

            # 缓存规程信息，年计划只安排均衡修
            rules_model = self.env['metro_park_maintenance.repair_rule']
            field_names = ['id', 'name', 'period', 'repair_days', 'positive_offset', 'negative_offset']
            rules = rules_model.search_read([('target_plan_type', '=', 'year'),
                                             ('rule_status', '=', 'normal'),
                                             ('rule_type', '=', 'plan')], fields=field_names)
            rules_cache = {rule['id']: rule for rule in rules}

            # 取得所有的计划配置
            plan_config_model = self.env['metro_park_maintenance.plan_config_data']
            plan_config = plan_config_model.search([])
            if not plan_config:
                raise exceptions.ValidationError("没有配置排程设定信息")

            dev_info_array = []
            var_index = 0

            # 取得所有电客车, 只对电客车进行排列, 不考虑车的状态, 周计划时再考虑
            dev_type = self.env.ref('metro_park_base.dev_type_electric_train').id
            devs = self.env["metro_park_maintenance.train_dev"] \
                .search([('dev_type', '=', dev_type)])

            # 取得历史维修信息, 开始日期之前的修程信息,
            # 如果没有历史信息的话则自动添加偏移, 正负5加上自身的话一共是11天
            # 一般情况下肯定是有历史信息
            history_plans = self.env['metro_park_maintenance.rule_info'] \
                .get_year_plan_history_info(start_date.format('YYYY-MM-DD'))
            history_plan_cache = {plan.dev.id: plan for plan in history_plans}
            if len(history_plan_cache) == 0:
                # 取得偏移信息
                tmp_pre_date = plan_start_date.subtract(months=1)
                offset_cache = self.env["metro_park_maintenance.balance_rule_offset"].get_month_info(
                    tmp_pre_date.year, tmp_pre_date.month)

                month_days = plan_start_date.days_in_month
                index = 0
                for dev in devs:
                    if index >= month_days:
                        index = 0
                    tmp_date = plan_start_date.add(days=index)
                    # 跳过周六周天
                    while tmp_date.day_of_week == 0 or tmp_date.day_of_week == 6:
                        index = index + 1
                        tmp_date = plan_start_date.add(days=index)
                    history_plan_cache[dev.id] = {
                        "date": start_date.subtract(months=1).add(days=index),  # 模拟上月的历史记录
                        "repair_num": 0
                    }
                    if dev.id in offset_cache:
                        history_plan_cache[dev.id]["repair_num"] = offset_cache[dev.id]["offset_num"]
                    index += 1
            else:
                # 有可能有设备没有历史记录，比如新设备
                for dev in devs:
                    if dev.id not in history_plan_cache:
                        history_plan_cache[dev.id] = {
                            "date": start_date.subtract(month=1).add(days=random.randint(27, 30)),  # 模拟上月的历史记录
                            "repair_num": 0
                        }

            # 取得修次配置,设的修程顺序
            config_datas = self.env["metro_park_maintenance.plan_config_data"] \
                .search([], order="index asc")

            # 规程变量缓存
            month_vars = {}
            rule_var_cache = {}
            for dev in devs:

                dev_info = dict()
                dev_info['dev_id'] = dev.id
                dev_info['var_array'] = []

                # 处理均衡修, 只有第一个月才需要考虑历史，每台每设备每个月对应变量,
                # 变量的取值对应这一年剩余的天数中的某一天
                repair_num = 0
                for sub_index, month in enumerate(range(start_month, end_month + 1)):
                    var_info = dict()

                    month_start = pendulum.date(year, month, 1)
                    month_end = pendulum.date(year, month, month_start.days_in_month)

                    # 如果是有历史信息, 并且历史信息的修次大于设置的修次，则使用历史信息的修次
                    if month == start_month:
                        # 历史修次结合配置
                        history_repair_info = history_plan_cache.get(dev['id'], False)
                        if history_repair_info:
                            # 取得的修次是原有的修次，在此基础上加1是现在的修次
                            repair_num = history_repair_info["repair_num"] + 1
                        else:
                            repair_num = 0

                    # 添加偏差
                    real_repair_num = repair_num + (month - start_month)
                    rule_id = config_datas[real_repair_num % len(config_datas)].rule.id
                    rule = rules_cache[rule_id]

                    var_info['index'] = var_index
                    var_info['plan_month'] = month
                    var_info['rule_id'] = rule_id
                    var_info["left_days"] = rule["period"]
                    var_info["period"] = rule["period"]
                    var_info["positive_offset"] = rule["positive_offset"]
                    var_info["negative_offset"] = rule["negative_offset"]
                    var_info["repair_num"] = repair_num
                    var_info["month_start_val"] = month_start.day_of_year
                    var_info["month_end_val"] = month_end.day_of_year
                    var_info["repeat_index"] = -1

                    # 针对于设备
                    var_info["sub_index"] = sub_index
                    var_info["is_start_index"] = True if sub_index == 0 else False
                    var_info["prev_index"] = var_index - 1
                    var_info["dev_id"] = dev.id

                    # 修几天
                    var_info["repair_days"] = rule["repair_days"]

                    # D2等需要重复排列, 先设置为False
                    var_info["repeat"] = False
                    var_info["is_last_repair_day"] = False
                    var_info["is_first_repair_day"] = True

                    # 修程的第几天
                    var_info["repair_day"] = 1
                    if rule["repair_days"] == 1:
                        var_info["is_last_repair_day"] = True

                    # 第一个月需要考虑历史信息，决定了最终的位置
                    if month == start_month:
                        history_repair_info = history_plan_cache.get(dev['id'], False)
                        if history_repair_info:

                            # 最后一个计划开始的日期
                            tmp_date = pendulum.parse(str(history_repair_info["date"]))
                            tmp_delta = plan_start_date - tmp_date

                            # 已经使用了的天数
                            offset_days = tmp_delta.days

                            # 已经超超期,需要直接安排
                            if offset_days > rule['period'] + rule['positive_offset']:
                                var_info['left_days'] = 0
                                var_info['positive_offset'] = 0
                                var_info['negative_offset'] = 0
                            # 在负区间内
                            elif rule['period'] - rule['negative_offset'] <= offset_days < rule['period']:
                                var_info['left_days'] = rule['period'] - offset_days
                                var_info['negative_offset'] = rule['period'] - offset_days
                            # 在正区间内
                            elif rule['period'] <= offset_days <= rule['period'] + rule['positive_offset']:
                                var_info['left_days'] = 0
                                var_info['negative_offset'] = 0
                                var_info['positive_offset'] = \
                                    rule['period'] + rule['positive_offset'] - offset_days
                            else:
                                # 还没有到达检修周期, 肯定是在上个月进行的，所以无论如何都可以排
                                var_info['left_days'] = rule['period'] - offset_days

                    dev_info['var_array'].append(var_info)

                    # 保存变量, 用于限制同一天的同一规程不能超出数量
                    rule_var_cache.setdefault(rule_id, []).append(var_index)
                    month_vars.setdefault(month, []).append(var_index)

                    # 用于返回的时候查找值
                    index_var_cache[var_index] = var_info
                    var_index = var_index + 1

                    # 检修多天的情况
                    last_info = None
                    repair_days = rule["repair_days"]
                    for repair_day, tmp in enumerate(range(1, repair_days)):
                        # 复制的时候带了修次等信息
                        tmp_info = copy.deepcopy(var_info)
                        tmp_info["is_first_repair_day"] = False
                        tmp_info["index"] = var_index
                        tmp_info["repeat"] = True
                        tmp_info["prev_index"] = var_index - 1

                        # 检修的第几天
                        tmp_info["repair_day"] = repair_day + 2
                        tmp_info["repeat_index"] = var_index - 1

                        # 推荐值区间
                        tmp_info["start_val"] = month_start.day_of_year
                        tmp_info["end_val"] = month_end.day_of_year

                        index_var_cache[var_index] = tmp_info
                        # 用于某天的检修任务不超过多少个
                        rule_var_cache.setdefault(rule_id, []).append(var_index)
                        month_vars.setdefault(month, []).append(var_index)
                        var_index = var_index + 1
                        last_info = tmp_info

                        dev_info['var_array'].append(tmp_info)

                    if last_info:
                        last_info["is_last_repair_day"] = True

                if len(dev_info['var_array']) > 0:
                    dev_info_array.append(dev_info)
                else:
                    _logger.info('设备{dev_no}没有排次信息'.format(dev_no=dev['dev_no']))

            info.update({
                "year": year,
                "start_month": start_month,
                "dev_info_array": dev_info_array,
                "constrains": info["constrains"],
                "start_val": start_date.day_of_year,
                "end_val": end_date.day_of_year,
                # index 多加一个1刚好是数量
                "var_num": var_index,
                "holidays": holidays,
                # 工班数量
                "work_class_count": info["work_class_count"],
                "index_var_cache": index_var_cache,
                "rule_var_cache": rule_var_cache,
            })

            return {
                "cmd": "plan_year",
                "data": info
            }
        except Exception as e:
            _logger.info(e)
            raise e

    @api.model
    def deal_plan_data(self, info, json_result):
        '''
        处理前端返回的计算数据
        :return:
        '''
        if json_result['status'] != 200:
            raise exceptions.ValidationError('计算出错! {error}'.format(
                error=json_result['error']))

        year = int(info['year'])
        start_month = int(info['start_month'])
        dev_info_array = info['dev_info_array']

        start_date = pendulum.date(year, start_month, 1)
        year_start_date = pendulum.date(year, 1, 1)

        year_plan_id = info["year_plan_id"]
        plan_id = 'metro_park_maintenance.year_plan, {plan_id}'.format(
            plan_id=year_plan_id)

        result = json_result['datas']

        # 更新规则数据
        vals = []
        for info in dev_info_array:
            dev_id = info['dev_id']
            for var in info['var_array']:
                var_index = var["index"]
                rule_id = var['rule_id']
                # 属于一件中的哪天
                val = result[var_index]
                tmp_date = year_start_date.add(days=val - 1)

                # 这里根据dev date作为标识
                date_str = tmp_date.format("YYYY-MM-DD")
                vals.append({
                    'dev': dev_id,
                    'rule': rule_id,
                    'data_source': 'year',
                    'date': date_str,
                    'repair_day': var['repair_day'],
                    'repair_num': var['repair_num'],
                    'plan_id': plan_id
                })

        # 先删除原有的数据, active仅对odoo的orm有效
        old_records = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', plan_id),
                     ('date', '>=', start_date.format('YYYY-MM-DD'))])
        old_records.write({
            "active": False
        })

        # 创建新的计划, 创建时会自动去创建plan_data
        return self.env["metro_park_maintenance.rule_info"].create(vals)

    def unlink(self):
        '''
        必需要日计划删除完成以后才能删除周计划
        :return:
        '''
        # 检查月计划是否已删除
        for record in self:
            year = record.year
            records = self.env["metro_park_maintenance.month_plan"] \
                .search([("year", '=', year)])
            if len(records) > 0:
                raise exceptions.ValidationError("{year}年计划有关联的月计划，"
                                                 "请先删除相关联的月计划".format(year=year))
        # 删除计划数据
        for record in self:
            start_date = pendulum.date(record.year, 1, 1).format('YYYY-MM-DD')
            end_date = pendulum.date(record.year, 12, 31).format('YYYY-MM-DD')
            # 先删除具体信息
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([('date', '=', start_date),
                         ('date', '=', end_date),
                         ('data_source', '=', 'year')])
            records.write({
                "active": False
            })

            # 对应用很多设备, 只有具体信息删除完了以后才删除计划数据
            records = self.env["metro_park_maintenance.plan_data"] \
                .search([("date", '>=', start_date), ("date", "<=", end_date)])
            for tmp_record in records:
                if tmp_record.rule_infos:
                    tmp_record.rule_infos.write({
                        "active": False
                    })
                    tmp_record.write({
                        "active": False
                    })

        # 删除年计划汇总
        for record in self:
            year = record.year
            records = self.env["metro_park_maintenance.year_plan_summary"] \
                .search([('year', '=', year)])
            records.unlink()

        self.write({
            "active": False
        })

        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('{year}年，年计划删除成功!'.format(year=year))

    @api.multi
    def publish_plan(self):
        '''
        年计划发布
        :return:
        '''
        self.ensure_one()
        self.state = "published"
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('year', '=', self.year), ('data_source', '=', 'year')])
        rule_infos.write({
            "state": "published"
        })
        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('{year}年，年计划发布成功!'.format(year=self.year))

        # 年计划推送给pms
        try:
            use_pms_maintaince = self.env['metro_park_base.system_config'].search_read(
                [])[0].get('start_pms')
        except Exception as e:
            _logger.info('pms基础信息未配置' + str(e))
        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'Y', '1')
        except Exception as error:
            _logger.error('PMS接口获取失败 {error}'.format(error=error))

    @api.multi
    def view_year_plan_summary_action(self):
        '''
        查看年计划
        :return:
        '''
        tree_id = self.env.ref(
            'metro_park_maintenance.year_plan_summary_list').id

        # 首先同步数据
        self.env['metro_park_maintenance.year_plan_summary'] \
            .check_records(self.year)

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "metro_park_maintenance.year_plan_summary",
            "name": "查看年计划",
            "context": {
                "year": self.year, "view_year_plan": True, 'create_plan_id': self.id
            },
            "views": [[tree_id, "tree"]],
            "domain": [("year", "=", self.year)]
        }

    @api.multi
    def view_year_plan_editor_action(self):
        '''
        年计划编辑
        :return:
        '''
        return {
            "type": "ir.actions.client",
            "tag": "year_plan_editor_action",
            "name": "年计划编辑",
            "params": {
                "year_plan_id": self.id
            }
        }

    @api.multi
    def view_month_plan_time_line(self):
        '''
        查看年计划，时间轴
        :return:
        '''
        return {
            "type": "ir.actions.client",
            'tag': 'year_plan_time_line',
            "name": "年计划",
            'params': {
                'year': self.year
            }
        }

    @api.model
    def get_plan_data(self, year_plan_id):
        '''
        取得计划数据, 年的话只显示每个月的统计量, 分组的话是按设备进行分组
        :return:
        '''
        record = self.browse(year_plan_id)
        year = record.year

        # 取得开始日期和结束日期
        start_date = pendulum.date(year, 1, 1).format('YYYY-MM-DD')
        end_date = pendulum.Date(year, 12, 31).format('YYYY-MM-DD')

        # 取得所有设备
        model = self.env['metro_park_maintenance.plan_data']
        records = model.search([('year', '=', year)])

        # 对修程进行缓存
        rule_model = self.env['metro_park_maintenance.repair_rule']
        rules = rule_model.search([])
        rule_cache = {rule.id: rule for rule in rules}

        # 对检技通进行缓存
        tmp_rule_model = self.env['metro_park_maintenance.repair_tmp_rule']
        tmp_rules = tmp_rule_model.search([])
        tmp_rule_cache = {rule.id: rule for rule in tmp_rules}

        rst = {
            'year': year,
            'start_date': start_date,
            'end_date': end_date,
        }

        # 组装数据
        groups = {}
        for record in records:
            if len(record.rule_infos) > 0:
                start_time = pendulum.parse(str(record.date))
                rule_infos = record.rule_infos
                for info in rule_infos:
                    if info["rule_type"] == "normal":
                        rule = rule_cache[info["rule_id"]]
                        repair_days = rule.repair_days
                        end_time = start_time.add(days=repair_days)
                        groups.setdefault(record.dev.id, []).append({
                            'rule_type': info["rule_type"],
                            'start': start_time.format('YYYY-MM-DD'),
                            'end': end_time.format('YYYY-MM-DD'),
                            'content': rule.content
                        })
                    else:
                        rule = tmp_rule_cache[info["rule_id"]]
                        groups.setdefault(record.dev.id, []).append({
                            'rule_type': info["rule_type"],
                            'start': rule.start_date.format('YYYY-MM-DD'),
                            'end': rule.end_date.format('YYYY-MM-DD'),
                            'content': rule.content
                        })

        rst['groups'] = groups
        return rst

    @api.multi
    def export_year_plan(self):
        '''
        导出年计划
        :return:
        '''
        return {
            'name': '年计划下载',
            'type': 'ir.actions.act_url',
            'url': '/getPlanDataImportWizard/%s' % self.year
        }

    @api.multi
    def import_year_plan(self):
        '''
        导入年计划
        :return:
        '''
        form_id = self.env.ref("metro_park_maintenance.year_plan_import_wizard_form").id

        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'context': {
                'default_year_plan_id': self.id
            },
            'res_model': "metro_park_maintenance.year_plan_import_wizard",
            'target': 'new',
        }

    @api.model
    def get_year_plan_info(self, year):
        '''
        取得年计划信息
        :return:
        '''
        info = self.search_read([('year', '=', year)])
        return info[0]

    @api.multi
    def clear_year_info(self, start_month, end_month):
        '''
        清除年计划内容, 清除相应的年计划内容，直接归档
        :return:
        '''
        start_date = pendulum.date(self.year, start_month, 1)
        week_day, month_count_day = calendar.monthrange(self.year, end_month)
        end_date = pendulum.date(self.year, end_month, month_count_day)
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('plan_id', '=', 'metro_park_maintenance.year_plan, {plan_id}'.format(plan_id=self.id)),
                     ('date', '>=', start_date.format('YYYY-MM-DD')),
                     ('date', '<=', end_date.format('YYYY-MM-DD'))])
        rule_infos.write({
            "active": False
        })

    @api.multi
    def reback_plan(self):
        '''
        撤回计划
        :return:
        '''
        year = self.year
        month_plans = self.env["metro_park_maintenance.month_plan"] \
            .search([('year', '=', year), ('state', '=', 'published')])
        if len(month_plans) > 0:
            raise exceptions.ValidationError('已经有月计划发布, 无`法进行撤回!')
        self.state = 'draft'
        self.env['metro_park_maintenance.plan_log'] \
            .sudo() \
            .add_plan_log('{year}年，看计划撤回成功!'.format(year=self.year))

        # 撤销年计划
        sys_config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = sys_config.get('start_pms', False)

        try:
            if use_pms_maintaince == 'yes':
                self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'Y', '3')
        except Exception as error:
            _logger.error('PMS接口获取失败 {error}'.format(error=error))

    @api.model
    def edit_dev_rules(self, year_plan_id, dev_id):
        '''
        编辑设备的修程信息
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.rule_info",
            'view_mode': 'tree',
            "target": "new",
            'context': {
                "default_dev_id": dev_id,
                "default_plan_id": 'metro_park_maintenance.year_plan, {plan_id}'
                    .format(plan_id=year_plan_id)
            },
            'domain': [('dev.id', '=', dev_id),
                       ('plan_id', '=', 'metro_park_maintenance.year_plan, {plan_id}'
                        .format(plan_id=year_plan_id))],
            "views": [[self.env.ref('metro_park_maintenance.dev_year_rule_edit').id, 'tree']]
        }
