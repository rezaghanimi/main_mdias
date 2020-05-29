# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import requests
import json
import datetime
import pendulum
import logging

_logger = logging.getLogger(__name__)


class Tcms(models.Model):
    '''
    tms, tcms 提供车辆相关的信息
    '''
    _name = 'tcms.tcms'

    tids_name = fields.Char(string='TCMS')
    ip = fields.Char(string='IP')

    @api.model
    def get_train_info(self, **kwargs):
        '''
        获取TCMS列车状态信息
        :param kwargs:
        :return:
        '''
        host = self.get_host_info()
        session = self.get_login_session_info()
        train_number = []
        for val in range(1001, 1046):
            train_number.append(val)

        # 列车状态
        login_state = 'http://{host}/txieasyui?taskFramePN=BFBigData&command=GetRealTimeData&colname' \
                      '=json_ajax&colname1=' \
                      '{{%27dataform%27:%27eui_variable_data%27,%27variable%27:%27data%27}}&obj ectName' \
                      '=shanghai&machineIds={train_number}&keys=["'.format(host=host, train_number=train_number)

        # 当日 里程
        high_day_mileage = 'ZT2606'
        low_day_mileage = 'ZT2607'

        # 总里程
        high_all_mileage = 'ZT2431'
        low_all_mileage = 'ZT2432'

        # 压缩机1工作时间
        high_compressor_1 = 'ZT2433'
        low_compressor_1 = 'ZT2434'

        # 压缩机2工作时间
        high_compressor_2 = 'ZT2435'
        low_compressor_2 = 'ZT2436'

        # 牵引能耗
        high_traction_energy_consumption = 'ZT2437'
        low_traction_energy_consumption = 'ZT2438'

        # 辅助能耗
        high_auxiliary_energy_consumption = 'ZT2439'
        low_auxiliary_energy_consumption = 'ZT2440'

        # 再生能耗
        high_regeneration_energy_consumption = 'ZT2441'
        low_regeneration_energy_consumption = 'ZT2442'

        # # 当日里程
        high_day_mileage_text = session.get(login_state + high_day_mileage + '"]', verify=False)
        low_day_mileage_text = session.get(login_state + low_day_mileage + '"]', verify=False)
        day_mileage_value = self.deal_data_info(
            high_day_mileage_text.text,
            low_day_mileage_text.text,
            high_day_mileage,
            low_day_mileage
        )

        # 总里程
        high_all_mileage_text = session.get(login_state + high_all_mileage + '"]', verify=False)
        low_all_mileage_text = session.get(login_state + low_all_mileage + '"]', verify=False)
        all_mileage_value = self.deal_data_info(
            high_all_mileage_text.text,
            low_all_mileage_text.text,
            high_all_mileage,
            low_all_mileage
        )

        # 压缩机1工作时间
        high_compressor_1_text = session.get(login_state + high_compressor_1 + '"]', verify=False)
        low_compressor_1_text = session.get(login_state + low_compressor_1 + '"]', verify=False)
        compressor_1_value = self.deal_data_info(
            high_compressor_1_text.text,
            low_compressor_1_text.text,
            high_compressor_1,
            low_compressor_1)

        # 压缩机2工作时间
        high_compressor_2_text = session.get(login_state + high_compressor_2 + '"]', verify=False)
        low_compressor_2_text = session.get(login_state + low_compressor_2 + '"]', verify=False)
        compressor_2_value = self.deal_data_info(
            high_compressor_2_text.text,
            low_compressor_2_text.text,
            low_compressor_1,
            low_compressor_2
        )

        # 牵引能耗
        high_traction_energy_consumption_text = session.get(login_state + high_traction_energy_consumption + '"]',
                                                            verify=False)
        low_traction_energy_consumption_text = session.get(login_state + low_traction_energy_consumption + '"]',
                                                           verify=False)
        traction_energy_consumption_value = self.deal_data_info(
            high_traction_energy_consumption_text.text,
            low_traction_energy_consumption_text.text,
            high_traction_energy_consumption,
            low_traction_energy_consumption
        )

        # 辅助能耗
        high_auxiliary_energy_consumption_text = session.get(login_state + high_auxiliary_energy_consumption + '"]',
                                                             verify=False)
        low_auxiliary_energy_consumption_text = session.get(login_state + low_auxiliary_energy_consumption + '"]',
                                                            verify=False)
        auxiliary_energy_consumption_value = self.deal_data_info(
            high_auxiliary_energy_consumption_text.text,
            low_auxiliary_energy_consumption_text.text,
            high_auxiliary_energy_consumption,
            low_auxiliary_energy_consumption
        )

        # 再生能耗
        high_regeneration_energy_consumption_text = session.get(
            login_state + high_regeneration_energy_consumption + '"]',
            verify=False
        )
        low_regeneration_energy_consumption_text = session.get(
            login_state + low_regeneration_energy_consumption + '"]',
            verify=False
        )
        regeneration_energy_consumption_value = self.deal_data_info(
            high_regeneration_energy_consumption_text.text,
            low_regeneration_energy_consumption_text.text,
            high_regeneration_energy_consumption,
            low_regeneration_energy_consumption
        )

        # 创建记录
        self.create_data(
            day_mileage_value,
            all_mileage_value,
            traction_energy_consumption_value,
            auxiliary_energy_consumption_value,
            regeneration_energy_consumption_value,
        )

    @api.model
    def get_login_session_info(self):
        '''
        获取session的信息
        :return:
        '''
        host = self.get_host_info()
        # 登录
        login_url = 'http://' + host + '/txieasyui?taskFramePN=AccessCtrl&command=' \
                                       'Login&colname=json_ajax&colname1={%27dataform%27:%27eui_form_data%27}' \
                                       '&loginname=cdapi&loginpass=202cb962ac59075b964b07152d234b70'
        param = {
            'loginname': 'cdapi',
            'loginpass': '202cb962ac59075b964b07152d234b70',
        }

        session = requests.Session()

        session.post(login_url, data=param, verify=False)

        return session

    @api.multi
    def get_host_info(self):
        '''
        获取TCMS 的host 信息
        :return:
        '''
        host = self.search([('tids_name', '=', 'TCMS')])
        if not host:
            raise exceptions.ValidationError("TCMS 登录信息错误!")
        else:
            return host.ip

    @api.multi
    def deal_data_info(self, high, low, high_key, low_key):
        '''
        计算方式 高字节 * 65536 + 低字节
        :param high: 高字节
        :param low: 低字节
        :param high_key: 高字节key
        :param low_key: 低字节key
        :return:
        '''
        data = []
        for val in range(1001, 1046):
            high_val = eval(high).get(str(val))
            low_val = eval(low).get(str(val))
            high_key_val = eval(high_val.get(high_key)) if high_val.get(high_key) else 0
            low_key_val = eval(low_val.get(low_key)) if low_val.get(low_key) else 0
            if high_key_val and low_key_val:
                value = {str(val): high_key_val * 65536 + low_key_val}
            elif not high_key_val and low_key_val:
                value = {str(val): low_key_val}
            elif not low_key_val and high_key_val:
                value = {str(val): high_key_val * 65536}
            else:
                value = {str(val): 0}
            data.append(value)
        return data

    @api.multi
    def create_data(self, *args):
        data = []
        day_mileage_value = args[0]  # 当日里程
        all_mileage_value = args[1]  # 总里程
        traction_energy_consumption_value = args[2]  # 牵引能耗
        auxiliary_energy_consumption_value = args[3]  # 辅助能耗
        regeneration_energy_consumption_value = args[4]  # 再生能耗
        for key, rec in enumerate(range(1001, 1046)):
            data.append({
                'name': '1' + str(rec),
                'today_mileage': day_mileage_value[key].get(str(rec)),
                'total_mileage': all_mileage_value[key].get(str(rec)),
                'traction_consumption': traction_energy_consumption_value[key].get(str(rec)),
                'auxiliary_consumption': auxiliary_energy_consumption_value[key].get(str(rec)),
                'regeneration_consumption': regeneration_energy_consumption_value[key].get(str(rec)),
                'update_time': datetime.datetime.now(),
            })
        self.env['funenc.tcms.vehicle.data'].create(data)
