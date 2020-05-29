# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import UserError


class PageHtml(models.Model):
    '''
    大屏投放页面
    '''
    _name = 'metro_park_production.screen.page'
    _order = "index asc"

    index = fields.Integer(string="序号", default=0, required=True)
    name = fields.Char(string="名称", required=True)
    location = fields.Many2one(comodel_name='metro_park_base.location', string='位置')
    html_value = fields.Html(string='页面数据')

    @api.model
    def jump_location_pages(self):
        '''
        跳转到当前用户所属位置的大屏页面列表
        :return:
        '''
        location_id = self.env.user.cur_location
        if not location_id:
            raise UserError('用户未选择位置信息,请在设置中配置用户所属位置及当前位置!')

        tree_id = self.env.ref(
            'metro_park_production.big_screen_page_list').id
        form_id = self.env.ref(
            'metro_park_production.big_screen_page_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "context": {
                "default_location_id": location_id
            },
            "res_model": "metro_park_production.screen.page",
            "name": "大屏页面",
            "views": [[tree_id, "tree"], [form_id, "form"]]
        }

    @api.multi
    def edit_html_value(self):
        '''
        更新html页面
        :return:
        '''
        return {
            "type": "ir.actions.act_window",
            "res_id": self.id,
            "res_model": "metro_park_production.screen.page",
            'view_mode': 'form',
            'target': "new",
            'context': {},
            "views": [[
                self.env.ref('metro_park_production.big_screen_page_edit_form').id, "form"]]
        }

    @api.model
    def publish_big_screen(self):
        '''
        发布大屏
        :return:
        '''
        location = self.env.user.cur_location
        if not location:
            raise UserError('用户未选择位置信息,请在设置中配置用户所属位置及当前位置!')

        url = '/metro_park_production/static/large_screen/screen_display.html?location_id=%s' % location.id
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }

    @api.model
    def request_data(self, location_id):
        '''
            为了兼容原有的接口
            :param mid:
            :return:
        '''
        model = self.env["metro_park_production.screen.page"]
        records = model.sudo().search([('location', '=', int(location_id))])
        if not records:
            return []

        val = records.read(['html_value'])
        return {
            'pages': val,
            'background': 'black'
        }
