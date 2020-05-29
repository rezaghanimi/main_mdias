
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json

try:
    import websocket
    from websocket import create_connection
except ImportError:
    websocket = None


class DayRunPlanComputeWizard(models.TransientModel):
    '''
    车间日生产计划计算向导
    '''
    _name = 'metro_park_dispatch.day_run_plan_compute_wizard'
    
    time_table = fields.Many2one(string='运行图',
                                 comodel_name='metro_park_base.time_table')
    day_run_plan_id = fields.Many2one(string='日计划',
                                      comodel_name='metro_park_dispatch.work_shop_day_plan')
    run_trains = fields.Many2many(string='运营车',
                                  comodel_name='metro_park_dispatch.cur_train_manage',
                                  relation='day_run_plan_compute_wizard_and_cur_train_rel',
                                  col1='compute_wizard_id',
                                  col2='cur_train_id')

    @api.multi
    def on_ok(self):
        '''
        确认, 添加运行图并自动计算
        :return:
        '''

        # 取得用于计划的数据
        plan_datas = self.day_run_plan_id.get_plan_datas({
            "time_table_id": self.time_table.id,
            "run_trains": self.run_trains.mapped("train.id")
        })

        if len(plan_datas["data"]['tasks']) > 0:
            # 安排收车轨道
            config = self.env["metro_park_base.system_config"].get_configs()
            calc_host = config["calc_host"] or '127.0.0.1:9520'
            ws = create_connection("ws://{host}".format(host=calc_host))

            ws.send(json.dumps(plan_datas))
            result = ws.recv()
            result = json.loads(result)
        else:
            result = []

        # 处理计算结果
        self.day_run_plan_id.deal_plan_data(plan_datas, result)

