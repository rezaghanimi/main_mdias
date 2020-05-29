
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepartmentExtend(models.Model):
    '''
    部门属性扩展, 添加维护的设备
    '''
    _inherit = 'funenc.wechat.department'
    
    devs = fields.Many2many(string="车辆设备",
                            comodel_name='metro_park_maintenance.train_dev',
                            inverse_name='maintenance_department',
                            help="管理的车辆设备")

    locations = fields.Many2many(string="归属场段",
                                 comodel_name="metro_park_base.location")

    department_code = fields.Char(string='部门编码')
    work_master = fields.Char(string="工班长姓氏", help='月计划需要安排')

    @api.model
    def get_work_class_count(self):
        '''
        取得工班数量
        :return:
        '''
        # 取得有均衡修工班属性的工班
        department_property_work_class = \
            self.env.ref("metro_park_base.department_property_balance_work_class").id
        work_classes = self.env["funenc.wechat.department"].search(
            [("properties", "in", [department_property_work_class])])
        work_class_count = len(work_classes)
        return work_class_count

    @api.model
    def get_work_class_domain(self):
        '''
        取得工班的domain
        :return:
        '''
        department_property_work_class = \
            self.env.ref("metro_park_base.department_property_balance_work_class").id
        return [("properties", "in", [department_property_work_class])]