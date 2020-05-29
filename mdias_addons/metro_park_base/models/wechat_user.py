# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WechatUserExtend(models.Model):
    '''
    用户属性扩展， 扩展增加用户所属场段
    '''
    _inherit = 'funenc.wechat.user'
    _track_log = True

    locations = fields.Many2many(string="所属场段",
                                 comodel_name="metro_park_base.location",
                                 column1="wechat_user_id",
                                 column2="location_id")
    cur_location = fields.Many2one(string="当前场段",
                                   comodel_name="metro_park_base.location")

    @api.model
    def get_cur_wechat_user(self):
        '''
        取得当前用微信户, 默认取值当前
        :return:
        '''
        return self.env.user.wx_user_ids[0]\
            if len(self.env.user.wx_user_ids) > 0 else None

    @api.model
    def get_cur_user_line(self):
        '''
        取得当前用户的线别, 那有可能属于多条线
        :return:
        '''
        wechat_user = self.get_cur_wechat_user()
        if wechat_user:
            return wechat_user.line

