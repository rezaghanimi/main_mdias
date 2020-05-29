
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pendulum


class TestClient(models.Model):
    '''
    测试客户端
    '''
    _name = 'mdias_test.test_client'
    
    msg = fields.Char(string='消息')


class User(models.Model):

    _inherit = 'res.users'

    @api.model
    def test_call_message(self, *args, **kwargs):
        print('call  succeed ')
        pass

    @api.model
    def message_test(self):
        template = self.env.ref('mdias_test.message_test_template', raise_if_not_found=True)
        content = template.render({
            'message': {
                'type_description': '测试消息',
                'content': '这是一条测试消息',
                'remark': '消息类型: Qweb,html模板',
                'data': pendulum.now().strftime(models.DEFAULT_SERVER_DATETIME_FORMAT)
            },
        }, engine='ir.qweb', minimal_qcontext=True, ).decode()
        action = {
            'name': '查看用户',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'res_model': 'res.users',
            'target': 'new',
            'views': [(self.env.ref('base.change_password_wizard_view').id, 'form')],
            'class_names': 'btn-sm btn-link',
        }
        for i in range(10):
            self.post_bus_message(
                content, to=self.env.user.id, model_name=self._name,
                callback_name='test_call_message', action=action)

    @api.model
    def test_message_to_server(self):
        self.env['funenc.socket_info_send'].post_message_to_server('测试消息to SERVER')

