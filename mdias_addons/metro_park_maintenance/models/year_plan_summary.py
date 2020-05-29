
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class YearPlanSummary(models.Model):
    '''
    年计划月份汇总
    '''
    _name = 'metro_park_maintenance.year_plan_summary'
    _description = '年计划详情'

    year = fields.Integer(string="年")
    train_dev = fields.Many2one(string='车辆',
                                comodel_name='metro_park_maintenance.train_dev')

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布'),
                                        ('deleted', '已删除')],
                             default='draft')

    month1_rules = fields.Many2many(string="1月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month1_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month2_rules = fields.Many2many(string="2月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month2_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month3_rules = fields.Many2many(string="3月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month3_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month4_rules = fields.Many2many(string="4月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month4_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month5_rules = fields.Many2many(string="5月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month5_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month6_rules = fields.Many2many(string="6月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month6_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month7_rules = fields.Many2many(string="7月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month7_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month8_rules = fields.Many2many(string="8月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month8_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month9_rules = fields.Many2many(string="9月",
                                    comodel_name="metro_park_maintenance.rule_info",
                                    relation="summary_month9_and_rule_info_rel",
                                    column1="summary_id",
                                    column2="rule_id",
                                    compute="_compute_month_rules")

    month10_rules = fields.Many2many(string="10月",
                                     comodel_name="metro_park_maintenance.rule_info",
                                     relation="summary_month10_and_rule_info_rel",
                                     column1="summary_id",
                                     column2="rule_id",
                                     compute="_compute_month_rules")

    month11_rules = fields.Many2many(string="11月",
                                     comodel_name="metro_park_maintenance.rule_info",
                                     relation="summary_month11_and_rule_info_rel",
                                     column1="summary_id",
                                     column2="rule_id",
                                     compute="_compute_month_rules")

    month12_rules = fields.Many2many(string="12月",
                                     comodel_name="metro_park_maintenance.rule_info",
                                     relation="summary_month12_and_rule_info_rel",
                                     column1="summary_id",
                                     column2="rule_id",
                                     compute="_compute_month_rules")

    remark = fields.Char(string='备注')
    button = fields.Char(string="操作", help="占位使用字段")

    @api.model
    def check_records(self, year):
        '''
        创建年份数据
        :return:
        '''
        dev_type_electric_train = \
            self.env.ref('metro_park_base.dev_type_electric_train').id
        devs = self.env["metro_park_maintenance.train_dev"]\
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids
        records = self.search([('year', '=', year)])
        old_ids = records.mapped("train_dev.id")
        difference = set(dev_ids).difference(old_ids)
        datas = []
        for tmp_id in difference:
            datas.append({
                "train_dev": tmp_id,
                "year": year
            })
        self.create(datas)

    @api.multi
    def view_detail(self):
        '''
        查看详情
        :return:
        '''
        tree_id = self.env.ref(
            'metro_park_maintenance.year_summary_info_list').id
        form_id = self.env.ref(
            'metro_park_maintenance.year_summary_info_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_maintenance.rule_info",
            "name": "日计划详情",
            "views": [[tree_id, "tree"], [form_id, "form"]],
            "context": {
              "default_dev": self.train_dev.id,
            },
            "domain": [("year", "=", self.year),
                       ("dev", "=", self.train_dev.id),
                       ('data_source', '=', 'year')]
        }

    @api.model
    def search_read(self,
                    domain=None,
                    fields=None,
                    offset=0,
                    limit=None,
                    order=None):
        '''
        重写，搜索出要的结果
        :param domain:
        :param fields:
        :param offset:
        :param limit:
        :param order:
        :return:
        '''
        years = []
        for item in domain:
            if 'year' == item[0]:
                years.append(item[2])

        rule_infos = self.env["metro_park_maintenance.rule_info"]\
            .search_read([('year', 'in', years),
                          ('rule_type', '=', 'normal'),
                          ('data_source', '=', 'year')])
        month_cache = {}
        for rule in rule_infos:
            month_cache.setdefault(
                "{dev}_{year}_{month}".format(dev=rule["dev_no"], year=rule["year"],
                                              month=rule["month"]), []).append(rule["id"])
        rst = []
        records = self.search([('year', 'in', years)], offset=offset, limit=limit, order=order)
        for record in records:
            item = {
                "id": record.id,
                "train_dev": (record.train_dev.id, record.train_dev.dev_name),
                "remark": record.remark
            }
            for month in range(1, 13):
                key = "{dev}_{year}_{month}".format(dev=record.train_dev.dev_no,
                                                    year=record.year,
                                                    month=month)
                item["month{month}_rules".format(month=month)] = month_cache.get(key, [])
            rst.append(item)

        return rst
