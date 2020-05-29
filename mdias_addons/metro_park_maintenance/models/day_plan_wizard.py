# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging

_logger = logging.getLogger(__name__)


class DayPlanWizard(models.TransientModel):
    '''
    日计划向导, 主里只能过通跳action的方式来进行
    '''
    _name = 'metro_park_maintenance.day_plan_wizard'

    name = fields.Char(string='名称')
    
    year_plan_id = fields.Many2one(string="年", 
                                   comodel_name="metro_park_maintenance.year_plan",
                                   domain="[('state', '=', 'published')]",
                                   required=True)
    month_plan_id = fields.Many2one(string="月",
                                    comodel_name="metro_park_maintenance.month_plan",
                                    domain="[('state', '=', 'published')]",
                                    required=True)
    week_plan_id = fields.Many2one(string="周",
                                   comodel_name="metro_park_maintenance.week_plan",
                                   domain="[('state', '=', 'published')]",
                                   required=True)

    day = fields.Many2one(string="日",
                          comodel_name="metro_park_maintenance.year_dates",
                          required=True)

    pms_work_class_info = fields.Many2one(comodel_name='pms.department', 
                                          string='工班')

    use_pms_maintaince = fields.Selection(selection=[('yes', '是'), ('no', '否')],
                                          string="是否使用pms",
                                          default='no',
                                          compute="_compute_use_pms_work_class")

    # 时刻表
    time_table_id = fields.Many2one(string="运行图",
                                    comodel_name="metro_park_base.time_table",
                                    required=True)

    # 设置运营车, 根据运营任务先把车生成出来
    run_trains = fields.Many2many(string="运营车",
                                  comodel_name="metro_park_maintenance.train_dev",
                                  relation="day_plan_and_run_train_wizard_rel",
                                  column1="day_plan_id",
                                  column2="train_dev_id")

    train_infos = fields.Many2many(
        string="上一日车辆位置",
        comodel_name="metro_park_maintenance.pre_date_wizard_train_infos",
        relation="train_dev_pre_wizard_train_info_rel",
        column1="pan_id",
        column2="location")

    def _get_default_limit_info(self):
        '''
        取得默认限制
        :return:
        '''
        rst = []
        location = self.env.user.cur_location
        line = location.line
        location_ids = line.get_locations()
        locations = self.env['metro_park_base.location'].browse(location_ids)
        for location in locations:
            rst.append((0, 0, {
                "location": location.id,
                "max_repair_after_high_run": location.max_repair_after_high_run,
                "max_repair_back_time": location.max_repair_back_time
            }))
        return rst

    limit_infos = fields.Many2many(string="地点最大高峰车数量",
                                   comodel_name="metro_park_maintenance.day_plan_wizard_limit",
                                   relation="day_plan_wizard_limit_info_rel",
                                   column1='plan_id',
                                   column2='limit_id',
                                   default=_get_default_limit_info,
                                   help="这里的初始值同样是通默认值带入")

    remark = fields.Text(string='备注')

    @api.depends('year_plan_id')
    def _compute_use_pms_work_class(self):
        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)
        for record in self:
            record.use_pms_maintaince = use_pms_maintaince
    
    @api.onchange("year_plan_id")
    def on_change_year_plan(self):
        '''
        改变时限制月
        :return: 
        '''
        if self.year_plan_id:
            self.month_plan_id = False
            self.week_plan_id = False
            return {
                "domain": {
                    "month_plan_id":
                        [('year_plan', '=', self.year_plan_id.id),
                         ('state', '=', 'published')]
                }
            }
        else:
            self.month_plan_id = False
            self.week_plan_id = False
            self.day = False
            
    @api.onchange("month_plan_id")
    def on_change_month_plan(self):
        '''
        改变时限制月
        :return: 
        '''
        if self.month_plan_id:
            return {
                "domain": {
                    "week_plan_id": 
                        [('month_plan_id', '=', self.month_plan_id.id),
                         ('state', '=', 'published')]
                }
            }
        else:
            self.week_plan_id = False
            self.day = False
            
    @api.onchange('week_plan_id')
    def on_change_week_plan(self):
        '''
        更改周计划
        :return:
        '''
        if self.week_plan_id:
            year = self.week_plan_id.month_plan_id.year
    
            year_start = pendulum.date(year, 1, 1)
            day_of_week = year_start.day_of_week
            year_start = year_start.subtract(days=day_of_week - 1)
            day_range_start = year_start.add(weeks=self.week_plan_id.week - 1)

            names = []
            for day in range(0, 7):
                names.append(
                    day_range_start.add(days=day).format('YYYY-MM-DD'))
                
            return {
                "domain": {
                    "day": [("name", "in", list(set(names)))]
                }
            }

    @api.onchange("day")
    def on_change_day(self):
        '''
        更改日期
        :return:
        '''
        if self.year_plan_id \
                and self.month_plan_id \
                and self.week_plan_id \
                and self.day:
            self.name = self.day.name

    @api.onchange('day')
    def on_change_day(self):
        '''
        更改日期的时候计算现车及上日车的最终位置
        :return:
        '''
        pass

    @api.multi
    def on_ok(self):
        '''
        点击确定按扭, 创建的时候就把当日的运行图数据放进去，这样便于修改
        :return:
        '''
        # 每天线路分别实现这个函数
        pass

    @api.model
    def get_day_plan_action(self):
        '''
        取得日计划动作
        :return:
        '''
        records = self.env['metro_park_maintenance.year_plan'] \
            .search([('state', '=', 'published')])
        years = records.mapped('year')
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.day_plan_wizard",
            'view_mode': 'form',
            "target": "new",
            "domain": {
                "year": [("val", "in", years)]
            },
            "views": [[self.env.ref('metro_park_maintenance.day_plan_wizard_form').id, "form"]]
        }

    @api.model
    def get_parent_plan_data(self):
        '''
        获取上一级计划的检修计划数据
        :return:
        '''
        option = []
        datas = self.env['metro_park_maintenance.rule_info']\
            .search_read([('data_source', '=', 'week')],
                         fields=['id', 'day', 'rule_name'])
        for data in datas:
            option.append({
                'value': data.get('id'),
                'label': str(data.get('day')) + '/' + str(data.get('rule_name')),
            })
        return option

    @api.onchange('time_table_id')
    def on_change_time_table_id(self):
        '''
        更改时刻表
        :return:
        '''
        pass


