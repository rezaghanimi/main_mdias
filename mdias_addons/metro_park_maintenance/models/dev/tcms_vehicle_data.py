# -*- coding: utf-8 -*-
from odoo import models, fields, api
import hashlib
import aiohttp
import asyncio
import json
import logging

_logger = logging.getLogger(__name__)

DEV_CACHES = {}


class FunencTcmsVehicleData(models.Model):
    _name = "funenc.tcms.vehicle.data"
    _description = "车辆同步历史"
    _rec_name = 'train_dev_id'
    _order = 'date desc'
    _track_log = True

    name = fields.Char(string="车辆号", required=True)
    today_mileage = fields.Char(string="当日里程")
    total_mileage = fields.Char(string="公里数")
    traction_consumption = fields.Char(string="牵引能耗")
    auxiliary_consumption = fields.Char(string="辅助能耗")
    regeneration_consumption = fields.Char(string="再生能耗")
    # update_time = fields.Datetime(string="更新时间")
    date = fields.Date(string="日期", compute='_compute_date', store=True)
    train_dev_id = fields.Many2one(comodel_name="metro_park_maintenance.train_dev", string="关联设备",
                                   compute='_compute_train_dev', store=True)

    @api.model
    def get_cur_train_action(self):
        tree_id = self.env.ref('metro_park_maintenance.view_funenc_tcms_vehicle_data_tree').id
        form_id = self.env.ref('metro_park_maintenance.view_funenc_tcms_vehicle_data_form').id
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "funenc.tcms.vehicle.data",
            "name": "TCMS车辆数据",
            "views": [[tree_id, "tree"], [form_id, "form"]]
        }

    @api.model
    @api.depends('write_date')
    def _compute_date(self):
        """
        根据更新时间得到日期
        :return:
        """
        for res in self:
            res.date = str(res.write_date)[:10]

    def _get_dev_id_by_database(self, name):
        dev_id = self.env['metro_park_maintenance.train_dev'].search([('dev_no', '=', name)], limit=1).id
        DEV_CACHES[name] = dev_id
        return dev_id

    @api.depends('name')
    def _compute_train_dev(self):
        """
        根据车辆号自动查找设备：与设备管理中查找编号为记录车辆号的设备进行关联
        :return:
        """
        for res in self:
            if res.name in DEV_CACHES and not DEV_CACHES[res.name]:
                res.train_dev_id = DEV_CACHES[res.name]
            else:
                res.train_dev_id = self._get_dev_id_by_database(res.name)

    @api.model
    def get_miles_by_date(self, date):
        '''
        取得日期公里数
        :return:
        '''
        sql = "SELECT DISTINCT on (name) name, id, total_mileage, date FROM funenc_tcms_vehicle_data where date < '" + date + \
              "' order by name asc, date desc"
        self.env.cr.execute(sql)
        ids = [x[1] for x in self.env.cr.fetchall()]
        records = self.browse(ids)
        rst = {}
        for record in records:
            rst[record.name] = record.total_mileage
        return rst

    @api.model
    def start_pull_vehicle_data(self):
        """
        从网址中爬取车辆数据
        :return:
        """
        # 获取tcms配置参数,并判断使用哪种工具进行同步
        config = self.env['metro_park_base.system_config'].search([], limit=1)
        if config and config.tcms_synchronize_tool == 'api':
            return self.env['tcms.tcms'].get_train_info(sync_miles=True)
        _logger.info(">>>Start pull tcms vehicle data...")
        # 获取现车车辆列表并封装为车号数组
        cur_train_manages = self.env['metro_park_dispatch.cur_train_manage'].search([])
        vehicles = list()
        for cur_train_manage in cur_train_manages:
            try:
                # 如果车号为5位数，比如11001，则需要截取后4位
                if len(cur_train_manage.train_name) == 5:
                    # 测试将车号转为float类型，如果车辆不为1001-1045的车辆，则跳过，保证过滤掉G1000这样的车
                    float(cur_train_manage.train_name)
                    # 由于tcms网站中只需要4位车号，需要截取现车车号后4位
                    vehicles.append(cur_train_manage.train_name[1:])
            except Exception as error:
                _logger.info('get train no error, {error}'.format(error=error))
        if len(vehicles) < 1:
            _logger.info(">>>现车管理中不存在需要更新的车辆信息.")
            return
        # 获取tcms配置参数
        config = self.env['metro_park_base.system_config'].search([], limit=1)
        if not config:
            _logger.info(">>>未配置TCMS系统参数，更新请求已关闭！")
            return False
        # 兼容处理，asyncio.run是python3.7的新特征，不支持py3.6以下，所以加上一个异常处理
        try:
            # python3.7
            asyncio.run(self.tcms_login(config, vehicles))
        except Exception as error:
            _logger.info(">>> python3.7 run asyncio.run error: {}".format(error))
            # python 3.6
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(loop.create_task(self.tcms_login(config, vehicles)))
                loop.close()
            except Exception as e:
                _logger.info(">>> python3.6 run asyncio.new_event_loop error: {}".format(e))
        _logger.info(">>>Stop pull tcms vehicle data...")
        return {'type': 'ir.actions.act_window_close'}

    async def tcms_login(self, config, vehicles):
        """
        使用aiohttp登陆
        :param config 系统配置文件
        :param vehicles 车辆列表
        :return:
        """
        jar = aiohttp.CookieJar(unsafe=True)
        async with aiohttp.ClientSession(cookie_jar=jar) as session:
            if not config.tcms_url or not config.tcms_username or not config.tcms_password:
                _logger.info(">>> TCMS基础信息错误，url地址、登陆名称以及登陆密码不正确！")
                return
            tcms_url = config.tcms_url
            login_url = '{}/txieasyui'.format(tcms_url)  # 登陆url
            username = config.tcms_username
            md = hashlib.md5()
            # 对密码进行md5加密
            md.update(config.tcms_password.encode())
            password = md.hexdigest()
            params = {
                'taskFramePN': 'AccessCtrl',
                'command': 'Login',
                'colname': 'json',
                'colname1': "{'dataform': 'eui_form_data'}",
                'loginname': username,  # 用户名
                'loginpass': password,  # md5加密后的str
            }
            async with session.get(login_url, params=params, timeout=5) as resp:
                _logger.info(resp)
                await self.read_date(tcms_url, session, vehicles)

    async def read_date(self, tcms_url, session, vehicles):
        read_url = tcms_url + "/txieasyui?taskFramePN=VehicleRela&command=getVehicleRealData&colname=json_ajax&colname1={'dataform':'eui_variable_data','variable':'getVehicleRealData'}"
        # keys表示要获取对应的车辆信息keys，
        keys = ["XN213", "XN214", "XN215", "XN216", "XN217", "XN179", "XN180", "XN185", "XN186", "XN187"]
        datas = {
            'objectName': 'shanghai',
            'machineIds': str(vehicles),
            'keys': str(keys),
        }
        async with session.post(read_url, data=datas, timeout=5) as resp:
            result = await resp.text()
            info_json = json.loads(result)
            _logger.info(info_json)
            try:
                vehicle_data = info_json['vehicleData']
                bigdata = info_json['bigdata']
                for vehicle in vehicles:
                    chat1 = ['1001', '1002', '1003', '1004', '1005', '1006']
                    line = bigdata.get(vehicle)
                    line_data = {
                        'miles': line.get('XN214') if vehicle in chat1 else line.get('XN180'),  # 总里程
                        'traction_energy': line.get('XN215') if vehicle in chat1 else line.get('XN185'),  # 牵引能耗
                        'auxiliary_energy': line.get('XN216') if vehicle in chat1 else line.get('XN186'),  # 辅助能耗
                        'renewable_energy': line.get('XN217') if vehicle in chat1 else line.get('XN187'),  # 再生能耗
                        # 'write_date': fields.datetime.now(),
                    }
                    # 往车辆运行公里数中修改数据
                    domain = [('dev_name', '=', "1{}".format(vehicle))]
                    res_vehicles = self.env['metro_park_maintenance.train_dev'].search(domain)
                    if res_vehicles:
                        res_vehicles.write(line_data)

                    # ---历史公里记录表同时也保存一份----
                    # now_time = fields.datetime.now()
                    today = fields.date.today()
                    new_vehicle = "1%s" % vehicle
                    vehicle_data = {
                        'name': new_vehicle,  # 车辆号
                        'today_mileage': line.get('XN213') if vehicle in chat1 else line.get('XN179'),  # 当日里程
                        'total_mileage': line.get('XN214') if vehicle in chat1 else line.get('XN180'),  # 总里程
                        'traction_consumption': line.get('XN215') if vehicle in chat1 else line.get('XN185'),  # 牵引能耗
                        'auxiliary_consumption': line.get('XN216') if vehicle in chat1 else line.get('XN186'),  # 辅助能耗
                        'regeneration_consumption': line.get('XN217') if vehicle in chat1 else line.get('XN187'),# 再生能耗
                        # 'update_time': now_time,
                    }
                    res_vehicles = self.search([('name', '=', new_vehicle), ('date', '=', today)])
                    if res_vehicles:
                        res_vehicles.write(vehicle_data)
                    else:
                        line = list()
                        line.append(vehicle_data)
                        self.create(line)
            except Exception as e:
                _logger.info(str(e))

    @api.model
    def export_data_rec(self):
        return {
            'name': '车辆历史公里数信息导出',
            'type': 'ir.actions.act_url',
            'url': '/funenc_tcms_vehicle_data_export'
        }

    @api.model
    def add_miles_button(self):
        """
        车辆公里数录入
        :return:
        """
        return {
            "type": "ir.actions.act_window",
            "res_model": 'maintenance.vehicle.history.add',
            "views": [[False, "form"]],
            "target": "new",
            'name': "车辆公里数录入",
            "context": {'form_view_initial_mode': 'edit'},
        }

    @api.model
    def batch_deletion_data(self):
        """
        按照选择的时间段批量删除车辆历史公里数记录
        :return:
        """
        return {
            "type": "ir.actions.act_window",
            "res_model": 'maintenance.vehicle.history.delete',
            "views": [[False, "form"]],
            "target": "new",
            'name': "批量删除",
            "context": {'form_view_initial_mode': 'edit'},
        }
