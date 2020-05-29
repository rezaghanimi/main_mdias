
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from ..model_extend import LogManage

LogManage.register_type('LOGIN', '登陆')


class ResUsers(models.Model):

    _inherit = 'res.users'

    @classmethod
    def _login(cls, db, login, password):
        res = super(ResUsers, cls)._login(db, login, password)
        LogManage.put_log(content="用户%s登陆账号" % login, mode="LOGIN")
        return res
