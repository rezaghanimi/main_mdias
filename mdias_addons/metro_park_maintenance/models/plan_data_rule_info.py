# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import pendulum
import datetime
from odoo.models import DEFAULT_SERVER_DATETIME_FORMAT
import logging

_logger = logging.getLogger(__name__)


class RuleInfo(models.Model):
    '''
    日计划设备检修信息，包含计划内容和日常维护及运行内容
    '''

    _name = 'metro_park_maintenance.rule_info'
    _rec_name = 'rule_name'
    _track_log = True
    _order = "dev asc"

    plan_data = fields.Many2one(
        comodel_name="metro_park_maintenance.plan_data",
        string="日计划信息",
        ondelete='cascade')

    rule_type = fields.Selection(selection=[('normal', '规程'),
                                            ('temp', '检技通'),
                                            ('run', '运营'),
                                            ('receive_train', '接车'),
                                            ('send_train', '发车')],
                                 default='normal',
                                 string="类型")

    work_content = fields.Char(string='作业内容', compute="_get_work_content")

    # 用于标记数据来源, 便于清理
    data_source = fields.Selection(selection=[('year', '年计划'),
                                              ('month', '月计划'),
                                              ('week', '周计划'),
                                              ('day', '日计划')],
                                   default="year")

    # 冗余数据，便于查询规则的存历史数据, 用于年计划等的排列
    dev = fields.Many2one(string="设备",
                          comodel_name="metro_park_maintenance.train_dev")

    # 由于可能是计算之前日期，所以还只能在这里计算
    miles = fields.Float(string="里程数", compute="_compute_last_repair_info")
    last_mile_repair_date = fields.Date(string="上次里程检日期", compute="_compute_last_repair_info")
    last_repair_miles = fields.Float(string="上次里程检公里数", compute="_compute_last_repair_info")
    miles_after_last_repair = fields.Float(string="上次里程后公里数", compute="_compute_miles_after_last_repair")

    dev_no = fields.Char(string="设备编号", related="dev.dev_no")
    user_define_dev = fields.Many2one(string="指定设备",
                                      comodel_name="metro_park_maintenance.train_dev",
                                      help="有些时候需要用户指定设备")

    user_define_dev_visible = fields.Boolean(string="用户自定义设备字段是否显示",
                                             compute="_compute_user_define_dev_visible")

    date = fields.Date(string="日期", help="冗余数据, 便于查询")
    repair_num = fields.Integer(string="修次",
                                default=0,
                                help="修次指的时当前位于维修计划的第几次，以便确定具体的规程，仅均衡修有用")
    # 方便查询
    year = fields.Integer(
        string="年份", compute="_compute_month", store=True, help="显示年份")
    month = fields.Integer(
        string="月份", compute="_compute_month", store=True, help="年中的月")
    day = fields.Integer(
        string="日", compute="_compute_month", store=True, help="月份中的天")

    rule = fields.Many2one(
        string='规则',
        comodel_name='metro_park_maintenance.repair_rule')

    is_mile_rule = fields.Boolean(string="是否里程检",
                                  help="区分是否是公里数",
                                  default=False,
                                  compute="_compute_is_mile")

    work_area = fields.Many2one(string="区域要求",
                                comodel_name="metro_park_base.park_area")

    work_requirement = fields.Many2many(string='段内作业需求',
                                        related="rule.work_requirement",
                                        help="登高、地沟等要求")

    # 作业地点, 有些作业多个地点都可以进行
    locations = fields.Many2many(string='作业地点',
                                 comodel_name='metro_park_base.location',
                                 relation="plan_data_rule_info_locations_rel",
                                 column1="rule_id",
                                 column2="location_id")
    # 最终作业地点
    final_location = fields.Many2one(string="作业地点",
                                     comodel_name="metro_park_base.location")

    user_define_location = fields.Many2one(string="指定地点",
                                           comodel_name="metro_park_base.location",
                                           help="用于用户指定地点")
    user_define_location_visible = fields.Boolean(string="用户指定地点是否可见",
                                                  default=False,
                                                  compute="_compute_user_define_location")

    compute_location = fields.Char(string='作业地点',
                                   help="用于日生产计划导出",
                                   compute="_compute_final_location")

    repair_days = fields.Integer(string='检修天数',
                                 related='rule.repair_days',
                                 store=True)
    # 导入的时候需要计算这个
    repair_day = fields.Integer(string="检修第几天")

    tmp_rule = fields.Many2one(
        string="检技通",
        comodel_name="metro_park_maintenance.repair_tmp_rule", help='检技通')

    rule_name = fields.Char(string="修程(检技通)", compute="_compute_rule_info")
    rule_no = fields.Char(string="代号(检技通)", compute="_compute_rule_info")

    rule_id = fields.Integer(
        string="规程id",
        compute="_compute_rule_info",
        help="用于计算")

    # 具体日计划的时候才会确定时间，
    # 这个是根据用时来确定的，用时是每天中的用时，而不是整个修程的用时
    work_start_time = fields.Integer(string="开始时间", help="这里是个跨天的时间")
    work_end_time = fields.Integer(string="结束时间", help="这里是个跨天的时间")

    rail = fields.Many2one(string="作业地点",
                           comodel_name="metro_park_base.rails_sec",
                           help="具体到某条轨道, 日计划时才会安排")

    rail_type = fields.Many2one(string="轨道类型",
                                compute="_compute_rail_type",
                                store=True,
                                help="导入的时候可能没有明确到轨道, 这里就只写个类型")

    prev_date_location = fields.Many2one(string="上一日位置",
                                         comodel_name="metro_park_base.location",
                                         compute="_compute_last_repair_info")

    # 作业时间
    work_time = fields.Char(string="工作时间", compute="compute_work_time")

    # 次日作业
    next_day_work = fields.Many2many(string="次日作业",
                                     comodel_name="metro_park_maintenance.rule_info",
                                     relation="rule_info_next_day_work_rel",
                                     column1="rule_info_id1",
                                     column2="rule_info_id2",
                                     compute="_compute_next_day_work")

    next_day_work_location = fields.Many2one(comodel_name="metro_park_base.location",
                                             compute="_compute_next_day_work", string="昨日作业地点")

    @api.onchange("user_define_location")
    def on_change_user_location(self):
        '''
        用户指定地址
        :return:
        '''
        if self.user_define_location:
            self.final_location = self.user_define_location.id

    @api.depends('user_define_location', 'locations')
    def _compute_final_location(self):
        '''
        计算最终位置
        :return:
        '''
        pass

    @api.depends()
    def _compute_next_day_work(self):
        '''
        计算次日作业
        :return: 
        '''
        if len(self) == 0:
            return

        for index, record in enumerate(self):
            if record.date:
                date_obj = pendulum.parse(str(record.date))
                date_obj = date_obj.add(days=1)
                break

        # 从周计里边去获取
        rule_infos = self.env["metro_park_maintenance.rule_info"].search(
            [('data_source', '=', 'week'),
             ('date', '=', date_obj.format('YYYY-MM-DD'))])

        rule_info_cache = dict()
        for index, info in enumerate(rule_infos):
            if info.dev:
                rule_info_cache.setdefault(info.dev.id, []).append(info.id)

        for record in self:
            if record.dev.id in rule_info_cache:
                record.next_day_work = rule_info_cache[record.dev.id]

        # 计算次日作业地点
        for record in self:
            next_day_work = False
            for ndw in record.next_day_work:
                next_day_work = ndw
                break
            if next_day_work and next_day_work.work_class and next_day_work.work_class.locations:
                record.next_day_work_location = next_day_work.work_class.locations[0].id

    @api.model
    def _get_department_domain(self):
        '''
        只选择作业工班
        :return:
        '''
        department_property_work_class_id = \
            self.env.ref("metro_park_base.department_property_work_class").id
        return [('properties', 'in', [department_property_work_class_id])]

    # 作业工班, 作业工班是根据生产说明来进行
    work_class = fields.Many2many(string="检修工班",
                                  comodel_name="funenc.wechat.department",
                                  relation="plan_data_rule_info_work_class_rel",
                                  column1="rule_info_id",
                                  column2="work_class_id",
                                  domain=_get_department_domain)

    work_class_location = fields.Many2one(string="location",
                                          comodel_name="metro_park_base.location",
                                          compute="_compute_work_class_location")

    @api.depends("work_class", "rule")
    def _compute_work_class_location(self):
        '''
        计算均衡修地址
        :return:
        '''
        for record in self:
            if record.rule and record.work_class and record.work_class.locations:
                record.work_class_location = record.work_class.locations[0].id

    # 检修工班
    pms_work_class = fields.Many2one(string="检修工班(pms)", comodel_name="pms.department")

    work_class_name = fields.Char(string="工班名称",
                                  compute="_compute_work_class_name")

    use_pms_maintaince = fields.Selection(selection=[('yes', '是'), ('no', '否')],
                                          default="no",
                                          compute="_compute_use_pms_work_class", store=True)

    state = fields.Selection(string='状态',
                             selection=[('draft', '草稿'),
                                        ('published', '发布'),
                                        ('repairing', '维修中'),
                                        ('finished', '已完成')],
                             default='draft')

    time_table_data = fields.Many2one(string="运行图数据",
                                      comodel_name="metro_park_base.time_table_data",
                                      help="仅针对于收发车任务和运营任务有效, 主要目的是为了关联相关信息")

    train_no = fields.Char(string="车次号",
                           related="time_table_data.train_no",
                           store=True)

    out_location = fields.Many2one(string="出发场段",
                                   related="time_table_data.out_location")

    back_location = fields.Many2one(string="回库场段",
                                    related="time_table_data.back_location")

    remark = fields.Text(string='备注')
    operation_btn = fields.Char(string="操作按扭")
    send_state = fields.Selection([
        ('send', '发送'),
        ('not_send', '未发送'),
    ], default='not_send')

    # 复制的父计划的ID
    parent_id = fields.Integer(string='父计划ID')

    dispatch_users_info = fields.Many2one(comodel_name='funenc.wechat.user',
                                          string='派工人姓名(需要派工时候填写)')

    # 计划id
    plan_id = fields.Reference(string="计划id",
                               selection=[('metro_park_maintenance.day_plan', 'metro_park_maintenance.day_plan'),
                                          ('metro_park_maintenance.month_plan', 'metro_park_maintenance.month_plan'),
                                          ('metro_park_maintenance.week_plan', 'metro_park_maintenance.week_plan'),
                                          ('metro_park_maintenance.year_plan', 'metro_park_maintenance.year_plan')])

    active = fields.Boolean(default=True, help="用于假删除")

    @api.depends('rule', 'tmp_rule')
    def _compute_rule_info(self):
        '''
        计算显示名称
        :return:
        '''
        for record in self:
            if record.rule:
                record.rule_name = record.rule.name
                record.rule_no = record.rule.no
                record.rule_id = record.rule.id
            else:
                record.rule_name = record.tmp_rule.name
                record.rule_no = record.tmp_rule.no
                record.rule_id = record.tmp_rule.id

    @api.model
    def clear_plan(self, start_date, end_date, data_source):
        '''
        删除计划
        :param start_date:  开始日期
        :param end_date: 结束日期
        :param data_source: 数据来源
        :return:
        '''
        records = self.search([('data_source', '=', data_source),
                               ('start_date', '>=', start_date),
                               ('end_date', '<=', end_date)])
        records.unlink()

    @api.one
    @api.depends('date')
    def _compute_month(self):
        '''
        用于显示月份
        :return:
        '''
        if self.date:
            tmp_date = pendulum.parse(str(self.date))
            self.month = tmp_date.month
            self.year = tmp_date.year
            self.day = tmp_date.day

    @api.one
    @api.constrains('rule_type')
    def _get_work_content(self):
        '''
        用于修改作业内容的值
        :return:
        '''
        dic = {
            'run': '运营',
            'receive_train': '接车',
            'send_train': '发车'
        }
        if self.rule_type == 'normal':
            self.work_content = self.rule.name
        elif self.rule_type == 'temp':
            self.work_content = self.rule.no
        else:
            self.work_content = dic.get(self.rule_type)

    @api.model
    def del_plan_info(self, info, data_source=None):
        '''
        删除计划信息
        :param info:
        :param data_source:
        :return:
        '''
        record = self.browse(int(info.get('rule_info_id')))
        record.unlink()

    @api.model
    def add_plan_info(self, info):
        '''
        添加计划信息, 这里plan_id传进来是reference类型的
        :param info:
        :return:
        '''
        dev_id = info["dev_id"]
        plan_date = info["plan_date"]
        rule_id = int(info["rule_id"])
        data_source = info["data_source"]
        plan_id = info["plan_id"]

        rec = self.create([{
            "date": str(plan_date),
            "dev": dev_id,
            "rule": rule_id,
            "rule_type": "normal",
            "data_source": data_source,
            "state": "draft",
            "plan_id": plan_id
        }])

        return {
            'plan_id': rec.plan_id.id if rec.plan_id else '',
            'id': rec.id,
            'rule': rec.rule_name,
        }

    @api.model
    def get_last_plan_rule(self):
        '''
        取得设备历史修程信息, 版本1
        待优化
        :return:
        '''
        sql = 'SELECT info.id, data.dev, info.rule ,data.date FROM metro_park_maintenance_plan_data as data,' \
              'metro_park_maintenance_rule_info as info WHERE info.plan_data = data.id  order by data.date desc'
        self.env.cr.execute(sql)
        ids = [x[0] for x in self.env.cr.fetchall()]
        records = self.browse(ids)
        rst = {}
        for record in records:
            key = '{dev_id}_{rule_id}'.format(
                dev_id=record.dev.id, rule_id=record.rule.id)
            rst[key] = {
                "date": record.plan_data.date,
                "repair_num": record.repair_num
            }
        return rst

    @api.model
    def get_year_plan_history_info(self, start_date, ignore_repair_num=True):
        '''
        取得最后的历史修程信息,
        1、必需要在特定时间之前已经完成的。
        :return: 返回设备在什么时候进行的维修
        '''
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train').id
        # 车辆
        devs = self.env["metro_park_maintenance.train_dev"] \
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids

        # 规程, 只取年计划的规程
        rules = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', '=', 'year'), ('rule_status', '=', 'normal')])
        rule_ids = rules.ids

        # 通过设备唯一化来处理
        sql = 'select distinct on(dev) dev, rule, date, id from metro_park_maintenance_rule_info' \
              ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
              'and date < \'{date}\' and active=true and data_source = \'year\' order by dev, date desc'
        sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                         dev_ids=str(dev_ids).strip('[]'),
                         date=start_date)

        self.env.cr.execute(sql)
        ids = [x[3] for x in self.env.cr.fetchall()]
        records = self.env["metro_park_maintenance.rule_info"].browse(ids)

        # 处理跨月的情况, 导入进来的数据没有repair_day信息
        # if not ignore_repair_num:
        #     for record in records:
        #         if record.repair_day != record.rule.repair_days:
        #             tmp_rule_id = record.rule.id
        #             tmp_record = self.env["metro_park_maintenance.rule_info"].search(
        #                 [("rule", "=", tmp_rule_id),
        #                  ("date", ">=", start_date),
        #                  ("repair_num", '=', record.rule.repair_days)],
        #                 order="date asc", limit=1)
        #             records = records.union(tmp_record)

        return records

    @api.model
    def get_month_plan_history_info(self, start_date):
        '''
        取得最后的历史修程信息,
        1、必需要在特定时间之前已经完成的。
        :return: 返回设备在什么时候进行的维修
        '''
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train').id
        # 车辆
        devs = self.env["metro_park_maintenance.train_dev"] \
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids

        # 规程, 只取年计划的规程
        rules = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', '=', 'year'), ('rule_status', '=', 'normal')])
        rule_ids = rules.ids

        # 通过设备唯一化来处理
        sql = 'select distinct on(dev) dev, rule, date, id from metro_park_maintenance_rule_info' \
              ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
              'and date < \'{date}\' and active=true and data_source = \'month\' order by dev, date desc'
        sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                         dev_ids=str(dev_ids).strip('[]'),
                         date=start_date)

        self.env.cr.execute(sql)
        ids = [x[3] for x in self.env.cr.fetchall()]
        return self.env["metro_park_maintenance.rule_info"].browse(ids)

    @api.model
    def get_week_history_info(self, start_date, end_date):
        '''
        取得最后的历史修程信息,
        1、必需要在特定时间之前已经完成的。
        :return: 返回设备在什么时候进行的维修
        '''
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train').id
        # 车辆
        devs = self.env["metro_park_maintenance.train_dev"] \
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids

        # 只有周计划的修程
        rules = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', 'in', ['week']), ('rule_status', '=', 'normal')])
        rule_ids = rules.ids

        sql = 'select DISTINCT on(dev, rule) dev, rule, date, id from metro_park_maintenance_rule_info' \
              ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
              'and date < \'{start_date}\' and date > \'{end_date}\' ' \
              'and active=true and data_source=\'week\' order by dev asc, ' \
              'rule asc, date desc'
        sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                         dev_ids=str(dev_ids).strip('[]'),
                         start_date=start_date,
                         end_date=end_date)
        self.env.cr.execute(sql)
        ids = [x[3] for x in self.env.cr.fetchall()]
        return self.env["metro_park_maintenance.rule_info"].browse(ids)

    @api.model
    def get_week_history_balance_info(self, start_date, end_date):
        '''
        取得最后的历史修程信息,
        1、必需要在特定时间之前已经完成的。
        :return: 返回设备在什么时候进行的维修
        '''
        dev_type_electric_train = self.env.ref('metro_park_base.dev_type_electric_train').id
        # 车辆
        devs = self.env["metro_park_maintenance.train_dev"] \
            .search([('dev_type', '=', dev_type_electric_train)])
        dev_ids = devs.ids

        # 只有周计划的修程
        rules = self.env["metro_park_maintenance.repair_rule"] \
            .search([('target_plan_type', 'in', ['year'])])
        rule_ids = rules.ids

        sql = 'select DISTINCT on(dev, rule) dev, rule, date, id from metro_park_maintenance_rule_info' \
              ' where rule in ({rule_ids}) and dev in ({dev_ids}) ' \
              'and date < \'{start_date}\' and date > \'{end_date}\'' \
              ' and active=true and data_source=\'week\' order by dev asc, ' \
              'rule asc, date desc'
        sql = sql.format(rule_ids=str(rule_ids).strip('[]'),
                         dev_ids=str(dev_ids).strip('[]'),
                         start_date=start_date,
                         end_date=end_date)
        self.env.cr.execute(sql)
        ids = [x[3] for x in self.env.cr.fetchall()]
        return self.env["metro_park_maintenance.rule_info"].browse(ids)

    @api.model
    def get_history_rule_info(self, devs=None):
        '''
        取得设备历史修程信息，版本2
        待优化
        :return:
        '''
        if devs:
            sql = 'SELECT DISTINCT id, dev, rule, date FROM metro_park_maintenance_rule_info ' \
                  'where dev in (' + ','.join(str(devs)) + \
                  ') and state=\'published\' order by date desc'
        else:
            sql = 'SELECT DISTINCT id, dev, rule, date FROM metro_park_maintenance_rule_info ' \
                  'where state=\'published\' order by date desc'
        self.env.cr.execute(sql)
        ids = [x[0] for x in self.env.cr.fetchall()]
        records = self.browse(ids)
        rst = {}
        for record in records:
            key = '{dev_id}_{rule_id}'.format(
                dev_id=record.dev.id, rule_id=record.rule.id)
            rst[key] = record.plan_data.date
        return rst

    @api.model
    def get_history_rule_info_before(self, date):
        '''
        取得设备历史修程信息，版本2, 这个取得了所有的设备信息
        待优化
        :return:
        '''
        sql = "SELECT DISTINCT on(dev) dev, id, rule, date FROM metro_park_maintenance_rule_info where date < '" + date + \
              "' and state='published' order by dev asc, date desc"
        self.env.cr.execute(sql)
        ids = [x[1] for x in self.env.cr.fetchall()]
        records = self.browse(ids)
        rst = {}
        for record in records:
            key = '{dev_id}_{rule_id}'.format(
                dev_id=record.dev.id, rule_id=record.rule.id)
            rst[key] = record.plan_data.date
        return rst

    @api.model
    def get_last_repair_date(self, rule_ids, date_str):
        '''
        取得
        :return:
        '''
        sql = 'SELECT DISTINCT on(dev) dev, id, rule, date FROM metro_park_maintenance_rule_info ' \
              'where rule in (' + str(rule_ids).replace("[", "").replace("]", "") + ') and state=\'published\' and date < \'' \
              + date_str + '\' order by dev asc, date desc'
        self.env.cr.execute(sql)
        ids = [x[1] for x in self.env.cr.fetchall()]
        records = self.browse(ids)
        rst = {}
        for record in records:
            rst[record.dev.id] = record.plan_data.date
        return rst

    @api.one
    @api.depends("work_start_time", "work_end_time")
    def compute_work_time(self):
        '''
        计算工作时间，以xx:xx-xx:xx的形式显示
        :return:
        '''
        if self.work_start_time and self.work_end_time:
            start_time = self.env['metro_park_base.time_helper'].time_int_to_time(self.work_start_time)['time']
            end_time = self.env['metro_park_base.time_helper'].time_int_to_time(self.work_end_time)['time']
            # start_time = self.datetime_local_data(self.work_start_time)
            # end_time = self.datetime_local_data(self.work_end_time)
            self.work_time = '{start_time}-{end_time}'.format(start_time=start_time, end_time=end_time)
        else:
            self.work_time = '09:00-17:00'

    @api.model
    def datetime_local_data(self, date_time):
        """
        将10位时间戳转为+8小时的日期
        :param date_time: 毫秒级时间戳(int)
        :return: data_str %H:%M
        """
        dt = datetime.datetime.fromtimestamp(float(date_time)/10 ** (len(str(date_time)) - 10),
                                             datetime.timezone(datetime.timedelta(hours=8)))
        # return dt.strftime('%Y-%m-%d %H:%M:%S')
        return dt.strftime('%H:%M')

    @api.model
    def get_devs(self, date):
        '''
        取得特定日期的检修设备
        :param date:
        :return:
        '''
        records = self.search([('date', '=', date)])
        return records.mapped("dev.id")

    @api.model
    def get_detain_train_devs(self, date):
        '''
        取得特定日期的检修设备
        :param date:
        :return:
        '''
        records = self.search([('date', '=', date), ('rule.balance', '=', 'yes')])
        return records.mapped("dev.id")

    @api.multi
    def timing_task_maintenance_plan(self):
        maintenance_datas = self.search([('rule_type', '=', 'normal')])
        for maintenance_data in maintenance_datas:
            if maintenance_data.work_end_time:
                if (maintenance_data.work_end_time > datetime.datetime.now()) \
                        and maintenance_data.state != 'finished':
                    template = self.env.ref(
                        'metro_park_production.early_waring_message', raise_if_not_found=True)
                    content = template.render({
                        'message': {
                            'type_description': '检修任务未完成预警',
                            'content': "%s车 工单号%s" % (
                                maintenance_data.plan_data.dev.dev_name, maintenance_data.dev_no),
                            'remark': '',
                            'data': pendulum.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        },
                    }, engine='ir.qweb', minimal_qcontext=True, ).decode()
                    title = '预警提醒'
                    action = {
                        'name': '查看用户',
                        'type': 'ir.actions.act_window',
                        'res_id': self.id,
                        'res_model': 'res.users',
                        'target': 'new',
                        'views': [(self.env.ref('base.change_password_wizard_view').id, 'form')],
                        'class_names': 'btn-sm btn-link',
                    }
                    self.env['res.users'].post_bus_message(
                        content, callback_name='callback_name', title=title, action=action)

    @api.model
    def _compute_rail_type(self):
        '''
        计算轨道类型
        :return:
        '''
        pass

    def _compute_use_pms_work_class(self):
        '''
        计算是否使用pms工班
        :return:
        '''
        config = self.env['metro_park_base.system_config'].get_configs()
        use_pms_maintaince = config.get('start_pms', False)
        for record in self:
            record.use_pms_maintaince = use_pms_maintaince

    @api.multi
    def get_tasks_after_run(self):
        '''
        取处运营任务之后的检修任务，
        一般是找到这些任务后查看作业要求,
        如果是有多个的话可能还要调到多处去才行
        :return:
        '''
        self.ensure_one()

        main_line_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_run_rule').id
        receive_train_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_receive_train_rule').id
        send_train_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_send_train_rule').id

        run_task = self.get_next_run_task()
        if not run_task:
            # 后边没有运营任务就取当天所有的
            tasks = self.search(
                [('date', '=', str(self.date)),
                 ('dev', '=', self.dev.id),
                 ('data_source', '=', 'day'),
                 ('work_start_time', '>=', str(self.work_end_time)),
                 ('rule', 'not in', [main_line_rule_id, receive_train_rule_id, send_train_rule_id])],
                order="work_start_time asc")
        else:
            # 后边有运营任务就取到下一个运营任务的
            tasks = self.search(
                [('date', '=', str(self.date)),
                 ('dev', '=', self.dev.id),
                 ('work_start_time', '>=', str(self.work_end_time)),
                 ('work_end_time', "<=", str(run_task.work_end_time)),
                 ('rule', 'not in', [main_line_rule_id, receive_train_rule_id, send_train_rule_id])],
                order="work_start_time asc")

        return tasks

    @api.multi
    def have_next_run_task(self):
        '''
        是否之后还有运营任务
        :return:
        '''
        return True if self.get_next_run_task() is not None else False

    @api.multi
    def have_prev_task(self):
        '''
        是否之前有任务
        :return:
        '''
        return True if self.get_prev_run_task() is not None else False

    @api.multi
    def is_one_more_task(self):
        '''
        多余一个任务
        :return:
        '''
        self.ensure_one()

        main_line_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_run_rule').id

        tasks = self.search(
            [('date', '=', str(self.date)),
             ('dev', '=', self.dev.id),
             ('rule', 'in', [main_line_rule_id])],
            order="work_start_time asc")

        return len(tasks) > 1

    @api.multi
    def get_next_run_task(self):
        '''
        当前是一个收车任务，但后面还有运行， 高峰车的情况, 这个也是判断高峰车的标准 train_no
        :return:
        '''
        date_str = str(self.date)
        main_line_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_run_rule').id
        # 同一车跑了两个任务, 那么第一个不用考虑
        # 第二天的检修任务，但轨道要对应上
        records = self.search([('rule', '=', main_line_rule_id),
                               ('dev.id', '=', self.dev.id),
                               ('date', '=', date_str),
                               ('work_start_time', '>', self.work_end_time)],
                              order="work_start_time asc")
        return records[0] if records else None

    @api.multi
    def get_prev_run_task(self):
        '''
        取得上一个任务
        :return:
        '''
        date_str = str(self.date)
        main_line_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_run_rule').id
        records = self.search([('rule', '=', main_line_rule_id),
                               ('dev.id', '=', self.dev.id),
                               ('date', '=', date_str),
                               ('work_end_time', '<', self.work_start_time)],
                              order="work_start_time asc")
        return records[0] if records else None

    @api.model
    def get_tasks_before_run(self, date, dev_id):
        '''
        取得运营之前的任务
        :return:
        '''
        main_line_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_run_rule').id
        receive_train_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_receive_train_rule').id
        send_train_rule_id = \
            self.env.ref('metro_park_maintenance.main_line_send_train_rule').id

        run_task_ids = [main_line_rule_id, receive_train_rule_id, send_train_rule_id]
        run_task = self.get_next_run_task()
        if not run_task:
            # 后边没有运营任务就取当天所有的
            tasks = self.search(
                [('date', '=', date),
                 ('dev', '=', self.dev.id),
                 ('rule', 'not in', run_task_ids)],
                order="work_start_time asc")
        else:
            # 后边有运营任务就取到下一个运营任务前的检修任务
            tasks = self.search(
                [('date', '=', date),
                 ('dev', '=', dev_id),
                 ('work_end_time', "<=", str(run_task.work_end_time)),
                 ('rule', 'not in', run_task_ids)],
                order="work_start_time asc")

        return tasks

    @api.multi
    def del_year_plan_rule_info(self):
        '''
        删除年计划规程信息
        :return:
        '''
        self.unlink()

    @api.multi
    def unlink(self):
        '''
        重写方法，删除相应工单
        :return:
        '''
        # 先删除相应的工单
        return super(RuleInfo, self).unlink()

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        '''
        创建计划
        :param vals_list:
        :return:
        '''
        dates = []
        plan_ids = []
        for val in vals_list:
            if not val["date"]:
                raise exceptions.ValidationError('创建rule info必需包含date字段!')

            if "plan_id" not in val:
                raise exceptions.ValidationError('创建rule info必需包含plan_id字段!')
            else:
                plan_ids.append(val['plan_id'])

            dates.append(val["date"])

        # 缓存，加快效率
        model = self.env["metro_park_maintenance.plan_data"]
        records = model.search([("date", 'in', dates), ("plan_id", 'in', plan_ids)])
        dev_date_cache = {}
        for record in records:
            key = '{date}_{dev}_{plan_id}'.format(
                date=str(record.date), dev=record.dev.id, plan_id=val["plan_id"])
            dev_date_cache[key] = record

        for val in vals_list:
            date = val["date"]
            date_obj = pendulum.parse(date)
            dev = val.get('dev', None)
            if dev:
                key = '{date}_{dev}_{plan_id}'.format(
                    date=date, dev=dev, plan_id=val["plan_id"])
                old_record = dev_date_cache.get(key, False)
                if not old_record:
                    old_record = model.create([{
                        "dev": val["dev"],
                        "year": date_obj.year,
                        "month": date_obj.month,
                        "day": date_obj.day,
                        "plan_id": val["plan_id"]
                    }])
                    # 缓存新创建的记录
                    dev_date_cache[key] = old_record
                val["plan_data"] = old_record.id
            else:
                val["dev"] = False

        return super(RuleInfo, self).create(vals_list)

    @api.model
    def week_create_data(self, *args, **kwargs):
        '''
        创建周计划
        :param args:
        :param kwargs:
        :return:
        '''
        form_id = \
            self.env.ref('metro_park_maintenance.week_rule_info_form').id

        return {
            'name': '创建周计划',
            'type': 'ir.actions.act_window',
            'res_model': 'metro_park_maintenance.rule_info',
            'target': 'new',
            'views': [(form_id, 'form')],
            'context': {
                'active_id': self._context.get('active_id'),
                'active_model': self._context.get('active_model'),
            }
        }

    @api.multi
    def clear_duplicate_data(self):
        '''
        去除重复的数据
        :return:
        '''
        parent_ids = self.mapped("parent_id")
        rst = []
        for record in self:
            if record.id in parent_ids:
                rst.append(record.id)
        return rst

    @api.depends("use_pms_maintaince", "work_class", "pms_work_class")
    def _compute_work_class_name(self):
        '''
        计算作业部门显示名称
        :return:
        '''
        for record in self:
            if record.use_pms_maintaince == 'yes':
                if record.pms_work_class:
                    names = record.pms_work_class.mapped("department")
                    record.work_class_name = ','.join(names)
            else:
                if record.work_class:
                    names = record.work_class.mapped("name")
                    record.work_class_name = ','.join(names)

    @api.multi
    def name_get(self):
        '''
        重写，显示个修次
        :return:
        '''
        result = []
        for record in self:
            if record.repair_days:
                result.append((record.id, "%s(第%s天),%s" % (
                    record.rule_name, record.repair_days, record.id)))
            else:
                result.append((record.id, "%s,%s" % (
                    record.rule_name, record.id)))

        return result

    @api.model
    def update_rule_info(self, data):
        '''
        更新规程信息
        :return:
        '''
        old_info = data["old_info"]
        new_info = data["new_info"]

        dev_id = old_info["dev_id"]
        new_dev_id = new_info["dev_id"]

        old_info = data["old_info"]
        new_info = data["new_info"]

        rule_info_id = old_info["rule_info_id"]

        # 如果设备不同则删除原来的
        if dev_id != new_dev_id:
            old_rule_info = self.browse(int(rule_info_id))
            old_rule_info.write({
                "active": False
            })
            # 添加新的数据
            self.add_plan_info(new_info)
        else:
            rule = self.browse(int(rule_info_id))
            rule.write({
                "date": new_info["plan_date"],
                "dev": dev_id
            })

    @api.depends("rule")
    def _compute_location(self):
        '''
        如果是规则有位置要求，则使用规的位置，不然就都可以
        :return:
        '''
        all_locations = \
            self.env["metro_park_base.location"].search([])
        all_location_names = '/'.join(all_locations.mapped('name'))

        for record in self:
            if record.final_location:
                record.compute_location = record.final_location.name
            elif record.rule:
                locations = record.rule.locations
                location_names = locations.mapped("name")
                record.compute_location = '/'.join(location_names)
            else:
                record.compute_location = all_location_names

    @api.onchange("user_define_dev")
    def _on_change_user_define_dev(self):
        '''
        用户指定的时候设备也发生变化
        :return:
        '''
        if self.user_define_dev:
            self.dev = self.user_define_dev.id

    @api.depends('rule')
    def _compute_user_define_dev_visible(self):
        '''
        只有运行营任务才让选择设备
        :return:
        '''

        for record in self:
            if record.rule and record.rule_type == 'run':
                record.user_define_dev_visible = True
                record.user_define_location_visible = True
            else:
                record.user_define_dev_visible = False
                record.user_define_location_visible = False

    @api.multi
    def get_spec_tasks(self, rule_id):
        '''
        取得洗车任务
        :return:
        '''

        def func(record):
            return record.rule.id == rule_id

        return self.filtered(func=func)

    @api.multi
    def get_rule_display_name(self):
        '''
        取得规程显示名称
        :return:
        '''
        self.ensure_one()
        if self.repair_days > 1 and self.repair_day > 0:
            return "{rule_name}(第{day}天)".format(
                rule_name=self.rule.name, day=self.repair_day)
        else:
            return self.rule_name

    @api.model
    def _compute_is_mile(self):
        '''
        计算是否为公里数, 放在每条线路的基础数据中去实线
        :return:
        '''
        assert False, '请在线路数据中实现此函数!'

    @api.multi
    def get_selected_devs_temp_rule_ids(self):
        '''
        取得检技通选择的domain
        :return:
        '''
        plan_id = self.env.context.get('plan_id')
        exclude_keys = []
        rule_infos = self.env['metro_park_maintenance.rule_info'].search(
            [('plan_id', '=', 'metro_park_maintenance.rule_info, {plan_id}'.format(plan_id=plan_id))])
        for info in rule_infos:
            if info.tmp_rule:
                key = "{rule_id}_{dev_id}".format(rule_id=info.tmp_rule.id, dev_id=info.dev.id)
                exclude_keys.append(key)
        day_plan = self.env['metro_park_maintenance.day_plan'].browse(plan_id)
        ids = self.mapped("dev.id")
        rule_ids = self.env['metro_park_maintenance.repair_tmp_rule']\
            .get_devs_temp_rules(ids, str(day_plan.plan_date), exclude_keys)
        return rule_ids

    @api.depends('dev', 'rule')
    def _compute_pre_date_miles(self):
        '''
        获取上一日公里数
        :return:
        '''
        pass

    @api.multi
    def user_define_dev_action(self):
        '''
        用户指定设备
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.user_define_dev",
            'view_mode': 'form',
            "target": "new",
            'context': {
                'plan_info_id': self.id,
            },
            "views": [[self.env.ref('metro_park_maintenance.user_define_dev_form').id, "form"]]
        }

    @api.model
    def add_selected_temp_rules(
            self, day_plan_id, select_ids, temp_rule_ids):
        '''
        安排检技通
        :param day_plan_id:
        :param select_ids:
        :param temp_rule_ids:
        :return:
        '''
        day_plan = self.env['metro_park_maintenance.day_plan'].browse(day_plan_id)
        rule_infos = self.browse(select_ids)
        train_ids = rule_infos.mapped("dev.id")
        vals = []
        for train_id in train_ids:
            for rule_id in temp_rule_ids:
                vals.append({
                    "dev": train_id,
                    "temp_rule_id": rule_id,
                    "plan_id": "metro_park_maintenance.day_plan, {plan_id}".format(
                        plan_id=day_plan_id),
                    "data_source": "day",
                    "rule_type": 'temp',
                    "date": str(day_plan.plan_date)
                })
        self.create(vals)

    @api.depends("miles", "last_repair_miles")
    def _compute_miles_after_last_repair(self):
        '''
        计算距离上次里程公里数
        :return:
        '''
        for record in self:
            record.miles_after_last_repair = record.miles - record.last_repair_miles

    @api.depends("plan_id", "dev")
    def _compute_last_repair_info(self):
        '''
        计算上次里程修信息， 线别中去实现此函数
        :return:
        '''
        pass

    @api.depends('plan_id')
    def _compute_last_mile(self):
        '''
        计算里程数, 根据公里历史记录计算里程数
        :return:
        '''

        for record in self:
            if not record.plan_id or not record.dev:
                continue
            pre_date_train_infos = record.plan_id.pre_date_train_infos.filtered(
                lambda item: item.train.id == record.dev.id)
            record.miles = pre_date_train_infos.miles

    @api.depends("miles", "last_repair_miles")
    def _compute_miles_after_last_repair(self):
        '''
        计算距离上次里程公里数
        :return:
        '''
        for record in self:
            record.miles_after_last_repair = record.miles - record.last_repair_miles





