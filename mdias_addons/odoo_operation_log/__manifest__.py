# -*- coding: utf-8 -*-
{
    'name': "odoo_operation_log",

    'summary': """
    日志""",

    'description': """
        日志管理软件,在数据发生变更时候自动保存数据变化
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",
    'category': 'funenc',
    'version': '0.1',
    'depends': ['base', 'vue_template_manager'],
    'data': [

        'security/assess_group.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/ir_cron.xml',
        'views/log_config.xml',
        'views/menus.xml'

    ],
    'application': True,
    'qweb': ['static/src/xml/operation_list.xml', ]
}
