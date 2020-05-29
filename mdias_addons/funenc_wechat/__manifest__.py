# -*- coding: utf-8 -*-
{
    'name': "funenc_wechat",
    'summary': """富能通企业微信模块""",
    'description': """富能通企业微信模块""",
    'author': "funenc",
    'website': "http://www.funenc.com",
    'depends': ['base', 'web'],
    'category': 'funenc',
    'version': '1.2',
    'data': [
        'views/web_assets.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/log_view.xml',
        'views/account_view.xml',
        'views/user_view.xml',
        'views/department_view.xml',
        'views/app.xml',
        'views/render_template.xml',
        'views/property.xml',
        'views/menu.xml',
        'data/account.xml',
        'views/res_config_settings.xml'
    ],
    'qweb': ['static/xml/*.xml'],
    'application': True
}