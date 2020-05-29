
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
import pendulum
import logging
import json

try:
    import websocket
    from websocket import create_connection
except ImportError:
    websocket = None

_logger = logging.getLogger(__name__)

TASK_TYPE_RUN = 'run'
TASK_TYPE_PLAN = 'plan'
TASK_TYPE_MILE = 'mile'


class WorkShopDayPlan(models.Model):
    '''
    车间日生产计划
    '''
    _name = 'metro_park_dispatch.work_shop_day_plan'
    _rec_name = 'plan_date'
    _order = "plan_date desc"
    
    state = fields.Selection(string='状态',
                             selection=[("un_publish", "未发布"), ("published", "已发布")],
                             default="un_publish")

    plan_date = fields.Date(string='计划日期')

    day_plan_id = fields.Many2one(string="日计划",
                                  comodel_name="metro_park_maintenance.day_plan")

    plan_datas = fields.One2many(string="计划数据",
                                 comodel_name="metro_park_dispatch.work_shop_day_plan_data",
                                 inverse_name="plan_id")

    run_trains = fields.Many2many(string="运营车",
                                  comodel_name="metro_park_dispatch.cur_train_manage",
                                  relation="work_shop_day_plan_cur_train_rel",
                                  column1="work_shop_day_plan_id",
                                  column2="cur_train_id")

    hot_backup_train = fields.Many2many(string="热备车",
                                        comodel_name="metro_park_dispatch.cur_train_manage",
                                        relation="work_shop_day_plan_hot_backup_train_rel",
                                        column1="work_shop_day_plan_id",
                                        column2="cur_train_id")

    btns = fields.Char(string="操作按扭")


    @api.multi
    def view_day_run_plan_data(self):
        '''
        查看日期数据
        :return:
        '''
        tree_id = self.env.ref(
            'metro_park_dispatch.work_shop_day_plan_data_list').id
        form_id = self.env.ref(
            'metro_park_dispatch.work_shop_day_plan_data_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "metro_park_dispatch.work_shop_day_plan_data",
            "name": "车间日生产计划",
            "context": {
                "work_shop_day_plan_id": self.id,
            },
            "views": [[tree_id, "tree"], [form_id, "form"]],
            'domain': [('plan_id', '=', self.id)]
        }

    @api.multi
    def set_run_trains(self):
        '''
        设置运营车
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.run_train_wizard",
            'view_mode': 'form',
            "target": "new",
            "context": {
                "default_cur_trains": self.run_trains.ids,
                "default_work_shop_day_plan_id": self.id,
            },
            "views": [[self.env.ref('metro_park_dispatch.run_train_wizard_form').id, "form"]]
        }

    @api.multi
    def auto_calc(self):
        '''
        计算车辆和位置
        :return:
        '''
        form_id = self.env.ref('metro_park_dispatch.day_run_plan_compute_wizard_form').id
        time_table_id = self.env["metro_park_dispatch.nor_time_table_config"]\
            .get_date_config(str(self.plan_date))

        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.day_run_plan_compute_wizard",
            'view_mode': 'form',
            "target": "new",
            "context": {
                "default_run_trains": self.run_trains.ids,
                "default_day_run_plan_id": self.id,
                "default_time_table": time_table_id
            },
            "views": [[form_id, "form"]]
        }

    @api.multi
    def plan_rails(self):
        '''
        安全轨道
         1、更改状态, 安排当日回库的轨道, 根据前一天的收车计划和次日的检修计划和发车计划决定收车的位置
         2、设定次日的发车轨道.
        :return:
        '''

        # 如果没有前一天的收车计划的话则只是发布次日的检修计划
        plan_date = str(self.plan_date)

        # 这里要避免重复发布
        plan_datas = self.env["metro_park_dispatch.work_shop_day_plan_data"] \
            .search([('plan_date', '=', plan_date)])

        # 缓存数据, 根据time_table_data进行分组
        plan_data_cache = {}
        for info in plan_datas:
            if info.time_table_data_id:
                plan_data_cache.setdefault(info.time_table_data_id.id, []).append(info)

        # 安排收车轨道
        config = self.env["metro_park_base.system_config"].get_configs()
        calc_host = config["calc_host"] or '127.0.0.1:9520'
        ws = create_connection("ws://{host}".format(host=calc_host))

        location = self.env.user.cur_location
        if not location:
            raise exceptions.ValidationError("当前用户没有设置location")

        line = location.line
        locations_ids = line.get_locations()

        # 分别安排出库位置
        for location_id in locations_ids:
            # 发送服务器计算, 这里是取得计划前一日的轨道信息
            rail_info = self.get_rail_plan_info(location_id)
            ws.send(json.dumps({"cmd": "plan_rail", "data": rail_info}))
            result = ws.recv()
            result = json.loads(result)

            # 设置回库轨道
            self.set_back_rails(rail_info, result)

        ws.close()

        # 检调提交次日计划, 场调再发布当日
        self.set_out_rail(plan_date)

    @api.model
    def set_back_rails(self, plan_data, rst):
        '''
        确定当日收车轨道
        :return:
        '''
        if rst["status"] != 200:
            raise exceptions.Warning('计算出错！')

        tasks = plan_data["tasks"]
        rails = plan_data["rails"]
        vals = rst["datas"]

        info_ids = []
        for index, task in enumerate(tasks):
            data_id = task["data_id"]
            info_ids.append(data_id)
            val = vals[index]
            info = self.env["metro_park_dispatch.work_shop_day_plan_data"]\
                .browse(data_id)
            # 值是从1开始的，所以这里要减1
            info.rail = rails[val - 1]

    @api.model
    def set_out_rail(self, date):
        '''
        设置发车的股道
        :param date:
        :return:
        '''
        date_obj = pendulum.parse(date)
        prev_date_obj = date_obj.subtract(days=1)

        receive_train_rule_id = \
            self.env.ref('metro_park_base_data_10.main_line_receive_train_rule').id
        back_datas = \
            self.env["metro_park_dispatch.work_shop_day_plan_data"] \
                .search([('plan_date', '=', prev_date_obj.format('YYYY-MM-DD'))])

        train_back_rail_cache = dict()
        for plan in back_datas:
            if plan.rule.id == receive_train_rule_id:
                train_back_rail_cache[plan.train_id.id] = plan.rail.id

        out_datas = \
            self.env["metro_park_dispatch.train_out_plan"] \
                .search([('date', '=', date_obj.format('YYYY-MM-DD'))],
                        order="plan_out_time desc")
        for out_data in out_datas:
            if out_data.train_id.id in train_back_rail_cache:
                out_data["rail"] = train_back_rail_cache[out_data.train_id.id]

    @api.multi
    def publish_plan(self):
        '''
        发布计划, 当日的收车和次日的发车, 发布以后再到收发车那边再进行发布，各条线路各自发布
        :return:
        '''
        pass

    @api.multi
    def reback_plan(self):
        '''
        撤回已经发布的计划, 各条线路各自处理
        :return:
        '''
        pass

    @api.multi
    def reback_day_plan(self):
        '''
        撤回日计划
        :return:
        '''
        # 删除数据
        self.plan_datas.unlink()

        # 设置日计划状态为unplublished
        self.day_plan_id.state = 'draft'

        # 删除自身
        self.unlink()
