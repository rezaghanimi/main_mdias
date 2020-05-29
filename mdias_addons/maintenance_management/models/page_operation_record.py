# -*- coding: utf-8 -*-
# @author    magicianliang

from odoo import api, fields, models


class PageOperationRecord(models.Model):
    _name = 'maintenance_management.page_operation_record'
    _description = '维保设备页面操作记录'
    _order = 'create_date desc'

    name = fields.Char(string='操作页面')

    @api.model
    def create_data(self, args):
        '''
        创建页面操作记录
        :param args:
        :return:
        '''

        dic_name = {
            'ATS_s': '板桥ATS备机',
            'ATS_m': '板桥ATS主机',
            'CI_s': '板桥CI备机',
            'CI_m': '板桥CI主机',
            'PSCADA_m': '板桥PSCADA',
            'TCMS_m': '板桥TCMS',
            'PMS_m': '板桥PMS',
            'sg_m': '板桥施工管理',
            'hxjh_m': '板桥核心交换机主机',
            'hxjh_s': '板桥核心交换机备机',
            'jrjh_m': '板桥接入交换机主机',
            'jrjh_s': '板桥接入交换机备机',
            'mdtxqzj_m': '板桥通信前置机主机',
            'mdtxqzj_s': '板桥通信前置机备机',
            'ups_m': '板桥电源',
            'mdyy_m': '板桥应用服务器五',
            'mdyy_s': '板桥应用服务器六',
            'mdsj_m': '数据库服务器一',
            'mdsj_s': '数据库服务器二',
            'mdjl_m': '板桥应用服务器一',
            'mdjl_s': '板桥应用服务器二',
            'mdjl_m_1': '板桥应用服务器三',
            'mdjl_s_1': '板桥应用服务器四',
            'jxdd': '板桥检修部调度工作站',
            'ccjx': '板桥检修工作站',
            'ccdd': '车场调度工作站',
            'xhycz': '板桥信号员操作工作站',
            'zbycz': '板桥值班员操作工作站',
            'whgz_m': '板桥维护工作站',
            'ctqzd': '板桥出退勤终端',
            'pbgzz': '派班工作站',
            'tpy_jrjh_m': '太平园接入交换机主机',
            'tpy_ctqzd': '太平园出退勤终端',
            'tpy_pbgzz': '太平园派班工作站',
            'gdl_ups': '高大路电源',
            'gdl_pscada_m': '高大路PSCADA',
            'gdl_ci_s': '高大路CI备机',
            'gdl_ci_m': '高大路CI主机',
            'gdl_qzj_m': '高大路通信前置机主机',
            'gdl_qzj_s': '高大路通信前置机备机',
            'gdl_jrjh_m': '高大路接入交换机主机',
            'gdl_jrjh_s': '高大路接入交换机备机',
            'gdl_jxdd': '高大路检修调度工作站',
            'gdl_ccjx': '高大路车场检修工作站',
            'gdl_ccdd': '高大路车场调度工作站',
            'gdl_xhycz': '高大路信号员操作工作站',
            'gdl_zbycz': '高大路值班员操作工作站',
            'gdl_ctqzd': '高大路出退勤终端',
            'gdl_pbgzz': '高大路派班工作站',
        }
        self.create([{'name': dic_name.get(args)}])
