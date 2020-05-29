# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, tools
from operator import itemgetter
import json

import logging

_logger = logging.getLogger(__name__)


class InterlockRoute(models.Model):
    '''
    联锁进路, 说明, 信号机等由于基础模块里没有进行维护，所以这里通过名称来进行对应
    '''

    _name = 'metro_park.interlock.route'
    _rec_name = 'origin_press_btn'
    _description = '联锁进路'
    _track_log = True

    table_id = fields.Many2one(string='所属联锁表',
                               comodel_name='metro_park.interlock.table',
                               ondelete="cascade")

    index = fields.Integer(string='序号')
    route_type = fields.Selection(selection=[('train', '列车进路'), ('dispatch', '调车')],
                                  string="进路类型",
                                  required=True)

    direction = fields.Char(string='方向')
    route_sub_type = fields.Char(string='类型')

    start_rail = fields.Many2one(string="起始轨道",
                                 comodel_name="metro_park_base.rails_sec")
    end_rail = fields.Many2one(string="终止轨道",
                               comodel_name="metro_park_base.rails_sec")

    method = fields.Char(string='方式')

    origin_press_btn = fields.Char(string='原表按下按钮')
    mdias_press_start = fields.Char(string='mdias始端按钮')
    # mdias_press_change = fields.Char(string='mdias变通进路按钮')
    mdias_press_end = fields.Char(string='mdias终端按钮')

    direction_switch = fields.Many2one(string='方向道岔',
                                       comodel_name="metro_park_base.switches")
    signals_infos = fields.Many2one(string='信号机信息',
                                    comodel_name='metro_park.interlock.signal_infos',
                                    inverse_name="route_id")
    # 多个道岔
    switch_infos = fields.One2many(string='道岔',
                                   comodel_name='metro_park.interlock.switch_info',
                                   inverse_name="route_id")
    switch_text = fields.Char(string="道岔原始数据")

    hostile_signal_infos = fields.One2many(string='敌对信号',
                                           comodel_name='metro_park.interlock.hostile_signal_info',
                                           inverse_name="route_id")
    hostile_signal_text = fields.Char(string='敌对信号原始数据')

    sec_infos = fields.One2many(string="轨道区段",
                                comodel_name="metro_park.interlock.sec_infos",
                                inverse_name="route_id")
    sec_text = fields.Char(string="轨道区段原始数据")

    location = fields.Many2one(string="所属场段",
                               comodel_name="metro_park_base.location")

    length = fields.Float(string='长度')

    face_route = fields.Many2one(string="迎面进路",
                                 comodel_name="metro_park_base.rails_sec")
    other_interlock = fields.Many2one(string="其它(联锁)",
                                      comodel_name="metro_park_base.other_interlock")

    rail_and_switches = fields.Text(string="轨道区段",
                                    compute="_compute_rail_and_switches",
                                    store=True,
                                    help="经过的轨道和区段，用于占压显示")

    _sql_constraints = [('index_unique', 'UNIQUE(location, index)', "编号不能重复")]

    @api.model
    def search_route(self, location, start_rail, end_rail, route_type):
        '''
        直接搜索路径
        :return:
        '''
        records = self.search([
            ('start_rail', '=', start_rail.id),
            ('end_rail', '=', end_rail.id),
            ('location', '=', location),
            ('route_type', '=', route_type)
        ])

        return records

    @api.model
    def create_cache(self, location, start_rail, end_rail, route_type, tmp_routes):

        if not tmp_routes or len(tmp_routes) == 0:
            return

        record = self.env['interlock_table.route_cache'].search([
            ('route_type', '=', route_type),
            ('start_rail', '=', start_rail),
            ('end_rail', '=', end_rail),
            ('location', '=', location)
        ])
        if record:
            return

        # 添加缓存
        vals = []
        for route in tmp_routes:
            val = {
                "route_type": route_type,
                "start_rail": start_rail,
                "end_rail": end_rail,
                "location": location,
                "route_info": [],
            }
            for index, sub_route in enumerate(route):
                val["route_info"].append((0, 0, {
                    "index": index,
                    "route": sub_route.id
                }))
            vals.append(val)
        self.env['interlock_table.route_cache'].create(vals)

    @api.model
    def get_asist_lines(self, location_id):
        '''
        查找牵出线
        :return:
        '''
        tmp_id = self.env.ref('metro_park_base.rail_type_pull_out').id
        records = self.search(
            [('start_rail.rail_type.id', '=', tmp_id), ('location', '=', location_id)])
        return records

    @api.model
    def get_route_info(self, route_id):
        '''
        取得进路信息, 没有查找其它的相关信息
        :param route_id:
        :return:
        '''
        return self.browse(route_id)

    @api.model
    def search_dispatch_route(self, location, start_rail, end_rail):
        '''
        搜索调车进路
        :param location:
        :param start_rail:
        :param end_rail:
        :return:
        '''
        route_type = 'dispatch'

        # 先从缓存中去获取
        routes_cahce = self.env["interlock_table.route_cache"].get_route_cache(
            location, start_rail.id, end_rail.id, route_type)
        if routes_cahce:
            return routes_cahce

        origin_start_id = start_rail.id
        origin_end_id = end_rail.id

        # 相邻的
        records = self.search_route(location, start_rail, end_rail, route_type)
        if records:
            self.create_cache(location, origin_start_id,
                              origin_end_id, route_type, [records])
            return [records]

        rail_type_pull_out_id = self.env.ref(
            'metro_park_base.rail_type_pull_out').id

        # 高大路洗车的特殊处理
        if start_rail.rail_type.id == end_rail.rail_type.id == rail_type_pull_out_id \
                and start_rail.usage == '洗车牵出线':
            wash_rail = self.env['metro_park_base.rails_sec'].search([
                ('available', '=', True),
                ('rail_type', '=', self.env.ref(
                    'metro_park_base.rail_type_wash').id),
                ('location', '=', location)
            ])
            if not wash_rail:
                raise exceptions.Warning("无法找到洗车线，请确定基础基础数据是否配置正确！")
            to_washs = self.search_sub_routes(
                location, start_rail, wash_rail,
                [], route_type, 'from_exchange', 0
            )
            from_washs = self.search_sub_routes(
                location, wash_rail, end_rail,
                [], route_type, 'to_exchange', 0
            )
            wash_routes = []
            if to_washs and from_washs:
                wash_routes += [to_wash +
                                from_wash for to_wash in to_washs for from_wash in from_washs]
            self.create_cache(location, origin_start_id,
                              origin_end_id, route_type, wash_routes)
            return wash_routes

        # 起点是牵出线
        if start_rail.rail_type.id == rail_type_pull_out_id \
                and start_rail.usage != '洗车牵出线':
            routes = self.search_sub_routes(
                location, start_rail, end_rail,
                [], route_type, 'from_exchange', 0
            )
            self.create_cache(location, origin_start_id,
                              origin_end_id, route_type, routes)
            return routes

        # 终点是牵出线
        if end_rail.rail_type.id == rail_type_pull_out_id \
                and end_rail.usage != '洗车牵出线':
            routes = self.search_sub_routes(
                location, start_rail, end_rail,
                [], route_type, 'to_exchange', 0
            )
            self.create_cache(location, origin_start_id,
                              origin_end_id, route_type, routes)
            return routes

        # 取得所有的牵出线
        exchange_rails = self.env['metro_park_base.rails_sec'].search([
            ('available', '=', True),
            ('rail_type', '=', rail_type_pull_out_id),
            ('location', '=', location),
            ('usage', '!=', '洗车牵出线')
        ])

        if not exchange_rails:
            raise exceptions.Warning("无法找到牵出线，请确定是否导入联锁表")

        routes = []
        for exchange_rail in exchange_rails:
            to_exchanges = self.search_sub_routes(
                location, start_rail, exchange_rail,
                [], route_type, 'to_exchange', 0
            )
            if to_exchanges:
                from_exchanges = self.search_sub_routes(
                    location, exchange_rail, end_rail,
                    [], route_type, 'from_exchange', 0
                )
                if from_exchanges:
                    routes += [
                        to_route + from_route for to_route in to_exchanges for from_route in from_exchanges]
        self.create_cache(location, origin_start_id,
                          origin_end_id, route_type, routes)
        return routes

    @api.model
    def search_train_plan_route(
            self, location, start_rail, end_rail, route_type):
        '''
        搜索调车进路, 已经分成多勾
        :param location:
        :param start_rail:
        :param end_rail:
        :param route_type:
        :return:
        '''
        # 先从缓存中去获取
        routes_cahce = self.env["interlock_table.route_cache"].get_route_cache(
            location, start_rail.id, end_rail.id, route_type)
        if routes_cahce:
            return routes_cahce

        origin_start_id = start_rail.id
        origin_end_id = end_rail.id

        if start_rail.reverse_port == end_rail:
            routes = self.search_route(
                location=location, start_rail=start_rail, end_rail=end_rail, route_type='dispatch')
            self.create_cache(location, origin_start_id,
                              origin_end_id, route_type, routes)
            return routes

        # 找取B到A的路由，更新终起点为A
        start_route = None
        if start_rail.port == 'B':
            reverse_rail = start_rail.reverse_port
            start_route = self.search_route(
                location=location, start_rail=start_rail, end_rail=reverse_rail, route_type='dispatch')
            if not start_route:
                raise exceptions.Warning("没有找到B-A的路由")
            start_rail = reverse_rail

        # 找到A到B的路由, 同时更新终点为A
        end_route = None
        if end_rail.port == "B":
            reverse_rail = end_rail.reverse_port
            end_route = self \
                .search_route(location=location,
                              start_rail=reverse_rail,
                              end_rail=end_rail,
                              route_type='dispatch')
            if not end_route:
                raise exceptions.Warning("没有找到路由")
            end_rail = reverse_rail

        # 查看是否能直接找到
        routes = self \
            .search_route(location, start_rail, end_rail, 'train')
        if not routes:
            routes = self.search_sub_routes(
                location, start_rail, end_rail,
                [], route_type, '', 0
            )

        # 收发车的A->B或B-A要单独算一勾计划
        real_routes = []
        for route in routes:
            if start_route:
                real_routes.append(start_route)
                real_routes.append(route)
            elif end_route:
                real_routes.append(route)
                real_routes.append(end_route)
            else:
                real_routes.append(route)

        self.create_cache(location, origin_start_id,
                          origin_end_id, route_type, real_routes)
        return real_routes

    @api.model
    def search_sub_routes(self, location, start_rail, end_rail,
                          blacks, route_type='dispatch', sub_type='', depth=0):

        def check_same_switch(tmp_sub_routes):
            switch_list = []
            for sub_route in tmp_sub_routes:
                tmp_switches = sub_route.mapped(
                    "switch_infos.switches.switch.id")
                if set(switch_list).intersection(tmp_switches):
                    return False
                switch_list += tmp_switches
            return True

        def get_best_route(all_sub_routes):
            # 1.信号机最少 (一个联锁表的基础进路算一个)
            # 2.道岔最少 (双动，反位算两个，正位算一个)
            # 3.定位由于反位 (定位个数多的优于反位个数多的)

            if len(all_sub_routes) <= 1:
                return all_sub_routes

            statistical = []
            for index, tmp_sub_routes in enumerate(all_sub_routes):
                statistical.append(tmp_sub_routes.get_switch_count(index))

            result = sorted(statistical, key=itemgetter(
                'signal_count', 'switch_count', 'reverse_count'))

            return [all_sub_routes[result[0]['index']]]

        # 先从缓存中去获取
        routes_cahce = self.env["interlock_table.route_cache"].get_route_cache(
            location, start_rail.id, end_rail.id, route_type)
        if routes_cahce:
            return routes_cahce

        if depth > 4:
            return []

        # 直接查找
        all_sub_routes = []
        rail_type_pull_out_id = self.env.ref(
            'metro_park_base.rail_type_pull_out').id

        domain = [('location', '=', location)]
        if route_type == 'dispatch':
            domain.append(('route_sub_type', 'not in', ['发车', '接车']))
        elif route_type == 'back_plan':
            domain.append(('route_sub_type', '=', '接车'))
        else:
            domain.append(('route_sub_type', 'like', '发车'))
        sub_routes = self.search(domain + [
            ('start_rail', '=', start_rail.id),
            ('end_rail', '=', end_rail.id)
        ])
        if not sub_routes:  # 没找到
            if sub_type == 'to_exchange':
                domain.append(('end_rail', '=', end_rail.id))
                domain.append(
                    ('start_rail', 'not in', blacks.ids if blacks else []))
                sub_end_routes = self.search(domain)
                for sub_end_route in sub_end_routes:
                    tmp_end_rail = sub_end_route.start_rail
                    sub_start_routes = self.search_sub_routes(
                        location, start_rail, tmp_end_rail,
                        blacks + end_rail if blacks else end_rail,
                        'dispatch', '', depth + 1
                    )
                    if sub_start_routes:
                        for start_route in sub_start_routes:
                            all_sub_routes.append(start_route + sub_end_route)
            elif sub_type == 'from_exchange':
                domain.append(('start_rail', '=', start_rail.id))
                domain.append(
                    ('end_rail', 'not in', blacks.ids if blacks else []))
                sub_start_routes = self.search(domain)
                for sub_start_route in sub_start_routes:
                    tmp_start_rail = sub_start_route.end_rail
                    sub_end_routes = self.search_sub_routes(
                        location, tmp_start_rail, end_rail,
                        blacks + start_rail if blacks else start_rail,
                        'dispatch', '', depth + 1
                    )
                    if sub_end_routes:
                        for end_route in sub_end_routes:
                            all_sub_routes.append(
                                sub_start_route + end_route)
            else:
                domain.append(('end_rail', '=', end_rail.id))
                domain.append(
                    ('end_rail.rail_type', '!=', rail_type_pull_out_id))
                domain.append(
                    ('start_rail.rail_type', '!=', rail_type_pull_out_id))
                domain.append(
                    ('start_rail', 'not in', blacks.ids if blacks else []))
                sub_end_routes = self.search(domain)
                for sub_end_route in sub_end_routes:
                    tmp_end_rail = sub_end_route.start_rail
                    sub_start_routes = self.search_sub_routes(
                        location, start_rail, tmp_end_rail,
                        blacks + end_rail if blacks else end_rail,
                        route_type, '', depth + 1
                    )
                    if sub_start_routes:
                        for start_route in sub_start_routes:
                            all_sub_routes.append(
                                start_route + sub_end_route)
        else:
            all_sub_routes = [sub_routes]

        if depth > 0:
            rets = []
            for sub_routes in all_sub_routes:
                if check_same_switch(sub_routes):
                    rets.append(sub_routes)
            self.create_cache(location, start_rail.id,
                              end_rail.id, route_type, rets)
            return rets

        # 调车最优路径的判断
        if route_type == 'dispatch' and depth == 0:
            best_route = get_best_route(all_sub_routes)
            if best_route:
                self.create_cache(location, start_rail.id,
                                  end_rail.id, route_type, best_route)
            return best_route

        if all_sub_routes:
            self.create_cache(location, start_rail.id,
                              end_rail.id, route_type, all_sub_routes)

        return all_sub_routes

    @api.depends('sec_infos', 'switch_infos')
    def _compute_rail_and_switches(self):
        '''
        计算经过的轨道和区段
        :return:
        '''
        for record in self:
            record.rail_and_switches = \
                json.dumps(record.get_rail_and_switches())

    @api.multi
    def get_rail_and_switches(self):
        '''
        取得所有的区段和道岔
        :return:
        '''

        def get_special_sections(rails):
            if rails.endswith('DG'):
                secs = rails.replace('/', '_').replace('DG', '').split('-')
                return secs
            else:
                return [rails.replace('/', '_').replace('-', '_')]

        self.ensure_one()

        rst = []
        sec_switches = []
        # 去掉DG
        sec_names = self.sec_infos.mapped("sec.no")
        for sec in sec_names:
            if sec.endswith("DG"):  # 取出道岔信息，和后面道岔数据求交集
                sec_switches += get_special_sections(sec)
            else:
                rst += get_special_sections(sec)

        if self.start_rail.no.endswith("DG"):
            sec_switches += get_special_sections(self.start_rail.no)
        else:
            rst += get_special_sections(self.start_rail.no)

        if self.end_rail.no.endswith("DG"):
            sec_switches += get_special_sections(self.end_rail.no)
        else:
            rst += get_special_sections(self.end_rail.no)

        # 取得SWITCH
        switches = []
        for switch in self.switch_infos.filtered(
                lambda r: r.is_protect is not True):
            switches += switch.display.strip('[()]').split("/")

        rst += list(set(switches).intersection(set(sec_switches)))

        return list(set(rst))

    @api.multi
    def get_protect_switches(self):
        '''
        获取所有的防护道岔
        '''
        self.ensure_one()

        protect_switches = []
        for switch in self.switch_infos.filtered(
                lambda r: r.is_protect):
            protect_switches += switch.display.strip('[()]').split("/")

        return list(set(protect_switches))

    @api.multi
    def get_switches_direction(self):
        ret = {}
        for switch in self.switch_infos:
            switches_name = switch.mapped("switches.switch.name")
            for name in switches_name:
                ret[name] = {
                    "is_reverse": switch.is_reverse,
                    "is_protect": switch.is_protect
                }
        return ret

    @api.multi
    def get_press_btns(self):
        '''
        取得进路要按下的按扭
        :return:
        '''
        return [str(self.mdias_press_start).upper(), str(self.mdias_press_end).upper()]

    @api.multi
    def get_switch_count(self, index):
        # 2.道岔最少 (双动，反位算两个，正位算一个)
        # 3.定位由于反位 (定位个数多的优于反位个数多的)
        switch_count = 0  # 总道岔数
        reverse_count = 0  # 反位的道岔个数
        for item in self:
            for switch in item.switch_text.split(','):
                if not switch.startswith('['):  # 排除防护道岔
                    if switch.find('/') != -1:  # 是否双动
                        if switch.startswith('('):
                            switch_count += 2
                            reverse_count += 2
                        else:
                            switch_count += 1
                    else:
                        switch_count += 1
                        if switch.startswith('('):
                            reverse_count += 1

        return {
            'index': index,
            'signal_count': len(self),
            'switch_count': switch_count,
            'reverse_count': switch_count
        }
