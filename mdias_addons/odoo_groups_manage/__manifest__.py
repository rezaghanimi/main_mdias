# -*- coding: utf-8 -*-
{
    'name': "odoo_groups_manage",

    'summary': """
        odoo权限管理模块""",

    'description': """
        odoo权限管理模块，需要依赖与vue_template
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '0.1',

    'depends': ['base', 'vue_template_manager'],

    'qweb': [
        'static/xml/*.xml'
    ],
    'data': [
        'security/groups_data.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'views/assets.xml',
        'views/res_groups_view.xml',
        'views/res_users_view.xml',
        'views/menus.xml'
    ],
    'application': True
}
