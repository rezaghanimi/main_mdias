# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class RepairTmpRule(models.Model):
    '''
    检技通，检技通的本质是一个临时规则
    '''
    _name = 'metro_park_maintenance.repair_tmp_rule'
    _description = "检技通"
    _rec_name = 'no'
    _track_log = True

    no = fields.Char(string='检技通号')
    name = fields.Char(string='名称')
    sequence = fields.Char(string='序号')
    content = fields.Text(string='详细内容')

    check_tech_info_id = fields.Char(string='PMS传递过来的唯一标识')

    # 由于地铁公司是专人发检技通，所以是需要记录是谁发的
    work_user = fields.Many2one(string='下发工程师', comodel_name='res.users')

    # 必需要写是针对于哪些车辆
    trains = fields.Many2many(string='针对车辆',
                              comodel_name='metro_park_maintenance.train_dev',
                              relation='tmp_rule_dev_rel',
                              col1='tmp_rule_id',
                              col2='dev_id',
                              required=True)

    repair_rules = fields.Many2many(string='结合修程',
                                    comodel_name='metro_park_maintenance.repair_rule',
                                    relation='tmp_rule_and_rule_rel',
                                    col1='tmp_rule_id',
                                    col2='rule_id')

    start_date = fields.Date(string='开始日期', help='开始日期')
    end_date = fields.Date(string='结束日期', help='结束日期')

    # 上边的时间只是个宽泛的时间, 这个才是真实的耗时
    time_consume = fields.Float(string='每车耗时(分钟)')

    # 这个用于查询统计用
    plan_train_count = fields.Integer(string='计划完成车辆数',
                                      compute='_compute_plan_train_count')
    finished_train_count = fields.Integer(string='实际完成车辆数', help="用于统计")

    button = fields.Char(string='操作', help='占位符')
    data_source = fields.Selection(
        selection=[('mdias', 'mdias'), ('pms', 'pms')], default='mdias')

    @api.depends('trains')
    @api.one
    def _compute_plan_train_count(self):
        '''
        计算列车数量
        :return:
        '''
        self.finished_train_count = len(self.trains.ids)

    @api.multi
    def view_record(self):
        '''
        查看
        :return:
        '''
        self.ensure_one()
        action = self.env.ref('metro_park_maintenance.repair_tmp_rule_act_window').read()[0]
        form_id = self.env.ref('metro_park_maintenance.repair_tmp_rule_form').id
        action['view_mode'] = 'form'
        action['res_id'] = self.id
        action['views'] = [[form_id, 'form']]
        action['target'] = 'new'
        return action

    @api.multi
    def edit_record(self):
        '''
        编加
        :return:
        '''
        self.ensure_one()
        action = self.env.ref('metro_park_maintenance.repair_tmp_rule_act_window').read()[0]
        form_id = self.env.ref('metro_park_maintenance.repair_tmp_rule_form').id
        action['view_mode'] = 'form'
        action['res_id'] = self.id
        action['context'] = {
            'form_view_initial_mode': 'edit'
        }
        action['target'] = 'new'
        action['views'] = [[form_id, 'form']]
        return action

    @api.multi
    def unlink_record(self):
        '''
        删除
        :return:
        '''
        self.ensure_one()
        self.unlink()

    @api.model
    def manual_sync(self):
        '''
        手动同步检技通
        :return:
        '''
        try:
            self.env['mdias_pms_interface'].get_repair_tmp_rule()
            return 'success'
        except Exception as error:
            _logger.info('manual sync error:', error)
            return 'fail'

    @api.model
    def import_data_repair_tmp_rule(self):
        '''
        导入数据
        :return:
        '''
        form_id = self.env.ref("metro_park_maintenance.repair_tmp_rule_form_import").id
        return {
            'name': '检技通导入',
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': 'metro_park_maintenance.repair_tmp_rule_import',
            'target': 'new',
        }

    @api.model
    def export_data_repair_tmp_rule(self):
        return {
            'name': '检技通导出',
            'type': 'ir.actions.act_url',
            'url': '/repair_tmp_rule/export_data_repair_tmp_rule'
        }

    @api.model
    def create_data_rec(self):
        view_id = self.env.ref('metro_park_maintenance.repair_tmp_rule_form').id
        return {
            'type': 'ir.actions.act_window',
            'views': [[view_id, 'form']],
            'view_mode': 'form',
            'res_model': 'metro_park_maintenance.repair_tmp_rule',
            'target': 'new',
        }

    @api.model
    def get_temp_repair_rules(self, date_str):
        '''
        取得检技通信息
        :return:
        '''
        # 取得当天所有的检技通
        records = self.search(
            [('start_date', '<=', date_str), ('end_date', '>=', date_str)])

        # 取得当天已经安排了的信息
        planed_infos = self.env['metro_park_maintenance.temp_rule_plan_history'].search(
            [('rule_info_id.date', '=', date_str)])
        planed_info_cache = {info.key: True for info in planed_infos}
        temp_rule_infos = []
        for record in records:

            if not record.trains:
                continue

            for train in record.trains:
                key = '{rule_id}_{dev_id}'.format(rule_id=record.id, dev_id=train.id)
                if key not in planed_info_cache:
                    temp_rule_infos.append({
                        "train_id": train.id,
                        "tmp_rule_id": record.id,
                    })

    @api.model
    def get_devs_temp_rules(self, dev_ids, date_str, exclude_keys):
        '''
        取得检技通信息
        :return:
        '''
        # 取得当天所有的检技通
        records = self.search(
            [('start_date', '<=', date_str),
             ('end_date', '>=', date_str), ('trains', 'in', dev_ids)])
        train_ids = records.mapped('trains.id')
        ids = records.ids
        exclude_ids = []
        # 取得当天已经安排了的信息
        planed_infos = self.env['metro_park_maintenance.temp_rule_plan_history'].search(
            [('rule_info_id.date', '=', date_str)])
        planed_info_cache = {info.key: True for info in planed_infos}
        for record in records:
            if not record.trains:
                continue
            for train in record.trains:
                key = '{rule_id}_{dev_id}'.format(rule_id=record.id, dev_id=train.id)
                if key in planed_info_cache or key in exclude_keys:
                    exclude_ids.append(record.id)

        rst = []
        for tmp_id in ids:
            if tmp_id not in exclude_ids:
                rst.append(tmp_id)

        return rst

