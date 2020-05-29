# -*- coding: utf-8 -*-


from odoo import models, fields, api, exceptions
import pendulum
from odoo.exceptions import ValidationError


class HistoryMiles(models.Model):
    '''
    历史公里数(月)
    '''
    _name = 'metro_park_maintenance.history_miles'
    _description = '历史公里数'

    train_dev = fields.Many2one(string='车辆', readonly=True,
                                comodel_name='metro_park_maintenance.train_dev')
    total_miles = \
        fields.Float(string='历史公里数', help="总公里数, tcms 同步过来的当前公里数")

    last_repair_miles = \
        fields.Float(string="上次里程检公里数", readonly=True, help="里程检完成以后公里数")

    miles_after_last_repair = \
        fields.Float(string="距离上次里程检后的公里数", readonly=True)

    @api.model
    def _get_year_selection(self):
        '''
        取得年份
        :return: 
        '''
        rst = []
        for year in range(2018, 2050):
            rst.append((year, str(year)))
        return rst

    year = fields.Selection(string='年', selection=_get_year_selection)
    year_target_miles = fields.Float(string="年度目标公里数")

    month = fields.Selection(string='月',
                             selection=[(1, '1月'), (2, '2月'),
                                        (3, '3月'), (4, '4月'),
                                        (5, '5月'), (6, '6月'),
                                        (7, '7月'), (8, '8月'),
                                        (9, '9月'), (10, '10月'),
                                        (11, '11月'), (12, '12月')])
    month_target_miles = fields.Float(string="月度目标公里数", readonly=True)
    year_month = fields.Date(string="月份", compute="compute_year_month")

    # 每日公里数, 未来的天数的预估值
    day1 = fields.Float(string="1号", default=0)
    day1_is_manual = fields.Boolean(string="day1是否手动", default=False)

    day2 = fields.Float(string="2号", default=0)
    day2_is_manual = fields.Boolean(string="day2是否手动", default=False)

    day3 = fields.Float(string="3号", default=0)
    day3_is_manual = fields.Boolean(string="day3是否手动", default=False)

    day4 = fields.Float(string="4号", default=0)
    day4_is_manual = fields.Boolean(string="day4是否手动", default=False)

    day5 = fields.Float(string="5号", default=0)
    day5_is_manual = fields.Boolean(string="day5是否手动", default=False)

    day6 = fields.Float(string="6号", default=0)
    day6_is_manual = fields.Boolean(string="day6是否手动", default=False)

    day7 = fields.Float(string="7号", default=0)
    day7_is_manual = fields.Boolean(string="day7是否手动", default=False)

    day8 = fields.Float(string="8号", default=0)
    day8_is_manual = fields.Boolean(string="day8是否手动", default=False)

    day9 = fields.Float(string="9号", default=0)
    day9_is_manual = fields.Boolean(string="day9是否手动", default=False)

    day10 = fields.Float(string="10号", default=0)
    day10_is_manual = fields.Boolean(string="day10是否手动", default=False)

    day11 = fields.Float(string="11号", default=0)
    day11_is_manual = fields.Boolean(string="day11是否手动", default=False)

    day12 = fields.Float(string="12号", default=0)
    day12_is_manual = fields.Boolean(string="day12是否手动", default=False)

    day13 = fields.Float(string="13号", default=0)
    day13_is_manual = fields.Boolean(string="day13是否手动", default=False)

    day14 = fields.Float(string="14号", default=0)
    day14_is_manual = fields.Boolean(string="day14是否手动", default=False)

    day15 = fields.Float(string="15号", default=0)
    day15_is_manual = fields.Boolean(string="day15是否手动", default=False)

    day16 = fields.Float(string="16号", default=0)
    day16_is_manual = fields.Boolean(string="day16是否手动", default=False)

    day17 = fields.Float(string="17号", default=0)
    day17_is_manual = fields.Boolean(string="day17是否手动", default=False)

    day18 = fields.Float(string="18号", default=0)
    day18_is_manual = fields.Boolean(string="day18是否手动", default=False)

    day19 = fields.Float(string="19号", default=0)
    day19_is_manual = fields.Boolean(string="day19是否手动", default=False)

    day20 = fields.Float(string="20号", default=0)
    day20_is_manual = fields.Boolean(string="day20是否手动", default=False)

    day21 = fields.Float(string="21号", default=0)
    day21_is_manual = fields.Boolean(string="day21是否手动", default=False)

    day22 = fields.Float(string="22号", default=0)
    day22_is_manual = fields.Boolean(string="day22是否手动", default=False)

    day23 = fields.Float(string="23号", default=0)
    day23_is_manual = fields.Boolean(string="day23是否手动", default=False)

    day24 = fields.Float(string="24号", default=0)
    day24_is_manual = fields.Boolean(string="day24是否手动", default=False)

    day25 = fields.Float(string="25号", default=0)
    day25_is_manual = fields.Boolean(string="day25是否手动", default=False)

    day26 = fields.Float(string="26号", default=0)
    day26_is_manual = fields.Boolean(string="day26是否手动", default=False)

    day27 = fields.Float(string="27号", default=0)
    day27_is_manual = fields.Boolean(string="day27是否手动", default=False)

    day28 = fields.Float(string="28号", default=0)
    day28_is_manual = fields.Boolean(string="day28是否手动", default=False)

    day29 = fields.Float(string="29号", default=0)
    day29_is_manual = fields.Boolean(string="day29是否手动", default=False)
    day29_visible = fields.Boolean(string="29号是否可见", compute="_compute_visible")

    day30 = fields.Float(string="30号", default=0)
    day30_is_manual = fields.Boolean(string="day30是否手动")
    day30_visible = fields.Boolean(string="30号是否可见", compute="_compute_visible")

    day31 = fields.Float(string="31号", default=0)
    day31_is_manual = fields.Boolean(string="day31是否手动")
    day31_visible = fields.Boolean(string="31号是否可见", compute="_compute_visible")

    run_miles = fields.Float(string='运行里程', compute="_compute_run_miles", default="0")

    positive_offset_miles = fields.Float(string='正向偏差里程', compute="_compute_run_miles", default="0")
    negative_offset_miles = fields.Float(string='负向偏差里程', compute="_compute_run_miles", default="0")

    remark = fields.Char(string='备注')
    lock_days = fields.Char(string='手动输入公里数的日期')

    def _compute_visible(self):
        '''
        计算29\30\31是否显示, 根据当前的月数进行计算
        :return:
        '''
        for record in self:
            if record.year and record.month:
                year_month = pendulum.datetime(int(record.year), int(record.month), 1)
                days_in_month = year_month.days_in_month
                if days_in_month < 29:
                    record.day29_visible = True
                    record.day30_visible = True
                    record.day31_visible = True
                elif days_in_month < 30:
                    record.day30_visible = True
                    record.day31_visible = True
                elif days_in_month < 31:
                    record.day31_visible = True

    def _compute_run_miles(self):
        '''
        计算运行里程
        :return:
        '''
        rule = self.env.ref("metro_park_base.repair_rule_l")
        for record in self:
            record.run_miles = rule.run_miles
            record.positive_offset_miles = rule.positive_offset_miles
            record.negative_offset_miles = rule.negative_offset_miles

    @api.depends('year', 'month')
    def compute_year_month(self):
        '''
        计算年月
        :return:
        '''
        for record in self:
            if record.year and record.month:
                tem_date = pendulum.Date(int(record.year), int(record.month), 1)
                record.year_month = tem_date.format("YYYY-MM-DD")

    @api.model
    def check_dev(self, year, month):

        # 取得所有的电客车
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train')
        dev_model = self.env['metro_park_maintenance.train_dev']
        devs = dev_model.search([("dev_type", '=', dev_type_electric_train.id)])
        dev_ids = devs.ids

        # 查找没有记录的设备
        records = self.search([('year', '=', year), ('month', '=', month)])
        exits_ids = records.mapped('train_dev.id')
        diff_ids = list(set(dev_ids).difference(set(exits_ids)))
        vals = []
        tmp_devs = dev_model.browse(diff_ids)
        for dev in tmp_devs:
            for month in range(12):
                vals.append({
                    'train_dev': dev.id,
                    'year': year,
                    'month': month + 1
                })
        self.create(vals)

    @api.model
    def get_miles_predict_action(self, **kwargs):
        '''
        默认当前月，如果没有当前月的则添加, 说明，这种在搜索时先要检查并创建
        :return:
        '''
        today = pendulum.today('UTC')

        # 检查是否添加记录
        year = today.year
        month = today.month
        self.check_dev(year, month)

        tree_id = self.env.ref(
            'metro_park_maintenance.history_miles_list').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "metro_park_maintenance.history_miles",
            "name": "公里数预估",
            "views": [[tree_id, "tree"]],
            "context": {'_search_default_year': year, '_search_default_month': month}
        }

    @api.multi
    def year_miles_edit(self):
        '''
        年度目标公里数修改form
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.history_miles",
            'view_mode': 'form',
            'res_id': self.id,
            'context': {
                'form_view_initial_mode': 'edit'
            },
            'target': 'new',
            "views": [[self.env.ref('metro_park_maintenance.history_miles_wizard_form').id, "form"]]
        }

    def write(self, values, compute=False):
        '''
        重写，如果需要重新计算则调用重新计算函数
        :param values:
        :param compute:
        :return:
        '''
        if not compute:
            self.compute_month_miles(train_id=self.train_dev.id, values=values)

        return super(HistoryMiles, self).write(values)

    @api.multi
    def compute_month_miles(self, train_id, values):
        """
        根据年度目标修改月度目标，同时修改这个月每天的预估公里
        :param train_id:
        :param values:
        :return:
        """
        today_time, year, month, day, days_in_month = self.get_year_month_day()  # 取出时间
        if self.month != month:
            return

        # 写入历史公里数
        if month == 1:
            total_year = year - 1
            total_month = 12
        else:
            total_year = year
            total_month = month - 1

        last_month = self.env['metro_park_maintenance.history_miles'] \
            .search([('train_dev', '=', train_id),
                     ('year', '=', total_year),
                     ('month', '=', total_month)])

        # 先把历史数据写入，方便后面取用
        last_day = pendulum.date(total_year, total_month, 1).days_in_month
        self.write({'total_miles': getattr(last_month, 'day%s' % last_day)}, True)

        # 如果是重新设置年度目标公里数
        if 'year_target_miles' in values:
            # 本年首月数据
            first_month = self.env['metro_park_maintenance.history_miles'] \
                .search([('train_dev', '=', train_id),
                         ('year', '=', year),
                         ('month', '=', 1)])
            # 计算本月以前已跑公里数
            left_miles = values['year_target_miles'] - (self.day1 - first_month.day1)
            # 计算出月度目标
            month_target_miles = left_miles / (13 - self.month)
            # 每月的公里数
            values['month_target_miles'] = month_target_miles
        elif self.year_target_miles:
            values['month_target_miles'] = self.month_target_miles
        else:
            # raise ValidationError("请先设置年度目标公里数！")
            return

        # 获取这个月剩余所有天数的列表
        day_field_names = self.get_day_field_names()

        # 把所选数据从今天开始所有day数据取出生成dict
        day_info = {}
        # 这里减2是因为要取前边的数据
        for day_field_name in day_field_names[day - (1 if day == 1 else 2):]:
            day_info[day_field_name] = getattr(self, day_field_name)
            day_info['%s_is_manual' % day_field_name] = getattr(self, '%s_is_manual' % day_field_name)

        # 从values中获取被修改了的天，并将其锁定
        edit_days = [day_field_name for day_field_name in day_field_names[day - 1:] if day_field_name in values]
        if edit_days:
            for edit_day in edit_days:
                values['%s_is_manual' % edit_day] = True
            if self.lock_days:
                history_mile_locks = eval(self.lock_days) + edit_days
            else:
                history_mile_locks = edit_days
        else:
            history_mile_locks = eval(self.lock_days or "[]") or []

        # 取出这个月的检修天数, 并设置成为lock, 这样才不支分
        repair_days = self.env['metro_park_maintenance.rule_info'] \
            .search([('dev', '=', self.train_dev.id),
                     ('year', '=', year),
                     ('month', '=', month),
                     ('day', '>=', day),
                     ('state', '=', 'published')])
        repair_list = []
        for day_field_name in repair_days:
            values['day%s_is_manual' % day_field_name.day] = True
            repair_list.append('day%s' % day_field_name.day)

        history_mile_locks = [i for i in history_mile_locks if (i >= 'day%s' % day) and i not in repair_list]

        # 合并数据字典，整理出所有的数据
        for key, value in values.items():
            day_info[key] = value

        # 维修日期的天数和之前是一样的
        for day_field_name in repair_days:
            day_info['day%s' % day_field_name.day] = day_info[
                'day%s' % (day_field_name.day - 1)] if day_field_name.day > 1 else self.total_miles

        # 可以预估公里数的天
        unlock_days = []
        for day_field_name, locked in day_info.items():
            day_data = day_field_name.split("_")[0]
            if locked is False:
                unlock_days.append(day_data)

        if history_mile_locks:
            day_info['lock_days'] = history_mile_locks
            # 判断当天是否已被锁定，如果是的话基础数据为当天，如果不是基础数据为昨天
            if ('day%s' % day) not in history_mile_locks:
                history_mile_locks.append('day%s' % (day - 1))
            # 查看月末是否被锁定，没被锁定就按照月度目标来处理
            if ('day%s' % days_in_month) not in history_mile_locks:
                history_mile_locks.append('day%s' % days_in_month)
                day_info['day%s' % days_in_month] = self.total_miles + day_info['month_target_miles']

            history_mile_locks = sorted(history_mile_locks)
            for index in range(len(history_mile_locks)-1):
                start_date = int(history_mile_locks[index].split('y')[1])
                end_date = int(history_mile_locks[index+1].split('y')[1])
                dif_day = end_date - start_date
                if dif_day > 1:
                    basic_data = day_info[history_mile_locks[index]]
                    miles = day_info[history_mile_locks[index+1]] - day_info[history_mile_locks[index]]
                    if miles > 0:
                        day_miles = (miles / dif_day)
                    else:
                        day_miles = 0
                        day_info[history_mile_locks[index + 1]] = \
                            day_info[history_mile_locks[index]]
                    for tmp_day in range(start_date + 1, end_date):
                        day_info['day%s' % tmp_day] = \
                            basic_data + day_miles * (tmp_day - start_date)
        else:
            # 预估量=(本月目标-本月已跑)/(本月剩余天数-锁定天数)
            month_miles = getattr(self, 'day%s' % (day - 1)) - self.total_miles  # 本月已跑

            # 平均公里数 = (月公里数 - 已经跑了的公里数) / (剩余的天数 - 检修天数)
            day_miles = (day_info['month_target_miles'] - month_miles) / (1 + days_in_month - day - len(repair_days))

            # 判断日期，决定基础数据和补足天数，在这个数据的基础(之前的公里数)上加上预估值
            if day_info['day%s' % day] == 0:
                if day == 1:
                    basic_data = self.total_miles
                    factor = 1
                else:
                    basic_data = day_info['day%s' % day]
                    factor = 1
            else:
                if day_info['day%s_is_manual' % day] is True:
                    basic_data = day_info['day%s' % day]
                    factor = 0
                elif day == 1:
                    basic_data = self.total_miles
                    factor = 1
                else:
                    basic_data = day_info['day%s' % (day - 1)]
                    factor = 1

            for day_field_name in unlock_days:
                dif = int(day_field_name.split('day')[1]) - day + factor
                day_info[day_field_name] = basic_data + (day_miles * dif)

        self.write(day_info, True)

    @api.multi
    def daily_miles(self, train_id, values):
        """
        tcms接口会调用这个方法，把每天的实际公里数写入数据库
        :param train_id:
        :param values:
        :param miles:
        :return:
        """
        today_time = pendulum.today()
        year = today_time.year
        month = today_time.month
        record = self.env['metro_park_maintenance.history_miles'] \
            .search([('train_dev', '=', train_id),
                     ('year', '=', year),
                     ('month', '=', month)], limit=1)
        record.write(values)

    @api.model
    def get_year_month_day(self):
        '''
        取得年度目标公里数
        :return:
        '''
        today_time = pendulum.today()
        year = today_time.year
        month = today_time.month
        today = today_time.day
        days_in_month = today_time.days_in_month
        return today_time, year, month, today, days_in_month

    @api.model
    def get_day_field_names(self):
        '''
        获取这个月的day字段列表
        :return:
        '''
        if self.year and self.month:
            year_month = pendulum.datetime(int(self.year), int(self.month), 1)
            days_in_mon = year_month.days_in_month
            fields_name = ['day' + str(i + 1) for i in range(days_in_mon)]
            return fields_name

    @api.model
    def set_year_miles(self):
        """
        批量设置车辆目标公里数
        :return:
        """
        form_id = self.env.ref("metro_park_maintenance.year_miles_set_wizard_form").id
        return {
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': "metro_park_maintenance.train_miles_set_wizard",
            'target': 'new',
        }

    @api.model
    def get_day_mile(self, train_id, date_str):
        '''
        取得具体某天的预估公里数
        :return:
        '''
        tmp_date = pendulum.parse(date_str)

        year = tmp_date.year
        month = tmp_date.month
        day = tmp_date.day

        day_str = 'day{day}'.format(day=day)
        record = self.search([(year, '=', year),
                              ('month', '=', month),
                              ('train_dev', '=', train_id)])

        if not record:
            raise exceptions.ValidationError('{date}未设置预估公里数!'.format(date=day_str))

        return {
            'dev_id': train_id,
            'predict_miles': record[day_str],
            'last_repair_miles': record['last_repair_miles']
        }

    @api.model
    def get_devs_day_miles(self, train_devs, date_str):
        '''
        取得具体某天的预估公里数, 批量获取
        :return:
        '''
        tmp_date = pendulum.parse(date_str)

        year = tmp_date.year
        month = tmp_date.month
        day = tmp_date.day

        day_str = 'day{day}'.format(day=day)
        records = self.search([('year', '=', year),
                               ('month', '=', month),
                               ('train_dev', 'in', train_devs)])

        if not records:
            raise exceptions.ValidationError('{date}未设置预估公里数!'.format(date=day_str))

        rst = {}
        for record in records:
            rst[record.train_dev.id] = {
                'dev_id': record.train_dev.id,
                'predict_miles': record[day_str],
                'last_repair_miles': record['last_repair_miles'],
                'total_miles': record['total_miles']
            }

        # 新添设备可能没有设置公里数
        devs = self.env["metro_park_maintenance.train_dev"].browse(train_devs)
        for dev in devs:
            if dev.id not in train_devs:
                raise exceptions.ValidationError("设备{dev}没有设置当日预估里程!".format(dev=dev))

        return rst

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """
        重写，搜索的时候建立新数据
        """
        year = None
        month = None
        for tmp in domain:
            if len(tmp) == 3 and tmp[0] == 'year':
                year = int(tmp[2])
            if len(tmp) == 3 and tmp[0] == 'month':
                month = int(tmp[2])

        if year and month:
            self.check_dev(year, month)

        # 要重新计算下
        return super(HistoryMiles, self).search_read(domain, fields, offset, limit, order)

    @api.model
    def get_history_miles(self, date):
        '''
        取得公里数预估, 10号线的处理方式
        计算公式
        预估公里数 = 上一天的公里数 + 当天计划车跑的公里数
        :return:
        '''
        tmp_date = pendulum.parse(str(date))

        year = tmp_date.year
        month = tmp_date.month
        day = tmp_date.day

        # 检查, 防止没有数据
        self.check_dev(year, month)

        records = self.search([('year', '=', year), ('month', '=', month)])
        result = {}
        field_name = 'day{day}'.format(day=day)
        for record in records:
            result[record.train_dev.id] = record[field_name]

        return result







