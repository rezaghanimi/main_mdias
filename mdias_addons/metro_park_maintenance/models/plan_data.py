# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum
from . import util
import time


class PlanData(models.Model):
    '''
    计划数据, 所有的计划数据都放在这个里面, 年计划创建的时候就生成了全年的数据，
    因为年计划就要计算，所以提前添加
    '''
    _name = 'metro_park_maintenance.plan_data'

    dev = fields.Many2one(string="设备",
                          comodel_name="metro_park_maintenance.train_dev")
    dev_no = fields.Char(related="dev.dev_no")
    planed = fields.Boolean(string="是否计划", default=False, help='这个用于控制是否显示')

    # 计划id
    plan_id = fields.Reference(string="计划id",
                               selection=[('metro_park_maintenance.day_plan', 'metro_park_maintenance.day_plan'),
                                          ('metro_park_maintenance.month_plan', 'metro_park_maintenance.month_plan'),
                                          ('metro_park_maintenance.week_plan', 'metro_park_maintenance.week_plan'),
                                          ('metro_park_maintenance.year_plan', 'metro_park_maintenance.year_plan')])

    year = fields.Integer(string='年')
    month = fields.Integer(string='月')
    day = fields.Integer(string='日')

    # 用于周计划查询
    week = fields.Integer(string='周',
                          compute='_compute_date', store=True)

    # 用于日期搜索, 所以这里存为store
    date = fields.Date(string='日期',
                       compute='_compute_date',
                       store=True,
                       help="这个主要是便于计算")

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布')],
                             default='draft')

    # 1天可能对应多个修程
    rule_infos = fields.One2many(string='检修信息',
                                 comodel_name='metro_park_maintenance.rule_info',
                                 inverse_name='plan_data')
    active = fields.Boolean(default=True)

    @api.one
    @api.depends('year', 'month', 'day')
    def _compute_date(self):
        '''
        计算日期、周数，便于搜索
        :return:
        '''
        if self.year and self.month and self.day:
            date = pendulum.date(self.year, self.month, self.day)
            self.date = date.format('YYYY-MM-DD')
            self.week = date.week_of_year

    @api.model
    def get_plan_data(self, start_date, end_date):
        '''
        取得计划数据
        :return:
        '''
        records = self.search([('date', '>=', start_date),
                               ('date', '<=', end_date)])
        return records

    @api.model
    def get_month_plan_info(self, month_plan_id):
        '''
        取得月计划数据, 和生产作业的区别是这个不包含周计划的内容
        :return:
        '''
        month_plan = self.env['metro_park_maintenance.month_plan'].browse(month_plan_id)
        plan_state = month_plan.state

        year = month_plan.year
        month = month_plan.month
        domain = [('year', '=', year), ('month', '=', month)]

        rules = self.env['metro_park_maintenance.repair_rule'].search_read(
            [('target_plan_type', 'in', ['year', 'month'])])
        rule_cache = {rule['id']: rule for rule in rules}

        dates = []
        month_obj = pendulum.date(year, month, 1)
        days = month_obj.days_in_month

        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search(domain + [('data_source', '=', 'month'),
                              ('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                                  plan_id=month_plan_id))])
        ids = rule_infos.mapped('plan_data.id')
        records = self.search(domain + [('id', 'in', ids)], order='date asc')

        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"].search(
            [('dev_type', '=', dev_type_electric_train.id)])

        # 日期数据缓存
        weeks = ["日", "一", "二", "三", "四", "五", "六"]
        for day in range(1, days + 1):
            tmp_date_obj = pendulum.date(year, month, day)
            dates.append({
                "date": tmp_date_obj.format('YYYY-MM-DD'),
                "week": weeks[tmp_date_obj.day_of_week]
            })

        plan_data = dict()
        for month_plan in records:
            for info in month_plan.rule_infos:
                rules_info = []
                key = '{dev}_{date}'.format(dev=info.dev.id, date=str(info.date))
                if info.rule and info.rule.id in rule_cache:
                    rule_info = {
                        "rule_no": info.rule.no,
                        "id": info.rule.id,
                        "plan_id": info.id,
                        "date": info.date,
                        "work_class": info.work_class.name if info.work_class else "",
                        "name": '{rule_no}{work_master}'.format(
                            rule_no=info.rule.no,
                            work_master=info.work_class.work_master) if
                        info.work_class and info.work_class.work_master else info.rule.no
                    }
                    rules_info.append(rule_info)

                plan_data[key] = {
                    "dev": info.dev.id,
                    "date": str(info.date),
                    "rules": rules_info
                }

        return {
            'dates': dates,
            'devs': devs.read(["id", "dev_name", "dev_no"]),
            'plan_datas': plan_data,
            'rules': rules,
            'state': plan_state
        }

    @api.model
    def get_month_work_info(self, month_plan_id):
        '''
        生产作业统计表, 相对于月计划多了周计划的内容，同时也支持导入
        :return:
        '''
        month_plan = self.env['metro_park_maintenance.month_plan']\
            .browse(month_plan_id)
        plan_state = month_plan.state

        year = month_plan.year
        month = month_plan.month

        domain = [('year', '=', year), ('month', '=', month)]
        rules = self.env['metro_park_maintenance.repair_rule'].search_read(
            [('target_plan_type', 'in', ['year', 'month', 'week'])])
        rule_cache = {rule['id']: rule for rule in rules}

        def get_rules(tmp_ids):
            rst = []
            for tmp_id in tmp_ids:
                if tmp_id in rule_cache:
                    rst.append(rule_cache[tmp_id])
            return rst

        dates = []
        month_obj = pendulum.date(year, month, 1)
        days = month_obj.days_in_month

        # 这个地方把周计划也取出来了
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search(domain + [('rule.target_plan_type', 'in', ['year', 'month', 'week']),
                              ('plan_id', '=', 'metro_park_maintenance.month_plan, {plan_id}'.format(
                                  plan_id=self.id))])
        ids = rule_infos.mapped('plan_data.id')
        records = self.search(domain + [('id', 'in', ids)], order='date asc')

        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"].search(
            [('dev_type', '=', dev_type_electric_train.id)])

        # 日期数据缓存
        weeks = ["日", "一", "二", "三", "四", "五", "六"]
        for day in range(1, days + 1):
            tmp_date_obj = pendulum.date(year, month, day)
            dates.append({
                "date": tmp_date_obj.format('YYYY-MM-DD'),
                "week": weeks[tmp_date_obj.day_of_week]
            })

        plan_data = dict()
        for month_plan in records:
            key = '{dev}_{date}'.format(dev=month_plan.dev.id, date=str(month_plan.date))
            rule_ids = month_plan.mapped('rule_infos.rule.id')
            plan_data[key] = {
                "dev": month_plan.dev.id,
                "date": str(month_plan.date),
                "rules": get_rules(rule_ids)
            }

        return {
            'dates': dates,
            'devs': devs.read(["id", "dev_name", "dev_no"]),
            'plan_datas': plan_data,
            'rules': rules,
            'state': plan_state
        }

    @api.model
    def get_year_plan_datas(self, year_plan_id):
        '''
        :param year_plan_id:
        :return:
        '''
        plan_data = dict()
        records = self.search(
            [("plan_id", "=", "metro_park_maintenance.year_plan, {plan_id}"
              .format(plan_id=year_plan_id))],
            order='date asc')
        for record in records:
            rule_infos = record.rule_infos
            tmp_infos = []
            for info in rule_infos:
                key = '{dev}_{date}'.format(dev=info.dev.id, date=str(info.date))
                tmp = {
                    "id": info.rule.id,
                    "no": info.rule.no,
                    "repair_num": info.repair_num,
                    "state": info.state,
                    "display": info.rule.no,
                    "repair_day": info.repair_day,
                    "plan_id": info.id
                }
                tmp_infos.append(tmp)
                plan_data[key] = {
                    "dev": info.dev.id,
                    "date": str(info.date),
                    "rules": tmp_infos,
                }
        return {
            'plan_datas': plan_data,
        }

    @api.model
    def get_year_plan_info(self, year_plan_id, start_month, end_month):
        '''
        取得月计划数据, 这里不放临时的, 传进来的plan_id为一个数字
        :return:
        '''
        record = self.env['metro_park_maintenance.year_plan'].browse(year_plan_id)
        year_plan_state = record.state
        year = record.year

        rules = self.env['metro_park_maintenance.repair_rule'].search_read(
            [('target_plan_type', 'in', ['year'])])

        dates = []
        month_obj = pendulum.date(year, start_month, 1)
        start_date = pendulum.date(year, start_month, 1)
        end_date = pendulum.date(year, end_month, 1)
        end_date = pendulum.date(year, end_month, end_date.days_in_month)
        delta = end_date - start_date
        days = delta.days

        records = self.search(
            [("plan_id", "=", "metro_park_maintenance.year_plan, {plan_id}"
              .format(plan_id=year_plan_id))],
            order='date asc')

        # 只处理电客户车数据
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"].search(
            [('dev_type', '=', dev_type_electric_train.id)])

        plan_data = dict()
        for record in records:
            rule_infos = record.rule_infos
            tmp_infos = []
            for info in rule_infos:
                key = '{dev}_{date}'.format(dev=info.dev.id, date=str(info.date))
                tmp = {
                    "id": info.rule.id,
                    "no": info.rule.no,
                    "repair_num": info.repair_num,
                    "state": info.state,
                    "display": info.rule.no,
                    "repair_day": info.repair_day,
                    "plan_id": info.id
                }
                tmp_infos.append(tmp)
                plan_data[key] = {
                    "dev": info.dev.id,
                    "date": str(info.date),
                    "rules": tmp_infos,
                }

        # 日期数据缓存
        weeks = ["日", "一", "二", "三", "四", "五", "六"]
        for day in range(1, days + 1):
            tmp_date_obj = start_date.add(days=day - 1)
            dates.append({
                "date": tmp_date_obj.format('YYYY-MM-DD'),
                "week": weeks[tmp_date_obj.day_of_week]
            })

        months = []
        for month in range(start_month, end_month + 1):
            tmp_month_start = pendulum.date(year, month, 1)
            tmp_month_days = tmp_month_start.days_in_month
            tmp_dates = []
            for index, day in enumerate(range(1, tmp_month_days + 1)):
                tmp_date = pendulum.date(year, month, day)
                tmp_dates.append(tmp_date.format('YYYY-MM-DD'))

            months.append({
                "name": '{month}月'.format(month=month),
                "span": tmp_month_days,
                "dates": dates
            })

        return {
            'dates': dates,
            'months': months,
            'devs': devs.read(["id", "dev_name", "dev_no"]),
            'plan_datas': plan_data,
            'rules': rules,
            'state': year_plan_state,
            'rule_cache': {rule['id']: rule for rule in rules}
        }

    @api.model
    def get_week_plan_info(self, week_plan_id):
        '''
        取得周计划统计
        :return:
        '''
        week_plan_model = self.env['metro_park_maintenance.week_plan']
        week_info = week_plan_model.browse(week_plan_id)
        week_plan_state = week_info.state
        cur_plan_start_date = week_info.start_date

        rules = self.env['metro_park_maintenance.repair_rule'].search_read(
            [('target_plan_type', 'in', ['year', 'month', 'week'])])

        dates = []
        start_date = pendulum.parse(str(week_info.start_date)).subtract(months=1)
        end_date = pendulum.parse(str(week_info.end_date))

        # 这个地方把周计划也取出来了
        rule_infos = self.env["metro_park_maintenance.rule_info"] \
            .search([('rule.target_plan_type', 'in', ['year', 'month', 'week']),
                     ('date', '>=', start_date.format('YYYY-MM-DD')),
                     ('date', '<=', end_date.format('YYYY-MM-DD')),
                     ('data_source', '=', 'week')])
        ids = rule_infos.mapped('plan_data.id')
        records = self.search([('id', 'in', ids)], order='date asc')

        # 只处理电客车数据
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train')
        devs = self.env["metro_park_maintenance.train_dev"].search(
            [('dev_type', '=', dev_type_electric_train.id)])

        plan_data = dict()
        for week_info in records:

            rule_infos = week_info.rule_infos
            tmp_infos = []
            for info in rule_infos:
                key = '{dev}_{date}'.format(dev=info.dev.id, date=str(info.date))
                tmp = {
                    "id": info.rule.id,
                    "no": info.rule.no,
                    "repair_num": info.repair_num,
                    "state": info.state,
                    "display": info.rule.no,
                    "repair_day": info.repair_day,
                    "disabled": True if week_info.date < cur_plan_start_date else False,
                    "plan_id": info.id
                }
                tmp_infos.append(tmp)
                plan_data[key] = {
                    "dev": info.dev.id,
                    "date": str(info.date),
                    "rules": tmp_infos
                }

        # 日期数据缓存
        weeks = ["日", "一", "二", "三", "四", "五", "六"]
        while start_date <= end_date:
            dates.append({
                "date": start_date.format('YYYY-MM-DD'),
                "week": weeks[start_date.day_of_week]
            })
            start_date = start_date.add(days=1)

        return {
            'dates': dates,
            'devs': devs.read(["id", "dev_name", "dev_no"]),
            'plan_datas': plan_data,
            'rules': rules,
            'state': week_plan_state,
            # 便于获取规程信息
            'rule_cache': {rule['id']: rule for rule in rules}
        }

    @api.model
    def get_day_plan_info(self, day_plan_id):
        '''
        取得计划数据, 这里没有考虑检技通的, 扩展了rule_info, 通过type来进行了区分
        :return:
        '''
        record = self.env['metro_park_maintenance.day_plan'] \
            .browse(day_plan_id)

        plan_date = str(record.plan_date)

        records = self.search([('date', '=', plan_date),
                               ('state', '!=', 'delete')],
                              order='date asc')
        rule_info_ids = records.mapped('rule_infos.id')
        rule_infos = self.env['metro_park_maintenance.rule_info'].browse(rule_info_ids)
        rule_infos = rule_infos.read()
        rule_info_cache = util.record_to_cache(rule_infos)

        dev_ids = records.mapped("dev.id")
        devs = self.env['metro_park_maintenance.train_dev'].browse(dev_ids)
        devs = devs.read(fields=['id', 'dev_name'])
        dev_cache = {dev['id']: dev for dev in devs}

        record_data = records.read()
        record_cache = util.record_to_cache(record_data)

        # 按照设备进行分组
        plan_datas = dict()
        for record in records:
            key = record.dev.id
            info_ids = record.mapped('rule_infos.id')
            tmp_record = util.get_cache_datas(record_cache, [record.id])[0]
            # 这里多条数据, 取出来有检技通或是别的
            tmp_record['rule_infos'] = util.get_cache_datas(rule_info_cache, info_ids)
            plan_datas[key] = {
                'dev': dev_cache[key],
                'plan_data': tmp_record
            }

        # 规程
        rules = self.env['metro_park_maintenance.repair_rule'] \
            .search_read([])
        return {
            'plan_datas': plan_datas,
            'devs': devs,
            'plan_date': plan_date,
            "rules": rules
        }
