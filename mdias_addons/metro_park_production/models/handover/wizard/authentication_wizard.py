# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessDenied


class HandoverLoginWizard(models.TransientModel):
    _abstract = False
    _register = True

    _name = 'metro_park_production.wizard.authentication'

    login_account = fields.Char()
    password = fields.Char()
    context = fields.Text()

    @api.multi
    def login(self):
        dbname = self.env.cr.dbname
        login = self.login_account
        password = self.password
        user = self.env['res.users'].search([('login', '=', login)])
        if not user:
            raise UserError('用户不存在,请确认账号是否正确')
        try:
            uid = user._login(dbname, login, password)
            handover_id = self.env.context.get('handover_id', False)
            handover_type = self.env.context.get('handover_type', False)
            if not (handover_id and handover_type):
                raise UserError('请刷新页面重重新认证')
            model = 'metro_park_production.handover.%s' % handover_type
            record = self.env[model].browse(handover_id)
            record.write({
                'accept_user': uid,
                'handover_date': datetime.now(),
                'state': 'handed'
            })
        except AccessDenied:
            raise UserError('账号密码错误')
