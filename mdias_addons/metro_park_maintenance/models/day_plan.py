# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import pendulum
import logging

try:
    import websocket
    from websocket import create_connection
except ImportError:
    websocket = None

TASK_TYPE_RUN = 'run'
TASK_TYPE_PLAN = 'plan'
TASK_TYPE_MILE = 'mile'

_logger = logging.getLogger(__name__)


class DayPlan(models.Model):
    '''
    日计划, 计处日计划
    '''
    _name = 'metro_park_maintenance.day_plan'
    _track_log = True
    _rec_name = 'plan_name'
    _order = "year desc, month desc, day desc"

    week_plan_id = fields.Many2one(string="周",
                                   comodel_name="metro_park_maintenance.week_plan")

    plan_name = fields.Char(string="名称", required=True)
    plan_date = fields.Date(string='日期')

    year = fields.Integer(string="年",
                          compute="_compute_date_info",
                          store=True)
    month = fields.Integer(string="月",
                           compute="_compute_date_info",
                           store=True)
    day = fields.Integer(string="日",
                         compute="_compute_date_info",
                         store=True,
                         help="此字段仅用于搜索, 对应某一个月")

    operation_buttons = fields.Char(string="操作按扭")
    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布')],
                             default='draft')
    active = fields.Boolean(default=True)

    pms_work_class_info = fields.Many2one(
        comodel_name='pms.department', string='工班')

    # 设置运营车
    run_trains = fields.Many2many(string="运营车",
                                  comodel_name="metro_park_maintenance.train_dev",
                                  relation="day_plan_and_run_train_rel",
                                  column1="day_plan_id",
                                  column2="train_dev_id")

    train_infos = fields.Many2many(
        string="车辆信息",
        comodel_name="metro_park_maintenance.pre_date_train_infos",
        relation="day_plan_pre_date_train_info_rel",
        column1="day_plan_id",
        column2="pre_location",
        help="上一日的车辆信息")

    run_train_count = fields.Integer(string="运营车数量", compute='_compute_run_train_count')
    run_task_count = fields.Integer(string="运营任务数量", compute='_compute_run_task_count')
    # 热备是一个任务
    hot_back_trains = fields.Many2many(string="热备车",
                                       comodel_name="metro_park_maintenance.train_dev",
                                       relation="hot_back_train_rel",
                                       column1="day_plan_id",
                                       column2="train_id")
    # 设置当日时刻表
    time_table_id = fields.Many2one(string="时刻表",
                                    comodel_name="metro_park_base.time_table")

    remark = fields.Text(string='备注')
    plan_info_description = fields.Text(string="计划信息",
                                        help='用于排查计划',
                                        compute='_compute_plan_description')

    limit_infos = fields.Many2many(string="地点最大高峰车数量",
                                   comodel_name="metro_park_maintenance.day_plan_limit",
                                   relation="day_plan_limit_info_rel",
                                   column1='plan_id',
                                   column2='limit_id',
                                   help="因为高峰车其实也要考虑里程")

    use_pms_maintaince = fields.Selection(selection=[('yes', '是'), ('no', '否')],
                                          default="no",
                                          compute="_compute_use_pms_work_class", store=True)

    def _compute_use_pms_work_class(self):
        '''
        计算是否使用pms工班
        :return:
        '''
        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)
        for record in self:
            record.use_pms_maintaince = use_pms_maintaince

    @api.depends('run_trains')
    def _compute_run_train_count(self):
        '''
        计算运营车数量
        :return:
        '''
        for record in self:
            record.run_train_count = len(record.run_trains)

    @api.one
    @api.constrains('plan_name')
    def _check_plan_name(self):
        '''
        检查名称
        :return:
        '''
        if self.plan_name:
            record = self.search([('plan_name', '=', self.plan_name), ('id', '!=', self.id)])
            if record:
                return exceptions.ValidationError('计划名称重复! 请使用其它名称!')

    @api.multi
    def view_day_plan_action(self):
        '''
        查看日计划数据, 业主要求可以修改，先展示出来吧
        :return:
        '''
        tree_id = self.env.ref('metro_park_maintenance.day_plan_info_list').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_maintenance.rule_info",
            "name": "日计划({date})".format(date=self.plan_date),
            "views": [[tree_id, "tree"], [False, "form"]],
            "domain": [('plan_id', '=', 'metro_park_maintenance.day_plan, {plan_id}'
                        .format(plan_id=self.id))],
            "context": {
                "plan_id": self.id,
                "plan_date": str(self.plan_date)
            }
        }

    @api.multi
    def export_day_plan_action(self):
        '''
        日计划下载
        :return:
        '''
        return {
            'name': '日计划下载',
            'type': 'ir.actions.act_url',
            'url': '/export_day_plan/%s' % self.id
        }

    @api.multi
    def publish_plan_to_park_dispatch_pms_info(self):
        train_info = self.env['metro_park_maintenance.train_dev'].sudo().search([('object_code', '!=', '')])
        plan_recs = self.env['metro_park_maintenance.rule_info'].search(
            [
                ('data_source', '=', 'day'),
                ('dev', 'in', train_info.ids),
                ('date', '=', self.plan_name),
            ])
        for info in plan_recs:
            if not info.pms_work_class:
                return
        self.publish_plan_to_park_dispatch()

    @api.multi
    def publish_plan_to_park_dispatch(self):
        '''
        发布计划给场调，工作内容如下
        1、检修计划发过去。
        2、收发车计划发过去。
        3、在场调处再安排轨道。
        :return:
        '''
        infos = self.env["metro_park_maintenance.rule_info"] \
            .search([("plan_id", "=", "metro_park_maintenance.day_plan, {id}".format(id=self.id))])

        # 检查是否已经发布
        records = self.env['metro_park_dispatch.work_shop_day_plan'].search(
            [('plan_date', '=', self.plan_date)])
        if records:
            raise exceptions.Warning("当前日期已经有车间日生产计划!")

        next_date = pendulum.parse(str(self.plan_date)) \
            .add(days=1).format("YYYY-MM-DD")

        # 创建车间日生产计划
        data = {
            "plan_date": str(self.plan_date),
            "state": "un_publish",
            "day_plan_id": self.id
        }
        datas = []
        for info in infos:
            # 取得第二天的修程, 只显示均衡修和登顶等作业
            next_day_infos = self.env["metro_park_maintenance.rule_info"] \
                .search([("date", "=", next_date),
                         ("dev", "=", info.dev.id),
                         ("rule", "!=", False),
                         ("data_source", "=", "week"),
                         ('state', '=', 'published')])
            ids = infos.mapped("parent_id")
            next_day_ids = []
            for tmp_info in next_day_infos:
                if tmp_info.id not in ids:
                    next_day_ids.append(tmp_info.id)

            datas.append((0, 0, {
                "rule_info_id": info.id,
                "rule": info.rule.id,
                "dev": info.dev.id,
                "work_start_tm": info.work_start_time,
                "work_end_tm": info.work_end_time,
                "work_requirement": info.work_requirement,
                "location": info.final_location,
                "work_class": [(6, 0, info.work_class.ids)],
                "pms_work_class": info.pms_work_class,
                "next_day_works": [(6, 0, next_day_ids)],
                "time_table_data_id": info.time_table_data.id
            }))
        use_pms_maintaince = ''

        try:
            use_pms_maintaince = self.env['metro_park_base.system_config'].search_read(
                [])[0].get('start_pms')
        except Exception as e:
            _logger.info('pms基础信息未配置' + str(e))

        if use_pms_maintaince == 'yes':
            try:
                info = self.env['mdias_pms_interface'].sudo().year_month_week_day_plan(self, 'D', '1')
                if info == 'err':
                    return 'err'
            except Exception as e:
                _logger.info('pms基础信息未配置' + str(e))
        else:
            data["plan_datas"] = datas
            self.env["metro_park_dispatch.work_shop_day_plan"] \
                .create(data)

            # 关联检修工单, 这里还要删除相关的工单才行
            self.publish_maintaince_order()

        # 更改状态
        self.state = "published"

    @api.multi
    def publish_maintaince_order(self):
        '''
        发布到检修工单
        :return:
        '''
        rule_infos = self.env["metro_park_maintenance.rule_info"].search(
            [('year', '=', self.year),
             ('month', '=', self.month),
             ('day', '=', self.day),
             ('data_source', '=', 'day'),
             ("plan_id", '=', "metro_park_maintenance.day_plan, {plan_id}".format(plan_id=self.id)),
             ('rule_type', 'in', ['normal', 'temp'])])
        vals = []
        for rule_info in rule_infos:
            vals.append({
                "day_plan_info": rule_info.id
            })
        self.env["metro_park_maintenance.maintaince_order"] \
            .create(vals)

    @api.depends("plan_date")
    def _compute_date_info(self):
        '''
        计算日期相关信息
        :return:
        '''
        for record in self:
            tmp_date = pendulum.parse(str(record.plan_date))
            record.year = tmp_date.year
            record.month = tmp_date.month
            record.day = tmp_date.day

    @api.multi
    def unlink(self):
        '''
        删除日计划则删除相关的计划信息
        :return:
        '''
        for record in self:
            # 先删除具体信息
            records = self.env["metro_park_maintenance.rule_info"] \
                .search([('date', '=', record.plan_date),
                         ('data_source', '=', 'day')])
            records.unlink()

        super(DayPlan, self).unlink()

    @api.multi
    def plan_train(self):
        '''
        各条线路重写这个函数, 10号线的放在metro park base data line10下面去了
        :return:
        '''
        pass

    @api.multi
    def deal_train_plan_data(self, data, rst):
        '''
        处理计划数据, 将计算结果转换成为车辆写入数据库
        :return:
        '''
        if rst["status"] != 200:
            raise exceptions.Warning("计算出错!")

        dev_place_info = {}
        for info in self.train_infos:
            dev_place_info[info.train.id] = info.location.id

        rst = rst['datas']
        run_tasks = data['run_tasks']
        dev_infos = data['devs']
        for run_task in run_tasks:
            info_id = run_task['id']
            index = run_task["index"]
            info = self.env["metro_park_maintenance.rule_info"].browse(info_id)
            val = rst[index]
            # 如果超出了，则安排高峰车
            if val > len(dev_infos):
                continue
            # val - 1 为对应的index
            dev_info = dev_infos[val - 1]
            dev_id = dev_info['id']
            info.dev = dev_id

            # if info.time_table_data.out_location.id != dev_place_info[dev_id]:
            #     raise exceptions.ValidationError('地点不一致！')

    @api.multi
    def get_manage_run_train_action(self):
        '''
        取得现车管理
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.day_plan",
            'view_mode': 'form',
            "res_id": self.id,
            "target": "new",
            'context': {},
            "views": [[self.env.ref(
                'metro_park_maintenance.day_plan_manage_run_train').id, "form"]]
        }

    @api.multi
    def get_pre_date_train_infos_action(self):
        '''
        取得上日车辆位置
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.day_plan",
            'view_mode': 'form',
            "res_id": self.id,
            "target": "new",
            'context': {},
            "views": [[self.env.ref(
                'metro_park_maintenance.pre_date_train_infos_manage').id, "form"]]
        }

    @api.model
    def auto_plan_temp_rule(self):
        '''
        自动安排检技通
        车相同，日期范围内，没有安排的
        :return:
        '''
        pass

    @api.depends()
    def _compute_run_task_count(self):
        '''
        运营任务数量
        :return:
        '''
        for record in self:
            date = str(record.plan_date)
            infos = self.env['metro_park_maintenance.rule_info'].search(
                [('date', '=', date), ('data_source', '=', 'day'), ('rule_type', '=', 'run')])
            record.run_task_count = len(infos)

    @api.depends('run_task_count', 'run_trains')
    def _compute_plan_description(self):
        '''
        计算计划信息
        :return:
        '''
        raise exceptions.Warning('线别没有实现此函数!')

    @api.multi
    def get_plan_info(self):
        '''
        取得计划信息
        :return:
        '''
        info = pendulum.parse(str(self.plan_date)).format('YYYY年-MM月-DD日')
        return {
            "info": info
        }

    @api.multi
    def get_train_info_ids(self):
        '''
        :return:
        '''
        return self.train_infos.ids

    @api.model
    def add_miles_plan(self, plan_id, train_info_ids):
        '''
        添加里程检
        :param train_info_ids:
        :return:
        '''
        mile_rule_id = self.env.ref("metro_park_base_data_10.repair_rule_l")
        plan = self.env["metro_park_maintenance.day_plan"].browse(plan_id)
        train_infos = self.env["metro_park_maintenance.pre_date_train_infos"].browse(train_info_ids)
        trains = train_infos.mapped('train')
        vals = []
        for train in trains:
            vals.append({
                'dev': train.id,
                'rule': mile_rule_id.id,
                'data_source': 'day',
                'date': str(plan.plan_date),
                'parent_id': plan_id,
                'repair_num': 1,
                'plan_id': 'metro_park_maintenance.day_plan, {plan_id}'.format(
                    plan_id=plan_id)
            })
        self.env["metro_park_maintenance.rule_info"].create(vals)



