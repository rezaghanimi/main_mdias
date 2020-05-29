
# -*- coding: utf-8 -*-

from odoo import models, api


class Mdiastest(models.Model):
    '''
    测试模型
    '''
    _name = 'mdias.test'

    @api.model
    def send_msg_to_client(self):
        '''
        测试 web socket
        :return:
        '''
        self.env["funenc.socket_io"].send_broadcast_msg({
            "msg_type": "say_hello_word",
            "msg_data": {
                "test_data": "test_data"
            }
        })
