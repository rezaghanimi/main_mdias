from odoo import models, fields, api
import xlrd
import base64


class PlanImport(models.Model):
    '''
    导入计划
    '''
    _name = 'metro_park_dispatch.construction_plan_import'

    work_code = fields.Char(string='作业代码')
    work_department = fields.Char(string='作业部门')
    work_datetime = fields.Char(string='作业时间')
    work_area = fields.Text(string='作业区域')
    work_content = fields.Text(string='作业内容')
    work_effect_area = fields.Text(string='影响范围')
    work_power = fields.Char(string='接触网供电安排')
    work_safeguard_procedures = fields.Char(string='防护措施')
    work_cooperate_request = fields.Char(string='配合要求')
    apply_user = fields.Char(string='申请人')
    remark = fields.Text(string='备注')
    work_safe_desc = fields.Text('施工安全预想')

    @api.model
    def import_data_rec(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "metro_park_dispatch.construction_plan_import_file",
            'view_mode': 'form',
            "target": "new",
            "views": [[False, "form"]]
        }


class PlanImportFile(models.TransientModel):
    '''
    导入向导，负责读取文件
    '''
    _name = 'metro_park_dispatch.construction_plan_import_file'

    file = fields.Binary(string='文件')
    file_name = fields.Char('File Name')

    @api.multi
    def construction_plan_import_file(self):
        '''
        导入向导
        :return:
        '''
        one_sheet_content = []
        records = self.file
        data = xlrd.open_workbook(file_contents=base64.decodebytes(records))
        sheet_names = data.sheet_names()
        assert len(sheet_names) > 0
        sheet_name = sheet_names[0]
        sheet_data = data.sheet_by_name(sheet_name)
        rows = sheet_data.nrows
        cols = sheet_data.ncols
        keys = (
            'work_code', 'work_department', 'work_datetime',
            'work_area', 'work_content', 'work_effect_area',
            'work_power', 'work_safeguard_procedures',
            'work_cooperate_request', 'apply_user',
            'remark', 'work_safe_desc'
        )
        for key in range(2, rows):
            row_content = []
            for val in range(cols):
                row_content.append(sheet_data.cell_value(key, val))
                one_dict = dict(zip(keys, row_content))
            one_sheet_content.append(one_dict)
        for create_data in one_sheet_content:
            self.env['metro_park_dispatch.construction_plan_import'].create(create_data)
