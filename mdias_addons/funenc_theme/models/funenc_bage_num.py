# -*- coding: utf-8 -*-

from odoo import models, api


class BadgeNum(models.Model):
    _name = 'funenc_theme_pub.bage_num'

    @api.model
    def get_badge_num(self):
        '''
        取得徽章, 各自应用里继承这个类，然后得写这个函数，返回形式如：
        :return:
        result = {}
        '''
        return []
