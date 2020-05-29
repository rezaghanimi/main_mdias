
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

'''
// 信号状态
struct SignalStatus {
    BYTE red_blue: 1;             // 红/兰
    BYTE white : 1;               // 白灯
    BYTE yellow : 1;              // 黄灯
    BYTE yellow_twice : 1;        // 双黄
    BYTE green_yellow : 1;        // 绿黄
    BYTE green : 1;               // 绿灯
    BYTE red_white : 1;           // 红白
    BYTE green_twice : 1;         // 双绿

    BYTE train_btn_flash : 1;     // 列车按钮闪亮
    BYTE ligth_broken_wire : 1;   // 灯丝断丝
    BYTE shunt_btn_light : 1;     // 调车按钮闪亮
    BYTE flash : 1;               // 闪光
    BYTE reversed : 1;            // 0
    BYTE reversed2 : 1;           // 0
    BYTE delay_180s : 1;          // 延时3分钟
    BYTE delay_30s : 1;           // 延时30秒
                                  
    BYTE guaid_10s : 1;           // 引导10s
    BYTE ramp_delay_lock : 1;     // 坡道延时解锁
    BYTE closed : 1;              // 封闭
    BYTE notice : 5;              // 提示信息
};
'''


class Signals(models.Model):
    '''
    信号机
    '''
    _name = 'metro_park_base.signals'
    _description = '信号机'
    _track_log = True

    name = fields.Char(string='名称')
    location = fields.Many2one(string="位置",
                               comodel_name="metro_park_base.location")
    remark = fields.Char(string='备注')

    index = fields.Integer(string="码位序号")
    da_start = fields.Integer(string="调车始端")
    guaid_flash = fields.Integer(string="引导闪烁")
    signal_end = fields.Integer(string="信号终端")
    type = fields.Integer(string="类型编号")

    # 联锁相关信息
    red_blue = fields.Integer(string="红/兰")
    white = fields.Integer(string="白灯")
    yellow = fields.Integer(string="黄灯")
    yellow_twice = fields.Integer(string="双黄")
    green_yellow = fields.Integer(string="绿黄")
    green = fields.Integer(string="绿灯")

    red_white = fields.Integer(string="红白")
    green_twice = fields.Integer(string="双绿")

    train_btn_flash = fields.Integer(string="列车按钮闪亮")
    ligth_broken_wire = fields.Integer(string="灯丝断丝")
    shunt_btn_light = fields.Integer(string="调车按钮闪亮")
    close_lock = fields.Integer(string="接近锁闭")

    reversed = fields.Integer(string="预留1")
    reversed2 = fields.Integer(string="预留2")

    guaid_10s = fields.Integer(string="引导10s")
    delay_30s = fields.Integer(string="延时30秒")
    delay_180s = fields.Integer(string="延时3分钟")

    ramp_delay_lock = fields.Integer(string="坡道延时解锁")
    closed = fields.Integer(string="封闭")
    notice = fields.Char(string="提示信息")

    @api.model
    def update_status(self, location, data):
        '''
        更新状态
        :param data:
        :param location:
        :return:
        '''
        name = data["name"]
        record = self.search(
            [("name", "=", name), ('location', '=', location)])
        if record:
            record.write(data)
        else:
            logging.info("没有找到信号机{name}".format(name=name))
