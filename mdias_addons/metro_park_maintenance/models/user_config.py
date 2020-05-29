# -*- coding: utf-8 -*-
from odoo import models, fields, api


# 集成原系统配置表单，增加tcms系统基本参数，用于获取tcms站点中的车辆数据
class FunencTcmsData(models.Model):
    _inherit = "metro_park_base.system_config"

    tcms_url = fields.Char(string="TCMS URL", default='http://119.6.107.149:8788')
    tcms_username = fields.Char(string='登陆用户账号')
    tcms_password = fields.Char(string='登陆用户密码')
    tcms_synchronize_tool = fields.Selection(string="同步工具", selection=[('api', 'API接口'), ('web', '网页抓取')], default='api')

