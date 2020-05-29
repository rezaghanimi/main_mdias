# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
import logging
_logger = logging.getLogger(__name__)


class MalfunctionRepair(models.Model):
    _name = "funenc.malfunction.repair"
    _description = "故障报修"
    _rec_name = 'name'
    _order = 'id desc'
    _track_log = True

    REPAIRSTATE = [
        ('draft', '草稿'),
        ('submitted', '已提交'),
        ('processing', '处理中'),
        ('completed', '已完成'),
    ]

    code = fields.Char(string="报修编号", default='New', index=True)
    name = fields.Char(string="报修标题", required=True, index=True)
    train_dev_id = fields.Many2one(comodel_name="metro_park_maintenance.train_dev", string="报修设备", required=True, index=True)
    dev_no = fields.Char(string="设备编码", related="train_dev_id.dev_no")
    line_id = fields.Many2one(string="线别", related="train_dev_id.line")
    dev_type = fields.Many2one(string="设备类型", related="train_dev_id.dev_type")
    standard = fields.Many2one(string="型号规格", related="train_dev_id.standard")
    fact_sheet = fields.Text(string="情况说明")
    repair_content = fields.Text(string="报修内容")
    line_ids = fields.One2many(comodel_name="funenc.malfunction.repair.line", inverse_name="repair_id", string="维修列表")

    state = fields.Selection(string="状态", selection=REPAIRSTATE, default='draft', index=True)
    operation_btns = fields.Char(string="操作")

    @api.model
    def get_cur_train_action(self):
        tree_id = self.env.ref('metro_park_maintenance.view_funenc_malfunction_repair_tree').id
        form_id = self.env.ref('metro_park_maintenance.view_funenc_malfunction_repair_form').id
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "funenc.malfunction.repair",
            "name": "故障报修记录",
            "views": [[tree_id, "tree"], [form_id, "form"]]
        }

    @api.model
    def create(self, values):
        """
        创建时写入单据编号以及其他的检查
        :param values:
        :return:
        """
        if not values.get('code') or values.get('code') == 'New':
            values.update({'code': self.env['ir.sequence'].sudo().next_by_code('malfunction.repair.code')})
        return super(MalfunctionRepair, self).create(values)

    @api.model
    def create_repair_form(self):
        form_id = self.env.ref("metro_park_maintenance.view_funenc_malfunction_repair_form").id
        return {
            'name': '创建故障报修单',
            'type': 'ir.actions.act_window',
            'views': [[form_id, 'form']],
            'view_mode': 'form',
            'res_model': 'funenc.malfunction.repair',
            'target': 'new',
        }

    @api.multi
    def submit_malfunction_repair(self):
        """
        提交故障报修单
        :return:
        """
        self.write({'state': 'submitted'})
        raise exceptions.UserError("请使用模拟提交功能！")

    def withdraw_malfunction_repair(self):
        """
        撤回按钮，将单据撤回至草稿状态
        :return:
        """
        self.write({'state': 'draft'})

    def demo_submit_malfunction_repair(self):
        """
        模拟提交按钮
        :return:
        """
        self.write({'state': 'submitted'})

    def demo_malfunction_complete(self):
        """
        模拟完成
        :return:
        """
        self.write({'state': 'completed'})


class MalfunctionRepairLine(models.Model):
    _name = "funenc.malfunction.repair.line"
    _description = "故障报修列表"
    _rec_name = 'device_id'

    LineState = [
        ('0x55', '正常'),
        ('0xAA', '故障'),
    ]
    
    repair_id = fields.Many2one(comodel_name="funenc.malfunction.repair", string="故障报修", ondelete='cascade')
    device_id = fields.Many2one(comodel_name="funenc.alarm.device", string="报警设备", required=True)
    description = fields.Char(string="故障描述")
    state = fields.Selection(string="故障状态", selection=LineState, default='0xAA')

