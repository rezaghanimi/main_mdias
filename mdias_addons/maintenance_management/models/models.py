# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import base64
import os

PATH_DIR = os.path.dirname(os.path.dirname(__file__))


class MaintenanceManagement(models.Model):
    _name = 'maintenance_management.maintenance_management'

    name = fields.Binary()

    @api.model
    def get_map_info(self):
        user = self.env.user
        if user.cur_location:
            line_id = user.cur_location.line.name
        else:
            raise exceptions.ValidationError('当前用户没有配置所属场段或车辆段!')
        # 每次进来都需要打开文件对比一次看看时候修改过
        if line_id == '8号线':
            line_dirname = '{}/static/xml/eight_line_station.xml'.format(PATH_DIR)
        elif line_id == '6号线':
            line_dirname = '{}/static/xml/six_line_station.xml'.format(PATH_DIR)
        elif line_id == '10号线':
            line_dirname = '{}/static/xml/ten_line_station.xml'.format(PATH_DIR)
        else:
            raise exceptions.ValidationError('所属场段目前没有设置')
        with open(line_dirname, 'rb') as f:
            file = base64.b64encode(f.read())
            # 查看是否有一样的问题没有就创建一新条记录
            rec = self.sudo().search([('name', '=', file)])
            if not rec:
                rec = self.create({
                    'name': file
                })
            return rec.read()
