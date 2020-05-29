# -*- coding: utf-8 -*-
from odoo import models, api


class EarlyWaringInfo(models.AbstractModel):
    TYPE_TRAIN_MAINTAIN = 'train_maintain'
    TYPE_TRAIN_RUN_START = 'train_run_start'
    TYPE_TRAIN_RUN_FINISHED = 'train_run_finished'
    TYPE_CONSTRUCTION = 'construction'

    DATA_MAP_FOR_TYPE = {
        TYPE_TRAIN_MAINTAIN: ('车辆检修计划', '完成率'),
        TYPE_TRAIN_RUN_START: ('发车计划', '准点率'),
        TYPE_TRAIN_RUN_FINISHED: ('收车计划', '准点率'),
        TYPE_CONSTRUCTION: ('施工', '完成率')
    }

    _name = 'metro_park_production.early_waring_info'

    BASE_DOMAIN = [('state', 'in', ['published', 'finished'])]

    @classmethod
    def check_finished(cls, record):
        if record.state == 'finished':
            return True
        else:
            return False

    @classmethod
    def _group_by(cls, values, key):
        result = {}
        if isinstance(key, (str,)):
            key = lambda v: getattr(v, key)
        for value in values:
            k = key(value)
            result.setdefault(k, [])
            result[k].append(value)
        return result

    @property
    def task_obj(self):
        return self.env['metro_park_maintenance.rule_info']

    def get_train(self, offset, limit):
        trains = self.env['metro_park_maintenance.train_dev'].search([], offset=offset, limit=limit, order='id')
        return trains

    def make_train_task_info(self, type_name, domain, date_start, date_end, offset, limit):
        # 查询当前类型下面的颜色和值
        one, two, three = self.get_color_change_status(type_name)
        trains = self.get_train(offset, limit)
        domain = domain + [('date', '>=', date_start),
                           ('date', '<=', date_end), ('dev', 'in', trains.ids)] + self.BASE_DOMAIN

        records = self.task_obj.search(domain)

        train_result = []
        exit_train_no = []
        values = self._group_by(records, key=lambda record: record.dev_no)
        for dev_no, tasks in values.items():
            finished_num = 0
            exit_train_no.append(dev_no)
            for task in tasks:
                if self.check_finished(task):
                    finished_num += 1
            if finished_num == 0:
                finished_num = 1
            proportion = finished_num / len(tasks) * 100
            if proportion < one.get('single_threshold_value_percentage'):
                single_customColor = one.get('single_color')
            elif two.get('single_threshold_value_percentage') > proportion >= one.get(
                    'single_threshold_value_percentage'):
                single_customColor = two.get('single_color')
            elif two.get('single_threshold_value_percentage') <= proportion < three.get(
                    'single_threshold_value_percentage'):
                single_customColor = three.get('single_color')
            else:
                single_customColor = "#409eff"

            train_result.append({
                'train_name': dev_no,
                'finished_num': finished_num,
                'total_num': len(tasks),
                'single_customColor': single_customColor,
            })
        all_train_no = trains.mapped('dev_no')
        single_customColor = "#409eff"
        for dev_no in set(all_train_no) - set(exit_train_no):
            train_result.append({
                'train_name': dev_no,
                'finished_num': 0,
                'total_num': 0,
                'single_customColor': single_customColor,
            })
        return train_result

    def make_train_maintain_info(self, *args, **kwargs):
        domain = [('rule_type', '=', 'normal')]
        return self.make_train_task_info('车辆检修', domain, *args, **kwargs)

    def make_train_start_info(self, *args, **kwargs):
        domain = [('rule_type', '=', 'send_train')]
        return self.make_train_task_info('发车任务', domain, *args, **kwargs)

    def make_train_finished_info(self, *args, **kwargs):
        domain = [('rule_type', '=', 'recieve_train')]
        return self.make_train_task_info('收车任务', domain, *args, **kwargs)

    def make_construction_info(self, date_start, date_end, offset, limit):
        return False

    @api.model
    def request_early_waring_task_info(self, data_type, date_start, date_end, offset=0, limit=5):
        """
            :param data_type: 请求数据类型：检车检修, 发车计划, 检修计划
            :param date_start: 开始时间
            :param date_end: 结束时间
            :param offset: 偏移，分页处理
        """
        if data_type == self.TYPE_TRAIN_MAINTAIN:
            return self.make_train_maintain_info(date_start, date_end, offset, limit)
        elif data_type == self.TYPE_TRAIN_RUN_START:
            return self.make_train_start_info(date_start, date_end, offset, limit)
        elif data_type == self.TYPE_TRAIN_RUN_FINISHED:
            return self.make_train_finished_info(date_start, date_end, offset, limit)
        elif data_type == self.TYPE_CONSTRUCTION:
            return self.make_construction_info(date_start, date_end, offset, limit)
        else:
            return False

    @api.model
    def get_overall_info(self, data_type, date_start, date_end):
        config_data = {
            'train_maintain': '车辆检修',
            'train_run_start': '发车任务',
            'train_run_finished': '收车任务',
            'construction': '施工任务',
        }
        sum_num = 0
        finished_num = 0
        view_id = None
        model = None
        action_domain = []
        if data_type in [self.TYPE_TRAIN_MAINTAIN, self.TYPE_TRAIN_RUN_START, self.TYPE_TRAIN_RUN_FINISHED]:
            view_id = 'metro_park_maintenance.rule_info_list'
            model = 'metro_park_maintenance.rule_info'
            if data_type == self.TYPE_TRAIN_MAINTAIN:
                domain = [('rule_type', '=', 'normal')]

            elif data_type == self.TYPE_TRAIN_RUN_START:
                domain = [('rule_type', '=', 'send_train')]
            elif data_type == self.TYPE_TRAIN_RUN_FINISHED:
                domain = [('rule_type', '=', 'recieve_train')]
            else:
                return False
            action_domain = domain
            domain = domain + self.BASE_DOMAIN + [('date', '>=', date_start),
                                                  ('date', '<=', date_end)]
            records = self.task_obj.search(domain)
            sum_num = len(records)
            for record in records:
                if self.check_finished(record):
                    finished_num += 1
        elif data_type == self.TYPE_CONSTRUCTION:
            pass
        else:
            return
        one, two, three = self.get_color_change_status(config_data.get(data_type))
        if sum_num == 0:
            proportion = 0
        else:
            proportion = finished_num / sum_num * 100
        if proportion < one.get('single_threshold_value_percentage'):
            all_customColor = one.get('all_color')
        elif two.get('single_threshold_value_percentage') > proportion >= one.get(
                'single_threshold_value_percentage'):
            all_customColor = two.get('all_color')
        elif two.get('single_threshold_value_percentage') <= proportion < three.get(
                'single_threshold_value_percentage'):
            all_customColor = three.get('all_color')
        else:
            all_customColor = "#409eff"
        page_count = len(self.env['metro_park_maintenance.train_dev'].search([]))
        result = {
            'train_info': self.DATA_MAP_FOR_TYPE[data_type],
            'sum_num': sum_num,
            'finished_num': finished_num,
            'action_domain': action_domain,
            'model': model,
            'all_customColor': all_customColor,
            'page_count': page_count,
        }
        if view_id:
            result.update({
                'view_id': self.env.ref(view_id)
            })
        return result

    @api.multi
    def get_color_change_status(self, type_name):
        local_datas = self.env['metro_park_production.early_waring'].search([('name', '=', type_name)])
        for local_data in local_datas.settings:
            if local_data.waring_line_name == '一级预警':
                one = {
                    "waring_line_name": local_data.waring_line_name,
                    "single_threshold_value_percentage": local_data.single_threshold_value_percentage,
                    "all_threshold_value_percentage": local_data.all_threshold_value_percentage,
                    "all_color": local_data.all_color,
                    "single_color": local_data.single_color,
                }
            elif local_data.waring_line_name == '二级预警':
                two = {
                    "waring_line_name": local_data.waring_line_name,
                    "single_threshold_value_percentage": local_data.single_threshold_value_percentage,
                    "all_threshold_value_percentage": local_data.all_threshold_value_percentage,
                    "all_color": local_data.all_color,
                    "single_color": local_data.single_color,
                }
            else:
                three = {
                    "waring_line_name": local_data.waring_line_name,
                    "single_threshold_value_percentage": local_data.single_threshold_value_percentage,
                    "all_threshold_value_percentage": local_data.all_threshold_value_percentage,
                    "all_color": local_data.all_color,
                    "single_color": local_data.single_color,
                }
        return [one, two, three]
