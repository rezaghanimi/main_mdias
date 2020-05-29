
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MonthPlanComputeWizard(models.TransientModel):
    '''
    月计划计算向导
    '''
    _name = 'metro_park_maintenance.month_plan_compute_wizard'
    
    max_plan_per_day = fields.Integer(string='每日最大任务数量', default=5)
    calc_host = fields.Char(string='计算服务器')

    # 规程数量限制
    rule_count_constrain = \
        fields.One2many(comodel_name="metro_park_maintenance.rule_count_constrain",
                        inverse_name="month_compute_wizard",
                        string="数量限制")

    # 空调专检第一月
    def _get_kt_default_val(self):
        '''
        取得kt专检初始值
        :return:
        '''
        kt = self.env.ref("metro_park_base.selection_yes").id
        return kt

    plan_kt = fields.Many2one(comodel_name="metro_park_base.selections",
                              string="空调专检")

    plan_kt_month = fields.Many2one(comodel_name="metro_park_base.selections",
                                    string='空调专检月份',
                                    help="空调专检的月份")

    plan_kt_month_visible = fields.Boolean(string='空调专检月份是否显示',
                                           compute="_compute_month_visible")

    @api.onchange('calc_host')
    def on_change_plan_kt(self):
        '''
        plan kt 改变时处理方式
        :return:
        '''
        return {
            "domain": {
                "plan_kt": [('value', 'in', ['yes', 'no'])],
                "plan_kt_month": [('value', 'in', ['plan_kt_month_1', 'plan_kt_month_2'])]
            }
        }

    @api.depends("plan_kt")
    def _compute_month_visible(self):
        '''
        计算月份是否显示，在plan_kt选择yes的时候进行显示
        :return:
        '''
        selection_yes = self.env.ref("metro_park_base.selection_yes").id
        if self.plan_kt.id == selection_yes:
            self.plan_kt_month_visible = True
        else:
            self.plan_kt_month_visible = False

    @api.onchange("max_plan_per_day")
    def on_change_work_class_count(self):
        '''
        更改工班数量
        :return:
        '''
        records = self.env["metro_park_maintenance.repair_rule"]\
            .search([('target_plan_type', 'in', ['year', 'month']),
                     ('rule_status', '=', 'normal')])
        rst = [(5, 0, 0)]
        for record in records:
            rst.append((0, 0, {
                "rule": record.id,
                "count": record.max_plan_per_day
            }))
        self.rule_count_constrain = rst

    @api.model
    def get_default_info(self, month_plan_id):
        '''
        取得默认配置
        :return:
        '''
        month_plan = self.env["metro_park_maintenance.month_plan"].browse(month_plan_id)

        config = self.env["metro_park_base.system_config"].get_configs()
        calc_host = config["calc_host"] or "ws://127.0.0.1:9520"

        rst = {
            "work_class_count": 6,
            "calc_host": calc_host
        }

        plan_kt_yes = self.env.ref("metro_park_base.selection_yes").id
        plan_kt_no = self.env.ref("metro_park_base.selection_no").id
        if month_plan.month == 3 or month_plan.month == 4:
            rst['plan_kt'] = plan_kt_yes
        else:
            rst['plan_kt'] = plan_kt_no

        if month_plan.month == 3:
            rst['plan_kt_month'] = \
                self.env.ref('metro_park_base.plan_kt_month_1').id
        elif month_plan.month == 4:
            rst['plan_kt_month'] = \
                self.env.ref('metro_park_base.plan_kt_month_2').id
        else:
            rst['plan_kt_month'] = None

        return rst

    @api.model
    def get_work_class_count(self):
        '''
        取得工班数量
        :return:
        '''
        # 取得有均衡修工班属性的工班
        department_property_work_class = \
            self.env.ref("metro_park_base.department_property_balance_work_class").id
        work_classes = self.env["funenc.wechat.department"].search(
            [("properties", "in", [department_property_work_class])])
        work_class_count = len(work_classes)
        return work_class_count

    @api.multi
    def get_wizard_data(self):
        '''
        取得向导数据
        :return:
        '''
        return self.read()[0]


