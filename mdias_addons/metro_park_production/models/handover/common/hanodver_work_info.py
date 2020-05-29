# -*- coding: utf-8 -*-

from odoo import models, fields


class HandoverWorkInfo(models.Model):
    _name = 'metro_park_production.handover.work_info'
    _track_log = True

    line_execute_time_table = fields.Many2one(comodel_name='metro_park_base.time_table', string='正线执行时刻表')
    track_ids = fields.Many2many('metro_park_base.rails_sec',
                                 'handover_work_info_and_track_ref',
                                 'work_info_id',
                                 'track_id', string='停电股道',
                                 domain=[('is_track', '=', True)])
    stop_electric_area = fields.Many2many('metro_park_base.electric_area',
                                          'handover_work_info_electric_area_ref',
                                          'work_info_id',
                                          'area_id'
                                          '停电区域')
    track_ground_wire = fields.Text("股道地线")
    electric_area_ground_wire = fields.Text("区域地线")

    eight_hundred_radio = fields.Text("800兆电台")

    four_hundred_radio = fields.Text("400兆电台")
    standby_application_condition = fields.Text(string='备品情况')
    equipment_condition = fields.Text("设备情况")
    construction_condition = fields.Text("施工情况")

    track_condition = fields.One2many('metro_park_production.handover.parker', 'handover_work_info_id',
                                      string='股道存车情况')
    track_type_condition = fields.One2many('metro_park_production.handover.track_type_condition',
                                           'handover_work_info_id',
                                           string='股道类型使用情况')
    plan_carport = fields.Many2many('metro_park_dispatch.train_out_plan',
                                    'handover_work_info_and_train_out_plan_ref',
                                    'work_info_id', 'train_id', string='库备车')
    other_remark = fields.Text(string='其他交班事宜')
