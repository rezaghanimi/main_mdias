# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api, tools
from ...odoo_operation_log.model_extend import LogManage

_logger = logging.getLogger(__name__)

'''
enum CODE_TYPE {
  CODE_TYPE_NONE,
  CODE_TYPE_DAOCHA,             // 道岔
  CODE_TYPE_QUDUAN,             // 区段
  CODE_TYPE_JZXH,               // 进站信号
  CODE_TYPE_CZXH,               // 出站信号
  CODE_TYPE_DCXH,               // 调车信号
  CODE_TYPE_BSD,                // 表示灯
  CODE_TYPE_QFJS,               // 铅封计数
  CODE_TYPE_BJ                  // 报警
};

#pragma pack(push)
#pragma pack(1)

// 道岔状态
struct TurnoutStatus {
    BYTE pos : 1;                 // 定位
    BYTE pos_reverse : 1;         // 反位
    BYTE hold : 1;                // 占用
    BYTE lock : 1;                // 锁闭
    BYTE lock_s : 1;              // 单锁
    BYTE closed : 1;              // 封闭
    BYTE lock_gt : 1;             // 引导总锁闭
    BYTE switch_crowded : 1;      // 挤岔
    BYTE lock_protect : 1;        // 防护锁闭
    BYTE pos_blue : 1;            // 正位蓝
    BYTE reverse_blue : 1;        // 反位蓝
    BYTE notice : 5;              // 提示信息
};

// 表示灯
struct IndicatorLightStatus {
    BYTE light : 1;               // 亮灯
    BYTE flash : 1;               // 闪灯
    BYTE red : 1;                 // 红灯
    BYTE yellow : 1;              // 黄灯
    BYTE green : 1;               // 绿灯
    BYTE blue : 1;                // 蓝灯
    BYTE white : 1;               // 白灯
    BYTE yellow2 : 1;             // 黄灯
};


// 报警
struct AlarmStatus {
    BYTE value;
};
'''


class Switches(models.Model):
    '''
    道岔信息
    struct TurnoutStatus {
        BYTE pos : 1;                 // 定位
        BYTE pos_reverse : 1;         // 反位
        BYTE hold : 1;                // 占用
        BYTE lock : 1;                // 锁闭
        BYTE lock_s : 1;              // 单锁
        BYTE closed : 1;              // 封闭
        BYTE lock_gt : 1;             // 引导总锁闭
        BYTE switch_crowded : 1;      // 挤岔
        BYTE lock_protect : 1;        // 防护锁闭
        BYTE pos_blue : 1;            // 正位蓝
        BYTE reverse_blue : 1;        // 反位蓝
        BYTE notice : 5;              // 提示信息
    };
    '''
    _name = 'metro_park_base.switches'
    _track_log = True
    _inherit = ['metro_park_base.abs_hold_lister']

    name = fields.Char(string='名称')
    location = fields.Many2one(
        string="位置", comodel_name="metro_park_base.location")

    # 正向轨道
    positive_rail = fields.Many2one(
        comodel_name="metro_park_base.rails_sec", string="正向连接的轨道")
    negative_rail = fields.Many2one(
        comodel_name="metro_park_base.rails_sec", string="正向连接的轨道")
    header_rail = fields.Many2one(
        comodel_name="metro_park_base.rails_sec", string="岔尖连接的区段")

    positive_switch = fields.Many2one(
        comodel_name="metro_park_base.switches", string="正向连接的道岔")
    negative_switch = fields.Many2one(
        comodel_name="metro_park_base.switches", string="反向连接的道岔")
    header_switch = fields.Many2one(
        comodel_name="metro_park_base.switches", string="岔尖连接的道岔")

    rail_sec_id = fields.Many2one(
        comodel_name="metro_park_base.rails_sec", string="所属道岔区段")

    # x方向的坐标, 只是个大致的坐标
    x_pos = fields.Integer(string="x坐标")
    y_pos = fields.Integer(string="y坐标")

    pos = fields.Integer(string="定位", defult=0)
    pos_reverse = fields.Integer(string="反位", defult=0)
    hold = fields.Integer(string="占用", defult=0)
    lock = fields.Integer(string="锁闭", defult=0)
    lock_s = fields.Integer(string="单锁", defult=0)
    closed = fields.Integer(string="封闭", defult=0)
    lock_gt = fields.Integer(string="引导总锁闭", defult=0)
    switch_crowded = fields.Integer(string="挤岔", defult=0)
    lock_protect = fields.Integer(string="防护锁闭", defult=0)

    pos_blue = fields.Integer(string="正位蓝")
    reverse_blue = fields.Integer(string="反位蓝")
    notice = fields.Char(string="提示信息")

    is_together = fields.Boolean(string="挤岔", compute="_compute_error")
    is_sperate = fields.Boolean(string="四开", compute="_compute_error")

    remark = fields.Char(string='备注')

    # _sql_constraints = [('name_unique', 'UNIQUE(name)', "名称不能重复")]

    @api.depends('pos', 'pos_reverse')
    def _compute_error(self):
        '''
        计算错误状态
        :return:
        '''
        for record in self:
            if record.pos == 1 and record.pos_reverse == 1:
                record.is_together = True
                record.is_sperate = False
            elif record.pos == 0 and record.pos_reverse == 0:
                record.is_sperate = True
                record.is_together = False
            else:
                record.is_sperate = False
                record.is_together = False

    @api.model
    @tools.ormcache()
    def get_switches(self):
        switches = self.search([])
        switch_cache = {switch.name: switches.id for switch in switches}
        return switch_cache

    @api.multi
    def get_hold_neighbors(self, black_switches):
        '''
        取得被占用的邻居, 调用之前先检查是否两端都处于占压状态
        :return:
        '''
        self.ensure_one()
        rst = []
        if self.positive_rail \
                and self.positive_rail.hold == 1 \
                and self.pos == 1:
            rst.append(self.positive_rail)

        if self.negative_rail \
                and self.negative_rail.hold == 1 \
                and self.pos_reverse == 1:
            rst.append(self.negative_rail)

        if self.header_rail \
                and self.header_rail.hold == 1:
            rst.append(self.header_rail)

        if self.positive_switch \
                and self.pos == 1 \
                and self.positive_switch.hold == 1 \
                and self.positive_switch.name not in black_switches:
            rst.append(self.positive_switch)

        if self.negative_switch \
                and self.pos_reverse == 1 \
                and self.negative_switch.hold == 1 \
                and self.negative_switch.name not in black_switches:
            rst.append(self.negative_switch)

        if self.header_switch \
                and self.header_switch.hold == 1 \
                and self.header_switch.name not in black_switches:
            tmp_switch = self.header_switch
            if tmp_switch.header_switch.id == self.id:
                rst.append(tmp_switch)
            elif tmp_switch.positive_switch.id == self.id and tmp_switch.pos == 1:
                rst.append(tmp_switch)
            elif tmp_switch.negative_switch.id == self.id and tmp_switch.pos_reverse == 1:
                rst.append(tmp_switch)

        return rst

    @api.multi
    def get_hold_neighbors_switch(self, black_switches):
        '''
        取得被占用的邻居, 调用之前先检查是否两端都处于占压状态
        :return:
        '''
        self.ensure_one()
        rst = []
        if self.positive_switch and self.pos == 1 \
                and self.positive_switch.hold \
                and self.positive_switch.name not in black_switches:
            rst.append(self.positive_switch)

        if self.negative_switch and self.pos_reverse == 1 \
                and self.negative_switch.hold \
                and self.positive_switch.name not in black_switches:
            rst.append(self.negative_switch)

        if self.header_switch and self.header_switch.hold == 1 \
                and self.header_switch.name not in black_switches:
            # 还得判断heder switch的方位
            tmp_switch = self.header_switch
            if tmp_switch.header_switch.id == self.id:
                rst.append(tmp_switch)
            elif tmp_switch.positive_switch.id == self.id and tmp_switch.pos == 1:
                rst.append(tmp_switch)
            elif tmp_switch.negative_switch.id == self.id and tmp_switch.pos_reverse == 1:
                rst.append(tmp_switch)
        return rst

    @api.model
    def update_status(self, location, data):
        '''
        更新道岔状态
        :param name:
        :param data:
        :param location:
        :return:
        '''
        name = data["name"]
        record = self.search(
            [("name", "=", name), ('location', '=', location)])
        if record:
            record.write(data)
            return record

    @api.model
    def get_switch_id_by_no(self, switch_no, location_id):
        return self.search([("name", "=", switch_no), ('location', '=', location_id)])

    @api.multi
    def is_switch(self):
        '''
        是否为switch
        :return:
        '''
        return True

    @api.multi
    def get_train(self):
        '''
        取得占压的车辆, 取最后进去的车
        :return:
        '''
        self.ensure_one()
        record = self.env["metro_park_dispatch.cur_train_manage"] \
            .search([('cur_switch', '=', self.id)], order="write_date desc")
        return record

    @api.multi
    def get_connected_un_hold_neighbors_switch(self, black_switches):
        '''
        取得相连的道岔，用于未占压的情况
        :return:
        '''
        self.ensure_one()
        rst = []
        if self.positive_switch \
                and self.pos == 1 \
                and self.positive_switch.name not in black_switches:
            rst.append(self.positive_switch)

        if self.negative_switch \
                and self.pos_reverse == 1 \
                and self.negative_switch.name not in black_switches:
            rst.append(self.negative_switch)

        if self.header_switch \
                and self.header_switch.name not in black_switches:
            rst.append(self.header_switch)
        return rst

    @api.multi
    def get_connected_switch_names(self, switch_names, all_switches, hold=True):
        '''
        取得相连的道岔, 同正同反的当成一个来处理, 所以必需在本次的占压信息里面，肯定是同时发过来的
        :return:
        '''
        for record in self:
            if hold:
                tmp_switches = \
                    record.get_hold_neighbors_switch(switch_names)
            else:
                tmp_switches = \
                    record.get_connected_un_hold_neighbors_switch(switch_names)

            for switch in tmp_switches:
                if switch.name not in switch_names and switch.name in all_switches:
                    switch_names.append(switch.name)
                    switch.get_connected_switch_names(switch_names, all_switches, hold)

    @api.model
    def update_train_info(self, location_id, switch_name, hold_switches, black_switches, hold):
        '''
        更新车辆信息, 道岔有可能会两边都占压
        :param location_id:
        :param switch_name:
        :param hold_switches:
        :param black_switches:
        :param hold:
        :return:
        '''
        record = self.search(
            [('name', '=', switch_name), ('location', '=', location_id)])
        track_obj = self.env['metro_park_dispatch.train_track']
        if record:

            # 取得所有同正同反的道岔
            switch_names = [record.name]
            # 取得相联连的道岔
            record.get_connected_switch_names(
                switch_names, hold_switches, hold)
            black_switches += switch_names

            if hold:
                trains = []
                neighbours = []
                for switch_name in switch_names:
                    tmp_record = self.search(
                        [('name', '=', switch_name), ('location', '=', location_id)])
                    neighbours += tmp_record.get_hold_neighbors(black_switches)

                # 有可能出现两个邻居都有车
                all_switches = self.search(
                    [('hold', '=', 1), ('location.id', '=', location_id)])
                all_switch_cache = {
                    switch.name: switch for switch in all_switches}
                neighboar_has_trains = 0
                for neighbour in neighbours:
                    # 取得邻居连接的连接的多个道岔
                    if neighbour.is_switch():
                        neighbour_trains = []
                        sub_neighbour_names = []
                        neighbour.get_connected_switch_names(
                            sub_neighbour_names, all_switches.mapped("name"), True)
                        for name in sub_neighbour_names:
                            switch = all_switch_cache[name]
                            tmp_trains = switch.get_train()
                            neighbour_trains += tmp_trains
                            if len(tmp_trains) > 0 and switch.is_switch():
                                black_switches.append(switch.name)
                        if len(neighbour_trains) > 0:
                            neighboar_has_trains += 1
                        trains += neighbour_trains
                    else:
                        tmp_trains = neighbour.get_train()
                        if len(tmp_trains) > 0:
                            neighboar_has_trains += 1
                        trains += tmp_trains

                    if neighbour.is_switch():
                        black_switches.append(neighbour.name)

                # 两边都有车，暂不做处理
                if neighboar_has_trains > 1:
                    return

                # if len(trains) == 0:
                #     LogManage.put_log(
                #         content='在相邻位置上没有找到车,使用ats进行推断-MDIAS', mode='cur_train_position_change')
                #     # 转换成为轨道区段名称
                #     ats_position = record.rail_sec_id.no
                #     train = self.env["metro_park_dispatch.cur_train_manage"].search(
                #         [('ats_position', 'in', [ats_position, ats_position.replace("/", "_")])])
                #     if train:
                #         LogManage.put_log(
                #             content='道岔处理根据ats推断成功-MDIAS', mode='cur_train_position_change')
                #         trains.append(train)

                # 对所有的车更新位置
                for train in trains:
                    black_switches.append(record.id)
                    if record.is_switch():
                        train.cur_switch = record.id
                        train.cur_rail = False
                        LogManage.put_log(content='车{name}到达{position} MDIAS'.format(
                            name=train["train_no"],
                            position=record["name"]),
                            mode='cur_train_position_change')
                    else:
                        train.cur_rail = record.id
                        train.cur_switch = False
                        LogManage.put_log(content='车{name}到达{position} MDIAS'.format(
                            name=train["train_no"],
                            position=record["no"]),
                            mode='cur_train_position_change')
                    # 提交，线程操作有可能不同步
                    self._cr.commit()
                    train.notify_train_position_changed()
                    track_obj.update_track(train.id, switch_id=record.id)
            else:
                neighbours = []
                trains = []
                for switch_name in switch_names:
                    tmp_record = self.search(
                        [('name', '=', switch_name), ('location', '=', location_id)])
                    # 需要将车转移给占压的区段
                    neighbours += tmp_record.get_hold_neighbors(black_switches)
                    trains += self.env["metro_park_dispatch.cur_train_manage"] \
                        .search([('cur_switch', '=', tmp_record.id)], limit=1)

                # 如果是只有一边有占压，那么显示然车跑到一边去了
                if len(neighbours) == 1:
                    neighbour = neighbours[0]
                    for train in trains:
                        if neighbour.is_switch():
                            _logger.info('set train position {train} -> {position}'.format(
                                train=train.train_no, position=neighbour.name))
                            train.cur_switch = neighbour.id
                            train.cur_rail = False
                            LogManage.put_log(content='车{name}到达{position} MDIAS'.format(
                                name=train["train_no"],
                                position=neighbour["name"]),
                                mode='cur_train_position_change')
                        else:
                            train.cur_rail = neighbour.id
                            train.cur_switch = False
                            _logger.info('set train position {train} -> {position}'.format(
                                train=train.train_no, position=neighbour.no))
                            LogManage.put_log(content='车{name}到达{position} MDIAS'.format(
                                name=train["train_no"],
                                position=neighbour["no"]),
                                mode='cur_train_position_change')
                        # 提前提交，notify是在线程里处理，有可能还没有提交过去
                        self._cr.commit()
                        train.notify_train_position_changed()
                for train in trains:
                    track_obj.update_track(train.id, switch_id=record.id, level=True)

