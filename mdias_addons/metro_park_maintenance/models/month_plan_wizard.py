# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum
import logging
_logger = logging.getLogger(__name__)


class MonthPlanWizard(models.TransientModel):
    '''
    月计划向导,只能创建下一月的
    '''
    _name = 'metro_park_maintenance.month_plan_wizard'

    plan_name = fields.Char(string="计划名称", required=True)

    # 直接选年计划，从年计划中获取月份
    year_plan = fields.Many2one(string='年',
                                comodel_name='metro_park_maintenance.year_plan',
                                domain="[('state', '=', 'published')]",
                                required=True)

    month = fields.Many2one(string='月',
                            comodel_name='metro_park_maintenance.month',
                            required=True)

    pms_work_class_info = fields.Many2one(comodel_name='pms.department',
                                          string='工班')

    remark = fields.Text(string="备注")
    use_pms_maintaince = fields.Selection([('yes', '是'), ('no', '否')],
                                          string="是否使用pms",
                                          default='no',
                                          compute="_compute_use_pms_work_class")

    @api.depends('year_plan')
    def _compute_use_pms_work_class(self):
        try:
            config = self.env['metro_park_base.system_config'].get_configs()
            use_pms_maintaince = config.get('start_pms', False)
            for record in self:
                record.use_pms_maintaince = use_pms_maintaince
        except Exception as e:
            _logger.info('PMS基础信息未配置' + str(e))

    @api.onchange("month")
    def on_change_year(self):
        '''
        改变年的时候进行相应调整
        :return:
        '''
        if self.month:
            self.plan_name = '{year}年{month}月'\
                .format(year=self.year_plan.year, month=self.month.val)

    @api.model
    def get_month_plan_action(self):
        '''
        取得月计划向导action
        :return:
        '''
        return {
            "type": 'ir.actions.act_window',
            "view_type": 'form',
            "view_mode": 'form',
            "res_model": "metro_park_maintenance.month_plan_wizard",
            "target": 'new',
            "views": [[False, 'form']],
            "domain": {}
        }

    @api.onchange("year_plan")
    def on_change_year_plan(self):
        '''
        改变年的时候限制月
        :return:
        '''
        if self.year_plan:
            records = self.env["metro_park_maintenance.month_plan"] \
                .search([("year_plan.id", '=', self.year_plan.id)])
            months = records.mapped("month")
            return {
                "domain": {
                    "month": [("val", "not in", months)]
                }
            }

    @api.multi
    def on_ok(self):
        '''
        确定按扭点击, 根据选中的年月创建月计划, 月计划其实事先就创建好了， 只是改变下状态而罢了
        周计划也是一样
        放到
        :return:
        '''
        year = self.year_plan.year
        month = self.month.val

        # 如果当前的月计划还没有创建则进行创建
        month_plan_model = self.env['metro_park_maintenance.month_plan']
        sequence = self.env['ir.sequence'].next_by_code('month.plan.number')

        # 创建月计划
        record = month_plan_model.create([{
            'plan_name': self.plan_name,
            # 关联到年计划
            'year_plan': self.year_plan.id,
            'year': year,
            'month': month,
            'plan_no': sequence,
            "pms_work_class_info": self.pms_work_class_info.id,
        }])

        # 复制年计划数据
        rule_infos = self.env["metro_park_maintenance.rule_info"]\
            .search([('plan_id', '=', 'metro_park_maintenance.year_plan, {plan_id}'
                      .format(plan_id=self.year_plan.id)), ('month', '=', self.month.val)])
        vals = []
        for info in rule_infos:
            vals.append({
                'dev': info.dev.id,
                'rule': info.rule.id,
                'data_source': 'month',
                'date': str(info.date),
                # 父项记录的id
                'parent_id': info.id,
                'repair_day': info.repair_day,
                'repair_num': info.repair_num,
                'plan_id': 'metro_park_maintenance.month_plan, {plan_id}'.format(
                    plan_id=record.id)
            })
        return self.env["metro_park_maintenance.rule_info"] \
            .create(vals)
