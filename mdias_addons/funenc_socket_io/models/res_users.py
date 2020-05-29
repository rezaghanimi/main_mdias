# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum
from odoo.models import DEFAULT_SERVER_DATETIME_FORMAT


class Users(models.Model):

    _inherit = 'res.users'

    def post_bus_message(self, message, title='Title', msg_type='text',
                         to=None, callback_name=None, model_name=None, action=None):
        """
        :param message: 消息内容，支持html形式
        :param msg_type: text, html
        :param to: 消息接受者,None采用广播 @type user list, user id
        :param action: 按钮点击的action回调action
        :return:
        """
        message = {
            'message_title': title,
            'message_body': message,
            'message_type': msg_type,
            'action': action
        }

        self.trigger_up_event('bus_message', message, to=to,
                              callback_name=callback_name, model_name=model_name)
