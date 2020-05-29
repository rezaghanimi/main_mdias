# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


def get_many2many_content(m2m, field):
    """
    获取多对多字段的打印文本
    :param m2m: Many2Many的字段
    :param field: 想要获取的文本字段
    :return: 遍历字段后拼接field的str
    """
    m2m_list = []
    for order in m2m:
        m2m_list.append(str(getattr(order, field)))
    return '，'.join(m2m_list)


def plan_carport_get_many2many_content(m2m, field):
    m2m_list = []
    for order in m2m:
        plan_carport = getattr(order, field)
        train_name = plan_carport.train_name
        m2m_list.append(train_name)
    return '，'.join(m2m_list)


def format_context(order):
    """
    格式化内容，防止内容为空时前端页面显示为false
    :param order:
    :return:
    """
    if order:
        return order
    else:
        return "/"


def format_list(train_list, row, col):
    """
    因为模板的原因，table除第一行外需要特殊的格式化
    :param train_list:
    :param row:
    :param col:
    :return:
    """
    track_condition = [["" for i in range(row)] for j in range(col)]
    if len(train_list) > row:
        for i in range(row, len(train_list)):
            x = i // row
            y = i % row
            track_condition[x - 1][y] = train_list[i].train_id.dev_name
    return track_condition


def format_list_head(train_list, row):
    """
    因为模版的原因，table的第一行需要特殊的格式化
    :param train_list:
    :param row:
    :return:
    """
    length = len(train_list)
    result_list = [i.train_id.dev_name for i in train_list[:row]]
    if length < row:
        result_list = result_list + ["" for i in range(row - length)]
    return result_list


def format_text(train_list, col):
    length = len(train_list)

    if length:
        result_list = [i.description for i in train_list[1:]]
        result_list = result_list + ["" for i in range(col - len(train_list))]
    else:
        return ["" for i in range(col - 1)]
    return result_list


def get_print_data(obj):
    today = pendulum.today()
    if obj._HANDOVER_TYPE == 'parker':
        table_head = ["股道编号", "使用情况", "股道编号", "使用情况", "股道编号", "使用情况"]
        track_condition = [["", "", "", "", "", ""] for i in range(10)]
        for i in range(len(obj.track_condition)):
            num = (i + 1) * 2 - 1
            x = num // 6
            y = num % 6 - 1
            track_condition[x][y] = obj.track_condition[i].track_id.alias
            track_condition[x][y + 1] = obj.track_condition[i].description
        track_condition.insert(0, table_head)

        data = {
            "year": today.year,
            "month": today.month,
            "day": today.day,
            "template_name": "park_handover_template",
            "handover_type": '白班' if obj.handover_type == 'day' else '夜班',
            "line_execute_time_table": obj.line_execute_time_table.no,
            "track_ids": get_many2many_content(obj.track_ids, "alias"),
            "track_ground_wire": format_context(obj.track_ground_wire),
            "stop_electric_area": get_many2many_content(obj.stop_electric_area, "name"),
            "electric_area_ground_wire": format_context(obj.electric_area_ground_wire),
            "key_info": format_context(obj.key_info),
            "eight_hundred_radio": format_context(obj.eight_hundred_radio),
            "four_hundred_radio": format_context(obj.four_hundred_radio),
            "standby_application_condition": format_context(obj.standby_application_condition),
            "equipment_condition": format_context(obj.equipment_condition),
            "construction_condition": format_context(obj.construction_condition),
            "track_condition": track_condition,
            "plan_carport": plan_carport_get_many2many_content(obj.plan_carport, "train_id"),
            "other_remark": format_context(obj.other_remark),
            "handover_date": obj.handover_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    elif obj._HANDOVER_TYPE == 'checker':
        data = {
            "year": today.year,
            "month": today.month,
            "day": today.day,
            "week": today.day_of_week,
            "template_name": "checker_handover_template",
            "work_time": obj.date_work_start.strftime('%Y-%m-%d %H:%M:%S') + "——" + obj.date_work_end.strftime(
                '%Y-%m-%d %H:%M:%S'),
            "run_train_head": format_list_head(obj.run_train, 7),
            "run_train": format_list(obj.run_train, 7, 3),
            "reserve_train": format_list_head(obj.reserve_train, 7),
            "day_check_train_head": format_list_head(obj.day_check_train, 7),
            "day_check_train": format_list(obj.day_check_train, 7, 4),
            "wash_train": format_list_head(obj.wash_train, 7),
            "reach_top_train": format_list_head(obj.reach_top_train, 7),
            "fault_train": format_list_head(obj.fault_train, 6),
            "not_run_train": format_list_head(obj.not_run_train, 6),
            "special_run_train": format_list_head(obj.special_run_train, 6),
            "maintain_train": [[i.train_id.dev_name, i.work_content, i.work_progress, i.completion_status] for i in
                               obj.maintain_train] + [["", "", "", ""] for i in range(6 - len(obj.maintain_train))],
            "other_train": format_list_head(obj.other_train, 6),
            "instruction_info_first": obj.instruction_info[0].description if obj.instruction_info else "",
            "instruction_info": format_text(obj.instruction_info, 5),
            "safe_info_first": obj.safe_info[0].description if obj.safe_info else "",
            "safe_info": format_text(obj.safe_info, 5),
            "handover_thing_info_first": obj.handover_thing_info[0].description if obj.handover_thing_info else "",
            "handover_thing_info": format_text(obj.handover_thing_info, 17),
            "handover_date": obj.handover_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    elif obj._HANDOVER_TYPE == "signaler":
        table_head = ["股道编号", "使用情况", "股道编号", "使用情况", "股道编号", "使用情况"]
        track_condition = [["", "", "", "", "", ""] for i in range(10)]
        for i in range(len(obj.track_condition)):
            num = (i + 1) * 2 - 1
            x = num // 6
            y = num % 6 - 1
            track_condition[x][y] = obj.track_condition[i].track_id.alias
            track_condition[x][y + 1] = obj.track_condition[i].description
        track_condition.insert(0, table_head)
        data = {
            "year": today.year,
            "month": today.month,
            "day": today.day,
            "template_name": "signaler_handover_template",
            "handover_type": '白班' if obj.handover_type == 'day' else '夜班',
            "line_execute_time_table": obj.line_execute_time_table.no,
            "track_ids": get_many2many_content(obj.track_ids, "alias"),
            "track_ground_wire": format_context(obj.track_ground_wire),
            "stop_electric_area": get_many2many_content(obj.stop_electric_area, "name"),
            "electric_area_ground_wire": format_context(obj.electric_area_ground_wire),
            "eight_hundred_radio": format_context(obj.eight_hundred_radio),
            "four_hundred_radio": format_context(obj.four_hundred_radio),
            "standby_application_condition": format_context(obj.standby_application_condition),
            "equipment_condition": format_context(obj.equipment_condition),
            "clean_condition": format_context(obj.clean_condition),
            "zone_run_train": format_context(obj.zone_run_train),
            "track_condition": track_condition,
            "construction_condition": format_context(obj.construction_condition),
            "plan_carport": plan_carport_get_many2many_content(obj.plan_carport, "train_id"),
            "other_remark": format_context(obj.other_remark),
            "handover_date": obj.handover_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    elif obj._HANDOVER_TYPE == "dispatcher":
        data = {
            "year": today.year,
            "month": today.month,
            "day": today.day,
            "template_name": "dispatcher_handover_template",
            "handover_type": '白班' if obj.handover_type == 'day' else '夜班',
            "line_execute_time_table": obj.line_execute_diagram.no,
            "eight_hundred_radio_total": obj.eight_hundred_radio_total,
            "eight_hundred_radio_give": obj.eight_hundred_radio_give,
            "four_hundred_radio_total": obj.four_hundred_radio_total,
            "four_hundred_radio_give": obj.four_hundred_radio_give,
            "key_total": obj.key_total,
            "key_give": obj.key_give,
            "umbrella_total": obj.umbrella_total,
            "umbrella_give": obj.umbrella_give,
            "other_equipment": format_context(obj.other_equipment),
            "nun_person_plan": format_context(obj.nun_person_plan),
            "sick_leave_num": obj.sick_leave_num,
            "compassionate_leave_num": obj.compassionate_leave_num,
            "annual_leave_num": obj.annual_leave_num,
            "handover_num": obj.handover_num,
            "break_off_num": obj.break_off_num,
            "marriage_leave_num": obj.marriage_leave_num,
            "funeral_leave_num": obj.funeral_leave_num,
            "nursing_leave_num": obj.nursing_leave_num,
            "num_person_learning": obj.num_person_learning,
            "num_other_learning": obj.num_other_learning,
            "handover_other": format_context(obj.handover_other),
            "handover_date": obj.handover_date.strftime('%Y-%m-%d %H:%M:%S')
        }
    return data


class AbstractHandover(models.AbstractModel):
    _name = 'metro_park_production.handover.abstract'
    _log_track = True
    _HANDOVER_TYPE = None

    handover_sign_user = fields.Many2one('res.users', string='交班人', default=lambda self: self.env.user.id)
    handover_date = fields.Datetime('交接班时间', default=fields.Datetime.now)
    department_id = fields.Many2one('funenc.wechat.department', '部门')
    accept_user = fields.Many2one('res.users', '接班人', limit=10)
    state = fields.Selection([('new', '新建'), ('handed', '已交接')], string='状态', default='new', required=True)
    location_id = fields.Many2one("metro_park_base.location",
                                  default=lambda self: self.env.user.cur_location, required=True)

    @api.multi
    def action_ok_handover(self):
        form_id = self.env.ref('metro_park_production.handover_authentication_form').id

        return {
            "name": "交接班认证",
            "type": "ir.actions.act_window",
            "res_model": 'metro_park_production.wizard.authentication',
            "views": [[form_id, 'form']],
            'target': 'new',
            'context': {'dialog_size': 'medium', 'handover_type': self._HANDOVER_TYPE, 'handover_id': self.id}
        }

    @api.multi
    def get_print_template(self):
        data = get_print_data(self)
        return {
            "type": "ir.actions.client",
            "tag": "get_handover_print_templates",
            'target': 'new',
            'context': {"vue_data": data}
        }
