
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum


class YearPlanComputeWizard(models.TransientModel):
    '''
    年计划计算向导
    说明，梯形排列的情况在修次那里去处理，提供一个初始化函数
    '''
    _name = 'year_plan_compute_wizard'

    @api.model
    def get_default_month(self):
        '''
        取得默认的月份
        :return:
        '''
        return self.env.ref("metro_park_maintenance.month_1").id

    @api.model
    def get_default_end_month(self):
        '''
        取得默认的月份
        :return:
        '''
        return self.env.ref("metro_park_maintenance.month_12").id

    month = fields.Many2one(comodel_name="metro_park_maintenance.month",
                            required=True,
                            string="开始月份",
                            default=get_default_month)

    end_month = fields.Many2one(comodel_name="metro_park_maintenance.month",
                                required=True,
                                string="开始月份",
                                default=get_default_end_month)

    # 工班数量限制
    work_class_count = fields.Integer(string="工班数量")

    # 计算服务器
    calc_host = fields.Char(string="计算服务器地址", default="ws://127.0.0.1:9520")

    # 每个月的检修数量
    month_repair_count = fields.One2many(comodel_name="metro_park_maintenance.month_repair_count",
                                         inverse_name="compute_wizard_id",
                                         string="月检修信息")

    @api.model
    def default_rule_constrain(self):
        records = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', '=', 'year')])
        rst = [(5, 0, 0)]
        for record in records:
            rst.append((0, 0, {
                "rule": record.id,
                "count": record.max_plan_per_day
            }))
        return rst

    # 规程数量限制
    rule_count_constrain = \
        fields.One2many(comodel_name="metro_park_maintenance.rule_count_constrain",
                        default=default_rule_constrain,
                        inverse_name="year_compute_wizard",
                        string="数量限制", help='年计划时可以不考虑，月计划再进行考虑, 月计划需要根据实际情况重新排列')

    @api.multi
    def get_wizard_data(self):
        constrains = {}
        for constrain in self.rule_count_constrain:
            constrains[constrain.rule.id] = int(constrain.count)

        if self.month.val > self.end_month.val:
            raise exceptions.Warning('开始月份超过结束月份!')

        return {
            'month': self.month.val,
            'end_month': self.end_month.val,
            'work_class_count': self.work_class_count,
            'constrains': constrains,
            'calc_host': self.calc_host,
            'month_repair_count': self.month_repair_count.read()
        }

    @api.model
    def get_work_class_count(self):
        '''
        取得工班数量
        :return:
        '''
        count = self.env["funenc.wechat.department"].get_work_class_count() or 5
        return count

    @api.model
    def get_compute_host(self):
        '''
        取得计算host
        :return:
        '''
        config = self.env["metro_park_base.system_config"].get_configs()
        calc_host = config["calc_host"] or "ws://127.0.0.1:9520"
        return calc_host

    @api.onchange("month")
    def on_change_start_month(self):
        ''''
        计算每个月的平均数量，允许有误差
        '''
        # 查询特殊日期配置, 黑名单
        special_days = \
            self.env['metro_park_maintenance.holidays'].search([])
        special_days_cache = {record.date: True for record in special_days}

        year_plan_id = self.env.context.get("year_plan_id", None)
        if not year_plan_id:
            raise exceptions.ValidationError("上下文中没有找年信息!")

        year_plan = self.env["metro_park_maintenance.year_plan"].browse(year_plan_id)
        year = year_plan.year

        devs = self.env["metro_park_maintenance.train_dev"].search([])

        # 取得白名单配置
        year_start = pendulum.date(year, 1, 1).format("YYYY-MM-DD")
        year_end = pendulum.date(year, 12, 31).format("YYYY-MM-DD")
        white_list = self.env["metro_park_maintenance.white_list"].search(
            [('date', ">=", year_start), ('date', "<=", year_end)])
        white_dates = white_list.mapped("date")

        # 取得一年中的星期六和星期天的索引，这些要排除除值的范围
        holidays = []

        # 收集所有的周六周天和节假日
        plan_start_date = pendulum.date(year, self.month.val, 1)
        for month in range(self.month.val, 13):
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

        holiday_count = len(holidays)
        month_count = 12 - self.month.val + 1
        total_repair = month_count * len(devs)
        plan_end_date = pendulum.date(year, 12, 31)
        delta = plan_end_date - plan_start_date
        days = delta.days - holiday_count
        per_day_count = total_repair / days

        vals = [(5, 0, 0)]
        for month in range(self.month.val, 13):
            tmp_month = pendulum.date(year, month, 1)
            tmp_days = tmp_month.days_in_month
            month_days = tmp_month.days_in_month
            holidays = 0
            for tmp_day in range(1, tmp_days + 1):
                tmp_date = pendulum.date(year, month, tmp_day)
                last_plan_date_str = tmp_date.format('YYYY-MM-DD')
                week_day = tmp_date.day_of_week
                if (week_day == 0 or week_day == 6) and last_plan_date_str not in white_dates:
                    holidays += 1
                elif last_plan_date_str in special_days_cache and last_plan_date_str not in white_dates:
                    holidays += 1
            left_days = month_days - holidays
            repair_count = int(left_days * per_day_count)
            vals.append((0, 0, {
                "month": month,
                "count": repair_count
            }))

        self.month_repair_count = vals

        if self.month and self.end_month and self.month.val > self.end_month.val:
            self.end_month = False
