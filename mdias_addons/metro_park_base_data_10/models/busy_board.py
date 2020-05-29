
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class BusyBoard(models.Model):
    '''
    占线板信息
    '''
    _inherit = 'metro_park_base.busy_board'

    @api.model
    def get_busy_board_info(self, location_alias):
        '''
        取得占线板信息
        :return:
        '''
        rst = []
        records = self.search(
            ['|',
             ('rail.location.alias', '=', location_alias),
             ('switch.location.alias', '=', location_alias)])
        for record in records:
            if not record.icons:
                continue
            rst.append({
                'uid': record.uid,
                'icons': record.icons.split(',')
            })

        return rst

    @api.model
    def update_construction_icons(self):
        '''
        从施工调度获取占线板信息
        :return:
        '''
        info = self.get_work_area_info()
        rail_nos = info.rails
        switch_names = info.switches
        rails = self.env['metro_park_base.rails_sec'].search(
            [('no', 'in', rail_nos)])
        switches = self.env['metro_park_base.switches'].search(
            [('name', 'in', switch_names)])
        for rail in rails:
            self.set_busy_icon_status(
                rail.no, rail.loation.alias, 'construction')
        for switch in switches:
            self.set_busy_icon_status(
                switch.name, switch.loation.alias, 'construction')

    @api.model
    def get_work_area_info(self):
        '''
        :return:
        '''
        now_str = pendulum.now('UTC').format('YYYY-MM-DD HH:mm:ss')

        # 取昨当前的计划
        plans = self.env['metro_park_dispatch.construction_plan'].search(
            [('out_work_start_time', '<=', now_str), ('out_work_end_time', '>=', now_str)])
        work_area_ids = []
        for plan in plans:
            work_area_ids += plan.work_areas.ids

        work_area_infos = \
            self.env['metro_park_dispatch.construction_area_relation'].browse(
                work_area_ids)
        rst = {'rails': [], 'switches': []}
        for info in work_area_infos:
            if info.element_type == 'rail':
                rst['rails'].append(info.park_element_code)
                rst['switches'].append(info.park_element_code)

        return rst

    @api.model
    def set_busy_icon_status(self, uid, location_alias, operation, busy_types):
        '''
        设置轨道占线板信息
        :return:
        '''
        # 如果找到rail则使用rail
        if location_alias == 'ban_qiao':
            location_alias = 'banqiao'

        if location_alias == 'gao_da_lu':
            location_alias = 'gaodalu'

        # 联锁用的是-, 基础数据用的是/
        old_icons = []
        uid = uid.replace('_', '/')
        rail = self.env["metro_park_base.rails_sec"].search(
            [('location.alias', '=', location_alias), ('no', 'in', [uid, uid + 'G'])])
        if rail:
            record = self.search([('rail', '=', rail.id)])
            if record:
                old_icons = record.icons or ''
                old_icons = old_icons.split(',')
                if operation == 'add':
                    old_icons += busy_types
                elif operation == 'del':
                    tmp = []
                    for icon in old_icons:
                        if icon not in busy_types:
                            tmp.append(icon)
                    old_icons = tmp
                old_icons = list(set(old_icons))
                record.icons = ','.join(old_icons)
            else:
                old_icons = busy_types
                self.create([{
                    "icons": ','.join(busy_types),
                    "rail": rail.id
                }])

        # 如果找到switch就使用switch信息
        switch = self.env['metro_park_base.switches'].search(
            [('location.alias', '=', location_alias), ('name', '=', uid)])
        if switch:
            record = self.search([('switch', '=', switch.id)])
            if record:
                old_icons = record.icons or ''
                old_icons = old_icons.split(',')
                if operation == 'add':
                    old_icons += busy_types
                elif operation == 'del':
                    tmp = []
                    for icon in old_icons:
                        if icon not in busy_types:
                            tmp.append(icon)
                    old_icons = tmp
                old_icons = list(set(old_icons))
                record.icons = ','.join(old_icons)
            else:
                old_icons = busy_types
                self.create([{
                    "icons": ','.join(busy_types),
                    "switch": switch.id
                }])

        # 完事了通知前端发生改变
        # if operation == 'del':
        #     return

        rst = [{
            'uid': uid,
            'icons': old_icons
        }]

        self.trigger_up_event('funenc_socketio_server_msg', data={
            "msg_type": "update_busy_icons",
            "location_alias": location_alias,
            "msg_data": rst
        })
