
# -*- coding: utf-8 -*-

from odoo import models, fields, api

CUR_TRAIN_STATUS = [('fault', '故障'),
                    ('repair', '检修'),
                    ('detain', '扣车'),
                    ('wait', '待命')]


class WorkShopDayPlan(models.Model):
    '''
    车间日生产计划
    '''
    _name = 'metro_park_dispatch.work_shop_day_plan_data'

    plan_id = fields.Many2one(string="计划id",
                              comodel_name="metro_park_dispatch.work_shop_day_plan")
    # store便于搜索
    plan_date = fields.Date(string="计划日期",
                            related="plan_id.plan_date",
                            store=True)

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布'),
                                        ('finished', '已完成')],
                             default='draft')

    rule = fields.Many2one(
        string='规则', comodel_name='metro_park_maintenance.repair_rule')

    tmp_rule = fields.Many2one(
        string="检技通", comodel_name="metro_park_maintenance.repair_tmp_rule")

    # 现车实际上和车辆是绑定的
    dev = fields.Many2one(string='车辆',
                          comodel_name='metro_park_maintenance.train_dev')

    rule_info_id = fields.Many2one(string='计划信息',
                                   comodel_name='metro_park_maintenance.rule_info')

    # 安排的具体工作时间
    work_start_tm = fields.Integer(string='开始时间', help="时间可以选择次日")
    work_end_tm = fields.Integer(string='作业结束时间', help="时间可以选择次日")

    # 由检修修程具体去去弄
    work_content = fields.Char(string='作业内容',
                               related="rule_info_id.work_content")
    # 作业区域
    work_area = fields.Many2one(string="作业库",
                                comodel_name="metro_park_base.park_area")
    # 这里是选择轨道属性
    work_requirement = fields.Many2many(string='作业要求',
                                        comodel_name='metro_park_base.rail_property',
                                        relation="work_shop_plan_rail_property_rail",
                                        column1="work_shop_day_plan_id",
                                        column2="property_id")

    location = fields.Many2one(string='位置',
                               comodel_name='metro_park_base.location')

    work_class = fields.Many2many(string='作业工班',
                                  comodel_name='funenc.wechat.department',
                                  relation="work_shop_day_plan_work_class_rel",
                                  column1='work_shop_data_id',
                                  column2='class_id')

    train_status = fields.Selection(string='车辆状态',
                                    selection=[('normal', '正常')])

    back_location = fields.Many2one(string='夜间回段',
                                    comodel_name='metro_park_base.location',
                                    help="只有运行营任才有效")

    # 次日检修作业, 考虑均衡修，这里怕是得一级一级的找吧
    next_day_works = fields.Many2many(string='次日作业',
                                      comodel_name="metro_park_maintenance.rule_info",
                                      relation="work_shop_day_plan_rule_info_rel",
                                      column1="work_shop_day_plan_id",
                                      column2="rule_info_id")

    time_table_data_id = fields.Many2one(string="运行图数据",
                                         comodel_name="metro_park_base.time_table_data",
                                         help="仅针对于收发车任务和运营任务有效, 主要目的是为了关联相关信息")

    rail = fields.Many2one(string="作业地点",
                           comodel_name="metro_park_base.rails_sec",
                           help="具体到某条轨道, 日计划时才会安排")

    # 具体的轨道等可以在这里写上
    work_remark = fields.Text(string='作业备注')

    # 其它备注项
    remark = fields.Text(string='备注')

    @api.multi
    def get_next_run_task(self):
        '''
        当前是一个收车任务，但后面还有运行， 高峰车的情况, 这个也是判断高峰车的标准 train_no
        :return:
        '''
        # 线别数据中实现
        assert False, '没有实现get_next_run_task'

    @api.multi
    def get_prev_run_task(self):
        '''
        取得同一车的运营任务
        :return:
        '''
        assert False, '没有实现get_prev_run_task'

    @api.multi
    def is_high_run_task(self):
        '''
        如果后面还有正线运营任务的话那么就是高峰车，如果没有话则不是
        :return:
        '''
        return True if self.get_after_run_task() is not None else False

    @api.model
    def get_detain_train_devs(self, date):
        '''
        取得特定日期的检修设备
        :param date:
        :return:
        '''
        records = self.search([('plan_date', '=', date), ('rule.balance', '=', 'yes')])
        return records.mapped("dev.id")

    @api.multi
    def get_tasks_after_run(self):
        '''
        取处运营任务之后的检修任务，
        一般是找到这些任务后查看作业要求,
        如果是有多个的话可能还要调到多处去才行
        :return:
        '''
        # 线别数据中实现
        assert False, '没有实现get_tasks_after_run'

