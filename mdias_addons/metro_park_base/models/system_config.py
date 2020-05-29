# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SystemConfig(models.Model):
    '''
    系统配置，使用一个单表来替带配置，系统的那个配置模块不好用
    '''
    _name = 'metro_park_base.system_config'
    _description = '系统配置'
    _track_log = True

    name = fields.Char(string='显示名称', default='系统配置', help='只是为了显示用')

    auto_pull_dispatch_data = \
        fields.Boolean(string='自动拉取施工调度数据', default=False)

    base_url = fields.Char(string="基础地址",
                           default="http://127.0.0.1:8069")
    tcms_address = fields.Char(string="TCMS地址",
                               deault="http://119.6.107.149:8788/RMD/Common/jsp/index/index.jsp")

    calc_host = fields.Char(string="计算服务器地址")

    driver_plan_host = fields.Char(string="司机排班地址")

    ats_server_host = fields.Char(string="ats服务器地址", default="127.0.0.1")

    gao_da_lu_interlock_host = fields.Char(string="高大路联锁服务器地址")

    ban_qiao_interlock_host = fields.Char(string="板桥联锁服务器地址")

    out_train_pre_min = fields.Integer(
        string="发车提醒时间", default=5, help="发车提前分钟数")
    back_train_need_min = fields.Integer(
        string="接车提醒时间", default=5, help="发车提前分钟数")

    construction_api_host = fields.Char(string='施工调度数据请求接口地址')
    construction_app_id = fields.Char(string='施工调度接口应用ID')
    construction_app_key = fields.Char(string='施工调度接口应用KEY')
    # pms接口IP信息
    pms_ip = fields.Char(string='PMS接口IP信息')
    # 是否启用PMS
    start_pms = fields.Selection([('yes', '是'), ('no', '否')], string='是否启用PMS', default='no', required=True)

    @api.model
    def set_auto_pull_construction_data(self, auto):
        '''
        设置自动同步
        :param auto:
        :return:
        '''
        records = self.env['metro_park_base.system_config'].search([])
        if len(records) == 0:
            self.create([{'auto_pull_dispatch_data': auto}])
        else:
            record = records[0]
            record.auto_pull_dispatch_data = auto
        return False

    @api.multi
    def write(self, vals):
        res = super(SystemConfig, self).write(vals)
        self._init_config()
        return res

    _CONFIG = None

    def _init_config(self):
        records = self.env['metro_park_base.system_config'].search_read([])
        if len(records) == 0:
            self.create([{'auto_pull_dispatch_data': False}])
            records = self.env['metro_park_base.system_config'].search_read([])
        self._CONFIG = records[0]

    @api.model
    def get_configs(self):
        '''
        取得配置
        :return:
        '''
        if not self._CONFIG:
            self._init_config()
        return self._CONFIG

    @api.model
    def jump_form_edit(self):
        '''
        直接跳转 form视图
        :return:
        '''
        res_id = None
        records = self.search([])
        if len(records) > 0:
            res_id = records[0].id
        action = self.env.ref(
            'metro_park_base.system_config_act_window').read()[0]
        action['res_id'] = res_id
        action['context'] = {'form_view_initial_mode': 'edit'}
        action['target'] = "new"
        return action
