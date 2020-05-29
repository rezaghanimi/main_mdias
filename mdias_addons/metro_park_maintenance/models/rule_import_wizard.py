
# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import base64
import xlrd


class RuleImportWizard(models.TransientModel):
    '''
    规则导入向导
    '''
    _name = 'metro_park_maintenance.rule_import_wizard'
    _description = '修程导入向导'
    
    excel_file = fields.Binary(string='excel_file')

    @api.model
    def get_rule_import_action(self):
        '''
        规则导入向导动作
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_maintenance.rule_import_wizard",
            'view_mode': 'form',
            "views": [[self.env.ref(
                'metro_park_maintenance.rule_import_wizard_form').id, "form"]]
        }

    @api.model
    def on_ok(self):
        '''
        确定按扭点击
        :return:
        '''

        # 获取execl中数据
        bin_data = base64.b64decode(self.excel_file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        tmp_sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
        all_data = []
        for row in range(0, tmp_sheet.nrows):
            all_data.append(tmp_sheet.row_values(row))

        train_type_ar = []
        location_ar = []
        rail_type_ar = []

        for data, index in enumerate(all_data):
            train_type = data[5]
            rail_type_str = data[13]
            rail_types = rail_type_str.split(',')
            location_str = data[12]
            locations = location_str.split(',')

            train_type_ar.append(train_type)
            location_ar += locations
            rail_type_ar += rail_types

        dev_standard_model = self.env['metro_park_base.dev_standard']
        location_model = self.env['metro_park_base.location']
        rail_type_model = self.env['metro_park_base.rail_type']

        train_types = dev_standard_model.search([('name', 'in', location_ar)])
        locations = location_model.search([('name', 'in', location_ar)])
        rail_types = rail_type_model.search([('name', 'in', rail_type_ar)])

        train_types_cache = {train_type['name']: train_type['id'] for train_type in train_types}
        locations_cache = {location['name']: location['id'] for location in locations}
        rail_types_cache = {rail_type['name']: rail_type['id'] for rail_type in rail_types}

        vals = []
        for data, index in enumerate(all_data):
            val = {}
            name = data[0]
            val['name'] = name
            code = data[1]
            val['code'] = code
            period = data[2]
            val['period'] = period
            offset = data[3]
            val['offset'] = offset
            priority = data[4]
            val['priority'] = priority

            train_type = data[5]
            train_type = train_types_cache[train_type]
            val['train_type'] = train_type

            target_plan_type = data[6]
            val['target_plan_type'] = target_plan_type

            work_start_time = data[7]
            val['work_start_time'] = work_start_time

            work_end_time = data[8]
            val['work_end_time'] = work_end_time

            repair_days = data[9]
            val['repair_days'] = repair_days

            miles = data[10]
            val['miles'] = miles

            positive_offset_miles = data[11]
            val['positive_offset_miles'] = positive_offset_miles

            locations = data[12]
            locations = locations.split(',')
            location_ids = []
            for location in locations:
                if location not in locations_cache:
                    raise exceptions.ValidationError(
                        '位置{location}不存在, 行数{index}'.format(
                            location=location, index=index+2))
                location_ids.append(locations_cache[location])
            val['locations'] = (6, 0, location_ids)

            request_location_types = data[13]
            rail_types = request_location_types.split(',')
            rail_type_ids = []
            for rail_type in rail_types:
                if rail_type not in rail_types_cache:
                    raise exceptions.ValidationError(
                        '轨道类型不存在{rail_type}'.format(rail_type=rail_type))
                rail_type_ids.append(rail_types_cache[rail_type])
            val['rail_types'] = (6, 0, rail_type_ids)

            detain_train = data[14]
            val['detain_train'] = detain_train

            vals.append(val)

        # 导入规程
        self.env['metro_park_maintenance.repair_rule'].create(vals)








