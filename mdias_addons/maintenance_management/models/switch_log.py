# -*- coding:utf-8 -*-

from odoo import api, models, fields
import requests
import random
import string
import datetime
import re
import logging
import time

_logger = logging.getLogger(__name__)

LOGIN_URL = "login.cgi"
CONFIG_URL = "config.cgi"


class SwitchLog(models.Model):
    _name = 'maintenance_management.switch_log'

    _description = '交换机日志'
    _track_log = True

    log_time = fields.Char(string='日志时间')
    log_model = fields.Char(string='日志模块')
    log_class = fields.Char(string='日志级别')
    log_symbol = fields.Char(string='日志助记符')
    log_contents = fields.Char(string='日志内容')
    log_name = fields.Char(string='交换机名称')

    @api.model
    def get_switch_data(self, args):
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; text/xml; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        }

        # 交换机的名称
        switches_name = {
            'hxjh_m': '板桥核心交换机A登录信息',
            'hxjh_s': '板桥核心交换机B登录信息',
            'jrjh_m': '板桥接入交换机A登录信息',
            'jrjh_s': '板桥接入交换机B登录信息',
            'tpy_jrjh_m': '太平园接入交换机A登录信息',
            'tpy_jrjh_s': '太平园接入交换机B登录信息',
            'gdl_jrjh_m': '高大路接入交换机A登录信息',
            'gdl_jrjh_s': '高大路接入交换机B登录信息',
            'gdl_jrjh_m_1': '高大路排班室交换机A登录信息',
            'gdl_jrjh_s_1': '高大路排班室交换机B登录信息',
        }
        session = requests.Session()
        ip = self.env['maintenance_management.database_data'].search([('name', '=', switches_name.get(args))]).ip
        if ip:
            ip = 'https://' + ip
        else:
            _logger.info('请检查交换机基础配置是否错误')
            return '请检查配置是否错误'
        try:
            switch_data = self.env['maintenance_management.database_data'].search(
                [('name', '=', switches_name.get(args))])
            UserName = eval(switch_data.other)[0]
            Password = eval(switch_data.other)[1]
            switch_login_data = "&UserName={}&Password={}&Edition=0".format(UserName, Password)
            ret = self.posts(ip, LOGIN_URL, switch_login_data, header, session)
            token = ret.content.decode().split('&')[1].split('=')[1]
            header['Token'] = token
            header['Cookie'] = self.get_cookie_str(ret.headers.get('set-cookie').split(';')[0], token)

            ret = session.post(self.get_url(ip, CONFIG_URL), self.get_data(CONFIG_URL), headers=header,
                               verify=False, timeout=2)
            config_data = ret.content.decode('utf-8')
            all_create_data = []
            for value, config_rec in enumerate(config_data.split('\n')):
                if value > 12:
                    if not config_rec.split(' ')[1]:
                        log_contents = config_rec.split(']:')[1]
                        log_time = str(config_rec.split(' ')[0:5])[1:-1].replace(',', ' ').replace("'", '')
                        log_model = config_rec.split(' ')[6].split('/')[0].split('%%01')[-1]
                        log_class_get_data = config_rec.split(' ')[6].split('/')[1]
                        try:
                            log_symbol = config_rec.split(' ')[6].split('/')[2].split('(')[0]
                        except:
                            log_symbol = ''
                            _logger.info('交换机日志获取信息错误')
                    else:
                        log_contents = config_rec.split(']:')[1]
                        log_time = str(config_rec.split(' ')[0:3])[1:-1].replace(',', ' ').replace("'", '')
                        log_model = config_rec.split(' ')[5].split('/')[0].split('%%01')[-1]
                        try:
                            log_symbol = config_rec.split(' ')[5].split('/')[2].split('(')[0]
                        except:
                            log_symbol = ''
                            _logger.info('交换机日志获取信息错误')
                        log_class_get_data = config_rec.split(' ')[5].split('/')[1]
                    if log_class_get_data == '3':
                        log_class = '错误'
                    else:
                        log_class = '警告'
                    search_data = self.search_read([
                        ('log_time', '=', log_time),
                        ('log_model', '=', log_model),
                        ('log_class', '=', log_class),
                        ('log_symbol', '=', log_symbol),
                        ('log_contents', '=', log_contents),
                        ('log_name', '=', switches_name.get(args)),
                    ])
                    if not search_data:
                        all_create_data.append({
                            'log_time': log_time,
                            'log_model': log_model,
                            'log_class': log_class,
                            'log_symbol': log_symbol,
                            'log_contents': log_contents,
                            'log_name': switches_name.get(args)
                        })
                        self.create(all_create_data)
            tree_id = self.env.ref('maintenance_management.switch_log_tree_id').id
            form_id = self.env.ref('maintenance_management.switch_log_form_id').id
            return {
                "name": "交换机日志",
                "type": "ir.actions.act_window",
                "res_model": "maintenance_management.switch_log",
                "par": args,
                "domain": [('log_name', '=', switches_name.get(args))],
                "views": [
                    [tree_id, "list"],
                    [form_id, "form"],
                ],
            }
        except Exception as e:
            _logger.info(e)
            _logger.info('信息配置错误')
            return '请检查配置是否错误'

    # 获取页面数据
    def posts(self, ip, url, data, headers, session):
        return session.post(self.get_url(ip, url), data=data, headers=headers, verify=False)

    # 获取url
    def get_url(self, base_url, url):
        tmp = random.random()
        return "%s/%s?_=%s" % (base_url, url, str(tmp) + '0' * (17 - len(str(tmp))))

    # 自动生成 32位token
    def get_token(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 32))

    # xml_rpc 数据
    def get_data(self, url):
        msg_id = int(random.random() * 1000)
        if url == CONFIG_URL:
            ms = 'MessageID={}&<rpc message-id="{}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">' \
                 '<edit-config operation="merge">' \
                 '<target>' \
                 '<running/>' \
                 '</target>' \
                 '<error-option>stop-on-error</error-option>' \
                 '<config>' \
                 '<featurename istop="true" type="cli">' \
                 '<display> logbuffer</display></featurename>' \
                 '</config>' \
                 '</edit-config>' \
                 '</rpc>]]>]]>'.format(msg_id, msg_id)
            return ms

    def get_cookie_str(self, sessionid, token):
        ret = "%s; icbs_language=zh-cn; LSWlanguage=lsw_lang_zh.js; UserName=admin; Token=%s" % (
            sessionid, token)
        if token:
            ret = "%s; Token=%s" % (ret, token)
        return ret

    @api.model
    def model_temperature(self, args):
        # 板桥的核心交换机只有2,4端口有数据
        if args in ['hxjh_m', 'hxjh_s']:
            port = '2'
        # 高大路的核心交换机只有25,26端口有数据
        elif args in ['gdl_jrjh_m', 'gdl_jrjh_s']:
            port = '25'
        return {
            'name': '日志与光模块数据',
            'type': 'ir.actions.client',
            'tag': 'transmission_channel_monitoring',
            'args_name': args,
            'node_name': port,
            'button_model': 'temperature',
        }

    @api.model
    def model_current(self, args):
        # 板桥的核心交换机只有2,4端口有数据
        if args in ['hxjh_m', 'hxjh_s']:
            port = '2'
        # 高大路的核心交换机只有25,26端口有数据
        elif args in ['gdl_jrjh_m', 'gdl_jrjh_s']:
            port = '25'
        return {
            'name': '日志与光模块数据',
            'type': 'ir.actions.client',
            'tag': 'transmission_channel_monitoring',
            'args_name': args,
            'node_name': port,
            'button_model': 'current',
        }

    @api.model
    def model_voltage(self, args):
        # 板桥的核心交换机只有2,4端口有数据
        if args in ['hxjh_m', 'hxjh_s']:
            port = '2'
        # 高大路的核心交换机只有25,26端口有数据
        elif args in ['gdl_jrjh_m', 'gdl_jrjh_s']:
            port = '25'
        return {
            'name': '日志与光模块数据',
            'type': 'ir.actions.client',
            'tag': 'transmission_channel_monitoring',
            'args_name': args,
            'node_name': port,
            'button_model': 'voltage',
        }

    @api.model
    def model_transmission_power(self, args):
        # 板桥的核心交换机只有2,4端口有数据
        if args in ['hxjh_m', 'hxjh_s']:
            port = '2'
        # 高大路的核心交换机只有25,26端口有数据
        elif args in ['gdl_jrjh_m', 'gdl_jrjh_s']:
            port = '25'
        return {
            'name': '日志与光模块数据',
            'type': 'ir.actions.client',
            'tag': 'transmission_channel_monitoring',
            'args_name': args,
            'node_name': port,
            'button_model': 'transmission',
        }

    @api.model
    def model_receive_power(self, args):
        # 板桥的核心交换机只有2,4端口有数据
        if args in ['hxjh_m', 'hxjh_s']:
            port = '2'
        # 高大路的核心交换机只有25,26端口有数据
        elif args in ['gdl_jrjh_m', 'gdl_jrjh_s']:
            port = '25'
        return {
            'name': '日志与光模块数据',
            'type': 'ir.actions.client',
            'tag': 'transmission_channel_monitoring',
            'args_name': args,
            'node_name': port,
            'button_model': 'receive',
        }

    @api.model
    def choose_node_return_data(self, node_type, node_name):
        '''
        选择事件的时候获取相应的数据
        :param node_type: 类型
        :param node_name: 端口名字
        :return:
        '''
        datetime.datetime.now()
        switches_name = {
            'hxjh_m': '板桥核心交换机A',
            'hxjh_s': '板桥核心交换机B',
            'tpy_jrjh_m': '高大路接入交换机A',
            'gdl_jrjh_m': '高大路接入交换机A',
            'gdl_jrjh_s': '高大路接入交换机B',
        }
        data = self.env['maintenance_management.transmission_channel'].search_read([
            ('switches', '=', switches_name.get(node_type)),
            ('node_name', '=', node_name),
            ('write_date', '<', datetime.datetime.now()),
            ('write_date', '>', datetime.datetime.now() - datetime.timedelta(hours=24)),
        ])

        # 用来存放合适的数据
        lis = [[[], []], [[], []], [[], []], [[], []], [[], []], [[], []]]
        for rec in data:
            if rec.get('temperature'):
                lis[0][0].append(rec.get('temperature'))
                lis[0][1].append(
                    (rec.get('write_date') + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')[10:])
            if rec.get('current'):
                lis[1][0].append(rec.get('current'))
                lis[1][1].append(
                    (rec.get('write_date') + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')[10:])
            if rec.get('voltage'):
                lis[2][0].append(rec.get('voltage'))
                lis[2][1].append(
                    (rec.get('write_date') + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')[10:])
            if rec.get('transmitted_light_power'):
                lis[3][0].append(rec.get('transmitted_light_power'))
                lis[3][1].append(
                    (rec.get('write_date') + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')[10:])
            if rec.get('received_light_power'):
                lis[4][0].append(rec.get('received_light_power'))
                lis[4][1].append(
                    (rec.get('write_date') + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')[10:])
        return lis

    @api.multi
    def get_form_data(self):
        '''
        :return:
        '''
        data = 'MessageID=192&<rpc message-id="192" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">' + \
               '<get><filter type="subtree"><featurename istop="true" type="mib">' \
               '<hwEntityStateEntry position' \
               '="iso.org.dod.internet.private.enterprises.huawei.huaweiMgmt.hwDatacomm.' \
               'hwEntityExtentMIB.hwEntityExtObjects.hwEntityState.hwEntityStateTable">' \
               '<entPhysicalIndex>67108873</entPhysicalIndex><hwEntityBoardName/><hwEntityCpuUsage/>' \
               '<hwEntityCpuUsageThreshold/><hwEntityMemUsage/><hwEntityMemUsageThreshold/><hwEntityTemperature/>' \
               '<hwEntityTemperatureThreshold/><hwEntityOperStatus/></hwEntityStateEntry></featurename></filter>' \
               '</get></rpc>]]>]]>'

        return data

    @api.model
    def get_light_models(self, args):
        '''
        获取当前交换机的端口的的数据和状态
        :param name:  交换机的名称
        :return:
        '''
        header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; text/xml; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        }

        # 交换机的名称
        switches_name = {
            'hxjh_m': '板桥核心交换机A登录信息',
            'hxjh_s': '板桥核心交换机B登录信息',
            'jrjh_m': '板桥接入交换机A登录信息',
            'jrjh_s': '板桥接入交换机B登录信息',
            'tpy_jrjh_m': '太平园接入交换机A登录信息',
            'gdl_jrjh_m': '高大路接入交换机A登录信息',
            'gdl_jrjh_s': '高大路接入交换机B登录信息',
            'gdl_jrjh_m_1': '高大路排班室交换机A登录信息',
            'gdl_jrjh_s_1': '高大路排班室交换机B登录信息',
        }
        try:
            session = requests.Session()
            ip = self.env['maintenance_management.database_data'].search([('name', '=', switches_name.get(args))]).ip
            if ip:
                ip = 'https://' + ip
            else:
                return '请检查配置是否错误'
            switch_data = self.env['maintenance_management.database_data'].search(
                [('name', '=', switches_name.get(args))])
            UserName = eval(switch_data.other)[0]
            Password = eval(switch_data.other)[1]
            switch_login_data = "&UserName={}&Password={}&Edition=0".format(UserName, Password)
            ret = session.post(self.get_url(ip, LOGIN_URL), data=switch_login_data, headers=header, verify=False,
                               timeout=3)
            token = ret.content.decode().split('&')[1].split('=')[1]
            header['Token'] = token
            header['Cookie'] = self.get_cookie_str(ret.headers.get('set-cookie').split(';')[0], token)

            lig_ret = session.post(self.get_url(ip, 'customizeservice.cgi'), data='CustomizeCode=100&SlotID=[1:0]',
                                   headers=header, verify=False)
            config_data = lig_ret.content.decode('utf-8')
            token = config_data.split('Token=')[1]
            header['Cookie'] = self.get_cookie_str(ret.headers.get('set-cookie').split(';')[0], token)
            equipment_info = session.post(self.get_url(ip, CONFIG_URL), self.get_form_data(), headers=header,
                                          verify=False)
            # 用来存放数据
            all_data = []
            # 获取设备面板的数据
            slot_data = config_data.split('Token=')[0]
            for data in eval(slot_data).get('0'):
                # 获取当前的端口号有是不是链接状态
                port = data[0].split('/')[-1]
                #
                network = data[1]
                network_two = data[3]
                if network == 1 and network_two == 2:
                    work = False
                else:
                    work = True

                light = data[3]
                if light == 1:
                    light_button = True
                else:
                    light_button = False
                all_data.append({
                    'name': port,
                    'work': work,
                    'light_button': light_button,
                })
            cup = re.findall('<hwEntityCpuUsage>(.*)(?=</hwEntityCpuUsage>)', equipment_info.text)[0]
            memory = re.findall('<hwEntityMemUsage>(.*)(?=</hwEntityMemUsage>)', equipment_info.text)[0]
            temperature = re.findall('<hwEntityTemperature>(.*)(?=</hwEntityTemperature>)', equipment_info.text)[0]
            return [all_data, [cup, memory, temperature]]
        except Exception as e:
            _logger.info(e)
            _logger.info('获取交换机日志失败')
            return '数据获取失败'
