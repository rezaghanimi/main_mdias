
# -*- coding: utf-8 -*-

from odoo import models, api


class InitDepartmentProperty(models.TransientModel):
    '''
    初始化轨道和道岔信息
    '''
    _name = 'metro_park_base_data_10.init_department_property'

    @api.model
    def init_property(self):
        '''
        建立板桥道岔位置关系, 一定要先把道岔和轨道建立了才行
        :return:
        '''
        department_mode = self.env["funenc.wechat.department"]

        # 找到运营二分公司
        top_department = department_mode.search([('name', '=', '运营二分公司')])
        work_shop = department_mode.search([('name', '=', '车辆检修四车间'), ('parent_id', '=', top_department.id)])

        # 找到所有的检修工班
        work_class1 = department_mode.search([('name', '=', '均衡修1班'), ('parent_id', '=', work_shop.id)])
        work_class2 = department_mode.search([('name', '=', '均衡修2班'), ('parent_id', '=', work_shop.id)])
        work_class3 = department_mode.search([('name', '=', '均衡修3班'), ('parent_id', '=', work_shop.id)])
        work_class4 = department_mode.search([('name', '=', '均衡修4班'), ('parent_id', '=', work_shop.id)])
        work_class5 = department_mode.search([('name', '=', '均衡修5班'), ('parent_id', '=', work_shop.id)])

        ban_qiao = self.env.ref("metro_park_base_data_10.ban_qiao").id
        gao_da_lu = self.env.ref("metro_park_base_data_10.gao_da_lu").id

        # 设置工班属性
        property_balance_id = self.env.ref("metro_park_base.department_property_balance_work_class").id
        if work_class1:
            work_class1.properties = [(4, property_balance_id)]
            work_class1.locations = [(4, ban_qiao)]
        if work_class2:
            work_class2.properties = [(4, property_balance_id)]
            work_class2.locations = [(4, ban_qiao)]
        if work_class3:
            work_class3.properties = [(4, property_balance_id)]
            work_class3.locations = [(4, ban_qiao)]
        if work_class4:
            work_class4.properties = [(4, property_balance_id)]
            work_class4.locations = [(4, gao_da_lu)]
        if work_class5:
            work_class5.properties = [(4, property_balance_id)]
            work_class5.locations = [(4, gao_da_lu)]

        # 设置工班长姓名
        if work_class1:
            work_class1.work_master = '钟'
        if work_class2:
            work_class2.work_master = '耀'
        if work_class3:
            work_class3.work_master = '帅'
        if work_class4:
            work_class4.work_master = '国'
        if work_class5:
            work_class5.work_master = '彬'

        # 里程3 里程4 高大路
        # 里程1 里程2 板桥




