# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging
from . import util


_logger = logging.getLogger(__name__)


class WeekPlanWizard(models.TransientModel):
    '''
    周计划向导
    '''
    _name = 'metro_park_maintenance.week_plan_wizard'

    @api.model
    def get_year_domain(self):
        '''
        取得年的选择范围
        :return:
        '''
        records = self.env['metro_park_maintenance.year_plan'] \
            .search([('state', '=', 'published')])
        years = records.mapped('year')
        return [('val', 'in', years)]

    plan_name = fields.Char(string="名称", required=True)
    year_plan = fields.Many2one(
        comodel_name="metro_park_maintenance.year_plan",
        domain="[('state', '=', 'published')]",
        string="年计划",
        help="限定月计划的范围")

    month_plan = fields.Many2one(
        comodel_name="metro_park_maintenance.month_plan",
        domain="[('state', '=', 'published')]",
        string="月计划",
        help="从月计划去选择周")

    week = fields.Many2one(string='周',
                           comodel_name='metro_park_maintenance.week',
                           required=True)

    start_date = fields.Date(string="开始日期", compute="_compute_date")
    end_date = fields.Date(string="结束日期", compute="_compute_date")

    pms_work_class_info = fields.Many2one(comodel_name='pms.department', string='工班')
    remark = fields.Text(string='备注')

    use_pms_maintaince = fields.Selection([('yes', '是'), ('no', '否')],
                                          string="是否使用pms", default='no',
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

    @api.onchange('month_plan', 'week')
    def on_change_week(self):
        '''
        更改月计划和周
        :return:
        '''
        if self.year_plan and self.month_plan and self.week:
            start_date, end_date = util.get_week_date_range(self.year_plan.year, self.week.val)

            self.start_date = start_date
            self.end_date = end_date

            self.plan_name = '第{week}周'.format(week=self.week.val)

    @api.one
    @api.depends('month_plan', 'week')
    def _compute_date(self):
        '''
        计算时间
        :return:
        '''
        if self.year_plan and self.month_plan and self.week:
            start_date, end_date = util.get_week_date_range(self.year_plan.year, self.week.val)
            self.start_date = start_date
            self.end_date = end_date

    @api.multi
    def on_ok(self):
        '''
        确认按扭点击
        :return:
        '''
        year = self.month_plan.year
        week = self.week.val

        ids = ['metro_park_maintenance.month_plan, {plan_id}'.format(
            plan_id=self.month_plan.id)]
        month = self.month_plan.month
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

        # 查询上一个周的工班
        work_classes = []
        pre_date = pendulum.parse(str(self.start_date)).subtract(days=1)
        his_infos = self.env["metro_park_maintenance.week_work_class_info"].search(
            [('date', 'in', [pre_date.format('YYYY-MM-DD'), pre_date.subtract(days=1).format(
                'YYYY-MM-DD')])], limit=2, order='date asc')
        if his_infos:
            work_classes = his_infos.mapped('work_class_name')

        def get_work_class():
            if len(work_classes) == 0:
                return '里程修1班/里程修3班'
            elif len(work_classes) == 1:
                return work_classes[0]
            else:
                if work_classes[-1] == work_classes[-2]:
                    if work_classes[-1] == '里程修1班/里程修3班':
                        return '里程修2班/里程修4班'
                    else:
                        return '里程修1班/里程修3班'
                else:
                    return work_classes[-1]

        # 连续干两天
        work_class_info = []
        for week_day in range(1, 8):
            work_class = get_work_class()
            work_classes.append(work_class)
            remark = '1、{work_class}.综合检修班当班.\n\r' \
                     '2、请根据周计划次日及第三、四日计划提前安排登顶、月检及数据测量列车回库需求或调车转轨；'.format(work_class=work_class)
            work_class_info.append((0, 0, {
                "date": pre_date.add(days=week_day).format('YYYY-MM-DD'),
                "work_class_name": work_class,
                "remark": remark
            }))

        # 创建周计划
        record = self.env['metro_park_maintenance.week_plan'].create({
            'year': year,
            'week': week,
            'plan_name': self.plan_name,
            "pms_work_class_info": self.pms_work_class_info.id,
            "month_plan_id": self.month_plan.id,
            "mile_work_class_info": work_class_info
        })

        # 检查开始月份是否发布和结束是否发布
        start_date_obj = pendulum.parse(str(self.start_date))
        end_date_obj = pendulum.parse(str(self.end_date))

        start_year = start_date_obj.year
        start_month = start_date_obj.month
        end_year = end_date_obj.year
        end_month = end_date_obj.month

        start_plan = self.env["metro_park_maintenance.month_plan"].search(
            [('year', '=', start_year), ('month', '=', start_month)])
        if start_plan.state != 'published':
            raise exceptions.Warning('开始月份没有发布!')

        end_plan = self.env["metro_park_maintenance.month_plan"].search(
            [('year', '=', end_year), ('month', '=', end_month)])
        if end_plan.state != 'published':
            raise exceptions.Warning('结束月份没有发布!')

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
                'work_class_names': [],
                'repair_num': info.repair_num,
                'work_class': [[6, 0, info.work_class.ids]],
                'pms_work_class': info.pms_work_class,
                'plan_id':
                    'metro_park_maintenance.week_plan, {plan_id}'
                        .format(plan_id=record.id)})

        # 创建新的计划
        infos = self.env["metro_park_maintenance.rule_info"] \
            .create(vals)
        return infos

    @api.model
    def get_week_plan_action(self):
        '''
        跳转到添加页面,指定plan_type用于区分计划类型
        :return:
        '''
        # 取得year的domain
        domain = self.get_year_domain()

        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.week_plan_wizard",
            'view_mode': 'form',
            "domain": domain,
            "target": "new",
            "views": [[self.env.ref(
                'metro_park_maintenance.week_plan_wizard_form').id, "form"]]
        }

    @api.model
    def get_parent_plan_data(self):
        '''
        获取上一级计划的检修计划数据
        :return:
        '''
        option = []
        datas = self.env['metro_park_maintenance.rule_info'] \
            .search_read([('data_source', '=', 'month')],
                         fields=['id', 'date', 'rule_name'])
        for data in datas:
            option.append({
                'value': data.get('id'),
                'label': str(data.get('date')) + '/' + str(data.get('rule_name')),
            })
        return option

    @api.onchange("week")
    def on_change_year(self):
        '''
        改变年的时候进行相应调整
        :return:
        '''
        if self.month_plan and self.week:
            self.plan_name = \
                '{year}年,第{week}周'.format(year=self.year_plan.year, week=self.week.val)

    @api.onchange('month_plan')
    def on_change_month_plan(self):
        '''
        修改月计划时选择相应的月份的周
        :return:
        '''
        if self.month_plan:
            year = self.month_plan.year
            month = self.month_plan.month
            month_start = pendulum.date(year, month, 1)
            month_end = pendulum.date(year, month, month_start.days_in_month)

            # 初始月份跨年了的情况
            start_week = month_start.week_of_year
            if month == 1 and start_week > 10:
                start_week = 1

            end_week = month_end.week_of_year
            # 跨年的情况
            if end_week < start_week:
                next_year_start = pendulum.date(year + 1, 1, 1)
                tmp_day = next_year_start.day_of_week
                tmp_end = next_year_start.subtract(days=tmp_day)
                end_week = tmp_end.week_of_year

            weeks = []
            for week in range(start_week, end_week + 1):
                weeks.append(week)

            week_plans = self.env["metro_park_maintenance.week_plan"] \
                .search([('week', 'in', weeks),
                         ('month_plan_id', '=', self.month_plan.id)])
            new_weeks = []
            old_weeks = week_plans.mapped("week")
            for week in weeks:
                if week not in old_weeks:
                    new_weeks.append(week)

            return {
                "domain": {
                    "week": [('val', 'in', new_weeks)]
                }
            }
