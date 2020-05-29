# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ...odoo_operation_log.model_extend import LogManage
import pendulum

_logger = logging.getLogger(__name__)

'''
{'lock': 0, 'index': 43, 'type': 2, 'block': 0, 'name': '21AG', 'hold': 0, 'notice': 0}
struct SectionStatus {
    BYTE hold : 1;                // 占用
    BYTE lock : 1;                // 锁闭
    BYTE block : 1;               // 封锁
    BYTE notice : 5;              // 提示信息
};'''


class RailsSec(models.Model):
    '''
    轨道管理
    出入站信号机前面有两个区段，我把靠外面那个当成出入段线，靠里面那个当做转换轨
    '''
    _name = 'metro_park_base.rails_sec'
    _description = '轨道管理'
    _inherit = ['metro_park_base.abs_hold_lister']
    _track_log = True

    _rec_name = 'alias'

    no = fields.Char(string='轨道编号')
    alias = fields.Char(string="别名")
    location = fields.Many2one(
        comodel_name="metro_park_base.location", string="位置")

    usage = fields.Char(string='轨道用途')

    index = fields.Integer(string="码位序号")
    name = fields.Char(string='名称')
    type = fields.Integer(string="类型编号")

    # is track 之后才能叫做 track，否则叫rail
    is_track = fields.Boolean(string='是否股道')
    rail_type = fields.Many2one(
        string='股道类型',
        comodel_name='metro_park_base.rail_type')

    rail_property = fields.Many2many(string='轨道属性',
                                     comodel_name='metro_park_base.rail_property',
                                     relation="rail_and_rail_property_rel",
                                     column1="rail_id",
                                     column2="property_id")

    port = fields.Selection(string='端口',
                            selection=[('A', 'A'), ('B', 'B')])

    reverse_port = fields.Many2one(string="反向端口",
                                   comodel_name="metro_park_base.rails_sec",
                                   compute="_compute_reverse_port",
                                   ondelete="set null",
                                   help="这里指向另外一端，这样才能关关起来")

    electric_live = fields.Boolean(string='是否带电')
    rail_length = fields.Char(string='轨长')
    rail_status = fields.Boolean(string='状态')

    electric_area = fields.Many2one(string="供电分区",
                                    comodel_name="metro_park_base.electric_area")
    special_switch = fields.Char(string="专用隔离开关")

    remark = fields.Text(string='备注')

    # 联锁发过来的相关状态
    lock = fields.Integer(string="锁闭")
    block = fields.Integer(string="封锁")
    hold = fields.Integer(string="是否占用")
    notice = fields.Integer(string="提示信息")

    # 左边连接的区段和右边连接区段
    left_rail_id = fields.Many2one(comodel_name='metro_park_base.rails_sec',
                                   string="左边的区段")
    right_rail_id = fields.Many2one(comodel_name='metro_park_base.rails_sec',
                                    string="右边的区段")

    # 与轨道<场段>相连的左右道岔,可为空
    left_switch_id = fields.Many2one('metro_park_base.switches', string='左道岔')
    left_switch_position = fields.Selection(selection=[('positive', 'positive'),
                                                       ('negative', 'negative'),
                                                       ('header', 'header')])
    right_switch_id = fields.Many2one('metro_park_base.switches', string='右道岔')
    right_switch_position = fields.Selection(selection=[('positive', 'positive'),
                                                        ('negative', 'negative'),
                                                        ('header', 'header')])

    x_pos = fields.Integer(string="x坐标")
    y_pos = fields.Integer(string="y坐标")

    can_stop = fields.Boolean(string="用于停车",
                              default=False)
    stop_order = fields.Integer(string="计划序号",
                                default=999,
                                help='用于安排加库位置的时候的优先级, 主要是为了把车分散开，避免一个车的发不出来')
    available = fields.Boolean(string="是否可用",
                               default=True)

    _sql_constraints = [('no_unique', 'UNIQUE(no, location)', "轨道编号不能重复"),
                        ('no_alias', 'UNIQUE(alias, location)', "轨道别名不能重复"),
                        ('left_rail_id_unique', 'UNIQUE(left_rail_id)', "左轨道不能不能连接两根不同轨道")]

    @api.one
    @api.constrains
    def constrains_connect_rail_or_switch(self):
        if (self.left_switch_id and self.left_rail_id) or \
                (self.right_rail_id and self.right_switch_id):
            raise ValidationError('轨道一端不能同时连接道岔和轨道')

    @api.model
    def get_rails_by_types(self, types):
        '''
        根据类型取得轨道集合
        :return:
        '''
        records = self.search([('rail_type', 'in', types)])
        return records

    @api.model
    def get_tracks(self):
        '''
        取得股道
        :return:
        '''
        tracks = self.search([('is_track', '=', True)])
        return tracks

    @api.multi
    def is_left_switch_connect(self):
        '''
        左方向道岔是否连接
        :return:
        '''
        self.ensure_one()
        if self.left_switch_id \
                and self.left_switch_position == "positive" \
                and self.left_switch_id.pos == 1 \
                and self.left_switch_id.hold == 1:
            return True

        if self.left_switch_id \
                and self.left_switch_position == "negative" \
                and self.left_switch_id.pos_reverse == 1 \
                and self.left_switch_id.hold == 1:
            return True

        return False

    @api.multi
    def is_right_switch_connect(self):
        '''
        右方向道岔是否连接
        :return:
        '''
        self.ensure_one()
        if self.right_switch_id \
                and self.right_switch_position == "positive" \
                and self.left_switch_id.pos == 1\
                and self.right_switch_id.hold == 1:
            return True

        if self.right_switch_id \
                and self.right_switch_position == "negative" \
                and self.right_switch_id.pos_reverse == 1 \
                and self.right_switch_id.hold == 1:
            return True

        return False

    @api.multi
    def get_hold_neighbors(self):
        '''
        取得被占用的邻居，区段不会出现多个同时占用的情况，所以直接返回
        :return:
        '''
        self.ensure_one()
        rst = []

        if self.left_rail_id \
                and self.left_rail_id.hold:
            rst.append(self.left_rail_id)

        if self.right_rail_id \
                and self.right_rail_id.hold:
            rst.append(self.right_rail_id)

        # 避免烧脑，写成两句
        if self.left_switch_id \
                and self.left_switch_id.hold \
                and (self.left_switch_position == 'negative'
                     and self.left_switch_id.pos_reverse == 1):
            rst.append(self.left_switch_id)

        if self.left_switch_id \
                and self.left_switch_id.hold \
                and (self.left_switch_position == 'positive'
                     and self.left_switch_id.pos == 1):
            rst.append(self.left_switch_id)

        if self.left_switch_id \
                and self.left_switch_id.hold \
                and self.left_switch_position == 'header':
            rst.append(self.left_switch_id)

        # 避免烧脑，写成两句
        if self.right_switch_id \
                and self.right_switch_id.hold \
                and (self.right_switch_position == 'negative'
                     and self.right_switch_id.pos_reverse == 1):
            rst.append(self.right_switch_id)

        if self.right_switch_id \
                and self.right_switch_id.hold \
                and (self.right_switch_position == 'positive'
                     and self.right_switch_id.pos == 1):
            rst.append(self.right_switch_id)

        if self.right_switch_id \
                and self.right_switch_id.hold \
                and self.right_switch_position == 'header':
            rst.append(self.right_switch_id)

        return rst

    @api.depends("port")
    def _compute_reverse_port(self):
        '''
        动态计算反向端口
        :return:
        '''
        all_rails = self.search([])
        rail_cache = {"%s_%d" % (record.no, record.location.id): record.id for record in all_rails}
        for record in self:
            if record.port:
                name = ""
                if record.port == 'A':
                    name = "%sBG_%d" % (record.no.rstrip(
                        'AG'), record.location.id)
                elif record.port == 'B':
                    name = "%sAG_%d" % (record.no.rstrip(
                        'BG'), record.location.id)
                if name in rail_cache:
                    record.reverse_port = rail_cache.get(name)

    @api.model
    def update_status(self, location_id, data):
        '''
        更新状态
        :param data:
        :param location_id:
        :return:
        '''

        name = data["name"]
        name = name.replace('_', "/")

        record = self.search(
            [('no', '=', name), ('location', '=', location_id)])
        if record:
            record.write(data)
            return record
        else:
            _logger.info("没有找到区段{name}".format(name=name))

    @api.multi
    def is_switch(self):
        '''
        是否为switch
        :return:
        '''
        return False

    @api.multi
    def get_train(self):
        '''
        取得占压的车辆
        :return:
        '''
        self.ensure_one()
        record = self.env["metro_park_dispatch.cur_train_manage"]\
            .search([('cur_rail', '=', self.id)])
        return record

    @api.model
    def update_train_info(self, location_id, data):
        '''
        更新车辆信息
        :return:
        '''
        name = data["name"]
        name = name.replace('_', "/")
        hold = data["hold"]
        track_obj = self.env['metro_park_dispatch.train_track']
        record = self.search(
            [('no', '=', name), ('location', '=', location_id)])
        if record:

            rail_type_back_sec = self.env.ref(
                "metro_park_base.rail_type_back_sec").id
            rail_type_out_sec = self.env.ref(
                "metro_park_base.rail_type_out_sec").id

            # 如果是出入段线的话则删除
            if record.rail_type.id == rail_type_back_sec \
                    or record.rail_type.id == rail_type_out_sec:
                right_rail = record.right_rail_id
                train = record.env["metro_park_dispatch.cur_train_manage"] \
                    .search([('cur_rail', '=', right_rail.id)], limit=1)
                if train:
                    train.cur_rail = False
                    train.cur_switch = False
                    train.notify_train_position_changed(right_rail.location.alias)
                    _logger.info(
                        "the train is on rail back sec, clear it")
                    LogManage.put_log(content='车{name}到达{position}出入段线,清除车号-MDIAS'.format(
                        name=train["train_no"],
                        position=record["no"]),
                        mode='cur_train_position_change')
                return

            if hold:
                neighbours = record.get_hold_neighbors()

                all_switches = self.env["metro_park_base.switches"]\
                    .search([('hold', '=', 1), ('location.id', '=', location_id)])
                all_switch_cache = {
                    switch.name: switch for switch in all_switches}

                # 有可能出现两个邻居都有车
                neighbour_has_train_count = 0
                trains = []
                for neighbour in neighbours:
                    # 如果是道岔，则看几个连在一起的道岔，不可能会太多
                    tmp_trains = []
                    if neighbour.is_switch():
                        if neighbour.is_switch():
                            neighbour_trains = []
                            sub_neighbour_names = []
                            neighbour.get_connected_switch_names(
                                sub_neighbour_names, all_switches.mapped("name"), True)
                            for name in sub_neighbour_names:
                                switch = all_switch_cache[name]
                                tmp_trains += switch.get_train()
                            tmp_trains += neighbour_trains
                    tmp_trains += neighbour.get_train()

                    # 防止两边都有车的情况
                    if len(tmp_trains) > 0:
                        neighbour_has_train_count += 1
                    trains += tmp_trains

                # 两边都有车，暂不做处理
                if neighbour_has_train_count > 1:
                    return

                # if len(trains) == 0:
                #     LogManage.put_log(
                #         content='在相邻位置上没有找到车,使用ats进行推断-MDIAS', mode='cur_train_position_change')
                #     train = self.env["metro_park_dispatch.cur_train_manage"].search(
                #         [('ats_position', '=', record.no)])
                #     if train:
                #         LogManage.put_log(
                #             content='轨道处理根据ats推断成功-MDIAS', mode='cur_train_position_change')
                #         trains.append(train)

                # 多余一个车没办法进行处理，只能跑到相邻的轨道上去
                for train in trains:
                    if record.is_switch():
                        train.cur_switch = record.id
                        train.cur_rail = False
                        try:
                            _logger.info('set train position {train} -> {position}'.format(
                                train=train.train_no, position=record.name))
                            LogManage.put_log(content='车{name}到达{position}-MDIAS'.format(
                                name=train["train_no"],
                                position=record["name"]),
                                mode='cur_train_position_change')
                        except Exception as error:
                            _logger.info('put log error {error}'.format(error=error))
                    else:
                        train.cur_rail = record.id
                        train.cur_switch = False

                        _logger.info('set train position {train} -> {position}'.format(
                            train=train.train_no, position=record.no))

                        LogManage.put_log(content='车{name}到达{position}-MDIAS'.format(
                            name=train["train_no"],
                            position=record["no"]),
                            mode='cur_train_position_change')

                    # 提前提交，notify是在线程里处理，有可能还没有提交过去
                    self._cr.commit()
                    train.notify_train_position_changed()

                    track_obj.update_track(train.id, rail_id=record.id)
            else:
                # 如果出清的时候上面还有车，那需要把车移到相邻的轨道上去
                train = record.env["metro_park_dispatch.cur_train_manage"] \
                    .search([('cur_rail', '=', record.id)], limit=1)
                # 当前轨道上有车的时候才处理
                if train:
                    neighbours = record.get_hold_neighbors()
                    # 如果刚好是只有一个相邻
                    if len(neighbours) == 1:
                        neighbour = neighbours[0]
                        if neighbour.is_switch():
                            train.cur_switch = neighbour.id
                            train.cur_rail = False
                            _logger.info('set train position {train} -> {position}'.format(
                                train=train.train_no, position=neighbour.name))
                            LogManage.put_log(content='车{name}到达{position}出入段线,清除车号-MDIAS'.format(
                                name=train["train_no"],
                                position=neighbour["name"]),
                                mode='cur_train_position_change')
                        else:
                            train.cur_rail = neighbour.id
                            train.cur_switch = False
                            _logger.info('set train position {train} -> {position}'.format(
                                train=train.train_no, position=neighbour.no))
                            LogManage.put_log(content='车{name}到达{position}出入段线,清除车号-MDIAS'.format(
                                name=train["train_no"],
                                position=neighbour["no"]),
                                mode='cur_train_position_change')
                        # 提前提交，notify是在线程里处理，有可能还没有提交过去
                        self._cr.commit()
                        train.notify_train_position_changed()
                    track_obj.update_track(train.id, rail_id=record.id, level=True)

    @api.model
    def get_rail_id_by_no(self, rail_no, location_id):
        '''
        通过rail_no获取location_id
        :param rail_no:
        :param location_id:
        :return:
        '''
        return self.search(['|',
                            ('no', '=', rail_no),
                            ('alias', '=', rail_no),
                            ('location', '=', location_id)])
