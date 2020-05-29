# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
import pendulum
import datetime
import base64
import xlrd
from . import utility


def format_time(sheet, row, col):
    return sheet.cell_value(row, col).split(":") \
        if sheet.cell_type(row, col) == 1 else \
        [i for i in xlrd.xldate_as_tuple(sheet.cell_value(row, col), 0) if i != 0]


class ImportRunPlanWizard(models.TransientModel):
    '''
    运行计划导入向导
    '''
    _name = 'metro_park_dispatch.import_run_plan_wizard'

    date = fields.Date(string="日期", default=lambda self: fields.date.today())
    type = fields.Selection(string='类型',
                            selection=[('run_plan', '运行图'),
                                       ('custom', '自行编制')],
                            default="run_plan",
                            required=True)
    time_table_id = fields.Many2one(comodel_name="metro_park_base.time_table",
                                    string="当日运行图",
                                    help="根据当日的时刻表生成收车计划")
    next_day_time_table_id = fields.Many2one(comodel_name="metro_park_base.time_table",
                                             string="次日运行图",
                                             help="根据次日的生成发车计划")
    file = fields.Binary(string='文件')
    remark = fields.Text(string='备注')

    @api.multi
    def on_ok_btn_clicked(self):
        '''
        点击确认按扭
        :return:
        '''
        if self.type == "run_plan":
            self.import_from_time_table()
        else:
            self.import_from_excel()

    @api.multi
    def import_from_time_table(self):
        '''
        根据选择的运行图生成收发车计划, 这里只取当前的轨道,
        收车计划是根据当日运行图的表生成，发车计划是根据第二日的运行图生成
        :return:
        '''
        park_type_id = self.env.ref("metro_park_base.location_type_park").id

        # 生成收车计划
        time_table = self.time_table_id
        time_table_datas = time_table.time_table_data
        for data in time_table_datas:
            back_location = data.back_location
            receive_train_need_min = back_location.receive_train_need_min

            # 添加收车计划, 具体哪个车用户自己去添加
            if back_location.location_type.id == park_type_id:
                back_time = utility.time_str_to_int(str(data['plan_in_time']))
                tmp_model = self.env['metro_park_dispatch.train_back_plan']
                tmp_model.create({
                    'plan_back_time': back_time,
                    'exchange_rail_time': back_time + receive_train_need_min * 60,
                    'plan_train_no': data['train_no'],
                    'plan_back_location': back_location.id,
                    'state': 'unpublish',
                    'date': self.date
                })

        # 生成发车计划
        next_day_time_table = self.next_day_time_table_id
        next_day_time_table_data = next_day_time_table.time_table_data

        # 添加发车计划，具体哪个车用户自己去添加
        next_day = pendulum.parse(str(self.date)).add(days=1)
        for data in next_day_time_table_data:
            out_location = data.out_location
            send_train_pre_min = out_location.send_train_pre_min
            if out_location.location_type.id == park_type_id:
                tmp_model = self.env['metro_park_dispatch.train_out_plan']
                plan_out_time = utility.time_str_to_int(str(data["plan_out_time"]))
                tmp_model.create({
                    'plan_out_time': plan_out_time - send_train_pre_min * 60,    # 这个里间是出库时间，并不等于排计划的时间
                    'exchange_rail_time': plan_out_time,
                    'plan_train_no': data['train_no'],
                    'plan_out_location': out_location.id,
                    'state': 'unpublish',
                    'date': next_day.format('YYYY-MM-DD')
                })

    @api.multi
    def import_from_excel(self):
        """
        根据上传的excel生成收发车计划
        :return:
        """
        datas = self.read_excel()
        if datas['date'] != self.date:
            raise ValidationError("文件内日期与所选择日期不符")
        train_dev = self.env['metro_park_maintenance.train_dev']
        cur_train = self.env['metro_park_dispatch.cur_train_manage']
        rails_sec = self.env['metro_park_base.rails_sec']
        val1 = []
        val2 = []
        for i in datas['data']:
            plan_out_rail = rails_sec.search([('no', 'like', "%" + i['plan_out_rail'] + "%"),
                                              ('location', '=', i['location'])])
            train_id = train_dev.search([('dev_name', '=', i['dev_name'])]).id
            if not plan_out_rail:
                raise ValidationError("不存在股道%s，请先配置" % i['plan_out_rail'])
            val1.append({
                'status': 'wait_accept',
                'date': datas['date'],
                'train_id': cur_train.search([('train', '=', train_id)]).id,
                'plan_train_no': i['plan_train_no'],
                'plan_out_rail': plan_out_rail.id,
                'plan_out_time': datetime.datetime(1987, 1, 1, int(i['plan_out_time'][0]), int(i['plan_out_time'][1]),
                                                   int(i['plan_out_time'][2])),
                'exchange_rail_time': datetime.datetime(1987, 1, 1, int(i['exchange_rail_time'][0]),
                                                        int(i['exchange_rail_time'][1]),
                                                        int(i['exchange_rail_time'][2])),
                'plan_out_location': plan_out_rail.location.id,
                'remark': 'excel导入',
                'plan_out_end_rail': self.env['metro_park_base.rails_sec'].search([('no', '=', "T1701G")]).id
            })

            val2.append({
                'status': 'wait_accept',
                'date': datas['date'],
                'train_id': cur_train.search([('train', '=', train_id)]).id,
                'plan_train_no': i['plan_train_no'],
                'plan_back_time': datetime.datetime(1987, 1, 1, int(i['plan_back_time'][0]),
                                                    int(i['plan_back_time'][1]), int(i['plan_back_time'][2])),
                'plan_back_location': i['plan_back_location'],
                'plan_back_rail': plan_out_rail.id,
                'wash': True if i['wash'] else False,
                "dispatch": False,
                'repair_plan': "",
            })
        self.env['metro_park_dispatch.train_out_plan'].create(val1)
        self.env['metro_park_dispatch.train_back_plan'].create(val2)

    def read_excel(self):
        '''
        从 excel 中读取数据
        :return:
        '''
        # 获取execl中数据
        bin_data = base64.b64decode(self.file)
        workbook = xlrd.open_workbook(file_contents=bin_data)
        # 根据sheet索引或者名称获取sheet内容
        # 这里不知道为什么出现bug，不管怎么调整索引都必须为1才能获取到sheet，保险起见换成name
        sheet = workbook.sheet_by_name('Sheet1')
        date = xlrd.xldate_as_tuple(sheet.cell_value(1, 0), 0)
        date = datetime.date(date[0], date[1], date[2])
        all_data = []
        banqiao = self.env['metro_park_base.location'].search([('name', 'like', "%板桥%")]).id
        gaodalu = self.env['metro_park_base.location'].search([('name', 'like', "%高大路%")]).id
        location = banqiao
        for row in range(4, sheet.nrows):
            if sheet.cell_value(row, 5) and (sheet.cell_value(row, 5) != "列车整备时间"):
                if sheet.cell_value(row, 9):
                    plan_back_time = format_time(sheet, row, 9)
                    plan_back_location = banqiao
                else:
                    plan_back_time = format_time(sheet, row, 10)
                    plan_back_location = gaodalu
                all_data.append({
                    'plan_train_no': int(sheet.cell_value(row, 1)),
                    'dev_name': int(sheet.cell_value(row, 2)),
                    'plan_out_rail': str(sheet.cell_value(row, 3)).split(".")[0],
                    'plan_out_time': format_time(sheet, row, 7),
                    'exchange_rail_time': format_time(sheet, row, 8),
                    'plan_back_time': plan_back_time,
                    "plan_back_location": plan_back_location,
                    'wash': sheet.cell_value(row, 11),
                    'repair_plan': sheet.cell_value(row, 12),
                    'location': location
                })
            else:
                location = gaodalu
        return {
            'date': date,
            'data': all_data
        }
