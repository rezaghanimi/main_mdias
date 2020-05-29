# -*- coding: utf-8 -*-
# @author    magicianliang

import odoo
from odoo.tools import config
from odoo import api, fields, models
from odoo.models import SUPERUSER_ID
import threading
import time
from odoo.service.server import server

INITDATA = ''


class SocketInfoSend(models.Model):
    '''
    SocketInfoSend
    '''
    _name = 'maintenance_management.socket_info'

    @api.multi
    def call_api_task(self):
        main_methods = ['get_battery_data', 'monitor_all_equipment', 'equipment_monitoring',
                        'change_zabbix_connect_state']
        for main_method in main_methods:
            main_threading = threading.Thread(target=self.methods_to_perform, args=[main_method], daemon=True)
            main_threading.start()

    @api.multi
    def methods_to_perform(self, method):
        db_name = config.options['db_name']
        db_registry = odoo.registry(db_name)
        with api.Environment.manage(), db_registry.cursor() as cr:
            obj = api.Environment(cr, SUPERUSER_ID, {})['maintenance_management.database_data']
            while True:
                time.sleep(180)
                getattr(obj.env['maintenance_management.database_data'].sudo(), method)()
                obj.env.cr.commit()

    @api.multi
    def _register_hook(self):
        '''
        启动服务, 如果为安装模式则不启动
        :return:
        '''

        if getattr(server, 'main_thread_id') \
                != threading.currentThread().ident:
            return

        new_thread = threading.Thread(target=self.call_api_task, daemon=True)
        new_thread.start()

