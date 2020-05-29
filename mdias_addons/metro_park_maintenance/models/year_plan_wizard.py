# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class YearPlanWizard(models.TransientModel):
    '''
    添加年计划向导，用于选择月份
    '''
    _name = 'year_plan_wizard'
    _description = '年计划向导，用于选择年份'

    @api.model
    def _compute_domain(self):
        '''
        限制已经有的年份不要进行选择, 可能创建同一年份的重复项
        :return:
        '''
        records = self.env['metro_park_maintenance.year_plan'].search([])
        years = records.mapped('year')
        return [('val', 'not in', years)]

    year = fields.Many2one(string='年',
                           required=True,
                           comodel_name='metro_park_maintenance.year')

    plan_name = fields.Char(string="计划名称",
                            required=True,
                            help="由于可以创建多个年计划, 所以这里名称可以重复")

    def get_default_month(self):
        '''
        取得默认月份, 1月
        :return:
        '''
        month1 = self.env.ref("metro_park_maintenance.month_1")
        return month1.id

    start_month = fields.Many2one(string="开始月份",
                                  comodel_name="metro_park_maintenance.month",
                                  default=get_default_month)

    pms_work_class_info = fields.Many2one('pms.department',
                                          string='工班')

    use_pms_maintaince = fields.Selection([('yes', '是'), ('no', '否')],
                                          string="是否使用pms",
                                          default='no',
                                          compute="_compute_use_pms_work_class")

    @api.depends('year')
    def _compute_use_pms_work_class(self):
        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)
        for record in self:
            record.use_pms_maintaince = use_pms_maintaince

    @api.onchange("year")
    def on_change_year(self):
        '''
        改变年的时候进行相应调整
        :return:
        '''
        for record in self:
            if record.year:
                record.plan_name = record.year.val

    @api.model
    def _get_default_month(self):
        '''
        取得默认月份
        :return:
        '''
        record = self.env["metro_park_maintenance.month"].search(
            [('val', '=', 1)])
        return record.id

    @api.multi
    def on_ok(self):
        '''
        点击确定按扭
        :return:
        '''
        self.env["metro_park_maintenance.year_plan"].create({
            "year": self.year.val,
            "plan_name": self.plan_name,
            "start_month": self.start_month.val,
            "pms_work_class_info": self.pms_work_class_info.id,
        })

    @api.model
    def get_year_domain(self, record):
        '''
        取得年份的domain
        :param record:
        :return:
        '''
        records = self.env['metro_park_maintenance.year_plan'].search([])
        years = records.mapped('year')
        return [('val', 'not in', years)]
